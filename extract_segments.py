# -*- coding: utf-8 -*-
"""
sports-industry-monitor — Phase 2: 공시 추출 (v5.1)
v5.1: 신규 종목 반영 — 울버린(WWW)·컬럼비아(COLM) 추출 대상 추가,
      미즈노·요넥스·골드윈(일본)·안타·리닝(홍콩)·푸마(독일)는 EDGAR 미대상 표기
v5: 전년 동기 수치(prev_revenue) 추출 — 공시 비교표에 명시된 경우만, 미기재는
    null(대시보드에서 YoY 역산 + [역산] 표기). schema_v=2로 캐시 자동 갱신.
v4: 첨부 목록 폴백(index.json 미비 공시 대응) / v3: 실적 문서 내용 검증
출력: docs/segments.json — §29-D: 명시 수치만 추출, 미기재는 null
동일 공시(accession)+동일 스키마는 재추출하지 않음(캐시)
"""

import os
import re
import json
import html
import time
import datetime
import requests

CONTACT_EMAIL = "여기에이메일"   # 반드시 영문 이메일로 교체

_safe_email = CONTACT_EMAIL.encode("ascii", "ignore").decode() or "contact@example.com"
UA = {"User-Agent": f"sports-industry-monitor ({_safe_email})"}
API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
KST = datetime.timezone(datetime.timedelta(hours=9))
SCHEMA_V = 2   # 추출 스키마 버전 (필드 변경 시 +1 → 캐시 자동 무효화)

US_TICKERS = ["NKE", "ONON", "DECK", "AS", "LULU", "BIRK",
              "CROX", "VFC", "UAA", "WWW", "COLM",
              "DKS", "ASO"]
NON_US = {"ADS.DE": "EDGAR 미대상(독일 상장)",
          "PUM.DE": "EDGAR 미대상(독일 상장)",
          "7936.T": "EDGAR 미대상(일본 상장)",
          "8022.T": "EDGAR 미대상(일본 상장)",
          "7906.T": "EDGAR 미대상(일본 상장)",
          "8111.T": "EDGAR 미대상(일본 상장)",
          "2020.HK": "EDGAR 미대상(홍콩 상장)",
          "2331.HK": "EDGAR 미대상(홍콩 상장)",
          "JD.L": "EDGAR 미대상(영국 상장)"}

SEG_PATH = "docs/segments.json"


def sec_get(url, is_json=True):
    time.sleep(0.4)
    r = requests.get(url, headers=UA, timeout=60)
    r.raise_for_status()
    return r.json() if is_json else r.text


def load_cik_map():
    data = sec_get("https://www.sec.gov/files/company_tickers.json")
    m = {}
    for v in data.values():
        m[v["ticker"].upper()] = int(v["cik_str"])
    return m


def strip_html(text):
    text = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", text,
                  flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    return re.sub(r"[ \t\xa0]+", " ", text)


def looks_like_earnings(txt):
    """실적자료 내용 검증 (§29-D: 문서 선택 오류 방어)"""
    t = txt.lower()
    has_rev = re.search(r"net (sales|revenue)|total revenue|revenues", t)
    has_period = re.search(
        r"(first|second|third|fourth) quarter|fiscal (year|20)|quarter ended|"
        r"three months ended|six months ended|nine months ended|year ended", t)
    has_fin = re.search(
        r"gross (profit|margin)|operating income|income statement|"
        r"balance sheet|earnings per share|diluted", t)
    return bool(has_rev and has_period and has_fin)


def _bad_name(n):
    """index 파일·XBRL 렌더 파일(R1.htm 등) 제외"""
    ln = n.lower()
    return ("index" in ln) or re.fullmatch(r"r\d+\.html?", ln)


def list_filing_docs(cik, nod, primary):
    """공시 첨부 htm 목록 [(이름, 크기)].
    1차: index.json / 2차 폴백: 디렉터리 HTML에서 파일명 직접 추출"""
    names = []
    try:
        idx = sec_get(
            f"https://www.sec.gov/Archives/edgar/data/{cik}/{nod}/index.json")
        for it in idx.get("directory", {}).get("item", []):
            n = it["name"]
            if (n.lower().endswith((".htm", ".html"))
                    and n != primary and not _bad_name(n)):
                names.append((n, int(it.get("size") or 0)))
    except Exception:
        pass
    try:
        listing = sec_get(
            f"https://www.sec.gov/Archives/edgar/data/{cik}/{nod}/",
            is_json=False)
        for n in re.findall(r'href="[^"]*?([\w.-]+\.html?)"', listing, re.I):
            if (n != primary and not _bad_name(n)
                    and all(n != x for x, _ in names)):
                names.append((n, 0))
    except Exception:
        pass
    return names


def find_latest_filing(cik):
    """최신 '실적' 공시 반환. 최근 8-K/6-K 15건 최신순, 첨부 3개까지 내용 검증."""
    sub = sec_get(f"https://data.sec.gov/submissions/CIK{cik:010d}.json")
    rec = sub["filings"]["recent"]
    forms = rec["form"]
    accs = rec["accessionNumber"]
    dates = rec["filingDate"]
    docs = rec["primaryDocument"]

    checked = 0
    for i in range(len(forms)):
        if forms[i] not in ("8-K", "6-K"):
            continue
        checked += 1
        if checked > 15:
            break
        acc = accs[i]
        nod = acc.replace("-", "")
        try:
            names = list_filing_docs(cik, nod, docs[i])
            if not names:
                print(f"  - {forms[i]} {dates[i]}: 첨부 htm 없음, 건너뜀")
                continue
            prio = [nm for nm in names
                    if re.search(r"ex.?99|press|earn|release|result",
                                 nm[0], re.I)]
            pool = prio if prio else names
            pool.sort(key=lambda nm: nm[1], reverse=True)
            found = None
            for nm, _sz in pool[:3]:
                url = (f"https://www.sec.gov/Archives/edgar/data/{cik}/{nod}/"
                       f"{nm}")
                txt = strip_html(sec_get(url, is_json=False))
                if len(txt) < 3000:
                    print(f"  - {forms[i]} {dates[i]} {nm}: "
                          f"본문 짧음({len(txt)}자)")
                    continue
                if not looks_like_earnings(txt):
                    print(f"  - {forms[i]} {dates[i]} {nm}: "
                          f"실적자료 아님(내용 검증 불통과), 건너뜀")
                    continue
                found = {"accession": acc, "text": txt, "url": url,
                         "source": f"{forms[i]} {dates[i]} {nm}"}
                break
            if found:
                return found
        except Exception as e:
            print(f"  - {forms[i]} {dates[i]}: 오류로 건너뜀: {str(e)[:100]}")
            continue

    for i in range(len(forms)):
        if forms[i] in ("10-Q", "10-K", "20-F"):
            acc = accs[i]
            nod = acc.replace("-", "")
            url = (f"https://www.sec.gov/Archives/edgar/data/{cik}/{nod}/"
                   f"{docs[i]}")
            txt = strip_html(sec_get(url, is_json=False))
            return {"accession": acc, "text": txt, "url": url,
                    "source": f"{forms[i]} {dates[i]}"}
    return None


def cap_text(txt):
    if len(txt) <= 160000:
        return txt
    return txt[:30000] + "\n...(중략)...\n" + txt[-130000:]


def claude_extract(ticker, name, doc_text):
    dks_extra = ""
    if ticker == "DKS":
        dks_extra = """
  "sub_segments": [
    {"name": "DICK'S", "revenue": number|null, "prev_revenue": number|null,
     "yoy_pct": number|null, "segment_profit": number|null,
     "inventory": number|null},
    {"name": "Foot Locker", "revenue": number|null, "prev_revenue": number|null,
     "yoy_pct": number|null, "segment_profit": number|null,
     "inventory": number|null, "proforma_comp_pct": number|null}
  ],"""
    prompt = f"""You are a financial data extractor. The following is text from the latest
SEC earnings-related filing of {name} ({ticker}).

Extract ONLY figures that are EXPLICITLY stated in the document. Never compute,
estimate, or infer missing values — use null instead. Revenue figures in
MILLIONS of the reporting currency. yoy_pct = year-over-year growth in percent
for the most recent quarter (or fiscal year if only annual data is present).
prev_revenue = the PRIOR-YEAR comparative figure for the same period, ONLY if
it is explicitly stated in a comparative table or the text; otherwise null.

Respond with ONLY a JSON object, no markdown fences, no commentary:
{{
  "period": "string describing the reported period, e.g. 'Q1 FY26 ended 2026-08-31'",
  "prev_period": "string describing the prior-year comparative period, or null",
  "currency": "USD/CHF/etc or null",
  "regions": [
    {{"name": "North America|EMEA|Greater China|Asia Pacific|etc",
      "revenue": number|null, "prev_revenue": number|null, "yoy_pct": number|null}}
  ],
  "channels": [
    {{"name": "DTC|Wholesale|etc",
      "revenue": number|null, "prev_revenue": number|null, "yoy_pct": number|null}}
  ],{dks_extra}
  "notes": "one short sentence in Korean about data caveats, or null"
}}
If the document contains no regional breakdown, use an empty list for regions.
Same for channels. If the document is not an earnings report at all, return
{{"period": null, "prev_period": null, "currency": null, "regions": [],
"channels": [], "notes": "실적 문서 아님"}}

DOCUMENT:
{cap_text(doc_text)}"""

    r = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={"x-api-key": API_KEY,
                 "anthropic-version": "2023-06-01",
                 "content-type": "application/json"},
        json={"model": "claude-sonnet-4-6",
              "max_tokens": 2500,
              "messages": [{"role": "user", "content": prompt}]},
        timeout=180)
    r.raise_for_status()
    parts = r.json().get("content", [])
    text = "".join(p.get("text", "") for p in parts if p.get("type") == "text")
    text = re.sub(r"```json|```", "", text).strip()
    obj = json.loads(text)
    obj["schema_v"] = SCHEMA_V
    return obj


def main():
    if not API_KEY:
        print("[ERROR] ANTHROPIC_API_KEY 미설정")
        raise SystemExit(1)

    old = {"items": {}}
    if os.path.exists(SEG_PATH):
        try:
            with open(SEG_PATH, encoding="utf-8") as f:
                old = json.load(f)
        except Exception:
            pass
    old_items = old.get("items", {})

    out = {"generated_at":
           datetime.datetime.now(KST).strftime("%Y-%m-%d %H:%M KST"),
           "items": {}}

    for t, reason in NON_US.items():
        out["items"][t] = {"error": reason, "extract": None}

    cik_map = load_cik_map()

    for t in US_TICKERS:
        entry = {"accession": None, "source": None, "url": None,
                 "extract": None, "error": None}
        try:
            cik = cik_map.get(t)
            if not cik:
                entry["error"] = "CIK 미확인"
                out["items"][t] = entry
                continue
            print(f"{t}: 공시 탐색 중 ...")
            filing = find_latest_filing(cik)
            if not filing:
                entry["error"] = "실적 공시 미발견"
                out["items"][t] = entry
                continue
            entry["accession"] = filing["accession"]
            entry["source"] = filing["source"]
            entry["url"] = filing["url"]

            prev = old_items.get(t) or {}
            px = prev.get("extract") or {}
            if (prev.get("accession") == filing["accession"]
                    and px.get("schema_v") == SCHEMA_V
                    and (px.get("regions") or px.get("channels")
                         or px.get("sub_segments"))):
                entry["extract"] = px
                print(f"{t}: 동일 공시({filing['accession']}) → 캐시 사용")
            else:
                print(f"{t}: 신규 공시 추출 중 ... ({filing['source']})")
                entry["extract"] = claude_extract(t, t, filing["text"])
        except Exception as e:
            entry["error"] = str(e)[:200]
            print(f"[WARN] {t}: {e}")
        out["items"][t] = entry

    os.makedirs("docs", exist_ok=True)
    with open(SEG_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("saved", SEG_PATH)


if __name__ == "__main__":
    main()

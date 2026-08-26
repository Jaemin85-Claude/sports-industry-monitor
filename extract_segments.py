# -*- coding: utf-8 -*-
"""
sports-industry-monitor — Phase 2: 공시 추출
SEC EDGAR에서 최신 실적 공시(8-K/6-K 보도자료, 폴백: 10-Q/10-K/20-F)를 찾아
Claude API로 지역별·채널별 매출과 DKS 부문(딕스/풋락커) 분리 수치를 추출
출력: docs/segments.json
§29-D: 공시에 명시된 수치만 추출, 실패/미기재는 null → 대시보드 "미확인"
이미 추출한 공시(accession 동일)는 재추출하지 않음 → API 비용 최소화
"""

import os
import re
import json
import html
import time
import datetime
import requests

CONTACT_EMAIL = "nightsit7@gmail.com"   # SEC 접속 규정용 연락처 (실제 이메일로 교체)

UA = {"User-Agent": f"sports-industry-monitor ({CONTACT_EMAIL})"}
API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
KST = datetime.timezone(datetime.timedelta(hours=9))

# EDGAR 추출 대상 (미국 상장). 비대상은 NON_US에 사유 기재
US_TICKERS = ["NKE", "ONON", "DECK", "AS", "LULU", "BIRK",
              "CROX", "VFC", "UAA", "DKS", "ASO"]
NON_US = {"ADS.DE": "EDGAR 미대상(독일 상장)",
          "7936.T": "EDGAR 미대상(일본 상장)",
          "JD.L": "EDGAR 미대상(영국 상장)"}

SEG_PATH = "docs/segments.json"


def sec_get(url, is_json=True):
    time.sleep(0.4)  # SEC 요청 간격 준수
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


def find_latest_filing(cik):
    """최신 실적 공시 문서 텍스트와 메타 반환.
    우선순위: 8-K/6-K의 EX-99 보도자료 → 폴백: 10-Q/10-K/20-F 본문"""
    sub = sec_get(f"https://data.sec.gov/submissions/CIK{cik:010d}.json")
    rec = sub["filings"]["recent"]
    forms = rec["form"]
    accs = rec["accessionNumber"]
    dates = rec["filingDate"]
    docs = rec["primaryDocument"]

    # 1) 최근 8-K/6-K 최대 8건에서 EX-99 탐색
    tried = 0
    for i in range(len(forms)):
        if forms[i] not in ("8-K", "6-K"):
            continue
        tried += 1
        if tried > 8:
            break
        acc = accs[i]
        nod = acc.replace("-", "")
        try:
            idx = sec_get(
                f"https://www.sec.gov/Archives/edgar/data/{cik}/{nod}/index.json")
            items = idx.get("directory", {}).get("item", [])
            ex = [it for it in items
                  if re.search(r"ex.*99", it["name"], re.I)
                  and it["name"].lower().endswith((".htm", ".html"))]
            if not ex:
                continue
            ex.sort(key=lambda it: int(it.get("size") or 0), reverse=True)
            url = (f"https://www.sec.gov/Archives/edgar/data/{cik}/{nod}/"
                   f"{ex[0]['name']}")
            txt = strip_html(sec_get(url, is_json=False))
            if len(txt) < 3000:   # 실적자료로 보기엔 너무 짧으면 다음 후보
                continue
            return {"accession": acc, "text": txt, "url": url,
                    "source": f"{forms[i]} {dates[i]} {ex[0]['name']}"}
        except Exception:
            continue

    # 2) 폴백: 최신 10-Q / 10-K / 20-F 본문
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
    """길면 앞 30k + 뒤 130k (부문 주석은 보통 후반부)"""
    if len(txt) <= 160000:
        return txt
    return txt[:30000] + "\n...(중략)...\n" + txt[-130000:]


def claude_extract(ticker, name, doc_text):
    dks_extra = ""
    if ticker == "DKS":
        dks_extra = """
  "sub_segments": [
    {"name": "DICK'S", "revenue": number|null, "yoy_pct": number|null,
     "segment_profit": number|null, "inventory": number|null},
    {"name": "Foot Locker", "revenue": number|null, "yoy_pct": number|null,
     "segment_profit": number|null, "inventory": number|null,
     "proforma_comp_pct": number|null}
  ],"""
    prompt = f"""You are a financial data extractor. The following is text from the latest
SEC earnings-related filing of {name} ({ticker}).

Extract ONLY figures that are EXPLICITLY stated in the document. Never compute,
estimate, or infer missing values — use null instead. Revenue figures in
MILLIONS of the reporting currency. yoy_pct = year-over-year growth in percent
for the most recent quarter (or fiscal year if only annual data is present).

Respond with ONLY a JSON object, no markdown fences, no commentary:
{{
  "period": "string describing the reported period, e.g. 'Q1 FY26 ended 2026-08-31'",
  "currency": "USD/CHF/etc or null",
  "regions": [
    {{"name": "North America|EMEA|Greater China|Asia Pacific|etc",
      "revenue": number|null, "yoy_pct": number|null}}
  ],
  "channels": [
    {{"name": "DTC|Wholesale|etc", "revenue": number|null, "yoy_pct": number|null}}
  ],{dks_extra}
  "notes": "one short sentence in Korean about data caveats, or null"
}}
If the document contains no regional breakdown, use an empty list for regions.
Same for channels. If the document is not an earnings report at all, return
{{"period": null, "currency": null, "regions": [], "channels": [], "notes": "실적 문서 아님"}}

DOCUMENT:
{cap_text(doc_text)}"""

    r = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={"x-api-key": API_KEY,
                 "anthropic-version": "2023-06-01",
                 "content-type": "application/json"},
        json={"model": "claude-sonnet-4-6",
              "max_tokens": 2000,
              "messages": [{"role": "user", "content": prompt}]},
        timeout=180)
    r.raise_for_status()
    parts = r.json().get("content", [])
    text = "".join(p.get("text", "") for p in parts if p.get("type") == "text")
    text = re.sub(r"```json|```", "", text).strip()
    return json.loads(text)


def main():
    if not API_KEY:
        print("[ERROR] ANTHROPIC_API_KEY 미설정")
        raise SystemExit(1)

    # 기존 결과 로드 (accession 캐시)
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

    # 비미국 상장 — 사유 명시
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
            filing = find_latest_filing(cik)
            if not filing:
                entry["error"] = "실적 공시 미발견"
                out["items"][t] = entry
                continue
            entry["accession"] = filing["accession"]
            entry["source"] = filing["source"]
            entry["url"] = filing["url"]

            prev = old_items.get(t) or {}
            if (prev.get("accession") == filing["accession"]
                    and prev.get("extract")):
                entry["extract"] = prev["extract"]
                print(f"{t}: 동일 공시({filing['accession']}) → 캐시 사용")
            else:
                print(f"{t}: 신규 공시 추출 중 ... ({filing['source']})")
                entry["extract"] = claude_extract(
                    t, t, filing["text"])
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

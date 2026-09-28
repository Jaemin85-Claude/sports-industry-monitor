# -*- coding: utf-8 -*-
"""
sports-industry-monitor — Phase 6: DART 국내 법인 실적 (v1)
프로브(2026-09-28)로 확정한 corp_code·경로만 사용 (§검증 우선):
  - route "api": 사업보고서 제출 법인 → 단일회사 주요계정 API(fnlttSinglAcnt)
  - route "doc": 감사보고서만 내는 외감 법인 → 공시서류 원본파일(document.xml) → Claude 추출
  - route "none": 공시 미발견 → 화면에 사유 표기
당기·전기 매출액/영업이익/당기순이익(원) → docs/kr_domestic.json 갱신
캐시: 같은 접수번호(rcept_no)는 재추출하지 않음 → 연 1회 신규 공시분만 비용 발생
§29-D: 공시에 명시된 수치만, 실패·미기재는 null(화면 '미확인')
"""

import os
import io
import re
import json
import time
import zipfile
import datetime
import requests

DART_KEY = os.environ.get("DART_API_KEY", "")
ANTHROPIC_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
BASE = "https://opendart.fss.or.kr/api"
UA = {"User-Agent": "sports-industry-monitor dart"}
KST = datetime.timezone(datetime.timedelta(hours=9))
OUT_PATH = "docs/kr_domestic.json"
YEARS_BACK = 3
MAX_DOC_CHARS = 70000

# ── 법인 정의 (프로브 확정) ─────────────────────────────
# id, 표시명, 유형, 연결 글로벌 티커, corp_code, 경로, 결산월, 주석
ENTITIES = [
    ("nike_kr",     "나이키코리아",        "글로벌 브랜드 국내법인", "NKE",    "01503133", "doc",  5,  "유한회사 — 5월 결산"),
    ("adidas_kr",   "아디다스코리아",      "글로벌 브랜드 국내법인", "ADS.DE", "00148133", "none", 12, "DART 공시 미발견(2026-09 조사) — 재조사 예정"),
    ("asics_kr",    "아식스코리아",        "글로벌 브랜드 국내법인", "7936.T", "00664385", "doc",  12, "12월 결산"),
    ("puma_kr",     "푸마코리아",          "글로벌 브랜드 국내법인", "PUM.DE", "01471250", "doc",  12, "유한회사 — K-IFRS"),
    ("descente_kr", "데상트코리아",        "글로벌 브랜드 국내법인", None,     "00411154", "doc",  12, "일본 본사 상장폐지(2025.1) — 국내 법인은 DART로 추적"),
    ("nb_eland",    "뉴발란스(이랜드월드)", "글로벌 브랜드 국내법인", None,     "00207108", "api",  12, "라이선스 — 이랜드월드 법인 전체 수치(뉴발란스 부문 분리 불가)"),
    ("abcmart_kr",  "에이비씨마트코리아",  "국내 유통(비상장)",      None,     "00496340", "doc",  12, "일본 ABC-Mart 자회사, 신발 멀티숍 1위"),
    ("shoemarker",  "슈마커코리아",        "국내 유통(비상장)",      None,     "00396402", "none", 12, "DART 공시 미발견(2026-09 조사) — 외감 기준 미달 가능성"),
    ("musinsa",     "무신사",              "국내 유통(비상장)",      None,     "01137727", "api",  12, "온라인 패션 플랫폼 — 2024년부터 사업보고서 제출, 거래액≠매출"),
    ("k2_kr",       "K2코리아",            "국내 브랜드(비상장)",    None,     "00407063", "doc",  12, "K2·아이더·다이나핏"),
    ("blackyak",    "비와이엔블랙야크",    "국내 브랜드(비상장)",    None,     "00520850", "doc",  12, "블랙야크·나우 (별도 상장사 블랙야크아이앤씨 478560 존재)"),
    ("nepa",        "네파",                "국내 브랜드(비상장)",    None,     "00932930", "doc",  12, "아웃도어"),
    ("shinsung",    "신성통상(탑텐)",      "국내 브랜드(비상장)",    None,     "00136341", "api",  6,  "2025년 자진 상장폐지 — 6월 결산, 사업보고서는 계속 제출"),
]


def log(msg):
    print(msg, flush=True)


def dart(url, params, as_bytes=False, timeout=90):
    params = dict(params, crtfc_key=DART_KEY)
    r = requests.get(url, params=params, headers=UA, timeout=timeout)
    r.raise_for_status()
    return r.content if as_bytes else r.json()


def to_int(s):
    if s in (None, "", "-"):
        return None
    try:
        return int(str(s).replace(",", "").replace(" ", ""))
    except ValueError:
        return None


# ── 경로 A: 구조화 API ──────────────────────────────────
ACCOUNT_MAP = {
    "rev": ["매출액", "수익(매출액)", "영업수익", "매출"],
    "op":  ["영업이익", "영업이익(손실)", "영업손익"],
    "ni":  ["당기순이익", "당기순이익(손실)", "당기순손익", "당기순손실"],
}


def fetch_api_years(corp_code, fy_end_month, years):
    """연도별 별도(OFS) 우선, 없으면 연결(CFS). 반환 {end: {rev, op, ni, source}}"""
    out = {}
    for y in years:
        try:
            data = dart(f"{BASE}/fnlttSinglAcnt.json", {
                "corp_code": corp_code, "bsns_year": str(y), "reprt_code": "11011"})
        except Exception as e:
            log(f"    {y}: API 오류 {str(e)[:80]}")
            continue
        if data.get("status") != "000":
            log(f"    {y}: {data.get('status')} {data.get('message')}")
            continue
        rows = data.get("list", [])
        for fs in ("OFS", "CFS"):
            sub = [r for r in rows if r.get("fs_div") == fs]
            if not sub:
                continue
            rec = {"rev": None, "op": None, "ni": None,
                   "source": f"사업보고서 {y} ({'별도' if fs == 'OFS' else '연결'}) rcept={sub[0].get('rcept_no')}",
                   "rcept_no": sub[0].get("rcept_no")}
            for key, names in ACCOUNT_MAP.items():
                for r in sub:
                    if (r.get("account_nm") or "").replace(" ", "") in [n.replace(" ", "") for n in names]:
                        rec[key] = to_int(r.get("thstrm_amount"))
                        break
            if rec["rev"] is not None:
                end = f"{y}-{fy_end_month:02d}-{'30' if fy_end_month in (4, 6, 9, 11) else '31'}"
                if fy_end_month == 2:
                    end = f"{y}-02-28"
                out[end] = rec
                log(f"    {y} {fs}: 매출 {rec['rev']:,} / 영업이익 {rec['op']} / 순이익 {rec['ni']}")
                break
    return out


# ── 경로 B: 감사보고서 원본 + Claude 추출 ─────────────────
def list_audit_reports(corp_code):
    bgn = (datetime.date.today() - datetime.timedelta(days=365 * YEARS_BACK + 60)).strftime("%Y%m%d")
    data = dart(f"{BASE}/list.json", {
        "corp_code": corp_code, "bgn_de": bgn,
        "page_count": 100, "sort": "date", "sort_mth": "desc"})
    if data.get("status") != "000":
        return []
    out = []
    for it in data.get("list", []):
        nm = it.get("report_nm") or ""
        if "감사보고서" in nm and "연결" not in nm and "정정" not in nm:
            out.append((it.get("rcept_no"), it.get("rcept_dt"), nm))
    return out


def fetch_document_text(rcept_no):
    raw = dart(f"{BASE}/document.xml", {"rcept_no": rcept_no}, as_bytes=True, timeout=120)
    if raw[:2] != b"PK":
        raise RuntimeError("원본이 zip이 아님")
    z = zipfile.ZipFile(io.BytesIO(raw))
    name = max(z.namelist(), key=lambda n: z.getinfo(n).file_size)
    content = z.read(name)
    txt = None
    for enc in ("utf-8", "euc-kr", "cp949"):
        try:
            txt = content.decode(enc)
            break
        except Exception:
            continue
    if txt is None:
        raise RuntimeError("디코딩 실패")
    plain = re.sub(r"<[^>]+>", " ", txt)
    plain = re.sub(r"\s+", " ", plain)
    # 손익계산서 부근 우선 포함: 앞부분(회사명·기간) + 손익계산서 창
    idx = plain.find("손익계산서")
    if len(plain) > MAX_DOC_CHARS and idx > 20000:
        plain = plain[:15000] + " ...(중략)... " + plain[idx - 2000: idx - 2000 + (MAX_DOC_CHARS - 15000)]
    return plain[:MAX_DOC_CHARS]


def claude_extract(name, text):
    prompt = f"""You are extracting figures from a Korean statutory audit report (감사보고서)
of {name}. Find the income statement (손익계산서 / 포괄손익계산서) and extract, for the
CURRENT period (당기) and the PRIOR period (전기):
- period end date (YYYY-MM-DD)
- 매출액 (or 수익(매출액), 영업수익) — total revenue
- 영업이익 (영업이익(손실)) — operating income; losses as negative
- 당기순이익 (당기순이익(손실)) — net income; losses as negative

Amounts must be in KRW units of 원 (convert if the statement says 단위: 천원 or 백만원).
Use ONLY figures explicitly stated. If a figure is not stated, use null.

Respond with ONLY a JSON object, no markdown fences:
{{
  "unit_note": "단위 표기 그대로, 예: 단위: 원",
  "current": {{"end": "YYYY-MM-DD", "rev": number|null, "op": number|null, "ni": number|null}},
  "prior":   {{"end": "YYYY-MM-DD", "rev": number|null, "op": number|null, "ni": number|null}}
}}

DOCUMENT:
{text}"""
    r = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={"x-api-key": ANTHROPIC_KEY, "anthropic-version": "2023-06-01",
                 "content-type": "application/json"},
        json={"model": "claude-sonnet-4-6", "max_tokens": 800,
              "messages": [{"role": "user", "content": prompt}]},
        timeout=180)
    r.raise_for_status()
    parts = r.json().get("content", [])
    txt = "".join(p.get("text", "") for p in parts if p.get("type") == "text")
    txt = re.sub(r"```json|```", "", txt).strip()
    return json.loads(txt)


def fetch_doc_years(name, corp_code, cached):
    """cached: {rcept_no: {end: rec}} 기존 추출. 반환 {end: rec}, 사용된 캐시 dict"""
    reports = list_audit_reports(corp_code)
    log(f"    감사보고서(별도) {len(reports)}건")
    out, new_cache = {}, {}
    for rcept, dt, nm in reports[:2]:   # 최신 2건 = 당기·전기 × 2 → 3개년 확보
        if rcept in cached:
            log(f"    {dt} {nm}: 캐시 사용")
            for end, rec in cached[rcept].items():
                out.setdefault(end, rec)
            new_cache[rcept] = cached[rcept]
            continue
        try:
            log(f"    {dt} {nm} rcept={rcept}: 원본 다운로드 → 추출")
            text = fetch_document_text(rcept)
            ex = claude_extract(name, text)
        except Exception as e:
            log(f"      실패: {str(e)[:120]}")
            continue
        recs = {}
        for which in ("current", "prior"):
            p = ex.get(which) or {}
            if p.get("end") and p.get("rev") is not None:
                recs[p["end"]] = {"rev": to_int(p.get("rev")), "op": to_int(p.get("op")),
                                  "ni": to_int(p.get("ni")),
                                  "source": f"{nm} {dt} rcept={rcept} ({which}) · {ex.get('unit_note', '')}",
                                  "rcept_no": rcept}
        for end, rec in recs.items():
            out.setdefault(end, rec)
            log(f"      {end}: 매출 {rec['rev']:,} / 영업이익 {rec['op']} / 순이익 {rec['ni']}")
        new_cache[rcept] = recs
        time.sleep(1)
    return out, new_cache


def main():
    if not DART_KEY:
        log("[ERROR] DART_API_KEY 미설정")
        raise SystemExit(1)
    old = {}
    if os.path.exists(OUT_PATH):
        try:
            with open(OUT_PATH, encoding="utf-8") as f:
                old = json.load(f)
        except Exception:
            pass
    old_cache = old.get("_cache", {})
    today = datetime.datetime.now(KST).date()
    years = [today.year - i for i in range(0, YEARS_BACK + 1)]

    result = {"updated_at": today.isoformat(),
              "cadence": "월 1회 자동 체크 — 새 감사보고서/사업보고서만 추출 (DART OpenAPI)",
              "source_note": "DART: 사업보고서 제출 법인은 구조화 API(별도 우선), 외감 법인은 감사보고서 원본을 Claude로 추출. 단위: 원. null = 미확인(§29-D)",
              "entities": [], "_cache": {}}

    for eid, name, etype, link, code, route, fy_m, note in ENTITIES:
        log(f"[{eid}] {name} ({route}) corp={code}")
        recs = {}
        if route == "api":
            recs = fetch_api_years(code, fy_m, years)
        elif route == "doc":
            if not ANTHROPIC_KEY:
                log("    [WARN] ANTHROPIC_API_KEY 미설정 → 추출 생략")
            else:
                recs, cache = fetch_doc_years(name, code, old_cache.get(eid, {}))
                result["_cache"][eid] = cache
        else:
            log("    공시 미발견 경로 — 수치 없음")
        ends = sorted(recs)[-3:]
        years_out = []
        for end in ends:
            r = recs[end]
            years_out.append({"fy": f"FY{end[2:4]}", "end": end,
                              "rev": r.get("rev"), "op": r.get("op"), "ni": r.get("ni"),
                              "source": r.get("source")})
        if not years_out:
            years_out = [{"fy": None, "end": None, "rev": None, "op": None, "ni": None, "source": None}]
        result["entities"].append({
            "id": eid, "name": name, "type": etype, "link": link,
            "corp_code": code, "route": route, "fy_end_month": fy_m, "note": note,
            "years": years_out,
        })
        log(f"    → {len(ends)}개년 수록")

    os.makedirs("docs", exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    n = sum(1 for e in result["entities"] if e["years"] and e["years"][0].get("rev") is not None)
    log(f"saved {OUT_PATH} — 수치 확보 {n}/{len(ENTITIES)}개 법인")


if __name__ == "__main__":
    main()

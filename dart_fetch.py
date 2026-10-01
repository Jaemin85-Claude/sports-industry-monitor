# -*- coding: utf-8 -*-
"""
sports-industry-monitor — Phase 6: DART 국내 법인 실적 (v2.4)
v2.5: 국내 법인 5곳 추가(감사보고서 경로, 2026-10-01 DART 공시 목록 확인) — 크림(KREAM)·트렌비·발란·머스트잇
      (병행수입·리셀 플랫폼), 트렉시(자사, 대표 승인). 에이비씨마트코리아를 일본 본사 ABC마트(2670.T)에 연결
v2.4: 원본 추출에 매출원가 추가(SCHEMA_V=3 → 8개 법인 1회 재추출) → 재고일수 계산 가능.
      블랙야크아이앤씨(478560) 상장 목록 편입
v2.3: 재조사(2026-09-29) 반영 — 아디다스코리아는 2017년 유한책임회사 전환으로 외감 공시 의무 없음
      (마지막 감사보고서 2016), 슈마커코리아(00396402)는 시흥 화학업체(동명)로 확인되어 코드 제거
v2.2: 전체재무제표 결산일을 법인별 결산월로 산정(신성통상 6월 → 06-30), 종목별 재무제표 기준 예외
      (LS네트웍스 별도 — 2024년 LS증권 연결 편입으로 연결 수치가 브랜드와 무관)
v2.1: 캐시 판정 강화 — 빈 캐시·재고 항목 없는 캐시는 재추출
v2: ① 국내 상장 20개사 — 종목코드→법인코드 매칭 후 연결 전체재무제표 API(fnlttSinglAcntAll)로
       매출·매출원가·영업이익·순이익·재고자산 3개년 → docs/kr_listed_fin.json
    ② 국내 법인 — 구조화 API 경로도 전체재무제표(별도)로 전환(재고 포함), 원본 추출에 재고자산 추가
       (SCHEMA_V=2로 캐시 갱신)
v1.1: Anthropic 401/403·크레딧 소진 시 즉시 실패(워크플로우 빨간 X), 오류 응답 본문 로그
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
SCHEMA_V = 3
LISTED_PATH = "docs/kr_listed_fin.json"

# ── 국내 상장 20개사 (야후 티커 → 종목코드 앞 6자리로 법인코드 매칭) ──
KR_LISTED = ["081660.KS", "383220.KS", "298540.KQ", "120110.KS", "337930.KQ",
             "000680.KS", "036620.KQ", "278470.KS", "031430.KS", "020000.KS",
             "093050.KS", "028260.KS", "111770.KS", "241590.KS", "105630.KS",
             "009970.KS", "023530.KS", "004170.KS", "069960.KS", "478560.KS"]

# 전체재무제표 계정 매칭 (account_id 우선, 이름 보조)
ACC_FULL = {
    "rev":  (["ifrs-full_Revenue", "ifrs_Revenue"], ["매출액", "수익(매출액)", "영업수익", "매출"]),
    "cogs": (["ifrs-full_CostOfSales", "ifrs_CostOfSales"], ["매출원가"]),
    "op":   (["dart_OperatingIncomeLoss"], ["영업이익", "영업이익(손실)", "영업손익"]),
    "ni":   (["ifrs-full_ProfitLoss", "ifrs_ProfitLoss"], ["당기순이익", "당기순이익(손실)", "당기순손익"]),
    "inv":  (["ifrs-full_Inventories", "ifrs_Inventories"], ["재고자산"]),
}

# ── 법인 정의 (프로브 확정) ─────────────────────────────
# id, 표시명, 유형, 연결 글로벌 티커, corp_code, 경로, 결산월, 주석
ENTITIES = [
    ("nike_kr",     "나이키코리아",        "글로벌 브랜드 국내법인", "NKE",    "01503133", "doc",  5,  "유한회사 — 5월 결산"),
    ("adidas_kr",   "아디다스코리아",      "글로벌 브랜드 국내법인", "ADS.DE", "00148133", "none", 12, "2017년 유한책임회사 전환 → 외감 공시 의무 없음(마지막 감사보고서 2016년) — 대체 지표: 아디다스 글로벌 IR '일본/한국' 지역 매출(Phase 7-A)"),
    ("asics_kr",    "아식스코리아",        "글로벌 브랜드 국내법인", "7936.T", "00664385", "doc",  12, "12월 결산"),
    ("puma_kr",     "푸마코리아",          "글로벌 브랜드 국내법인", "PUM.DE", "01471250", "doc",  12, "유한회사 — K-IFRS"),
    ("descente_kr", "데상트코리아",        "글로벌 브랜드 국내법인", None,     "00411154", "doc",  12, "일본 본사 상장폐지(2025.1) — 국내 법인은 DART로 추적"),
    ("nb_eland",    "뉴발란스(이랜드월드)", "글로벌 브랜드 국내법인", None,     "00207108", "api",  12, "라이선스 — 이랜드월드 법인 전체 수치(뉴발란스 부문 분리 불가)"),
    ("abcmart_kr",  "에이비씨마트코리아",  "국내 유통(비상장)",      "2670.T", "00496340", "doc",  12, "일본 ABC-Mart 자회사, 신발 멀티숍 1위"),
    ("shoemarker",  "슈마커",              "국내 유통(비상장)",      None,     None,       "none", 12, "DART 법인 목록에 운영 법인 없음(동명 '슈마커코리아'는 시흥 화학업체) — 외감 대상 아님 또는 타 법인명 운영, 확인 불가"),
    ("musinsa",     "무신사",              "국내 유통(비상장)",      None,     "01137727", "api",  12, "온라인 패션 플랫폼 — 2024년부터 사업보고서 제출, 거래액≠매출"),
    ("k2_kr",       "K2코리아",            "국내 브랜드(비상장)",    None,     "00407063", "doc",  12, "K2·아이더·다이나핏"),
    ("blackyak",    "비와이엔블랙야크",    "국내 브랜드(비상장)",    None,     "00520850", "doc",  12, "블랙야크·나우 (별도 상장사 블랙야크아이앤씨 478560 존재)"),
    ("nepa",        "네파",                "국내 브랜드(비상장)",    None,     "00932930", "doc",  12, "아웃도어"),
    ("shinsung",    "신성통상(탑텐)",      "국내 브랜드(비상장)",    None,     "00136341", "api",  6,  "2025년 자진 상장폐지 — 6월 결산, 사업보고서는 계속 제출"),
    ("kream",       "크림(KREAM)",         "국내 유통(비상장)",      None,     "01529876", "doc",  12, "네이버 자회사 — 스니커즈·명품 리셀 플랫폼, 거래액≠매출"),
    ("trenbe",      "트렌비",              "국내 유통(비상장)",      None,     "01537334", "doc",  12, "명품 병행수입 플랫폼 — 별도 감사보고서 기준"),
    ("balaan",      "발란",                "국내 유통(비상장)",      None,     "01551565", "doc",  12, "명품 병행수입 플랫폼"),
    ("mustit",      "머스트잇",            "국내 유통(비상장)",      None,     "01557082", "doc",  12, "명품 병행수입 플랫폼 — 2025년 감사보고서 미공시(2026.10 확인)"),
    ("trexi",       "트렉시(자사)",        "자사",                   None,     "01454031", "doc",  12, "자사 — 병행수입·브랜드 온라인 벤더, DART 공개 감사보고서(별도) 수치"),
]



# ── Anthropic 호출 공통: 인증/크레딧 오류는 즉시 실패(워크플로우 빨간 X) ──
def anthropic_post(payload, timeout=180):
    """401(키 무효/만료)·403·400 credit(잔액 소진) → SystemExit(2)로 즉시 종료.
    그 외 오류는 응답 본문을 포함해 예외로 올려 호출부가 처리."""
    resp = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={"x-api-key": ANTHROPIC_KEY, "anthropic-version": "2023-06-01",
                 "content-type": "application/json"},
        json=payload, timeout=timeout)
    if resp.status_code in (401, 403) or (resp.status_code == 400 and "credit" in resp.text.lower()):
        print(f"[FATAL] Anthropic API {resp.status_code}: {resp.text[:300]}", flush=True)
        print("[FATAL] 키 만료/무효 또는 크레딧 소진 — console.anthropic.com 확인 후 "
              "GitHub Secret ANTHROPIC_API_KEY 갱신", flush=True)
        raise SystemExit(2)
    if resp.status_code != 200:
        raise RuntimeError(f"Anthropic {resp.status_code}: {resp.text[:200]}")
    return resp.json()

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
        return int(round(float(str(s).replace(",", "").replace(" ", ""))))
    except (ValueError, OverflowError):
        return None


# ── 경로 A: 구조화 API ──────────────────────────────────
ACCOUNT_MAP = {
    "rev": ["매출액", "수익(매출액)", "영업수익", "매출"],
    "op":  ["영업이익", "영업이익(손실)", "영업손익"],
    "ni":  ["당기순이익", "당기순이익(손실)", "당기순손익", "당기순손실"],
}


def load_corp_map_by_stock():
    """corpCode.xml(zip) → {종목코드: (corp_code, corp_name)}"""
    import zipfile, io
    import xml.etree.ElementTree as ET
    raw = dart(f"{BASE}/corpCode.xml", {}, as_bytes=True, timeout=180)
    z = zipfile.ZipFile(io.BytesIO(raw))
    name = [n for n in z.namelist() if n.lower().endswith(".xml")][0]
    root = ET.fromstring(z.read(name))
    m = {}
    for el in root.iter("list"):
        sc = (el.findtext("stock_code") or "").strip()
        if sc:
            m[sc] = ((el.findtext("corp_code") or "").strip(), (el.findtext("corp_name") or "").strip())
    return m


def _pick(rows, ids, names, sj_pref):
    """전체재무제표 행에서 계정 1개 선택: account_id 일치 > 이름 정확 > 이름 포함. sj_div 우선순위 적용."""
    def order(r):
        sj = r.get("sj_div") or ""
        return sj_pref.index(sj) if sj in sj_pref else 99
    cand = [r for r in rows if (r.get("account_id") or "") in ids]
    if not cand:
        cand = [r for r in rows if (r.get("account_nm") or "").replace(" ", "") in [n.replace(" ", "") for n in names]]
    if not cand:
        cand = [r for r in rows if any(n.replace(" ", "") in (r.get("account_nm") or "").replace(" ", "") for n in names)]
    if not cand:
        return None
    cand.sort(key=order)
    return cand[0]


# 종목별 재무제표 기준 예외 (기본 연결 CFS)
FS_OVERRIDE = {"000680.KS": "OFS"}   # LS네트웍스: LS증권 연결 편입 → 별도로 브랜드 사업 추적
LISTED_FY_MONTH = {}                  # 12월 결산 외 종목이 생기면 {"티커": 월} 추가


def _end_date(y, m):
    import calendar
    return f"{y}-{m:02d}-{calendar.monthrange(y, m)[1]:02d}"


def fetch_full_statements(corp_code, fs_div, years_try, fy_month=12):
    """전체재무제표(사업보고서) 1건으로 당기·전기·전전기 3개년 확보.
    반환 ({end: {rev, cogs, op, ni, inv}}, source) — 값 없는 항목은 None"""
    for y in years_try:
        try:
            data = dart(f"{BASE}/fnlttSinglAcntAll.json", {
                "corp_code": corp_code, "bsns_year": str(y),
                "reprt_code": "11011", "fs_div": fs_div})
        except Exception as e:
            log(f"    {y} {fs_div}: API 오류 {str(e)[:80]}")
            continue
        if data.get("status") != "000":
            log(f"    {y} {fs_div}: {data.get('status')} {data.get('message')}")
            continue
        rows = data.get("list", [])
        out = {}
        # 기간 라벨 → 결산일 추출 (thstrm_dt 예: '2025.12.31 현재' / '2025.01.01 ~ 2025.12.31')
        def end_of(key):
            for r in rows:
                dt = r.get(key) or ""
                m = re.findall(r"(\d{4})\.(\d{2})\.(\d{2})", dt)
                if m:
                    yy, mm, dd = m[-1]
                    return f"{yy}-{mm}-{dd}"
            return None
        periods = [("thstrm_amount", end_of("thstrm_dt") or _end_date(y, fy_month)),
                   ("frmtrm_amount", end_of("frmtrm_dt") or _end_date(y - 1, fy_month)),
                   ("bfefrmtrm_amount", end_of("bfefrmtrm_dt") or _end_date(y - 2, fy_month))]
        for amt_key, end in periods:
            rec = {}
            for k, (ids, names) in ACC_FULL.items():
                sj_pref = ["BS"] if k == "inv" else ["IS", "CIS"]
                r = _pick(rows, ids, names, sj_pref)
                rec[k] = to_int(r.get(amt_key)) if r else None
            if rec.get("rev") is not None:
                out[end] = rec
        if out:
            src_txt = f"사업보고서 {y} ({'연결' if fs_div == 'CFS' else '별도'}) rcept={rows[0].get('rcept_no')}"
            for end, rec in sorted(out.items()):
                log(f"    {end}: 매출 {rec['rev']:,} / 원가 {rec['cogs']} / 영업이익 {rec['op']} / 순이익 {rec['ni']} / 재고 {rec['inv']}")
            return out, src_txt
    return {}, None


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
- 매출원가 (cost of sales) — from the income statement; null if the statement shows only
  gross profit without a cost line
Also from the statement of financial position (재무상태표): 재고자산 (inventories) at
each period end.

Amounts must be in KRW units of 원 (convert if the statement says 단위: 천원 or 백만원).
Use ONLY figures explicitly stated. If a figure is not stated, use null.

Respond with ONLY a JSON object, no markdown fences:
{{
  "unit_note": "단위 표기 그대로, 예: 단위: 원",
  "current": {{"end": "YYYY-MM-DD", "rev": number|null, "cogs": number|null, "op": number|null, "ni": number|null, "inv": number|null}},
  "prior":   {{"end": "YYYY-MM-DD", "rev": number|null, "cogs": number|null, "op": number|null, "ni": number|null, "inv": number|null}}
}}

DOCUMENT:
{text}"""
    data = anthropic_post({"model": "claude-sonnet-4-6", "max_tokens": 800,
              "messages": [{"role": "user", "content": prompt}]}, timeout=180)
    parts = data.get("content", [])
    txt = "".join(p.get("text", "") for p in parts if p.get("type") == "text")
    txt = re.sub(r"```json|```", "", txt).strip()
    return json.loads(txt)


def fetch_doc_years(name, corp_code, cached):
    """cached: {rcept_no: {end: rec}} 기존 추출. 반환 {end: rec}, 사용된 캐시 dict"""
    reports = list_audit_reports(corp_code)
    log(f"    감사보고서(별도) {len(reports)}건")
    out, new_cache = {}, {}
    for rcept, dt, nm in reports[:2]:   # 최신 2건 = 당기·전기 × 2 → 3개년 확보
        if (rcept in cached and cached[rcept]
                and all(v.get("schema_v") == SCHEMA_V and "inv" in v and "cogs" in v for v in cached[rcept].values())):
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
                                  "ni": to_int(p.get("ni")), "inv": to_int(p.get("inv")),
                                  "cogs": to_int(p.get("cogs")),
                                  "schema_v": SCHEMA_V,
                                  "source": f"{nm} {dt} rcept={rcept} ({which}) · {ex.get('unit_note', '')}",
                                  "rcept_no": rcept}
        for end, rec in recs.items():
            out.setdefault(end, rec)
            log(f"      {end}: 매출 {rec['rev']:,} / 원가 {rec.get('cogs')} / 영업이익 {rec['op']} / 순이익 {rec['ni']} / 재고 {rec['inv']}")
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
        log(f"[{eid}] {name} ({route}) corp={code or '-'}")
        recs = {}
        if route == "api":
            recs, src_txt = fetch_full_statements(code, "OFS", years, fy_m)
            for r in recs.values():
                r["source"] = src_txt
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
                              "inv": r.get("inv"), "cogs": r.get("cogs"),
                              "source": r.get("source")})
        if not years_out:
            years_out = [{"fy": None, "end": None, "rev": None, "op": None, "ni": None, "inv": None, "source": None}]
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

    # ── 국내 상장 20개사: 연결 전체재무제표 3개년 ──
    log("\n[상장] 법인코드 매칭(종목코드) ...")
    try:
        cmap = load_corp_map_by_stock()
    except Exception as e:
        log(f"[WARN] corpCode 로드 실패: {str(e)[:120]} — 상장사 처리 생략")
        return
    listed = {"updated_at": today.isoformat(), "basis": "DART 연결 전체재무제표(사업보고서)", "items": {}}
    for tk in KR_LISTED:
        sc = tk.split(".")[0]
        hit = cmap.get(sc)
        if not hit:
            log(f"[{tk}] 법인코드 미발견")
            listed["items"][tk] = {"error": "법인코드 미발견"}
            continue
        code, cname = hit
        log(f"[{tk}] {cname} corp={code}")
        fs = FS_OVERRIDE.get(tk, "CFS"); fym = LISTED_FY_MONTH.get(tk, 12)
        if fs != "CFS":
            log(f"    기준 예외: {'별도' if fs == 'OFS' else fs}")
        recs, src_txt = fetch_full_statements(code, fs, years, fym)
        if not recs and fs == "CFS":
            log("    연결 없음 → 별도 시도")
            recs, src_txt = fetch_full_statements(code, "OFS", years, fym)
        ys = []
        for end in sorted(recs):
            r = recs[end]
            ys.append({"end": end, "rev": r.get("rev"), "cogs": r.get("cogs"), "op": r.get("op"),
                       "ni": r.get("ni"), "inv": r.get("inv")})
        listed["items"][tk] = {"corp_code": code, "corp_name": cname, "source": src_txt, "years": ys[-3:]}
    with open(LISTED_PATH, "w", encoding="utf-8") as f:
        json.dump(listed, f, ensure_ascii=False, indent=1)
    ok = sum(1 for v in listed["items"].values() if v.get("years"))
    log(f"saved {LISTED_PATH} — 상장 {ok}/{len(KR_LISTED)}개사 3개년 확보")


if __name__ == "__main__":
    main()

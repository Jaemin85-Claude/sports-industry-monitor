# -*- coding: utf-8 -*-
"""
sports-industry-monitor — Phase 6: DART 국내 법인 실적 (v2.4)
v3.0: 수입 브랜드 유통사 비교군 9곳(FIN_IDS, 트렉시 포함)에 재무상태표·현금흐름표 추출 추가(대표 요청 2026-10-03) —
      현금·단기금융상품·매출채권·매입채무·차입금·리스부채·자산·부채·자본총계·영업활동현금흐름·CAPEX·감가상각비.
      손익 추출(캐시 SCHEMA_V=3)은 그대로 두고 별도 호출·별도 캐시(_cache_fin, FIN_V=1) — 다른 법인은 재추출 없음.
      검증: 자산총계 ≠ 부채+자본(1% 초과) 또는 재고가 손익 추출 값과 1% 넘게 다르면 그 해 chk 표시(화면 '확인 필요').
      원본 창: 재무상태표~현금흐름표 표 부근(멀면 두 창)
v2.9: 아이웨어 2곳 추가(2026-10-03 DART 감사보고서 확인, 대표 요청) — 케어링아이웨어코리아(케링 아이웨어 한국 법인:
      구찌·생로랑·보테가·까르띠에 등), 시원아이웨어(디올·펜디 등 명품 아이웨어 수입 유통). 둘 다 2025년 첫 감사보고서라 2개년
v2.8: 국내 패션 브랜드 13곳 추가(2026-10-03 DART 공시 목록 확인, 대표 요청) — 상장 3곳은 사업보고서 경로
      (에이유브랜즈·피스피스스튜디오·에스제이그룹), 외감 10곳은 감사보고서 경로(마뗑킴·레이어·하이라이트브랜즈·
      하고하우스·비케이브·파이브스페이스·코자·안다르·시선인터내셔널·로우클래식) → 대시보드 '국내 패션 브랜드 비교'.
      아이웨어 4곳(감사보고서) — 아이아이컴바인드(젠틀몬스터)·블루엘리펀트·룩소티카코리아(글로벌 국내법인)·
      다비치안경체인(유통) → '아이웨어 비교'(수입 후보 글로벌 아이웨어의 국내 경쟁 구도)
v2.7: 수입 브랜드 유통사 8곳 추가(감사보고서 경로, 2026-10-02 DART 공시 목록·대표자 확인) — 대림코퍼레이션·렉스몬드(오케이몰)·
      베이지그·크리드네트웍스·한아아이앤티·티원글로벌·비블루아이앤·스타인터내셔널 → 대시보드에서 트렉시와 비교
v2.6: 발란 주석에 2026.2 회생절차 폐지·청산 절차 진행 반영(2026.10 대표 확인)
v2.5: 국내 법인 5곳 추가(감사보고서 경로, 2026-10-01 DART 공시 목록 확인) — 크림(KREAM)·트렌비·발란·머스트잇
      (병행수입·리셀 플랫폼), 트렉시(자사, 대표 승인). 에이비씨마트코리아를 일본 본사 ABC마트(2670.T)에 연결.
      원본 추출 보강 — 압축 파일 중 손익계산서가 있는 문서 우선 선택, 응답에 설명 문장이 섞여도 JSON만 파싱,
      수치를 못 찾으면 진단 로그(문서 글자 수·핵심어 유무·응답 앞부분)
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
# 재무상태표·현금흐름표 추가 추출 대상(수입 브랜드 유통사 비교군) — 손익과 별도 캐시
FIN_IDS = {"trexi", "daelim_corp", "rexmond", "bazig", "creed", "hana_int", "t1global", "bbluein", "starintl"}
FIN_V = 1
FIN_KEYS = ("assets", "liab", "equity", "cash", "stfin", "ar", "ap", "borrow", "lease", "inv", "ocf", "capex", "da")

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
    ("balaan",      "발란",                "국내 유통(비상장)",      None,     "01551565", "doc",  12, "명품 병행수입 플랫폼 — 2025.3 기업회생 신청, 2026.2 회생절차 폐지 후 청산 절차 진행(2026.10 대표 확인). 2024·2025년 감사보고서 원문에 재무제표 수치 없음"),
    ("mustit",      "머스트잇",            "국내 유통(비상장)",      None,     "01557082", "doc",  12, "명품 병행수입 플랫폼 — 2025년 감사보고서 미공시(2026.10 확인)"),
    # ── 수입 브랜드 유통사 비교군(트렉시와 비교, v2.7) — 소재지·설립은 DART 기업개황 ──
    ("daelim_corp", "대림코퍼레이션",      "수입 브랜드 유통(비상장)", None,    "01635043", "doc",  12, "경남 양산 · 2014년 설립"),
    ("rexmond",     "렉스몬드(오케이몰)",  "수입 브랜드 유통(비상장)", None,    "00864921", "doc",  12, "서울 중구 · 온라인몰 오케이몰(okmall.com) 운영"),
    ("bazig",       "베이지그",            "수입 브랜드 유통(비상장)", None,    "01730409", "doc",  12, "부산 사상 · 2003년 설립"),
    ("creed",       "크리드네트웍스",      "수입 브랜드 유통(비상장)", None,    "01947115", "doc",  12, "서울 성수 · 2025년 첫 외부감사(2개년만)"),
    ("hana_int",    "한아아이앤티",        "수입 브랜드 유통(비상장)", None,    "00599319", "doc",  12, "서울 도봉 · 온라인몰 하하몰(hahamall.net) 운영"),
    ("t1global",    "티원글로벌",          "수입 브랜드 유통(비상장)", None,    "01631108", "doc",  12, "서울 성수 · 2017년 설립"),
    ("bbluein",     "비블루아이앤",        "수입 브랜드 유통(비상장)", None,    "01139381", "doc",  12, "서울 노원 · 2007년 설립"),
    ("starintl",    "스타인터내셔널",      "수입 브랜드 유통(비상장)", None,    "01653924", "doc",  12, "서울 서초 · 2019년 설립"),
    # ── 국내 패션 브랜드(v2.8) — 상장사도 별도 재무제표로 맞춤(외감 법인 감사보고서가 별도 기준) ──
    ("aubrandz",    "에이유브랜즈(락피쉬)", "국내 패션 브랜드", None,    "01803927", "api",  12, "코스닥 481070 · 락피쉬웨더웨어 · 2025.4 상장"),
    ("piecepeace",  "피스피스스튜디오(마르디)", "국내 패션 브랜드", None, "01755259", "api",  12, "코스닥 · 마르디 메크르디 · 2026 상장"),
    ("sjgroup",     "에스제이그룹(캉골)",  "국내 패션 브랜드",      None,     "01222432", "api",  12, "코스닥 306040 · 캉골·헬렌카민스키"),
    ("matinkim",    "마뗑킴",              "국내 패션 브랜드",      None,     "01826414", "doc",  12, "대명화학 그룹"),
    ("layer",       "레이어(마리떼)",      "국내 패션 브랜드",      None,     "01634345", "doc",  12, "마리떼 프랑소와 저버 · 대명화학 그룹"),
    ("highlight",   "하이라이트브랜즈(코닥)", "국내 패션 브랜드",   None,     "01565966", "doc",  12, "코닥어패럴 · 대명화학 그룹"),
    ("hagohouse",   "하고하우스",          "국내 패션 브랜드",      None,     "01743856", "doc",  12, "브랜드 육성·투자 · 대명화학 그룹 · 별도 기준"),
    ("bcave",       "비케이브(커버낫)",    "국내 패션 브랜드",      None,     "01461509", "doc",  12, "커버낫·리(Lee)·와키윌리"),
    ("fivespace",   "파이브스페이스(아더에러)", "국내 패션 브랜드", None,     "01664744", "doc",  12, "아더에러"),
    ("koza",        "코자(스탠드오일)",    "국내 패션 브랜드",      None,     "01904192", "doc",  12, "스탠드오일 · 2025년 첫 감사보고서"),
    ("andar",       "안다르",              "국내 패션 브랜드",      None,     "01468186", "doc",  12, "애슬레저 · 에코마케팅 자회사"),
    ("sisun",       "시선인터내셔널(미샤)", "국내 패션 브랜드",     None,     "00369329", "doc",  12, "미샤·잇미샤 여성복"),
    ("lowclassic",  "로우클래식",          "국내 패션 브랜드",      None,     "01651847", "doc",  12, "여성 디자이너 브랜드"),
    # ── 아이웨어(v2.8) — 국내 브랜드 vs 글로벌 국내법인 vs 안경 체인 ──
    ("iicombined",  "아이아이컴바인드(젠틀몬스터)", "국내 아이웨어", None, "01134410", "doc", 12, "젠틀몬스터·탬버린즈·누데이크 — 별도 기준"),
    ("blueelephant", "블루엘리펀트",       "국내 아이웨어",         None,     "01706448", "doc",  12, "5만원대 아이웨어 · 2019년 설립"),
    ("luxottica_kr", "룩소티카코리아",     "글로벌 아이웨어 국내법인", "EL.PA", "00760865", "doc", 12, "에실로룩소티카 한국 법인 — 레이밴·오클리 등"),
    ("kering_ey_kr", "케어링아이웨어코리아", "글로벌 아이웨어 국내법인", None, "01504071", "doc", 12, "케링 아이웨어 한국 법인 — 구찌·생로랑·보테가·까르띠에 등"),
    ("seeone",      "시원아이웨어",        "아이웨어 수입 유통",     None,     "01475450", "doc",  12, "디올·펜디 등 명품 아이웨어 수입 유통"),
    ("davich",      "다비치안경체인",      "안경 유통 체인",         None,     "01336726", "doc",  12, "안경원 체인(유통)"),
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


_PLAIN = {}   # 같은 실행에서 손익·재무상태표 추출이 같은 원본을 두 번 받지 않도록


def fetch_document_plain(rcept_no):
    """원본 zip → 손익계산서가 있는 문서(가장 큰 것)의 평문 전체"""
    if rcept_no in _PLAIN:
        return _PLAIN[rcept_no]
    raw = dart(f"{BASE}/document.xml", {"rcept_no": rcept_no}, as_bytes=True, timeout=120)
    if raw[:2] != b"PK":
        raise RuntimeError("원본이 zip이 아님")
    z = zipfile.ZipFile(io.BytesIO(raw))
    docs = []   # (손익계산서 포함 여부, 크기, 이름, 본문)
    for name in z.namelist():
        content = z.read(name)
        txt = None
        for enc in ("utf-8", "euc-kr", "cp949"):
            try:
                txt = content.decode(enc)
                break
            except Exception:
                continue
        if txt is None:
            continue
        plain = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", txt))
        docs.append(("손익계산서" in plain, len(content), name, plain))
    if not docs:
        raise RuntimeError("디코딩 실패")
    # 손익계산서가 있는 문서 중 가장 큰 것(없으면 가장 큰 문서) — 첨부가 본문보다 큰 공시 대응
    has_is, _, name, plain = max(docs, key=lambda d: (d[0], d[1]))
    if len(docs) > 1 or not has_is:
        log(f"      원본 파일 {len(docs)}개 중 {name} 선택 · 손익계산서 {'있음' if has_is else '없음'} · {len(plain):,}자")
    _PLAIN[rcept_no] = plain
    return plain


def fetch_document_text(rcept_no):
    plain = fetch_document_plain(rcept_no)
    # 손익계산서 부근 우선 포함: 앞부분(회사명·기간) + 손익계산서 창
    idx = plain.find("손익계산서")
    if len(plain) > MAX_DOC_CHARS and idx > 20000:
        plain = plain[:15000] + " ...(중략)... " + plain[idx - 2000: idx - 2000 + (MAX_DOC_CHARS - 15000)]
    elif len(plain) > MAX_DOC_CHARS:
        # 첫 언급이 감사의견 문단이고 실제 표(금액이 붙은 손익계산서)가 상한 뒤에 있으면 표 부근으로 창 이동
        tbl = next((m.start() for m in re.finditer("손익계산서", plain)
                    if re.search(r"\d{1,3}(?:,\d{3}){2,}", plain[m.start(): m.start() + 1500])), -1)
        if tbl > MAX_DOC_CHARS - 10000:
            st = max(15000, tbl - 12000)   # 재무상태표(재고)도 포함되도록 앞쪽 여유
            plain = plain[:15000] + " ...(중략)... " + plain[st: st + (MAX_DOC_CHARS - 15000)]
            log(f"      손익계산서 표 위치 {tbl:,}자 → 창 이동")
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
    return ask_json(prompt, 800)


def ask_json(prompt, max_tokens):
    data = anthropic_post({"model": "claude-sonnet-4-6", "max_tokens": max_tokens,
              "messages": [{"role": "user", "content": prompt}]}, timeout=180)
    parts = data.get("content", [])
    txt = "".join(p.get("text", "") for p in parts if p.get("type") == "text")
    txt = re.sub(r"```json|```", "", txt).strip()
    try:
        return json.loads(txt)
    except ValueError:
        m = re.search(r"\{.*\}", txt, re.S)   # 설명 문장이 섞인 응답 → JSON 부분만
        if m:
            try:
                return json.loads(m.group(0))
            except ValueError:
                pass
        raise RuntimeError("응답이 JSON 아님: " + re.sub(r"\s+", " ", txt)[:150])


# ── 재무상태표·현금흐름표 추가 추출(v3.0, FIN_IDS만) ──────────
def _sp(word):
    """'재 무 상 태 표'처럼 글자 사이가 띄어진 제목도 찾도록"""
    return r"\s*".join(map(re.escape, word))


def _table_pos(plain, word, start=0, need=None):
    """word 뒤 1500자 안에 큰 금액(1,234,567 꼴)이 있는 첫 위치 = 실제 표(목차·감사의견 문단 제외)"""
    for m in re.finditer(_sp(word), plain[start:]):
        p = start + m.start()
        if (re.search(r"\d{1,3}(?:,\d{3}){2,}", plain[p: p + 1500])
                and (need is None or re.search(_sp(need), plain[p: p + 4000]))):
            return p
    return -1


def fin_window(plain):
    """앞부분(회사명·단위) + 재무상태표~현금흐름표 표 부근. 둘이 멀면 두 창으로 나눔"""
    if len(plain) <= MAX_DOC_CHARS:
        return plain
    head, room = 8000, MAX_DOC_CHARS - 8000
    bs = _table_pos(plain, "재무상태표")
    cf = _table_pos(plain, "현금흐름표", max(bs, 0), need="영업활동")
    found = [p for p in (bs, cf) if p >= 0]
    if not found:
        log("      재무상태표·현금흐름표 표 위치 못 찾음 → 앞부분")
        return plain[:MAX_DOC_CHARS]
    if len(found) == 1 or (cf + 15000) - (bs - 1000) <= room:
        a = max(head, found[0] - 1000)
        return plain[:head] + " ...(중략)... " + plain[a: a + room]
    log(f"      재무상태표 {bs:,}자 · 현금흐름표 {cf:,}자 → 두 창")
    return " ...(중략)... ".join([plain[:head]] + [plain[max(head, p - 1000): max(head, p - 1000) + room // 2] for p in found])


def claude_extract_fin(name, text):
    prompt = f"""You are extracting figures from a Korean statutory audit report (감사보고서, separate
financial statements) of {name}. For the CURRENT period (당기) and the PRIOR period (전기):

From the statement of financial position (재무상태표), at each period end:
- end: period end date (YYYY-MM-DD)
- assets: 자산총계
- liab: 부채총계
- equity: 자본총계 (negative if 자본잠식)
- cash: 현금및현금성자산
- stfin: 단기금융상품 (short-term financial instruments / deposits); null if none shown
- ar: 매출채권 (net of allowance). If only "매출채권및기타채권" is shown, use that line.
- ap: 매입채무. If only "매입채무및기타채무" is shown, use that line.
- borrow: interest-bearing borrowings = 단기차입금 + 유동성장기차입금(유동성장기부채) + 장기차입금
  + 사채(유동성사채 포함). Exclude lease liabilities. 0 if the company shows none.
- lease: 리스부채 (current + non-current); null if not shown
- inv: 재고자산
From the cash flow statement (현금흐름표), for each period:
- ocf: 영업활동으로 인한 현금흐름 / 영업활동현금흐름 (net; outflow as negative)
- capex: 유형자산의 취득 + 무형자산의 취득 (cash paid, as a positive number); 0 if none
- da: 감가상각비 + 사용권자산상각비 + 무형자산상각비 (from cash flow adjustments or notes); null if not found
For the PRIOR period also:
- equity_begin: 자본총계 at the beginning of the prior period (전기초), from 자본변동표; null if not shown

Amounts must be in KRW units of 원 (convert if the statement says 단위: 천원 or 백만원).
Use ONLY figures explicitly stated; if a figure is not stated, use null. Do not compute anything
except the sums described for borrow, capex and da.

Respond with ONLY a JSON object, no markdown fences:
{{
  "unit_note": "단위 표기 그대로",
  "current": {{"end": "YYYY-MM-DD", "assets": n, "liab": n, "equity": n, "cash": n, "stfin": n, "ar": n, "ap": n, "borrow": n, "lease": n, "inv": n, "ocf": n, "capex": n, "da": n}},
  "prior":   {{"end": "YYYY-MM-DD", "assets": n, "liab": n, "equity": n, "cash": n, "stfin": n, "ar": n, "ap": n, "borrow": n, "lease": n, "inv": n, "ocf": n, "capex": n, "da": n, "equity_begin": n}}
}}
(n = number or null)

DOCUMENT:
{text}"""
    return ask_json(prompt, 1000)


def fin_check(rec, pl):
    """검증: 자산 = 부채 + 자본(1% 이내), 재고가 손익 추출 값과 1% 이내. 어긋나면 사유 문자열"""
    bad = []
    a, l, e = rec.get("assets"), rec.get("liab"), rec.get("equity")
    if None in (a, l, e):
        bad.append("자산·부채·자본 일부 없음")
    elif abs(a - (l + e)) > 0.01 * abs(a):
        bad.append("자산≠부채+자본")
    i1, i2 = rec.get("inv"), (pl or {}).get("inv")
    if i1 is not None and i2 is not None and abs(i1 - i2) > 0.01 * max(abs(i2), 1):
        bad.append("재고가 손익 추출 값과 다름")
    return " · ".join(bad) or None


def fetch_fin_years(name, reports, cached, pl_recs):
    """reports: 감사보고서 목록(최신순). cached: {rcept_no: {end: rec}}. 반환 {end: rec}, 새 캐시"""
    out, new_cache = {}, {}
    for rcept, dt, nm in reports[:2]:
        if rcept in cached and cached[rcept] and all(v.get("fin_v") == FIN_V for v in cached[rcept].values()):
            log(f"    [재무상태표·현금흐름] {dt}: 캐시 사용")
            recs = cached[rcept]
        else:
            try:
                log(f"    [재무상태표·현금흐름] {dt} {nm} rcept={rcept}: 추출")
                ex = claude_extract_fin(name, fin_window(fetch_document_plain(rcept)))
            except Exception as e:
                log(f"      실패: {str(e)[:120]}")
                continue
            recs = {}
            for which in ("current", "prior"):
                p = ex.get(which) or {}
                if not p.get("end"):
                    continue
                rec = {k: to_int(p.get(k)) for k in FIN_KEYS}
                if which == "prior":
                    rec["equity_begin"] = to_int(p.get("equity_begin"))
                if all(rec.get(k) is None for k in ("assets", "equity", "ocf")):
                    continue
                rec.update(fin_v=FIN_V, source=f"{nm} {dt} rcept={rcept} ({which}) · {ex.get('unit_note', '')}")
                recs[p["end"]] = rec
            if not recs:
                log(f"      수치 없음 — 응답 {json.dumps(ex, ensure_ascii=False)[:150]}")
            time.sleep(1)
        for end, rec in recs.items():
            rec["chk"] = fin_check(rec, pl_recs.get(end))
            out.setdefault(end, rec)
            log(f"      {end}: 자산 {rec.get('assets')} / 부채 {rec.get('liab')} / 자본 {rec.get('equity')} / 현금 {rec.get('cash')}"
                f" / 차입금 {rec.get('borrow')} / 리스 {rec.get('lease')} / OCF {rec.get('ocf')} / CAPEX {rec.get('capex')}"
                f" / 상각 {rec.get('da')}{' ⚠ ' + rec['chk'] if rec.get('chk') else ''}")
        new_cache[rcept] = recs
    return out, new_cache


def fetch_doc_years(name, corp_code, cached, reports=None):
    """cached: {rcept_no: {end: rec}} 기존 추출. 반환 {end: rec}, 사용된 캐시 dict"""
    if reports is None:
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
        if not recs:
            log(f"      수치 없음 — 문서 {len(text):,}자 · 손익계산서 {'있음' if '손익계산서' in text else '없음'}"
                f" · 매출 {'있음' if '매출' in text else '없음'} · 응답 {json.dumps(ex, ensure_ascii=False)[:150]}")
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
    old_fin = old.get("_cache_fin", {})
    today = datetime.datetime.now(KST).date()
    years = [today.year - i for i in range(0, YEARS_BACK + 1)]

    result = {"updated_at": today.isoformat(),
              "cadence": "월 1회 자동 체크 — 새 감사보고서/사업보고서만 추출 (DART OpenAPI)",
              "source_note": "DART: 사업보고서 제출 법인은 구조화 API(별도 우선), 외감 법인은 감사보고서 원본을 Claude로 추출. 단위: 원. null = 미확인(§29-D)",
              "entities": [], "_cache": {}, "_cache_fin": {}}

    for eid, name, etype, link, code, route, fy_m, note in ENTITIES:
        log(f"[{eid}] {name} ({route}) corp={code or '-'}")
        recs, fin_by_end = {}, {}
        if route == "api":
            recs, src_txt = fetch_full_statements(code, "OFS", years, fy_m)
            for r in recs.values():
                r["source"] = src_txt
        elif route == "doc":
            if not ANTHROPIC_KEY:
                log("    [WARN] ANTHROPIC_API_KEY 미설정 → 추출 생략")
            else:
                reports = list_audit_reports(code)
                recs, cache = fetch_doc_years(name, code, old_cache.get(eid, {}), reports)
                result["_cache"][eid] = cache
                if eid in FIN_IDS:
                    fins, fcache = fetch_fin_years(name, reports, old_fin.get(eid, {}), recs)
                    result["_cache_fin"][eid] = fcache
                    fin_by_end = {end: {k: v for k, v in f.items() if k != "fin_v"} for end, f in fins.items()}
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
            if end in fin_by_end:
                years_out[-1]["fin"] = fin_by_end[end]
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
    fy = [y for e in result["entities"] if e["id"] in FIN_IDS for y in e["years"] if y.get("fin")]
    log(f"  재무상태표·현금흐름: {sum(1 for e in result['entities'] if e['id'] in FIN_IDS and any(y.get('fin') for y in e['years']))}"
        f"/{len(FIN_IDS)}개 법인 · {len(fy)}개 연도 · 확인 필요 {sum(1 for y in fy if y['fin'].get('chk'))}건")

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

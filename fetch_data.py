# -*- coding: utf-8 -*-
"""
sports-industry-monitor — Phase 1 데이터 수집 (v4)
v4.13: (대표 지시 2026-10-10) 분기 재고 — 최신 분기 재고를 1년 전 같은 분기와 비교(q_inv_yoy, 기준일 q_inv_date·q_inv_prev_date)하고
      같은 분기 매출 증감(q_inv_rev_yoy)도 저장. 연간 재고(inv_yoy)는 그대로 — 화면은 같은 기간끼리 비교하고 기간을 표시
v4.12: (대표 지시 2026-10-09) 분기 매출 증감은 최신 분기와 350~380일 전 분기를 짝지어 비교(푸마가 작년 1분기와 비교되던 문제),
      짝이 없으면 비움. 매출·총이익·영업이익은 연도마다 값 단위로 대체 항목을 쓰고, 그래도 비면 같은 결산일 이전 값(푸마 영업이익률).
      종목·환율 수집이 실패하면(감시 통화는 1% 칸 계산 실패 포함) 이전 data.json 값을 이어 쓰고 stale_since·최상위 fetch_status 기록,
      절반 넘게 실패하거나 감시 통화가 실패하면 soft_fail.txt에 표시. 날짜가 아닌 분기 열은 건너뜀.
      블랙야크아이앤씨는 처음부터 .KQ로, 리얄은 직접 조회 없이 달러 ÷ 3.75(404 로그 소음 제거)
v4.11: 환율에 스위스 프랑(CHF)·위안(CNY)·홍콩 달러(HKD)·사우디 리얄(SAR) 추가 — 기업 목록·상세의 외화 매출을 모두
      원화로 환산해 보이기 위함(대표 요청 2026-10-09, 온·안타·리닝·탑스포츠·비바굿즈·세노미). 값만 표시(1% 칸 알림 없음).
      리얄은 달러 고정(1달러 = 3.75리얄)이라 원화·달러 쌍이 모두 비면 달러 환율 ÷ 3.75로 계산
v4.10: 글로벌 아이웨어 2곳 추가 — 에실로룩소티카(EL.PA)·사필로(SFL.MI). 수입 후보 글로벌 아이웨어 브랜드의
      본사 실적·재고를 국내 아이웨어(젠틀몬스터·블루엘리펀트 등, dart_fetch v2.8)와 함께 보기 위함(대표 요청)
v4.9: 환율 1% 칸 알림 — 엔·유로·달러는 2년 일별 환율로 1년 이동평균 대비 %를 계산하고, 1% 단위 선
     (−1%, −2% … / +1%, +2% …)을 새로 넘은 날을 알림으로 기록(최근 30영업일 안에 닿은 선은 제외).
     data.json fx[통화]에 1년 일별 추이(hist)·1년 평균·다음 알림 가격·지난 1년 알림 목록,
     최상위 fx_push에 오늘 새로 생긴 알림 문구(점검 세션이 휴대폰 알림으로 그대로 전달).
     알림의 first_seen은 이전 data.json에서 이어받아 같은 알림이 두 번 나가지 않게 함
v4.8: 환율에 엔(JPYKRW=X) 추가 — 소싱 지도 일본 지역. 값은 1엔당 원화(화면은 100엔 단위)
v4.7: 상장 10곳 추가 — 휴먼메이드(456A.T)·비바굿즈(클락스, 0933.HK)·불카브라스(VULC3.SA)
     (글로벌 브랜드), ABC마트(2670.T)·탑스포츠(6110.HK)·TJX·로스·벌링턴·럭스익스피리언스(LUXE)
     (글로벌 유통), 쿠팡(CPNG, 국내 유통). 재무 통화(fin_currency) 별도 기록 — 야후 currency는
     주가 통화라 중국 기업(안타·리닝·탑스포츠 위안)·마이테레사(유로) 재무 단위가 틀리게 표시되던 문제
v4.6: 세노미 리테일(4240.SR, 사우디 상장) 추가 — 소싱 지도 중동 현지 유통사.
     종목마다 수집 결과 한 줄 로그(연간·재고·주가 유무) — 빈 데이터 조기 발견용
v4.5: 닥터마틴(DOCS.L, 런던 상장) 추가 — 글로벌 브랜드
v4.4: 환율 — 원화 직접 쌍 이력이 1년이 안 돼 1년 전 값이 비면(브라질 헤알) 달러 경유로 대체
v4.3: 소싱 지도 2단계 — 현지 유통사 3곳 추가(프레이저스·잘란도·그루포 SBF, 글로벌 유통)와
     환율 수집(유로·파운드·달러·브라질 헤알 대비 원화, 최근값과 1년 전 값) → data.json 'fx'
v4.2: 블랙야크아이앤씨(478560) 추가 — 시장(코스피/코스닥) 미확인이라 .KS 실패 시 .KQ 자동 재시도
     (한국 종목 공통), 실제 조회된 티커를 기록
v4.1: 신성통상(005390) 제외 — 2025년 자진 상장폐지 확인, Phase 6 비상장 DART 대상으로 이동
v4: 국내 상장 20개사 추가(총 42종목→41), 그룹 6개로 세분(글로벌 브랜드/글로벌 유통/
    국내 브랜드/국내 패션대기업/국내 OEM/국내 유통), 종목별 주석(note) 필드
v3: 브랜드 8종 추가 — 미즈노(8022.T)·요넥스(7906.T)·골드윈(8111.T)·
    안타스포츠(2020.HK)·리닝(2331.HK)·푸마(PUM.DE)·울버린(WWW)·컬럼비아(COLM)
    → 총 22종목 (브랜드 19 + 유통 3)
yfinance로 3개년 재무(매출/GM/영업률/재고) + 분기YoY + 주가(부지표) + 실적일 수집
출력: docs/data.json
§29-D: 조회 실패 항목은 null(대시보드에서 '미확인' 표기), 임의 수치 생성 금지
"""

import os
import json
import math
import datetime
import yfinance as yf

# ────────────────────────────────────────────────
# 감시 대상 (티커: [한글명, 구분])  ※ 확장 시 이 블록에 한 줄 추가
# ────────────────────────────────────────────────
WATCH = {
    # ── 글로벌 브랜드 ──
    "NKE":     ["나이키", "글로벌 브랜드"],
    "ADS.DE":  ["아디다스", "글로벌 브랜드"],
    "ONON":    ["온홀딩", "글로벌 브랜드"],
    "DECK":    ["데커스(HOKA)", "글로벌 브랜드"],
    "AS":      ["아머스포츠", "글로벌 브랜드"],
    "LULU":    ["룰루레몬", "글로벌 브랜드"],
    "7936.T":  ["아식스", "글로벌 브랜드"],
    "BIRK":    ["버켄스탁", "글로벌 브랜드"],
    "CROX":    ["크록스", "글로벌 브랜드"],
    "VFC":     ["VF Corp", "글로벌 브랜드"],
    "UAA":     ["언더아머", "글로벌 브랜드"],
    "8022.T":  ["미즈노", "글로벌 브랜드"],
    "7906.T":  ["요넥스", "글로벌 브랜드"],
    "8111.T":  ["골드윈", "글로벌 브랜드"],
    "2020.HK": ["안타스포츠", "글로벌 브랜드"],
    "2331.HK": ["리닝", "글로벌 브랜드"],
    "PUM.DE":  ["푸마", "글로벌 브랜드"],
    "WWW":     ["울버린(새코니)", "글로벌 브랜드"],
    "COLM":    ["컬럼비아", "글로벌 브랜드"],
    "DOCS.L":  ["닥터마틴", "글로벌 브랜드", "영국 · 부츠·신발, 3월 결산"],
    "EL.PA":   ["에실로룩소티카", "글로벌 브랜드", "아이웨어 · 레이밴·오클리 + 명품 라이선스, 한국 법인 룩소티카코리아"],
    "SFL.MI":  ["사필로", "글로벌 브랜드", "아이웨어 · 카레라·폴라로이드 + 패션 브랜드 라이선스"],
    "456A.T":  ["휴먼메이드", "글로벌 브랜드", "일본 · 니고의 스트리트 브랜드, 2025.11 도쿄 그로스 상장"],
    "0933.HK": ["비바굿즈(클락스)", "글로벌 브랜드", "홍콩 · 클락스 대주주(리닝 일가) — 보시니 등 포함 연결 수치"],
    "VULC3.SA": ["불카브라스", "글로벌 브랜드", "브라질 · 올림피쿠스 + 언더아머·미즈노 브라질 라이선스"],
    # ── 글로벌 유통 ──
    "DKS":     ["딕스+풋락커", "글로벌 유통"],
    "JD.L":    ["JD스포츠", "글로벌 유통"],
    "ASO":     ["아카데미스포츠", "글로벌 유통"],
    "FRAS.L":  ["프레이저스(스포츠다이렉트)", "글로벌 유통", "영국 · 스포츠다이렉트 등 운영, 할인 판매 비중 큼"],
    "ZAL.DE":  ["잘란도", "글로벌 유통", "독일 · 유럽 최대 온라인 패션몰, 오프프라이스 '라운지' 운영"],
    "SBFG3.SA": ["그루포 SBF(센타우로)", "글로벌 유통", "브라질 · 센타우로 매장, 나이키 브라질 유통(피지아)"],
    "4240.SR": ["세노미 리테일", "글로벌 유통", "사우디 · 해외 패션 브랜드 프랜차이즈 매장 운영(구 알호카이르)"],
    "LUXE":    ["럭스익스피리언스(마이테레사)", "글로벌 유통", "독일 · 마이테레사·네타포르테·육스 — 명품·디자이너 온라인, 6월 결산"],
    "2670.T":  ["ABC마트", "글로벌 유통", "일본 · 신발 멀티숍, 에이비씨마트코리아 모회사, 2월 결산"],
    "6110.HK": ["탑스포츠", "글로벌 유통", "중국 · 나이키·아디다스 매장 운영 1위, 나이키가 2027년부터 온라인 판매 종료 통보(2026.7), 2월 결산"],
    "TJX":     ["TJX", "글로벌 유통", "미국 · TJ맥스·마셜스 — 오프프라이스(브랜드 재고 처분) 1위, 1월 결산"],
    "ROST":    ["로스스토어", "글로벌 유통", "미국 · 오프프라이스 2위, 1월 결산"],
    "BURL":    ["벌링턴", "글로벌 유통", "미국 · 오프프라이스 3위, 1월 결산"],
    # ── 국내 브랜드 ──
    "081660.KS": ["휠라홀딩스", "국내 브랜드", "휠라·케이스위스·아쿠쉬네트(타이틀리스트)"],
    "383220.KS": ["F&F", "국내 브랜드", "MLB·디스커버리·듀베티카, 중국 비중 큼"],
    "298540.KQ": ["더네이쳐홀딩스", "국내 브랜드", "내셔널지오그래픽·마크곤잘레스 라이선스"],
    "120110.KS": ["코오롱인더", "국내 브랜드", "코오롱스포츠·헤드 — 산업자재 비중 큼, 패션은 부문"],
    "337930.KQ": ["브랜드엑스(젝시믹스)", "국내 브랜드", "애슬레저 — 룰루레몬 국내 대응 지표"],
    "000680.KS": ["LS네트웍스(프로스펙스)", "국내 브랜드", "토종 스포츠 브랜드, 유통·기타 사업 혼재"],
    "036620.KQ": ["감성코퍼레이션", "국내 브랜드", "스노우피크 어패럴 라이선스"],
    "278470.KS": ["에이피알(널디)", "국내 브랜드", "뷰티 디바이스 비중이 큼 — 널디는 일부"],
    "478560.KS": ["블랙야크아이앤씨", "국내 브랜드", "블랙야크 관련 상장사(2026 신규 확인) — 사업 범위 확인 필요, 비와이엔블랙야크(비상장)와 별개 법인"],
    # ── 국내 패션대기업 ──
    "031430.KS": ["신세계인터내셔날", "국내 패션대기업", "수입 브랜드·자체 브랜드·코스메틱"],
    "020000.KS": ["한섬", "국내 패션대기업", "타임·마인·시스템 등 자체 브랜드"],
    "093050.KS": ["LF", "국내 패션대기업", "헤지스·닥스 등, 식품·금융 혼재"],
    "028260.KS": ["삼성물산(패션부문)", "국내 패션대기업", "빈폴·아미·메종키츠네 — 건설·상사 포함 연결 수치"],
    # ── 국내 OEM (브랜드 오더 선행지표) ──
    "111770.KS": ["영원무역", "국내 OEM", "노스페이스·룰루레몬·파타고니아 OEM — 아웃도어 생산량 선행"],
    "241590.KS": ["화승엔터프라이즈", "국내 OEM", "아디다스 신발 OEM — 아디다스 주문 선행"],
    "105630.KS": ["한세실업", "국내 OEM", "갭·타겟 등 미국 의류 OEM"],
    "009970.KS": ["영원무역홀딩스", "국내 OEM", "영원아웃도어(노스페이스 한국) 지분 — 간접 추적"],
    # ── 국내 유통 ──
    "023530.KS": ["롯데쇼핑", "국내 유통", "백화점·마트·이커머스 연결"],
    "004170.KS": ["신세계", "국내 유통", "백화점 중심"],
    "069960.KS": ["현대백화점", "국내 유통", "백화점·아울렛, 한섬 모회사"],
    "CPNG":    ["쿠팡", "국내 유통", "미국 상장(달러 실적) · 국내 최대 온라인 판매 채널"],
}
GROUP_ORDER = ["글로벌 브랜드", "글로벌 유통", "국내 브랜드",
               "국내 패션대기업", "국내 OEM", "국내 유통"]
# 야후 조회 티커 대체표(v4.12) — 항목 키(history·dart_fetch가 씀)는 그대로 두고 조회만 바꿈.
#   블랙야크아이앤씨는 코스닥 확인됨 → .KS 404·재시도 로그가 매일 찍히던 것 제거
YF_ALIAS = {"478560.KS": "478560.KQ"}

KST = datetime.timezone(datetime.timedelta(hours=9))
SCRIPT = "fetch_data"

# 환율 (소싱 지도: 현지 통화 1단위 = 원화 몇 원) — 코드: [표시명, 야후 티커]
#   중동(디르함·리얄)은 달러에 고정이라 달러로 대신함
FX = {
    "EUR": ["유로", "EURKRW=X"],
    "GBP": ["파운드", "GBPKRW=X"],
    "USD": ["달러", "USDKRW=X"],
    "BRL": ["브라질 헤알", "BRLKRW=X"],
    "JPY": ["엔", "JPYKRW=X"],
    # v4.11 원화 환산용(값만 표시)
    "CHF": ["스위스 프랑", "CHFKRW=X"],
    "CNY": ["위안", "CNYKRW=X"],
    "HKD": ["홍콩 달러", "HKDKRW=X"],
    "SAR": ["사우디 리얄", None],    # v4.12 직접 조회 안 함(SARKRW=X 매일 404) — 달러 환율 ÷ 3.75
}
SAR_PEG = 3.75   # 1달러 = 3.75리얄(고정)
# 1% 칸 알림 대상(v4.9) — 파운드·헤알은 값만 표시
FX_ALERT = ["JPY", "EUR", "USD"]
FX_ALERT_LABEL = {"JPY": "엔(100엔)", "EUR": "유로", "USD": "달러"}
FX_LOOKBACK = 30      # 최근 30영업일 안에 이미 닿은 선은 다시 알리지 않음
FX_MIN_POINTS = 200   # 1년 평균 계산에 필요한 최소 일수
FX_HINT = {"dn": "▼ 매입 부담 줄어듦 — 결제 시점 앞당김·선매입 검토 참고",
           "up": "▲ 매입 부담 커짐 — 선물환·결제 시점·수출 비중 검토 참고"}


def _row(df, names):
    if df is None or getattr(df, "empty", True):
        return None
    for n in names:
        if n in df.index:
            return df.loc[n]
    return None


def _num(v):
    try:
        f = float(v)
        if f != f:
            return None
        return f
    except Exception:
        return None


def _vals(df, names):
    """v4.12: 열(연도·분기)마다 names 순서로 처음 있는 값 — 행 단위가 아니라 값 단위 대체
    (예: 'Operating Income' 행은 있어도 그해 값이 비면 같은 열의 'Total Operating Income As Reported').
    반환: {열: 값 또는 None}, 해당 행이 하나도 없으면 None"""
    if df is None or getattr(df, "empty", True):
        return None
    rows = [df.loc[n] for n in names if n in df.index]
    if not rows:
        return None
    out = {}
    for c in df.columns:
        v = None
        for r in rows:
            v = _num(r.get(c))
            if v is not None:
                break
        out[c] = v
    return out


def _day(c):
    """열 이름 → 날짜. 날짜가 아니면(NaT 등) None — 그 열만 건너뛰고 종목 전체를 실패로 만들지 않음"""
    try:
        return datetime.date.fromisoformat(str(c)[:10])
    except ValueError:
        return None


def soft_fail(msg):
    """심각한 실패 표시 — 저장은 하되 워크플로우 마지막 단계가 빨간 X로 끝내 점검 알림이 가게 함"""
    print(f"실패 표시: {msg}", flush=True)
    with open("soft_fail.txt", "a", encoding="utf-8") as f:
        f.write(f"{SCRIPT}: {msg}\n")


def fetch_one(ticker, name, group, note=None):
    d = {"ticker": ticker, "name": name, "group": group, "note": note,
         "currency": None, "fin_currency": None, "fy": [],
         "latest_q_yoy": None, "q_end": None, "q_prev_end": None,
         "inventory": None, "inv_yoy": None, "inv_sales_pct": None,
         "inv_date": None, "inv_prev_date": None,
         # v4.13 분기 재고(동기간 비교): 최신 분기 재고 vs 1년 전 같은 분기 + 같은 분기 매출 증감
         "q_inv": None, "q_inv_date": None, "q_inv_prev_date": None,
         "q_inv_yoy": None, "q_inv_rev_yoy": None,
         "price": None, "off_high_pct": None, "earn_date": None,
         "error": None}
    try:
        tk = yf.Ticker(ticker)

        # ── 연간 손익 3개년 ──
        inc = tk.income_stmt
        rev_v = _vals(inc, ["Total Revenue", "Operating Revenue"])
        gp_v = _vals(inc, ["Gross Profit"]) or {}
        op_v = _vals(inc, ["Operating Income",
                           "Total Operating Income As Reported"]) or {}
        if rev_v is not None:
            cols = sorted(inc.columns)
            years = []
            for c in cols:
                years.append({
                    "end": str(c)[:10],
                    "rev": rev_v.get(c),
                    "gp": gp_v.get(c),
                    "op": op_v.get(c),
                })
            for i, y in enumerate(years):
                prev = years[i - 1]["rev"] if i > 0 else None
                y["rev_yoy"] = ((y["rev"] / prev - 1) * 100) if (y["rev"] and prev) else None
                y["gm_pct"] = (y["gp"] / y["rev"] * 100) if (y["gp"] and y["rev"]) else None
                y["op_pct"] = (y["op"] / y["rev"] * 100) if (y["op"] and y["rev"]) else None
            d["fy"] = years[-3:]

        # ── 최근 분기 매출 YoY (기준일 포함) ──
        # v4.12: 열 순서(-1 vs -5)가 아니라 날짜로 짝지음 — 매출 값이 있는 최신 분기와 350~380일 전 분기
        #   (52/53주 회계연도 364·371일 포함). 야후 분기 열이 한 칸 빠지면 엉뚱한 분기와 비교되던 문제(푸마)
        qinc = tk.quarterly_income_stmt
        q_rev = _vals(qinc, ["Total Revenue", "Operating Revenue"])
        if q_rev:
            qs = sorted((e, v) for e, v in ((_day(c), v) for c, v in q_rev.items() if v) if e)
            if qs:
                q_end, cur = qs[-1]
                d["q_end"] = q_end.isoformat()
                # 로그 확인용(저장 안 함): 매출 있는 분기 열 수, 바로 앞 열과의 간격(180일 근처면 반기 자료)
                d["_q_cols"] = (len(qs), (q_end - qs[-2][0]).days if len(qs) > 1 else None)
                pair = [(abs((q_end - e).days - 365), e, v) for e, v in qs[:-1]
                        if 350 <= (q_end - e).days <= 380]
                if pair:
                    _, pe, prv = min(pair)
                    d["q_prev_end"] = pe.isoformat()
                    d["latest_q_yoy"] = (cur / prv - 1) * 100

        # ── 재고 (기준일 포함) ──
        bs = tk.balance_sheet
        inv_r = _row(bs, ["Inventory", "Inventories"])
        if inv_r is not None:
            bcols = sorted(bs.columns)
            if len(bcols) >= 1:
                inv_now = _num(inv_r.get(bcols[-1]))
                d["inventory"] = inv_now
                d["inv_date"] = str(bcols[-1])[:10]
                if len(bcols) >= 2:
                    inv_prev = _num(inv_r.get(bcols[-2]))
                    d["inv_prev_date"] = str(bcols[-2])[:10]
                    if inv_now and inv_prev:
                        d["inv_yoy"] = (inv_now / inv_prev - 1) * 100
                last_rev = d["fy"][-1]["rev"] if d["fy"] else None
                if inv_now and last_rev:
                    d["inv_sales_pct"] = inv_now / last_rev * 100

        # ── v4.13 분기 재고 — 최신 분기 vs 1년 전 같은 분기(350~380일, 분기 매출과 같은 짝짓기) ──
        #   연간 재고(위)는 그대로 두고 따로 저장(쌓아 온 기록의 뜻이 바뀌지 않게). 같은 분기 매출 증감도 함께 —
        #   재고 경고·소싱 지도가 '같은 기간 재고 vs 같은 기간 매출'로 비교하도록. 실패해도 종목 전체는 정상
        try:
            q_inv = _vals(tk.quarterly_balance_sheet, ["Inventory", "Inventories"])
        except Exception:
            q_inv = None
        if q_inv:
            qi = sorted((e, v) for e, v in ((_day(c), v) for c, v in q_inv.items() if v) if e)
            d["_qi_cols"] = len(qi)
            if qi:
                ie, iv = qi[-1]
                pair = [(abs((ie - e).days - 365), e, v) for e, v in qi[:-1] if 350 <= (ie - e).days <= 380]
                if pair:
                    _, pe, pv = min(pair)
                    d.update(q_inv=iv, q_inv_date=ie.isoformat(), q_inv_prev_date=pe.isoformat(),
                             q_inv_yoy=(iv / pv - 1) * 100)
                    if q_rev:   # 같은 분기 매출(재무상태표·손익 열 날짜가 며칠 다를 수 있어 7일 안에서 찾음)
                        qr = [(e, v) for e, v in ((_day(c), v) for c, v in q_rev.items() if v) if e]
                        near = lambda day: next((v for e, v in qr if abs((e - day).days) <= 7), None)
                        rc, rp = near(ie), near(pe)
                        if rc and rp:
                            d["q_inv_rev_yoy"] = (rc / rp - 1) * 100

        # ── 주가 (부지표) ──
        hist = tk.history(period="1y")
        if hist is not None and not hist.empty:
            closes = hist["Close"].dropna()
            last = float(closes.iloc[-1])
            d["price"] = last
            d["off_high_pct"] = (last / float(closes.max()) - 1) * 100
        try:
            d["currency"] = tk.fast_info.get("currency", None)
        except Exception:
            pass
        # 재무제표 통화(주가 통화와 다를 수 있음: 홍콩 상장 중국 기업=CNY, LUXE=EUR)
        try:
            d["fin_currency"] = (tk.info or {}).get("financialCurrency")
        except Exception:
            pass

        # ── 다음 실적 발표일 ──
        try:
            cal = tk.calendar
            dates = cal.get("Earnings Date") if isinstance(cal, dict) else None
            if dates:
                today = datetime.datetime.now(KST).date()
                future = [x for x in dates
                          if isinstance(x, datetime.date) and x >= today]
                if future:
                    d["earn_date"] = min(future).isoformat()
        except Exception:
            pass

    except Exception as e:
        d["error"] = (str(e) or type(e).__name__)[:200]
        print(f"[WARN] {ticker} 실패: {e}")
    return d


def _fx_series(tk):
    # v4.9: 2년+α (1% 칸 알림의 1년 이동평균을 지난 1년 내내 계산하려면 2년 필요)
    start = (datetime.date.today() - datetime.timedelta(days=800)).isoformat()
    h = yf.Ticker(tk).history(start=start, interval="1d")
    return h["Close"].dropna() if h is not None and not h.empty else None


def _cross_series(code, usd):
    """달러 경유: 현지통화→달러 × 달러→원화"""
    cross = _fx_series(f"{code}USD=X")
    if usd is None or cross is None:
        return None
    return (cross * usd.reindex(cross.index, method="ffill")).dropna()


def _year_ago(s):
    """365일 이전 가장 가까운 날 종가 (이력이 1년이 안 되면 None)"""
    prev = s[s.index <= s.index[-1] - datetime.timedelta(days=365)]
    return float(prev.iloc[-1]) if len(prev) else None


def _line_txt(line):
    """1% 선 이름: 0 → '1년 평균', -4 → '−4% 선', 2 → '+2% 선'"""
    if line == 0:
        return "1년 평균"
    return f"{'+' if line > 0 else '−'}{abs(line)}% 선"


def fx_levels(s):
    """1% 칸 알림(v4.9): 1년 이동평균 대비 %(dev)를 1% 선으로 나눠, 최근 30영업일 안에
    닿지 않았던 선을 새로 넘은 날을 알림으로 기록. 반환: 표시·알림용 dict (자료 부족 시 None)"""
    roll = s.rolling("365D").mean()
    cnt = s.rolling("365D").count()
    dev = (s / roll - 1) * 100
    ok = cnt >= FX_MIN_POINTS
    if not ok.iloc[-1]:
        return None
    dn_line = [math.ceil(v - 1e-9) for v in dev]    # 내려가며 넘은 가장 낮은 선
    up_line = [math.floor(v + 1e-9) for v in dev]   # 올라가며 넘은 가장 높은 선
    last_dt = s.index[-1]
    win_start = last_dt - datetime.timedelta(days=365)
    alerts = []
    for i in range(FX_LOOKBACK, len(s)):
        if s.index[i] <= win_start or not ok.iloc[i] or not ok.iloc[i - FX_LOOKBACK:i].all():
            continue
        if dn_line[i] < min(dn_line[i - FX_LOOKBACK:i]):
            d, line = "dn", dn_line[i]
        elif up_line[i] > max(up_line[i - FX_LOOKBACK:i]):
            d, line = "up", up_line[i]
        else:
            continue
        alerts.append({"date": s.index[i].strftime("%Y-%m-%d"), "dir": d, "line": line,
                       "rate": round(float(s.iloc[i]), 4), "dev": round(float(dev.iloc[i]), 2)})
    avg = float(roll.iloc[-1])
    recent = dev.iloc[-FX_LOOKBACK:]
    return {
        "hist": [[t.strftime("%Y-%m-%d"), round(float(v), 4)] for t, v in s[s.index > win_start].items()],
        "avg1y": round(avg, 4),
        "dev_pct": round(float(dev.iloc[-1]), 2),
        "next_dn": round(avg * (1 + (dn_line[-1] - 1) / 100), 4),
        "next_up": round(avg * (1 + (up_line[-1] + 1) / 100), 4),
        "seen30": [round(float(recent.min()), 2), round(float(recent.max()), 2)],
        "alerts": alerts,
    }


def fx_rate_txt(code, rate):
    return f"{rate * 100:,.0f}" if code == "JPY" else f"{rate:,.0f}"


def mark_first_seen(fx, prev_fx, today):
    """알림마다 처음 잡힌 날(KST) — 이전 data.json에서 이어받음. 첫 배포 때는 최근 4일 안 알림만 '오늘'"""
    recent = (today - datetime.timedelta(days=4)).isoformat()
    for code in FX_ALERT:
        cur = fx.get(code) or {}
        if not cur.get("alerts"):
            continue
        prev_list = (prev_fx.get(code) or {}).get("alerts")
        prev = {(a["date"], a["dir"], a["line"]): a.get("first_seen") for a in (prev_list or [])}
        for a in cur["alerts"]:
            k = (a["date"], a["dir"], a["line"])
            if prev.get(k):
                a["first_seen"] = prev[k]
            elif prev_list is not None or a["date"] >= recent:
                a["first_seen"] = today.isoformat()
            else:
                a["first_seen"] = a["date"]


def build_fx_push(fx, today):
    """오늘 새로 잡힌 알림(first_seen=오늘, 시장 날짜 4일 이내) → 휴대폰 알림 문구. 없으면 None"""
    t, recent = today.isoformat(), (today - datetime.timedelta(days=4)).isoformat()
    items = []
    for code in FX_ALERT:
        for a in (fx.get(code) or {}).get("alerts") or []:
            if a.get("first_seen") == t and a["date"] >= recent:
                items.append({**a, "code": code})
    if not items:
        return None
    lines = ["💱 매입 환율 알림"]
    for a in items:
        lines.append(f"{FX_ALERT_LABEL[a['code']]} {fx_rate_txt(a['code'], a['rate'])}원 — "
                     f"1년 평균 대비 {_line_txt(a['line'])} {'아래로' if a['dir'] == 'dn' else '위로'} "
                     f"({'+' if a['dev'] >= 0 else '−'}{abs(a['dev']):.1f}%)")
    for d in ("dn", "up"):
        if any(a["dir"] == d for a in items):
            lines.append(FX_HINT[d])
    return {"date": t, "items": items, "text": "\n".join(lines)}


def fetch_fx(prev_fx=None, prev_date=None):
    """환율: 최근 종가와 1년 전(365일 이전 가장 가까운 날) 종가, 변동률.
    원화 직접 쌍이 비거나 이력이 1년이 안 되면 달러 경유(현지통화→달러 × 달러→원화)로 계산.
    v4.12: 수집 실패한 통화는 이전 data.json 값(1% 칸 알림 목록 포함)을 이어 쓰고 stale_since 표시
    — 알림 first_seen이 끊기지 않아 다음 날 같은 알림이 다시 나가지 않음. 감시 통화는 값을 받았어도 1% 칸 계산이
    예외·자료 부족이면 실패로 보고 같은 방식(이전 값이 있을 때). 리얄은 직접 조회 없이 달러 ÷ 3.75"""
    prev_fx = prev_fx or {}
    out = {}
    usd = None
    for code, (name, tk) in FX.items():
        if tk is None:      # 리얄: 아래에서 달러로 계산
            continue
        p_code = prev_fx.get(code) or {}
        try:
            s = _fx_series(tk)
            via = None
            has_s = s is not None and not s.empty
            if code != "USD" and (not has_s or _year_ago(s) is None):
                if has_s:
                    print(f"  환율 {code}: 원화 직접 쌍 이력 {s.index[0]:%Y-%m-%d}부터 {len(s)}일 "
                          f"— 1년 전 값 없음, 달러 경유 시도")
                try:
                    if usd is None:
                        usd = _fx_series("USDKRW=X")
                    c = _cross_series(code, usd)
                except Exception as e:      # 경유 실패해도 직접 쌍(현재값)은 유지
                    c = None
                    print(f"  환율 {code} 달러 경유 실패: {str(e)[:100]}")
                # 직접 쌍이 있으면 달러 경유가 1년 전 값까지 있을 때만 대체
                if c is not None and not c.empty and (not has_s or _year_ago(c) is not None):
                    s, via = c, "달러 경유"
            if s is None or s.empty:
                print(f"  환율 {code} 없음")
                continue
            last_dt = s.index[-1]
            last = float(s.iloc[-1])
            yago = _year_ago(s)
            out[code] = {"name": name, "rate": round(last, 4),
                         "yago": round(yago, 4) if yago else None,
                         "chg_pct": round((last / yago - 1) * 100, 2) if yago else None,
                         "asof": last_dt.strftime("%Y-%m-%d"), "via": via}
            print(f"  환율 {code}: {last:,.2f}원 (1년 전 대비 {out[code]['chg_pct']}%)"
                  f"{' · ' + via if via else ''}")
            if code in FX_ALERT:
                lv = fx_levels(s)
                if lv is None and "alerts" in p_code and p_code.get("rate"):
                    # 어제는 1% 칸 계산이 됐는데 오늘 자료가 짧음 → 오늘 값만 두면 알림 목록이 끊겨
                    # 다음 날 같은 알림이 다시 '오늘 처음'이 됨. 이전 값(알림 목록 포함)을 통째로 이어 씀(아래 keep_prev)
                    print(f"  환율 {code}: 1년 평균 계산 자료 부족 ({len(s)}일) — 1% 칸 알림 목록 끊김 방지로 이전 값 사용")
                    out.pop(code, None)
                elif lv is None:
                    print(f"  환율 {code}: 1년 평균 계산 자료 부족 ({len(s)}일) — 1% 칸 알림 건너뜀")
                else:
                    out[code].update(lv)
                    al = lv["alerts"]
                    n_dn = sum(1 for a in al if a["dir"] == "dn")
                    print(f"  환율 {code}: 1년 평균 {lv['avg1y']:,.4f} 대비 {lv['dev_pct']:+.1f}% · "
                          f"지난 1년 알림 {len(al)}건(내림 {n_dn}·오름 {len(al) - n_dn})"
                          + (f" · 최근 {al[-1]['date']} {_line_txt(al[-1]['line'])} "
                             f"{'아래로' if al[-1]['dir'] == 'dn' else '위로'}" if al else ""))
        except Exception as e:
            print(f"  환율 {code} 실패: {str(e)[:100]}")
            # 값은 받았는데 1% 칸 계산 등에서 예외 → 반쪽 값(알림 목록 없음) 대신 이전 값을 이어 씀(아래 keep_prev).
            # 이전 값이 없으면 받은 값이라도 둠
            if p_code.get("rate"):
                out.pop(code, None)

    def keep_prev(code):
        p = prev_fx.get(code) or {}
        if not p.get("rate"):
            return
        out[code] = {**p, "stale_since": p.get("stale_since") or prev_date}
        print(f"  환율 {code}: 이전 값 이어 씀 {p['rate']:,.2f}원 ({out[code]['stale_since']} 수집분)", flush=True)

    for code, (name, tk) in FX.items():
        if tk is not None and code not in out:
            keep_prev(code)
    u = out.get("USD") or {}
    if u.get("rate"):
        out["SAR"] = {"name": FX["SAR"][0], "rate": round(u["rate"] / SAR_PEG, 4),
                      "yago": round(u["yago"] / SAR_PEG, 4) if u.get("yago") else None,
                      "chg_pct": u.get("chg_pct"), "asof": u.get("asof"), "via": f"달러 고정 {SAR_PEG}"}
        if u.get("stale_since"):     # 달러가 이전 값이면 리얄도 이전 값
            out["SAR"]["stale_since"] = u["stale_since"]
        print(f"  환율 SAR: {out['SAR']['rate']:,.2f}원 · 달러 고정 {SAR_PEG}으로 계산", flush=True)
    else:
        keep_prev("SAR")
    return {c: out[c] for c in FX if c in out}      # 순서는 FX 표 그대로


def load_prev():
    """이전 data.json(v4.12 이어 쓰기·알림 first_seen용) → (종목별 항목, fx, 수집 날짜). 없거나 깨지면 빈 값"""
    try:
        with open("docs/data.json", encoding="utf-8") as f:
            prev = json.load(f)
    except Exception:
        return {}, {}, None
    items = {it["ticker"]: it for it in prev.get("items") or [] if isinstance(it, dict) and it.get("ticker")}
    ga = str(prev.get("generated_at") or "")[:10]
    try:
        pdate = datetime.date.fromisoformat(ga).isoformat()
    except ValueError:
        pdate = None
    return items, prev.get("fx") or {}, pdate


def _has_data(item):
    return bool((item or {}).get("fy")) or (item or {}).get("price") is not None


def fill_same_end(item, prev):
    """v4.12: 야후가 같은 결산일의 총이익·영업이익을 어떤 날만 비우면(푸마 영업이익률) 이전 data.json 값을 이어 씀.
    매출이 같은(0.5% 이내) 연도만 — 재작성 등으로 매출이 바뀌었으면 섞지 않음. 반환: 채운 항목 목록"""
    pm = {y.get("end"): y for y in (prev or {}).get("fy") or []}
    got = []
    for y in item.get("fy") or []:
        p = pm.get(y.get("end")) or {}
        if not (y.get("rev") and p.get("rev")) or abs(p["rev"] / y["rev"] - 1) > 0.005:
            continue
        for k, pk in (("gp", "gm_pct"), ("op", "op_pct")):
            if y.get(k) is None and p.get(k) is not None:
                y[k] = p[k]
                y[pk] = (y[k] / y["rev"] * 100) if y[k] else None
                got.append(f"{y['end'][:4]} {k}")
    return got


def main():
    today = datetime.datetime.now(KST).date()
    prev_items, prev_fx, prev_date = load_prev()
    prev_date = prev_date or today.isoformat()
    out = {"generated_at":
           datetime.datetime.now(KST).strftime("%Y-%m-%d %H:%M KST"),
           "items": []}
    n_ok, kept, failed = 0, [], []
    for ticker, spec in WATCH.items():
        name, group = spec[0], spec[1]
        note = spec[2] if len(spec) > 2 else None
        yf_tk = YF_ALIAS.get(ticker, ticker)
        print(f"fetch {ticker} ({name}){' → ' + yf_tk if yf_tk != ticker else ''} ...", flush=True)
        item = fetch_one(yf_tk, name, group, note)
        if yf_tk != ticker:                       # 대체표: 키는 원래 티커, 조회 티커는 따로 기록
            item["ticker"] = ticker
            item["yf_ticker"] = yf_tk
        # 한국 종목: 시장 접미사가 틀리면 데이터가 비므로 반대 접미사로 1회 재시도
        elif (item.get("error") or not item.get("fy")) and ticker[-3:] in (".KS", ".KQ"):
            alt = ticker[:-3] + (".KQ" if ticker.endswith(".KS") else ".KS")
            print(f"  → {ticker} 비어 있음, {alt} 재시도", flush=True)
            item2 = fetch_one(alt, name, group, note)
            if item2.get("fy") or item2.get("price") is not None:
                item2["ticker"] = ticker          # 대시보드 키는 원래 티커 유지
                item2["yf_ticker"] = alt
                item = item2
        q_cols = item.pop("_q_cols", None)        # 로그용(저장 안 함)
        qi_cols = item.pop("_qi_cols", None)
        # v4.12: 수집 실패(예외, 또는 연간 재무·주가 둘 다 없음) → 이전 data.json 값 이어 쓰기
        prev = prev_items.get(ticker)
        why = item.get("error") or (None if _has_data(item) else "연간 재무·주가 없음")
        if why and _has_data(prev):
            item = {**prev, "name": name, "group": group, "note": note,
                    "stale_since": prev.get("stale_since") or prev_date}
            kept.append(ticker)
            print(f"  ↳ 수집 실패({why[:80]}) — 이전 값 이어 씀({item['stale_since']} 수집분)", flush=True)
            out["items"].append(item)
            continue
        if not _has_data(item):                   # 이전 값도 없고 오늘 값도 없음 → '값 없음'
            item["error"] = why
            failed.append(ticker)
            print(f"  ↳ 수집 실패({why[:80]}) — 이전 값도 없음", flush=True)
            out["items"].append(item)
            continue
        if why:     # 예외가 났지만 연간 재무·주가 중 받은 값이 있고 이전 값은 없음 → 받은 값 저장(정상으로 셈, error는 남김)
            print(f"  ↳ 일부 실패({why[:80]}) — 이전 값이 없어 받은 값만 저장", flush=True)
        n_ok += 1
        got = fill_same_end(item, prev)
        if got:
            print(f"  ↳ 오늘 빈 값은 같은 결산일 이전 값으로: {', '.join(got)}", flush=True)
        q_txt = ""
        if item.get("q_end"):
            q_txt = f" · 분기 {item['q_end']} vs {item.get('q_prev_end') or '전년 짝 없음'}"
            if q_cols:      # 매출 있는 분기 열 수·바로 앞 열 간격(180일 근처면 반기 자료 — 실데이터 확인용)
                q_txt += f" (열 {q_cols[0]}개" + (f", 앞 열과 {q_cols[1]}일)" if q_cols[1] else ")")
        if item.get("q_inv_date"):     # v4.13 분기 재고 동기간 짝
            q_txt += (f" · 재고 분기 {item['q_inv_date']} vs {item['q_inv_prev_date']} ({item['q_inv_yoy']:+.1f}%"
                      + (f" · 같은 분기 매출 {item['q_inv_rev_yoy']:+.1f}%)" if item.get("q_inv_rev_yoy") is not None else ")"))
        elif qi_cols is not None:
            q_txt += f" · 재고 분기 짝 없음(열 {qi_cols}개)"
        print(f"  ↳ 연간 {len(item['fy'])}개 · 재고 {'O' if item.get('inventory') else '-'} · "
              f"주가 {'O' if item.get('price') is not None else '-'} · "
              f"통화 {item.get('currency') or '-'}/재무 {item.get('fin_currency') or '-'}" + q_txt, flush=True)
        out["items"].append(item)
    out["group_order"] = GROUP_ORDER
    print("fetch 환율 ...", flush=True)
    out["fx"] = fetch_fx(prev_fx, prev_date)
    mark_first_seen(out["fx"], prev_fx, today)
    out["fx_push"] = build_fx_push(out["fx"], today)
    print(f"  환율 알림: 오늘 새 알림 {len(out['fx_push']['items']) if out['fx_push'] else 0}건", flush=True)
    fx_kept = [c for c, v in out["fx"].items() if v.get("stale_since")]
    fx_failed = [c for c in FX if c not in out["fx"]]
    out["fetch_status"] = {"date": today.isoformat(), "ok": n_ok, "kept": kept, "failed": failed,
                           "fx_kept": fx_kept, "fx_failed": fx_failed}
    # '실패' 대신 '값 없음'(화면 수집 상태와 같은 말) — 정상인 날 로그에 '실패' 글자가 매일 찍히지 않게
    print(f"수집 결과: 정상 {n_ok} · 이전 값 {len(kept)} · 값 없음 {len(failed)}"
          + (f" · 환율 이전 값 {', '.join(fx_kept)}" if fx_kept else "")
          + (f" · 환율 없음 {', '.join(fx_failed)}" if fx_failed else ""), flush=True)
    if kept or failed:
        print(f"  이전 값: {', '.join(kept) or '-'} / 값 없음: {', '.join(failed) or '-'}", flush=True)
    os.makedirs("docs", exist_ok=True)
    with open("docs/data.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("saved docs/data.json")
    # 심각한 실패 → soft_fail.txt (저장은 했고, 워크플로우 마지막 단계가 빨간 X로 끝냄)
    if len(kept) + len(failed) > len(WATCH) / 2:
        soft_fail(f"종목 {len(kept) + len(failed)}/{len(WATCH)}곳 수집 실패"
                  f"(이전 값 {len(kept)} · 값 없음 {len(failed)})")
    bad_fx = [c for c in FX_ALERT if c in fx_kept or c in fx_failed]
    if bad_fx:
        soft_fail(f"감시 환율 수집 실패 — {', '.join(bad_fx)}"
                  f"({'이전 값 사용' if all(c in fx_kept for c in bad_fx) else '일부 값 없음'})")


if __name__ == "__main__":
    main()

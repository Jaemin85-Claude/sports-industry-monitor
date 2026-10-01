# -*- coding: utf-8 -*-
"""
sports-industry-monitor — Phase 1 데이터 수집 (v4)
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
    # ── 글로벌 유통 ──
    "DKS":     ["딕스+풋락커", "글로벌 유통"],
    "JD.L":    ["JD스포츠", "글로벌 유통"],
    "ASO":     ["아카데미스포츠", "글로벌 유통"],
    "FRAS.L":  ["프레이저스(스포츠다이렉트)", "글로벌 유통", "영국 · 스포츠다이렉트 등 운영, 할인 판매 비중 큼"],
    "ZAL.DE":  ["잘란도", "글로벌 유통", "독일 · 유럽 최대 온라인 패션몰, 오프프라이스 '라운지' 운영"],
    "SBFG3.SA": ["그루포 SBF(센타우로)", "글로벌 유통", "브라질 · 센타우로 매장, 나이키 브라질 유통(피지아)"],
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
}
GROUP_ORDER = ["글로벌 브랜드", "글로벌 유통", "국내 브랜드",
               "국내 패션대기업", "국내 OEM", "국내 유통"]

KST = datetime.timezone(datetime.timedelta(hours=9))

# 환율 (소싱 지도: 현지 통화 1단위 = 원화 몇 원) — 코드: [표시명, 야후 티커]
#   중동(디르함·리얄)은 달러에 고정이라 달러로 대신함
FX = {
    "EUR": ["유로", "EURKRW=X"],
    "GBP": ["파운드", "GBPKRW=X"],
    "USD": ["달러", "USDKRW=X"],
    "BRL": ["브라질 헤알", "BRLKRW=X"],
}


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


def fetch_one(ticker, name, group, note=None):
    d = {"ticker": ticker, "name": name, "group": group, "note": note,
         "currency": None, "fy": [],
         "latest_q_yoy": None, "q_end": None, "q_prev_end": None,
         "inventory": None, "inv_yoy": None, "inv_sales_pct": None,
         "inv_date": None, "inv_prev_date": None,
         "price": None, "off_high_pct": None, "earn_date": None,
         "error": None}
    try:
        tk = yf.Ticker(ticker)

        # ── 연간 손익 3개년 ──
        inc = tk.income_stmt
        rev_r = _row(inc, ["Total Revenue", "Operating Revenue"])
        gp_r = _row(inc, ["Gross Profit"])
        op_r = _row(inc, ["Operating Income",
                          "Total Operating Income As Reported"])
        if rev_r is not None:
            cols = sorted(inc.columns)
            years = []
            for c in cols:
                years.append({
                    "end": str(c)[:10],
                    "rev": _num(rev_r.get(c)),
                    "gp": _num(gp_r.get(c)) if gp_r is not None else None,
                    "op": _num(op_r.get(c)) if op_r is not None else None,
                })
            for i, y in enumerate(years):
                prev = years[i - 1]["rev"] if i > 0 else None
                y["rev_yoy"] = ((y["rev"] / prev - 1) * 100) if (y["rev"] and prev) else None
                y["gm_pct"] = (y["gp"] / y["rev"] * 100) if (y["gp"] and y["rev"]) else None
                y["op_pct"] = (y["op"] / y["rev"] * 100) if (y["op"] and y["rev"]) else None
            d["fy"] = years[-3:]

        # ── 최근 분기 매출 YoY (기준일 포함) ──
        qinc = tk.quarterly_income_stmt
        q_rev = _row(qinc, ["Total Revenue", "Operating Revenue"])
        if q_rev is not None:
            qcols = sorted(qinc.columns)
            if len(qcols) >= 5:
                cur = _num(q_rev.get(qcols[-1]))
                prv = _num(q_rev.get(qcols[-5]))
                d["q_end"] = str(qcols[-1])[:10]
                d["q_prev_end"] = str(qcols[-5])[:10]
                if cur and prv:
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
        d["error"] = str(e)[:200]
        print(f"[WARN] {ticker} 실패: {e}")
    return d


def _fx_series(tk):
    h = yf.Ticker(tk).history(period="13mo", interval="1d")
    return h["Close"].dropna() if h is not None and not h.empty else None


def fetch_fx():
    """환율: 최근 종가와 1년 전(365일 이전 가장 가까운 날) 종가, 변동률.
    원화 직접 쌍이 비면 달러 경유(현지통화→달러 × 달러→원화)로 계산"""
    out = {}
    usd = None
    for code, (name, tk) in FX.items():
        try:
            s = _fx_series(tk)
            via = None
            if (s is None or s.empty) and code != "USD":
                if usd is None:
                    usd = _fx_series("USDKRW=X")
                cross = _fx_series(f"{code}USD=X")
                if usd is not None and cross is not None:
                    s = (cross * usd.reindex(cross.index, method="ffill")).dropna()
                    via = "달러 경유"
            if s is None or s.empty:
                print(f"  환율 {code} 없음")
                continue
            last_dt = s.index[-1]
            last = float(s.iloc[-1])
            prev = s[s.index <= last_dt - datetime.timedelta(days=365)]
            yago = float(prev.iloc[-1]) if len(prev) else None
            out[code] = {"name": name, "rate": round(last, 4),
                         "yago": round(yago, 4) if yago else None,
                         "chg_pct": round((last / yago - 1) * 100, 2) if yago else None,
                         "asof": last_dt.strftime("%Y-%m-%d"), "via": via}
            print(f"  환율 {code}: {last:,.2f}원 (1년 전 대비 {out[code]['chg_pct']}%)")
        except Exception as e:
            print(f"  환율 {code} 실패: {str(e)[:100]}")
    return out


def main():
    out = {"generated_at":
           datetime.datetime.now(KST).strftime("%Y-%m-%d %H:%M KST"),
           "items": []}
    for ticker, spec in WATCH.items():
        name, group = spec[0], spec[1]
        note = spec[2] if len(spec) > 2 else None
        print(f"fetch {ticker} ({name}) ...", flush=True)
        item = fetch_one(ticker, name, group, note)
        # 한국 종목: 시장 접미사가 틀리면 데이터가 비므로 반대 접미사로 1회 재시도
        if (item.get("error") or not item.get("fy")) and ticker[-3:] in (".KS", ".KQ"):
            alt = ticker[:-3] + (".KQ" if ticker.endswith(".KS") else ".KS")
            print(f"  → {ticker} 비어 있음, {alt} 재시도", flush=True)
            item2 = fetch_one(alt, name, group, note)
            if item2.get("fy") or item2.get("price") is not None:
                item2["ticker"] = ticker          # 대시보드 키는 원래 티커 유지
                item2["yf_ticker"] = alt
                item = item2
        out["items"].append(item)
    out["group_order"] = GROUP_ORDER
    print("fetch 환율 ...", flush=True)
    out["fx"] = fetch_fx()
    os.makedirs("docs", exist_ok=True)
    with open("docs/data.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("saved docs/data.json")


if __name__ == "__main__":
    main()

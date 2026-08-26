# -*- coding: utf-8 -*-
"""
sports-industry-monitor — Phase 1 데이터 수집
yfinance로 14종목의 3개년 재무(매출/GM/영업률/재고) + 주가(부지표) + 실적일 수집
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
    "NKE":     ["나이키", "브랜드"],
    "ADS.DE":  ["아디다스", "브랜드"],
    "ONON":    ["온홀딩", "브랜드"],
    "DECK":    ["데커스(HOKA)", "브랜드"],
    "AS":      ["아머스포츠", "브랜드"],
    "LULU":    ["룰루레몬", "브랜드"],
    "7936.T":  ["아식스", "브랜드"],
    "BIRK":    ["버켄스탁", "브랜드"],
    "CROX":    ["크록스", "브랜드"],
    "VFC":     ["VF Corp", "브랜드"],
    "UAA":     ["언더아머", "브랜드"],
    "DKS":     ["딕스+풋락커", "유통"],
    "JD.L":    ["JD스포츠", "유통"],
    "ASO":     ["아카데미스포츠", "유통"],
}

KST = datetime.timezone(datetime.timedelta(hours=9))


def _row(df, names):
    """재무제표 DataFrame에서 계정 행 탐색 (명칭 변형 대응)"""
    if df is None or getattr(df, "empty", True):
        return None
    for n in names:
        if n in df.index:
            return df.loc[n]
    return None


def _num(v):
    try:
        f = float(v)
        if f != f:  # NaN
            return None
        return f
    except Exception:
        return None


def fetch_one(ticker, name, group):
    d = {"ticker": ticker, "name": name, "group": group,
         "currency": None, "fy": [], "latest_q_yoy": None,
         "inventory": None, "inv_yoy": None, "inv_sales_pct": None,
         "price": None, "off_high_pct": None, "earn_date": None,
         "error": None}
    try:
        tk = yf.Ticker(ticker)

        # ── 연간 손익 3개년 (+YoY 계산용 1년 추가) ──
        inc = tk.income_stmt
        rev_r = _row(inc, ["Total Revenue", "Operating Revenue"])
        gp_r = _row(inc, ["Gross Profit"])
        op_r = _row(inc, ["Operating Income", "Total Operating Income As Reported"])
        if rev_r is not None:
            cols = sorted(inc.columns)  # 과거→최신
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
            d["fy"] = years[-3:]  # 최근 3개년

        # ── 최근 분기 매출 YoY (5개 분기 필요) ──
        qinc = tk.quarterly_income_stmt
        q_rev = _row(qinc, ["Total Revenue", "Operating Revenue"])
        if q_rev is not None:
            qcols = sorted(qinc.columns)
            if len(qcols) >= 5:
                cur = _num(q_rev.get(qcols[-1]))
                prv = _num(q_rev.get(qcols[-5]))
                if cur and prv:
                    d["latest_q_yoy"] = (cur / prv - 1) * 100

        # ── 재고 (연간 최신 vs 전년) ──
        bs = tk.balance_sheet
        inv_r = _row(bs, ["Inventory", "Inventories"])
        if inv_r is not None:
            bcols = sorted(bs.columns)
            if len(bcols) >= 1:
                inv_now = _num(inv_r.get(bcols[-1]))
                d["inventory"] = inv_now
                if len(bcols) >= 2:
                    inv_prev = _num(inv_r.get(bcols[-2]))
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


def main():
    out = {"generated_at": datetime.datetime.now(KST).strftime("%Y-%m-%d %H:%M KST"),
           "items": []}
    for ticker, (name, group) in WATCH.items():
        print(f"fetch {ticker} ({name}) ...")
        out["items"].append(fetch_one(ticker, name, group))
    os.makedirs("docs", exist_ok=True)
    with open("docs/data.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("saved docs/data.json")


if __name__ == "__main__":
    main()

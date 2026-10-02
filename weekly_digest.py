# -*- coding: utf-8 -*-
"""
sports-industry-monitor — Phase 9: 주간 요약 (v1)
v1.1: 환율 줄에 '1년 평균 대비 %'(fetch_data v4.9) + 지난 7일 1% 칸 알림 목록
v1: 월요일 아침 주간 요약 — docs/*.json(현재)과 history.json·git 이력(7일 전 main)을 비교해 한 주 변화를 정리.
    출력: 기본 = 메일 본문(텍스트), --short = 휴대폰 알림용 3줄. 저장소에 아무것도 쓰지 않음(읽기 전용).
    매주 월 07:47(KST) 점검 전용 세션의 루틴이 실행 → Claude 앱 알림 + 대표 본인 Gmail로 발송.
§29-D: 파일에 있는 값만 비교·정렬, 없는 값은 '―'/생략(임의 수치 생성 금지)
"""

import os
import sys
import json
import datetime
import subprocess

KST = datetime.timezone(datetime.timedelta(hours=9))
DOCS = "docs"
DASH_URL = "https://jaemin85-claude.github.io/sports-industry-monitor/"
DAYS = 7


def load(name):
    try:
        with open(os.path.join(DOCS, name), encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def load_old(name, days=DAYS):
    """git 이력에서 N일 전 시점의 docs 파일(없으면 None)"""
    try:
        before = (datetime.datetime.now(KST) - datetime.timedelta(days=days)).isoformat()
        sha = subprocess.run(["git", "log", "-1", f"--before={before}", "--format=%H", "HEAD", "--", f"{DOCS}/{name}"],
                             capture_output=True, text=True, timeout=30).stdout.strip()
        if not sha:
            return None
        raw = subprocess.run(["git", "show", f"{sha}:{DOCS}/{name}"], capture_output=True, text=True, timeout=30).stdout
        return json.loads(raw) if raw else None
    except Exception:
        return None


def load_old_with(name, key):
    """7일 전 파일에 key가 없으면(수집 시작 전) 6일 전…1일 전 순으로 — (파일, 며칠 전)"""
    for d in range(DAYS, 0, -1):
        o = load_old(name, d)
        if o and o.get(key):
            return o, d
    return None, None


def pct(v, d=1):
    return "―" if v is None else f"{'+' if v > 0 else ''}{v:.{d}f}%"


def won(v):
    if v is None:
        return "―"
    return f"{v / 1e12:.2f}조" if abs(v) >= 1e12 else f"{v / 1e8:,.0f}억"


def price_moves(data, hist, today):
    """history.json 일별 주가로 7일 변화(7일 전 기록이 없으면 가장 오래된 기록부터)"""
    cutoff = (today - datetime.timedelta(days=DAYS)).isoformat()
    names = {x["ticker"]: x["name"] for x in (data or {}).get("items", [])}
    out, span_min = [], None
    for t, series in ((hist or {}).get("tickers") or {}).items():
        pts = [p for p in series if p.get("price") is not None]
        if len(pts) < 2 or t not in names:
            continue
        old = [p for p in pts if p["date"] <= cutoff]
        base = old[-1] if old else pts[0]
        last = pts[-1]
        if base is last or not base["price"]:
            continue
        days = (datetime.date.fromisoformat(last["date"]) - datetime.date.fromisoformat(base["date"])).days
        if days <= 0:
            continue
        span_min = days if span_min is None else min(span_min, days)
        out.append((names[t], (last["price"] / base["price"] - 1) * 100, days))
    out.sort(key=lambda r: r[1], reverse=True)
    return out, span_min


def fx_moves(data, old):
    cur, prv = (data or {}).get("fx") or {}, (old or {}).get("fx") or {}
    rows = []
    for code in ["USD", "EUR", "GBP", "JPY", "BRL"]:
        c = cur.get(code)
        if not c:
            continue
        unit = 100 if code == "JPY" else 1
        rate = c["rate"] * unit
        p = prv.get(code)
        wk = (c["rate"] / p["rate"] - 1) * 100 if p and p.get("rate") else None
        rows.append((code, c.get("name", code), rate, wk, c.get("chg_pct"), c.get("dev_pct")))
    return rows


FX_SH = {"JPY": "엔", "EUR": "유로", "USD": "달러"}


def fx_alerts_week(data, start):
    """지난 7일 1% 칸 알림 (fetch_data v4.9 fx[통화].alerts) — 날짜순"""
    out = []
    for code, c in ((data or {}).get("fx") or {}).items():
        for a in c.get("alerts") or []:
            if a.get("date", "") >= start.isoformat():
                rate = a["rate"] * (100 if code == "JPY" else 1)
                line = "1년 평균" if a["line"] == 0 else f"{'+' if a['line'] > 0 else '−'}{abs(a['line'])}% 선"
                out.append((a["date"], f"{a['date'][5:].replace('-', '/')} {FX_SH.get(code, code)} {rate:,.0f}원 "
                                       f"{line} {'아래로' if a['dir'] == 'dn' else '위로'}"))
    return [t for _, t in sorted(out)]


def new_results(data, old):
    """한 주 사이 새 분기·연간 실적이 반영된 상장사"""
    if not old:
        return []
    prev = {x["ticker"]: x for x in old.get("items", [])}
    out = []
    for x in (data or {}).get("items", []):
        p = prev.get(x["ticker"])
        if not p:
            continue
        fy_new = (x.get("fy") or [{}])[-1].get("end") != (p.get("fy") or [{}])[-1].get("end")
        q_new = x.get("q_end") and x.get("q_end") != p.get("q_end")
        if fy_new or q_new:
            out.append((x["name"], x.get("q_end"), x.get("latest_q_yoy"), x.get("inv_yoy")))
    return out


def upcoming_earnings(data, today):
    end = today + datetime.timedelta(days=DAYS)
    out = []
    for x in (data or {}).get("items", []):
        d = x.get("earn_date")
        if d and today.isoformat() <= d <= end.isoformat():
            out.append((d, x["name"]))
    return sorted(out)


def top_news(news, today, n=6):
    cutoff = (today - datetime.timedelta(days=DAYS)).isoformat()
    items = [i for i in (news or {}).get("items", []) if (i.get("first_seen") or "") >= cutoff and (i.get("importance") or 0) >= 2]
    items.sort(key=lambda i: i.get("first_seen") or "", reverse=True)      # 최신 먼저
    items.sort(key=lambda i: -(i.get("importance") or 0))                # 중요도 높은 것 먼저(안정 정렬)
    seen, per, out = set(), {}, []
    for i in items:
        s = (i.get("summary") or i.get("title") or "").strip()
        k, lab = s[:24], i.get("label") or ""
        if not s or k in seen or per.get(lab, 0) >= 2:      # 같은 회사는 2건까지(같은 사건 반복 방지)
            continue
        seen.add(k)
        per[lab] = per.get(lab, 0) + 1
        out.append((i.get("importance") or 0, i.get("label") or "", s, i.get("first_seen") or ""))
        if len(out) >= n:
            break
    return out, len([i for i in items if (i.get("importance") or 0) >= 3])


def naver_moves(nv):
    """네이버 주간 검색 지수: 최근 주 vs 그 전 주(규모 1 미만 제외)"""
    rows = []
    for b in (nv or {}).get("brands", []):
        s = [v for v in (b.get("s") or []) if v is not None]
        if len(s) < 2 or (b.get("scale") or 0) < 1 or not s[-2]:
            continue
        rows.append((b["name"], (s[-1] / s[-2] - 1) * 100, b.get("yoy")))
    rows.sort(key=lambda r: r[1], reverse=True)
    return rows


def dart_changes(kr, old):
    """한 주 사이 새 감사보고서·사업보고서 수치가 들어온 국내 법인"""
    if not kr or not old:
        return []
    prev = {e["id"]: e for e in old.get("entities", [])}
    out = []
    for e in kr.get("entities", []):
        ys = [y for y in e.get("years", []) if y.get("rev") is not None]
        pys = [y for y in (prev.get(e["id"]) or {}).get("years", []) if y.get("rev") is not None]
        if ys and (not pys or ys[-1].get("end") != pys[-1].get("end")):
            l = ys[-1]
            p = ys[-2] if len(ys) > 1 else None
            yoy = (l["rev"] / p["rev"] - 1) * 100 if p and p.get("rev") else None
            out.append((e["name"], l.get("end"), l["rev"], yoy, e["id"] in prev))
    return out


def inventory_warnings(data, kr):
    out = []
    for x in (data or {}).get("items", []):
        fy = (x.get("fy") or [{}])[-1]
        iv, rv = x.get("inv_yoy"), fy.get("rev_yoy")
        if iv is not None and rv is not None and iv >= 10 and iv - rv >= 10:
            out.append((x["name"], iv, rv))
    for e in (kr or {}).get("entities", []):
        ys = [y for y in e.get("years", []) if y.get("rev") is not None]
        if len(ys) < 2:
            continue
        l, p = ys[-1], ys[-2]
        if l.get("inv") and p.get("inv") and p.get("rev"):
            iv, rv = (l["inv"] / p["inv"] - 1) * 100, (l["rev"] / p["rev"] - 1) * 100
            if iv >= 10 and iv - rv >= 10:
                out.append((e["name"], iv, rv))
    out.sort(key=lambda r: r[1] - r[2], reverse=True)
    return out


def build(today):
    data, hist, news = load("data.json"), load("history.json"), load("news.json")
    nv, kr, kosis = load("naver_trend.json"), load("kr_domestic.json"), load("kosis.json")
    data_old, kr_old = load_old("data.json"), load_old("kr_domestic.json")
    fx_old, fx_days = load_old_with("data.json", "fx")
    start = today - datetime.timedelta(days=DAYS)
    period = f"{start:%m/%d}~{today:%m/%d}"

    moves, span = price_moves(data, hist, today)
    fx = fx_moves(data, fx_old)
    fxa = fx_alerts_week(data, start)
    res = new_results(data, data_old)
    earn = upcoming_earnings(data, today)
    nws, n_imp = top_news(news, today)
    nvm = naver_moves(nv)
    dch = dart_changes(kr, kr_old)
    inv = inventory_warnings(data, kr)

    # ── 휴대폰 알림 3줄 ──
    usd = next((r for r in fx if r[0] == "USD"), None)
    l2 = []
    if moves:
        up, dn = moves[0], moves[-1]
        l2.append(f"주가 ▲{up[0]} {pct(up[1])} ▼{dn[0]} {pct(dn[1])}")
    if usd:
        l2.append(f"달러 {usd[2]:,.0f}원{f'({pct(usd[3])})' if usd[3] is not None else ''}")
    short = [f"📋 스포츠 산업 모니터 주간 요약 {period}",
             " · ".join(l2) or "주가·환율 비교 자료 없음",
             f"중요 뉴스 {n_imp}건 · 새 실적 {len(res)}곳 · 이번 주 실적 발표 {len(earn)}곳 · 재고 경고 {len(inv)}곳"]

    # ── 메일 본문 ──
    L = [f"스포츠 산업 모니터 — 주간 요약 ({period}, {today:%Y-%m-%d} 기준)", ""]
    L += ["■ 한 줄 요약", *[f"  {s}" for s in short[1:]], ""]

    L.append("■ 중요 뉴스 (지난 7일)")
    if nws:
        for imp, lab, s, d in nws:
            L.append(f"  {'★' * imp} [{lab}] {s} ({d[5:].replace('-', '/')})")
    else:
        L.append("  해당 없음")
    L.append("")

    L.append(f"■ 주가 변화 (지난 {span or DAYS}일)" + (" — 기록이 7일이 안 되어 가능한 기간만" if span and span < DAYS else ""))
    if moves:
        L.append("  상승 " + " · ".join(f"{n} {pct(v)}" for n, v, _ in moves[:3]))
        L.append("  하락 " + " · ".join(f"{n} {pct(v)}" for n, v, _ in moves[::-1][:3]))
    else:
        L.append("  비교 자료 없음")
    L.append("")

    L.append("■ 환율 (원화 기준)" + (f" — 주간 변화는 {fx_days}일 기준(수집 이력 부족)" if fx_days and fx_days < DAYS else ""))
    for code, name, rate, wk, yr, dev in fx:
        unit = "100엔" if code == "JPY" else name
        L.append(f"  {unit} {rate:,.1f}원 · 주간 {pct(wk)} · 1년 {pct(yr)}"
                 + (f" · 1년 평균 대비 {pct(dev)}" if dev is not None else ""))
    if not fx:
        L.append("  자료 없음")
    elif any(r[5] is not None for r in fx):
        L.append("  1% 칸 알림(지난 7일): " + (" · ".join(fxa) if fxa else "없음"))
    L.append("")

    L.append("■ 새로 반영된 실적")
    if res:
        for n, q, qy, iv in res:
            L.append(f"  {n}: {q or '―'} 분기 매출 전년 대비 {pct(qy)} · 재고 {pct(iv)}")
    else:
        L.append("  없음")
    L.append("")

    L.append("■ 이번 주 실적 발표 예정")
    L += [f"  {d[5:].replace('-', '/')} {n}" for d, n in earn] or ["  없음"]
    L.append("")

    L.append("■ 국내")
    if nvm:
        L.append("  네이버 검색(주간, 최근 주 vs 전 주) 상승 " + " · ".join(f"{n} {pct(v)}" for n, v, _ in nvm[:3]))
        L.append("  네이버 검색(주간) 하락 " + " · ".join(f"{n} {pct(v)}" for n, v, _ in nvm[::-1][:3]))
    m = (nv or {}).get("monthly") or {}
    if m.get("months") and m.get("yoy"):
        last_m = m["months"][-1]
        yv = m["yoy"].get(last_m) if isinstance(m["yoy"], dict) else (m["yoy"][-1] if m["yoy"] else None)
        if yv is not None:
            L.append(f"  네이버 브랜드 검색 합계 {last_m} 전년 대비 {pct(yv)}")
    ser = (kosis or {}).get("series") or {}
    for key, label in [("online_shoes", "온라인 신발 거래액"), ("online_apparel", "온라인 의복 거래액")]:
        s = ser.get(key) or {}
        if s.get("yoy"):
            p = sorted(s["yoy"])[-1]
            L.append(f"  {label} {p} 전년 대비 {pct(s['yoy'][p])} (KOSIS)")
    if dch:
        for n, end, rev, yoy, existed in dch:
            L.append(f"  공시 반영: {n} {end[:7] if end else ''} 매출 {won(rev)} ({pct(yoy)}){'' if existed else ' · 새로 추가'}")
    L.append("")

    L.append("■ 재고 경고 (재고 증가율이 매출보다 10%p 이상 높음)")
    L += [f"  {n}: 재고 {pct(i)} vs 매출 {pct(r)}" for n, i, r in inv[:6]] or ["  없음"]
    if len(inv) > 6:
        L.append(f"  외 {len(inv) - 6}곳")
    L += ["", f"대시보드: {DASH_URL}", "※ 공시·수집값 그대로 비교한 자동 요약입니다."]
    return short, "\n".join(L)


def main():
    today = datetime.datetime.now(KST).date()
    short, body = build(today)
    print("\n".join(short) if "--short" in sys.argv else body)


if __name__ == "__main__":
    main()

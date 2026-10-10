# -*- coding: utf-8 -*-
"""
sports-industry-monitor — Phase 9: 주간 요약 (v1)
v1.8: (2026-10-10) 본사 발언 줄에 병행수입 매입 관점 신호(extract_segments v11.2 sig — 할인 물량↑ / 할인·공급↓) 표시
v1.7: (대표 지시 2026-10-10) '■ 이번 주 새 본사 발언' — 지난 7일 안에 새로 뽑힌 실적 문서의 재고·할인·유통 문장(한국어 요약 + 원문 앞부분).
      추출 시각(extracted_at, extract_segments v11.1·ir_fetch v1.4)이 7일 안이고 문서 날짜가 14일 안인 것만(재추출로 옛 발표가 다시 나오지 않게).
      알림 3줄에 '본사 발언 n곳'(있을 때만)
v1.6: (대표 지시 2026-10-10) 재고 증감을 같은 기간끼리(분기 자료가 있으면 같은 분기, 없으면 연간 결산) — 재고 경고·새 실적 줄에 비교 기간 표기
v1.5: (2026-10-09) 분기 실적 판정은 기간 문구의 첫 구절만 봄(build_dashboard v32.13과 같게) — 딕스 '인수 효과 포함, 본체 +5.6%'
v1.4: (대표 지시 2026-10-09) 대시보드(build_dashboard v32.12)와 같은 순위 규칙 — 새 실적 줄에 기준(분기 '26.06, 분기 증감이 없으면 연간 FY25),
      딕스는 인수 효과 기간(ACQ)엔 '인수 효과 포함'(분기 실적이면 본체 증가율)·재고 경고에서 뺌, 삼성물산(전사 수치)은 새 실적·재고 경고에서 뺌,
      공시(SEC·IR) 분기가 야후보다 45일 넘게 새로우면 '새 실적 반영 대기' 줄, 재고 경고에 결산 연도(FY24 등) 표시
      수집 실패로 이전 값을 쓴 종목·통화·네이버 브랜드(stale_since)는 이번 주 변화에서 빼고, 새 실적은 결산일이 더 늦어질 때만
v1.3: 새 실적 줄 — 야후(연결) 연간 매출이 DART 값과 20% 넘게 다른 상장사(LS네트웍스: 지정 별도 vs 야후 LS증권 포함 연결)는
      분기 매출 전년 대비를 빼고 '야후 연결 기준이라 제외'로 표시(build_dashboard v32.9와 같은 규칙)
v1.2: (대표 요청 2026-10-06) 국내 비교 회사 뉴스(유통사·패션 브랜드)·통관·상표권 뉴스를 따로 묶고 '중요 뉴스'에서는 중복 제외.
      아이웨어 검색(네이버 주간·전년 대비), 국내 패션·아이웨어 올해 누적 검색 변화(naver_trend v1.5 brand_monthly) 추가
v1.1: 환율 줄에 '1년 평균 대비 %'(fetch_data v4.9) + 지난 7일 1% 칸 알림 목록
v1: 월요일 아침 주간 요약 — docs/*.json(현재)과 history.json·git 이력(7일 전 main)을 비교해 한 주 변화를 정리.
    출력: 기본 = 메일 본문(텍스트), --short = 휴대폰 알림용 3줄. 저장소에 아무것도 쓰지 않음(읽기 전용).
    매주 월 07:47(KST) 점검 전용 세션의 루틴이 실행 → Claude 앱 알림 + 대표 본인 Gmail로 발송.
§29-D: 파일에 있는 값만 비교·정렬, 없는 값은 '―'/생략(임의 수치 생성 금지)
"""

import os
import re
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
    # 그날 수집에 실패해 이전 값을 이어 쓴 종목(stale_since)은 기록이 멈춰 있어 비교 기간만 짧게 만듦 → 제외
    names = {x["ticker"]: x["name"] for x in (data or {}).get("items", []) if not x.get("stale_since")}
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
        st = c.get("stale_since")     # 오늘 수집 실패 → 이전 값(주간 변화는 비움)
        wk = (c["rate"] / p["rate"] - 1) * 100 if p and p.get("rate") and not st else None
        rows.append((code, c.get("name", code), rate, wk, c.get("chg_pct"), c.get("dev_pct"), st))
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


def yahoo_cfs_diff(x, krf):
    """야후 연간 매출(최근 공통 연도)이 DART 값과 20% 넘게 다르면 True — build_dashboard merge_kr_listed와 같은 규칙"""
    e = ((krf or {}).get("items") or {}).get(x.get("ticker")) or {}
    dmap = {(y.get("end") or "")[:4]: y.get("rev") for y in e.get("years") or []}
    diff = [(y["end"], abs(y["rev"] / dmap[y["end"][:4]] - 1)) for y in (x.get("fy") or [])
            if y.get("rev") and y.get("end") and dmap.get(y["end"][:4])]
    return bool(diff) and max(diff)[1] > 0.2


# ── v1.4 순위 규칙 — build_dashboard.py v32.12의 ACQ·WHOLE_CO·PEND_DAYS와 같게 유지 ──
ACQ = {"DKS": {"until": "2026-11-30", "why": "풋락커 인수(2025-09) 효과 포함", "core": "DICK'S"}}   # 인수 효과 기간
WHOLE_CO = {"028260.KS": "삼성물산은 건설·상사 포함 전사 수치라 제외"}                         # 회사 전체 수치
PEND_DAYS = 45                                                                              # 공시 분기가 이만큼 넘게 새로우면 반영 대기
MON3 = {m: i + 1 for i, m in enumerate("jan feb mar apr may jun jul aug sep oct nov dec".split())}


def acq_on(t, today):
    a = ACQ.get(t)
    return a if a and today.isoformat() <= a["until"] else None


def ym(d):
    """결산·분기 종료일 표기: 2026-06-30 → '26.06"""
    return f"'{d[2:4]}.{d[5:7]}" if d else ""


def fy_lbl(d):
    return f"FY{d[2:4]}" if d else ""


def period_end(p):
    """공시 기간 문자열의 종료일('ended 2026-08-31' / 'ended August 1, 2026') — 없거나 실적 기간이 아니면 None"""
    p = str(p or "")
    if re.search(r"pro ?forma|target|investor", p, re.I):
        return None
    m = re.search(r"ended\s+(\d{4}-\d{2}-\d{2})", p, re.I)
    if m:
        return m.group(1)
    m = re.search(r"ended\s+([A-Za-z]{3})[a-z]*\.?\s+(\d{1,2}),?\s+(\d{4})", p, re.I)
    mo = m and MON3.get(m.group(1).lower())
    return f"{m.group(3)}-{mo:02d}-{int(m.group(2)):02d}" if mo else None


def is_qtr_period(p):
    p = re.split(r";|\balso\b", str(p or ""), flags=re.I)[0]   # v1.5 첫 구절만(분기·누적을 함께 적은 추출)
    return bool(re.search(r"\bQ[1-4]\b|quarter|thirteen weeks|13 weeks|three months|분기", p, re.I)) and \
        not re.search(r"pro ?forma|누적|six months|nine months|26 weeks|39 weeks|twenty-six|thirty-nine", p, re.I)


def pend_of(x, segs, segs_ir):
    """야후 분기(q_end)보다 공시(SEC·IR) 분기 종료일이 45일 넘게 새로우면 (종료일, 출처)"""
    if not x.get("q_end"):
        return None
    best = None
    for src, d in (("SEC", segs), ("IR", segs_ir)):
        e = ((d or {}).get("items") or {}).get(x["ticker"]) or {}
        end = period_end((e.get("extract") or {}).get("period"))
        if end and (not best or end > best[0]):
            best = (end, src)
    if not best:
        return None
    try:    # 없는 날짜('February 30')·형식이 다른 q_end는 판단하지 않음 — 대시보드 pendOf처럼 넘어가고 메일 전체는 계속
        gap = (datetime.date.fromisoformat(best[0]) - datetime.date.fromisoformat(str(x["q_end"])[:10])).days
    except (ValueError, TypeError):
        return None
    return best if gap > PEND_DAYS else None


def acq_core(t, segs, segs_ir):
    """인수 회사 본체 매출 증가율 — 공시 추출이 분기 실적이고 본체 부문에 당기·전년 매출이 있을 때만(대시보드처럼 IR 우선)"""
    a = ACQ.get(t) or {}
    e = ((segs_ir or {}).get("items") or {}).get(t) or {}
    if not e.get("extract"):
        e = ((segs or {}).get("items") or {}).get(t) or {}
    ex = e.get("extract") or {}
    if not a or not is_qtr_period(ex.get("period")):
        return None
    c = next((z for z in ex.get("sub_segments") or [] if z.get("name") == a.get("core")), None)
    return (c["revenue"] / c["prev_revenue"] - 1) * 100 if c and c.get("revenue") is not None and c.get("prev_revenue") else None


def new_results(data, old, krf=None, today=None, segs=None, segs_ir=None):
    """한 주 사이 새 분기·연간 실적이 반영된 상장사 — (이름, 기준, 매출 증감(분기, 없으면 연간) 또는 사유, 재고 증감, 재고 기준, 덧붙임)
    v1.4 전사 수치(삼성물산)는 빼고 두 번째 값으로 돌려줌, 인수 효과 기간(딕스)은 '인수 효과 포함'"""
    if not old:
        return [], []
    today = today or datetime.datetime.now(KST).date()
    prev = {x["ticker"]: x for x in old.get("items", [])}
    out, skipped = [], []
    for x in (data or {}).get("items", []):
        p = prev.get(x["ticker"])
        if not p or x.get("stale_since"):      # 오늘 수집 실패(이전 값)는 새 실적이 아님
            continue
        # 두 값이 모두 있고 새 값이 더 늦을 때만 새 실적(값이 비었다 생기거나 앞 분기로 흔들린 것은 제외)
        xe, pe = (x.get("fy") or [{}])[-1].get("end"), (p.get("fy") or [{}])[-1].get("end")
        fy_new = bool(xe and pe and xe > pe)
        q_new = bool(x.get("q_end") and p.get("q_end") and x["q_end"] > p["q_end"])
        if fy_new or q_new:
            if x["ticker"] in WHOLE_CO:
                skipped.append(WHOLE_CO[x["ticker"]])
                continue
            fy = (x.get("fy") or [{}])[-1]
            fy_end = fy.get("end")
            qy = "야후 연결 기준이라 제외" if yahoo_cfs_diff(x, krf) else x.get("latest_q_yoy")
            if qy is None:      # 대시보드 basisOf와 같게: 분기 증감이 없으면 연간 매출 증감(분기 자료 없는 곳·전년 짝 없는 분기)
                qy, basis = fy.get("rev_yoy"), f"연간 {fy_lbl(fy_end)}".strip()
            else:
                basis = f"분기 {ym(x.get('q_end'))}" if x.get("q_end") else "분기 ―"
            extra = ""
            a = acq_on(x["ticker"], today)
            if a:
                c = acq_core(x["ticker"], segs, segs_ir)
                extra = f" (인수 효과 포함{f', 본체 {pct(c)}' if c is not None else ''})"
            iv, _, ilbl = inv_pick(x, krf)      # v1.6 재고도 같은 기간끼리, 비교 기간 표기
            out.append((x["name"], basis, qy, iv, ilbl, extra))
    return out, skipped


def pending_results(data, segs, segs_ir):
    """공시에는 새 분기 실적이 있는데 야후(분기 매출 증감)에 아직 안 들어온 상장사"""
    out = []
    for x in (data or {}).get("items", []):
        pe = pend_of(x, segs, segs_ir)
        if pe:
            out.append((x["name"], pe[1], pe[0], x.get("q_end")))
    return out


def upcoming_earnings(data, today):
    end = today + datetime.timedelta(days=DAYS)
    out = []
    for x in (data or {}).get("items", []):
        d = x.get("earn_date")
        if d and today.isoformat() <= d <= end.isoformat():
            out.append((d, x["name"]))
    return sorted(out)


TOPIC_KO = {"inventory": "재고", "discount": "할인·판촉", "channel": "유통·도매"}
SIG_KO = {"more": "할인 물량↑", "less": "할인·공급↓"}   # v1.8 병행수입 매입 관점 신호(대시보드 본사 발언·브랜드 점검표와 같음)


def _doc_date(e):
    """본사 발언이 나온 문서 날짜 — SEC는 source의 공시일, IR은 doc_date(없으면 URL의 dd-mm-yyyy)"""
    if e.get("doc_date"):
        return str(e["doc_date"])[:10]
    m = re.search(r"\b(\d{4}-\d{2}-\d{2})\b", str(e.get("source") or ""))
    if m:
        return m.group(1)
    m = re.search(r"/(\d{2})-(\d{2})-(\d{4})-", str(e.get("url") or ""))
    return f"{m.group(3)}-{m.group(2)}-{m.group(1)}" if m else None


def _kst(v):
    """'2026-10-12 01:58' / '2026-10-12' → KST datetime, 실패 시 None"""
    m = re.match(r"(\d{4}-\d{2}-\d{2})(?:[ T](\d{2}):(\d{2}))?", str(v or ""))
    if not m:
        return None
    try:
        d = datetime.date.fromisoformat(m.group(1))
    except ValueError:
        return None
    return datetime.datetime(d.year, d.month, d.day, int(m.group(2) or 0), int(m.group(3) or 0), tzinfo=KST)


def new_mgmt_notes(data, segs, segs_ir, now):
    """v1.7 이번 주 새 본사 발언 — 추출 시각이 7일 안 + 문서 날짜가 14일 안(추출 시각이 없는 옛 기록은 문서 날짜 7일 안).
    → [(회사, 문서 날짜, 기간, 노트 목록)] 문서 날짜 최신순"""
    names = {x.get("ticker"): x.get("name") for x in (data or {}).get("items", [])}
    today = now.date()
    found = {}
    for src in (segs, segs_ir):
        for t, e in ((src or {}).get("items") or {}).items():
            ex = (e or {}).get("extract") or {}
            notes = [n for n in ex.get("mgmt_notes") or [] if isinstance(n, dict) and n.get("quote")]
            dd = _doc_date(e or {})
            try:
                ddate = datetime.date.fromisoformat(dd) if dd else None
            except ValueError:
                ddate = None
            if not notes or not ddate:
                continue
            ea = _kst(ex.get("extracted_at") or (e or {}).get("fetched_at"))
            if ea:
                fresh = ea > now - datetime.timedelta(days=DAYS) and ddate >= today - datetime.timedelta(days=14)
            else:
                fresh = ddate >= today - datetime.timedelta(days=DAYS)
            if fresh:
                per = re.split(r";|\(|\bended\b", str(ex.get("period") or ""), flags=re.I)[0].strip()
                found[t] = (names.get(t) or t, dd, per, notes)
    return sorted(found.values(), key=lambda r: r[1], reverse=True)


SEP_GROUPS = ("kr_peer", "kr_fb", "customs")   # 따로 묶는 뉴스(v1.2) — '중요 뉴스'에서는 제외


def top_news(news, today, n=6):
    cutoff = (today - datetime.timedelta(days=DAYS)).isoformat()
    items = [i for i in (news or {}).get("items", []) if (i.get("first_seen") or "") >= cutoff and (i.get("importance") or 0) >= 2
             and i.get("group") not in SEP_GROUPS]
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


def group_news(news, today, groups, n=6):
    """지난 7일 특정 그룹 뉴스(중요도 무관) — 최신·중요도 순, 같은 요약 반복 제외"""
    cutoff = (today - datetime.timedelta(days=DAYS)).isoformat()
    items = [i for i in (news or {}).get("items", []) if (i.get("first_seen") or "") >= cutoff and i.get("group") in groups]
    items.sort(key=lambda i: i.get("first_seen") or "", reverse=True)      # 최신 먼저
    items.sort(key=lambda i: -(i.get("importance") or 0))                # 중요도 높은 것 먼저(안정 정렬)
    seen, out = set(), []
    for i in items:
        s = (i.get("summary") or i.get("title") or "").strip()
        if not s or s[:24] in seen:
            continue
        seen.add(s[:24])
        out.append((i.get("importance") or 0, i.get("label") or "", s, i.get("first_seen") or ""))
    return out[:n], len(out)


EYE_KR = ("젠틀몬스터", "블루엘리펀트")


def eye_moves(nv):
    """아이웨어(글로벌 + 젠틀몬스터·블루엘리펀트): 전년 대비(최근 4주) 순, 규모 1 미만 제외"""
    rows = [(b["name"], b.get("yoy")) for b in (nv or {}).get("brands", [])
            if (b.get("group") == "eye" or b.get("name") in EYE_KR) and b.get("yoy") is not None and (b.get("scale") or 0) >= 1]
    rows.sort(key=lambda r: r[1], reverse=True)
    return rows


def ytd_search(nv):
    """국내 패션·아이웨어 브랜드 올해 누적 검색(1월~지난달) vs 전년 같은 기간 — brand_monthly"""
    bm = (nv or {}).get("brand_monthly") or {}
    mo, ser = bm.get("months") or [], bm.get("series") or {}
    if not mo:
        return [], None
    cy, cm = int(mo[-1][:4]), int(mo[-1][5:7])
    idx = lambda y: [i for i, p in enumerate(mo) if int(p[:4]) == y and int(p[5:7]) <= cm]
    a, b = idx(cy), idx(cy - 1)
    if len(a) != cm or len(b) != cm:
        return [], None
    rows = []
    for name, v in ser.items():
        x, y = sum(v[i] for i in a), sum(v[i] for i in b)
        if y and x + y >= 2:      # 검색이 거의 없는 브랜드 제외
            rows.append((name, (x / y - 1) * 100))
    rows.sort(key=lambda r: r[1], reverse=True)
    return rows, f"{cy}년 1~{cm}월"


def naver_moves(nv):
    """네이버 주간 검색 지수: 최근 주 vs 그 전 주(규모 1 미만 제외) — 수입·해외 브랜드(global)만"""
    rows = []
    for b in (nv or {}).get("brands", []):
        if b.get("group", "global") != "global" or b.get("stale_since"):   # 이전 값 브랜드는 지난 회차 변화라 제외
            continue
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


def inv_pick(x, krf=None):
    """v1.6 재고 증감은 같은 기간끼리(build_dashboard v32.14 invPick과 같게) — 분기 재고·같은 분기 매출이 있으면
    최근 분기 vs 1년 전 같은 분기, 없으면 연간 결산. 반환 (재고 증감, 같은 기간 매출 증감, 비교 기간 표기)"""
    if x.get("q_inv_yoy") is not None and x.get("q_inv_rev_yoy") is not None and not yahoo_cfs_diff(x, krf):
        return x["q_inv_yoy"], x["q_inv_rev_yoy"], f"분기 {ym(x.get('q_inv_date'))} vs {ym(x.get('q_inv_prev_date'))}"
    e = ((krf or {}).get("items") or {}).get(x.get("ticker")) or {}
    ys = [y for y in e.get("years") or [] if y.get("rev") is not None]
    if len(ys) >= 2:     # 국내 상장사 연간은 대시보드(merge_kr_listed)처럼 DART 사업보고서 값
        l, p = ys[-1], ys[-2]
        iv = (l["inv"] / p["inv"] - 1) * 100 if l.get("inv") and p.get("inv") else None
        rv = (l["rev"] / p["rev"] - 1) * 100 if p.get("rev") else None
        return iv, rv, f"결산 {ym(l.get('end'))} vs {ym(p.get('end'))}"
    fy = (x.get("fy") or [{}])[-1]
    d, p = x.get("inv_date"), x.get("inv_prev_date")
    return x.get("inv_yoy"), fy.get("rev_yoy"), (f"결산 {ym(d)}" + (f" vs {ym(p)}" if p else "")) if d else ""


def inventory_warnings(data, kr, today=None, krf=None):
    """재고 경고 — (이름, 재고 증감, 같은 기간 매출 증감, 비교 기간) 목록과 제외 사유 목록.
    v1.4 대시보드와 같게 전사 수치(삼성물산)·인수 효과 기간(딕스)은 빼고 사유로 돌려줌"""
    today = today or datetime.datetime.now(KST).date()
    out, skipped = [], []
    for x in (data or {}).get("items", []):
        iv, rv, lbl = inv_pick(x, krf)
        if iv is not None and rv is not None and iv >= 10 and iv - rv >= 10:
            a = acq_on(x["ticker"], today)
            if x["ticker"] in WHOLE_CO:
                skipped.append(WHOLE_CO[x["ticker"]])
            elif a:
                skipped.append(f"{x['name']}는 인수 효과 기간(~{int(a['until'][5:7])}/{int(a['until'][8:10])})이라 제외")
            else:
                out.append((x["name"], iv, rv, lbl))
    for e in (kr or {}).get("entities", []):
        ys = [y for y in e.get("years", []) if y.get("rev") is not None]
        if len(ys) < 2:
            continue
        l, p = ys[-1], ys[-2]
        if l.get("inv") and p.get("inv") and p.get("rev"):
            iv, rv = (l["inv"] / p["inv"] - 1) * 100, (l["rev"] / p["rev"] - 1) * 100
            if iv >= 10 and iv - rv >= 10:
                out.append((e["name"], iv, rv, f"결산 {ym(l.get('end'))} vs {ym(p.get('end'))}"))
    out.sort(key=lambda r: r[1] - r[2], reverse=True)
    return out, skipped


def build(today, now=None):
    data, hist, news = load("data.json"), load("history.json"), load("news.json")
    nv, kr, kosis = load("naver_trend.json"), load("kr_domestic.json"), load("kosis.json")
    data_old, kr_old = load_old("data.json"), load_old("kr_domestic.json")
    segs, segs_ir = load("segments.json"), load("segments_ir.json")
    fx_old, fx_days = load_old_with("data.json", "fx")
    start = today - datetime.timedelta(days=DAYS)
    period = f"{start:%m/%d}~{today:%m/%d}"

    moves, span = price_moves(data, hist, today)
    fx = fx_moves(data, fx_old)
    fxa = fx_alerts_week(data, start)
    res, res_skip = new_results(data, data_old, load("kr_listed_fin.json"), today, segs, segs_ir)
    pend = pending_results(data, segs, segs_ir)
    earn = upcoming_earnings(data, today)
    nws, n_imp = top_news(news, today)
    nvm = naver_moves(nv)
    kn, kn_n = group_news(news, today, ("kr_peer", "kr_fb"))
    cn, cn_n = group_news(news, today, ("customs",))
    eye = eye_moves(nv)
    ytd, ytd_p = ytd_search(nv)
    dch = dart_changes(kr, kr_old)
    inv, inv_skip = inventory_warnings(data, kr, today, load("kr_listed_fin.json"))
    mg = new_mgmt_notes(data, segs, segs_ir, now or datetime.datetime.now(KST))

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
             f"중요 뉴스 {n_imp}건 · 새 실적 {len(res)}곳{f' · 본사 발언 {len(mg)}곳' if mg else ''} · "
             f"이번 주 실적 발표 {len(earn)}곳 · 재고 경고 {len(inv)}곳"]

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

    L.append(f"■ 국내 비교 회사 뉴스 (지난 7일, 유통사·패션 브랜드{f' · 총 {kn_n}건' if kn_n > len(kn) else ''})")
    L += [f"  {'★' * imp} [{lab}] {s} ({d[5:].replace('-', '/')})" for imp, lab, s, d in kn] or ["  해당 없음"]
    L.append("")
    L.append(f"■ 통관·상표권 (지난 7일{f' · 총 {cn_n}건' if cn_n > len(cn) else ''})")
    L += [f"  {'★' * imp} {s} ({d[5:].replace('-', '/')})" for imp, lab, s, d in cn] or ["  해당 없음"]
    L.append("")

    L.append(f"■ 주가 변화 (지난 {span or DAYS}일)" + (" — 기록이 7일이 안 되어 가능한 기간만" if span and span < DAYS else ""))
    if moves:
        L.append("  상승 " + " · ".join(f"{n} {pct(v)}" for n, v, _ in moves[:3]))
        L.append("  하락 " + " · ".join(f"{n} {pct(v)}" for n, v, _ in moves[::-1][:3]))
    else:
        L.append("  비교 자료 없음")
    L.append("")

    L.append("■ 환율 (원화 기준)" + (f" — 주간 변화는 {fx_days}일 기준(수집 이력 부족)" if fx_days and fx_days < DAYS else ""))
    for code, name, rate, wk, yr, dev, st in fx:
        unit = "100엔" if code == "JPY" else name
        L.append(f"  {unit} {rate:,.1f}원 · 주간 {pct(wk)} · 1년 {pct(yr)}"
                 + (f" · 1년 평균 대비 {pct(dev)}" if dev is not None else "")
                 + (f" (이전 값 {st[5:].replace('-', '/')})" if st else ""))
    if not fx:
        L.append("  자료 없음")
    elif any(r[5] is not None for r in fx):
        L.append("  1% 칸 알림(지난 7일): " + (" · ".join(fxa) if fxa else "없음"))
    L.append("")

    L.append("■ 새로 반영된 실적")
    if res:
        for n, basis, qy, iv, ib, extra in res:
            L.append(f"  {n}: {basis} 매출 전년 대비 {qy if isinstance(qy, str) else pct(qy)}{extra}"
                     f" · 재고 {pct(iv)}{f'({ib})' if ib else ''}")
    else:
        L.append("  없음")
    if res_skip:
        L.append("  ※ " + " · ".join(res_skip))
    for n, src, end, q in pend:
        L.append(f"  새 실적 반영 대기: {n} — {src} 공시 {ym(end)} 분기 발표됨, 야후는 {ym(q)} 분기까지")
    L.append("")

    L.append("■ 이번 주 새 본사 발언 (실적 문서의 재고·할인·유통 문장 — 한국어 요약 / 원문)")
    for n, dd, per, notes in mg:
        L.append(f"  {n} ({dd[5:].replace('-', '/')} 발표{f' · {per}' if per else ''})")
        for x in notes:
            q = str(x.get("quote") or "")
            sg = SIG_KO.get(x.get("sig"))
            L.append(f"    [{TOPIC_KO.get(x.get('topic'), x.get('topic'))}{' · ' + sg if sg else ''}] {x.get('ko') or ''}")
            L.append(f"      \"{q[:160]}{'…' if len(q) > 160 else ''}\"")
    if not mg:
        L.append("  없음 — 본사 실적 발표가 나오면 다음 월요일 메일에 모아 보냄")
    L.append("")

    L.append("■ 이번 주 실적 발표 예정")
    L += [f"  {d[5:].replace('-', '/')} {n}" for d, n in earn] or ["  없음"]
    L.append("")

    L.append("■ 국내")
    if nvm:
        L.append("  네이버 검색(주간, 최근 주 vs 전 주) 상승 " + " · ".join(f"{n} {pct(v)}" for n, v, _ in nvm[:3]))
        L.append("  네이버 검색(주간) 하락 " + " · ".join(f"{n} {pct(v)}" for n, v, _ in nvm[::-1][:3]))
    m = (nv or {}).get("monthly") or {}
    if eye:
        L.append("  아이웨어 검색 전년 대비(최근 4주) 상위 " + " · ".join(f"{n} {pct(v)}" for n, v in eye[:3])
                 + " / 하위 " + " · ".join(f"{n} {pct(v)}" for n, v in eye[::-1][:3]))
    if ytd:
        L.append(f"  국내 패션·아이웨어 검색 {ytd_p} 전년 대비 증가 " + " · ".join(f"{n} {pct(v)}" for n, v in ytd[:3])
                 + " / 감소 " + " · ".join(f"{n} {pct(v)}" for n, v in ytd[::-1][:3]))
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

    L.append("■ 재고 경고 (재고 증가율이 같은 기간 매출보다 10%p 이상 높음 · 분기 자료가 있으면 같은 분기끼리, 없으면 연간 결산)")
    L += [f"  {n}: 재고 {pct(i)} vs 매출 {pct(r)}{f' ({fy})' if fy else ''}" for n, i, r, fy in inv[:6]] or ["  없음"]
    if len(inv) > 6:
        L.append(f"  외 {len(inv) - 6}곳")
    if inv_skip:
        L.append("  ※ " + " · ".join(inv_skip))
    L += ["", f"대시보드: {DASH_URL}", "※ 공시·수집값 그대로 비교한 자동 요약입니다."]
    return short, "\n".join(L)


def main():
    now = datetime.datetime.now(KST)
    short, body = build(now.date(), now)
    print("\n".join(short) if "--short" in sys.argv else body)


if __name__ == "__main__":
    main()

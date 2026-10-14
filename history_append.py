# -*- coding: utf-8 -*-
"""
sports-industry-monitor — 히스토리 축적 (v1)
v1.2: (대표 승인 2026-10-14) 브랜드 점검표 판정을 자료 날짜마다 기록(verdicts) — 화면과 같은 규칙(build_dashboard chk_verdicts,
      국내 상장사는 화면처럼 DART 재무 병합 뒤). 화면 '어제와 달라진 판정'·주간 메일 판정 요약에 씀. 같은 날 다시 돌면 덮어씀.
      기록마다 비교 기준 sig(감시 브랜드·본사 연결·원산지 통화표) — 바뀐 날은 비교하지 않음(목록 변경으로 생긴 판정 변화를 걸러냄).
      판정 계산이 실패하거나 판정한 브랜드가 없으면(자료 문제) 재무·주가 기록은 저장하고 soft_fail.txt에 남김(빨간 X → 12:23 점검 알림)
v1.1: (대표 지시 2026-10-09) 그날 수집에 실패해 이전 값을 이어 쓴 종목(data.json stale_since)은 새 점을 쌓지 않음
      — 같은 옛 값이 7일마다 '새 관측'처럼 기록되지 않게
매일 빌드 직전에 실행. docs/data.json(재무·주가)과 docs/segments.json(공시 추출)의
핵심 지표를 docs/history.json에 날짜별로 누적한다.
- 값이 직전 스냅샷과 같으면 저장하지 않되, 7일 이상 지났으면 그래도 1점 저장
  (파일 크기 억제 + 시계열 연속성)
- §29-D: data.json/segments.json에 있는 값만 그대로 기록, 계산·보정 없음
출력: docs/history.json
"""

import os
import re
import sys
import copy
import json
import datetime

sys.dont_write_bytecode = True   # v1.2 build_dashboard(판정 규칙)를 불러와도 저장소에 __pycache__를 남기지 않음

KST = datetime.timezone(datetime.timedelta(hours=9))
DATA_PATH = "docs/data.json"
SEG_PATH = "docs/segments.json"
SEG_IR_PATH = "docs/segments_ir.json"
NAVER_PATH = "docs/naver_trend.json"
HIST_PATH = "docs/history.json"
FORCE_DAYS = 7          # 변화 없어도 이 일수마다 1점 저장
MAX_POINTS = 400        # 종목당 최대 보관 점수 (약 1년+ 여유)
VERDICT_MAX = 400       # 판정 기록 최대 일수(v1.2)

# data.json에서 기록할 필드
FIELDS = ["rev_yoy", "gm_pct", "op_pct", "latest_q_yoy",
          "inv_yoy", "inv_sales_pct", "price", "off_high_pct"]


def load(path, default):
    if os.path.exists(path):
        try:
            with open(path, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return default


def snapshot_from_data(item):
    fy = item.get("fy") or []
    last = fy[-1] if fy else {}
    snap = {
        "rev_yoy": last.get("rev_yoy"),
        "gm_pct": last.get("gm_pct"),
        "op_pct": last.get("op_pct"),
        "latest_q_yoy": item.get("latest_q_yoy"),
        "inv_yoy": item.get("inv_yoy"),
        "inv_sales_pct": item.get("inv_sales_pct"),
        "price": item.get("price"),
        "off_high_pct": item.get("off_high_pct"),
    }
    return {k: (round(v, 4) if isinstance(v, (int, float)) else None)
            for k, v in snap.items()}


def snapshot_from_segments(entry):
    """지역·채널 비중(%)을 기록 — revenue 합 기준"""
    if not entry or not entry.get("extract"):
        return None
    ex = entry["extract"]
    out = {"period": ex.get("period"), "accession": entry.get("accession")}
    for kind in ("regions", "channels"):
        rows = [r for r in (ex.get(kind) or []) if r.get("revenue") is not None]
        total = sum(r["revenue"] for r in rows)
        if rows and total:
            out[kind] = {r["name"]: round(r["revenue"] / total * 100, 2)
                         for r in rows}
    return out


def same(a, b):
    return json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)


def soft_fail(msg):
    """심각한 실패 표시 — 저장은 하되 워크플로우 마지막 단계가 빨간 X로 끝내 점검 알림이 가게 함"""
    print(f"실패 표시: {msg}", flush=True)
    with open("soft_fail.txt", "a", encoding="utf-8") as f:
        f.write(f"history_append: {msg}\n")


def append_verdicts(hist, data, today):
    """v1.2 브랜드 점검표 판정 기록 — {date, rule, sig, b: {브랜드: [판정, 수요, 재고, 발언, 환율]}}.
    날짜는 data.json 수집 날짜(화면이 '오늘'로 보는 날 — 화면과 같은 글자로 비교) — 같은 날 다시 돌면 덮어씀.
    sig = 비교 기준(감시 브랜드·본사 연결·원산지 통화표, build_dashboard chk_sig) — 다르면 화면·주간 메일이 비교하지 않음.
    판정한 브랜드가 없거나(자료 문제) 수집 날짜가 없으면 그날 기록을 남기지 않고 soft_fail"""
    from build_dashboard import CHK_LV, CHK_RULE, chk_entry_ok, chk_records, chk_sig, chk_verdicts, merge_kr_listed
    day = str(data.get("generated_at") or "")[:10]
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", day):      # 화면은 generated_at 앞 10글자로 비교 — 다른 날짜로 바꿔 쓰면 화면과 어긋남
        soft_fail(f"브랜드 판정 기록 건너뜀 — data.json 수집 날짜 없음({day or '빈 값'})")
        return
    if day != today:
        print(f"  참고: data.json 수집 날짜 {day} ≠ 오늘 {today} — 그 날짜 기록을 다시 씀(수집이 갱신되지 않았는지 확인)", flush=True)
    d = copy.deepcopy(data)       # 재무·주가 기록(위)은 야후 값 그대로 — 판정만 화면처럼 DART 병합 뒤
    merge_kr_listed(d)
    naver = load(NAVER_PATH, None)
    v = chk_verdicts(d, naver, load(SEG_PATH, None), load(SEG_IR_PATH, None))
    sig = chk_sig(naver)
    ser = [r for r in chk_records(hist) if r["date"] != day]      # 모양이 틀린 기록은 걸러냄 · 같은 날 기록은 새로(또는 지움)
    if not v:      # 판정할 브랜드가 하나도 없는 건 자료 문제(네이버·본사 자료) — 그날 기록을 지우고 빨간 X로 알림
        hist["verdicts"] = ser[-VERDICT_MAX:]
        soft_fail(f"브랜드 판정 기록 건너뜀 {day} — 판정한 브랜드 없음(네이버 검색·본사 자료 확인)")
        return
    prev = next((r for r in reversed(ser) if r["date"] < day and r["rule"] == CHK_RULE), None)
    ser.append({"date": day, "rule": CHK_RULE, "sig": sig, "b": v})
    ser.sort(key=lambda r: r["date"])
    hist["verdicts"] = ser[-VERDICT_MAX:]
    cnt = " · ".join(f"{CHK_LV[k]} {sum(1 for x in v.values() if x[0] == k)}" for k in (2, 1, 0))
    if prev is None:
        chg = "비교할 이전 기록 없음"
    elif prev.get("sig") != sig:
        chg = f"{prev['date']} 뒤로 감시 브랜드·본사 연결·통화표가 바뀌어 비교 안 함"
    else:
        BAD = object()      # 모양이 틀린 값(0 == False 혼동을 피해 따로 표시)

        def lv(n):     # 기록에 없으면 None(판정 안 함), 모양이 틀리면 BAD(비교 안 함) — 화면 lvOf와 같은 기준
            x = prev["b"].get(n)
            return None if n not in prev["b"] else (x[0] if chk_entry_ok(x) else BAD)
        moved = [f"{n} {CHK_LV.get(lv(n), '판정 안 함')}→{CHK_LV[x[0]]}" for n, x in v.items() if lv(n) is not BAD and lv(n) != x[0]]
        gone = [f"{n} {CHK_LV[lv(n)]}→판정 안 함" for n in prev["b"] if n not in v and lv(n) is not None and lv(n) is not BAD]
        bad = [n for n in prev["b"] if lv(n) is BAD]
        chg = (f"{prev['date']} 대비 바뀜 {len(moved) + len(gone)}곳" + (f"({', '.join(moved + gone)})" if moved or gone else "")
               + (f" · 기록 모양이 틀려 비교 제외 {', '.join(bad)}" if bad else ""))
    print(f"판정 기록 {day}: {cnt} · {chg}", flush=True)


def main():
    today = datetime.datetime.now(KST).date().isoformat()
    data = load(DATA_PATH, {"items": []})
    segs = load(SEG_PATH, {"items": {}})
    hist = load(HIST_PATH, {"tickers": {}, "segments": {}})
    hist.setdefault("tickers", {})
    hist.setdefault("segments", {})

    added = 0
    # ── 재무·주가 스냅샷 ──
    for item in data.get("items", []):
        t = item.get("ticker")
        if not t:
            continue
        if item.get("stale_since"):     # v1.1 오늘 수집 실패 → 이전 값이라 새 관측이 아님
            continue
        snap = snapshot_from_data(item)
        if all(v is None for v in snap.values()):
            continue
        series = hist["tickers"].setdefault(t, [])
        if series:
            last = series[-1]
            last_vals = {k: last.get(k) for k in FIELDS}
            last_date = datetime.date.fromisoformat(last["date"])
            days = (datetime.date.fromisoformat(today) - last_date).days
            if last["date"] == today:
                series[-1] = {"date": today, **snap}      # 같은 날 재실행 → 갱신
                continue
            if same(last_vals, snap) and days < FORCE_DAYS:
                continue
        series.append({"date": today, **snap})
        added += 1
        if len(series) > MAX_POINTS:
            del series[:len(series) - MAX_POINTS]

    # ── 공시 분해 스냅샷 (accession 바뀔 때만) ──
    for t, entry in (segs.get("items") or {}).items():
        snap = snapshot_from_segments(entry)
        if not snap or not (snap.get("regions") or snap.get("channels")):
            continue
        series = hist["segments"].setdefault(t, [])
        if series and series[-1].get("accession") == snap["accession"]:
            continue
        series.append({"date": today, **snap})
        added += 1

    # ── v1.2 브랜드 점검표 판정 ──
    try:
        append_verdicts(hist, data, today)
    except Exception as e:
        soft_fail(f"브랜드 판정 기록 실패 — {type(e).__name__}: {str(e)[:160]}")

    hist["updated_at"] = datetime.datetime.now(KST).strftime("%Y-%m-%d %H:%M KST")
    os.makedirs("docs", exist_ok=True)
    with open(HIST_PATH, "w", encoding="utf-8") as f:
        json.dump(hist, f, ensure_ascii=False, separators=(",", ":"))
    n_t = sum(len(v) for v in hist["tickers"].values())
    n_s = sum(len(v) for v in hist["segments"].values())
    print(f"saved {HIST_PATH} — 신규 {added}점 / 누적 재무 {n_t}점·분해 {n_s}점", flush=True)


if __name__ == "__main__":
    main()

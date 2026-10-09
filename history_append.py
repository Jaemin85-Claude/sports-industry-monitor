# -*- coding: utf-8 -*-
"""
sports-industry-monitor — 히스토리 축적 (v1)
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
import json
import datetime

KST = datetime.timezone(datetime.timedelta(hours=9))
DATA_PATH = "docs/data.json"
SEG_PATH = "docs/segments.json"
HIST_PATH = "docs/history.json"
FORCE_DAYS = 7          # 변화 없어도 이 일수마다 1점 저장
MAX_POINTS = 400        # 종목당 최대 보관 점수 (약 1년+ 여유)

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

    hist["updated_at"] = datetime.datetime.now(KST).strftime("%Y-%m-%d %H:%M KST")
    os.makedirs("docs", exist_ok=True)
    with open(HIST_PATH, "w", encoding="utf-8") as f:
        json.dump(hist, f, ensure_ascii=False, separators=(",", ":"))
    n_t = sum(len(v) for v in hist["tickers"].values())
    n_s = sum(len(v) for v in hist["segments"].values())
    print(f"saved {HIST_PATH} — 신규 {added}점 / 누적 재무 {n_t}점·분해 {n_s}점", flush=True)


if __name__ == "__main__":
    main()

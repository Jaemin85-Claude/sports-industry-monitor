# -*- coding: utf-8 -*-
"""
sports-industry-monitor — Phase 5: KOSIS 국내 수요 지표 (v1)
프로브로 검증된 통계표만 사용 (§검증 우선):
  DT_1K41012 재별·상품군별 소매판매액지수  → 의복(G21), 신발·가방(G22), 총지수(G0)
  DT_1K41013 소매업태별 판매액지수        → 의복·신발·가방 소매점, 인터넷쇼핑, 백화점
  DT_1KE1007 온라인쇼핑 상품군별 거래액   → 의복/신발/가방/패션잡화/스포츠레저 (objL1+2)
  DT_1J22001 지출목적별 소비자물가지수     → 의류·신발 (C2 이름 필터, 코드 추측 없음)
출력: docs/kosis.json (월별 시계열 + YoY)
§29-D: API가 준 값만 사용, 없는 항목은 수록하지 않음(대시보드에서 '미확인')
"""

import os
import json
import datetime
import requests

API_KEY = os.environ.get("KOSIS_API_KEY", "")
UA = {"User-Agent": "sports-industry-monitor kosis"}
KST = datetime.timezone(datetime.timedelta(hours=9))
DATA_URL = "https://kosis.kr/openapi/Param/statisticsParameterData.do"
MONTHS = 37          # 최근 37개월 (YoY 계산 위해 13개월 이상 필요)
OUT_PATH = "docs/kosis.json"

# ── 수집 정의 ──────────────────────────────────────
# key: [표ID, objL레벨, 항목ID(itmId), 분류 매칭(C1/C2 이름 포함어), 표시명, 단위설명]
SERIES = [
    # 1) 상품군별 소매판매액지수 — 항목=경상지수(T1), 분류 C1=상품군
    ("retail_apparel",  "DT_1K41012", 1, "T1", {"c1": "의류"},
     "소매판매 의류", "지수(2020=100)"),
    ("retail_shoesbag", "DT_1K41012", 1, "T1", {"c1": "신발"},
     "소매판매 신발·가방", "지수(2020=100)"),
    ("retail_total",    "DT_1K41012", 1, "T1", {"c1": "총지수"},
     "소매판매 총지수", "지수(2020=100)"),
    # 2) 업태별 판매액지수 — 항목=경상지수(T1), 분류 C1=업태
    ("store_fashion",   "DT_1K41013", 1, "T1", {"c1": "의복"},
     "의복·신발·가방 소매점", "지수(2020=100)"),
    ("store_internet",  "DT_1K41013", 1, "T1", {"c1": "인터넷쇼핑"},
     "인터넷쇼핑 업태", "지수(2020=100)"),
    ("store_dept",      "DT_1K41013", 1, "T1", {"c1": "백화점"},
     "백화점 업태", "지수(2020=100)"),
    # 3) 온라인쇼핑 거래액 — 항목=거래액(T20), C1=상품군, C2=판매매체(합계)
    ("online_apparel",  "DT_1KE1007", 2, "T20", {"c1": "의복", "c2": "합계"},
     "온라인 의복 거래액", "백만원"),
    ("online_shoes",    "DT_1KE1007", 2, "T20", {"c1": "신발", "c2": "합계"},
     "온라인 신발 거래액", "백만원"),
    ("online_bag",      "DT_1KE1007", 2, "T20", {"c1": "가방", "c2": "합계"},
     "온라인 가방 거래액", "백만원"),
    ("online_fashionacc", "DT_1KE1007", 2, "T20",
     {"c1": "패션용품", "c2": "합계"},
     "온라인 패션용품·악세서리", "백만원"),
    ("online_sports",   "DT_1KE1007", 2, "T20",
     {"c1": "스포츠", "c2": "합계"},
     "온라인 스포츠·레저용품", "백만원"),
    # 4) CPI — 항목=소비자물가지수(T), C1=지역(전국), C2=지출목적
    ("cpi_apparel",     "DT_1J22001", 2, "T", {"c1": "전국", "c2": "의류"},
     "소비자물가 의류·신발", "지수(2020=100)"),
]


def fetch_table(tbl, obj_lv, itm):
    params = {
        "method": "getList", "apiKey": API_KEY,
        "orgId": "101", "tblId": tbl, "itmId": itm,
        "prdSe": "M", "newEstPrdCnt": str(MONTHS),
        "format": "json", "jsonVD": "Y",
    }
    for i in range(1, obj_lv + 1):
        params[f"objL{i}"] = "ALL"
    r = requests.get(DATA_URL, params=params, headers=UA, timeout=90)
    r.raise_for_status()
    data = r.json()
    if isinstance(data, dict):
        raise RuntimeError(f"{tbl} 오류: {data.get('errMsg', data)}")
    return data


def norm(s):
    return (s or "").replace(" ", "")


def pick(rows, match):
    """C1/C2 이름 포함 조건에 맞는 행만 (§29-D: 코드 추측 없이 이름 매칭)"""
    out = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        ok = True
        for lvl, needle in match.items():
            nm = norm(row.get(f"{lvl.upper()}_NM"))
            if norm(needle) not in nm:
                ok = False
                break
        if ok:
            out.append(row)
    return out


def to_series(rows):
    """{'202607': 122.9, ...} + 단위"""
    ser, unit = {}, None
    for row in rows:
        prd = str(row.get("PRD_DE") or "")
        val = row.get("DT")
        if not prd or val in (None, "", "-"):
            continue
        try:
            ser[prd] = float(str(val).replace(",", ""))
        except ValueError:
            continue
        unit = unit or row.get("UNIT_NM")
    return dict(sorted(ser.items())), unit


def yoy(ser):
    """월별 전년 동월 대비 %"""
    out = {}
    for prd, v in ser.items():
        y, m = prd[:4], prd[4:]
        prev = f"{int(y) - 1}{m}"
        pv = ser.get(prev)
        if pv:
            out[prd] = (v / pv - 1) * 100
    return out


def main():
    if not API_KEY:
        print("[ERROR] KOSIS_API_KEY 미설정")
        raise SystemExit(1)

    cache = {}
    out = {"generated_at":
           datetime.datetime.now(KST).strftime("%Y-%m-%d %H:%M KST"),
           "series": {}}

    for key, tbl, lv, itm, match, label, unit_desc in SERIES:
        try:
            ck = (tbl, lv, itm)
            if ck not in cache:
                print(f"fetch {tbl} (objL1~{lv}, itm={itm}) ...")
                cache[ck] = fetch_table(tbl, lv, itm)
            rows = pick(cache[ck], match)
            if not rows:
                print(f"  [WARN] {key}: 조건에 맞는 행 없음 → 수록 안 함")
                continue
            ser, unit = to_series(rows)
            if not ser:
                print(f"  [WARN] {key}: 값 없음 → 수록 안 함")
                continue
            out["series"][key] = {
                "label": label, "unit": unit or unit_desc,
                "table": tbl, "values": ser, "yoy": yoy(ser),
            }
            last = list(ser)[-1]
            y = out["series"][key]["yoy"].get(last)
            print(f"  ✔ {key}: {len(ser)}개월, 최근 {last} = {ser[last]}"
                  f"{'' if y is None else f' (YoY {y:+.1f}%)'}")
        except Exception as e:
            print(f"  [WARN] {key} 실패: {str(e)[:160]}")

    os.makedirs("docs", exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(f"saved {OUT_PATH} ({len(out['series'])}개 시계열)")


if __name__ == "__main__":
    main()

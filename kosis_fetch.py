# -*- coding: utf-8 -*-
"""
sports-industry-monitor — Phase 5: KOSIS 국내 수요 지표 (v1)
프로브로 검증된 통계표만 사용 (§검증 우선):
  DT_1K41012 재별·상품군별 소매판매액지수  → 의복(G21), 신발·가방(G22), 총지수(G0)
  DT_1K41013 소매업태별 판매액지수        → 의복·신발·가방 소매점, 인터넷쇼핑, 백화점
  DT_1KE10071 온라인쇼핑 판매매체별/상품군별 거래액 → 의복/신발/가방/패션잡화/스포츠레저
  DT_1J22001 지출목적별 소비자물가지수     → 의류·신발 (C2 이름 필터, 코드 추측 없음)
v3: 온라인쇼핑 표를 현행 DT_1KE10071로 교체(구표 DT_1KE1007은 2017년 종료),
    분류 이름 후보 복수 지정(축 순서·표기 차이 대응), 미발견 시 후보 목록 진단 출력
v2: 2단계 조회 — ① 1개월 표본으로 분류 코드(C1/C2) 발견 → ② 해당 코드만 지정해
    25개월 조회. CPI(22,064행)처럼 큰 표에서 전체를 받아 필터링하다 지연되던 문제 해결.
    출력 즉시 flush(진행 상황 확인), 타임아웃·재시도 추가.
출력: docs/kosis.json (월별 시계열 + YoY)
§29-D: API가 준 값만 사용, 없는 항목은 수록하지 않음(대시보드에서 '미확인')
"""

import os
import json
import time
import datetime
import requests

API_KEY = os.environ.get("KOSIS_API_KEY", "")
UA = {"User-Agent": "sports-industry-monitor kosis"}
KST = datetime.timezone(datetime.timedelta(hours=9))
DATA_URL = "https://kosis.kr/openapi/Param/statisticsParameterData.do"
MONTHS = 25          # 최근 25개월 (YoY 계산 위해 13개월 이상 필요)
TIMEOUT = 60
RETRY = 2
OUT_PATH = "docs/kosis.json"

# ── 수집 정의 ──────────────────────────────────────
# key: [표ID, objL레벨, 항목ID(itmId), 분류 매칭(C1/C2 이름 포함어), 표시명, 단위설명]
SERIES = [
    # (key, 표ID, objL레벨, itmId, needles, 표시명, 단위설명)
    #   needles: 각 원소는 "대체 표기" 튜플 — 모든 원소가 분류명(C1/C2) 어딘가에
    #   매칭되어야 채택 (축 순서·표기 차이에 무관, §29-D 코드 추측 없음)
    ("retail_apparel",  "DT_1K41012", 1, "T1", [("의복", "의류")],
     "소매판매 의복", "지수(2020=100)"),
    ("retail_shoesbag", "DT_1K41012", 1, "T1", [("신발",)],
     "소매판매 신발·가방", "지수(2020=100)"),
    ("retail_total",    "DT_1K41012", 1, "T1", [("총지수",)],
     "소매판매 총지수", "지수(2020=100)"),
    ("store_fashion",   "DT_1K41013", 1, "T1", [("의복",)],
     "의복·신발·가방 소매점", "지수(2020=100)"),
    ("store_internet",  "DT_1K41013", 1, "T1", [("인터넷",)],
     "인터넷쇼핑 업태", "지수(2020=100)"),
    ("store_dept",      "DT_1K41013", 1, "T1", [("백화점",)],
     "백화점 업태", "지수(2020=100)"),
    ("online_apparel",  "DT_1KE10071", 2, "T20", [("의복", "의류"), ("합계",)],
     "온라인 의복 거래액", "백만원"),
    ("online_shoes",    "DT_1KE10071", 2, "T20", [("신발",), ("합계",)],
     "온라인 신발 거래액", "백만원"),
    ("online_bag",      "DT_1KE10071", 2, "T20", [("가방",), ("합계",)],
     "온라인 가방 거래액", "백만원"),
    ("online_fashionacc", "DT_1KE10071", 2, "T20",
     [("패션용품",), ("합계",)], "온라인 패션용품·악세서리", "백만원"),
    ("online_sports",   "DT_1KE10071", 2, "T20", [("스포츠",), ("합계",)],
     "온라인 스포츠·레저용품", "백만원"),
    ("cpi_apparel",     "DT_1J22001", 2, "T", [("전국",), ("의류",)],
     "소비자물가 의류·신발", "지수(2020=100)"),
]


def log(msg):
    print(msg, flush=True)


def api(tbl, itm, obj_codes, months):
    """obj_codes: {'objL1': 코드 또는 'ALL', ...}"""
    params = {
        "method": "getList", "apiKey": API_KEY,
        "orgId": "101", "tblId": tbl, "itmId": itm,
        "prdSe": "M", "newEstPrdCnt": str(months),
        "format": "json", "jsonVD": "Y",
    }
    params.update(obj_codes)
    last = None
    for attempt in range(RETRY + 1):
        try:
            r = requests.get(DATA_URL, params=params, headers=UA,
                             timeout=TIMEOUT)
            r.raise_for_status()
            data = r.json()
            if isinstance(data, dict):
                raise RuntimeError(data.get("errMsg", str(data)[:120]))
            return data
        except Exception as e:
            last = e
            if attempt < RETRY:
                log(f"    재시도 {attempt + 1}/{RETRY} ({str(e)[:80]})")
                time.sleep(2)
    raise RuntimeError(str(last)[:160])


def discover(tbl, obj_lv, itm):
    """1개월 표본으로 분류 코드 발견 → [(C1코드, C1명, C2코드, C2명)]"""
    codes = {"objL%d" % i: "ALL" for i in range(1, obj_lv + 1)}
    rows = api(tbl, itm, codes, 1)
    out = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        out.append((row.get("C1"), row.get("C1_NM"),
                    row.get("C2"), row.get("C2_NM")))
    log(f"    분류 표본 {len(out)}건 확보")
    return out


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
        log("[ERROR] KOSIS_API_KEY 미설정")
        raise SystemExit(1)

    disc_cache = {}
    out = {"generated_at":
           datetime.datetime.now(KST).strftime("%Y-%m-%d %H:%M KST"),
           "series": {}}

    for key, tbl, lv, itm, match, label, unit_desc in SERIES:
        try:
            log(f"[{key}] {tbl} objL1~{lv} itm={itm}")
            dk = (tbl, lv, itm)
            if dk not in disc_cache:
                log(f"  1단계: 분류 코드 발견 중 ...")
                disc_cache[dk] = discover(tbl, lv, itm)
            # 이름 매칭으로 코드 확정 (§29-D: 코드 추측 없음)
            hit = None
            for c1, c1nm, c2, c2nm in disc_cache[dk]:
                names = [n for n in (c1nm, c2nm) if n]
                used, ok = set(), True
                for alts in match:
                    found = None
                    for i, nm in enumerate(names):
                        if i in used:
                            continue
                        if any(norm(a) in norm(nm) for a in alts):
                            found = i
                            break
                    if found is None:
                        ok = False
                        break
                    used.add(found)
                if ok:
                    hit = (c1, c1nm, c2, c2nm)
                    break
            if not hit:
                pool = sorted({f"{a}|{b}" for _, a, _, b in disc_cache[dk]})
                log(f"  [WARN] 분류 미발견 → 수록 안 함. 후보(최대 25): "
                    f"{', '.join(pool[:25])}")
                continue
            c1, c1nm, c2, c2nm = hit
            codes = {"objL1": c1 or "ALL"}
            if lv >= 2:
                codes["objL2"] = c2 or "ALL"
            log(f"  2단계: {c1nm}"
                f"{' / ' + str(c2nm) if lv >= 2 else ''} → {MONTHS}개월 조회")
            rows = api(tbl, itm, codes, MONTHS)
            ser, unit = to_series(rows)
            if not ser:
                log(f"  [WARN] 값 없음 → 수록 안 함")
                continue
            out["series"][key] = {
                "label": label, "unit": unit or unit_desc,
                "table": tbl, "values": ser, "yoy": yoy(ser),
            }
            last = list(ser)[-1]
            y = out["series"][key]["yoy"].get(last)
            log(f"  ✔ {len(ser)}개월, 최근 {last} = {ser[last]}"
                f"{'' if y is None else f' (YoY {y:+.1f}%)'}")
        except Exception as e:
            log(f"  [WARN] {key} 실패: {str(e)[:160]}")

    os.makedirs("docs", exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    log(f"saved {OUT_PATH} ({len(out['series'])}개 시계열)")


if __name__ == "__main__":
    main()

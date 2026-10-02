# -*- coding: utf-8 -*-
"""
sports-industry-monitor — Phase 5: KOSIS 국내 수요 지표 (v4)
v5: 해외직구(온라인쇼핑동향 해외직접구매액, 분기) 추가 — 표 ID를 추측하지 않고 ① 통계표 검색 API
    ② 후보 표 1분기 표본 조회로 표 이름에 '직접구매'가 있는 표를 찾아 사용(찾은 과정 로그 출력).
    나라(전체·미국·중국·일본·유럽)×상품군(전체·의류·패션·스포츠) 12분기 → kosis.json 'cross_border'
    (2026-10 실행 로그로 확인: DT_1KE1009 '지역별 / 상품군별 온라인쇼핑 해외직접구매액', 백만원.
     지역은 계층(유럽 ⊃ 유럽연합·영국·기타 유럽, 북미 ⊃ 미국·캐나다)이라 이름을 정확히 일치시켜 고름)
프로브로 검증된 통계표만 사용 (§검증 우선):
  DT_1K41012 재별·상품군별 소매판매액지수  → 의복(G21), 신발·가방(G22), 총지수(G0)
  DT_1K41013 소매업태별 판매액지수        → 의복·신발·가방 소매점, 인터넷쇼핑, 백화점
  DT_1KE10071 온라인쇼핑 판매매체별/상품군별 거래액 → 의복/신발/가방/패션잡화/스포츠레저
  DT_1J22001 지출목적별 소비자물가지수     → 의류·신발 (C2 이름 필터, 코드 추측 없음)
v4: 온라인쇼핑 판매매체 합계 표기 '계' 대응(현행 표는 '합계'가 아닌 '계') — 실행 로그로 확인.
    미발견 시 후보 출력 60건으로 확대.
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
SEARCH_URL = "https://kosis.kr/openapi/statisticsSearch.do"

# ── 해외직구(v5) ─────────────────────────────────────
CB_KEYWORD = "해외직접구매"
CB_CANDIDATES = ["DT_1KE1009", "DT_1KE10081", "DT_1KE10091", "DT_1KE10101", "DT_1KE10111",
                 "DT_1KE10121", "DT_1KE10131", "DT_1KE10141"]
CB_QUARTERS = 12
# 이름 매칭: 'exact' = 공백 뺀 이름이 정확히 일치(합계류), 그 밖 = 포함
CB_COUNTRIES = [("total", "전체", {"exact": ("계", "합계", "전체", "총계")}),
                ("us", "미국", {"exact": ("미국",)}),
                ("cn", "중국", {"exact": ("중국",)}),
                ("jp", "일본", {"exact": ("일본",)}),
                ("eu", "유럽", {"exact": ("유럽", "유럽(EU)")})]
CB_CATS = [("total", "전체", {"exact": ("계", "합계", "전체", "총계")}),
           ("fashion", "의류·패션", {"has": ("의류", "패션")}),
           ("sports", "스포츠·레저", {"has": ("스포츠",)})]

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
    ("online_apparel",  "DT_1KE10071", 2, "T20", [("의복", "의류"), ("합계", "계")],
     "온라인 의복 거래액", "백만원"),
    ("online_shoes",    "DT_1KE10071", 2, "T20", [("신발",), ("합계", "계")],
     "온라인 신발 거래액", "백만원"),
    ("online_bag",      "DT_1KE10071", 2, "T20", [("가방",), ("합계", "계")],
     "온라인 가방 거래액", "백만원"),
    ("online_fashionacc", "DT_1KE10071", 2, "T20",
     [("패션용품",), ("합계", "계")], "온라인 패션용품·악세서리", "백만원"),
    ("online_sports",   "DT_1KE10071", 2, "T20", [("스포츠",), ("합계", "계")],
     "온라인 스포츠·레저용품", "백만원"),
    ("cpi_apparel",     "DT_1J22001", 2, "T", [("전국",), ("의류",)],
     "소비자물가 의류·신발", "지수(2020=100)"),
]


def log(msg):
    print(msg, flush=True)


def api(tbl, itm, obj_codes, months, prd_se="M"):
    """obj_codes: {'objL1': 코드 또는 'ALL', ...} · months = 최근 시점 수(분기면 분기 수)"""
    params = {
        "method": "getList", "apiKey": API_KEY,
        "orgId": "101", "tblId": tbl, "itmId": itm,
        "prdSe": prd_se, "newEstPrdCnt": str(months),
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


def _nm_ok(name, rule):
    n = norm(name)
    if "exact" in rule:
        return n in {norm(a) for a in rule["exact"]}
    return any(norm(a) in n for a in rule["has"])


def cb_search():
    """통계표 검색 API로 '해외직접구매' 표 ID 후보 (실패해도 빈 목록)"""
    try:
        r = requests.get(SEARCH_URL, params={
            "method": "getList", "apiKey": API_KEY, "searchNm": CB_KEYWORD,
            "orgId": "101", "format": "json", "jsonVD": "Y", "resultCount": "20"},
            headers=UA, timeout=TIMEOUT)
        data = r.json()
        if isinstance(data, dict):
            log(f"  검색 API 응답: {str(data)[:160]}")
            return []
        out = []
        for row in data:
            tid, tnm = row.get("TBL_ID"), row.get("TBL_NM")
            log(f"  검색: {tid} | {tnm} | {row.get('ORG_ID')}")
            if tid and "직접구매" in norm(tnm) and tid not in out:
                out.append(tid)
        return out
    except Exception as e:
        log(f"  검색 API 실패: {str(e)[:120]}")
        return []


def cb_probe(tbl):
    """후보 표 1분기 표본 → (단계 수, 행) 또는 None. 분류 단계 수를 모르니 2→3→1 순서로 시도"""
    for lv in (2, 3, 1):
        codes = {"objL%d" % i: "ALL" for i in range(1, lv + 1)}
        try:
            rows = api(tbl, "ALL", codes, 1, prd_se="Q")
        except Exception as e:
            log(f"  {tbl} 단계 {lv}: {str(e)[:100]}")
            continue
        rows = [x for x in rows if isinstance(x, dict)]
        if rows:
            return lv, rows
    return None


def cb_axes(rows, lv):
    """각 분류 축(C1~C3)의 이름 집합"""
    return [sorted({r.get(f"C{i}_NM") for r in rows if r.get(f"C{i}_NM")}) for i in range(1, lv + 1)]


def fetch_cross_border():
    """해외직접구매액(분기) — 나라×상품군. 실패 시 None (§29-D: 값 없으면 수록 안 함)"""
    log("[cross_border] 해외직구 표 찾기")
    cands = cb_search() + [t for t in CB_CANDIDATES]
    seen, found = set(), None
    for tbl in cands:
        if tbl in seen:
            continue
        seen.add(tbl)
        pr = cb_probe(tbl)
        if not pr:
            continue
        lv, rows = pr
        tnm = rows[0].get("TBL_NM") or ""
        log(f"  {tbl} 표본 {len(rows)}행 · 표 이름: {tnm} · 시점 {rows[0].get('PRD_DE')}")
        if "직접구매" in norm(tnm):
            found = (tbl, lv, rows, tnm)
            break
    if not found:
        log("  [WARN] 해외직구 표 미발견 → 수록 안 함")
        return None
    tbl, lv, rows, tnm = found
    items = sorted({(r.get("ITM_ID"), r.get("ITM_NM"), r.get("UNIT_NM")) for r in rows})
    axes = cb_axes(rows, lv)
    log(f"  항목: {items}")
    for i, a in enumerate(axes, 1):
        log(f"  분류 C{i} ({len(a)}): {', '.join(a[:40])}")
    # 금액 항목: 이름에 '구매' 또는 단위 '백만원' — 구성비·증감률 제외
    itm = None
    for iid, inm, unit in items:
        n = norm(inm)
        if any(x in n for x in ("구성비", "증감", "비중", "률")):
            continue
        if "구매" in n or "백만원" in norm(unit) or len(items) == 1:
            itm = (iid, inm, unit)
            break
    if not itm:
        log("  [WARN] 금액 항목 미발견 → 수록 안 함")
        return None
    # 축 판정: 나라 축 = '미국'이 있는 축, 상품군 축 = '의류'/'패션'이 있는 축
    ax_cty = next((i for i, a in enumerate(axes) if any("미국" in norm(x) for x in a)), None)
    ax_cat = next((i for i, a in enumerate(axes) if i != ax_cty and
                   any(("의류" in norm(x) or "패션" in norm(x)) for x in a)), None)
    if ax_cty is None or ax_cat is None:
        log(f"  [WARN] 나라·상품군 축 판정 실패(나라 {ax_cty}, 상품군 {ax_cat}) → 수록 안 함")
        return None
    others = [i for i in range(lv) if i not in (ax_cty, ax_cat)]
    codes = {"objL%d" % i: "ALL" for i in range(1, lv + 1)}
    data = api(tbl, itm[0], codes, CB_QUARTERS, prd_se="Q")
    data = [r for r in data if isinstance(r, dict)]
    log(f"  {CB_QUARTERS}분기 조회 {len(data)}행 · 항목 {itm[1]} ({itm[2]})")

    def other_ok(r):
        # 나머지 축(있다면): '구매'가 들어간 값만, 그런 값이 없으면 합계류만
        for i in others:
            nm = r.get(f"C{i + 1}_NM") or ""
            vals = axes[i]
            if any("구매" in norm(v) for v in vals):
                if "구매" not in norm(nm):
                    return False
            elif not _nm_ok(nm, {"exact": ("계", "합계", "전체", "총계")}):
                return False
        return True

    series, names = {}, {}
    for ck, clab, crule in CB_COUNTRIES:
        for gk, glab, grule in CB_CATS:
            sel = [r for r in data if other_ok(r)
                   and _nm_ok(r.get(f"C{ax_cty + 1}_NM"), crule)
                   and _nm_ok(r.get(f"C{ax_cat + 1}_NM"), grule)]
            # 같은 시점이 여럿이면(예: '의류'·'패션' 둘 다 매칭) 첫 분류명만 사용
            if sel:
                first = (sel[0].get(f"C{ax_cty + 1}_NM"), sel[0].get(f"C{ax_cat + 1}_NM"))
                sel = [r for r in sel if (r.get(f"C{ax_cty + 1}_NM"), r.get(f"C{ax_cat + 1}_NM")) == first]
                names[f"{ck}|{gk}"] = f"{first[0]} / {first[1]}"
            ser, _ = to_series(sel)
            if ser:
                series[f"{ck}|{gk}"] = {"values": ser, "yoy": yoy_q(ser)}
    if not series:
        log("  [WARN] 해외직구 값 없음 → 수록 안 함")
        return None
    last = max(p for v in series.values() for p in v["values"])
    for k, v in series.items():
        y = v["yoy"].get(last)
        log(f"  ✔ {k} ({names.get(k)}): {last} = {v['values'].get(last)}"
            f"{'' if y is None else f' (전년 같은 분기 {y:+.1f}%)'}")
    return {"table": tbl, "table_name": tnm, "item": itm[1], "unit": itm[2] or "백만원",
            "last": last, "names": names,
            "countries": {k: lab for k, lab, _ in CB_COUNTRIES},
            "cats": {k: lab for k, lab, _ in CB_CATS}, "series": series}


def yoy_q(ser):
    """분기 전년 같은 분기 대비 % — PRD_DE '202602'·'20262' 모두 대응"""
    out = {}
    for prd, v in ser.items():
        prev = f"{int(prd[:4]) - 1}{prd[4:]}"
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
                log(f"  [WARN] 분류 미발견 → 수록 안 함. 후보(최대 60): "
                    f"{', '.join(pool[:60])}")
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

    try:
        cb = fetch_cross_border()
        if cb:
            out["cross_border"] = cb
    except Exception as e:
        log(f"  [WARN] 해외직구 실패: {str(e)[:160]}")

    os.makedirs("docs", exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    log(f"saved {OUT_PATH} ({len(out['series'])}개 시계열"
        f"{' · 해외직구 ' + str(len(out['cross_border']['series'])) + '개' if out.get('cross_border') else ''})")


if __name__ == "__main__":
    main()

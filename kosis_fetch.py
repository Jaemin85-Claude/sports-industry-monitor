# -*- coding: utf-8 -*-
"""
sports-industry-monitor — Phase 5: KOSIS 국내 수요 지표 (v4)
v5.2: (대표 지시 2026-10-20 '보완안 3') kosis.kr(국가정보자원관리원 27.101.x)도 공공데이터포털처럼 일부 GitHub 서버(IP)에서만 연결이 안 될 수
      있어(10/20 시험: 서버 7대 중 2대에서 같은 대역 정부 사이트가 막힘) — 시작할 때 kosis.kr에 연결만 먼저 시험(6초 × 2번 · 막히면 60초 ×
      재시도로 작업 20분 제한을 넘기던 것을 바로 멈춤)하고, 막혔거나 연결 오류로 못 받은 지표가 있으면 kosis.yml이 새 서버에서 다시 받음
      (KOSIS_ATTEMPT 2·3 — 최대 2번 더, GITHUB_OUTPUT retry=1 · 다시 받을 차례가 남으면 '절반 넘게' 실패 표시는 마지막 차례로 미룸).
      마지막 차례까지 막히면 모든 지표를 이전 값(stale_since)으로 두고 바로 실패 표시(월 1회 수집이라 다음 날을 기다리지 않음 — 수동으로 다시 실행).
      kosis.json conn = 이번 실행의 차례별 서버(IP 앞 두 자리·지역 · blocked = 연결 시험에서 막힘 · reached = 받음)·since(마지막 차례까지 연결
      문제로 못 받은 날)·got(이 실행이 실제로 받아 저장함 — 뒤 차례가 못 받거나 막혀도 앞 차례가 오늘 받은 값은 그대로 두고 실패로 세지 않음,
      커밋이 안 된 차례의 작업 출력은 믿지 않음) — 수집 상태 '통계청 연결 안 됨'(모두 막힘)·'통계청 연결 오류'. 다시 받을 연결 오류 줄은 [WARN]·'실패' 없이.
      KOSIS_TEST_BLOCK(브랜치 수동 실행 test_block — 막힌 서버로 가정할 차례, main에서는 무시)은 시험용
v5.1: (대표 지시 2026-10-09) 조용히 깨지는 것 막기 — 못 받은 시계열·해외직구는 이전 kosis.json 값을 이어 쓰고 stale_since
    (마지막 정상 수집일) 표시, 최상위 failed 목록(수집 상태 '일부 실패')에 기록. 하나도 못 받으면 갱신 시각을 옮기지 않음.
    절반 넘게 못 받으면 '실패 표시'(soft_fail.txt → 워크플로우 마지막 단계 빨간 X → 낮 점검 알림)
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
import re
import socket
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
SCRIPT = "kosis_fetch"
SEARCH_URL = "https://kosis.kr/openapi/statisticsSearch.do"
KOSIS_HOST = "kosis.kr"       # v5.2 시작할 때 연결만 시험하는 주소
NET_ERR = 0                    # v5.2 이번 실행에서 연결 오류·시간 초과로 끝난 요청 수 — 못 받은 지표가 있으면 새 서버에서 다시 받음(main이 비움)

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


def soft_fail(msg):
    """심각한 실패 표시 — 저장은 하되 워크플로우 마지막 단계가 빨간 X로 끝내 점검 알림이 가게 함"""
    print(f"실패 표시: {msg}", flush=True)
    with open("soft_fail.txt", "a", encoding="utf-8") as f:
        f.write(f"{SCRIPT}: {msg}\n")


def load_prev():
    """이전 kosis.json(없거나 깨졌으면 빈 dict)"""
    try:
        with open(OUT_PATH, encoding="utf-8") as f:
            d = json.load(f)
        return d if isinstance(d, dict) else {}
    except Exception:
        return {}


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
    if isinstance(last, (requests.ConnectionError, requests.Timeout)):
        global NET_ERR
        NET_ERR += 1   # v5.2 연결 문제로 끝남 — 새 서버에서 다시 받을 만함
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
        if isinstance(e, (requests.ConnectionError, requests.Timeout)):
            global NET_ERR
            NET_ERR += 1   # v5.2
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


def env_int(name, default):
    try:
        return max(1, int(os.environ.get(name, "") or default))
    except ValueError:
        return default


def tcp_ok(host, port=443, timeout=6, tries=2):
    """v5.2 연결만 시험(요청은 안 보냄) — 막힌 서버는 응답이 없어 시간 초과. 프록시를 거치는 환경이면 시험하지 않고 True"""
    if any(os.environ.get(k) for k in ("HTTPS_PROXY", "https_proxy")):
        return True
    for k in range(tries):
        try:
            socket.create_connection((host, port), timeout=timeout).close()
            return True
        except OSError:
            if k + 1 < tries:
                time.sleep(2)
    return False


def runner_where():
    """v5.2 이 GitHub 서버의 공인 IP 앞 두 자리·지역·망(ipinfo.io) — '4.154.x.x · Washington · AS8075 Microsoft Corporation'. 못 읽으면 ''"""
    d = {}
    try:
        d = requests.get("https://ipinfo.io/json", headers=UA, timeout=5).json()
        d = d if isinstance(d, dict) else {}
    except Exception:
        pass
    if not re.fullmatch(r"\d+(\.\d+){3}", str(d.get("ip") or "")):   # 호출 한도·오류 — IP만이라도
        try:
            r = requests.get("https://api.ipify.org", headers=UA, timeout=5)
            d = {"ip": r.text.strip()} if r.status_code == 200 else {}
        except Exception:
            d = {}
    ip = str(d.get("ip") or "").split(".")
    if len(ip) != 4 or not all(x.isdigit() for x in ip):
        return ""
    return " · ".join(x for x in (".".join(ip[:2]) + ".x.x", str(d.get("region") or ""), str(d.get("org") or "")) if x)


def conn_blocked(attempt):
    """v5.2 kosis.kr 연결 시험 — 막혔으면 True. KOSIS_TEST_BLOCK에 이번 차례가 있으면 막힌 서버로 가정(시험용 — main 실행에서는 무시)"""
    test = {x.strip() for x in os.environ.get("KOSIS_TEST_BLOCK", "").split(",") if x.strip()}
    if test and os.environ.get("GITHUB_REF_NAME") == "main":
        log("  [WARN] KOSIS_TEST_BLOCK은 main 실행에서 무시(시험은 브랜치에서)")
        test = set()
    if str(attempt) in test:
        log(f"  연결 시험 {KOSIS_HOST}: 막힘 — 시험(KOSIS_TEST_BLOCK): 막힌 서버로 가정")
        return True
    ok = tcp_ok(KOSIS_HOST)
    log(f"  연결 시험 {KOSIS_HOST}: {'정상' if ok else '막힘'}")
    return not ok


def prev_tries(pconn, attempt):
    """v5.2 같은 워크플로우 실행의 앞 차례들 — kosis.yml이 작업 출력(conn_tries)으로 넘김(커밋이 안 된 브랜치 시험에서도), 없으면 같은 실행의 파일"""
    if attempt <= 1:
        return []
    try:
        t = json.loads(os.environ.get("KOSIS_PREV_TRIES") or "null")
    except ValueError:
        t = None
    if not isinstance(t, list):
        pc, run_id = (pconn if isinstance(pconn, dict) else {}), os.environ.get("GITHUB_RUN_ID", "")
        t = pc.get("tries") if run_id and pc.get("run") == run_id and isinstance(pc.get("tries"), list) else []
    return [x for x in t if isinstance(x, dict)]


def conn_update(pconn, ok, attempt, final, where, blocked, reached):
    """v5.2 kosis.json conn — tries = 이번 워크플로우 실행의 차례별 서버(blocked = 연결 시험에서 막힘, reached = 지표를 하나라도 받음) ·
    since = 마지막 차례까지 연결 문제로 못 받은 날"""
    run_id = os.environ.get("GITHUB_RUN_ID", "")
    pc = pconn if isinstance(pconn, dict) else {}
    tries = prev_tries(pconn, attempt)[-4:] + [
        {"n": attempt, "where": where, "ok": ok, "blocked": blocked, "reached": reached,
         "at": datetime.datetime.now(KST).strftime("%m-%d %H:%M")}]
    since = pc.get("since") if isinstance(pc.get("since"), str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", pc["since"]) else None
    if ok:
        since = None
    elif final:
        since = since or datetime.datetime.now(KST).date().isoformat()
    c = {"run": run_id, "tries": tries}
    if since:
        c["since"] = since
    if not ok:
        c["keys"] = ["kosis"]
    return c


def gh_retry(conn):
    """v5.2 kosis.yml 다음 작업(새 서버)이 다시 받게 — GITHUB_OUTPUT retry=1 · 차례 기록(한 줄 JSON)"""
    with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as f:
        f.write(f"retry=1\nconn_tries={json.dumps(conn['tries'], separators=(',', ':'))}\n")


def tries_txt(tries):
    """실패 표시 글 — 'GitHub 서버 3대 모두 막힘(4.154.x.x · …; …)' / 연결 시험은 통과했으면 '연결 오류'"""
    wh = "; ".join(t.get("where") or "IP 확인 못 함" for t in tries)
    if tries and all(t.get("blocked") is True for t in tries):
        return ("GitHub 서버 " + (f"{len(tries)}대 모두 막힘" if len(tries) > 1 else "에서 막힘")).replace("서버 에서", "서버에서") + f"({wh})"
    return f"연결 오류·시간 초과(GitHub 서버 {len(tries)}대에서 시도: {wh})"


def save(out):
    os.makedirs("docs", exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)


def main():
    global NET_ERR
    if not API_KEY:
        log("[ERROR] KOSIS_API_KEY 미설정")
        raise SystemExit(1)
    NET_ERR = 0
    # v5.2 몇 번째 차례인지(kosis.yml: 1차 작업 1/3 → 새 서버 다시 받기 2/3·3/3). 환경 변수가 없으면 1/1(혼자 실행)
    attempt, attempts = env_int("KOSIS_ATTEMPT", 1), env_int("KOSIS_ATTEMPTS", 1)
    attempts = max(attempts, attempt)
    final = attempt >= attempts or not os.environ.get("GITHUB_OUTPUT")   # 다음 작업에 넘길 길이 없으면 이번이 마지막
    where = runner_where()
    log(f"GitHub 서버: {where or 'IP 확인 못 함'} · 차례 {attempt}/{attempts}")
    if conn_blocked(attempt):
        prev = load_prev()
        out = dict(prev)   # 받은 것 없음 — 값·갱신 시각은 그대로
        out["conn"] = conn_update(prev.get("conn"), False, attempt, final, where, True, False)
        pc = prev.get("conn") if isinstance(prev.get("conn"), dict) else {}
        run_id = os.environ.get("GITHUB_RUN_ID", "")
        # 같은 실행의 앞 차례가 실제로 받아 저장했는지 — 파일에 남은 표시(conn.got)로만 봄(커밋이 안 된 차례의 작업 출력은 믿지 않음)
        got = bool(run_id) and pc.get("got") == run_id
        if got:
            out["conn"]["got"] = run_id
        if not final:
            gh_retry(out["conn"])
            log(f"통계청(kosis.kr) 연결 안 됨 — 새 서버에서 다시 받기({attempt + 1}/{attempts}) · 지표는 그대로")
        elif got:   # 앞 차례(같은 실행)가 이미 받아 저장함 — 그 결과를 그대로 두고, 못 받은 지표 수로만 판단
            pf = [k for k in prev.get("failed") if isinstance(k, str)] if isinstance(prev.get("failed"), list) else []
            total = len(SERIES) + 1
            log(f"통계청(kosis.kr) 연결 안 됨 — 앞 차례가 받은 결과 그대로(못 받음 {len(pf)}개)")
            if len(pf) * 2 > total:
                soft_fail(f"KOSIS {total}개 중 {len(pf)}개 못 받음 — 다시 받기도 {tries_txt(out['conn']['tries'])}")
        else:   # 마지막 차례까지 막힘 — 모든 지표를 이전 값으로(v5.1 '하나도 못 받음'과 같게) + 바로 실패 표시
            pdate = str(prev.get("generated_at") or "")[:10] or None
            out["series"] = {k: dict(v, stale_since=v.get("stale_since") or pdate)
                             for k, v in (prev.get("series") or {}).items() if isinstance(v, dict)}
            pcb = prev.get("cross_border")
            if isinstance(pcb, dict) and pcb.get("series"):
                out["cross_border"] = dict(pcb, stale_since=pcb.get("stale_since") or pdate)
            out["failed"] = [k for k, *_ in SERIES] + ["cross_border"]
            n_kept = len(out["series"]) + (1 if out.get("cross_border") else 0)
            log(f"수집 결과: 정상 0 · 이전 값 {n_kept} — 통계청 연결 안 됨")
            allb = all(t.get("blocked") is True for t in out["conn"]["tries"])
            soft_fail(f"통계청(kosis.kr) 연결 {'안 됨' if allb else '오류'} — {tries_txt(out['conn']['tries'])} · "
                      + ("이전 값 유지" if n_kept else "값 없음") + " · kosis.yml 수동 실행으로 다시")
        save(out)
        log(f"saved {OUT_PATH} (연결 기록만)" if not final else f"saved {OUT_PATH}")
        return

    disc_cache = {}
    out = {"generated_at":
           datetime.datetime.now(KST).strftime("%Y-%m-%d %H:%M KST"),
           "series": {}}

    net_failed = []   # v5.2 연결 오류·시간 초과로 못 받은 지표(다른 이유로 못 받은 것과 구분 — 새 서버에서 다시 받을 만한 것만)
    for key, tbl, lv, itm, match, label, unit_desc in SERIES:
        n0 = NET_ERR
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
            if NET_ERR > n0 and not final:   # 새 서버에서 다시 받을 연결 오류 — 12:23 점검이 [WARN]·'실패' 줄로 알리므로 그 낱말 없이
                log(f"  {key}: 통계청 연결 오류 — 새 서버에서 다시 받기 예정")
            else:
                log(f"  [WARN] {key} 실패: {str(e)[:160]}")
        if key not in out["series"] and NET_ERR > n0:
            net_failed.append(key)

    n0 = NET_ERR
    try:
        cb = fetch_cross_border()
        if cb:
            out["cross_border"] = cb
    except Exception as e:
        log(f"  [WARN] 해외직구 실패: {str(e)[:160]}" if NET_ERR == n0 or final else "  해외직구: 통계청 연결 오류 — 새 서버에서 다시 받기 예정")
    if not out.get("cross_border") and NET_ERR > n0:
        net_failed.append("cross_border")

    # v5.1 못 받은 항목은 이전 값을 이어 씀(stale_since = 그 값을 마지막으로 정상 수집한 날짜, 이미 있으면 그대로)
    prev = load_prev()
    pdate = str(prev.get("generated_at") or "")[:10] or None
    psers = prev.get("series") or {}
    n_new = len(out["series"]) + (1 if out.get("cross_border") else 0)   # 이번 차례가 새로 받은 것
    # v5.2 같은 실행의 앞 차례가 오늘 받아 저장한 값(파일 conn.got = 이 실행)은 이번 차례가 못 받아도 그대로 둠 — 실패·이전 값으로 바꾸지 않음
    pc = prev.get("conn") if isinstance(prev.get("conn"), dict) else {}
    run_id = os.environ.get("GITHUB_RUN_ID", "")
    same = attempt > 1 and bool(run_id) and pc.get("got") == run_id
    pfail = {k for k in prev.get("failed") or [] if isinstance(k, str)} if isinstance(prev.get("failed"), list) else set()
    fresh = lambda v: isinstance(v, dict) and not v.get("stale_since")
    failed, kept = [], []
    for key, *_ in SERIES:
        if key in out["series"]:
            continue
        if same and key not in pfail and fresh(psers.get(key)) and (psers.get(key) or {}).get("values"):
            out["series"][key] = psers[key]
            if key in net_failed:
                net_failed.remove(key)
            continue
        failed.append(key)
        if (psers.get(key) or {}).get("values"):
            out["series"][key] = dict(psers[key], stale_since=psers[key].get("stale_since") or pdate)
            kept.append(key)
    pcb0 = prev.get("cross_border")
    if not out.get("cross_border") and same and "cross_border" not in pfail and fresh(pcb0) and pcb0.get("series"):
        out["cross_border"] = pcb0
        if "cross_border" in net_failed:
            net_failed.remove("cross_border")
    if not out.get("cross_border"):
        failed.append("cross_border")
        pcb = prev.get("cross_border")
        if pcb and pcb.get("series"):
            out["cross_border"] = dict(pcb, stale_since=pcb.get("stale_since") or pdate)
            kept.append("cross_border")
    total = len(SERIES) + 1
    if failed:
        out["failed"] = failed   # 수집 상태 화면 '일부 실패 n곳(이전 값)' — dart_fetch와 같은 필드
        log(f"수집 결과: 정상 {total - len(failed)} · 이전 값 {len(kept)} · 값 없음 {len(failed) - len(kept)}"
            f" — 못 받음: {', '.join(failed)}")
    if n_new == 0 and prev.get("generated_at"):
        out["generated_at"] = prev["generated_at"]   # 이번 차례가 새로 받은 게 없음 → 갱신 시각을 옮기지 않음('지연'이 뜨게 · 같은 실행의 앞 차례 값이면 그 시각)
    ok = not net_failed   # v5.2 연결 오류로 못 받은 지표가 있으면 다른 서버에서 다시
    out["conn"] = conn_update(prev.get("conn"), ok, attempt, final, where, False, n_new > 0)
    if run_id and (n_new > 0 or same):
        out["conn"]["got"] = run_id   # 이 실행이 실제로 받아 저장함 — 뒤 차례가 막혀도 이 값을 그대로 둠
    if not ok and not final:
        gh_retry(out["conn"])
        log(f"연결 오류로 {len(net_failed)}개 못 받음({', '.join(net_failed)}) — 새 서버에서 다시 받기({attempt + 1}/{attempts})")
    elif len(failed) * 2 > total:
        soft_fail(f"KOSIS {total}개 중 {len(failed)}개 못 받음(이전 값 {len(kept)}개)"
                  + (f" — 연결 오류로 {len(net_failed)}개 · {tries_txt(out['conn']['tries'])}" if not ok else ""))

    save(out)
    log(f"saved {OUT_PATH} ({len(out['series'])}개 시계열"
        f"{' · 해외직구 ' + str(len(out['cross_border']['series'])) + '개' if out.get('cross_border') else ''})")


if __name__ == "__main__":
    main()

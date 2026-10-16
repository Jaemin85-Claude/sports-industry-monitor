# -*- coding: utf-8 -*-
"""
sports-industry-monitor — Phase 10: 물류 (운임·운송기간)
v1: (대표 지시 2026-10-16 '만들어줘') 지정학 리스크(2026-02-28 미국·이스라엘의 이란 공격 이후 호르무즈 봉쇄, 홍해·수에즈 우회)에 따른
    물류비·운송기간 추이를 한국향·중동 기준으로 모아 docs/logistics.json에 저장 — 화면은 더보기 › 물류(build_dashboard v33.4).
    ① 관세청 수출입 운송비용(월간, 공공데이터포털 파일 3개 — 인증키 없이 내려받기, 공공누리 1유형): 해상 수입·수출(40ft 1개당 천원 —
       미국 서부·동부·EU·중국·일본·베트남), 항공 수입(kg당 원 — 미국·EU·중국·일본·베트남). 수입 = FOB 조건 수입신고의 운임(할증료 포함) —
       한국으로 들어오는 화물의 실제 운임. 중동은 보도자료에만 있고 파일에는 없음. 지난 달 값은 다음 해 2월까지 고쳐질 수 있어 매번 파일 전체로 바꿈
    ② KCCI(한국해양진흥공사 컨테이너선운임지수, 매주 월 14시): 부산발 13개 항로 + 종합(항로는 40ft당 달러) — 중동·북유럽·지중해 등.
       첫 실행에 2022-11부터 시계열을 받아 두고 매일 최근 10주를 다시 받아 합침(이용허락 제한 없음)
    ③ IMF PortWatch(무료 API, 주 1회 갱신 · 약 1주 늦음): 해협 하루 통과 척수(전체·컨테이너선) — 호르무즈·바브엘만데브·수에즈·희망봉,
       항만 하루 입항 — 부산·제벨알리·코르파칸·푸자이라. 주별 평균 + 전쟁 전(2026-01-01~02-27) 평균. 배 위치 신호(AIS) 기준이라
       신호를 끈 배는 빠짐(호르무즈는 실제보다 적게 잡힘). 출처 'IMF PortWatch'
    ④ Sea-Intelligence 전 세계 정시율(월간 보도자료 GLP): 정시 도착 비율(%)·늦은 배 평균 지연(일) — 제목·본문에서 숫자만 읽음, 새 기사만 받음
    못 받은 자료는 이전 값을 이어 쓰고 stale_since(마지막 정상 수집일) 표시 · 최상위 status(ok·kept·failed).
    한 실행에서 절반 넘게 실패하거나, 한 자료라도 3일 넘게 이전 값이면 실패 표시(soft_fail.txt → 낮 점검 알림)
출력: docs/logistics.json
§29-D: 출처가 준 값만 저장(추정값·임의 값 없음)
"""

import csv
import datetime
import html as htmlmod
import io
import json
import os
import re
import time

import requests

SCRIPT = "logistics_fetch"
OUT = "docs/logistics.json"
KST = datetime.timezone(datetime.timedelta(hours=9))
UA = {"User-Agent": "Mozilla/5.0 (sports-industry-monitor logistics; +https://github.com/Jaemin85-Claude/sports-industry-monitor)"}
TIMEOUT = 40
WAR_START = "2026-02-28"                       # 전쟁 시작(미국·이스라엘의 이란 공격) — '전쟁 전' 비교 기준
BASE_FROM, BASE_TO = "2026-01-01", "2026-02-27"   # 해협·항만 '전쟁 전 평균' 기간(일별 값 평균)
STALE_ALERT_DAYS = 3                           # 한 자료가 이 일수 넘게 이전 값이면 실패 표시

# ① 관세청 수출입 운송비용 — 공공데이터포털 파일 데이터(월간)
KCS = [  # (블록 키, 데이터 번호, 이름, 단위)
    ("kcs_sea_import", "15116806", "관세청 해상 수입", "천원/40ft"),
    ("kcs_sea_export", "15116850", "관세청 해상 수출", "천원/40ft"),
    ("kcs_air_import", "15116807", "관세청 항공 수입", "원/kg"),
]
KCS_PAGE = "https://www.data.go.kr/data/{}/fileData.do"
KCS_DOWN = "https://www.data.go.kr/cmm/cmm/fileDownload.do?atchFileId={}&fileDetailSn=1&insertDataPrcus=N"

# ② KCCI — 해양진흥공사 해양정보서비스
KCCI_CUR = "https://www.kobc.or.kr/ebz/shippinginfo/kcci/gridList.do?mId=0304000000"
KCCI_TS = "https://www.kobc.or.kr/ebz/shippinginfo/timeseries/gridList.do?mId=0304000000"
KCCI_FROM = "2022-11-01"       # 공식 발표 시작(2022-11-07) 전부터 요청
KCCI_REFRESH_DAYS = 70         # 매일 최근 10주를 다시 받아 합침(고쳐진 값 반영)
KCCI_NAMES = {"KCCI": "종합", "KUWI": "미주 서안", "KUEI": "미주 동안", "KNEI": "북유럽", "KMDI": "지중해",
              "KMEI": "중동", "KAUI": "호주", "KLEI": "남미 동안", "KLWI": "남미 서안", "KSAI": "남아프리카",
              "KWAI": "서아프리카", "KCI": "중국", "KJI": "일본", "KSEI": "동남아"}

# ③ IMF PortWatch — ArcGIS FeatureServer(무료, 키 없음)
PW = "https://services9.arcgis.com/weJ1QsnbMYJlCHdG/arcgis/rest/services/{}/FeatureServer/0/query"
PW_FROM_YEAR = 2025            # 주별 값은 2025년부터(작년 같은 때와 비교)
CHOKE = [("chokepoint6", "호르무즈 해협"), ("chokepoint4", "바브엘만데브 해협"),
         ("chokepoint1", "수에즈 운하"), ("chokepoint7", "희망봉")]
PORTS = [("Busan", "부산"), ("Jebel Ali", "제벨알리"), ("Khor Fakkan", "코르파칸"), ("Fujairah", "푸자이라")]

# ④ Sea-Intelligence 보도자료
GLP_LIST = "https://www.sea-intelligence.com/press-room"
GLP_SITE = "https://www.sea-intelligence.com"
GLP_MAX_FETCH = 16             # 한 실행에 새로 읽는 기사 수 상한
MONTHS = ["january", "february", "march", "april", "may", "june", "july", "august",
          "september", "october", "november", "december"]


def log(msg):
    print(msg, flush=True)


def soft_fail(msg):
    """심각한 실패 표시 — 저장은 하되 워크플로우 마지막 단계가 빨간 X로 끝내 점검 알림이 가게 함"""
    print(f"실패 표시: {msg}", flush=True)
    with open("soft_fail.txt", "a", encoding="utf-8") as f:
        f.write(f"{SCRIPT}: {msg}\n")


def http(url, params=None, data=None, timeout=TIMEOUT, tries=2):
    """GET(또는 data가 있으면 POST) — 연결 오류·5xx는 5초 뒤 한 번 더. 4xx는 바로 오류"""
    err = None
    for k in range(tries):
        try:
            if data is None:
                r = requests.get(url, params=params, headers=UA, timeout=timeout)
            else:
                r = requests.post(url, params=params, data=data, headers=UA, timeout=timeout)
            if r.status_code >= 500:
                raise requests.HTTPError(f"HTTP {r.status_code}")
            if r.status_code != 200:
                raise RuntimeError(f"HTTP {r.status_code}")
            return r
        except (requests.ConnectionError, requests.Timeout, requests.HTTPError) as e:
            err = e
            if k + 1 < tries:
                time.sleep(5)
    raise RuntimeError(f"{type(err).__name__}: {str(err)[:150]}")


def clean(s):
    """HTML 조각 → 글자만(공백 하나로)"""
    return re.sub(r"\s+", " ", htmlmod.unescape(re.sub(r"<[^>]+>", " ", s or ""))).strip()


def table_rows(page):
    """표의 행 → 칸 글자 목록(머리·본문 모두). 스크립트·스타일은 뺌"""
    page = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", page)
    out = []
    for tr in re.findall(r"(?is)<tr\b.*?</tr>", page):
        cs = [clean(c) for c in re.findall(r"(?is)<t[hd]\b[^>]*>(.*?)</t[hd]>", tr)]
        if cs:
            out.append(cs)
    return out


def num(s):
    """'8,885' → 8885, '62.4' → 62.4, 빈칸·'-' → None"""
    s = (s or "").replace(",", "").strip()
    if not re.fullmatch(r"-?\d+(\.\d+)?", s):
        return None
    v = float(s)
    return int(v) if v.is_integer() and "." not in s else v


def today_kst():
    return datetime.datetime.now(KST).date()


# ───────────────────────── ① 관세청 수출입 운송비용 ─────────────────────────
def kcs_page_meta(page):
    """파일 데이터 화면 → (내려받기 번호 FILE_…, 파일 이름 날짜, 수정일, 차기 등록 예정일). 번호가 여럿이면 가장 큰(최신) 것"""
    ids = sorted(set(re.findall(r"FILE_\d{9,}", page)), key=lambda x: int(x[5:]))
    title = clean((re.search(r"(?is)<title>(.*?)</title>", page) or [None, ""])[1])
    fdate = re.search(r"_(\d{8})\b", title)
    mod = re.search(r"수정일</strong>\s*<div class=\"value\">\s*([\d-]{10})", page)
    nxt = re.search(r"차기 등록 예정일</strong>\s*<div class=\"value\">\s*([\d-]{10})", page)
    return (ids[-1] if ids else None,
            f"{fdate.group(1)[:4]}-{fdate.group(1)[4:6]}-{fdate.group(1)[6:]}" if fdate else None,
            mod.group(1) if mod else None, nxt.group(1) if nxt else None)


def parse_kcs_csv(raw):
    """관세청 운송비용 CSV(첫 칸 '기간', 다음 칸 = 지역) → (지역 목록, [[YYYY-MM, 값…], …]). 형식이 다르면 ValueError"""
    text = None
    for enc in ("utf-8-sig", "cp949"):
        try:
            text = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    if text is None:
        raise ValueError("글자 인코딩을 읽지 못함")
    rows = [r for r in csv.reader(io.StringIO(text)) if any(c.strip() for c in r)]
    if not rows or rows[0][0].strip() != "기간":
        raise ValueError(f"첫 칸이 '기간'이 아님: {str(rows[:1])[:120]}")
    cols = [c.strip() for c in rows[0][1:]]
    if len(cols) < 3 or not all(cols):
        raise ValueError(f"지역 칸 이상: {cols}")
    out = []
    for r in rows[1:]:
        p = r[0].strip()
        if not re.fullmatch(r"\d{4}-\d{2}", p):
            continue
        vals = [num(c) for c in (r[1:] + [""] * len(cols))[:len(cols)]]
        if any(v is not None and v < 0 for v in vals):
            raise ValueError(f"음수 값: {r}")
        out.append([p] + vals)
    out.sort(key=lambda x: x[0])
    if len(out) < 24:
        raise ValueError(f"달 수가 너무 적음({len(out)})")
    return cols, out


def fetch_kcs_one(ds, name, unit):
    page = http(KCS_PAGE.format(ds)).text
    fid, fdate, mod, nxt = kcs_page_meta(page)
    if not fid:
        raise RuntimeError("화면에서 내려받기 번호(FILE_…)를 못 찾음")
    raw = http(KCS_DOWN.format(fid), timeout=60).content
    cols, rows = parse_kcs_csv(raw)
    last = rows[-1]
    gap = (today_kst() - datetime.date.fromisoformat(last[0] + "-01")).days
    if gap > 100:   # 9월 자료는 10월 중순에 올라옴 — 석 달 넘게 새 달이 없으면 파일 갱신이 멈춘 것
        raise RuntimeError(f"마지막 달이 {last[0]} — {gap}일째 새 달 없음")
    log(f"  {name}: {len(rows)}달 · {rows[0][0]}~{last[0]} · {' · '.join(f'{c} {v:,}' for c, v in zip(cols, last[1:]) if v is not None)} ({unit})")
    return {"name": name, "unit": unit, "dataset": ds, "cols": cols, "rows": rows,
            "file_date": fdate, "updated": mod, "next": nxt}


# ───────────────────────── ② KCCI ─────────────────────────
def parse_kcci_current(page):
    """이번 주 KCCI 표 → {날짜: {코드: 값}} (이번 주·지난 주 2개). 'Current Index 2026-10-12' 머리에서 날짜"""
    rows = table_rows(page)
    dates = None
    for r in rows:
        j = " ".join(r)
        ds = re.findall(r"(?:Current|Previous)\s+Index\s+(\d{4}-\d{2}-\d{2})", j)
        if len(ds) == 2:
            dates = ds
            break
    if not dates:
        raise ValueError("이번 주·지난 주 날짜 머리를 못 찾음")
    out = {dates[0]: {}, dates[1]: {}}
    for r in rows:
        for i, c in enumerate(r):
            if c in KCCI_NAMES:
                nums = [num(x) for x in r[i + 1:]]
                vals = [v for v in nums if v is not None]
                # 칸: 코드 | 항로 | 비중(%) | 이번 주 | 지난 주 | 변화 → 비중 칸(%)은 숫자가 아님(num이 None)
                if len(vals) >= 2:
                    out[dates[0]][c], out[dates[1]][c] = vals[0], vals[1]
                break
    if "KCCI" not in out[dates[0]] or len(out[dates[0]]) < 10:
        raise ValueError(f"코드 {len(out[dates[0]])}개만 읽음")
    return out


def parse_kcci_series(page):
    """시계열 표 → {날짜: {코드: 값}}. 둘째 머리 줄(KUWI | KUEI | …) 앞에 종합(KCCI)"""
    rows = table_rows(page)
    codes = None
    for r in rows:
        if len(r) >= 10 and all(c in KCCI_NAMES for c in r):
            codes = r if r[0] == "KCCI" else ["KCCI"] + r
            break
    if not codes:
        raise ValueError("코드 머리 줄을 못 찾음")
    out = {}
    for r in rows:
        if r and re.fullmatch(r"\d{4}-\d{2}-\d{2}", r[0]) and len(r) == len(codes) + 1:
            vals = {c: num(v) for c, v in zip(codes, r[1:]) if num(v) is not None}
            if vals.get("KCCI") is not None:
                out[r[0]] = vals
    return out


def fetch_kcci(prev):
    """이번 주 표 + 시계열(처음엔 2022-11부터, 그 뒤엔 최근 10주) → 이전 값과 합쳐 날짜순"""
    have = {r[0]: dict(zip(prev["cols"], r[1:])) for r in (prev or {}).get("rows") or [] if r and r[0]}
    have = {d: {c: v for c, v in vs.items() if v is not None} for d, vs in have.items()}
    today = today_kst()
    s_day = KCCI_FROM if len(have) < 52 else (datetime.date.fromisoformat(max(have)) - datetime.timedelta(days=KCCI_REFRESH_DAYS)).isoformat()
    got, how = {}, []
    try:
        cur = parse_kcci_current(http(KCCI_CUR).text)
        got.update(cur)
        how.append("이번 주 표")
    except Exception as e:
        log(f"  KCCI 이번 주 표 실패: {str(e)[:150]}")
    form = {"sDay": s_day, "eDay": today.isoformat(), "mId": "0304000000", "siteCode": "shippinginfo", "sources": "timeseries"}
    ser = {}
    want = (datetime.date.fromisoformat(s_day) + datetime.timedelta(days=21)).isoformat()
    for meth in ("GET", "POST"):   # 화면 검색 칸(sDay·eDay) — GET이 기간을 무시하면 POST(화면의 '검색'과 같음)
        try:
            r = http(KCCI_TS, params={k: form[k] for k in ("sDay", "eDay")} if meth == "GET" else None,
                     data=form if meth == "POST" else None)
            got_s = parse_kcci_series(r.text)
        except Exception as e:
            log(f"  KCCI 시계열({meth}) 실패: {str(e)[:150]}")
            continue
        if got_s and (not ser or min(got_s) < min(ser)):   # 더 오래전부터 온 쪽을 씀
            ser = got_s
        if ser and min(ser) <= want:
            break
    if ser:
        how.append(f"시계열 {len(ser)}주({min(ser)}~{max(ser)})")
        for d, vs in ser.items():
            got[d] = {**ser[d], **got.get(d, {})}   # 같은 날짜는 이번 주 표 값 우선
    if not got:
        raise RuntimeError("이번 주 표·시계열 모두 실패")
    merged = {**have}
    for d, vs in got.items():
        merged[d] = {**merged.get(d, {}), **vs}
    if s_day == KCCI_FROM and ser and min(ser) > "2023-06-30":
        log(f"  KCCI: 처음 받기에서 시계열이 {min(ser)}부터만 옴 — 이후 매일 쌓음")
    cols = list(KCCI_NAMES)
    rows = [[d] + [merged[d].get(c) for c in cols] for d in sorted(merged)]
    latest = rows[-1][0]
    if (today - datetime.date.fromisoformat(latest)).days > 16:
        raise RuntimeError(f"최신 주가 {latest} — 2주 넘게 새 값 없음")
    last = dict(zip(cols, rows[-1][1:]))
    f = lambda c: f"{last[c]:,}" if isinstance(last.get(c), (int, float)) else "―"
    log(f"  KCCI: {' · '.join(how)} · 모두 {len(rows)}주 · {latest} 종합 {f('KCCI')} · 중동 {f('KMEI')} · 북유럽 {f('KNEI')} · 지중해 {f('KMDI')} 달러/FEU")
    return {"cols": cols, "names": KCCI_NAMES, "rows": rows, "latest": latest}


# ───────────────────────── ③ IMF PortWatch ─────────────────────────
def pw_rows(layer, where, fields):
    """PortWatch 질의 — 1,000건씩 넘겨 받음. 날짜 오름차순"""
    out, off = [], 0
    while True:
        r = http(PW.format(layer), params={"where": where, "outFields": ",".join(fields), "orderByFields": "date ASC",
                                          "resultOffset": off, "resultRecordCount": 1000, "f": "json"}, timeout=60)
        d = r.json()
        if "error" in d:
            raise RuntimeError(f"PortWatch 오류: {str(d['error'])[:150]}")
        fs = d.get("features") or []
        out += [f.get("attributes") or {} for f in fs]
        if len(fs) < 1000 or off >= 9000:
            break
        off += 1000
    return out


def pw_date(v):
    """PortWatch 날짜 — 'YYYY-MM-DD' 글자 또는 밀리초 숫자"""
    if isinstance(v, (int, float)):
        return datetime.datetime.fromtimestamp(v / 1000, datetime.timezone.utc).date()
    return datetime.date.fromisoformat(str(v)[:10])


def weekly(rows, fields):
    """일별 → 주별(월요일 시작) 평균: [[주 시작일, 값1, 값2, 날 수], …]"""
    acc = {}
    for a in rows:
        d = pw_date(a.get("date"))
        wk = (d - datetime.timedelta(days=d.weekday())).isoformat()
        s = acc.setdefault(wk, [[0.0, 0] for _ in fields])
        for i, f in enumerate(fields):
            v = a.get(f)
            if isinstance(v, (int, float)):
                s[i][0] += v
                s[i][1] += 1
    out = []
    for wk in sorted(acc):
        s = acc[wk]
        out.append([wk] + [round(t / n, 1) if n else None for t, n in s] + [max(n for _, n in s)])
    return out


def period_avg(rows, field, d0, d1):
    vs = [a.get(field) for a in rows if d0 <= pw_date(a.get("date")).isoformat() <= d1 and isinstance(a.get(field), (int, float))]
    return round(sum(vs) / len(vs), 1) if vs else None


def pw_item(layer, where, fields, label):
    rows = pw_rows(layer, where, ["date"] + fields)
    if len(rows) < 100:
        raise RuntimeError(f"{label}: 일별 값 {len(rows)}개뿐")
    last = max(pw_date(a.get("date")) for a in rows)
    if (today_kst() - last).days > 30:
        raise RuntimeError(f"{label}: 최신 날짜 {last} — 한 달 넘게 새 값 없음")
    return {"weeks": weekly(rows, fields), "base": [period_avg(rows, f, BASE_FROM, BASE_TO) for f in fields],
            "last_date": last.isoformat()}


def fetch_pw(kind, prev):
    """해협(kind='choke') 또는 항만(kind='ports') — 항목마다 따로: 못 받은 항목은 이전 값(stale_since)"""
    if kind == "choke":
        layer, fields, items = "Daily_Chokepoints_Data", ["n_total", "n_container"], CHOKE
        where = lambda i: f"portid='{i}' AND year>={PW_FROM_YEAR}"
    else:
        layer, fields, items = "Daily_Ports_Data", ["portcalls", "portcalls_container"], PORTS
        where = lambda i: f"portname='{i}' AND year>={PW_FROM_YEAR}"
    old = {x.get("id"): x for x in (prev or {}).get("items") or []}
    out, bad, kept = [], [], []
    for iid, name in items:
        try:
            it = pw_item(layer, where(iid), fields, name)
            out.append({"id": iid, "name": name, **it})
            w = it["weeks"][-1]
            log(f"  {name}: 주 {len(it['weeks'])}개 · 마지막 주 {w[0]}({w[-1]}일) 하루 {w[1]}척(컨테이너선 {w[2]}) · 전쟁 전 {it['base'][0]}척({it['base'][1]})")
        except Exception as e:
            log(f"  {name}: 실패 — {str(e)[:150]}")
            if iid in old:
                o = dict(old[iid])
                o["stale_since"] = o.get("stale_since") or (prev or {}).get("fetched") or today_kst().isoformat()
                out.append(o)
                kept.append(name)
            else:
                bad.append(name)
        time.sleep(0.5)
    if not [x for x in out if not x.get("stale_since")]:
        raise RuntimeError(f"모두 실패({', '.join(bad + kept)})")
    return {"fields": fields, "items": out, "kept": kept, "failed": bad}


# ───────────────────────── ④ Sea-Intelligence 정시율 ─────────────────────────
def glp_list(page):
    """보도자료 목록 → [(주소, 제목)] (같은 기사는 한 번, '계속 읽기' 링크 제외)"""
    out, seen = [], set()
    for m in re.finditer(r'(?is)<a[^>]+href="([^"]*press-room/\d+-[^"#?]*)"[^>]*>(.*?)</a>', page):
        u, t = m.group(1), clean(m.group(2))
        if not t or t.lower().startswith("continue reading") or u in seen:
            continue
        seen.add(u)
        out.append((u if u.startswith("http") else GLP_SITE + u, t))
    return out


def is_glp(title):
    return bool(re.search(r"global\s+schedule\s+reliability", title, re.I))


def parse_glp(page, title):
    """GLP 월간 보도자료 → (자료 달 YYYY-MM, 정시율 %, 늦은 배 평균 지연 일 또는 None). 못 읽으면 ValueError
    달: 제목의 달 이름(연도 없으면 발행 연도, 발행 달보다 뒤면 작년) → 없으면 발행 달의 전달(보도자료는 약 4주 뒤 나옴)
    정시율: 제목의 'n%' → 없으면 본문에서 'schedule'이 든 첫 문장의 'to n%'"""
    pm = (re.search(r'"datePublished"\s*:\s*"(\d{4}-\d{2}-\d{2})', page)
          or re.search(r'property="datePublished"\s+content="(\d{4}-\d{2}-\d{2})', page)
          or re.search(r'"dateModified"\s*:\s*"(\d{4}-\d{2}-\d{2})', page)
          or re.search(r'property="dateModified"\s+content="(\d{4}-\d{2}-\d{2})', page))
    if not pm:
        raise ValueError("발행일 없음")
    pub = datetime.date.fromisoformat(pm.group(1))
    tm = re.search(r"\b(" + "|".join(MONTHS) + r")\b(?:\s+(20\d\d))?", title, re.I)
    if tm:
        mo = MONTHS.index(tm.group(1).lower()) + 1
        yr = int(tm.group(2)) if tm.group(2) else (pub.year if mo <= pub.month else pub.year - 1)
    else:
        prev = pub.replace(day=1) - datetime.timedelta(days=1)
        yr, mo = prev.year, prev.month
    body = clean(re.sub(r"(?is)<(script|style|head)[^>]*>.*?</\1>", " ", page))
    rel = None
    m = re.search(r"(\d{1,2}(?:\.\d+)?)\s?%", title)
    if m:
        rel = float(m.group(1))
    sents = re.split(r"(?<=[.!?;])\s+", body)
    if rel is None:
        for s in sents:
            m = re.search(r"\bto\s+(\d{1,2}(?:\.\d+)?)\s?%", s)
            if m and re.search(r"schedule", s, re.I):
                rel = float(m.group(1))
                break
    delay = None
    for s in sents:
        m = re.search(r"\bto\s+(\d{1,2}\.\d+)\s+days", s)
        if m and re.search(r"delay", s, re.I):
            delay = float(m.group(1))
            break
    if rel is None or not 15 <= rel <= 95:
        raise ValueError(f"정시율을 못 읽음({rel})")
    if delay is not None and not 1 <= delay <= 20:
        delay = None
    return f"{yr}-{mo:02d}", rel, delay


def fetch_glp(prev):
    """목록에서 'Global Schedule Reliability' 기사 중 아직 없는 것만 읽음(처음엔 둘째 쪽까지 — 지난 1년)"""
    old = {r[0]: r for r in (prev or {}).get("months") or [] if r and r[0]}
    skip = list((prev or {}).get("skip") or [])   # 읽었지만 쓰지 않은 기사(형식이 다름·같은 달 중복) — 매일 다시 받지 않게
    known = {r[3] for r in old.values() if len(r) > 3} | set(skip)
    arts = glp_list(http(GLP_LIST).text)
    if not arts:
        raise RuntimeError("보도자료 목록을 못 읽음")
    if len(old) < 10:
        try:
            arts += glp_list(http(GLP_LIST, params={"start": 100}).text)
        except Exception as e:
            log(f"  정시율 목록 둘째 쪽 실패: {str(e)[:120]}")
    new, tried = dict(old), 0
    for url, title in arts:
        if not is_glp(title) or url in known or tried >= GLP_MAX_FETCH:
            continue
        tried += 1
        try:
            page = http(url).text
        except Exception as e:
            log(f"  정시율 기사 받기 실패({title[:50]}): {str(e)[:120]}")   # 일시 오류 — 다음 실행에서 다시
            continue
        try:
            ym, rel, delay = parse_glp(page, title)
        except ValueError as e:
            log(f"  정시율 기사 형식 다름({title[:50]}): {str(e)[:120]} — 건너뜀")
            skip.append(url)
            continue
        if ym in new and new[ym][3] != url:
            log(f"  정시율 {ym}: 이미 다른 기사로 있음 — 그대로 둠({title[:50]})")
            skip.append(url)
            continue
        new[ym] = [ym, rel, delay, url]
        log(f"  정시율 {ym}: {rel}% · 늦은 배 평균 지연 {delay if delay is not None else '―'}일 ({title[:60]})")
        time.sleep(1)
    if not new:
        raise RuntimeError("정시율 기사를 하나도 못 읽음")
    months = [new[k] for k in sorted(new)]
    log(f"  정시율: {len(months)}달 · {months[0][0]}~{months[-1][0]} · 새로 읽은 기사 {tried}건")
    return {"months": months, "skip": skip[-200:]}


# ───────────────────────── 실행 ─────────────────────────
def run_block(key, label, fn, prev_all, out, status):
    """블록 하나 — 성공하면 새 값(fetched = 오늘), 실패하면 이전 값 + stale_since(마지막 정상 수집일)"""
    prev = prev_all.get(key)
    log(f"[{label}]")
    try:
        blk = fn(prev)
        blk["fetched"] = today_kst().isoformat()
        blk["label"] = label
        out[key] = blk
        inner = blk.pop("kept", []) or []
        bad = blk.pop("failed", []) or []
        if inner or bad:   # 해협·항만: 일부 항목만 이전 값·값 없음
            status["kept"].append(f"{label}({'·'.join(inner + bad)})")
        else:
            status["ok"].append(label)
    except Exception as e:
        log(f"  [WARN] {label} 실패 — {str(e)[:200]}" + (" · 이전 값 유지" if prev else ""))
        if prev:
            blk = dict(prev)
            blk["stale_since"] = prev.get("stale_since") or prev.get("fetched") or today_kst().isoformat()
            out[key] = blk
            status["kept"].append(label)
        else:
            status["failed"].append(label)


def main():
    prev_all = {}
    if os.path.exists(OUT):
        try:
            with open(OUT, encoding="utf-8") as f:
                prev_all = json.load(f)
        except Exception as e:
            log(f"[WARN] 이전 {OUT} 읽기 실패: {str(e)[:120]}")
    out = {"generated_at": datetime.datetime.now(KST).strftime("%Y-%m-%d %H:%M KST"), "war_start": WAR_START,
           "base_period": [BASE_FROM, BASE_TO]}
    status = {"ok": [], "kept": [], "failed": []}
    for key, ds, name, unit in KCS:
        run_block(key, name, lambda p, ds=ds, name=name, unit=unit: fetch_kcs_one(ds, name, unit), prev_all, out, status)
    run_block("kcci", "KCCI 부산발 운임", fetch_kcci, prev_all, out, status)
    run_block("choke", "해협 통과", lambda p: fetch_pw("choke", p), prev_all, out, status)
    run_block("ports", "항만 입항", lambda p: fetch_pw("ports", p), prev_all, out, status)
    run_block("glp", "전 세계 정시율", fetch_glp, prev_all, out, status)
    out["status"] = status
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    n_all = len(KCS) + 4
    n_kept = len([s for s in status["kept"] if "(" not in s])
    log(f"수집 결과: 정상 {len(status['ok'])} · 이전 값 {n_kept} · 일부 항목 이전 값 {len(status['kept']) - n_kept} · 값 없음 {len(status['failed'])}")
    log(f"saved {OUT}")
    bad = n_kept + len(status["failed"])
    if bad * 2 > n_all:
        soft_fail(f"물류 자료 {n_all}개 중 {bad}개 못 받음 — " + ", ".join(status["kept"] + status["failed"]))
    old = []
    today = today_kst()
    for key, blk in out.items():
        if not isinstance(blk, dict):
            continue
        ss = [blk.get("stale_since")] + [x.get("stale_since") for x in blk.get("items") or [] if isinstance(x, dict)]
        for s in ss:
            if s and (today - datetime.date.fromisoformat(s)).days > STALE_ALERT_DAYS:
                old.append(f"{blk.get('label') or key}({s}부터)")
                break
    if old:
        soft_fail(f"{STALE_ALERT_DAYS}일 넘게 이전 값: " + ", ".join(old))


if __name__ == "__main__":
    main()

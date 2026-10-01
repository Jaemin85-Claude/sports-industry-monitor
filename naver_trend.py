# -*- coding: utf-8 -*-
"""
sports-industry-monitor — Phase 8: 네이버 데이터랩 검색 관심도 (v1)
v1.1: 월간 합계 추가(교차 그래프용) — 전체 검색어를 5묶음(각 20개 이하)으로 한 번에 요청해 같은 배율로 합산,
      월별 전년 대비 계산(최근 37개월). 검색어 보정: 브룩스(모델명 고스트·글리세린), 가니(가니 코펜하겐)
v1: 핵심 브랜드 29개의 네이버 검색어 트렌드(주간, 최근 2년) — NAVER API HUB 검색어 트렌드 API.
    요청마다 나이키를 기준 키워드로 함께 넣고 '나이키 최근 4주 평균 = 100'으로 환산해 요청 간 비교가 되게 함.
    지표: 규모(나이키=100) · 전년 대비(최근 4주 vs 1년 전 같은 4주) · 최근 추세(최근 4주 vs 직전 12주)
키: GitHub Secrets NCP_APIGW_API_KEY_ID · NCP_APIGW_API_KEY
    키가 없거나 호출이 실패하면 기존 파일을 그대로 두고 정상 종료(대시보드 갱신은 계속) — 로그에 [WARN]/[ERROR]
출력: docs/naver_trend.json
§29-D: API가 준 값만 사용, 실패·미제공은 null
"""

import os
import json
import time
import datetime
import requests

URL = "https://naverapihub.apigw.ntruss.com/search-trend/v1/search"
KEY_ID = os.environ.get("NCP_APIGW_API_KEY_ID", "")
KEY = os.environ.get("NCP_APIGW_API_KEY", "")
KST = datetime.timezone(datetime.timedelta(hours=9))
OUT = "docs/naver_trend.json"
WEEKS = 104          # 차트용 2년
MONTHS = 37          # 월간 합계: 월별 전년 대비 25개월
PER_REQ = 4          # 요청당 브랜드 4개 + 기준(나이키) = API 상한 5개

# 기준 키워드: 모든 요청에 함께 넣어 환산 기준으로 씀
ANCHOR = ("나이키", "nike", "NKE", ["나이키", "nike"])

# (표시명, 뉴스 키, 연결 종목 또는 None, 검색어) — 한글·영문 표기를 함께 넣고,
# 흔한 단어(킨·에코·브룩스·헌터 등)는 제품어를 붙여 다른 뜻의 검색을 줄임
BRANDS = [
    ("뉴발란스", "newbalance", "krd:nb_eland", ["뉴발란스", "new balance", "newbalance"]),
    ("우포스", "oofos", None, ["우포스", "oofos", "우포스 슬리퍼"]),
    ("아디다스", "adidas", "ADS.DE", ["아디다스", "adidas"]),
    ("호카", "hoka", "DECK", ["호카", "hoka", "호카오네오네"]),
    ("드래곤디퓨전", "dragondiffusion", None, ["드래곤디퓨전", "드래곤 디퓨전", "dragon diffusion"]),
    ("메종키츠네", "kitsune", None, ["메종키츠네", "메종 키츠네", "maison kitsune"]),
    ("푸마", "puma", "PUM.DE", ["푸마", "puma"]),
    ("킨(KEEN)", "keen", None, ["킨샌들", "킨 샌들", "keen 샌들", "keen"]),
    ("가니", "ganni", None, ["가니 백", "가니 원피스", "가니 코펜하겐", "ganni"]),
    ("언더아머", "ua", "UAA", ["언더아머", "under armour"]),
    ("헌터", "hunter", None, ["헌터부츠", "헌터 부츠", "헌터 레인부츠", "hunter boots"]),
    ("닥터마틴", "drmartens", "DOCS.L", ["닥터마틴", "dr martens", "dr.martens"]),
    ("크록스", "crocs", "CROX", ["크록스", "crocs"]),
    ("핏플랍", "fitflop", None, ["핏플랍", "fitflop"]),
    ("락포트", "rockport", None, ["락포트", "rockport"]),
    ("피레넥스", "pyrenex", None, ["피레넥스", "pyrenex"]),
    ("클락스", "clarks", None, ["클락스", "clarks", "클락스 왈라비"]),
    ("브룩스", "brooks", None, ["브룩스 러닝화", "브룩스러닝", "brooks running", "브룩스 고스트", "브룩스 글리세린"]),
    ("파라부트", "paraboot", None, ["파라부트", "paraboot"]),
    ("와일드동키", "wilddonkey", None, ["와일드동키", "wild donkey"]),
    ("휴먼메이드", "humanmade", None, ["휴먼메이드", "human made"]),
    ("CEP", "cep", None, ["cep 컴프레션", "cep 양말", "cep 종아리"]),
    ("노르다", "norda", None, ["노르다", "norda", "노르다 001"]),
    ("비비안웨스트우드", "viviennewestwood", None, ["비비안웨스트우드", "비비안 웨스트우드", "vivienne westwood"]),
    ("에코(ECCO)", "ecco", None, ["에코 신발", "ecco 신발", "ecco"]),
    ("단톤", "danton", None, ["단톤", "danton"]),
    ("어그", "hoka", "DECK", ["어그", "ugg", "어그부츠"]),
    ("샤카웨어", "shakawear", None, ["샤카웨어", "shaka wear"]),
]


class FatalAPI(Exception):
    """인증·한도 오류 — 나머지 요청도 실패하므로 전체 중단"""


def date_range():
    """어제 기준 마지막 일요일까지의 완전한 주 WEEKS개 (주 시작 = 월요일)"""
    ref = datetime.datetime.now(KST).date() - datetime.timedelta(days=1)
    end = ref - datetime.timedelta(days=(ref.weekday() + 1) % 7)       # 일요일
    start = end - datetime.timedelta(days=7 * WEEKS - 1)                 # 월요일
    return start, end


def call(start, end, groups, unit="week"):
    body = {"startDate": start.isoformat(), "endDate": end.isoformat(), "timeUnit": unit,
            "keywordGroups": [{"groupName": g, "keywords": kw} for g, kw in groups]}
    headers = {"X-NCP-APIGW-API-KEY-ID": KEY_ID, "X-NCP-APIGW-API-KEY": KEY,
               "Content-Type": "application/json"}
    for attempt in range(3):
        r = requests.post(URL, headers=headers, json=body, timeout=30)
        if r.status_code in (401, 403):
            raise FatalAPI(f"인증 실패 {r.status_code}: {r.text[:200]} — "
                           "GitHub Secrets NCP_APIGW_API_KEY_ID·NCP_APIGW_API_KEY와 API HUB 이용 신청 확인")
        if r.status_code == 429:
            raise FatalAPI(f"호출 한도 초과 429: {r.text[:200]}")
        if r.status_code >= 500 and attempt < 2:
            time.sleep(3 * (attempt + 1))
            continue
        r.raise_for_status()
        return {res["title"]: {d["period"]: float(d["ratio"]) for d in res.get("data", [])}
                for res in r.json().get("results", [])}
    return {}


def mean(xs):
    return sum(xs) / len(xs) if xs else None


def metrics(vals):
    """vals: 주간 값(오래된 순). 비율 지표라 환산 배율과 무관"""
    recent = mean(vals[-4:])
    yago = mean(vals[-56:-52]) if len(vals) >= 56 else None
    prev12 = mean(vals[-16:-4]) if len(vals) >= 16 else None
    pct = lambda a, b: round((a / b - 1) * 100, 1) if (a is not None and b) else None
    return recent, pct(recent, yago), pct(recent, prev12)


def collect():
    start, end = date_range()
    names = [b[0] for b in BRANDS]
    weeks, rows, anchor_row = None, {}, None
    for i in range(0, len(BRANDS), PER_REQ):
        batch = BRANDS[i:i + PER_REQ]
        groups = [(ANCHOR[0], ANCHOR[3])] + [(b[0], b[3]) for b in batch]
        try:
            res = call(start, end, groups)
        except FatalAPI:
            raise
        except Exception as e:
            print(f"  [WARN] 요청 실패({', '.join(b[0] for b in batch)}): {str(e)[:150]}", flush=True)
            continue
        anc = res.get(ANCHOR[0]) or {}
        if not anc:
            print(f"  [WARN] 기준(나이키) 값 없음 — {', '.join(b[0] for b in batch)} 건너뜀", flush=True)
            continue
        if weeks is None:
            weeks = sorted(anc)
        anc_vals = [anc.get(w, 0.0) for w in weeks]
        base = mean(anc_vals[-4:])
        scale = (100.0 / base) if base else None
        if anchor_row is None:
            anchor_row = (anc_vals, scale)
        for name, news, link, kw in batch:
            vals = [res.get(name, {}).get(w, 0.0) for w in weeks]
            rows[name] = (vals, scale)
        time.sleep(0.5)
    if weeks is None:
        return None
    out_brands = []
    for name, news, link, kw in [(ANCHOR[0], ANCHOR[1], ANCHOR[2], ANCHOR[3])] + BRANDS:
        vals, scale = anchor_row if name == ANCHOR[0] else rows.get(name, (None, None))
        if vals is None:
            out_brands.append({"name": name, "news": news, "link": link, "keywords": kw,
                               "scale": None, "yoy": None, "trend": None, "s": None})
            continue
        recent, yoy, trend = metrics(vals)
        sc = round(recent * scale, 2) if (scale and recent is not None) else None
        out_brands.append({"name": name, "news": news, "link": link, "keywords": kw,
                           "scale": sc, "yoy": yoy, "trend": trend, "low": sc is not None and sc < 1,
                           "s": [round(v * scale, 2) if scale else round(v, 2) for v in vals]})
        print(f"  {name}: 규모 {sc if sc is not None else '―'} · 전년 대비 "
              f"{'%+.1f%%' % yoy if yoy is not None else '―'} · 최근 추세 "
              f"{'%+.1f%%' % trend if trend is not None else '―'}", flush=True)
    got = sum(1 for b in out_brands if b["s"] is not None)
    print(f"  수집 브랜드 {got}/{len(out_brands)}개 · 주간 {len(weeks)}점 ({weeks[0]} ~ {end.isoformat()})", flush=True)
    return {"generated_at": datetime.datetime.now(KST).strftime("%Y-%m-%d %H:%M KST"),
            "source": "네이버 데이터랩 검색어 트렌드 (NAVER API HUB)",
            "basis": "주간 검색량 지수 · 나이키 최근 4주 평균 = 100",
            "start": start.isoformat(), "end": end.isoformat(), "anchor": ANCHOR[0],
            "weeks": weeks, "brands": out_brands}


def month_range():
    """지난달까지 완전한 달 MONTHS개"""
    end = datetime.datetime.now(KST).date().replace(day=1) - datetime.timedelta(days=1)
    y, m = end.year, end.month - (MONTHS - 1)
    while m <= 0:
        y, m = y - 1, m + 12
    return datetime.date(y, m, 1), end


def collect_monthly():
    """기준·브랜드 검색어 전체를 20개씩 5묶음 이하로 나눠 한 번에 요청 → 같은 배율이라 묶음 값을 더하면
    전체 검색량에 비례. 월별 전년 대비(같은 달 비교)를 계산"""
    kws = list(dict.fromkeys(list(ANCHOR[3]) + [k for b in BRANDS for k in b[3]]))
    if len(kws) > 100:
        print(f"  [WARN] 월간 합계 검색어 {len(kws)}개 — 100개까지만 사용", flush=True)
        kws = kws[:100]
    groups = [(f"묶음{i // 20 + 1}", kws[i:i + 20]) for i in range(0, len(kws), 20)]
    start, end = month_range()
    res = call(start, end, groups, unit="month")
    months = sorted({p for s in res.values() for p in s})
    if not months:
        return None
    total = [sum(s.get(p, 0.0) for s in res.values()) for p in months]
    yoy = [round((total[i] / total[i - 12] - 1) * 100, 1) if i >= 12 and total[i - 12] else None
           for i in range(len(total))]
    last = next((v for v in reversed(yoy) if v is not None), None)
    print(f"  월간 합계: 검색어 {len(kws)}개 · {months[0][:7]} ~ {months[-1][:7]} · "
          f"최근 달 전년 대비 {'%+.1f%%' % last if last is not None else '―'}", flush=True)
    return {"months": [p[:7] for p in months], "total": [round(v, 3) for v in total], "yoy": yoy,
            "keywords": len(kws)}


def main():
    if not KEY_ID or not KEY:
        print("[WARN] 네이버 API 키 미설정 — 검색 관심도 수집 건너뜀(기존 파일 유지)")
        return
    try:
        out = collect()
    except FatalAPI as e:
        print(f"[ERROR] 네이버 API {e} — 기존 파일 유지", flush=True)
        return
    except Exception as e:
        print(f"[ERROR] 네이버 검색 관심도 수집 실패: {str(e)[:200]} — 기존 파일 유지", flush=True)
        return
    if not out:
        print("[ERROR] 네이버 검색 관심도: 받은 데이터 없음 — 기존 파일 유지")
        return
    try:
        out["monthly"] = collect_monthly()
    except FatalAPI as e:
        print(f"[ERROR] 네이버 API {e} — 월간 합계 생략", flush=True)
        out["monthly"] = None
    except Exception as e:
        print(f"  [WARN] 월간 합계 실패: {str(e)[:150]}", flush=True)
        out["monthly"] = None
    os.makedirs("docs", exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(f"saved {OUT}")


if __name__ == "__main__":
    main()

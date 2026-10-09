# -*- coding: utf-8 -*-
"""
sports-industry-monitor — Phase 8: 네이버 데이터랩 검색 관심도 (v1)
v1.7: (대표 지시 2026-10-09) 조용히 깨지는 것 막기 — 요청 묶음이 실패해 빈 브랜드는 이전 naver_trend.json 값을 이어 쓰고
      stale_since(마지막 정상 수집일) 표시. 월간 합계·브랜드 월간이 실패해도 이전 값 유지(달이 바뀌어 칸이 안 맞으면 묶음 전체를 이전 값으로).
      최상위 status(이전 값 쓴 브랜드·월간·값 없는 브랜드 월간). 브랜드(주간·월간) 절반 넘게 못 받음·전체 실패·인증·한도 오류·
      월간 합계 이틀 연속 실패면 '실패 표시'(soft_fail.txt → 워크플로우 마지막 단계 빨간 X → 낮 점검 알림)
v1.6: 스케쳐스 추가(대표 지시 2026-10-09) — 공식 표기 '스케쳐스'와 흔한 표기 '스케처스'·skechers 합산, 연결은 국내 법인
      (krd:skechers_kr, 미국 본사 상장폐지). 월간 합계(판매 vs 검색)에도 포함(대표 선택) — 37개월을 매번 다시 받아 선이 끊기지 않음
v1.5: 국내 패션·아이웨어 브랜드별 월간 검색(brand_monthly, 3년 전 1월부터) — '검색 관심도 vs 실적'(연간 검색 증감 vs 매출 증감)용.
      요청마다 나이키를 함께 넣어 '나이키 최근 12개월 월평균 = 100'으로 환산(유통사처럼 여러 브랜드를 더할 수 있게).
      페르솔 제외(규모 0.02, 검색량이 거의 없어 순위만 흐림)
v1.4: 글로벌 아이웨어 브랜드 11개 추가(EYE_BRANDS, group 'eye', 대표 요청) — 레이밴·오클리·페르솔·프라다·구찌·생로랑·
      까르띠에·디올·톰포드·린드버그·모스콧. 브랜드명만으로는 의류·가방 검색이 섞이는 명품은 '선글라스·안경' 검색어로 한정.
      같은 나이키 기준 · 월간 합계에는 넣지 않음. 국내 브랜드 수집(KR_BRANDS)은 group 'kr' 그대로(뉴스 키 = DART 법인 id 연결)
v1.3: 국내 패션·아이웨어 브랜드 13개 추가(KR_BRANDS, 대표 요청) — 같은 나이키 기준으로 주간 지수 수집, 결과에 group 표시.
      월간 합계(판매 vs 검색 교차 그래프)는 기존 브랜드만 유지해 시계열 의미가 바뀌지 않게 함
v1.2: 클락스→비바굿즈(0933.HK)·휴먼메이드→456A.T 기업 상세 연결(상장사 추가에 맞춤)
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
SCRIPT = "naver_trend"
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
    ("클락스", "clarks", "0933.HK", ["클락스", "clarks", "클락스 왈라비"]),
    ("브룩스", "brooks", None, ["브룩스 러닝화", "브룩스러닝", "brooks running", "브룩스 고스트", "브룩스 글리세린"]),
    ("파라부트", "paraboot", None, ["파라부트", "paraboot"]),
    ("와일드동키", "wilddonkey", None, ["와일드동키", "wild donkey"]),
    ("휴먼메이드", "humanmade", "456A.T", ["휴먼메이드", "human made"]),
    ("CEP", "cep", None, ["cep 컴프레션", "cep 양말", "cep 종아리"]),
    ("노르다", "norda", None, ["노르다", "norda", "노르다 001"]),
    ("비비안웨스트우드", "viviennewestwood", None, ["비비안웨스트우드", "비비안 웨스트우드", "vivienne westwood"]),
    ("에코(ECCO)", "ecco", None, ["에코 신발", "ecco 신발", "ecco"]),
    ("단톤", "danton", None, ["단톤", "danton"]),
    ("어그", "hoka", "DECK", ["어그", "ugg", "어그부츠"]),
    ("샤카웨어", "shakawear", None, ["샤카웨어", "shaka wear"]),
    ("스케쳐스", "skechers", "krd:skechers_kr", ["스케쳐스", "스케처스", "skechers"]),   # v1.6 맨 뒤에 둬 기존 묶음 유지
]
# 국내 패션 브랜드(v1.3) — 연결은 DART 국내 법인(krd:). 월간 합계에는 넣지 않음
KR_BRANDS = [
    ("락피쉬웨더웨어", "aubrandz", "krd:aubrandz", ["락피쉬웨더웨어", "락피쉬", "rockfish weatherwear"]),
    ("마르디 메크르디", "piecepeace", "krd:piecepeace", ["마르디메크르디", "마르디 메크르디", "mardi mercredi"]),
    ("마뗑킴", "matinkim", "krd:matinkim", ["마뗑킴", "마땡킴", "matin kim"]),
    ("마리떼", "layer", "krd:layer", ["마리떼", "마리떼프랑소와저버", "마리떼 프랑소와 저버", "marithe"]),
    ("코닥어패럴", "highlight", "krd:highlight", ["코닥어패럴", "코닥 어패럴", "kodak apparel"]),
    ("커버낫", "bcave", "krd:bcave", ["커버낫", "covernat"]),
    ("아더에러", "fivespace", "krd:fivespace", ["아더에러", "ader error", "adererror"]),
    ("스탠드오일", "koza", "krd:koza", ["스탠드오일", "stand oil"]),
    ("안다르", "andar", "krd:andar", ["안다르", "andar"]),
    ("캉골", "sjgroup", "krd:sjgroup", ["캉골", "kangol"]),
    ("로우클래식", "lowclassic", "krd:lowclassic", ["로우클래식", "low classic"]),
    ("젠틀몬스터", None, "krd:iicombined", ["젠틀몬스터", "gentle monster"]),
    ("블루엘리펀트", None, "krd:blueelephant", ["블루엘리펀트", "blue elephant"]),
]
KR_NAMES = {b[0] for b in KR_BRANDS}
# 글로벌 아이웨어(v1.4) — 연결: 레이밴·오클리·프라다 = 에실로룩소티카(라이선스 포함), 구찌·생로랑·까르띠에·
# 린드버그 = 케어링아이웨어코리아, 디올 = 시원아이웨어(국내 수입 유통). 톰포드·모스콧은 연결 대상 없음. 월간 합계에는 넣지 않음
EYE_BRANDS = [
    ("레이밴", None, "EL.PA", ["레이밴", "레이벤", "rayban", "ray-ban", "ray ban"]),
    ("오클리", None, "EL.PA", ["오클리", "oakley", "오클리 선글라스"]),
    ("프라다 아이웨어", "prada", "EL.PA", ["프라다 선글라스", "프라다 안경", "프라다 안경테", "prada 선글라스"]),
    ("구찌 아이웨어", "gucci", "krd:kering_ey_kr", ["구찌 선글라스", "구찌 안경", "구찌 안경테", "gucci 선글라스"]),
    ("생로랑 아이웨어", "ysl", "krd:kering_ey_kr", ["생로랑 선글라스", "생로랑 안경", "생로랑 안경테", "saint laurent 선글라스"]),
    ("까르띠에 아이웨어", None, "krd:kering_ey_kr", ["까르띠에 안경", "까르띠에 선글라스", "까르띠에 안경테", "cartier 안경"]),
    ("린드버그", None, "krd:kering_ey_kr", ["린드버그 안경", "린드버그 안경테", "lindberg 안경", "린드버그"]),
    ("디올 아이웨어", "dior", "krd:seeone", ["디올 선글라스", "디올 안경", "디올 안경테", "dior 선글라스"]),
    ("톰포드 아이웨어", None, None, ["톰포드 선글라스", "톰포드 안경", "톰포드 안경테", "tom ford 안경"]),
    ("모스콧", None, None, ["모스콧", "moscot", "모스콧 렘토쉬"]),
]
EYE_NAMES = {b[0] for b in EYE_BRANDS}


class FatalAPI(Exception):
    """인증·한도 오류 — 나머지 요청도 실패하므로 전체 중단"""


def soft_fail(msg):
    """심각한 실패 표시 — 저장은 하되 워크플로우 마지막 단계가 빨간 X로 끝내 점검 알림이 가게 함"""
    print(f"실패 표시: {msg}", flush=True)
    with open("soft_fail.txt", "a", encoding="utf-8") as f:
        f.write(f"{SCRIPT}: {msg}\n")


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
    ALL = BRANDS + KR_BRANDS + EYE_BRANDS
    weeks, rows, anchor_row = None, {}, None
    for i in range(0, len(ALL), PER_REQ):
        batch = ALL[i:i + PER_REQ]
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
    for name, news, link, kw in [(ANCHOR[0], ANCHOR[1], ANCHOR[2], ANCHOR[3])] + ALL:
        vals, scale = anchor_row if name == ANCHOR[0] else rows.get(name, (None, None))
        grp = "kr" if name in KR_NAMES else ("eye" if name in EYE_NAMES else "global")
        if vals is None:
            out_brands.append({"name": name, "news": news, "link": link, "keywords": kw, "group": grp,
                               "scale": None, "yoy": None, "trend": None, "s": None})
            continue
        recent, yoy, trend = metrics(vals)
        sc = round(recent * scale, 2) if (scale and recent is not None) else None
        out_brands.append({"name": name, "news": news, "link": link, "keywords": kw, "group": grp,
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


def collect_brand_monthly():
    """국내 패션·아이웨어 브랜드별 월간 검색(v1.5). 요청 = 나이키 + 브랜드 4개, 나이키 최근 12개월 월평균 = 100으로 환산"""
    today = datetime.datetime.now(KST).date()
    end = today.replace(day=1) - datetime.timedelta(days=1)
    start = datetime.date(end.year - 3, 1, 1)
    ALL = KR_BRANDS + EYE_BRANDS
    months, series = None, {}
    for i in range(0, len(ALL), PER_REQ):
        batch = ALL[i:i + PER_REQ]
        groups = [(ANCHOR[0], ANCHOR[3])] + [(b[0], b[3]) for b in batch]
        try:
            res = call(start, end, groups, unit="month")
        except FatalAPI:
            raise
        except Exception as e:
            print(f"  [WARN] 브랜드 월간 요청 실패({', '.join(b[0] for b in batch)}): {str(e)[:150]}", flush=True)
            continue
        anc = res.get(ANCHOR[0]) or {}
        if months is None and anc:
            months = sorted(anc)
        if not anc or months is None:
            continue
        base = mean([anc.get(m, 0.0) for m in months][-12:])
        if not base:
            continue
        for b in batch:
            series[b[0]] = [round(res.get(b[0], {}).get(m, 0.0) * 100.0 / base, 3) for m in months]
        time.sleep(0.5)
    if not months or not series:
        return None
    ym = [m[:7] for m in months]
    y1, y0 = str(end.year - 1), str(end.year - 2)
    def ysum(v, y, upto=12):
        xs = [x for p, x in zip(ym, v) if p[:4] == y and int(p[5:7]) <= upto]
        return sum(xs) if len(xs) == min(12, upto) else None
    def pct(a, b):
        return round((a / b - 1) * 100, 1) if (a is not None and b) else None
    for name, v in list(series.items())[:3]:
        print(f"  월간 {name}: {y1}년 vs {y0}년 {pct(ysum(v, y1), ysum(v, y0))}% · "
              f"{end.year}년 1~{end.month}월 vs 전년 같은 기간 {pct(ysum(v, str(end.year), end.month), ysum(v, y1, end.month))}%",
              flush=True)
    print(f"  브랜드 월간: {len(series)}/{len(ALL)}개 · {ym[0]} ~ {ym[-1]}", flush=True)
    return {"months": ym, "basis": "월간 검색량 지수 · 나이키 최근 12개월 월평균 = 100", "series": series}


def load_prev():
    """이전 naver_trend.json(없거나 깨졌거나 형식이 다르면 None)"""
    try:
        with open(OUT, encoding="utf-8") as f:
            d = json.load(f)
        return d if isinstance(d, dict) else None
    except Exception:
        return None


def keep_prev(out, prev):
    """v1.7 이번에 못 받은 값은 이전 파일 값을 이어 씀. stale_since = 그 값을 마지막으로 정상 수집한 날짜
    (이전 값에 이미 있으면 그대로). 반환 status {kept_brands, failed_brands, monthly_kept, brand_monthly_kept,
    brand_monthly_failed(이전 값도 없어 브랜드 월간에서 빠진 브랜드)}"""
    prev = prev or {}
    pdate = str(prev.get("generated_at") or "")[:10] or None
    # ① 주간 브랜드: 이름으로 찾아 값(규모·전년 대비·추세·주간 s)을 통째로 이어 씀. 연결·뉴스 키·그룹은 지금 정의대로.
    #    s는 그때 받은 배열 그대로라 주가 바뀐 날엔 끝 주가 weeks보다 한 주 이를 수 있음(None을 끼우면 그래프가 0으로 꺾임)
    old_b = {b.get("name"): b for b in prev.get("brands") or []}
    kept, failed = [], []
    for i, b in enumerate(out["brands"]):
        if b.get("s") is not None:
            continue
        ob = old_b.get(b["name"])
        if ob and ob.get("s") is not None:
            out["brands"][i] = dict(ob, news=b["news"], link=b["link"], group=b["group"],
                                    stale_since=ob.get("stale_since") or pdate)
            kept.append(b["name"])
        else:
            failed.append(b["name"])
    # ② 월간 합계: 실패(None)면 이전 묶음 그대로
    monthly_kept = False
    om = prev.get("monthly")
    if out.get("monthly") is None and om:
        out["monthly"] = dict(om, stale_since=om.get("stale_since") or pdate)
        monthly_kept = True
    # ③ 브랜드 월간: 빠진 브랜드만 이전 값으로. 달 목록이 바뀌었으면(매월 1일) 칸이 안 맞으므로 묶음 전체를 이전 값으로
    #    (화면·주간 메일이 여러 브랜드를 같은 칸끼리 더함). stale_since = {브랜드: 날짜}
    bm, obm = out.get("brand_monthly"), prev.get("brand_monthly")
    bm_kept = []
    names = [b[0] for b in KR_BRANDS + EYE_BRANDS]
    if obm and obm.get("series"):
        o_since = obm.get("stale_since") if isinstance(obm.get("stale_since"), dict) else {}
        lost = [n for n in names if n in obm["series"] and n not in ((bm or {}).get("series") or {})]
        if not bm or (lost and obm.get("months") != bm.get("months")):
            bm_kept = list(obm["series"])
            out["brand_monthly"] = dict(obm, stale_since={n: o_since.get(n) or pdate for n in bm_kept})
        elif lost:
            bm["series"].update({n: obm["series"][n] for n in lost})
            bm["stale_since"] = {n: o_since.get(n) or pdate for n in lost}
            bm_kept = lost
    got = (out.get("brand_monthly") or {}).get("series") or {}
    return {"kept_brands": kept, "failed_brands": failed, "monthly_kept": monthly_kept,
            "brand_monthly_kept": bm_kept, "brand_monthly_failed": [n for n in names if n not in got]}


def main():
    prev = load_prev()
    if not KEY_ID or not KEY:
        print("[WARN] 네이버 API 키 미설정 — 검색 관심도 수집 건너뜀(기존 파일 유지)")
        soft_fail("네이버 API 키 없음 — 검색 관심도 이전 값 유지")
        return
    try:
        out = collect()
    except FatalAPI as e:
        print(f"[ERROR] 네이버 API {e} — 기존 파일 유지", flush=True)
        soft_fail("네이버 API 인증·한도 오류 — 검색 관심도 이전 값 유지")
        return
    except Exception as e:
        print(f"[ERROR] 네이버 검색 관심도 수집 실패: {str(e)[:200]} — 기존 파일 유지", flush=True)
        soft_fail("네이버 검색 관심도 수집 실패 — 이전 값 유지")
        return
    if not out:
        print("[ERROR] 네이버 검색 관심도: 받은 데이터 없음 — 기존 파일 유지")
        soft_fail("네이버 검색 관심도 받은 데이터 없음 — 이전 값 유지")
        return
    m_fatal = False                              # v1.7 월간에서 인증·한도 오류
    try:
        out["monthly"] = collect_monthly()
    except FatalAPI as e:
        print(f"[ERROR] 네이버 API {e} — 월간 합계 생략", flush=True)
        out["monthly"], m_fatal = None, True
    except Exception as e:
        print(f"  [WARN] 월간 합계 실패: {str(e)[:150]}", flush=True)
        out["monthly"] = None
    try:
        out["brand_monthly"] = collect_brand_monthly()
    except FatalAPI as e:
        print(f"[ERROR] 네이버 API {e} — 브랜드 월간 생략", flush=True)
        out["brand_monthly"], m_fatal = None, True
    except Exception as e:
        print(f"  [WARN] 브랜드 월간 실패: {str(e)[:150]}", flush=True)
        out["brand_monthly"] = None
    bm_names = [b[0] for b in KR_BRANDS + EYE_BRANDS]
    bm_got = (out["brand_monthly"] or {}).get("series") or {}
    bm_bad = sum(1 for n in bm_names if n not in bm_got)   # 오늘 못 받은 브랜드 월간(이전 값으로 채우기 전)
    m_twice = out["monthly"] is None and bool(((prev or {}).get("monthly") or {}).get("stale_since"))
    st = out["status"] = keep_prev(out, prev)   # v1.7 못 받은 값은 이전 값으로
    n_all = len(out["brands"]) - 1               # 기준(나이키) 제외
    n_bad = len(st["kept_brands"]) + len(st["failed_brands"])
    print(f"  수집 결과: 정상 {n_all - n_bad} · 이전 값 {len(st['kept_brands'])} · 값 없음 {len(st['failed_brands'])}"
          + (" · 월간 합계 이전 값" if st["monthly_kept"] else "")
          + (f" · 브랜드 월간 이전 값 {len(st['brand_monthly_kept'])}" if st["brand_monthly_kept"] else "")
          + (f" · 브랜드 월간 값 없음 {len(st['brand_monthly_failed'])}" if st["brand_monthly_failed"] else ""), flush=True)
    if st["kept_brands"]:
        print(f"  이전 값 이어 씀: {', '.join(st['kept_brands'])}", flush=True)
    if n_bad * 2 > n_all:
        soft_fail(f"네이버 검색 관심도 브랜드 {n_all}개 중 {n_bad}개 못 받음(이전 값 {len(st['kept_brands'])}개)")
    # 월간(판매 vs 검색·검색 vs 실적): 인증·한도 오류, 월간 합계 이틀 연속 실패(요청 1건이라 하루 일시 오류는 넘김),
    # 브랜드 월간 절반 넘게 못 받음 → 실패 표시 한 줄
    why = ((["인증·한도 오류"] if m_fatal else []) + (["합계 이틀 연속 실패"] if m_twice else [])
           + ([f"브랜드별 {len(bm_names)}개 중 {bm_bad}개 못 받음"] if bm_bad * 2 > len(bm_names) else []))
    if why:
        soft_fail(f"네이버 월간 검색 {' · '.join(why)} — 이전 값 유지")
    os.makedirs("docs", exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(f"saved {OUT}")


if __name__ == "__main__":
    main()

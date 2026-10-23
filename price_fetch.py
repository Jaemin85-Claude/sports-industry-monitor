# -*- coding: utf-8 -*-
"""
sports-industry-monitor — Phase 11: 해외 정가 (나라별 브랜드 대표 상품 소비자가)
v1.3: (대표 지시 2026-10-22 '브랜드별 대표 인기 상품으로 골라서 추가 — 최소 5개 이상씩') 상품 13 → 56개(브랜드마다 5~7개 · 값 227개 —
    나라별로 같은 품번을 GitHub 서버에서 확인한 것만 · 그 나라 몰에 없거나 품번·사양이 다르거나 할인가가 정가로 보이면 그 나라는 뺌, 이유는 상품 줄 주석).
    ① SFCC형 몰(푸마 한국 등)이 가격인하 중이면 JSON-LD에 판매가만 있어, 이 상품 가격 칸의 취소선 정가(strike-through list)를 정가로 —
    취소선 곁 판매가 칸 값이 이 상품 판매가와 같을 때만(추천 상품 칸 섞임 방지 · 검토 반영) · 판매가보다 높고 5배 안(푸마 한국 팔레르모 10/22 119,000 → 35,700원 · 70% 할인)
    ② 한 실행 최대 6 → 11분(값 1개 약 2초 · update.yml 해외 정가 단계 8 → 13분 · 작업 25 → 32분) ③ 온러닝·살로몬 나라별 주소 도우미 _on·_sal.
    ④ 브랜치 시험(10/22 · 216/223 · 385초): 살로몬 해외가 9번째 요청 뒤 403(우회 안 함) → 같은 사이트 요청 간격 HOST_GAP(살로몬 해외 8초) ·
    몇 값만 못 받은 날(사이트가 중간에 막음·연결 끊김 — 써코니 한국 1건)도 다음 날 그 값만 한 번 더(알림 없이) · 같은 사이트가 연달아 2번
    응답 없으면(연결 오류·시간 초과) 그 실행에서 건너뜀(한 사이트가 11분을 다 쓰지 않게) · 푸마 인헤일 → 디비에이트 나이트로 엘리트 4
    (인헤일은 미국 몰이 전 색상 할인가 73.99달러뿐 — 할인가가 정가로 보이면 그 나라는 뺀다는 기준 · 다른 나라 몰에는 없음).
v1.2: (대표 지시 2026-10-22 '추가 가능 5곳 넣어주세요') 드래곤디퓨전·헌터·언더아머·써코니·브룩스 대표 상품 추가(접속 시험 10/22 —
    나라별 같은 상품 주소·가격 칸을 GitHub 서버에서 확인). ① 상품 페이지에 JSON-LD가 없고 schema.org 마이크로데이터(itemprop)만 있는
    SFCC형 몰(써코니 해외) — 이 상품 품번(data-stock-number)이 있을 때만, 판매가(itemprop price · 가능하면 priceincents)와
    '원래 가격'(price-standard — 판매가가 이 상품 가격과 같을 때만)을 읽음 · 독일식 소수점(190,00)도 ② 쇼피파이 변형 품번이 바코드인 몰
    (헌터 미국·영국)은 상품 주소(handle)에 품번이 있으면 그 상품 ③ 그 나라 수입사 품번이 따로 있으면 cc_code(브룩스 일본 BRM4933)
    ④ 이름으로 찾는 상품 중 code_in_page면 페이지에 품번이 있어야 함(써코니·브룩스 한국 — 품번이 JSON-LD 밖 상품 정보 칸에만 있음).
    브랜치 시험(10/22): 56/56 받음 — 써코니 독일은 할인 중(€160 → €128)인데 '128,00 &#8364;'의 HTML 기호 숫자가 섞여 원래 가격을 못 읽음 → 기호를 먼저 풂.
    검토 반영: 쇼피파이 .json도 변형의 통화(price_currency)가 그 나라 통화가 아니면 실패(멕시코 서버면 페소가 달러로 저장될 수 있음 —
    해외 쇼피파이 몰이 생겨서) · cc_code를 바꾸면 그 나라 이전 값은 쓰지 않음(prices.json items에 cc_code 저장) ·
    마이크로데이터 priceincents는 다음 가격 칸으로 넘어가 읽지 않음.
v1.1: (2026-10-22 main 첫 수집에서 푸마 멕시코가 전 색상 30% 세일이라 할인가 1,539.3페소가 정가로 저장됨 — JSON-LD에 정가 표기 없음)
    SFCC형 몰 화면 데이터의 "c_listPrice"(정가)·"c_salePrice"(판매가)를 정가 명세로 읽음 — 판매가가 이 상품 JSON-LD 가격과 같을 때만
    (추천 상품 섞임 방지 · 정가는 판매가의 1~3배일 때만). 푸마 멕시코 확인(2026-10-22 브랜치 진단: c_listPrice 2199 · c_salePrice 1539.3).
v1: (대표 지시 2026-10-21 '국가별 브랜드 대표상품 소비자가격 — 미주·유럽·중남미 vs 한국 RRP' · 수기 없음 · 할인 전 풀프라이스 ·
    환율로 한국이 몇 % 싸거나 비싼지 · 브랜드 상세 하단 · 나이키 포함) 브랜드 공식몰의 같은 상품(글로벌 품번)을 나라별로 받아
    docs/prices.json에 저장 — 원화 환산·차이(%)는 화면(build_dashboard)이 그날 환율(data.json fx)로 계산.
    ① 나이키 = 나이키 상품 정보(api.nike.com product_feed, styleColor로 찾음)의 정가 fullPrice — 할인 중이어도 정가가 따로 있음
    ② 그 밖의 공식몰 = 상품 페이지의 구조화 데이터(schema.org JSON-LD): 정가 명세(ListPrice·StrikethroughPrice)가 있으면 그 값,
       없으면 그 상품 색상·사이즈별 가격 중 가장 높은 값(일부 색상만 할인일 때 정가) · 살로몬 해외는 기본가(basePrice)
    ③ 한국 쇼피파이형 몰(살로몬·닥터마틴) = 상품 .json의 compare_at_price(정가)·price 중 높은 값, 변형(사이즈)의 품번이 글로벌 품번과 같아야 함
    찾는 상품 = 글로벌 품번이 품번·주소에 있는 JSON-LD 상품 우선(없을 때만 이름의 모델명 — 관련·추천 상품 칸은 빼고, 이름이 다른
    상품이 여럿이면 실패) — 추천·관련 상품 가격이 섞이지 않게. 넘겨짐(3xx)은 직접 따라가며 매번 robots.txt·막힘을 먼저 확인.
    할인 가드: 이번 값이 저장된 정가보다 낮으면(모든 색상이 할인 중일 때) 120일 동안은 저장된 정가를 지킴(obs에 이번 값) — 그 뒤에도 낮으면 새 정가.
    나이키 fullPrice는 정가 자체라 가드 없이 바로 반영. 정가가 1.5배 넘게 오르면(나이키는 내려도) 바로 바꾸지 않고 다음 확인 때
    비슷하면(10% 안) 반영(cand).
    주 1회(7일) — 매일 update-dashboard 안에서 돌되 7일이 안 지났고 상품 목록이 같으면 건너뜀(update.yml 수동 실행 입력 price_force=1 → PRICE_FORCE=1이면 바로).
    절반 넘게 실패했거나, 한 브랜드 값을 하나도 못 받았거나, 시간 초과로 다 못 받은 날은 '받은 날'(fetched)을 옮기지 않고 다음 날
    그때 못 받은 값만 다시 받음(tried · 다시 받기도 못 받으면 실패 표시 · 다음 주 받을 날이면 전체를 다시). 전체 받기는 잘 끝났는데
    몇 값만 못 받은 날도 다음 날 그 값만 한 번 더(v1.3 · 또 못 받아도 알림 없이 다음 주에 — 21일 기준은 그대로).
    상품의 품번을 바꾸면 그 상품의 이전 값·값 없음 기록은 쓰지 않음(id가 같아도 다른 상품).
    봇 차단은 우회하지 않음: 우리 봇 이름(UA)을 밝히고 robots.txt(RFC 9309 — 우리 이름 그룹 우선·* 와일드카드·가장 긴 규칙)를 먼저 확인,
    robots.txt가 서버 오류·연결 안 됨이면 그 사이트는 이번 실행 건너뜀(예외: robots.txt를 두지 않는 API 주소는 같은 회사 대표 사이트의
    robots.txt를 따름 — ROBOTS_ALT), 403/429를 받으면 그 사이트에 더 요청하지 않음, 주소당 1번만 요청
    (접속 시험 2026-10-21: 아디다스·뉴발란스·아식스·크록스 한국·에코·몽클레르·룰루레몬·랄프로렌·어그·스케쳐스 한국은 403/429라 넣지 않음).
    못 받으면 이전 값(stale_since = 마지막으로 받은 날) · 전에 받던 값이 '팔지 않음'으로 바뀌어도 실패로 셈 · 이전 값도 없으면 failed(값 없음, 처음 실패한 날).
    한 실행에서 절반 넘게 실패하거나, 한 값이 21일 넘게 이전 값·값 없음이면 실패 표시(soft_fail.txt).
    나라를 늘리면 MK + build_dashboard PR_ORD·PR_CC·PR_SYM + (새 통화면) fetch_data FX를 함께 고친다.
"""
import datetime, hashlib, json, os, re, time, urllib.parse
from html import unescape
import requests

SCRIPT = "price_fetch"
OUT = "docs/prices.json"
KST = datetime.timezone(datetime.timedelta(hours=9))
BOT = "sports-industry-monitor"   # robots.txt에서 우리를 가리키는 이름(UA 안의 이름과 같게)
UA = f"Mozilla/5.0 (compatible; {BOT} price bot; +https://github.com/Jaemin85-Claude/sports-industry-monitor)"
HDR = {"User-Agent": UA, "Accept": "text/html,application/json;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.8,ko;q=0.6"}
DAYS = 7            # 주 1회
SALE_GUARD = 120    # 일 — 이 기간 안에 정가보다 낮게 보이면 할인으로 보고 정가를 지킴
STALE_ALERT = 21    # 일 — 이 일수 넘게 이전 값이면 실패 표시
TIME_LIMIT = 13 * 60   # 초 — 한 실행 최대(넘으면 남은 것은 이전 값) · v1.3 상품 56개·값 227개(1개 약 2초)라 6 → 11분 · v1.4 값 299개라 13분
GAP = 1.5           # 초 — 요청 사이 쉬는 시간
HOST_GAP = {"www.salomon.com": 8}   # 초 — 같은 사이트 요청 사이 최소 간격(v1.3 · 10/22 브랜치 시험에서 살로몬 해외가 9번째 요청 뒤 403 — 천천히 요청)
JUMP = 1.5          # 배 — 정가가 이만큼 넘게 바뀌면 다음 확인 때 같아야 반영

# 나라 → (나이키 상품 정보 marketplace·language, 통화)
MK = {"KR": ("KR", "ko", "KRW"), "US": ("US", "en", "USD"), "GB": ("GB", "en-GB", "GBP"), "DE": ("DE", "de", "EUR"),
      "JP": ("JP", "ja", "JPY"), "MX": ("MX", "es-419", "MXN")}
NIKE_FEED = ("https://api.nike.com/product_feed/threads/v3/?filter=marketplace({m})&filter=language({l})"
             "&filter=channelId(d9a5bc42-4b9c-4976-858a-f159cf99c647)&filter=productInfo.merchProduct.styleColor({s})")

# 대표 상품 — brand는 브랜드 점검표(네이버 감시 브랜드) 이름과 같게. urls 없는 나라는 그 브랜드 공식몰에서 받지 못하는 곳(시험 2026-10-21)
DM = "https://www.drmartens.com"
def _on(slug):   # 온러닝 — 나라별 몰 주소(상품 주소 꼴이 같음)
    return {cc: f"https://www.on.com/{loc}/products/{slug}" for cc, loc in (("KR", "ko-kr"), ("US", "en-us"), ("GB", "en-gb"), ("DE", "de-de"), ("JP", "ja-jp"))}


def _sal(kr, slug):   # 살로몬 — 한국 쇼피파이 상품(.json, 색상 품번) + 해외 모델 페이지(미국·영국·독일, 모델 기본가)
    return {"KR": f"https://salomon.co.kr/products/{kr}.json", **{cc: f"https://www.salomon.com/{loc}/product/{slug}" for cc, loc in (("US", "en-us"), ("GB", "en-gb"), ("DE", "de-de"))}}


def _arc(kr, slug, jp=None, g="mens/"):   # 아크테릭스 — 한국 시즌 상품 페이지(시즌마다 번호·한국 품번이 바뀜) + 미국·영국·독일(같은 주소 꼴) + 일본 쇼피파이 페이지
    u = {"KR": f"https://arcteryx.co.kr/products/view/{kr}", **{cc: f"https://arcteryx.com/{loc}/en/shop/{g}{slug}" for cc, loc in (("US", "us"), ("GB", "gb"), ("DE", "de"))}}
    if jp:
        u["JP"] = f"https://arcteryx.jp/products/{jp}"
    return u


def _keen(kr, h, jp=True, gb=None, de=True):   # 킨 — 한국 LF 공식몰(고도몰 상품 번호) + 미국·영국·독일·일본 쇼피파이 상품 .json(같은 상품 주소 꼴)
    u = {"KR": f"https://www.keenfootwear.kr/goods/goods_view.php?goodsNo={kr}", "US": f"https://www.keenfootwear.com/products/{h}.json",
         "GB": f"https://www.keenfootwear.co.uk/products/{gb or h}.json"}
    if de:
        u["DE"] = f"https://www.keenfootwear.de/en/products/{h}.json"
    if jp:
        u["JP"] = f"https://www.keenfootwear.jp/products/{jp if isinstance(jp, str) else h}.json"
    return u


def _oofos(kr, h):   # 우포스 — 한국 LF 공식몰(고도몰) + 미국 쇼피파이 .json(영국·독일·일본·멕시코는 공식 온라인몰 없음 — 소매점 판매)
    return {"KR": f"https://www.oofos.co.kr/goods/goods_view.php?goodsNo={kr}", "US": f"https://www.oofos.com/products/{h}.json"}


PRODUCTS = [
    {"id": "nike-af1", "brand": "나이키", "name": "에어포스 1 '07", "code": "CW2288-111", "src": "nike", "cc": ["KR", "US", "GB", "DE", "JP", "MX"]},
    {"id": "nike-dunk", "brand": "나이키", "name": "덩크 로우 레트로", "code": "DD1391-100", "src": "nike", "cc": ["KR", "US", "GB", "DE", "JP", "MX"]},
    {"id": "nike-am90", "brand": "나이키", "name": "에어맥스 90", "code": "CN8490-100", "src": "nike", "cc": ["KR", "US", "GB", "DE", "JP", "MX"]},   # 브라질은 나이키 직영이 아님(시험 2026-10-21 · 결과 없음)
    {"id": "nike-blazer77", "brand": "나이키", "name": "블레이저 미드 '77 빈티지", "code": "BQ6806-100", "src": "nike", "cc": ["KR", "US", "GB", "DE", "JP", "MX"]},
    {"id": "nike-cortez", "brand": "나이키", "name": "코르테즈", "code": "DM4044-108", "src": "nike", "cc": ["KR", "US", "GB", "DE", "JP", "MX"]},
    {"id": "nike-aj1low", "brand": "나이키", "name": "에어 조던 1 로우", "code": "553558-161", "src": "nike", "cc": ["KR", "US", "GB", "DE", "JP", "MX"]},
    {"id": "nike-vomero5", "brand": "나이키", "name": "줌 보메로 5", "code": "BV1358-003", "src": "nike", "cc": ["KR", "US", "GB", "DE", "JP", "MX"]},
    {"id": "puma-speedcat", "brand": "푸마", "name": "스피드캣 OG", "code": "398846", "src": "page", "hint": "speedcat", "urls": {
        "KR": "https://kr.puma.com/kr/ko/pd/%EC%8A%A4%ED%94%BC%EB%93%9C%EC%BA%A3-og-%3Cbr%3Espeedcat-og/398846.html",
        "US": "https://us.puma.com/us/en/pd/speedcat-og-sneakers/398846",
        "GB": "https://uk.puma.com/uk/en/pd/speedcat-og-sneakers-unisex/398846",
        "DE": "https://eu.puma.com/de/de/pd/speedcat-og-sneakers/398846",
        "JP": "https://jp.puma.com/jp/ja/pd/%E3%83%A6%E3%83%8B%E3%82%BB%E3%83%83%E3%82%AF%E3%82%B9-%E3%82%B9%E3%83%94%E3%83%BC%E3%83%89%E3%82%AD%E3%83%A3%E3%83%83%E3%83%88-og-%E3%82%B9%E3%83%8B%E3%83%BC%E3%82%AB%E3%83%BC/398846",
        "MX": "https://mx.puma.com/mx/es/pd/tenis-speedcat-og/398846.html"}},
    {"id": "puma-palermo", "brand": "푸마", "name": "팔레르모", "code": "396463", "src": "page", "hint": "palermo", "urls": {
        "KR": "https://kr.puma.com/kr/ko/pd/%ED%8C%94%EB%A0%88%EB%A5%B4%EB%AA%A8-%3Cbr%3Epalermo/396463.html",
        "US": "https://us.puma.com/us/en/pd/palermo-sneakers/396463",
        "GB": "https://uk.puma.com/uk/en/pd/palermo-sneakers-unisex/396463",
        "DE": "https://eu.puma.com/de/de/pd/palermo-sneakers-unisex/396463",
        "JP": "https://jp.puma.com/jp/ja/pd/%E3%83%A6%E3%83%8B%E3%82%BB%E3%83%83%E3%82%AF%E3%82%B9-%E3%83%91%E3%83%AC%E3%83%AB%E3%83%A2-%E3%82%B9%E3%83%8B%E3%83%BC%E3%82%AB%E3%83%BC/396463"}},   # 멕시코 몰에는 팔레르모(396463) 없음(시험 10/22)
    {"id": "puma-mostro", "brand": "푸마", "name": "모스트로 OG", "code": "397330", "src": "page", "hint": "mostro", "urls": {
        "KR": "https://kr.puma.com/kr/ko/pd/%EB%AA%A8%EC%8A%A4%ED%8A%B8%EB%A1%9C-og-%3Cbr%3Emostro-og/397330.html",
        "US": "https://us.puma.com/us/en/pd/mostro-og-mens-sneakers/397330",
        "GB": "https://uk.puma.com/uk/en/pd/mostro-og-sneakers-unisex/397330",
        "DE": "https://eu.puma.com/de/de/pd/mostro-og-sneakers-unisex/397330",
        "JP": "https://jp.puma.com/jp/ja/pd/%E3%83%A6%E3%83%8B%E3%82%BB%E3%83%83%E3%82%AF%E3%82%B9-%E3%83%A2%E3%82%B9%E3%83%88%E3%83%AD-og-%E3%82%B9%E3%83%8B%E3%83%BC%E3%82%AB%E3%83%BC/397330",
        "MX": "https://mx.puma.com/mx/es/pd/tenis-mostro-og/397330.html"}},
    {"id": "puma-suede", "brand": "푸마", "name": "스웨이드 클래식", "code": "399781", "src": "page", "hint": "suede", "urls": {
        "KR": "https://kr.puma.com/kr/ko/pd/%EC%8A%A4%EC%9B%A8%EC%9D%B4%EB%93%9C-%ED%81%B4%EB%9E%98%EC%8B%9D%3Cbr%3Esuede-classic/399781.html",
        "US": "https://us.puma.com/us/en/pd/suede-classic-sneakers/399781",
        "GB": "https://uk.puma.com/uk/en/pd/suede-classic-sneakers-unisex/399781",
        "DE": "https://eu.puma.com/de/de/pd/suede-classic-sneakers-unisex/399781",
        "JP": "https://jp.puma.com/jp/ja/pd/%E3%83%A6%E3%83%8B%E3%82%BB%E3%83%83%E3%82%AF%E3%82%B9-%E3%82%B9%E3%82%A6%E3%82%A7%E3%83%BC%E3%83%89-%E3%82%AF%E3%83%A9%E3%82%B7%E3%83%83%E3%82%AF-%E3%82%B9%E3%83%8B%E3%83%BC%E3%82%AB%E3%83%BC/399781",
        "MX": "https://mx.puma.com/mx/es/pd/tenis-suede-classic/399781.html"}},
    {"id": "puma-dne4", "brand": "푸마", "name": "디비에이트 나이트로 엘리트 4(남성)", "code": "312127", "src": "page", "hint": "deviate nitro elite 4", "urls": {
        "KR": "https://kr.puma.com/kr/ko/pd/%EB%94%94%EB%B9%84%EC%97%90%EC%9D%B4%ED%8A%B8-%EB%82%98%EC%9D%B4%ED%8A%B8%EB%A1%9C-%EC%97%98%EB%A6%AC%ED%8A%B8-4-%3Cbr%3Edeviate-nitro-elite-4/312127.html",
        "US": "https://us.puma.com/us/en/pd/deviate-nitro-elite-4-mens-road-running-shoes/312127",
        "GB": "https://uk.puma.com/uk/en/pd/deviate-nitro%E2%84%A2-elite-4-running-shoes-men/312127",
        "DE": "https://eu.puma.com/de/de/pd/deviate-nitro-elite-4-laufschuhe-herren/312127",
        "JP": "https://jp.puma.com/jp/ja/pd/%E3%83%A1%E3%83%B3%E3%82%BA-%E3%83%87%E3%82%A3%E3%83%B4%E3%82%A3%E3%82%A8%E3%82%A4%E3%83%88-%E3%83%8B%E3%83%88%E3%83%AD-%E3%82%A8%E3%83%AA%E3%83%BC%E3%83%88-4-%E3%83%A9%E3%83%B3%E3%83%8B%E3%83%B3%E3%82%B0%E3%82%B7%E3%83%A5%E3%83%BC%E3%82%BA/312127",
        "MX": "https://mx.puma.com/mx/es/pd/tenis-de-running-deviate-nitrotm-elite-4-para-hombre/312127.html"}},   # 인헤일(401560) 대신 — 미국 몰은 전 색상 할인가(73.99달러)뿐이라 뺌(검토 반영 10/22)
    {"id": "on-cloudmonster", "brand": "온러닝", "name": "클라우드몬스터", "code": "61.98434", "src": "page", "hint": "cloudmonster", "urls": {
        cc: f"https://www.on.com/{loc}/products/cloudmonster-61/mens/all-white-shoes-61.98434"
        for cc, loc in (("KR", "ko-kr"), ("US", "en-us"), ("GB", "en-gb"), ("DE", "de-de"), ("JP", "ja-jp"))}},
    {"id": "on-cloud6", "brand": "온러닝", "name": "클라우드 6", "code": "3MF10071200", "src": "page", "hint": "cloud 6", "urls": _on("cloud-6-m-3mf1007/mens/white-white-shoes-3MF10071200")},
    {"id": "on-cloudsurfer2", "brand": "온러닝", "name": "클라우드서퍼 2", "code": "3MF10121043", "src": "page", "hint": "cloudsurfer", "urls": _on("cloudsurfer-2-3mf1012/mens/black-black-shoes-3MF10121043")},
    {"id": "on-cloudtilt", "brand": "온러닝", "name": "클라우드틸트", "code": "3ME10101430", "src": "page", "hint": "cloudtilt", "urls": _on("cloudtilt-m-3me1010/mens/black-ivory-shoes-3ME10101430")},
    {"id": "on-roger", "brand": "온러닝", "name": "더 로저 어드밴티지", "code": "3MF30641200", "src": "page", "hint": "roger", "urls": _on("the-roger-advantage-m-3mf3064/mens/white-white-shoes-3MF30641200")},
    {"id": "on-cloudnova2", "brand": "온러닝", "name": "클라우드노바 2", "code": "3ME30210108", "src": "page", "hint": "cloudnova", "urls": _on("cloudnova-2-3me3021/mens/all-white-shoes-3ME30210108")},
    {"id": "salomon-xt6", "brand": "살로몬", "name": "XT-6 고어텍스", "code": "L47450600", "alt": ["LG9333"], "src": "page", "hint": "xt-6", "urls": {
        "KR": "https://salomon.co.kr/products/l47450600.json",
        "US": "https://www.salomon.com/en-us/product/xt-6-gore-tex-lg9333",
        "GB": "https://www.salomon.com/en-gb/product/xt-6-gore-tex-lg9333",
        "DE": "https://www.salomon.com/de-de/product/xt-6-gore-tex-lg9333"}},
    {"id": "salomon-xt6base", "brand": "살로몬", "name": "XT-6", "code": "L41086600", "alt": ["LG4239"], "src": "page", "hint": "xt-6", "urls": _sal("l41086600", "xt-6-lg4239")},
    {"id": "salomon-xt4og", "brand": "살로몬", "name": "XT-4 OG", "code": "L47132900", "alt": ["LI3335"], "src": "page", "hint": "xt-4", "urls": _sal("l47132900", "xt-4-og-li3335")},
    {"id": "salomon-xt6expanse", "brand": "살로몬", "name": "XT-6 익스팬스", "code": "L41741300", "alt": ["LG9334"], "src": "page", "hint": "xt-6", "urls": _sal("l41741300", "xt-6-expanse-lg9334")},
    {"id": "salomon-xt4oggtx", "brand": "살로몬", "name": "XT-4 OG 고어텍스", "code": "L49210800", "alt": ["LI8806"], "src": "page", "hint": "xt-4", "urls": _sal("l49210800", "xt-4-og-gore-tex-li8806")},
    {"id": "drm-1461", "brand": "닥터마틴", "name": "1461 스무스", "code": "11838002", "src": "page", "hint": "1461", "urls": {
        "KR": "https://www.drmartens.co.kr/products/boots-1461-black-smooth.json",
        "US": f"{DM}/us/en/1461-smooth-leather-oxford-shoes-black/p/11838002",
        "GB": f"{DM}/uk/en_gb/1461-smooth-leather-oxford-shoes-black/p/11838002"}},
    {"id": "drm-jadon", "brand": "닥터마틴", "name": "제이든", "code": "15265001", "src": "page", "hint": "jadon", "urls": {
        "KR": "https://www.drmartens.co.kr/products/boots-jadon-black-15265001.json",
        "US": f"{DM}/us/en/jadon-smooth-leather-platform-boots-black/p/15265001",
        "GB": f"{DM}/uk/en_gb/jadon-smooth-leather-platform-boots-black/p/15265001"}},
    # 닥터마틴 1460 블랙은 한국 몰 품번(10072004)이 해외(11822006)와 달라 넣지 않음(같은 상품인지 확인 안 됨) — 체리레드(11822600)는 같아서 넣음(v1.3)
    # v1.2 — 접속 시험 2026-10-22: 해외 몰 주소는 GitHub 서버에서 확인(나라별 같은 품번)
    {"id": "drm-1460cr", "brand": "닥터마틴", "name": "1460 스무스 체리레드", "code": "11822600", "src": "page", "hint": "1460", "urls": {
        "KR": "https://www.drmartens.co.kr/products/boots-1460-cherry-red-11822600.json",
        "US": f"{DM}/us/en/1460-smooth-leather-lace-up-boots-cherry-red/p/11822600",
        "GB": f"{DM}/uk/en_gb/1460-smooth-leather-lace-up-boots-cherry-red/p/11822600"}},
    {"id": "drm-2976", "brand": "닥터마틴", "name": "2976 첼시", "code": "22227001", "src": "page", "hint": "2976", "urls": {
        "KR": "https://www.drmartens.co.kr/products/boots-2976ys-black-smooth.json",
        "US": f"{DM}/us/en/2976-smooth-leather-chelsea-boots-black/p/22227001",
        "GB": f"{DM}/uk/en_gb/2976-smooth-leather-chelsea-boots-black/p/22227001"}},
    {"id": "drm-1460bex", "brand": "닥터마틴", "name": "1460 벡스", "code": "25345001", "src": "page", "hint": "bex", "urls": {
        "KR": "https://www.drmartens.co.kr/products/boots-1460-bex-black-smooth.json",
        "US": f"{DM}/us/en/1460-bex-smooth-leather-lace-up-boots-black/p/25345001",
        "GB": f"{DM}/uk/en_gb/1460-bex-smooth-leather-lace-up-boots-black/p/25345001"}},
    {"id": "drm-1460mono", "brand": "닥터마틴", "name": "1460 모노", "code": "14353001", "src": "page", "hint": "mono", "urls": {
        "KR": "https://www.drmartens.co.kr/products/1460-mofalse.json",
        "US": f"{DM}/us/en/1460-mono-smooth-leather-lace-up-boots-black/p/14353001",
        "GB": f"{DM}/uk/en_gb/1460-mono-smooth-leather-lace-up-boots-black/p/14353001"}},
    {"id": "dd-santacroce", "brand": "드래곤디퓨전", "name": "산타크로체 빅 백", "code": "8892", "alt": ["W2BAS26025DBR"], "src": "page", "hint": "santa croce", "urls": {
        "KR": "https://www.kolonmall.com/Brands/DRAGON_DIFFUSION/Product/W2BAS26025DBR",   # 코오롱몰(공식 수입) 자체 품번
        "US": "https://dragondiffusion.com/products/santa-croce-big-dark-brown-woven-leather-bag-handmade"}},   # 글로벌 몰 1곳 — 접속한 나라 통화(미국 서버 → 달러), 달러가 아니면 실패
    {"id": "dd-santamaria", "brand": "드래곤디퓨전", "name": "산타마리아 백", "code": "8700", "alt": ["W2BAS26026BKX"], "src": "page", "hint": "santa maria", "urls": {
        "KR": "https://www.kolonmall.com/Brands/DRAGON_DIFFUSION/Product/W2BAS26026BKX",
        "US": "https://dragondiffusion.com/products/santa-maria-black-woven-leather-bag"}},
    {"id": "dd-triplejump", "brand": "드래곤디퓨전", "name": "트리플 점프 스몰 백", "code": "8811", "alt": ["W2BAS26029BKX"], "src": "page", "hint": "triple jump", "urls": {
        "KR": "https://www.kolonmall.com/Brands/DRAGON_DIFFUSION/Product/W2BAS26029BKX",
        "US": "https://dragondiffusion.com/products/triple-jump-small-black-woven-leather-bag-handmade"}},
    {"id": "dd-rosanna", "brand": "드래곤디퓨전", "name": "로잔나 백", "code": "8943", "alt": ["W2BAS26024BKX"], "src": "page", "hint": "rosanna", "urls": {
        "KR": "https://www.kolonmall.com/Brands/DRAGON_DIFFUSION/Product/W2BAS26024BKX",
        "US": "https://dragondiffusion.com/products/rosanna-black-woven-leather-bag-handmade"}},
    {"id": "dd-ars", "brand": "드래곤디퓨전", "name": "아르스 토트백", "code": "8848", "alt": ["W2BAS26027DBR"], "src": "page", "hint": "ars", "urls": {
        "KR": "https://www.kolonmall.com/Brands/DRAGON_DIFFUSION/Product/W2BAS26027DBR",
        "US": "https://dragondiffusion.com/products/ars-tote-dark-brown-woven-leather-bag"}},
    {"id": "hunter-origtall", "brand": "헌터", "name": "오리지널 톨(여성·무광)", "code": "WFT1000RMA", "src": "page", "hint": "wft1000rmablk", "urls": {
        "KR": "https://www.kolonmall.com/Brands/HUNTER/Product/K1760508652696038BK01",   # 코오롱몰 — 품번은 상품 이름 끝(WFT1000RMABLK)에만
        "US": "https://hunterboots.com/products/womens-original-tall-rain-boots-in-black-wft1000rma-hbl01.json",
        "GB": "https://hunterboots.co.uk/products/womens-original-tall-wellington-boots-wft1000rma-blk.json",
        "JP": "https://hunterboots.co.jp/products/wft1000rma-blk.json"}},
    {"id": "hunter-origshort", "brand": "헌터", "name": "오리지널 숏(여성·무광)", "code": "WFS1000RMA", "src": "page", "hint": "wfs1000rmablk", "urls": {
        "KR": "https://www.kolonmall.com/Brands/HUNTER/Product/K1760507742896066BK01",
        "US": "https://hunterboots.com/products/womens-original-short-rain-boots-in-black-wfs1000rma-hbl01.json",
        "GB": "https://hunterboots.co.uk/products/womens-original-short-boot-wfs1000rma-blk.json",
        "JP": "https://hunterboots.co.jp/products/wfs1000rma-blk.json"}},
    {"id": "hunter-playtall", "brand": "헌터", "name": "플레이 톨(여성)", "code": "WFT2007RMA", "src": "page", "hint": "wft2007rmablk", "urls": {
        "KR": "https://www.kolonmall.com/Brands/HUNTER/Product/K1760508641433091BK01",
        "US": "https://hunterboots.com/products/womens-play-tall-rain-boots-in-black-wft2007rma-hbl01.json",
        "GB": "https://hunterboots.co.uk/products/womens-play-tall-wellington-boots-wft2007rma-blk.json",
        "JP": "https://hunterboots.co.jp/products/wft2007rma-blk.json"}},
    {"id": "hunter-chelsea", "brand": "헌터", "name": "오리지널 첼시(여성)", "code": "WFS2078RMA", "src": "page", "hint": "wfs2078rmablk", "urls": {
        "KR": "https://www.kolonmall.com/Brands/HUNTER/Product/K1760510634046010NO01",
        "US": "https://hunterboots.com/products/womens-original-chelsea-boots-in-black-wfs2078rma-hbl01.json",
        "GB": "https://hunterboots.co.uk/products/womens-original-chelsea-boots-wfs2078rma-blk.json"}},   # 일본 몰에서 같은 품번(WFS2078RMA)을 못 찾음(시험 10/22)
    {"id": "hunter-playshort", "brand": "헌터", "name": "플레이 숏(여성)", "code": "WFS2020RMA", "src": "page", "hint": "wfs2020rmablk", "urls": {
        "KR": "https://www.kolonmall.com/Brands/HUNTER/Product/K1760066476268098BK01",
        "US": "https://hunterboots.com/products/womens-play-short-rain-boots-in-black-wfs2020rma-hbl01.json",
        "GB": "https://hunterboots.co.uk/products/womens-play-short-wellington-boots-wfs2020rma-blk.json"}},   # 일본 몰에는 없음(404, 10/22)
    {"id": "ua-tech2", "brand": "언더아머", "name": "UA 테크 2.0 반팔", "code": "1326413", "src": "page", "hint": "ua tech", "urls": {
        "KR": "https://www.underarmour.co.kr/ko-kr/p/%EC%83%81%EC%9D%98/ua_tech_2.0/1326413.html",
        "US": "https://www.underarmour.com/en-us/p/ua_tech_2.0_mens_short_sleeve/1326413.html",
        "GB": "https://www.underarmour.co.uk/en-gb/p/ua-tech-2.0-mens-short-sleeve/1326413.html",
        "DE": "https://www.underarmour.de/de-de/p/ua-tech-2.0/1326413.html",
        "MX": "https://www.underarmour.com.mx/es-mx/p/tops/ua_tech_2.0/1326413.html"}},   # 일본은 수입사(DOME) 품번·사양이 달라 뺌
    {"id": "ua-hg-ss", "brand": "언더아머", "name": "히트기어 컴프레션 반팔", "code": "1361518", "src": "page", "hint": "heatgear", "urls": {
        "KR": "https://www.underarmour.co.kr/ko-kr/p/%EC%83%81%EC%9D%98/heatgear/1361518.html",
        "US": "https://www.underarmour.com/en-us/p/heatgear_mens_compression_short_sleeve/1361518.html",
        "GB": "https://www.underarmour.co.uk/en-gb/p/heatgear-mens/1361518.html",
        "DE": "https://www.underarmour.de/de-de/p/heatgear/1361518.html",
        "MX": "https://www.underarmour.com.mx/es-mx/p/tops/heatgear/1361518.html"}},
    {"id": "ua-hg-ls", "brand": "언더아머", "name": "히트기어 컴프레션 긴팔", "code": "1361524", "src": "page", "hint": "heatgear", "urls": {
        "KR": "https://www.underarmour.co.kr/ko-kr/p/%EC%83%81%EC%9D%98/heatgear/1361524.html",
        "US": "https://www.underarmour.com/en-us/p/heatgear_mens_compression_long_sleeve/1361524.html",
        "GB": "https://www.underarmour.co.uk/en-gb/p/heatgear-mens-compression-long-sleeve/1361524.html",
        "DE": "https://www.underarmour.de/de-de/p/heatgear/1361524.html",
        "MX": "https://www.underarmour.com.mx/es-mx/p/house_of_baselayer/heatgear/1361524.html"}},
    {"id": "ua-tech-hz", "brand": "언더아머", "name": "UA 테크 ½ 집", "code": "1328495", "src": "page", "hint": "ua tech", "urls": {
        "KR": "https://www.underarmour.co.kr/ko-kr/p/%EC%83%81%EC%9D%98/ua_tech/1328495.html",
        "US": "https://www.underarmour.com/en-us/p/ua_tech_mens_1-2_zip_long_sleeve/1328495.html",
        "GB": "https://www.underarmour.co.uk/en-gb/p/ua-tech-mens-1-2-zip-long-sleeve/1328495.html",
        "DE": "https://www.underarmour.de/de-de/p/ua-tech/1328495.html"}},   # 멕시코 몰은 정가 없이 할인가(539.4페소)만 보여 뺌(시험 10/22)
    {"id": "ua-leftchest", "brand": "언더아머", "name": "레프트 체스트 로고 반팔", "code": "1326799", "src": "page", "hint": "left chest", "urls": {
        "KR": "https://www.underarmour.co.kr/ko-kr/p/%EC%83%81%EC%9D%98/ua_%EB%A0%88%ED%94%84%ED%8A%B8_%EC%B2%B4%EC%8A%A4%ED%8A%B8_%EB%A1%9C%EA%B3%A0/1326799.html",
        "US": "https://www.underarmour.com/en-us/p/ua_left_chest_logo_mens_short_sleeve/1326799.html",
        "GB": "https://www.underarmour.co.uk/en-gb/p/ua-left-chest-logo-mens-short-sleeve/1326799.html",
        "DE": "https://www.underarmour.de/de-de/p/ua-left-chest-logo/1326799.html",
        "MX": "https://www.underarmour.com.mx/es-mx/p/tops/ua_left_chest_logo/1326799.html"}},
    {"id": "saucony-ride19", "brand": "써코니", "name": "라이드 19(남성)", "code": "S21055", "src": "page", "hint": "라이드 19", "code_in_page": True, "urls": {
        "KR": "https://saucony.co.kr/product/%EB%82%A8%EC%84%B1-%EB%9D%BC%EC%9D%B4%EB%93%9C-19-whitecrimson/210/",   # 품번은 상품 정보 칸 '모델 S21055-172'
        "US": "https://www.saucony.com/en/ride-19/60823M.html",
        "GB": "https://www.saucony.com/UK/en_GB/ride-19/60823M.html",
        "DE": "https://www.saucony.com/DE/de_DE/ride-19/60823M.html"}},   # 해마다 새 모델(라이드 20 등)이 나오면 품번·주소를 바꿈
    {"id": "saucony-endspeed5", "brand": "써코니", "name": "엔돌핀 스피드 5(남성)", "code": "S21007", "src": "page", "hint": "엔돌핀 스피드 5", "code_in_page": True, "urls": {
        "KR": "https://saucony.co.kr/product/%EB%82%A8%EC%84%B1-%EC%97%94%EB%8F%8C%ED%95%80-%EC%8A%A4%ED%94%BC%EB%93%9C-5-whitegum/164/",
        "US": "https://www.saucony.com/en/endorphin-speed-5/60307M.html",
        "GB": "https://www.saucony.com/UK/en_GB/endorphin-speed-5/60307M.html",
        "DE": "https://www.saucony.com/DE/de_DE/endorphin-speed-5/60307M.html"}},
    {"id": "saucony-endpro5", "brand": "써코니", "name": "엔돌핀 프로 5(남성)", "code": "S21064", "src": "page", "hint": "엔돌핀 프로 5", "code_in_page": True, "urls": {
        "KR": "https://saucony.co.kr/product/%EB%82%A8%EC%84%B1-%EC%97%94%EB%8F%8C%ED%95%80-%ED%94%84%EB%A1%9C-5-whiteblack/302/",
        "US": "https://www.saucony.com/en/endorphin-pro-5/60803M.html",
        "GB": "https://www.saucony.com/UK/en_GB/endorphin-pro-5/60803M.html",
        "DE": "https://www.saucony.com/DE/de_DE/endorphin-pro-5/60803M.html"}},
    {"id": "saucony-triumph24", "brand": "써코니", "name": "트라이엄프 24(남성)", "code": "S100997", "src": "page", "hint": "트라이엄프 24", "code_in_page": True, "urls": {
        "KR": "https://saucony.co.kr/product/%EB%82%A8%EC%84%B1-%ED%8A%B8%EB%9D%BC%EC%9D%B4%EC%97%84%ED%94%84-24-triple-black/418/",
        "US": "https://www.saucony.com/en/triumph-24/61229M.html",
        "GB": "https://www.saucony.com/UK/en_GB/triumph-24/61229M.html",
        "DE": "https://www.saucony.com/DE/de_DE/triumph-24/61229M.html"}},
    {"id": "saucony-guide19", "brand": "써코니", "name": "가이드 19(남성)", "code": "S21058", "src": "page", "hint": "가이드 19", "code_in_page": True, "urls": {
        "KR": "https://saucony.co.kr/product/%EB%82%A8%EC%84%B1-%EA%B0%80%EC%9D%B4%EB%93%9C-19-triple-black/373/",
        "US": "https://www.saucony.com/en/guide-19/60838M.html",
        "GB": "https://www.saucony.com/UK/en_GB/guide-19/60838M.html",
        "DE": "https://www.saucony.com/DE/de_DE/guide-19/60838M.html"}},
    {"id": "saucony-hurricane26", "brand": "써코니", "name": "허리케인 26(남성)", "code": "S101098", "src": "page", "hint": "허리케인 26", "code_in_page": True, "urls": {
        "KR": "https://saucony.co.kr/product/%EB%82%A8%EC%84%B1-%ED%97%88%EB%A6%AC%EC%BC%80%EC%9D%B8-26-triple-black/535/",
        "US": "https://www.saucony.com/en/hurricane-26/61249M.html",
        "GB": "https://www.saucony.com/UK/en_GB/hurricane-26/61249M.html",
        "DE": "https://www.saucony.com/DE/de_DE/hurricane-26/61249M.html"}},
    {"id": "saucony-kinvara16", "brand": "써코니", "name": "킨바라 16(남성)", "code": "S21020", "src": "page", "hint": "킨바라 16", "code_in_page": True, "urls": {
        "KR": "https://saucony.co.kr/product/%EB%82%A8%EC%84%B1-%ED%82%A8%EB%B0%94%EB%9D%BC-16-blackwhite/153/",
        "US": "https://www.saucony.com/en/kinvara-16/60309M.html"}},   # 영국·독일 몰 같은 주소는 다른 색상 품번(S101468)만 있어 뺌(시험 10/22)
    {"id": "brooks-ghost18", "brand": "브룩스", "name": "고스트 18(남성)", "code": "1104931D", "cc_code": {"JP": "BRM4933"}, "src": "page", "hint": "고스트 18", "code_in_page": True, "urls": {
        "KR": "https://brooksrunning.co.kr/product/%EB%82%A8%EC%84%B1-%EA%B3%A0%EC%8A%A4%ED%8A%B8-18-%EB%B8%94%EB%9E%99-medium/852/",   # 품번은 prd_model 칸(1104931D020)
        "JP": "https://brooksrunning.co.jp/products/brm4933-b-b.json"}},   # 일본 수입사 품번 BRM4933 = 고스트 18 남성 보통 폭 · 미국·유럽 몰은 403(넣지 않음)
    {"id": "brooks-ghost18w", "brand": "브룩스", "name": "고스트 18(여성)", "code": "1204821B", "cc_code": {"JP": "BRW4822"}, "src": "page", "hint": "고스트 18", "code_in_page": True, "urls": {
        "KR": "https://brooksrunning.co.kr/product/%EC%97%AC%EC%84%B1-%EA%B3%A0%EC%8A%A4%ED%8A%B8-18-%ED%99%94%EC%9D%B4%ED%8A%B8-medium/864/",
        "JP": "https://brooksrunning.co.jp/products/brw4822-blk.json"}},
    {"id": "brooks-glycgts23", "brand": "브룩스", "name": "글리세린 GTS 23(남성)", "code": "1105031D", "cc_code": {"JP": "BRM5033"}, "src": "page", "hint": "글리세린 gts 23", "code_in_page": True, "urls": {
        "KR": "https://brooksrunning.co.kr/product/%EB%82%A8%EC%84%B1-%EA%B8%80%EB%A6%AC%EC%84%B8%EB%A6%B0-gts-23%ED%8E%84-medium/799/",
        "JP": "https://brooksrunning.co.jp/products/brm5033-blk-w.json"}},
    {"id": "brooks-glycmax2", "brand": "브룩스", "name": "글리세린 맥스 2(남성)", "code": "1104791D", "cc_code": {"JP": "BRM4793"}, "src": "page", "hint": "글리세린 맥스 2", "code_in_page": True, "urls": {
        "KR": "https://brooksrunning.co.kr/product/%EB%82%A8%EC%84%B1-%EA%B8%80%EB%A6%AC%EC%84%B8%EB%A6%B0-%EB%A7%A5%EC%8A%A4-2%ED%8C%AC%ED%85%80-medium/697/",
        "JP": "https://brooksrunning.co.jp/products/brm4793-b-b.json"}},
    {"id": "brooks-ghostamp", "brand": "브룩스", "name": "고스트 AMP(남성)", "code": "1104971D", "cc_code": {"JP": "BRM4973"}, "src": "page", "hint": "고스트 amp", "code_in_page": True, "urls": {
        "KR": "https://brooksrunning.co.kr/product/%EB%82%A8%EC%84%B1-%EA%B3%A0%EC%8A%A4%ED%8A%B8-amp%ED%94%84%EB%9D%BC%EC%9D%B4%EB%A8%B8medium/947/",
        "JP": "https://brooksrunning.co.jp/products/brm4973-blu.json"}},
    # v1.4 아크테릭스 — 한국은 시즌 상품 페이지마다 한국 품번(cc_code KR, 페이지 Model(KR))이 따로 · JSON-LD 판매가 + 화면 데이터 정가(retail_price)
    {"id": "arc-atomhoody", "brand": "아크테릭스", "name": "아톰 후디(남성)", "code": "X000009556", "cc_code": {"KR": "AJQSM09556"}, "src": "page", "hint": "atom hoody",
     "urls": _arc("686241", "atom-hoody-9556", "atom-hoody-m")},
    {"id": "arc-atomjacket", "brand": "아크테릭스", "name": "아톰 재킷(남성)", "code": "X000009561", "cc_code": {"KR": "AJPFM09561"}, "src": "page", "hint": "atom jacket",
     "urls": _arc("685690", "atom-jacket-9561", "atom-jacket-m")},   # 한국은 2025 가을·겨울 페이지(2026 페이지 없음 · 10/23)
    {"id": "arc-gammapant", "brand": "아크테릭스", "name": "감마 팬츠(남성)", "code": "X000010481", "cc_code": {"KR": "APQSM10481"}, "src": "page", "hint": "gamma pant",
     "urls": _arc("686323", "gamma-pant-0481", "gamma-pant-m")},
    {"id": "arc-squamish", "brand": "아크테릭스", "name": "스쿼미시 후디(남성)", "code": "X000010276", "cc_code": {"KR": "AJQSM10276"}, "src": "page", "hint": "squamish hoody",
     "urls": _arc("686259", "squamish-hoody-0276", "squamish-hoody-m")},
    {"id": "arc-cerium", "brand": "아크테릭스", "name": "세륨 후디(남성)", "code": "X000010521", "cc_code": {"KR": "AJQFM10521"}, "src": "page", "hint": "cerium hoody",
     "urls": _arc("686764", "cerium-hoody-0521", "cerium-hoody-m")},
    {"id": "arc-mantis26", "brand": "아크테릭스", "name": "맨티스 26 백팩", "code": "X000010643", "cc_code": {"KR": "ABQSU10643"}, "src": "page", "hint": "mantis 26",
     "urls": _arc("686432", "mantis-26-backpack-0643", g="")},   # 일본 몰 mantis-26-backpack은 옛 모델(X000009825)이라 뺌 · 맨티스 2 웨이스트 팩은 한국 페이지에 가격 데이터가 없어 넣지 않음(10/23)
    # v1.4 킨 — 품번 = 색상까지 정해진 7자리 · 한국 고도몰은 상품 정보 칸 ARTICLE, 미국·독일·일본 쇼피파이는 변형 품번이 바코드라 상품 태그, 영국은 변형 품번(1022258-10)
    {"id": "keen-newporth2", "brand": "킨(KEEN)", "name": "뉴포트 H2(남성 · 트리플 블랙)", "code": "1022258", "src": "page", "hint": "newport h2",
     "urls": _keen("1000000673", "mens-newport-h2-triple-black")},
    {"id": "keen-newporth2b", "brand": "킨(KEEN)", "name": "뉴포트 H2(남성 · 블랙)", "code": "1001907", "src": "page", "hint": "newport h2",
     "urls": _keen("1000000679", "mens-newport-h2-black")},
    {"id": "keen-uneek", "brand": "킨(KEEN)", "name": "유니크(남성 · 블랙)", "code": "1014097", "src": "page", "hint": "uneek",
     "urls": _keen("1000000653", "mens-uneek-monochrome-black-black", gb="mens-uneek-black-black")},
    {"id": "keen-jasper3", "brand": "킨(KEEN)", "name": "재스퍼 III(남성 · 블랙)", "code": "1032681", "src": "page", "hint": "jasper iii",
     "urls": _keen("1000000996", "mens-jasper-iii-black-black")},
    {"id": "keen-targhee4", "brand": "킨(KEEN)", "name": "타기 IV 워터프루프(남성 · 트리플 블랙)", "code": "1029827", "src": "page", "hint": "targhee iv",
     "urls": _keen("1000000580", "mens-targhee-iv-waterproof-triple-black")},
    {"id": "keen-jasper", "brand": "킨(KEEN)", "name": "재스퍼(남성 · 블랙)", "code": "1026592", "src": "page", "hint": "jasper",
     "urls": _keen("1000000804", "mens-jasper-hairy-black-black", jp=False)},   # 일본 몰에 없음(10/23)
    # v1.4 우포스 — 품번 = 모델 4자리 + 색상(한국 Article No. '1100 Black' · 미국 변형 품번 앞머리 '1100BLK…') · 한국 콜라보 상품(같은 Article No.)은 다른 상품 번호
    {"id": "oofos-ooriginal", "brand": "우포스", "name": "OOriginal 샌들(블랙)", "code": "1000", "cc_code": {"KR": "1000 Black", "US": "1000BLK"}, "src": "page", "hint": "ooriginal",
     "urls": _oofos("1000000050", "mens-original-sandal-black")},
    {"id": "oofos-ooahh", "brand": "우포스", "name": "OOahh 슬라이드(블랙)", "code": "1100", "cc_code": {"KR": "1100 Black", "US": "1100BLK"}, "src": "page", "hint": "ooahh",
     "urls": _oofos("1000000084", "mens-sandal-ooahh-slide-black")},
    {"id": "oofos-oocloog", "brand": "우포스", "name": "OOcloog 클로그(블랙)", "code": "1200", "cc_code": {"KR": "1200 Black", "US": "1200BLK"}, "src": "page", "hint": "oocloog",
     "urls": _oofos("1000000159", "mens-oocloog-clog-black")},
    {"id": "oofos-ooriginalplus", "brand": "우포스", "name": "OOriginal+ 샌들(블랙)", "code": "2000", "cc_code": {"KR": "2000 Black", "US": "2000BLACK"}, "src": "page", "hint": "ooriginal",
     "urls": _oofos("1000000062", "mens-ooriginal-plus-sandal-black")},
    {"id": "oofos-ooahhplus", "brand": "우포스", "name": "OOahh+ 슬라이드(블랙)", "code": "2200", "cc_code": {"KR": "2200 Black", "US": "2200BLACK"}, "src": "page", "hint": "ooahh",
     "urls": _oofos("1000000058", "mens-ooahh-plus-slide-sandal-black")},
    {"id": "oofos-ooriginalsport", "brand": "우포스", "name": "OOriginal Sport 샌들(그라파이트)", "code": "1001", "cc_code": {"KR": "1001 Graphite", "US": "1001GRPH"}, "src": "page", "hint": "ooriginal sport",
     "urls": _oofos("1000000087", "mens-sandal-ooriginal-sport-graphite")},
    {"id": "oofos-sportflex", "brand": "우포스", "name": "OOahh Sport Flex 슬라이드(매트 블랙)", "code": "1550", "cc_code": {"KR": "1550 Black Matte", "US": "1550MATBLK"}, "src": "page", "hint": "sport flex",
     "urls": _oofos("1000000031", "mens-ooahh-sport-flex-black-matte")},
]


def log(msg):
    print(msg, flush=True)


def soft_fail(msg):
    """심각한 실패 표시 — 저장은 하되 워크플로우 마지막 단계가 빨간 X로 끝내 점검 알림이 가게 함"""
    print(f"실패 표시: {msg}", flush=True)
    with open("soft_fail.txt", "a", encoding="utf-8") as f:
        f.write(f"{SCRIPT}: {msg}\n")


class Skip(Exception):
    """이 나라에서는 팔지 않음·주소 없음(실패로 세지 않음)"""


_ROB, _LAST, _BLOCKED, _HLAST, _DOWN = {}, [0.0], set(), {}, {}
# robots.txt를 두지 않는 API 주소 → 같은 회사 대표 사이트 robots.txt를 따름(그 사이트 robots.txt도 못 받으면 건너뜀)
# api.nike.com: 상품 정보 경로 밖 모든 주소(/, robots.txt, 없는 주소)에 Akamai가 '503 DNS failure' — 2026-10-21 브랜치 시험에서 확인
ROBOTS_ALT = {"api.nike.com": "https://www.nike.com"}


def _robots_rules(txt):
    """robots.txt → 우리에게 맞는 규칙 [(허용?, 정규식, 길이)] — RFC 9309: 우리 이름 그룹이 있으면 그것만, 없으면 *"""
    groups, g, rule_seen = [], None, True
    for line in txt.splitlines():
        line = line.split("#", 1)[0].strip()
        if ":" not in line: continue
        k, v = (x.strip() for x in line.split(":", 1)); k = k.lower()
        if k == "user-agent":
            if rule_seen: g = {"ua": set(), "rules": []}; groups.append(g); rule_seen = False
            g["ua"].add(v.lower())
        elif k in ("allow", "disallow") and g is not None:
            rule_seen = True
            if v:   # %2A·%24는 글자 그대로(와일드카드·끝 표시가 아님)
                lit = re.sub(r"%2[aA]", "\x00", re.sub(r"%24", "\x01", v))
                rx = re.escape(urllib.parse.unquote(lit)).replace(r"\*", ".*")
                if rx.endswith(r"\$"): rx = rx[:-2] + "$"
                rx = rx.replace("\x00", r"\*").replace("\x01", r"\$")
                g["rules"].append((k == "allow", re.compile(rx), len(v)))
    mine = [gg for gg in groups if BOT in gg["ua"]] or [gg for gg in groups if "*" in gg["ua"]]
    return [r for gg in mine for r in gg["rules"]]


def _robots_get(base):
    """규칙 목록, 또는 못 받은 이유(글) — 4xx면 규칙 없음, 429·5xx·연결 안 됨이면 이유(RFC 9309: 그 사이트 전체를 막힌 것으로)"""
    try:
        r = requests.get(base + "/robots.txt", headers=HDR, timeout=20)
        if r.status_code == 429 or r.status_code >= 500:
            return f"robots.txt HTTP {r.status_code}"
        if r.status_code != 200:
            return []
        raw = getattr(r, "content", None)
        return _robots_rules(raw.decode("utf-8", "replace") if isinstance(raw, bytes) else r.text)   # 글자 집합 표시가 없어도 UTF-8
    except requests.RequestException as e:
        return f"robots.txt 못 받음({type(e).__name__})"


def robots_ok(url):
    """(허용?, 이유) — 사이트별 robots.txt는 실행마다 1번만 받음"""
    p = urllib.parse.urlsplit(url); base = f"{p.scheme}://{p.netloc}"
    if base not in _ROB:
        _ROB[base] = _robots_get(base)
        alt = ROBOTS_ALT.get(p.netloc)
        if isinstance(_ROB[base], str) and alt:
            got = _robots_get(alt)
            if not isinstance(got, str):
                log(f"  {p.netloc}: {_ROB[base]} — robots.txt를 두지 않는 API 주소라 {urllib.parse.urlsplit(alt).netloc} robots.txt를 따름")
                _ROB[base] = got
    rules = _ROB[base]
    if isinstance(rules, str):
        return False, f"{rules} — 이 사이트 건너뜀"
    path = urllib.parse.unquote(p.path or "/") + ("?" + urllib.parse.unquote(p.query) if p.query else "")
    hit = [(n, a) for a, rx, n in rules if rx.match(path)]
    return (True, "") if not hit or max(hit)[1] else (False, "robots.txt가 막음")


_S = requests.Session()   # 넘겨짐 사이 쿠키를 이어 주려고(예전 allow_redirects=True와 같게)


def get(url, hops=5):
    """주소 → 응답. 넘겨짐(3xx)은 직접 따라가며 매번 막힘·robots.txt를 먼저 확인(막힌 주소는 요청하지 않음)"""
    moved = False
    for _ in range(hops + 1):
        host = urllib.parse.urlsplit(url).netloc
        pre = "넘겨진 주소: " if moved else ""
        if host in _BLOCKED:
            raise RuntimeError(pre + "이번 실행에서 이 사이트가 막음 — 더 요청 안 함")
        if _DOWN.get(host, 0) >= 2:
            raise RuntimeError(pre + "이번 실행에서 이 사이트가 연달아 응답 없음 — 더 요청 안 함")
        ok, why = robots_ok(url)
        if not ok:
            raise RuntimeError(pre + why)
        w = max(GAP - (time.time() - _LAST[0]), HOST_GAP.get(host, 0) - (time.time() - _HLAST.get(host, 0.0)))
        if w > 0: time.sleep(w)
        _LAST[0] = _HLAST[host] = time.time()
        try:
            r = _S.get(url, headers=HDR, timeout=25, allow_redirects=False)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            _DOWN[host] = _DOWN.get(host, 0) + 1   # v1.3 같은 사이트가 연달아 2번 응답 없으면 이번 실행에서 건너뜀(한 사이트가 시간 제한을 다 쓰지 않게)
            raise
        _DOWN.pop(host, None)
        loc = (getattr(r, "headers", None) or {}).get("Location") if 300 <= r.status_code < 400 else None
        if loc:
            try:
                loc = loc.encode("latin1").decode("utf-8")   # requests와 같게 UTF-8 주소 되살림
            except (UnicodeEncodeError, UnicodeDecodeError):
                pass
            url, moved = urllib.parse.urljoin(url, loc), True
            continue
        if r.status_code in (403, 429):
            _BLOCKED.add(host)   # 실제로 막은 사이트
            raise RuntimeError(pre + f"HTTP {r.status_code}(접속 차단 — 우회하지 않음)")
        if r.status_code >= 400:
            raise RuntimeError(pre + f"HTTP {r.status_code}")
        return r
    raise RuntimeError(f"넘겨짐이 {hops}번 넘음")


def _json(r):
    d = r.json()
    if not isinstance(d, dict):
        raise RuntimeError("응답 형식이 다름")
    return d


def num(v):
    try:
        x = float(str(v).replace(",", ""))
        return x if x > 0 else None
    except (TypeError, ValueError):
        return None


def _money(s):
    """화면 글자 가격 → 숫자: '$1,234.56' · '1.234,56 €' · '190,00' · '1.234 €'(독일식 천 단위) — '&#8364;'(€) 같은 HTML 기호는 먼저 풂(숫자가 섞이지 않게)"""
    t = re.sub(r"[^0-9.,]", "", unescape(str(s)))
    if re.fullmatch(r"\d{1,3}(\.\d{3})*,\d{1,2}", t):
        t = t.replace(".", "").replace(",", ".")
    elif re.fullmatch(r"\d{1,3}(\.\d{3})+", t):
        t = t.replace(".", "")
    return num(t)


def _micro(html, cur, codes):
    """schema.org 마이크로데이터(itemprop) 가격 — JSON-LD가 없는 SFCC형 몰(써코니 해외). 이 상품 품번(data-stock-number)이 있을 때만.
    판매가 = itemprop price(같이 있는 priceincents ÷ 100 우선 — 190,00 같은 독일식 표기 오해 방지), 정가 = 판매가 바로 뒤 '원래 가격'(price-standard)"""
    stock = " ".join(re.findall(r'data-stock-number="([^"]+)"', html)).lower()
    if not codes or not any(c in stock for c in codes):
        return [], [], False
    offers, end = [], 0
    for m in re.finditer(r'itemprop="priceCurrency"[^>]*>\s*([A-Z]{3})\s*<.{0,300}?itemprop="price"[^>]*>\s*([0-9][0-9.,]*)\s*<'
                         r'(?:(?:(?!itemprop="priceCurrency").){0,200}?itemprop="priceincents"[^>]*>\s*([0-9]+)\s*<)?', html, re.S):   # 다음 가격 칸의 priceincents를 가져오지 않게
        c, p, cents = m.groups()
        v = (int(cents) / 100 if cents else None) or _money(p)
        if c == cur and v:
            offers.append(v); end = m.end()
    lists = []
    for m in re.finditer(r'class="price-sales[^"]*"[^>]*>\s*([^<]*?)\s*<(?:(?!class="price-sales).){0,300}?class="price-standard[^"]*"[^>]*>\s*([^<]*?)\s*<',
                         html[:end], re.S):   # 이 상품 가격 칸(마이크로데이터) 앞만 · 바로 다음 판매가 칸 전까지 — 추천 상품 칸의 원래 가격과 짝짓지 않게
        sv, lv = _money(m.group(1)), _money(m.group(2))
        if sv and lv and sv <= lv <= sv * 3 and any(abs(sv - o) < 0.01 for o in offers):
            lists.append(lv)
    return offers, lists, True


def nike_price(code, cc):
    m, l, cur = MK[cc]
    d = _json(get(NIKE_FEED.format(m=m, l=l, s=code)))
    objs = [o for o in d.get("objects") or [] if isinstance(o, dict)]
    if not objs:
        raise Skip("이 나라 나이키에서 팔지 않음")
    for o in objs:
        for pi in o.get("productInfo") or []:
            mp, mer = pi.get("merchPrice") or {}, pi.get("merchProduct") or {}
            if mer.get("styleColor") != code:
                continue
            fp = num(mp.get("fullPrice"))
            if fp and mp.get("currency") == cur:
                return fp, {"cur_price": num(mp.get("currentPrice"))}
    raise RuntimeError("정가(fullPrice) 없음")


REL = {"isSimilarTo", "isRelatedTo", "isAccessoryOrSparePartFor", "isConsumableFor", "itemListElement"}   # 관련·추천 상품 칸


def _ld_nodes(html, skip=()):
    out = []
    for m in re.finditer(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', html, re.S | re.I):
        try:
            d = json.loads(m.group(1).strip())
        except ValueError:
            continue
        st = [d]
        while st:
            x = st.pop()
            if isinstance(x, list):
                st.extend(x)
            elif isinstance(x, dict):
                out.append(x)
                st.extend(v for k, v in x.items() if isinstance(v, (dict, list)) and k not in skip)
    return out


def _types(n):
    t = n.get("@type")
    return {str(x).lower() for x in (t if isinstance(t, list) else [t])}


def page_price(html, hint, cur, codes=()):
    """상품 페이지 → 정가. 글로벌 품번(codes)이 품번·주소에 있는 JSON-LD 상품만 보고, 그런 상품이 없을 때만 이름에 모델명(hint)이
    낱말로 있는 상품을 봄(추천·관련 상품 섞임 방지)"""
    offers, lists = [], []
    codes = [c.lower() for c in codes if c]
    nodes = [n for n in _ld_nodes(html) if _types(n) & {"product", "productgroup"}]
    word = re.compile(rf"(?<![\w-]){re.escape(hint)}(?![\w-])")
    by_code = [n for n in nodes if any(c in " ".join(str(n.get(k, "")) for k in ("sku", "productID", "productGroupID", "mpn", "url", "@id")).lower() for c in codes)]
    prods = by_code
    if not by_code:   # 품번이 없으면 이름으로 — 관련·추천 상품 칸은 빼고, 이름이 다른 상품이 여럿이면 실패(틀린 값을 저장하지 않게)
        prods = [n for n in _ld_nodes(html, REL) if _types(n) & {"product", "productgroup"} and word.search(str(n.get("name", "")).lower())]
        names = {str(n.get("name", "")).strip().lower() for n in _ld_nodes(html, REL | {"hasVariant"})
                 if _types(n) & {"product", "productgroup"} and word.search(str(n.get("name", "")).lower())}
        if len(names) > 1:
            raise RuntimeError(f"품번이 없고 이름이 비슷한 상품이 여럿({' / '.join(sorted(names))[:60]})")
    for p in prods:
        st = [p.get("offers"), p.get("hasVariant")]
        while st:
            x = st.pop()
            if isinstance(x, list): st.extend(x); continue
            if not isinstance(x, dict): continue
            if _types(x) & {"product"}: st.append(x.get("offers")); continue
            if str(x.get("priceCurrency", cur)) == cur:
                v = num(x.get("price") or x.get("highPrice") or x.get("lowPrice"))
                if v: offers.append(v)
            for ps in (x.get("priceSpecification") if isinstance(x.get("priceSpecification"), list) else [x.get("priceSpecification")]):
                if isinstance(ps, dict) and re.search(r"ListPrice|StrikethroughPrice", str(ps.get("priceType", ""))) and str(ps.get("priceCurrency", cur)) == cur:
                    v = num(ps.get("price"))
                    if v: lists.append(v)
            if x.get("offers"): st.append(x.get("offers"))
    flat = html.replace('\\"', '"')
    # SFCC형 몰(푸마 멕시코): 화면 데이터의 c_listPrice(정가)·c_salePrice(판매가) — 판매가가 이 상품 가격과 같을 때만(추천 상품 섞임 방지)
    for m in re.finditer(r'"c_listPrice":([0-9.]+),"c_salePrice":([0-9.]+)', flat):
        lp, sp = num(m.group(1)), num(m.group(2))
        if lp and sp and sp <= lp <= sp * 3 and any(abs(sp - o) < 0.01 for o in offers):
            lists.append(lp)
    # SFCC형 몰(푸마 한국 등): 가격인하 중이면 JSON-LD에는 판매가만 — 이 상품 가격 칸의 취소선 정가(strike-through list)를 정가로.
    # 이 상품 것만: 취소선 바로 곁 판매가 칸(sales — 푸마 한국은 취소선 바로 앞, SFCC 기본은 바로 뒤)의 값이 이 상품 판매가(JSON-LD)와 같을 때만
    # (추천 상품 칸의 할인 가격을 가져오지 않게) · 그런 정가가 한 가지일 때만 · 판매가보다 높고 5배 안(70% 할인까지 — 푸마 한국 팔레르모 10/22 119,000 → 35,700원)
    lps = set()
    for m in re.finditer(r'class="strike-through list"[^>]*>\s*(?:<(?!span class="value")[^>]+>\s*)*<span class="value"[^>]*>\s*([^<]+?)\s*</span>', html):
        back = html[max(0, m.start() - 600):m.start()]; k = back.rfind('class="sales')
        seg = back[k:] if k >= 0 else html[m.end():m.end() + 600]
        sm = re.search(r'class="sales[^"]*"(?:(?!strike-through).)*?<span class="value"[^>]*>\s*([^<]+?)\s*</span>', seg, re.S)
        lp, sv = _money(m.group(1)), _money(sm.group(1)) if sm else None
        if lp and sv and any(abs(sv - o) < 0.01 for o in offers) and sv <= lp <= sv * 5:
            lps.add(lp)
    if len(lps) == 1:
        lists.append(lps.pop())
    # 아크테릭스 한국: JSON-LD에는 판매가만 — 화면 데이터의 정가(retail_price). 이 상품 것만(같은 { } 묶음 안에 이 상품 품번) · 판매가(sell·last)가
    # 이 상품 JSON-LD 가격과 같을 때만 · 판매가보다 높고 5배 안
    for m in re.finditer(r'"retail_price":([0-9.]+),"sell_price":([0-9.]+),"last_price":([0-9.]+)', flat):
        back = flat[max(0, m.start() - 400):m.start()]
        if not any(c in back[back.rfind("{") + 1:].lower() for c in codes): continue
        lp, sps = num(m.group(1)), [num(m.group(2)), num(m.group(3))]
        if lp and any(sp and sp <= lp <= sp * 5 and any(abs(sp - o) < 0.01 for o in offers) for sp in sps):
            lists.append(lp)
    # 살로몬 해외: 상품 이름 바로 뒤 기본가(basePrice) — 화면 데이터가 따옴표를 \"로 감싸 둠. 품번이 맞는 것 우선, 없으면 이름(모델명)
    base_code, base_name = set(), set()
    for m in re.finditer(r'"name":"([^"]{0,80})","newModelCodes":\[([^\]]*)\],"price":\{"basePrice":([0-9.]+),"currency":"([A-Z]{3})"', flat):
        v = num(m.group(3))
        if not v or m.group(4) != cur: continue
        if any(c in m.group(2).lower() for c in codes): base_code.add(v)
        elif word.search(m.group(1).lower()): base_name.add(v)
    base = base_code or base_name
    if len(base) > 1:
        raise RuntimeError(f"여러 상품 기본가가 섞임({', '.join(f'{x:g}' for x in sorted(base))})")
    lists.extend(base)
    micro = False
    if not prods and not lists:   # JSON-LD가 없으면 마이크로데이터(써코니 해외 — 품번이 페이지 상품 칸에 있을 때만)
        mo, ml, micro = _micro(html, cur, codes)
        offers += mo; lists += ml
    if not prods and not lists and not micro:
        raise RuntimeError("상품 가격 데이터(JSON-LD) 없음")
    if not offers and not lists:
        raise RuntimeError(f"{cur} 가격 없음")
    full = max(lists) if lists else max(offers)
    if offers and max(offers) > full: full = max(offers)   # 정가 명세보다 높은 판매가는 없으므로 높은 쪽
    return full, {"cur_price": min(offers) if offers else None, "by": "품번" if by_code or base_code or micro else "이름" if prods or base_name else ""}


def shopify_price(url, code, cur):
    p = _json(get(url)).get("product") or {}
    vs = [v for v in p.get("variants") or [] if isinstance(v, dict) and code.lower() in str(v.get("sku", "")).lower()]
    tags = p.get("tags") if isinstance(p.get("tags"), list) else str(p.get("tags") or "").split(",")
    if not vs and (code.lower().replace("-", "") in str(p.get("handle", "")).lower().replace("-", "")
                   or code.lower() in {str(t).strip().lower() for t in tags}):
        vs = [v for v in p.get("variants") or [] if isinstance(v, dict)]   # 변형 품번이 바코드인 몰 — 상품 주소(handle, 헌터 미국·영국)나 상품 태그(킨 미국·독일)에 품번
    if not vs:
        raise RuntimeError("품번이 다른 상품(대응표 확인)")
    # 쇼피파이 마켓은 접속한 나라 통화로 보여 줄 수 있음(GitHub 서버가 멕시코면 페소) — 변형의 통화 표시가 다르면 실패(이전 값 유지)
    bad = {str(v.get(k)) for v in vs for k in ("price_currency", "compare_at_price_currency") if v.get(k) and str(v.get(k)) != cur}
    if bad:
        raise RuntimeError(f"{cur} 가격 없음(통화 {', '.join(sorted(bad))} — 접속한 서버 나라 통화)")
    full = max(max(num(v.get("price")) or 0, num(v.get("compare_at_price")) or 0) for v in vs)
    if not full:
        raise RuntimeError("가격 없음")
    return full, {"cur_price": min(num(v.get("price")) or full for v in vs)}


def godo_price(html, cur, code):
    """고도몰형 한국 몰(킨·우포스 — 수입사 LF 공식몰): 상품 정보 칸 품번(ARTICLE · Article No.)이 이 상품 품번과 같을 때만, 이 상품 주문 칸의
    숨은 값 정가(set_goods_fixedPrice)·판매가(set_goods_price) 중 높은 값 — 정가를 비워 두면(0) 판매가 · 같은 칸 값이 여러 가지면 실패"""
    if cur != "KRW":
        raise RuntimeError(f"{cur} 가격 없음")
    arts = {unescape(a).strip().lower() for a in re.findall(r'(?:ARTICLE</td>|Article No\.</th>)\s*<td[^>]*>\s*([^<]+?)\s*</td>', html)}
    if code.lower() not in arts:
        raise RuntimeError(f"상품 정보 칸 품번이 다름({', '.join(sorted(arts))[:40] or '품번 칸 없음'}) — 다른 상품으로 바뀜(대응표 확인)")
    def hid(k):
        vs = {num(v) for v in re.findall(rf'name="{k}"\s+value="([0-9.,]+)"', html)}
        if len(vs) > 1:
            raise RuntimeError(f"{k} 값이 여러 가지")
        return vs.pop() if vs else None
    fp, sp = hid("set_goods_fixedPrice"), hid("set_goods_price")
    if not (fp or sp):
        raise RuntimeError("상품 가격 칸(set_goods_price) 없음")
    return max(fp or 0, sp or 0), {"cur_price": sp or fp}


def fetch_one(prod, cc):
    cur = MK[cc][2]
    code = (prod.get("cc_code") or {}).get(cc, prod["code"])   # 그 나라 수입사 품번이 따로 있으면(브룩스 일본)
    if prod["src"] == "nike":
        return nike_price(prod["code"], cc), NIKE_FEED.format(m=MK[cc][0], l=MK[cc][1], s=prod["code"])
    url = prod["urls"].get(cc)
    if not url:
        raise Skip("주소 없음")
    if url.endswith(".json"):
        return shopify_price(url, code, cur), url[:-5]
    r = get(url)
    loc = urllib.parse.urlsplit(url).path.split("/")[1]
    if prod["id"].startswith("on-") and loc not in urllib.parse.urlsplit(r.url).path:   # 온: 그 나라 몰이 없으면 다른 나라로 넘김
        raise Skip(f"다른 나라 몰로 넘어감({urllib.parse.urlsplit(r.url).path.split('/')[1]})")
    if prod.get("code_in_page") and code.lower() not in r.text.lower():   # 품번이 JSON-LD 밖에만 있는 몰 — 페이지에 품번이 없으면 다른 상품
        raise RuntimeError(f"페이지에 품번({code}) 없음 — 다른 상품으로 바뀜(대응표 확인)")
    if 'name="set_goods_fixedPrice"' in r.text:   # 고도몰형 한국 몰(킨·우포스) — JSON-LD 없음, 상품 정보 칸 품번으로 확인
        return godo_price(r.text, cur, code), url
    return page_price(r.text, prod["hint"], cur, [code] + prod.get("alt", [])), url


def cfg_hash():
    return hashlib.sha1(json.dumps(PRODUCTS, ensure_ascii=False, sort_keys=True).encode()).hexdigest()[:12]


def main():
    t0 = time.time(); now = datetime.datetime.now(KST); today = now.date(); td = today.isoformat()
    old = {}
    if os.path.exists(OUT):
        try:
            with open(OUT, encoding="utf-8") as f: old = json.load(f)
        except (OSError, ValueError) as e:
            log(f"[WARN] {OUT} 읽기 실패 — 처음부터: {e}")
    def _days(d): return (today - datetime.date.fromisoformat(d)).days
    last, tried = old.get("fetched"), old.get("tried")   # 받은 날(잘 끝난 실행) · 못 받아 다시 받을 값이 남은 날
    att = old.get("attempt") or last                      # 마지막으로 전체를 받으러 간 날(잘 됐든 안 됐든)
    cfg = cfg_hash()
    if os.environ.get("PRICE_FORCE") == "1" or old.get("cfg") != cfg or not att or _days(att) >= DAYS:
        mode = "full"
    elif tried:
        mode = "retry"   # 지난 실행에서 못 받은 값만 다시
    else:
        mode = None
    codes = {p["id"]: p["code"] for p in PRODUCTS}
    # 품번이 바뀐 상품은 id가 같아도 다른 상품 — 이전 값·값 없음 기록을 쓰지 않음
    prev = {it["id"]: it for it in old.get("items", []) if isinstance(it, dict) and it.get("code") == codes.get(it.get("id"))}
    keys = {f"{p['id']} {cc}" for p in PRODUCTS for cc in (p["cc"] if p["src"] == "nike" else p["urls"])}
    failed = {k: f for f in old.get("failed", []) if isinstance(f, dict) and (k := f"{f.get('id')} {f.get('cc')}") in keys
              and f.get("code", codes.get(f.get("id"))) == codes.get(f.get("id"))}   # 값 없음(이전 값도 없음) — 처음 실패한 날
    ok_run, again = None, False
    if not mode:
        log(f"해외 정가: 주 1회 — 마지막 {att}, 다음 {datetime.date.fromisoformat(att) + datetime.timedelta(days=DAYS)} (건너뜀)")
        items = [it for it in old.get("items", []) if isinstance(it, dict) and it.get("id") in codes]
    else:
        if mode == "retry":
            log(f"해외 정가: 다시 받기 — {att} 받기에서 못 받은 값만")
        items, n_try, n_fail, n_cut, n_hold, n_name = [], 0, 0, 0, 0, 0
        bt = {}   # 브랜드별 [볼 값, 못 받은 값] — 한 브랜드를 통째로 못 받으면 다음 날 다시
        for prod in PRODUCTS:
            pi = prev.get(prod["id"]) or {}; pv = pi.get("m", {})
            cc_list = prod["cc"] if prod["src"] == "nike" else list(prod["urls"])
            m, b = {}, bt.setdefault(prod["brand"], [0, 0])
            for cc in cc_list:
                same = (pi.get("cc_code") or {}).get(cc) == (prod.get("cc_code") or {}).get(cc)   # 나라별 수입사 품번을 바꾸면 그 나라 이전 값은 다른 상품
                o = dict(pv.get(cc) or {}) if same and isinstance(pv.get(cc), dict) else {}; key = f"{prod['id']} {cc}"
                if mode == "retry" and o and not o.get("stale_since") and (o.get("obs_date") or "") >= (att or ""):
                    m[cc] = o; b[0] += 1   # 지난 받기에서 받은 값 — 그대로
                    continue
                if time.time() - t0 > TIME_LIMIT:   # 남은 것은 이전 값(다음 날 다시)
                    n_cut += 1
                    if o:
                        o.setdefault("stale_since", o.get("obs_date") or o.get("seen") or td); o["why"] = "시간 초과로 못 받음"; m[cc] = o
                    else:   # 이전 값도 없음 → 값 없음(처음 못 받은 날부터 21일 알림)
                        f = failed.get(key) or {"id": prod["id"], "cc": cc, "since": td}
                        f.update(code=prod["code"], brand=prod["brand"], name=prod["name"], why="시간 초과로 못 받음"); failed[key] = f
                    continue
                try:
                    (full, extra), src_url = fetch_one(prod, cc)
                    if MK[cc][2] == "KRW" and full < 1000:   # 원화가 1,000원 아래면 단위가 다른 응답
                        raise RuntimeError(f"원화 값이 이상함({full:g})")
                except Skip as e:
                    if not o:   # 처음부터 이 나라에서 팔지 않음 — 실패 아님
                        log(f"  {key}: 건너뜀 — {e}"); failed.pop(key, None)
                        continue
                    e = RuntimeError(f"전에는 받았는데 이번엔 {e}")   # 조용히 사라지지 않게 실패로 셈
                    n_try += 1; n_fail += 1; b[0] += 1; b[1] += 1
                    log(f"  {key}: 못 받음 — {e}")
                    o.setdefault("stale_since", o.get("obs_date") or o.get("seen") or td); o["why"] = str(e)[:80]; m[cc] = o
                    continue
                except Exception as e:   # 이상한 응답 모양(AttributeError 등)도 이 값만 실패로
                    n_try += 1; n_fail += 1; b[0] += 1; b[1] += 1
                    why = f"{type(e).__name__}: {e}" if not isinstance(e, RuntimeError) else str(e)
                    log(f"  {key}: 못 받음 — {why[:120]}")
                    if o:
                        o.setdefault("stale_since", o.get("obs_date") or o.get("seen") or td); o["why"] = why[:80]; m[cc] = o
                    else:
                        f = failed.get(key) or {"id": prod["id"], "cc": cc, "since": td}
                        f.update(code=prod["code"], brand=prod["brand"], name=prod["name"], why=why[:80]); failed[key] = f
                    continue
                n_try += 1; b[0] += 1; failed.pop(key, None)
                full = round(full, 2); cur = MK[cc][2]
                note, held = "", False
                same = o.get("p") and o.get("cur") == cur
                big = same and (full > o["p"] * JUMP or (prod["src"] == "nike" and full < o["p"] / JUMP))
                if big and not (o.get("cand") and abs(o["cand"] - full) <= o["cand"] * 0.10):   # 크게 바뀜 — 다음 확인 때 비슷하면 반영
                    n_hold += 1; held = True
                    o.update(cand=full, cand_date=td, obs=full, obs_date=td, url=src_url, sale=False)
                    o.pop("stale_since", None); o.pop("why", None)
                    note = f"정가 {o['p']:,g} {cur} 유지(이번 {full:,g} — 크게 바뀜, 다음 확인 때 비슷하면 반영)"
                elif (same and not big and prod["src"] != "nike" and full < o["p"] * 0.995
                      and _days(o.get("seen") or td) < SALE_GUARD):   # 할인 가드
                    o.update(obs=full, obs_date=td, sale=True, url=src_url)
                    for k in ("stale_since", "why", "cand", "cand_date"): o.pop(k, None)
                    note = f"정가 {o['p']:,g} {cur} 유지(이번 {full:,g} — 할인으로 봄)"
                else:
                    o = {"p": full, "cur": cur, "seen": td, "url": src_url, "obs": full, "obs_date": td, "sale": False}
                    note = f"정가 {full:,g} {cur}"
                if extra.get("cur_price") and extra["cur_price"] < (full if held else o["p"]) * 0.995:
                    o["sale"] = True   # 지금 할인 중인 색상·사이즈가 있음(정가는 그대로)
                if extra.get("by") == "이름":
                    n_name += 1; note += " · 이름으로 찾음(페이지에 품번 있음)" if prod.get("code_in_page") else " · 품번이 없어 이름으로 찾음"
                m[cc] = o
                log(f"  {key}: {note}" + (" · 할인 중 있음" if o.get("sale") else ""))
            items.append({"id": prod["id"], "brand": prod["brand"], "name": prod["name"], "code": prod["code"], "m": m,
                          **({"cc_code": prod["cc_code"]} if prod.get("cc_code") else {})})
        ok = n_try - n_fail
        whole = [br for br, (n, f) in bt.items() if n and f == n]
        half = bool(n_try and n_fail * 2 > n_try)
        log(f"해외 정가: {len(PRODUCTS)}개 상품 · 받음 {ok}/{n_try} · {time.time() - t0:.0f}초"
            + (f" · 크게 바뀜 {n_hold}건 다음 확인" if n_hold else "") + (f" · 이름으로 찾음 {n_name}건" if n_name else "")
            + (f" · 시간 초과로 {n_cut}건 못 받음" if n_cut else ""))
        # v1.3 전체 받기는 잘 끝났는데 몇 값만 못 받은 날(사이트가 중간에 막음·연결 끊김) → 다음 날 그 값만 한 번 더(조용한 다시 받기 —
        # 또 못 받아도 알림 없이 다음 주에 · 21일 기준은 그대로). 전체 받기가 잘 끝났으면 받은 날(fetched) = 받으러 간 날(attempt)
        quiet = mode == "retry" and last == att
        if mode == "full":
            if half:
                soft_fail(f"해외 정가 절반 넘게 못 받음({n_fail}/{n_try}) — 이전 값 유지, 내일 다시")
            elif whole:   # 첫날은 알림 없이 다음 날 다시(한 번 끊긴 것일 수 있음)
                log(f"해외 정가: {', '.join(whole)} 값을 하나도 못 받음 — 내일 다시")
            elif n_fail:
                log(f"해외 정가: {n_fail}건 못 받음 — 내일 그 값만 한 번 더")
        elif (half or whole) and not quiet:
            soft_fail(f"해외 정가 다시 받기도 못 받음({n_fail}/{n_try}" + (f" · {', '.join(whole)} 전부" if whole else "")
                      + ") — 이전 값 유지, 내일 다시")
        elif quiet and n_fail:
            log(f"해외 정가: 다시 받기에서도 {n_fail}건 못 받음 — 다음 주 받을 때 다시")
        if n_cut:
            log(f"[WARN] 해외 정가: 시간 초과({TIME_LIMIT}초)로 {n_cut}건 못 받음 — 내일 다시")
        ok_run = not (half or whole or n_cut) and not quiet
        again = (not ok_run and not quiet) or (mode == "full" and n_fail > 0)
    # 오래 멈춘 값(21일 넘게 이전 값·값 없음) 알림
    stale = [f"{it['brand']} {it['name']} {cc}" for it in items for cc, o in it.get("m", {}).items()
             if isinstance(o, dict) and o.get("stale_since") and _days(o["stale_since"]) > STALE_ALERT]
    stale += [f"{f.get('brand', '')} {f.get('name', '')} {f['cc']}(값 없음)" for f in failed.values() if _days(f["since"]) > STALE_ALERT]
    if stale:
        soft_fail(f"해외 정가 {len(stale)}건이 {STALE_ALERT}일 넘게 이전 값·값 없음: " + ", ".join(stale[:6]))
    out = {"generated_at": now.strftime("%Y-%m-%d %H:%M KST"),
           "fetched": td if ok_run else last,                       # 받은 날 — 잘 끝난 실행만
           "attempt": td if mode == "full" else att,                # 전체를 받으러 간 날 — 다음 주 받을 날의 기준
           "cfg": cfg if mode else old.get("cfg"),
           "status": "ok" if not stale else "kept", "items": items, "failed": list(failed.values()),
           "note": "브랜드 공식몰 정가(할인 전) · 나이키는 상품 정보 fullPrice · 미국은 판매세 별도, 그 밖은 부가세 포함"}
    if again:
        out["tried"] = td                                           # 못 받은 값이 남음 — 다음 날 그 값만 다시
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    log(f"saved {OUT} ({sum(len(it['m']) for it in items)}개 값" + (f" · 값 없음 {len(failed)}건" if failed else "") + ")")


if __name__ == "__main__":
    main()

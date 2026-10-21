# -*- coding: utf-8 -*-
"""
sports-industry-monitor — Phase 11: 해외 정가 (나라별 브랜드 대표 상품 소비자가)
v1: (대표 지시 2026-10-21 '국가별 브랜드 대표상품 소비자가격 — 미주·유럽·중남미 vs 한국 RRP' · 수기 없음 · 할인 전 풀프라이스 ·
    환율로 한국이 몇 % 싸거나 비싼지 · 브랜드 상세 하단 · 나이키 포함) 브랜드 공식몰의 같은 상품(글로벌 품번)을 나라별로 받아
    docs/prices.json에 저장 — 원화 환산·차이(%)는 화면(build_dashboard)이 그날 환율(data.json fx)로 계산.
    ① 나이키 = 나이키 상품 정보(api.nike.com product_feed, styleColor로 찾음)의 정가 fullPrice — 할인 중이어도 정가가 따로 있음
    ② 그 밖의 공식몰 = 상품 페이지의 구조화 데이터(schema.org JSON-LD): 정가 명세(ListPrice·StrikethroughPrice)가 있으면 그 값,
       없으면 그 상품 색상·사이즈별 가격 중 가장 높은 값(일부 색상만 할인일 때 정가) · 살로몬 해외는 기본가(basePrice)
    ③ 한국 쇼피파이형 몰(살로몬·닥터마틴) = 상품 .json의 compare_at_price(정가)·price 중 높은 값, 변형(사이즈)의 품번이 글로벌 품번과 같아야 함
    찾는 상품 = 글로벌 품번이 품번·주소에 있는 JSON-LD 상품 우선(없을 때만 이름의 모델명) — 추천·관련 상품 가격이 섞이지 않게.
    할인 가드: 이번 값이 저장된 정가보다 낮으면(모든 색상이 할인 중일 때) 120일 동안은 저장된 정가를 지킴(obs에 이번 값) — 그 뒤에도 낮으면 새 정가.
    나이키 fullPrice는 정가 자체라 가드 없이 바로 반영. 정가가 1.5배 넘게 오르면(나이키는 내려도) 바로 바꾸지 않고 다음 확인 때 같으면 반영(cand).
    주 1회(7일) — 매일 update-dashboard 안에서 돌되 7일이 안 지났고 상품 목록이 같으면 건너뜀(update.yml 수동 실행 입력 price_force=1 → PRICE_FORCE=1이면 바로).
    절반 넘게 실패했거나 시간 초과로 다 못 받은 날은 '받은 날'(fetched)을 옮기지 않아 다음 날 다시 받음.
    봇 차단은 우회하지 않음: 우리 봇 이름(UA)을 밝히고 robots.txt(RFC 9309 — 우리 이름 그룹 우선·* 와일드카드·가장 긴 규칙)를 먼저 확인,
    robots.txt가 서버 오류·연결 안 됨이면 그 사이트는 이번 실행 건너뜀(예외: robots.txt를 두지 않는 API 주소는 같은 회사 대표 사이트의
    robots.txt를 따름 — ROBOTS_ALT), 403/429를 받으면 그 사이트에 더 요청하지 않음, 주소당 1번만 요청
    (접속 시험 2026-10-21: 아디다스·뉴발란스·아식스·크록스 한국·에코·몽클레르·룰루레몬·랄프로렌·어그·스케쳐스 한국은 403/429라 넣지 않음).
    못 받으면 이전 값(stale_since = 마지막으로 받은 날) · 전에 받던 값이 '팔지 않음'으로 바뀌어도 실패로 셈 · 이전 값도 없으면 failed(값 없음, 처음 실패한 날).
    한 실행에서 절반 넘게 실패하거나, 한 값이 21일 넘게 이전 값·값 없음이면 실패 표시(soft_fail.txt).
    나라를 늘리면 MK + build_dashboard PR_ORD·PR_CC·PR_SYM + (새 통화면) fetch_data FX를 함께 고친다.
"""
import datetime, hashlib, json, os, re, time, urllib.parse
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
TIME_LIMIT = 6 * 60 # 초 — 한 실행 최대(넘으면 남은 것은 이전 값)
GAP = 1.5           # 초 — 요청 사이 쉬는 시간
JUMP = 1.5          # 배 — 정가가 이만큼 넘게 바뀌면 다음 확인 때 같아야 반영

# 나라 → (나이키 상품 정보 marketplace·language, 통화)
MK = {"KR": ("KR", "ko", "KRW"), "US": ("US", "en", "USD"), "GB": ("GB", "en-GB", "GBP"), "DE": ("DE", "de", "EUR"),
      "JP": ("JP", "ja", "JPY"), "MX": ("MX", "es-419", "MXN")}
NIKE_FEED = ("https://api.nike.com/product_feed/threads/v3/?filter=marketplace({m})&filter=language({l})"
             "&filter=channelId(d9a5bc42-4b9c-4976-858a-f159cf99c647)&filter=productInfo.merchProduct.styleColor({s})")

# 대표 상품 — brand는 브랜드 점검표(네이버 감시 브랜드) 이름과 같게. urls 없는 나라는 그 브랜드 공식몰에서 받지 못하는 곳(시험 2026-10-21)
DM = "https://www.drmartens.com"
PRODUCTS = [
    {"id": "nike-af1", "brand": "나이키", "name": "에어포스 1 '07", "code": "CW2288-111", "src": "nike", "cc": ["KR", "US", "GB", "DE", "JP", "MX"]},
    {"id": "nike-dunk", "brand": "나이키", "name": "덩크 로우 레트로", "code": "DD1391-100", "src": "nike", "cc": ["KR", "US", "GB", "DE", "JP", "MX"]},
    {"id": "nike-am90", "brand": "나이키", "name": "에어맥스 90", "code": "CN8490-100", "src": "nike", "cc": ["KR", "US", "GB", "DE", "JP", "MX"]},   # 브라질은 나이키 직영이 아님(시험 2026-10-21 · 결과 없음)
    {"id": "puma-speedcat", "brand": "푸마", "name": "스피드캣 OG", "code": "398846", "src": "page", "hint": "speedcat", "urls": {
        "KR": "https://kr.puma.com/kr/ko/pd/%EC%8A%A4%ED%94%BC%EB%93%9C%EC%BA%A3-og-%3Cbr%3Espeedcat-og/398846.html",
        "US": "https://us.puma.com/us/en/pd/speedcat-og-sneakers/398846",
        "GB": "https://uk.puma.com/uk/en/pd/speedcat-og-sneakers-unisex/398846",
        "DE": "https://eu.puma.com/de/de/pd/speedcat-og-sneakers/398846",
        "JP": "https://jp.puma.com/jp/ja/pd/%E3%83%A6%E3%83%8B%E3%82%BB%E3%83%83%E3%82%AF%E3%82%B9-%E3%82%B9%E3%83%94%E3%83%BC%E3%83%89%E3%82%AD%E3%83%A3%E3%83%83%E3%83%88-og-%E3%82%B9%E3%83%8B%E3%83%BC%E3%82%AB%E3%83%BC/398846",
        "MX": "https://mx.puma.com/mx/es/pd/tenis-speedcat-og/398846.html"}},
    {"id": "on-cloudmonster", "brand": "온러닝", "name": "클라우드몬스터", "code": "61.98434", "src": "page", "hint": "cloudmonster", "urls": {
        cc: f"https://www.on.com/{loc}/products/cloudmonster-61/mens/all-white-shoes-61.98434"
        for cc, loc in (("KR", "ko-kr"), ("US", "en-us"), ("GB", "en-gb"), ("DE", "de-de"), ("JP", "ja-jp"))}},
    {"id": "salomon-xt6", "brand": "살로몬", "name": "XT-6 고어텍스", "code": "L47450600", "alt": ["LG9333"], "src": "page", "hint": "xt-6", "urls": {
        "KR": "https://salomon.co.kr/products/l47450600.json",
        "US": "https://www.salomon.com/en-us/product/xt-6-gore-tex-lg9333",
        "GB": "https://www.salomon.com/en-gb/product/xt-6-gore-tex-lg9333",
        "DE": "https://www.salomon.com/de-de/product/xt-6-gore-tex-lg9333"}},
    {"id": "drm-1461", "brand": "닥터마틴", "name": "1461 스무스", "code": "11838002", "src": "page", "hint": "1461", "urls": {
        "KR": "https://www.drmartens.co.kr/products/boots-1461-black-smooth.json",
        "US": f"{DM}/us/en/1461-smooth-leather-oxford-shoes-black/p/11838002",
        "GB": f"{DM}/uk/en_gb/1461-smooth-leather-oxford-shoes-black/p/11838002"}},
    {"id": "drm-jadon", "brand": "닥터마틴", "name": "제이든", "code": "15265001", "src": "page", "hint": "jadon", "urls": {
        "KR": "https://www.drmartens.co.kr/products/boots-jadon-black-15265001.json",
        "US": f"{DM}/us/en/jadon-smooth-leather-platform-boots-black/p/15265001",
        "GB": f"{DM}/uk/en_gb/jadon-smooth-leather-platform-boots-black/p/15265001"}},
    # 닥터마틴 1460은 한국 몰 품번(10072004)이 해외(11822006)와 달라 넣지 않음(같은 상품인지 확인 안 됨)
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


_ROB, _LAST, _BLOCKED = {}, [0.0], set()
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
            if v:
                rx = re.escape(urllib.parse.unquote(v)).replace(r"\*", ".*")
                if rx.endswith(r"\$"): rx = rx[:-2] + "$"
                g["rules"].append((k == "allow", re.compile(rx), len(v)))
    mine = [gg for gg in groups if BOT in gg["ua"]] or [gg for gg in groups if "*" in gg["ua"]]
    return [r for gg in mine for r in gg["rules"]]


def _robots_get(base):
    """규칙 목록, 또는 못 받은 이유(글) — 4xx면 규칙 없음, 429·5xx·연결 안 됨이면 이유(RFC 9309: 그 사이트 전체를 막힌 것으로)"""
    try:
        r = requests.get(base + "/robots.txt", headers=HDR, timeout=20)
        if r.status_code == 429 or r.status_code >= 500:
            return f"robots.txt HTTP {r.status_code}"
        return _robots_rules(r.text) if r.status_code == 200 else []
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


def get(url):
    host = urllib.parse.urlsplit(url).netloc
    if host in _BLOCKED:
        raise RuntimeError("이번 실행에서 이 사이트가 막음 — 더 요청 안 함")
    ok, why = robots_ok(url)
    if not ok:
        raise RuntimeError(why)
    w = GAP - (time.time() - _LAST[0])
    if w > 0: time.sleep(w)
    _LAST[0] = time.time()
    r = requests.get(url, headers=HDR, timeout=25, allow_redirects=True)
    if r.status_code in (403, 429):
        _BLOCKED.add(host)
        raise RuntimeError(f"HTTP {r.status_code}(접속 차단 — 우회하지 않음)")
    if r.status_code >= 400:
        raise RuntimeError(f"HTTP {r.status_code}")
    if r.url != url and not robots_ok(r.url)[0]:   # 넘겨진 주소도 robots.txt 확인
        raise RuntimeError("넘겨진 주소를 robots.txt가 막음")
    return r


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


def _ld_nodes(html):
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
                st.extend(v for v in x.values() if isinstance(v, (dict, list)))
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
    prods = by_code or [n for n in nodes if word.search(str(n.get("name", "")).lower())]
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
    # 살로몬 해외: 상품 이름 바로 뒤 기본가(basePrice) — 화면 데이터가 따옴표를 \"로 감싸 둠. 품번이 맞는 것 우선, 없으면 이름(모델명)
    flat = html.replace('\\"', '"')
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
    if not prods and not lists:
        raise RuntimeError("상품 가격 데이터(JSON-LD) 없음")
    if not offers and not lists:
        raise RuntimeError(f"{cur} 가격 없음")
    full = max(lists) if lists else max(offers)
    if offers and max(offers) > full: full = max(offers)   # 정가 명세보다 높은 판매가는 없으므로 높은 쪽
    return full, {"cur_price": min(offers) if offers else None}


def shopify_price(url, code):
    p = _json(get(url)).get("product") or {}
    vs = [v for v in p.get("variants") or [] if isinstance(v, dict) and code.lower() in str(v.get("sku", "")).lower()]
    if not vs:
        raise RuntimeError("품번이 다른 상품(대응표 확인)")
    full = max(max(num(v.get("price")) or 0, num(v.get("compare_at_price")) or 0) for v in vs)
    if not full:
        raise RuntimeError("가격 없음")
    return full, {"cur_price": min(num(v.get("price")) or full for v in vs)}


def fetch_one(prod, cc):
    cur = MK[cc][2]
    if prod["src"] == "nike":
        return nike_price(prod["code"], cc), NIKE_FEED.format(m=MK[cc][0], l=MK[cc][1], s=prod["code"])
    url = prod["urls"].get(cc)
    if not url:
        raise Skip("주소 없음")
    if url.endswith(".json"):
        return shopify_price(url, prod["code"]), url[:-5]
    r = get(url)
    loc = urllib.parse.urlsplit(url).path.split("/")[1]
    if prod["id"].startswith("on-") and loc not in urllib.parse.urlsplit(r.url).path:   # 온: 그 나라 몰이 없으면 다른 나라로 넘김
        raise Skip(f"다른 나라 몰로 넘어감({urllib.parse.urlsplit(r.url).path.split('/')[1]})")
    return page_price(r.text, prod["hint"], cur, [prod["code"]] + prod.get("alt", [])), url


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
    last = old.get("fetched")
    due = (not last or (today - datetime.date.fromisoformat(last)).days >= DAYS or old.get("cfg") != cfg_hash()
           or os.environ.get("PRICE_FORCE") == "1")
    prev = {it["id"]: it for it in old.get("items", [])}
    ids = {p["id"] for p in PRODUCTS}
    keys = {f"{p['id']} {cc}" for p in PRODUCTS for cc in (p["cc"] if p["src"] == "nike" else p["urls"])}
    failed = {k: f for f in old.get("failed", []) if (k := f"{f.get('id')} {f.get('cc')}") in keys}   # 값 없음(이전 값도 없음) — 처음 실패한 날
    advance = due
    if not due:
        log(f"해외 정가: 주 1회 — 마지막 {last}, 다음 {datetime.date.fromisoformat(last) + datetime.timedelta(days=DAYS)} (건너뜀)")
        items = [it for it in old.get("items", []) if it.get("id") in ids]
    else:
        items, n_try, n_fail, n_cut, n_hold = [], 0, 0, 0, 0
        for prod in PRODUCTS:
            pv = (prev.get(prod["id"]) or {}).get("m", {})
            cc_list = prod["cc"] if prod["src"] == "nike" else list(prod["urls"])
            m = {}
            for cc in cc_list:
                o = dict(pv.get(cc) or {}); key = f"{prod['id']} {cc}"
                if time.time() - t0 > TIME_LIMIT:   # 남은 것은 이전 값(다음 날 다시)
                    n_cut += 1
                    if o:
                        o.setdefault("stale_since", o.get("obs_date") or o.get("seen") or td); o["why"] = "시간 초과로 못 받음"; m[cc] = o
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
                    n_try += 1; n_fail += 1
                    log(f"  {key}: 못 받음 — {e}")
                    o.setdefault("stale_since", o.get("obs_date") or o.get("seen") or td); o["why"] = str(e)[:80]; m[cc] = o
                    continue
                except Exception as e:   # 이상한 응답 모양(AttributeError 등)도 이 값만 실패로
                    n_try += 1; n_fail += 1
                    why = f"{type(e).__name__}: {e}" if not isinstance(e, RuntimeError) else str(e)
                    log(f"  {key}: 못 받음 — {why[:120]}")
                    if o:
                        o.setdefault("stale_since", o.get("obs_date") or o.get("seen") or td); o["why"] = why[:80]; m[cc] = o
                    else:
                        f = failed.get(key) or {"id": prod["id"], "cc": cc, "since": td}
                        f.update(brand=prod["brand"], name=prod["name"], why=why[:80]); failed[key] = f
                    continue
                n_try += 1; failed.pop(key, None)
                full = round(full, 2); cur = MK[cc][2]
                note = ""
                same = o.get("p") and o.get("cur") == cur
                big = same and (full > o["p"] * JUMP or (prod["src"] == "nike" and full < o["p"] / JUMP))
                if big and not (o.get("cand") and abs(o["cand"] - full) <= o["cand"] * 0.005):   # 크게 바뀜 — 다음 확인 때 같으면 반영
                    n_hold += 1
                    o.update(cand=full, cand_date=td, obs=full, obs_date=td, url=src_url)
                    o.pop("stale_since", None); o.pop("why", None)
                    note = f"정가 {o['p']:,g} {cur} 유지(이번 {full:,g} — 크게 바뀜, 다음 확인 때 같으면 반영)"
                elif (same and not big and prod["src"] != "nike" and full < o["p"] * 0.995
                      and (today - datetime.date.fromisoformat(o.get("seen") or td)).days < SALE_GUARD):   # 할인 가드
                    o.update(obs=full, obs_date=td, sale=True, url=src_url)
                    for k in ("stale_since", "why", "cand", "cand_date"): o.pop(k, None)
                    note = f"정가 {o['p']:,g} {cur} 유지(이번 {full:,g} — 할인으로 봄)"
                else:
                    o = {"p": full, "cur": cur, "seen": td, "url": src_url, "obs": full, "obs_date": td, "sale": False}
                    note = f"정가 {full:,g} {cur}"
                if extra.get("cur_price") and extra["cur_price"] < o["p"] * 0.995:
                    o["sale"] = True   # 지금 할인 중인 색상·사이즈가 있음(정가는 그대로)
                m[cc] = o
                log(f"  {key}: {note}" + (" · 할인 중 있음" if o.get("sale") else ""))
            items.append({"id": prod["id"], "brand": prod["brand"], "name": prod["name"], "code": prod["code"], "m": m})
        ok = n_try - n_fail
        log(f"해외 정가: {len(PRODUCTS)}개 상품 · 받음 {ok}/{n_try} · {time.time() - t0:.0f}초"
            + (f" · 크게 바뀜 {n_hold}건 다음 확인" if n_hold else "") + (f" · 시간 초과로 {n_cut}건 못 받음" if n_cut else ""))
        if n_try and n_fail * 2 > n_try:
            soft_fail(f"해외 정가 절반 넘게 못 받음({n_fail}/{n_try}) — 이전 값 유지, 내일 다시")
            advance = False
        if n_cut:
            log(f"[WARN] 해외 정가: 시간 초과({TIME_LIMIT}초)로 {n_cut}건 못 받음 — 내일 다시")
            advance = False
    # 오래 멈춘 값(21일 넘게 이전 값·값 없음) 알림
    def _old(d): return (today - datetime.date.fromisoformat(d)).days > STALE_ALERT
    stale = [f"{it['brand']} {it['name']} {cc}" for it in items for cc, o in it.get("m", {}).items()
             if o.get("stale_since") and _old(o["stale_since"])]
    stale += [f"{f.get('brand', '')} {f.get('name', '')} {f['cc']}(값 없음)" for f in failed.values() if _old(f["since"])]
    if stale:
        soft_fail(f"해외 정가 {len(stale)}건이 {STALE_ALERT}일 넘게 이전 값·값 없음: " + ", ".join(stale[:6]))
    out = {"generated_at": now.strftime("%Y-%m-%d %H:%M KST"),
           "fetched": td if advance else last,                     # 받은 날 — 절반 넘게 실패·시간 초과면 그대로(다음 날 다시)
           "cfg": cfg_hash() if advance else old.get("cfg"),
           "status": "ok" if not stale else "kept", "items": items, "failed": list(failed.values()),
           "note": "브랜드 공식몰 정가(할인 전) · 나이키는 상품 정보 fullPrice · 미국은 판매세 별도, 그 밖은 부가세 포함"}
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    log(f"saved {OUT} ({sum(len(it['m']) for it in items)}개 값" + (f" · 값 없음 {len(failed)}건" if failed else "") + ")")


if __name__ == "__main__":
    main()

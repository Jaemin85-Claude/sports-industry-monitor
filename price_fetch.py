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
    할인 가드: 이번 값이 저장된 정가보다 낮으면(모든 색상이 할인 중일 때) 120일 동안은 저장된 정가를 지킴(obs에 이번 값) — 그 뒤에도 낮으면 새 정가.
    주 1회(7일) — 매일 update-dashboard 안에서 돌되 7일이 안 지났고 상품 목록이 같으면 건너뜀(PRICE_FORCE=1이면 바로).
    봇 차단은 우회하지 않음: 우리 봇 이름(UA)을 밝히고 robots.txt를 먼저 확인, 주소당 1번만 요청(접속 시험 2026-10-21: 아디다스·뉴발란스·
    아식스·크록스 한국·에코·몽클레르·룰루레몬·랄프로렌·어그·스케쳐스 한국은 403/429라 넣지 않음).
    못 받으면 이전 값(stale_since) · 한 실행에서 절반 넘게 실패하거나 한 값이 21일 넘게 이전 값이면 실패 표시(soft_fail.txt).
"""
import datetime, hashlib, json, os, re, sys, time, urllib.parse, urllib.robotparser
import requests

SCRIPT = "price_fetch"
OUT = "docs/prices.json"
KST = datetime.timezone(datetime.timedelta(hours=9))
UA = "Mozilla/5.0 (compatible; sports-industry-monitor price bot; +https://github.com/Jaemin85-Claude/sports-industry-monitor)"
HDR = {"User-Agent": UA, "Accept": "text/html,application/json;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.8,ko;q=0.6"}
DAYS = 7            # 주 1회
SALE_GUARD = 120    # 일 — 이 기간 안에 정가보다 낮게 보이면 할인으로 보고 정가를 지킴
STALE_ALERT = 21    # 일 — 이 일수 넘게 이전 값이면 실패 표시
TIME_LIMIT = 6 * 60 # 초 — 한 실행 최대(넘으면 남은 것은 이전 값)
GAP = 1.5           # 초 — 요청 사이 쉬는 시간

# 나라 → (나이키 상품 정보 marketplace·language, 통화)
MK = {"KR": ("KR", "ko", "KRW"), "US": ("US", "en", "USD"), "GB": ("GB", "en-GB", "GBP"), "DE": ("DE", "de", "EUR"),
      "JP": ("JP", "ja", "JPY"), "MX": ("MX", "es-419", "MXN"), "BR": ("BR", "pt-BR", "BRL")}
NIKE_FEED = ("https://api.nike.com/product_feed/threads/v3/?filter=marketplace({m})&filter=language({l})"
             "&filter=channelId(d9a5bc42-4b9c-4976-858a-f159cf99c647)&filter=productInfo.merchProduct.styleColor({s})")

# 대표 상품 — brand는 브랜드 점검표(네이버 감시 브랜드) 이름과 같게. urls 없는 나라는 그 브랜드 공식몰에서 받지 못하는 곳(시험 2026-10-21)
DM = "https://www.drmartens.com"
PRODUCTS = [
    {"id": "nike-af1", "brand": "나이키", "name": "에어포스 1 '07", "code": "CW2288-111", "src": "nike", "cc": ["KR", "US", "GB", "DE", "JP", "MX", "BR"]},
    {"id": "nike-dunk", "brand": "나이키", "name": "덩크 로우 레트로", "code": "DD1391-100", "src": "nike", "cc": ["KR", "US", "GB", "DE", "JP", "MX", "BR"]},
    {"id": "nike-am90", "brand": "나이키", "name": "에어맥스 90", "code": "CN8490-100", "src": "nike", "cc": ["KR", "US", "GB", "DE", "JP", "MX", "BR"]},
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
    {"id": "salomon-xt6", "brand": "살로몬", "name": "XT-6 고어텍스", "code": "L47450600", "src": "page", "hint": "xt-6", "urls": {
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
    {"id": "drm-1460", "brand": "닥터마틴", "name": "1460 스무스", "code": "10072004", "src": "page", "hint": "1460", "urls": {
        "KR": "https://www.drmartens.co.kr/products/1460-2.json",
        "US": f"{DM}/us/en/1460-smooth-leather-lace-up-boots-black/p/10072004",
        "GB": f"{DM}/uk/en_gb/1460-smooth-leather-lace-up-boots-black/p/10072004"}},
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


_ROB, _LAST = {}, [0.0]


def robots_ok(url):
    p = urllib.parse.urlsplit(url); base = f"{p.scheme}://{p.netloc}"
    if base not in _ROB:
        rp = urllib.robotparser.RobotFileParser()
        try:
            r = requests.get(base + "/robots.txt", headers=HDR, timeout=20)
            rp.parse(r.text.splitlines() if r.status_code == 200 else [])
        except requests.RequestException:
            rp.parse([])   # robots.txt를 못 받으면 막지 않은 것으로(표준 동작)
        _ROB[base] = rp
    return _ROB[base].can_fetch(UA, url)


def get(url):
    if not robots_ok(url):
        raise RuntimeError("robots.txt가 막음")
    w = GAP - (time.time() - _LAST[0])
    if w > 0: time.sleep(w)
    _LAST[0] = time.time()
    r = requests.get(url, headers=HDR, timeout=25, allow_redirects=True)
    if r.status_code in (403, 429):
        raise RuntimeError(f"HTTP {r.status_code}(접속 차단 — 우회하지 않음)")
    if r.status_code >= 400:
        raise RuntimeError(f"HTTP {r.status_code}")
    return r


def num(v):
    try:
        x = float(str(v).replace(",", ""))
        return x if x > 0 else None
    except (TypeError, ValueError):
        return None


def nike_price(code, cc):
    m, l, cur = MK[cc]
    d = get(NIKE_FEED.format(m=m, l=l, s=code)).json()
    objs = d.get("objects") or []
    if not objs:
        raise Skip("이 나라 나이키에서 팔지 않음")
    for o in objs:
        for pi in o.get("productInfo") or []:
            mp, mer = pi.get("merchPrice") or {}, pi.get("merchProduct") or {}
            if mer.get("styleColor") not in (None, code):
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


def page_price(html, hint, cur):
    """상품 페이지 → 정가. 상품 이름에 hint가 든 JSON-LD 상품만 봄(추천 상품 섞임 방지)"""
    offers, lists = [], []
    prods = [n for n in _ld_nodes(html) if str(n.get("@type", "")).lower() in ("product", "productgroup")
             and hint in (str(n.get("name", "")) + " " + str(n.get("sku", ""))).lower()]
    for p in prods:
        st = [p.get("offers"), p.get("hasVariant")]
        while st:
            x = st.pop()
            if isinstance(x, list): st.extend(x); continue
            if not isinstance(x, dict): continue
            if x.get("@type") in ("Product",): st.append(x.get("offers")); continue
            if str(x.get("priceCurrency", cur)) == cur:
                v = num(x.get("price") or x.get("highPrice") or x.get("lowPrice"))
                if v: offers.append(v)
            for ps in (x.get("priceSpecification") if isinstance(x.get("priceSpecification"), list) else [x.get("priceSpecification")]):
                if isinstance(ps, dict) and re.search(r"ListPrice|StrikethroughPrice", str(ps.get("priceType", ""))) and str(ps.get("priceCurrency", cur)) == cur:
                    v = num(ps.get("price"))
                    if v: lists.append(v)
            if x.get("offers"): st.append(x.get("offers"))
    # 살로몬 해외: 상품 이름 바로 뒤 기본가(basePrice) — 화면 데이터가 따옴표를 \"로 감싸 둠
    flat = html.replace('\\"', '"')
    for m in re.finditer(r'"name":"([^"]{0,80})","newModelCodes":\[[^\]]*\],"price":\{"basePrice":([0-9.]+),"currency":"([A-Z]{3})"', flat):
        if hint in m.group(1).lower() and m.group(3) == cur:
            v = num(m.group(2))
            if v: lists.append(v)
    if not prods and not lists:
        raise RuntimeError("상품 가격 데이터(JSON-LD) 없음")
    if not offers and not lists:
        raise RuntimeError(f"{cur} 가격 없음")
    full = max(lists) if lists else max(offers)
    if offers and max(offers) > full: full = max(offers)   # 정가 명세보다 높은 판매가는 없으므로 높은 쪽
    return full, {"cur_price": min(offers) if offers else None, "has_list": bool(lists)}


def shopify_price(url, code):
    d = get(url).json()
    p = d.get("product") or {}
    vs = [v for v in p.get("variants") or [] if code.lower() in str(v.get("sku", "")).lower()]
    if not vs:
        raise RuntimeError("품번이 다른 상품(대응표 확인)")
    full = max(max(num(v.get("price")) or 0, num(v.get("compare_at_price")) or 0) for v in vs)
    if not full:
        raise RuntimeError("가격 없음")
    return full, {"cur_price": min(num(v.get("price")) or full for v in vs), "has_list": any(num(v.get("compare_at_price")) for v in vs)}


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
    return page_price(r.text, prod["hint"], cur), url


def cfg_hash():
    return hashlib.sha1(json.dumps(PRODUCTS, ensure_ascii=False, sort_keys=True).encode()).hexdigest()[:12]


def main():
    t0 = time.time(); now = datetime.datetime.now(KST); today = now.date()
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
    if not due:
        log(f"해외 정가: 주 1회 — 마지막 {last}, 다음 {datetime.date.fromisoformat(last) + datetime.timedelta(days=DAYS)} (건너뜀)")
        items = old.get("items", [])
    else:
        items, n_try, n_fail = [], 0, 0
        for prod in PRODUCTS:
            pv = (prev.get(prod["id"]) or {}).get("m", {})
            cc_list = prod["cc"] if prod["src"] == "nike" else list(prod["urls"])
            m = {}
            for cc in cc_list:
                o = dict(pv.get(cc) or {})
                if time.time() - t0 > TIME_LIMIT:
                    if o: o.setdefault("stale_since", o.get("seen") or today.isoformat()); m[cc] = o
                    continue
                try:
                    (full, extra), src_url = fetch_one(prod, cc)
                except Skip as e:
                    log(f"  {prod['id']} {cc}: 건너뜀 — {e}")
                    continue
                except (requests.RequestException, RuntimeError, ValueError) as e:
                    n_try += 1; n_fail += 1
                    log(f"  {prod['id']} {cc}: 못 받음 — {str(e)[:120]}")
                    if o:
                        o.setdefault("stale_since", today.isoformat()); o["why"] = str(e)[:80]; m[cc] = o
                    continue
                n_try += 1
                full = round(full, 2); cur = MK[cc][2]
                kept = False
                if o.get("p") and full < o["p"] * 0.995 and o.get("cur") == cur:   # 할인 가드
                    seen = datetime.date.fromisoformat(o.get("seen") or today.isoformat())
                    if (today - seen).days < SALE_GUARD:
                        kept = True
                if kept:
                    o.update(obs=full, obs_date=today.isoformat(), sale=True, url=src_url)
                    o.pop("stale_since", None); o.pop("why", None)
                else:
                    o = {"p": full, "cur": cur, "seen": today.isoformat(), "url": src_url, "obs": full, "obs_date": today.isoformat(), "sale": False}
                if extra.get("cur_price") and extra["cur_price"] < o["p"] * 0.995:
                    o["sale"] = True   # 지금 할인 중인 색상·사이즈가 있음(정가는 그대로)
                m[cc] = o
                log(f"  {prod['id']} {cc}: 정가 {full:g} {cur}" + (" · 할인 가드(저장된 정가 유지)" if kept else "") + (" · 할인 중 있음" if o.get("sale") else ""))
            items.append({"id": prod["id"], "brand": prod["brand"], "name": prod["name"], "code": prod["code"], "m": m})
        ok = n_try - n_fail
        log(f"해외 정가: {len(PRODUCTS)}개 상품 · 받음 {ok}/{n_try} · {time.time() - t0:.0f}초")
        if n_try and n_fail * 2 > n_try:
            soft_fail(f"해외 정가 절반 넘게 못 받음({n_fail}/{n_try}) — 이전 값 유지")
    # 오래 멈춘 값(21일 넘게) 알림
    stale = [f"{it['brand']} {it['name']} {cc}" for it in items for cc, o in it.get("m", {}).items()
             if o.get("stale_since") and (today - datetime.date.fromisoformat(o["stale_since"])).days > STALE_ALERT]
    if stale:
        soft_fail(f"해외 정가 {len(stale)}건이 {STALE_ALERT}일 넘게 이전 값: " + ", ".join(stale[:6]))
    out = {"generated_at": now.strftime("%Y-%m-%d %H:%M KST"), "fetched": today.isoformat() if due else last,
           "cfg": cfg_hash(), "status": "ok" if not stale else "kept", "items": items,
           "note": "브랜드 공식몰 정가(할인 전) · 나이키는 상품 정보 fullPrice · 미국은 판매세 별도, 그 밖은 부가세 포함"}
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    log(f"saved {OUT} ({sum(len(it['m']) for it in items)}개 값)")


if __name__ == "__main__":
    main()

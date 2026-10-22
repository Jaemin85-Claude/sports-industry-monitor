# -*- coding: utf-8 -*-
"""임시 시험(병합 안 함) — 5개 브랜드(드래곤디퓨전·헌터·언더아머·써코니·브룩스) 나라별 같은 상품 주소·품번·가격 위치 찾기.
price_fetch.get()(우리 봇 이름 · robots.txt · 403/429면 그 사이트 그만)을 그대로 씀. 저장·커밋 안 함."""
import json, re, sys, time, urllib.parse
import requests
import price_fetch as pf

pf.GAP = 0.8
T0 = time.time()


def tryget(url):
    try:
        r = pf.get(url)
        return r, r.text, ""
    except Exception as e:
        return None, "", str(e)[:90]


def big(u, cap=12_000_000):
    """사이트맵처럼 큰 파일 — robots 확인 후 cap까지만"""
    ok, why = pf.robots_ok(u)
    if not ok or urllib.parse.urlsplit(u).netloc in pf._BLOCKED:
        return "", f"robots/막힘 {why}"
    w = pf.GAP - (time.time() - pf._LAST[0])
    if w > 0: time.sleep(w)
    pf._LAST[0] = time.time()
    try:
        r = requests.get(u, headers=pf.HDR, timeout=30, stream=True)
        if r.status_code != 200: return "", f"HTTP {r.status_code}"
        b = b""
        for ch in r.iter_content(262144):
            b += ch
            if len(b) > cap: break
        r.close()
        return b.decode("utf-8", "replace"), ""
    except Exception as e:
        return "", str(e)[:60]


def ld_dump(h, cur=None):
    out = []
    for n in pf._ld_nodes(h):
        if not (pf._types(n) & {"product", "productgroup"}): continue
        offs = []
        st = [n.get("offers")]
        while st:
            x = st.pop()
            if isinstance(x, list): st.extend(x); continue
            if not isinstance(x, dict): continue
            ps = x.get("priceSpecification")
            lp = [q.get("price") for q in (ps if isinstance(ps, list) else [ps]) if isinstance(q, dict)]
            offs.append(f"{x.get('price') or x.get('lowPrice')}/{x.get('highPrice') or ''}{x.get('priceCurrency')}{' LP' + str(lp) if lp else ''} sku={x.get('sku', '')}")
            if x.get("offers"): st.append(x.get("offers"))
        out.append(f"[{'/'.join(sorted(pf._types(n)))}] name={str(n.get('name'))[:50]!r} sku={n.get('sku')} pid={n.get('productID')} pg={n.get('productGroupID')} mpn={n.get('mpn')} model={n.get('model')} "
                   f"url={str(n.get('url', ''))[:70]} offers={offs[:4]}")
    return out


def snippets(h, pat, n=12, w=110):
    out = []
    for m in re.finditer(pat, h):
        s = h[max(0, m.start() - w): m.end() + w].replace("\n", " ")
        out.append(re.sub(r"\s+", " ", s))
        if len(out) >= n: break
    return out


def shopify_scan(base, pat, pages=15):
    print(f"\n## Shopify {base} — /products.json 훑기 ({pat})", flush=True)
    rx = re.compile(pat, re.I)
    hits = 0
    for p in range(1, pages + 1):
        r, h, e = tryget(f"{base}/products.json?limit=250&page={p}")
        if not r:
            print(f"  쪽 {p} ✗ {e}"); break
        try:
            ps = json.loads(h).get("products") or []
        except ValueError:
            print(f"  쪽 {p} 형식 다름"); break
        if not ps: break
        for x in ps:
            vs = x.get("variants") or []
            skus = [str(v.get("sku", "")) for v in vs]
            blob = " ".join([x.get("title", ""), x.get("handle", ""), " ".join(skus), " ".join(x.get("tags", []) if isinstance(x.get("tags"), list) else [str(x.get("tags"))])])
            if rx.search(blob):
                hits += 1
                pr = sorted({(v.get("price"), v.get("compare_at_price")) for v in vs}, key=str)[:3]
                print(f"  ✓ {x.get('handle')} | {x.get('title')[:60]} | type={x.get('product_type')} | sku {skus[:3]} | 가격/정가 {pr}", flush=True)
                if hits > 40: return
        print(f"  쪽 {p}: {len(ps)}개", flush=True)


def sitemap_grep(home, pat, maxfiles=12, show=15):
    print(f"\n## 사이트맵 {home} — {pat}", flush=True)
    sp = urllib.parse.urlsplit(home); base = f"{sp.scheme}://{sp.netloc}"
    rb, e = big(base + "/robots.txt", 300_000)
    maps = re.findall(r"(?im)^\s*sitemap:\s*(\S+)", rb) or [base + "/sitemap.xml", base + "/sitemap_index.xml"]
    print(f"  robots 사이트맵 {len(maps)}개: {maps[:6]}", flush=True)
    rx = re.compile(pat, re.I)
    seen, found, n = set(), [], 0
    todo = [m for m in maps if not m.endswith(".gz")]
    while todo and n < maxfiles and time.time() - T0 < 30 * 60:
        m = todo.pop(0)
        if m in seen: continue
        seen.add(m); n += 1
        x, e = big(m)
        if not x:
            print(f"  ✗ {m[:100]} {e}"); continue
        locs = re.findall(r"<loc>\s*(?:<!\[CDATA\[)?\s*([^<\s\]]+)", x)
        subs = [l for l in locs if re.search(r"\.xml(\?|$)", l) and not l.endswith(".gz")]
        hit = [l for l in locs if rx.search(urllib.parse.unquote(l))]
        print(f"  {m[:100]} — loc {len(locs)} · 하위 {len(subs)} · 맞음 {len(hit)}", flush=True)
        found += hit
        # 하위 사이트맵: 상품 쪽 우선
        subs.sort(key=lambda l: (not re.search(r"product|pdp|item|goods", l, re.I), l))
        todo = subs + todo
    for l in list(dict.fromkeys(found))[:show]:
        print(f"    → {urllib.parse.unquote(l)[:160]}")
    return list(dict.fromkeys(found))


def page_report(url, cur, codepat, pricepat=None):
    r, h, e = tryget(url)
    if not r:
        print(f"  ✗ {url[:110]} {e}", flush=True); return None
    print(f"  {r.status_code} {len(h)//1000}KB {r.url[:120]}", flush=True)
    for l in ld_dump(h)[:6]: print(f"    LD {l}")
    og = re.search(r'<meta[^>]+property="og:title"[^>]+content="([^"]*)"', h)
    if og: print(f"    og:title {og.group(1)[:90]}")
    codes = sorted(set(re.findall(codepat, h)))[:12] if codepat else []
    if codepat: print(f"    품번 후보 {codes}")
    if pricepat:
        for s in snippets(h.replace('\\"', '"'), pricepat, 10): print(f"    가격? {s[:240]}")
    try:
        fp, meta = pf.page_price(h, HINT.get(cur, ""), cur, CODES)
        print(f"    page_price → {fp} {meta}")
    except Exception as ex:
        print(f"    page_price ✗ {ex}")
    return h


HINT, CODES = {}, []


def main():
    global CODES
    # 1) 헌터 — 쇼피파이 3곳 + 코오롱몰
    for base in ("https://hunterboots.com", "https://www.hunterboots.co.uk", "https://hunterboots.co.jp", "https://www.hunterboots.jp"):
        r, h, e = tryget(base + "/")
        print(f"\n# 헌터 홈 {base} → {r.status_code if r else e} {r.url if r else ''}", flush=True)
        if r and "shopify" in h.lower():
            b2 = f"{urllib.parse.urlsplit(r.url).scheme}://{urllib.parse.urlsplit(r.url).netloc}"
            shopify_scan(b2, r"wft1000rma|original[ -]tall|オリジナル\s*トール", 12)
    print("\n# 헌터 코오롱몰", flush=True)
    CODES = ["WFT1000RMA"]; HINT.update({"KRW": "hunter"})
    for k in ("K1760508619617098BK01", "K1760508652696038BK01", "K1760508546483007BK01", "K1760509384102071GR01", "K1760509367990077GR01",
              "K1760509356246099GR01", "K1760333168840025WH01", "K1760511051433082NA01"):
        page_report(f"https://www.kolonmall.com/Brands/HUNTER/Product/{k}", "KRW", r"W[FM]T\d{4}R[A-Z]{2,5}")
    r, h, e = tryget("https://www.kolonmall.com/Brands/HUNTER")
    if r:
        cs = sorted(set(re.findall(r'W[FM]T1000R[A-Z]{2,5}', h)))[:20]
        ks = set(re.findall(r'/Product/(K\d{10,}[A-Z]{2}\d{2})', h))
        print(f"  브랜드관 {len(h)//1000}KB · 품번 {cs} · 상품 링크 {len(ks)}")
        for s in snippets(h, r"WFT1000RMA", 6, 160): print(f"    {s[:330]}")
    # 2) 드래곤디퓨전 한국 상품 JSON-LD 품번
    print("\n# 드래곤디퓨전", flush=True)
    CODES = ["8892", "W2BAS26025DBR"]; HINT.update({"KRW": "santa croce", "USD": "santa croce"})
    page_report("https://www.kolonmall.com/Brands/DRAGON_DIFFUSION/Product/W2BAS26025DBR", "KRW", r"W2BAS\d{5}[A-Z]{3}|8892")
    page_report("https://dragondiffusion.com/products/santa-croce-big-dark-brown-woven-leather-bag-handmade", "USD", r"8892", r'"price(Currency)?"\s*:')
    # 3) 써코니 — 한국 카페24 + 해외 SFCC
    print("\n# 써코니", flush=True)
    kr = sitemap_grep("https://saucony.co.kr/", r"/product/", 4, 400)
    for l in kr[:400]:
        print(f"    KR 상품 {urllib.parse.unquote(l)[:120]}")
    CODES = ["S2044"]; HINT.update({"KRW": "jazz", "USD": "jazz", "GBP": "jazz", "EUR": "jazz"})
    pick = [l for l in kr if re.search(r"jazz|재즈", urllib.parse.unquote(l), re.I)][:3] + \
           [l for l in kr if re.search(r"shadow|섀도우|쉐도우|그리드|grid|omni|옴니", urllib.parse.unquote(l), re.I)][:3]
    for l in pick:
        page_report(l, "KRW", r"S[0-9]{4,5}-[0-9]{1,3}[A-Z]?|S[0-9]{5}")
    for u in ("https://www.saucony.com/en/jazz-original/884401807778.html", "https://www.saucony.com/UK/en_GB/jazz-original/11842M.html",
              "https://www.saucony.com/DE/de_DE/jazz-original/11842M.html"):
        h = page_report(u, {"/en/": "USD", "/UK/": "GBP", "/DE/": "EUR"}[re.search(r"/(en|UK|DE)/", u).group(0)], r"S2044-[0-9]{2,3}",
                        r'(?i)"(list|sales|standard|msrp|original)[_ ]?price"|price-(sales|standard|list)|data-price|itemprop="price"|"price"\s*:\s*\{|c_listPrice|strike')
    sitemap_grep("https://www.saucony.com/en/", r"jazz-original", 6, 10)
    # 4) 브룩스 — 한국 카페24 + 일본 쇼피파이
    print("\n# 브룩스", flush=True)
    r, h, e = tryget("https://brooksrunning.co.kr/")
    if r:
        links = sorted(set(re.findall(r'href="(/product/[^"]+/\d+/[^"]*)"', h)))
        print(f"  KR 홈 상품 링크 {len(links)}: {[urllib.parse.unquote(x)[:60] for x in links[:40]]}")
    kr = sitemap_grep("https://brooksrunning.co.kr/", r"/product/", 4, 300)
    CODES = ["1104421D", "1104931D", "1104191D", "1104491D"]; HINT.update({"KRW": "ghost", "JPY": "ghost"})
    pick = [l for l in kr if "brooksrunning.co.kr" in l and re.search(r"ghost|고스트|glycerin|글리세린", urllib.parse.unquote(l), re.I)][:6]
    for l in pick:
        page_report(l, "KRW", r"11[0-9]{4}1[A-Z][0-9]{3}|12[0-9]{4}1[A-Z][0-9]{3}")
    shopify_scan("https://brooksrunning.co.jp", r"ghost|glycerin|ゴースト|グリセリン", 10)
    # 5) 언더아머 — SFCC 나라별 사이트맵에서 1326413
    print("\n# 언더아머", flush=True)
    CODES = ["1326413"]; HINT.update({"KRW": "tech", "USD": "tech", "GBP": "tech", "EUR": "tech", "MXN": "tech"})
    for home, cur in (("https://www.underarmour.co.kr/ko-kr/", "KRW"), ("https://www.underarmour.co.uk/en-gb/", "GBP"),
                      ("https://www.underarmour.de/de-de/", "EUR"), ("https://www.underarmour.com.mx/es-mx/", "MXN")):
        f = sitemap_grep(home, r"1326413", 14, 6)
        for l in f[:2]:
            page_report(l, cur, r"1326413-[0-9]{3}", r'(?i)"(list|sales)"\s*:\s*\{|price-(sales|standard|list)|"listPrice"|strike')
    page_report("https://www.underarmour.com/en-us/p/shirts_and_tops/ua_tech_2.0/1326413.html", "USD", r"1326413-[0-9]{3}")
    print(f"\n걸린 시간 {time.time() - T0:.0f}초")


if __name__ == "__main__":
    main()

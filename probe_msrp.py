# -*- coding: utf-8 -*-
"""임시 시험(병합 안 함) — 브랜드 공식몰 나라별로 접속·robots·정가 표기(JSON-LD·쇼피파이·SFCC)를 확인해 연동 가능 여부를 가림.
price_fetch의 get()(우리 봇 이름 · robots.txt · 403/429면 그 사이트 그만 · 넘겨짐도 확인)을 그대로 씀. 저장·커밋 안 함."""
import json, re, sys, time, urllib.parse
import price_fetch as pf

pf.GAP = 0.8
CUR = {"KR": "KRW", "US": "USD", "GB": "GBP", "DE": "EUR", "JP": "JPY", "MX": "MXN"}
BLOCK_SIG = re.compile(r"captcha|px-captcha|cf-chl|challenge-platform|access denied|pardon our interruption|datadome|are you a robot|request unsuccessful|incapsula|perimeterx", re.I)
T0 = time.time()


def plat(h):
    p = []
    if "cdn.shopify.com" in h or "Shopify.theme" in h: p.append("shopify")
    if "demandware" in h or "/on/demandware.static/" in h: p.append("sfcc")
    if "__NEXT_DATA__" in h: p.append("next")
    if "Magento" in h or "mage/cookies" in h: p.append("magento")
    return "+".join(p) or "-"


def ld_prices(h, cur):
    """JSON-LD 상품 가격(이 통화) · 정가 명세(ListPrice·Strikethrough) · c_listPrice"""
    offers, lists, names = [], [], set()
    for n in pf._ld_nodes(h):
        if not (pf._types(n) & {"product", "productgroup"}): continue
        names.add(str(n.get("name", ""))[:30])
        st = [n.get("offers"), n.get("hasVariant")]
        while st:
            x = st.pop()
            if isinstance(x, list): st.extend(x); continue
            if not isinstance(x, dict): continue
            if pf._types(x) & {"product"}: st.append(x.get("offers")); continue
            if str(x.get("priceCurrency", cur)) == cur:
                v = pf.num(x.get("price") or x.get("highPrice") or x.get("lowPrice"))
                if v: offers.append(v)
            ps = x.get("priceSpecification")
            for q in (ps if isinstance(ps, list) else [ps]):
                if isinstance(q, dict) and re.search(r"ListPrice|Strikethrough", str(q.get("priceType", ""))):
                    v = pf.num(q.get("price"))
                    if v: lists.append(v)
            if x.get("offers"): st.append(x.get("offers"))
    flat = h.replace('\\"', '"')
    cl = [pf.num(m.group(1)) for m in re.finditer(r'"c_listPrice":([0-9.]+)', flat)][:3]
    return offers, lists, cl, names


def tryget(url):
    try:
        r = pf.get(url)
        h = r.text
        blk = bool(BLOCK_SIG.search(h[:20000])) and len(h) < 60000
        return r, h, ("차단 화면" if blk else "")
    except Exception as e:
        return None, "", str(e)[:70]


def sm_product(home):
    """사이트맵(robots.txt의 Sitemap:)에서 상품 페이지 주소 하나 — 큰 파일은 앞 1.5MB만 읽음(.gz 건너뜀)"""
    import requests
    sp = urllib.parse.urlsplit(home); base = f"{sp.scheme}://{sp.netloc}"
    def small(u):
        ok, why = pf.robots_ok(u)
        if not ok or urllib.parse.urlsplit(u).netloc in pf._BLOCKED: return ""
        w = pf.GAP - (time.time() - pf._LAST[0])
        if w > 0: time.sleep(w)
        pf._LAST[0] = time.time()
        try:
            r = requests.get(u, headers=pf.HDR, timeout=20, stream=True)
            if r.status_code != 200: return ""
            b = b""
            for ch in r.iter_content(65536):
                b += ch
                if len(b) > 1_500_000: break
            r.close(); return b.decode("utf-8", "replace")
        except Exception:
            return ""
    rb = small(base + "/robots.txt")
    maps = re.findall(r"(?im)^\s*sitemap:\s*(\S+)", rb)[:6] or [base + "/sitemap.xml"]
    loc_path = urllib.parse.urlsplit(home).path.rstrip("/")
    for m in maps:
        if m.endswith(".gz"): continue
        x = small(m)
        locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", x)
        subs = [l for l in locs if l.endswith(".xml") and re.search(r"product|pdp|item", l, re.I)]
        if subs:
            subs.sort(key=lambda l: (loc_path not in l, len(l)))
            x = small(subs[0]); locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", x)
        prods = [l for l in locs if not l.endswith(".xml") and re.search(r"/p/|/pd/|/product|/products/|\.html$|/[A-Z0-9]{5,}", l)]
        if loc_path:
            pr2 = [l for l in prods if loc_path in l]
            prods = pr2 or prods
        if prods: return prods[min(3, len(prods) - 1)]
    return ""


def main(path):
    data = json.load(open(path, encoding="utf-8"))
    summary = []
    for b in data:
        name = b["brand"]; ok_cc = []
        print(f"\n### {name}", flush=True)
        shop_hosts = set()
        for s in b.get("stores", []):
            cc, url = s["cc"], s["url"]
            if time.time() - T0 > 32 * 60: print("  (시간 초과 — 남은 것 건너뜀)"); break
            r, h, err = tryget(url)
            if not r:
                print(f"  {cc} 홈 ✗ {err} · {url}"); continue
            pl = plat(h)
            line = f"  {cc} 홈 {r.status_code} {pl} {len(h)//1000}KB" + (f" ⚠{err}" if err else "")
            if "shopify" in pl:
                base = f"{urllib.parse.urlsplit(r.url).scheme}://{urllib.parse.urlsplit(r.url).netloc}"
                r2, h2, e2 = tryget(base + "/products.json?limit=1")
                if r2 is not None:
                    try:
                        pj = json.loads(h2).get("products") or []
                        v = (pj[0].get("variants") or [{}])[0] if pj else {}
                        line += f" · products.json OK(예: {str(pj[0].get('title'))[:20] if pj else '-'} {v.get('price')}/{v.get('compare_at_price')})"
                        shop_hosts.add(cc)
                    except Exception:
                        line += " · products.json 형식 다름"
                else:
                    line += f" · products.json ✗ {e2}"
            if "shopify" not in pl and cc not in ((b.get("product") or {}).get("urls") or {}):
                pu = sm_product(r.url)
                if pu:
                    r4, h4, e4 = tryget(pu)
                    if r4 is not None:
                        offers, lists, cl, names = ld_prices(h4, CUR[cc])
                        line += f" · 사이트맵 상품 {'✓' if (offers or lists or cl) else '✗'} JSON-LD {sorted(set(offers))[:3]} 정가표기 {sorted(set(lists))[:2]} c_list {cl[:1]} ({pu[:70]})"
                        if offers or lists or cl: b.setdefault("_sm_ok", []).append(cc)
                    else:
                        line += f" · 사이트맵 상품 ✗ {e4} ({pu[:60]})"
                else:
                    line += " · 사이트맵 상품 못 찾음"
            print(line, flush=True)
        prod = b.get("product") or {}
        for cc, url in (prod.get("urls") or {}).items():
            if cc not in CUR or not url: continue
            if time.time() - T0 > 32 * 60: break
            r, h, err = tryget(url)
            if not r:
                print(f"  {cc} 상품 ✗ {err} · {url[:90]}"); continue
            offers, lists, cl, names = ld_prices(h, CUR[cc])
            sj = ""
            if "shopify" in plat(h) and "/products/" in r.url:
                r3, h3, e3 = tryget(r.url.split("?")[0] + ".json")
                if r3 is not None:
                    try:
                        vs = json.loads(h3)["product"]["variants"]
                        sj = f" · .json {vs[0].get('price')}/{vs[0].get('compare_at_price')} sku {vs[0].get('sku')}"
                    except Exception: sj = " · .json 형식 다름"
            got = bool(offers or lists or cl or sj)
            if got: ok_cc.append(cc)
            print(f"  {cc} 상품 {r.status_code} {'✓' if got else '✗ 가격 데이터 없음'} JSON-LD {sorted(set(offers))[:4]} 정가표기 {sorted(set(lists))[:3]} c_list {cl}{sj}"
                  f" · {', '.join(list(names)[:2])} · {url[:80]}" + (f" ⚠{err}" if err else ""), flush=True)
        sm = b.get("_sm_ok", [])
        summary.append((name, sorted(set(ok_cc) | set(sm) | shop_hosts), prod.get("code", "")))
    print("\n=== 요약(상품 가격을 읽은 나라) ===")
    for name, ok, code in summary:
        print(f"요약 | {name} | {code} | {','.join(ok) or '-'} | {'KR+' + str(len([c for c in ok if c != 'KR'])) if 'KR' in ok else 'KR 없음'}")
    print(f"걸린 시간 {time.time() - T0:.0f}초")


if __name__ == "__main__":
    main(sys.argv[1])

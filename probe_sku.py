# -*- coding: utf-8 -*-
# 임시 시험(병합하지 않음) — 해외 정가 두바이(UAE 공식몰 · AED) 추가 조사(대표 지시 2026-11-03): robots.txt·사이트맵·상품 페이지 구조 + price_fetch로 정가 읽기 시험
# robots.txt·요청 간격·막힘 처리는 price_fetch.get(우리 봇 이름 · RFC 9309)을 그대로 씀
import gzip, html, json, re, sys, time, urllib.parse
import requests
import price_fetch as pf
pf.MK.setdefault("AE", ("AE", "en-GB", "AED"))   # 시험용(병합하는 price_fetch에는 따로 넣음)
T0 = time.time(); LIMIT = 17 * 60
CHAL = [("cf-chl", r"cf-chl|challenge-platform|Just a moment"), ("akamai", r"Access Denied|errors\.edgesuite|_abck|bm-verify"),
        ("px", r"px-captcha|perimeterx|_pxAppId"), ("datadome", r"datadome|captcha-delivery"), ("captcha", r"captcha|Are you a robot|robot check"),
        ("incapsula", r"_Incapsula_Resource|incap_ses")]
def chal(h): return [k for k, rx in CHAL if re.search(rx, h, re.I)]
def out(kind, **kw): print(kind, json.dumps(kw, ensure_ascii=False), flush=True)
def body(r):
    c = r.content
    if c[:2] == b"\x1f\x8b": c = gzip.decompress(c)
    return c.decode("utf-8", "replace")
def left(): return LIMIT - (time.time() - T0)
SM = {}; CODES = {}
def sitemaps(host):
    if host not in SM:
        try:
            r = pf.get(f"https://{host}/robots.txt")
            SM[host] = [l.split(":", 1)[1].strip() for l in r.text.splitlines() if l.lower().startswith("sitemap:")]
        except Exception as e:
            out("ROBOTSERR", host=host, err=str(e)[:120]); SM[host] = []
    return SM[host]
def codes(j):   # 나라별 사이트맵 → {품번: 주소}, 겹치는 품번
    rx = re.compile(j["rx"]); key = j.get("key", "x"); CODES.setdefault(key, {})
    for cc, site in j["sites"].items():
        if site.get("preset"): continue
        host, pre = site["host"], site.get("path", "/")
        got, seen, queue = {}, 0, list(site.get("start") or sitemaps(host))
        t0 = time.time()
        while queue and seen < j.get("max_maps", 40) and left() > 120 and time.time() - t0 < j.get("per_host", 150):
            sm = queue.pop(0)
            try: r = pf.get(sm); seen += 1
            except Exception as e: out("SMERR", cc=cc, sm=sm[:120], err=str(e)[:120]); continue
            txt = body(r); locs = [html.unescape(x) for x in re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", txt)]   # XML 안 &lt;br&gt; 등을 풂
            if "<sitemapindex" in txt[:3000]:
                kids = [k for k in locs if urllib.parse.urlsplit(k).netloc == host]
                pref = [x.lower() for x in site.get("kid_pref", [])]
                if pref: kids = [k for k in kids if any(x in k.lower() for x in pref)] or kids
                kids.sort(key=lambda u: (not any(k in u.lower() for k in ("product", "pdp", "prod")), u))
                out("INDEX", cc=cc, sm=sm[-90:], n=len(kids), kids=[k[-80:] for k in kids[:6]])
                queue = kids + queue; continue
            for u in locs:
                sp = urllib.parse.urlsplit(u)
                if sp.netloc != host or not sp.path.startswith(pre): continue
                m = rx.search(sp.path)
                if m:
                    old = got.get(m.group(1))
                    if not old or sp.path.count("/") > urllib.parse.urlsplit(old).path.count("/"): got[m.group(1)] = u
        CODES[key][cc] = got
        out("CODES", key=key, cc=cc, host=host, maps_read=seen, n=len(got))
    cs = CODES[key]; base = cs.get(j.get("base", "KR")) or {}
    others = [cc for cc in cs if cc != j.get("base", "KR")]
    rows = [(sum(c in cs[cc] for cc in others), c) for c in base]
    rows.sort(key=lambda r: (-r[0], r[1]))
    out("INTERSECT", key=key, base=len(base), all=sum(1 for r in rows if r[0] == len(others)))
    for t in j.get("targets", []):
        out("TARGET", key=key, code=t, where={cc: urllib.parse.unquote(cs[cc].get(t) or "")[-120:] for cc in cs})
    for n, c in rows[: j.get("show", 0)]:
        print("ROW", json.dumps({"code": c, "n": n, "kr": urllib.parse.unquote(base[c])[-90:],
                                 "miss": [cc for cc in others if c not in cs[cc]]}, ensure_ascii=False), flush=True)
def walk(site, limit_maps=40, per_host=150):   # 사이트맵을 따라가며 (주소) 내놓음
    host = site["host"]; queue = list(site.get("start") or sitemaps(host) or [f"https://{host}/sitemap.xml"]); seen = 0; t0 = time.time()
    while queue and seen < limit_maps and left() > 120 and time.time() - t0 < per_host:
        sm = queue.pop(0)
        try: r = pf.get(sm); seen += 1
        except Exception as e: out("SMERR", host=host, sm=sm[:120], err=str(e)[:120]); continue
        txt = body(r); locs = [html.unescape(x) for x in re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", txt)]
        out("SMAP", host=host, sm=sm[-110:], final=r.url[-110:], kb=len(txt) // 1000, index="<sitemapindex" in txt[:3000], n=len(locs), sample=[x[-120:] for x in locs[: site.get("sample", 3)]])
        if "<sitemapindex" in txt[:3000]:
            kids = [k for k in locs if urllib.parse.urlsplit(k).netloc == host or site.get("any_host")]
            pref = [x.lower() for x in site.get("kid_pref", [])]
            if pref: kids = [k for k in kids if any(x in k.lower() for x in pref)] or kids
            kids.sort(key=lambda u: (not any(k in u.lower() for k in ("product", "pdp", "prod")), u))
            queue = kids + queue; continue
        for u in locs:
            yield u
def grep(j):   # 사이트맵에서 정규식에 맞는 상품 주소(풀어 쓴 주소 기준)
    rx = re.compile(j["rx"], re.I)
    for name, site in j["sites"].items():
        hits = []
        for u in walk(site, j.get("max_maps", 40), j.get("per_host", 150)):
            d = urllib.parse.unquote(u)
            if rx.search(d) and d not in hits: hits.append(d)
        out("GREP", site=name, n=len(hits), hits=hits[: j.get("show", 40)])
def pages(j):   # 페이지를 받아 제목·JSON-LD 이름·가격·품번 후보·상품 링크를 보여 줌
    for u in j["urls"]:
        if left() < 60: out("TIMEOUT"); return
        try:
            r = pf.get(u); h = r.text
        except Exception as e:
            out("PAGEERR", url=u[:150], err=f"{type(e).__name__}: {str(e)[:160]}"); continue
        og = re.search(r'<meta[^>]+property="og:title"[^>]+content="([^"]*)"', h)
        names = re.findall(r'"name"\s*:\s*"([^"]{4,120})"', h)[:6]
        prices = re.findall(r'"price"\s*:\s*"?([0-9.,]+)', h)[:6]
        codes = sorted(set(re.findall(j.get("code_rx", r"$^"), h)))[:20]
        links = []
        if j.get("link_rx"):
            for m in re.finditer(j["link_rx"], h):
                v = m.group(0)
                if v not in links: links.append(v)
        snips = []
        for rx in j.get("snip_rx", []):
            for m in list(re.finditer(rx, h))[:4]:
                snips.append(h[max(0, m.start() - 160): m.end() + 160].replace("\n", " "))
        out("PAGE", url=urllib.parse.unquote(u)[-120:], status=r.status_code, kb=len(h) // 1000, og=og.group(1)[:120] if og else None,
            names=names, prices=prices, codes=codes, links=links[: j.get("show", 60)], snips=snips)

def shopjson(j):   # 쇼피파이 몰 /products.json 쪽마다 → 상품 이름·handle·변형 품번·가격 · 품번 앞 8자리를 CODES[key][cc]에 넣음(다음 codes 작업에서 대조)
    key = j.get("key", "x"); cc = j.get("cc", "KR"); CODES.setdefault(key, {}).setdefault(cc, {})
    for u in j["urls"]:
        if left() < 60: out("TIMEOUT"); return
        try:
            r = pf.get(u); d = r.json()
        except Exception as e:
            out("PAGEERR", url=u[:150], err=f"{type(e).__name__}: {str(e)[:160]}"); continue
        ps = d.get("products") or []
        out("SHOPPAGE", url=u[-60:], n=len(ps))
        base = u.split("/products.json")[0]
        for pr in ps:
            vs = pr.get("variants") or []
            tg = pr.get("tags") if isinstance(pr.get("tags"), list) else str(pr.get("tags") or "").split(",")
            skus = sorted({str(v.get("sku") or "") for v in vs} | ({str(t).strip() for t in tg} if j.get("tags") else set()))
            m = [re.match(j.get("sku_rx", r"(\d{8})"), x) for x in skus]
            codes8 = sorted({x.group(1) for x in m if x})
            for c in codes8: CODES[key][cc].setdefault(c, f"{base}/products/{pr.get('handle')}.json")
            if j.get("show", True):
                print("SP", json.dumps({"h": pr.get("handle"), "t": (pr.get("title") or "")[:60], "c": codes8[:3], "p": [vs[0].get("price"), vs[0].get("compare_at_price")] if vs else None,
                                        "ty": pr.get("product_type")}, ensure_ascii=False), flush=True)
def tryp(j):   # 완성된 상품 정의(PRODUCTS 모양)로 나라별 정가 읽기 시험 — "ids"면 이 브랜치 price_fetch의 PRODUCTS 그대로(나라는 "only" 또는 pf.ccs)
    byid = {p["id"]: p for p in pf.PRODUCTS}
    jobs = [(p, None) for p in j.get("prods", [])] + [(byid[i], it.get("only")) for it in j.get("ids", []) for i in it["ids"]]
    for prod, only in jobs:
        for cc in (only or (pf.ccs(prod) if hasattr(pf, "ccs") else (prod["cc"] if prod["src"] == "nike" else list(prod["urls"])))):
            if cc not in pf.ccs(prod) if hasattr(pf, "ccs") else False: continue
            if left() < 30: out("TIMEOUT"); return
            t = time.time()
            try:
                (full, extra), src = pf.fetch_one(prod, cc)
                out("OK", id=prod["id"], cc=cc, full=full, cur=pf.MK[cc][2], extra=extra, t=round(time.time() - t, 1), src=src[-80:])
            except Exception as e:
                out("FAIL", id=prod["id"], cc=cc, err=f"{type(e).__name__}: {str(e)[:200]}", t=round(time.time() - t, 1))
def try_codes(j):   # 후보 품번을 나라별 주소로 price_fetch에 넣어 정가 읽기 시험
    cs = CODES.get(j.get("key", "x"), {})
    for cand in j["cands"]:
        code = cand["code"]; urls = {cc: cs.get(cc, {}).get(code) for cc in j["ccs"]}
        urls = {cc: u for cc, u in urls.items() if u}
        prod = {"id": "try-" + code, "brand": j.get("brand", ""), "name": cand.get("name", code), "code": code, "src": "page",
                "hint": cand.get("hint", ""), "urls": urls}
        out("TRY", code=code, urls={cc: urllib.parse.unquote(u)[-110:] for cc, u in urls.items()}, missing=[cc for cc in j["ccs"] if cc not in urls])
        for cc in urls:
            if left() < 30: out("TIMEOUT"); return
            try:
                (full, extra), src = pf.fetch_one(prod, cc)
                out("OK", code=code, cc=cc, full=full, cur=pf.MK[cc][2], extra=extra)
            except Exception as e:
                out("FAIL", code=code, cc=cc, err=f"{type(e).__name__}: {str(e)[:160]}")
def jsfollow(j):   # 페이지의 스크립트(src)를 받아 정규식에 맞는 글(목록을 받아 오는 주소 등)을 보여 줌
    for u in j["urls"]:
        try:
            h = pf.get(u).text
        except Exception as e:
            out("PAGEERR", url=u[:150], err=str(e)[:160]); continue
        base = "{0.scheme}://{0.netloc}".format(urllib.parse.urlsplit(u))
        srcs = []
        for s in re.findall(r'src="([^"]+\.js[^"]*)"', h):
            s = html.unescape(s); s = s if s.startswith("http") else base + s
            if urllib.parse.urlsplit(s).netloc == urllib.parse.urlsplit(u).netloc and s not in srcs and re.search(j.get("src_rx", "."), s): srcs.append(s)
        out("SRCS", url=u[-60:], n=len(srcs))
        for s in srcs[: j.get("max_js", 60)]:
            if left() < 60: out("TIMEOUT"); return
            try:
                t = pf.get(s).text
            except Exception as e:
                out("JSERR", js=s[-80:], err=str(e)[:120]); continue
            hits = []
            for m in re.finditer(j["rx"], t):
                v = t[max(0, m.start() - j.get("pad", 0)): m.end() + j.get("pad", 0)]
                if v not in hits: hits.append(v)
            if hits: out("JS", js=s.split("/chunks/")[-1][:90], kb=len(t) // 1000, hits=hits[: j.get("show", 30)])
def rxpage(j):   # 페이지를 받아 정규식(들)에 맞는 글을 모두(중복 없이) 보여 줌
    for u in j["urls"]:
        if left() < 60: out("TIMEOUT"); return
        try:
            r = pf.get(u); h = r.text
        except Exception as e:
            out("PAGEERR", url=u[:150], err=f"{type(e).__name__}: {str(e)[:160]}"); continue
        for rx in j["rx"]:
            hits = []
            for m in re.finditer(rx, h):
                v = m.groups() if m.groups() else m.group(0)
                v = [html.unescape(x or "")[:120] for x in v] if isinstance(v, tuple) else html.unescape(v)[:200]
                if v not in hits: hits.append(v)
            out("RX", url=urllib.parse.unquote(u)[-100:], status=r.status_code, kb=len(h) // 1000, rx=rx[:40], n=len(hits), hits=hits[: j.get("max", 80)])
def ae_list(h, offers):   # 시험: SFRA 취소선 정가 — <span class="value" content="799.00"> (글자 대신 content 속성) · 곁 판매가 칸이 이 상품 판매가와 같을 때만
    lps, pairs = set(), []
    for m in re.finditer(r'class="strike-through list"[^>]*>\s*(?:<(?!span class="value")[^>]+>\s*)*<span class="value"[^>]*?content="([0-9][0-9.,]*)"', h):
        back = h[max(0, m.start() - 600):m.start()]; k = back.rfind('class="sales')
        seg = back[k:] if k >= 0 else h[m.end():m.end() + 900]
        sm = re.search(r'class="sales[^"]*"(?:(?!strike-through).)*?<span class="value"[^>]*?content="([0-9][0-9.,]*)"', seg, re.S)
        lp, sv = pf.num(m.group(1)), pf.num(sm.group(1)) if sm else None
        pairs.append((lp, sv, "back" if k >= 0 else "fwd"))
        if lp and sv and any(abs(sv - o) < 0.01 for o in offers) and sv <= lp <= sv * 5:
            lps.add(lp)
    return lps, pairs
def aepage(j):   # 두바이 SFCC 상품 페이지(나이키·언더아머): price_fetch 읽기 + 취소선 정가(content) 시험 + 품번 표시 + 시험용 원문 조각
    for it in j["items"]:
        if left() < 60: out("TIMEOUT"); return
        u, code = it["url"], it["code"]
        try:
            r = pf.get(u); h = r.content.decode("utf-8", "replace")
        except Exception as e:
            out("AEERR", url=u[-90:], code=code, err=f"{type(e).__name__}: {str(e)[:200]}"); continue
        try:
            full, extra = pf.page_price(h, it.get("hint", ""), "AED", [code])
            pp = {"full": full, **extra}
        except Exception as e:
            pp = {"err": f"{type(e).__name__}: {str(e)[:160]}"}
        offers = [pf.num(x) for x in re.findall(r'"priceCurrency":"AED","price":"?([0-9.]+)', h)]
        lps, pairs = ae_list(h, [o for o in offers if o])
        gtm = re.findall(r'data-gtm-event-label="([^"]*\|\|[^"]*(?:price|Price)[^"]*)"', h)[:3]
        orig = sorted(set(re.findall(r'item_original_price&quot;:([0-9.]+)', h)))[:5]
        style = re.findall(r'Style(?: #)?:\s*([A-Z0-9-]+)', h)
        member = re.findall(r'data-producttype-memberonly="([a-z]+)"', h)[:2]
        avail = [a.rsplit("/", 1)[-1] for a in re.findall(r'"availability":"([^"]+)"', h)[:2]]
        sold = bool(re.search(r'availability__out-of-stock|Sold out|Out of stock', h))
        vg = re.findall(r'data-variation-group-id="([^"]+)"', h)[:3]
        out("AE", url=urllib.parse.unquote(u)[-90:], final=r.url[-90:], status=r.status_code, code=code, kb=len(h) // 1000, chal=chal(h), pf=pp, ld_offers=offers[:4],
            strike=sorted(lps), pairs=pairs[:4], gtm=gtm, orig=orig, style=sorted(set(style))[:6], code_in_style=code in style, member=member, vg=vg, avail=avail, sold=sold)
        if it.get("frag"):
            lds = [b for b in ld_blocks(h) if '"Product"' in b]
            i = h.find('class="prices'); 
            out("FRAG", url=u, code=code, ld=lds[0][:4000] if lds else None,
                price=h[max(0, i - 200): i + 2400] if i >= 0 else None,
                style=[h[max(0, m.start() - 250): m.end() + 120] for m in list(re.finditer(r'Style(?: #)?:\s*' + re.escape(code.split("-")[0]), h))[:1]],
                pid=[h[max(0, m.start() - 300): m.end() + 500] for m in list(re.finditer(r'data-variation-group-id=', h))[:1]])
def shopstats(j):   # 쇼피파이 /products.json 쪽 — 할인 표시(compare_at_price) 쓰는지 · 같은 모델 색상별 가격 차이
    for u in j["urls"]:
        if left() < 60: out("TIMEOUT"); return
        try:
            d = pf.get(u).json()
        except Exception as e:
            out("SHOPERR", url=u, err=f"{type(e).__name__}: {str(e)[:160]}"); continue
        ps = d.get("products") or []
        n_cmp = n_var = 0; diff = []
        for p in ps:
            vs = p.get("variants") or []; n_var += len(vs)
            n_cmp += sum(1 for v in vs if pf.num(v.get("compare_at_price")) and pf.num(v.get("compare_at_price")) > (pf.num(v.get("price")) or 0))
            by = {}
            for v in vs:
                by.setdefault(str(v.get("sku", ""))[:11], set()).add(v.get("price"))
            prices = sorted({pf.num(x) for xs in by.values() for x in xs if pf.num(x)})
            if len(prices) > 1:
                diff.append({"h": p.get("handle"), "prices": prices[:6], "cmp": sorted({str(v.get("compare_at_price")) for v in vs})[:4]})
        out("SHOPSTATS", url=u, products=len(ps), variants=n_var, with_compare_at=n_cmp, multi_price=len(diff), sample=diff[: j.get("show", 25)])

MARK = r'product-tile|c-product-tile|b-product-tile|recommend|einstein|carousel|b-pdp__priceline|product-detail__priceline|b-microproduct__price|data-gtm-onload="pdpView"|js-product-detail|quickview|minicart|set-item|bundle'
def aescope(j):   # 취소선 정가가 어느 칸(이 상품 가격 칸 · 추천 상품 칸)에 있는지 + 이 상품 GTM 상세(data-gtm-enhance-commerce-details)
    for it in j["items"]:
        if left() < 60: out("TIMEOUT"); return
        u, code = it["url"], it["code"]
        try:
            r = pf.get(u); h = r.content.decode("utf-8", "replace")
        except Exception as e:
            out("AEERR", url=u[-90:], err=f"{type(e).__name__}: {str(e)[:200]}"); continue
        main = [m.start() for m in re.finditer(r'data-variation-group-id="', h)]
        marks = {}
        for m in re.finditer(MARK, h):
            marks.setdefault(m.group(0), []).append(m.start())
        rows = []
        for m in re.finditer(r'class="strike-through list"[^>]*>\s*(?:<(?!span class="value")[^>]+>\s*)*<span class="value"[^>]*?content="([0-9][0-9.,]*)"', h):
            back = h[max(0, m.start() - 4000):m.start()]
            near = [(x.group(0), m.start() - (max(0, m.start() - 4000) + x.start())) for x in re.finditer(MARK, back)][-3:]
            k = h[max(0, m.start() - 600):m.start()].rfind('class="sales')
            seg = h[max(0, m.start() - 600):m.start()][k:] if k >= 0 else h[m.end():m.end() + 900]
            sm = re.search(r'class="sales[^"]*"(?:(?!strike-through).)*?<span class="value"[^>]*?content="([0-9][0-9.,]*)"', seg, re.S)
            rows.append({"at": m.start(), "lp": m.group(1), "sv": sm.group(1) if sm else None, "near": near})
        det = []
        for m in re.finditer(r'data-variation-group-id="([^"]+)"[^>]*?data-gtm-enhance-commerce-details="([^"]*)"', h, re.S):
            try:
                d = json.loads(html.unescape(m.group(2)))
                prods = (((d.get("ecommerce") or {}).get("detail") or {}).get("products") or [])
                det.append({"vg": m.group(1), "n": len(prods), "p0": {k: prods[0].get(k) for k in ("item_id", "item_variant_id", "price", "item_original_price", "discount", "item_name")} if prods else None})
            except Exception as e:
                det.append({"vg": m.group(1), "err": str(e)[:80], "raw": html.unescape(m.group(2))[:300]})
        out("SCOPE", url=urllib.parse.unquote(u)[-80:], code=code, kb=len(h) // 1000, main=main[:3], first_marks={k: v[:4] for k, v in marks.items()}, strikes=rows[:12], detail=det[:2])
        if it.get("tag"):
            for m in list(re.finditer(r'<div[^>]*?data-variation-group-id="[^"]*"[^>]*>', h, re.S))[:1]:
                out("TAG", url=u, body=m.group(0)[:9000])
            i = h.find('class="prices js-gtm-price')
            out("MAINPRICE", url=u, body=h[max(0, i - 1500): i + 1800] if i >= 0 else None)
        for k in it.get("frag_at", []):
            if k < len(rows):
                a = rows[k]["at"]
                out("FRAGAT", url=u, i=k, body=h[max(0, a - it.get("pre", 1800)): a + it.get("post", 900)])

def net(j):   # 연결 진단(SKU 8차): DNS · TCP 443/80 · TLS · robots.txt(우리 봇 이름 · 넘겨짐 안 따라감) — 상품 페이지는 받지 않음
    import socket, ssl, requests
    try:
        import logistics_fetch as lf
        out("RUNNER", where=lf.runner_where())
    except Exception as e:
        out("RUNNER", err=str(e)[:120])
    for host in j["hosts"]:
        r = {"host": host}
        try:
            r["dns"] = sorted({a[4][0] for a in socket.getaddrinfo(host, 443, proto=socket.IPPROTO_TCP)})[:6]
        except Exception as e:
            r["dns_err"] = f"{type(e).__name__}: {e}"[:160]; out("NET", **r); continue
        for ip in r["dns"][:2]:
            for port in (443, 80):
                t0 = time.time()
                try:
                    s = socket.create_connection((ip, port), timeout=10)
                    r[f"tcp{port}_{ip}"] = f"ok {time.time() - t0:.2f}s"
                    if port == 443:
                        try:
                            ss = ssl.create_default_context().wrap_socket(s, server_hostname=host)
                            r[f"tls_{ip}"] = f"{ss.version()} {ss.getpeercert().get('subject')}"[:160]; ss.close()
                        except Exception as e:
                            r[f"tls_{ip}"] = f"{type(e).__name__}: {e}"[:160]; s.close()
                    else:
                        s.close()
                except Exception as e:
                    r[f"tcp{port}_{ip}"] = f"{type(e).__name__}: {e}"[:160] + f" ({time.time() - t0:.1f}s)"
        for scheme in ("https", "http"):
            try:
                rr = requests.get(f"{scheme}://{host}/robots.txt", headers={"User-Agent": pf.UA}, timeout=(10, 20), allow_redirects=False)
                r[f"robots_{scheme}"] = f"{rr.status_code} loc={rr.headers.get('location', '')[:100]} {len(rr.content)}B server={rr.headers.get('server', '')[:40]}"
            except Exception as e:
                r[f"robots_{scheme}"] = f"{type(e).__name__}: {str(e)[:200]}"
        out("NET", **r)
def robots(j):   # 사이트의 robots.txt 사이트맵 줄
    for host in j["hosts"]:
        out("ROBOTS", host=host, sitemaps=sitemaps(host))
def robotsraw(j):   # robots.txt 원문(넘겨짐은 하나씩 보여 줌 · robots.txt만 — 상품 페이지는 pf.get으로)
    for host in j["hosts"]:
        u = f"https://{host}/robots.txt"
        for hop in range(4):
            try:
                r = requests.get(u, headers=pf.HDR, timeout=20, allow_redirects=False)
            except Exception as e:
                out("ROBOTSRAW", url=u, err=f"{type(e).__name__}: {str(e)[:200]}"); break
            hd = {k: v[:160] for k, v in r.headers.items() if k.lower() in ("location", "server", "content-type", "content-length", "x-cache", "cf-ray", "x-akamai-transformed", "via", "x-powered-by", "x-shopid", "x-sorting-hat-shopid", "powered-by", "x-dw-request-base-id")}
            t = r.content.decode("utf-8", "replace")
            out("ROBOTSRAW", url=u, hop=hop, status=r.status_code, hdr=hd, chal=chal(t), cookies=sorted(r.cookies.keys())[:12], body=t[: j.get("max", 4000)])
            loc = r.headers.get("Location") if 300 <= r.status_code < 400 else None
            if not loc: break
            u = urllib.parse.urljoin(u, loc)
def nikefeed(j):   # 나이키 상품 정보(product_feed)를 나라·언어 조합으로
    for m, l in j["combos"]:
        for s_ in j["codes"]:
            u = pf.NIKE_FEED.format(m=m, l=l, s=s_)
            try:
                r = pf.get(u); d = r.json()
            except Exception as e:
                out("NIKEFEED", m=m, l=l, code=s_, err=f"{type(e).__name__}: {str(e)[:200]}"); continue
            objs = [o for o in d.get("objects") or [] if isinstance(o, dict)]
            got = []
            for o in objs:
                for pi in o.get("productInfo") or []:
                    mp, mer = pi.get("merchPrice") or {}, pi.get("merchProduct") or {}
                    got.append({"sc": mer.get("styleColor"), "cur": mp.get("currency"), "full": mp.get("fullPrice"), "now": mp.get("currentPrice"), "st": mer.get("status")})
            out("NIKEFEED", m=m, l=l, code=s_, status=r.status_code, n=len(objs), keys=sorted(d.keys())[:8], got=got[:4], pages=d.get("pages"))
def ld_blocks(h):
    return [m.group(1).strip() for m in re.finditer(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', h, re.S | re.I)]
def dump(j):   # 페이지 구조 공부: 상태·최종 주소·막힘 표시·JSON-LD 원문·정규식 둘레 원문(그대로)·앞부분
    for u in j["urls"]:
        if left() < 60: out("TIMEOUT"); return
        try:
            r = pf.get(u); h = r.content.decode("utf-8", "replace")
        except Exception as e:
            out("DUMPERR", url=u[:200], err=f"{type(e).__name__}: {str(e)[:200]}"); continue
        hd = {k: v[:160] for k, v in r.headers.items() if k.lower() in ("server", "content-type", "x-cache", "cf-ray", "via", "x-powered-by", "x-shopid", "powered-by", "set-cookie")}
        ti = re.search(r"<title[^>]*>(.*?)</title>", h, re.S)
        out("DUMP", url=u, final=r.url, status=r.status_code, kb=len(h) // 1000, chal=chal(h), title=(ti.group(1).strip()[:160] if ti else None), hdr=hd)
        for i, b in enumerate(ld_blocks(h)[: j.get("max_ld", 6)]):
            out("LD", url=u[-80:], i=i, n=len(b), body=b[: j.get("ld_chars", 6000)])
        for rx in j.get("ctx", []):
            ms = list(re.finditer(rx, h))
            for m in ms[: j.get("per_rx", 3)]:
                pad = j.get("pad", 400)
                out("CTX", url=u[-80:], rx=rx[:50], n=len(ms), at=m.start(), body=h[max(0, m.start() - pad): m.end() + pad])
        if j.get("head"):
            out("HEAD", url=u[-80:], body=h[: j["head"]])
def shopprod(j):   # 쇼피파이 상품 .json — 변형 품번·바코드·가격·태그·body 안 품번 후보
    for u in j["urls"]:
        if left() < 60: out("TIMEOUT"); return
        try:
            r = pf.get(u); d = r.json()
        except Exception as e:
            out("SHOPERR", url=u[:200], err=f"{type(e).__name__}: {str(e)[:200]}"); continue
        p = d.get("product") or {}
        vs = p.get("variants") or []
        body_codes = sorted(set(re.findall(j.get("code_rx", r"3M[A-Z]\d{8}"), json.dumps(p))))[:20]
        out("SHOPPROD", url=u, final=r.url, status=r.status_code, handle=p.get("handle"), title=p.get("title"), vendor=p.get("vendor"), type=p.get("product_type"),
            tags=(p.get("tags") if isinstance(p.get("tags"), str) else ",".join(p.get("tags") or []))[:600], n_var=len(vs),
            var=[{k: v.get(k) for k in ("sku", "barcode", "price", "compare_at_price", "price_currency", "title", "option1", "option2")} for v in vs[:6]],
            opts=[(o.get("name"), (o.get("values") or [])[:8]) for o in p.get("options") or []], codes=body_codes)
        if j.get("raw"):
            q = dict(p); q.pop("body_html", None); q.pop("images", None); q.pop("image", None); q.pop("media", None)
            q["variants"] = [v for v in vs if any(w.lower() in str(v.get("sku", "")).lower() for w in j.get("want", []))][:3] + vs[:2]
            out("SHOPRAW", url=u, json=json.dumps({"product": q}, ensure_ascii=False)[:6000])
        for w in j.get("want", []):
            m = [v for v in vs if w.lower() in str(v.get("sku", "")).lower()]
            if m:
                out("WANT", url=u[-60:], code=w, n=len(m), prices=sorted({v.get("price") for v in m}), cmp=sorted({str(v.get("compare_at_price")) for v in m}),
                    curs=sorted({str(v.get("price_currency")) for v in m}), titles=[v.get("title") for v in m[:3]], skus=[v.get("sku") for v in m[:3]], avail=sum(1 for v in m if v.get("available")))
if __name__ == "__main__":
    pf.log = lambda m: print("  log:", m, flush=True)
    for j in json.load(open(sys.argv[1])):
        if left() < 30: print("시간 제한 — 남은 작업 건너뜀"); break
        {"net": net, "codes": codes, "try": try_codes, "grep": grep, "pages": pages, "tryp": tryp, "shopjson": shopjson, "jsfollow": jsfollow, "rxpage": rxpage, "robots": robots,
         "robotsraw": robotsraw, "nikefeed": nikefeed, "dump": dump, "shopprod": shopprod, "aepage": aepage, "shopstats": shopstats, "aescope": aescope}[j["t"]](j)
    print(f"끝 {int(time.time()-T0)}초")

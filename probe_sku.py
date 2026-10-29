# -*- coding: utf-8 -*-
# 임시 시험(병합하지 않음) — 해외 정가 SKU 늘리기(대표 상시 지시 2026-10-26): 나라별 몰 사이트맵에서 같은 품번 상품 찾기 + price_fetch로 정가 읽기 시험
# robots.txt·요청 간격·막힘 처리는 price_fetch.get(우리 봇 이름 · RFC 9309)을 그대로 씀
import gzip, html, json, re, sys, time, urllib.parse
import price_fetch as pf
T0 = time.time(); LIMIT = 17 * 60
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
    host = site["host"]; queue = list(site.get("start") or sitemaps(host)); seen = 0; t0 = time.time()
    while queue and seen < limit_maps and left() > 120 and time.time() - t0 < per_host:
        sm = queue.pop(0)
        try: r = pf.get(sm); seen += 1
        except Exception as e: out("SMERR", host=host, sm=sm[:120], err=str(e)[:120]); continue
        txt = body(r); locs = [html.unescape(x) for x in re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", txt)]
        if "<sitemapindex" in txt[:3000]:
            kids = [k for k in locs if urllib.parse.urlsplit(k).netloc == host]
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
def tryp(j):   # 완성된 상품 정의(PRODUCTS 모양)로 나라별 정가 읽기 시험
    for prod in j["prods"]:
        for cc in (prod["cc"] if prod["src"] == "nike" else list(prod["urls"])):
            if left() < 30: out("TIMEOUT"); return
            try:
                (full, extra), src = pf.fetch_one(prod, cc)
                out("OK", id=prod["id"], cc=cc, full=full, cur=pf.MK[cc][2], extra=extra)
            except Exception as e:
                out("FAIL", id=prod["id"], cc=cc, err=f"{type(e).__name__}: {str(e)[:200]}")
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
if __name__ == "__main__":
    pf.log = lambda m: print("  log:", m, flush=True)
    for j in json.load(open(sys.argv[1])):
        if left() < 30: print("시간 제한 — 남은 작업 건너뜀"); break
        {"codes": codes, "try": try_codes, "grep": grep, "pages": pages, "tryp": tryp, "shopjson": shopjson, "jsfollow": jsfollow}[j["t"]](j)
    print(f"끝 {int(time.time()-T0)}초")

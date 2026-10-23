# -*- coding: utf-8 -*-
# 임시 시험(병합하지 않음) — 브랜드별 대표 상품 늘리기(대표 지시 2026-10-22 '브랜드별 5개 이상'): 나라별 같은 품번 상품 주소 찾기 + price_fetch로 정가 읽기 시험
# robots.txt·요청 간격·막힘 처리는 price_fetch.get(우리 봇 이름 · RFC 9309)을 그대로 씀
import gzip, json, re, sys, time, urllib.parse, requests
import price_fetch as pf
T0 = time.time(); LIMIT = 17 * 60
def out(kind, **kw): print(kind, json.dumps(kw, ensure_ascii=False), flush=True)
def body(r):
    c = r.content
    if c[:2] == b"\x1f\x8b": c = gzip.decompress(c)
    return c.decode("utf-8", "replace")
def left(): return LIMIT - (time.time() - T0)
SM = {}
def sitemaps(host):
    if host not in SM:
        try:
            r = requests.get(f"https://{host}/robots.txt", headers=pf.HDR, timeout=20)
            SM[host] = [l.split(":", 1)[1].strip() for l in r.text.splitlines() if l.lower().startswith("sitemap:")] if r.status_code == 200 else []
        except Exception: SM[host] = []
    return SM[host]
def sitemap_find(j):
    host, pats, want = j["host"], [p.lower() for p in j["pats"]], j.get("want", 2)
    found = {p: [] for p in pats}; seen = 0; queue = list(j.get("start") or sitemaps(host)); prefer = j.get("prefer") or []
    while queue and seen < j.get("max_maps", 40) and left() > 60:
        sm = queue.pop(0)
        try: r = pf.get(sm); seen += 1
        except Exception as e: out("SMERR", host=host, sm=sm[:120], err=str(e)[:120]); continue
        txt = body(r); locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", txt)
        if "<sitemapindex" in txt[:3000]:
            kids = sorted(locs, key=lambda u: (not any(k in u.lower() for k in prefer), u)) if prefer else locs
            queue = kids + queue; continue
        for u in locs:
            ul = urllib.parse.unquote(u).lower()
            for p in pats:   # 'a&&b' = 둘 다 들어 있어야
                if all(q in ul for q in p.split("&&")) and len(found[p]) < want and u not in found[p]: found[p].append(u)
        if all(len(v) >= want for v in found.values()): break
    out("SITEMAP", host=host, read=seen, found=found)
def shopify_list(j):
    host, pats = j["host"], [p.lower() for p in j["pats"]]
    for page in range(1, j.get("pages", 4) + 1):
        if left() < 60: break
        try: d = pf._json(pf.get(f"https://{host}/products.json?limit=250&page={page}"))
        except Exception as e: out("SHOPERR", host=host, page=page, err=str(e)[:150]); return
        ps = d.get("products") or []
        for p in ps:
            skus = [str(v.get("sku") or "") for v in p.get("variants") or []]
            blob = (p.get("handle", "") + " " + p.get("title", "") + " " + " ".join(skus) + " " + str(p.get("tags", ""))).lower()
            hit = [q for q in pats if q in blob]
            if hit or j.get("all"):
                vs = p.get("variants") or []
                out("SHOP", host=host, hit=hit, handle=p.get("handle"), title=str(p.get("title"))[:70], sku=skus[:3],
                    price=sorted({(v.get("price"), v.get("compare_at_price")) for v in vs})[:3], cur=(vs[0].get("price_currency") if vs else None))
        if len(ps) < 250: break
def fetch(j):
    for prod in j["prods"]:
        if left() < 30: out("TIMEOUT"); return
        ccs = prod.get("cc") if prod.get("src") == "nike" else list((prod.get("urls") or {}).keys())
        for cc in ccs:
            try:
                (full, extra), src = pf.fetch_one(prod, cc)
                out("OK", id=prod["id"], cc=cc, full=full, cur=pf.MK[cc][2], extra=extra, src=src[:110])
            except Exception as e:
                out("FAIL", id=prod["id"], cc=cc, err=f"{type(e).__name__}: {str(e)[:160]}")
def page(j):   # 상품 페이지 원문에서 품번·가격 단서 보기(이름 찾기용)
    for u in j["urls"]:
        if left() < 30: return
        try: r = pf.get(u)
        except Exception as e: out("PAGEERR", url=u[:120], err=str(e)[:120]); continue
        t = r.text; codes = sorted(set(re.findall(j.get("rx", r"[A-Z0-9]{2,}[0-9][A-Z0-9.\-]{2,}"), t)))[:25]
        out("PAGE", url=u[:120], final=r.url[:120], codes=codes, title=(re.search(r"<title>(.*?)</title>", t, re.S) or [None, ""])[1].strip()[:80])
def grep(j):   # 페이지 원문에서 정규식 찾기(상품 목록 페이지의 상품 링크·품번)
    for u in j["urls"]:
        if left() < 30: return
        try: r = pf.get(u)
        except Exception as e: out("GREPERR", url=u[:120], err=str(e)[:120]); continue
        t = r.text; hits = []
        for rx in j["rx"]:
            for m in re.finditer(rx, t):
                g = "|".join(x or "" for x in m.groups()) if m.groups() else m.group(0)
                if g not in hits: hits.append(g)
                if len(hits) >= j.get("max", 60): break
        out("GREP", url=urllib.parse.unquote(u)[:120], n=len(t), hits=[urllib.parse.unquote(h)[:140] for h in hits])
def shopjson(j):   # 쇼피파이 상품 .json — 변형 품번·가격·통화 보기
    for u in j["urls"]:
        if left() < 30: return
        try: d = pf._json(pf.get(u))
        except Exception as e: out("SJERR", url=u[:120], err=str(e)[:150]); continue
        p = d.get("product") or {}; vs = p.get("variants") or []
        out("SJ", url=u[:110], handle=p.get("handle"), title=str(p.get("title"))[:70], vendor=p.get("vendor"), n=len(vs),
            sku=sorted({str(v.get("sku")) for v in vs})[:6], price=sorted({(v.get("price"), v.get("compare_at_price"), v.get("price_currency")) for v in vs})[:4],
            tags=str(p.get("tags"))[:200], body=re.sub(r"<[^>]+>", " ", str(p.get("body_html")))[:300])
def fetchb(j):   # price_fetch.PRODUCTS 중 고른 브랜드만 실제 수집 코드로
    fetch({"prods": [p for p in pf.PRODUCTS if p["brand"] in j["brands"]]})
KEYS = ["regularPrice", "listPrice", "originalPrice", "basePrice", "compare_at_price", "compareAtPrice", "strikethrough", "fullPrice", "salePrice", "c_listPrice", "c_salePrice", "ListPrice", "StrikethroughPrice", "priceSpecification"]
def detail(j):   # 정가 칸 위치 보기: JSON-LD 가격·정가 명세, 정가 낱말 주변
    for u in j["urls"]:
        if left() < 30: return
        try: r = pf.get(u)
        except Exception as e: out("DETERR", url=u[:120], err=str(e)[:120]); continue
        t = r.text; ld = []
        for m in re.finditer(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', t, re.S | re.I):
            sx = m.group(1)
            for k in ("price", "priceSpecification", "priceType", "sku", "mpn"):
                for mm in list(re.finditer(rf'"{k}"\s*:', sx))[:3]: ld.append(sx[mm.start():mm.start()+130])
        kv = {}
        for k in KEYS + j.get("near", []):
            occ = [mm.start() for mm in re.finditer(re.escape(k), t)]
            if occ: kv[k] = [len(occ)] + [t[max(0, i-50):i+100] for i in occ[:2]]
        out("DETAIL", url=urllib.parse.unquote(u)[:110], ld=ld[:8], keys=kv)
def snip(j):   # 키워드 주변 글자(페이지 구조 파악용)
    for u in j["urls"]:
        if left() < 30: return
        try: r = pf.get(u)
        except Exception as e: out("SNIPERR", url=u[:120], err=str(e)[:120]); continue
        t = r.text; res = {}
        for k in j["keys"]:
            occ = [mm.start() for mm in re.finditer(k, t)]
            res[k] = [len(occ)] + [re.sub(r"\s+", " ", t[max(0, i-j.get("b", 80)):i+j.get("a", 160)]) for i in occ[:j.get("n", 3)]]
        out("SNIP", url=urllib.parse.unquote(u)[:110], n=len(t), res=res)
if __name__ == "__main__":
    pf.log = lambda m: print("  log:", m, flush=True)
    for j in json.load(open(sys.argv[1])):
        if left() < 30: print("시간 제한 — 남은 작업 건너뜀"); break
        {"sitemap": sitemap_find, "shopify": shopify_list, "fetch": fetch, "page": page, "grep": grep, "detail": detail, "snip": snip, "shopjson": shopjson, "fetchb": fetchb}[j["t"]](j)
    print(f"끝 {int(time.time()-T0)}초")

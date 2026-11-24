# 임시 시험(병합 안 함 · 끝나면 바로 지움): 가니·아미·스투시 한국 공식몰 구조 진단 — 우리 봇 이름 · robots.txt 준수 · 공개 상품 정보만(목록 품번 안 씀)
import collections, json, re, time, traceback, urllib.parse
import price_fetch as pf


def tg(u):
    try:
        return pf.get(u), None
    except Exception as e:
        return None, f"{type(e).__name__}: {str(e)[:200]}"


def sn(t, rx, n=4, w=900, back=200):
    return [re.sub(r"\s+", " ", t[max(0, m.start() - back): m.start() + w]) for m in list(re.finditer(rx, t))[:n]]


def ldsum(t):
    out = []
    for n in pf._ld_nodes(t):
        ty = sorted(pf._types(n))
        offs = n.get("offers")
        offs = offs if isinstance(offs, list) else [offs] if isinstance(offs, dict) else []
        out.append({"ty": ty, "sku": n.get("sku"), "pg": n.get("productGroupID"), "name": str(n.get("name"))[:60], "color": n.get("color"),
                    "off": [(o.get("sku"), o.get("price"), o.get("priceCurrency"), str(o.get("availability"))[-12:]) for o in offs if isinstance(o, dict)][:8],
                    "nvar": len(n.get("hasVariant") or []),
                    "var": [(v.get("sku"), v.get("color"), ((v.get("offers") or {}) if isinstance(v.get("offers"), dict) else {}).get("price")) for v in (n.get("hasVariant") or [])][:30]})
    return out


def robots(host):
    r, e = tg(f"https://{host}/robots.txt")
    return e or "\n".join(l for l in r.text.splitlines() if l.strip() and not l.startswith("#"))[:3000]


def ganni(R):
    host = "www.ganni.com"
    R["robots"] = robots(host)
    maps = pf._robots_maps(host)
    R["maps"] = maps
    us = pf._sm_walk(maps or [f"https://{host}/sitemap_index.xml"], host, "/", max_maps=20, budget=150)
    R["sm_n"], R["sm_partial"] = len(us), us.partial
    locs = collections.Counter(urllib.parse.urlsplit(u).path.split("/")[1] for u in us)
    R["locs"] = locs.most_common(12)
    rx = re.compile(r"^/([a-z]{2}(?:-[a-z]{2})?)/([^/]+)-([A-Z]\d{4}(?:\d{3})?)\.html$")
    by = collections.defaultdict(set)
    shapes = collections.Counter()
    for u in us:
        m = rx.match(urllib.parse.urlsplit(u).path)
        if m:
            by[m.group(3)].add(m.group(2)); shapes[re.sub(r"\d", "9", m.group(3))] += 1
    R["pid_n"], R["pid_shapes"] = len(by), shapes.most_common()
    multi = {k: sorted(v) for k, v in by.items() if len(v) > 1}
    R["multi_n"], R["multi_ex"] = len(multi), dict(list(multi.items())[:8])
    R["old_ex"] = [(k, sorted(v)[:2]) for k, v in by.items() if len(k) == 5][:10]
    R["nonmatch_ex"] = [u for u in us if not rx.match(urllib.parse.urlsplit(u).path)][:15]
    pages = []
    want = list(dict.fromkeys(["A1050257", "A1010227", "A1040422", "A1170016", "A1030603"] + [k for k, _ in R["old_ex"][:2]] + list(multi)[:2]))
    for pid in want:
        slugs = sorted(by.get(pid) or [])
        for sl in slugs[:2] or [None]:
            if not sl:
                pages.append({"pid": pid, "err": "사이트맵에 없음"}); continue
            u = f"https://{host}/en-kr/{sl}-{pid}.html"
            r, e = tg(u)
            if e:
                pages.append({"pid": pid, "u": u, "err": e}); continue
            t = r.text
            pages.append({"pid": pid, "u": u, "final": r.url, "len": len(t), "title": (re.search(r"<title>([^<]*)", t) or [None, ""])[1][:100],
                          "ld": ldsum(t),
                          "price": sn(t, r"js-pdp-normal-price", 2, 700, 900),
                          "n_normal": t.count("js-pdp-normal-price"), "n_sales": t.count("js-pdp-sales-price"), "n_disc": t.count("js-pdp-discount"),
                          "dwvar": sorted(set(re.findall(r"dwvar_[A-Z0-9]+_color=([0-9A-Z]{3})", t)))[:20],
                          "colorlinks": sorted(set(re.findall(r'href="(/en-kr/[^"]*-' + pid + r'\.html[^"]*)"', t)))[:20],
                          "data_pid": sorted(set(re.findall(r'data-pid="([^"]+)"', t)))[:20],
                          "swatch": sn(t, r"color-swatch|b-swatch|swatch", 2, 500, 100)})
    R["pages"] = pages
    r, e = tg(f"https://{host}/en-kr/sale/")
    R["sale_list"] = e or {"final": r.url, "tiles": sn(r.text, r"b-tile__price", 3, 400, 100), "pids": sorted(set(re.findall(r"-([A-Z]\d{7})\.html", r.text)))[:30]}


def shop(R, base, pre, page_rx):
    host = urllib.parse.urlsplit(base).netloc
    R["robots"] = robots(host)
    ps, n = [], 0
    for page in range(1, 13):
        r, e = tg(f"{base}{pre}/products.json?limit=250&page={page}")
        if e:
            R["err_page"] = (page, e); break
        x = (pf._json(r) or {}).get("products") or []
        ps += x
        if len(x) < 250:
            break
    R["n"] = len(ps)
    vs = [v for p in ps for v in p.get("variants") or []]
    R["n_var"] = len(vs)
    R["cmp"] = [(v.get("sku"), v.get("price"), v.get("compare_at_price")) for v in vs if v.get("compare_at_price")][:15]
    R["cmp_n"] = sum(1 for v in vs if v.get("compare_at_price"))
    R["keys"] = sorted(vs[0].keys()) if vs else []
    R["min_price"] = min((float(v.get("price") or 0) for v in vs), default=None)
    R["max_price"] = max((float(v.get("price") or 0) for v in vs), default=None)
    R["sku_shapes"] = collections.Counter(re.sub(r"[A-Z]", "A", re.sub(r"\d", "9", str(v.get("sku") or ""))) for v in vs).most_common(10)
    R["types"] = collections.Counter(str(p.get("product_type")) for p in ps).most_common(20)
    seg = collections.defaultdict(set)
    for p in ps:
        for v in p.get("variants") or []:
            s = str(v.get("sku") or "")
            seg[re.split(r"[.\-]", s)[0]].add(float(v.get("price") or 0))
    R["seg_n"] = len(seg)
    R["seg_mixed"] = sum(1 for v in seg.values() if len(v) > 1)
    R["seg_mixed_ex"] = [(k, sorted(v)) for k, v in seg.items() if len(v) > 1][:10]
    nosku = [p.get("handle") for p in ps if not any(str(v.get("sku") or "").strip() for v in p.get("variants") or [])]
    R["nosku_n"], R["nosku_ex"] = len(nosku), nosku[:8]
    if ps:
        h = ps[0]["handle"]
        r, e = tg(f"{base}{pre}/products/{h}")
        R["page"] = e or {"u": r.url, "len": len(r.text), "price": sn(r.text, page_rx, 2, 500, 200), "won": f"₩{int(float(ps[0]['variants'][0]['price'])):,}" in r.text,
                          "krw": r.text.count("KRW"), "ld": ldsum(r.text)[:3]}
        r, e = tg(f"{base}{pre}/products/{h}.json")
        R["pjson"] = e or {"keys": sorted(((pf._json(r) or {}).get("product") or {}).get("variants", [{}])[0].keys())}


def main():
    R = {"start": time.time(), "ua": pf.UA}
    for k, f in (("GANNI", ganni), ("AMI", lambda R: shop(R, "https://www.amiparis.com", "/ko-kr", r"c-price")),
                 ("STUSSY", lambda R: shop(R, "https://kr.stussy.com", "", r"product__price"))):
        R[k] = {}
        t0 = time.time()
        try:
            f(R[k])
        except BaseException:
            R[k]["fatal"] = traceback.format_exc()[-2500:]
        R[k]["sec"] = round(time.time() - t0)
    R["blocked"] = sorted(pf._BLOCKED)
    R["sec"] = round(time.time() - R["start"])
    print("=== RESULT ===")
    print(json.dumps(R, ensure_ascii=False, default=str))
    print("=== END ===")


if __name__ == "__main__":
    main()

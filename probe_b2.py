# 임시 시험(병합 안 함 · 끝나면 바로 지움): 2차 그 밖 브랜드(메종키츠네·드롤드무슈·팔로마울) 국내 공식몰 구조 진단 — 우리 봇 이름 · robots.txt 준수 · 막히면 멈춤(우회 없음) · 공개 상품 정보만
import json, re, time
import price_fetch as pf

T0 = time.time()
CODE_MK = r"\b[A-Z]{2,5}\d{2,5}[A-Z]{2}\d{4}(?:[-_ ]?[A-Z]?\d{3,4})?\b"          # 메종키츠네 글로벌 품번 꼴
CODE_DM = r"\b[A-Z]{2,3}\d{3}[-_ ]?[A-Z]{2}\d{3}(?:[-_ ]?[A-Z]{2,3})?\b"        # 드롤드무슈 글로벌 품번 꼴
CODE_PW = r"\b[A-Z]{2}\d{4}(?:[-_ ]?\d{3})?\b"                                  # 팔로마울 꼴


def out(tag, obj):
    print("PB2 " + json.dumps({"t": tag, "d": obj}, ensure_ascii=False, default=str)[:20000], flush=True)


def fetch(u):
    try:
        r = pf.get(u)
        return r, None
    except Exception as e:
        return None, f"{type(e).__name__}: {str(e)[:200]}"


def sn(t, rx, n=6, w=220, b=40):
    o = []
    for m in re.finditer(rx, t, re.I | re.S):
        o.append(re.sub(r"\s+", " ", t[max(0, m.start() - b): m.start() + w]))
        if len(o) >= n:
            break
    return o


def uniq(xs, n=30):
    s, o = set(), []
    for x in xs:
        if x not in s:
            s.add(x); o.append(x)
        if len(o) >= n:
            break
    return o


def page(tag, u, code_rx, extra=(), n=4):
    r, e = fetch(u)
    if not r:
        out(tag, {"u": u, "err": e}); return None
    t = r.text
    d = {"u": u, "final": r.url, "st": r.status_code, "len": len(t), "title": (re.search(r"<title[^>]*>(.*?)</title>", t, re.S | re.I) or [None, ""])[1][:160],
         "codes": uniq(re.findall(code_rx, t)), "ld": [], "shopify": "cdn.shopify.com" in t, "magento": "Magento" in t or "mage/" in t,
         "hreflang": uniq(re.findall(r'hreflang="([^"]+)"\s+href="([^"]+)"', t) or re.findall(r'href="([^"]+)"\s+hreflang="([^"]+)"', t), 40)}
    try:
        for nd in pf._ld_nodes(t):
            ty = pf._types(nd)
            if ty & {"product", "productgroup"}:
                of = nd.get("offers"); ofl = of if isinstance(of, list) else [of] if isinstance(of, dict) else []
                d["ld"].append({"name": str(nd.get("name"))[:100], "sku": str(nd.get("sku"))[:40], "mpn": str(nd.get("mpn"))[:40],
                                "off": [[str((o or {}).get("price")), str((o or {}).get("priceCurrency")), str((o or {}).get("priceSpecification"))[:200]] for o in ofl[:4]]})
    except Exception as e2:
        d["ld_err"] = str(e2)[:100]
    for k, rx in extra:
        d[k] = sn(t, rx, n)
    out(tag, d)
    return t


# ── 메종키츠네 한국(maisonkitsune.com/kr — Magento) ──
r, e = fetch("https://maisonkitsune.com/robots.txt")
out("mk_robots", {"err": e, "txt": (r.text[:4000] if r else "")})
for u in ("https://maisonkitsune.com/kr/catalogsearch/result/?q=fox", "https://maisonkitsune.com/kr/woman/ready-to-wear/sweaters-cardigans.html?p=2",
          "https://maisonkitsune.com/kr/woman/ready-to-wear/sweaters-cardigans.html?product_list_limit=36", "https://maisonkitsune.com/kr/sale.html"):
    out("mk_robots_ok", [u, pf.robots_ok(u)])
sm = []
for u in ("https://maisonkitsune.com/media/sitemap/sitemap_kr.xml", "https://maisonkitsune.com/media/sitemap/sitemap_kr_ko.xml", "https://maisonkitsune.com/media/sitemap/sitemap_kr_en_product.xml"):
    r, e = fetch(u)
    if not r:
        out("mk_sm", {"u": u, "err": e}); continue
    t = r.text
    locs = re.findall(r"<loc>([^<]+)</loc>", t)
    blocks = re.findall(r"<url>.*?</url>", t, re.S)[:3]
    out("mk_sm", {"u": u, "len": len(t), "n_loc": len(locs), "head": t[:600], "blocks": [b[:1500] for b in blocks],
                  "img_codes": uniq(re.findall(CODE_MK, t), 20), "n_img": t.count("<image:loc>")})
    sm += [l for l in locs if "/kr/" in l and l.endswith(".html")]
prod = [l for l in sm if re.search(r"-[0-9a-f]{13}\.html$", l)]
out("mk_sm_prod", {"n": len(prod), "head": prod[:5]})
MK_EX = (("sku", r'"sku"\s*:'), ("jsoncfg", r'jsonConfig|spConfig|"optionPrices"'), ("price_amt", r'data-price-amount'), ("old", r'oldPrice|old-price|regularPrice|basePrice'),
         ("final", r'finalPrice|special-price'), ("dl", r'dataLayer|ecommerce|item_id|"id"\s*:\s*"[A-Z]'), ("ref", r'R[ée]f[ée]rence|참조|Ref\.|품번|style'),
         ("pid", r'data-product-id|product_id|"productId"'), ("krw", r'₩|KRW|원<'))
for i, u in enumerate((prod[:2] or ["https://maisonkitsune.com/kr/resort-shirt-feather-beige-6a31e8374476c.html"])):
    page(f"mk_page{i}", u, CODE_MK, MK_EX)
for i, u in enumerate(("https://maisonkitsune.com/kr/woman/ready-to-wear/sweaters-cardigans.html", "https://maisonkitsune.com/kr/sale.html")):
    t = page(f"mk_cat{i}", u, CODE_MK, MK_EX + (("tile", r'class="[^"]*product-item[^"]*"'), ("pager", r'toolbar-amount|pages-item|action\s+next|limiter')), 3)
    if t:
        out(f"mk_cat{i}_n", {"n_tiles": len(re.findall(r'class="[^"]*product-item-info', t)), "n_links": len(set(re.findall(r'href="(https://maisonkitsune\.com/kr/[^"]+-[0-9a-f]{13}\.html)"', t))),
                             "n_price_amt": t.count("data-price-amount"), "n_old": t.count('data-price-type="oldPrice"'), "n_final": t.count('data-price-type="finalPrice"')})

# ── 코오롱몰(드롤드무슈·팔로마울 국내 수입사몰) ──
r, e = fetch("https://www.kolonmall.com/robots.txt")
out("km_robots", {"err": e, "txt": (r.text[:3000] if r else "")})
KM_EX = (("pum", r'품번|모델명|모델번호|상품코드|스타일'), ("price", r'consumerPrice|normalPrice|salePrice|retailPrice|"price"\s*:'), ("brandList", r'/Brands/[A-Z_]+/List/\d+'))
for i, u in enumerate(("https://www.kolonmall.com/Product/D0TSW25250BRD", "https://www.kolonmall.com/Product/SVTAW25853WHX")):
    page(f"km_dm_page{i}", u, CODE_DM, KM_EX)
for b, rx in (("DROLEDEMONSIEUR", CODE_DM), ("PALOMAWOOL", CODE_PW)):
    t = page(f"km_brand_{b}", f"https://www.kolonmall.com/Brands/{b}", rx, KM_EX, 8)
    if t:
        lst = uniq(re.findall(rf'/Brands/{b}/List/\d+', t), 10)
        out(f"km_brand_{b}_lists", lst)
        for j, l in enumerate(lst[:2]):
            t2 = page(f"km_list_{b}{j}", "https://www.kolonmall.com" + l, rx, (("name", r'"name"\s*:\s*"'), ("pg", r'page=\d+|"totalCount"|totalElements')), 6)
            if t2:
                out(f"km_list_{b}{j}_n", {"prod": len(set(re.findall(r"/Product/([A-Z0-9]{8,20})", t2))), "names": uniq(re.findall(r'\(PALOMA WOOL\)[^"<]{0,80}|DROLE DE MONSIEUR[^"<]{0,80}', t2), 12)})
page("km_pw_page0", "https://www.kolonmall.com/Product/W1WAX25213NYX", CODE_PW, KM_EX)

# ── 브랜드 글로벌몰 한국 경로 ──
for host in ("https://droledemonsieur.com", "https://www.palomawool.com"):
    r, e = fetch(host + "/robots.txt")
    out("gl_robots", {"h": host, "err": e, "txt": (r.text[:2500] if r else "")})
    page("gl_home", host + "/", CODE_DM if "drole" in host else CODE_PW, (("loc", r'ko-kr|en-kr|/kr/|Korea|KRW|₩'),), 6)
    for pth in ("/ko-kr", "/en-kr", "/kr", "/ko"):
        r, e = fetch(host + pth)
        out("gl_path", {"u": host + pth, "err": e, "final": (r.url if r else None), "st": (r.status_code if r else None), "krw": (len(re.findall(r"₩|KRW", r.text)) if r else None)})
    r, e = fetch(host + "/products.json?limit=3")
    if r:
        try:
            ps = r.json().get("products") or []
            out("gl_pj", {"h": host, "n": len(ps), "p": [{"h": p.get("handle"), "t": p.get("title"), "v": [[v.get("sku"), v.get("price"), v.get("compare_at_price")] for v in (p.get("variants") or [])[:4]]} for p in ps]})
            if ps:
                for pth in ("/ko-kr", "/en-kr", ""):
                    r2, e2 = fetch(f"{host}{pth}/products/{ps[0]['handle']}.json")
                    out("gl_pjson", {"u": f"{host}{pth}/products/{ps[0]['handle']}.json", "err": e2, "final": (r2.url if r2 else None),
                                     "cur": (re.findall(r'"price_currency"\s*:\s*"([A-Z]{3})"', r2.text)[:2] if r2 else None),
                                     "v": (r2.json().get("product", {}).get("variants", [{}])[0].get("price") if r2 and r2.headers.get("content-type", "").startswith("application/json") else None)})
        except Exception as e3:
            out("gl_pj", {"h": host, "err": str(e3)[:200]})
    else:
        out("gl_pj", {"h": host, "err": e})
out("done", {"sec": round(time.time() - T0), "blocked": sorted(pf._BLOCKED)})

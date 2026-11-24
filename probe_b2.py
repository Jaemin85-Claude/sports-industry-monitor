# 임시 시험(병합 안 함 · 끝나면 바로 지움) 2회: 메종키츠네 한국 사이트맵 그림 품번·상품 페이지 가격 칸 · 코오롱몰 드롤드무슈·팔로마울 상품 자료 칸 · 글로벌몰 목록 — 우리 봇 이름 · robots.txt 준수 · 공개 상품 정보만
import json, re, time
import price_fetch as pf

T0 = time.time()


def out(tag, obj):
    print("PB2 " + json.dumps({"t": tag, "d": obj}, ensure_ascii=False, default=str)[:30000], flush=True)


def fetch(u):
    try:
        return pf.get(u), None
    except Exception as e:
        return None, f"{type(e).__name__}: {str(e)[:200]}"


def sn(t, rx, n=4, w=300, b=60):
    o = []
    for m in re.finditer(rx, t, re.S):
        o.append(re.sub(r"\s+", " ", t[max(0, m.start() - b): m.start() + w]))
        if len(o) >= n:
            break
    return o


# ── 메종키츠네: 한국 상품 사이트맵의 (주소, 그림 파일 이름) 모두 ──
r, e = fetch("https://maisonkitsune.com/media/sitemap/sitemap_kr_en_product.xml")
pairs = []
if r:
    for b in re.findall(r"<url>.*?</url>", r.text, re.S):
        loc = (re.search(r"<loc>([^<]+)</loc>", b) or [None, ""])[1]
        imgs = re.findall(r"<image:loc>([^<]+)</image:loc>", b)
        lm = (re.search(r"<lastmod>([^<]+)</lastmod>", b) or [None, ""])[1][:10]
        pairs.append([loc.rsplit("/", 1)[-1], [i.rsplit("/", 1)[-1] for i in imgs][:3], lm])
    for i in range(0, len(pairs), 150):
        out("mk_pairs", pairs[i:i + 150])
else:
    out("mk_pairs_err", e)

# 상품 페이지 12개 — 옷·가방·가니 여러 분류(사이트맵 차례대로 고르되 이름에 jumper/tee/shirt/cardigan/sweatshirt/bag/cap 있는 것)
pick, seen = [], set()
for loc, imgs, lm in pairs:
    k = next((w for w in ("jumper", "tee-shirt", "sweatshirt", "cardigan", "shirt", "jacket", "bag", "cap", "polo", "hoodie", "pants", "dress") if w in loc), None)
    if k and k not in seen:
        seen.add(k); pick.append(loc)
    if len(pick) >= 12:
        break


def mk_page(u):
    r, e = fetch("https://maisonkitsune.com/kr/" + u)
    if not r:
        return {"u": u, "err": e}
    t = r.text
    d = {"u": u, "final": r.url.rsplit("/", 1)[-1]}
    m = re.search(r'"event":"productPage","product":(\{.*?\})\}\);', t)
    d["dl"] = m.group(1)[:600] if m else None
    d["meta_price"] = re.findall(r'property="product:price:amount"\s+content="([^"]+)"', t)[:3]
    d["opt"] = sn(t, r'"optionPrices":\{', 2, 900, 0)
    d["skus"] = re.findall(r'"sku":"([^"]+)"', t)[:30]
    d["fp"] = re.findall(r"data-fp='([^']*)'", t)[:3]
    d["vat"] = re.findall(r'product-vat="([^"]+)"', t)[:3]
    d["ge"] = sn(t, r"GlobalE|globale|Global-e", 3, 200, 30)
    d["price_html"] = sn(t, r'class="[^"]*price[^"]*"[^>]*>\s*[₩\d]', 4, 200, 20)
    d["won_txt"] = re.findall(r"₩\s?[\d,]{4,}", t)[:8]
    d["special"] = sn(t, r'special_price|"special"', 2, 200, 20)
    return d


for u in pick:
    out("mk_page", mk_page(u))

# ── 코오롱몰 드롤드무슈: 상품 자료 칸 이름(브랜드 품번이 들어 있는 칸이 있는지) ──
r, e = fetch("https://www.kolonmall.com/Product/D0TSW25250BRD")
if r:
    t = r.text
    keys = sorted(set(re.findall(r'\\?"([a-zA-Z]{4,40})\\?":', t)))
    out("km_keys", [k for k in keys if re.search(r"code|no$|No|model|style|sku|item|origin|vendor|supplier|maker|partner|ref|barcode|ean|gtin", k, re.I)][:200])
    out("km_code_ctx", sn(t, r"D0TSW25250", 8, 260, 120))
    out("km_info", sn(t, r"상품정보|제조자|수입자|품번|모델", 6, 260, 40))
    out("km_wish", sn(t, r'"wishPrice"', 3, 160, 160))
else:
    out("km_keys", e)

# 코오롱몰 드롤드무슈 목록 — 몇 쪽·몇 개
for u in ("https://www.kolonmall.com/Brands/DROLEDEMONSIEUR/List/133020164007", "https://www.kolonmall.com/Brands/DROLEDEMONSIEUR/List/133020164007?page=2",
          "https://www.kolonmall.com/Brands/DROLEDEMONSIEUR/List/133020000136"):
    r, e = fetch(u)
    if not r:
        out("km_list", {"u": u, "err": e}); continue
    t = r.text
    tc = re.findall(r'"page":\{"__typename":"page","totalCount":(\d+),"currentPage":(\w+)\}', t)[:4]
    prods = []
    for m in re.finditer(r'"code":"([A-Z0-9]{10,16})","name":"([^"]{2,120})"', t):
        prods.append([m.group(1), m.group(2)])
    seen2, uniq = set(), []
    for c, n in prods:
        if c not in seen2:
            seen2.add(c); uniq.append([c, n])
    out("km_list", {"u": u, "tc": tc, "n_prod_links": len(set(re.findall(r"/Product/([A-Z0-9]{10,16})", t))), "codes_names": uniq[:80],
                    "wish": re.findall(r'"price":(\d+),"wishPrice":(\d+)', t)[:10], "brand_codes": sorted(set(re.findall(r'"brandCode":"(\d+)"', t)))[:10]})

# ── 드롤드무슈 글로벌몰(쇼피파이) 목록 크기·이름·품번 꼴 ──
allp = []
for pg in range(1, 6):
    r, e = fetch(f"https://droledemonsieur.com/products.json?limit=250&page={pg}")
    if not r:
        out("dm_pj_err", {"pg": pg, "err": e}); break
    ps = (r.json() or {}).get("products") or []
    allp += [[p.get("title"), p.get("handle"), [v.get("sku") for v in (p.get("variants") or [])][:2], (p.get("variants") or [{}])[0].get("price"),
              [o.get("values") for o in (p.get("options") or []) if (o.get("name") or "").lower() in ("color", "colour", "couleur")][:1]] for p in ps]
    if len(ps) < 250:
        break
out("dm_pj_n", len(allp))
for i in range(0, len(allp), 120):
    out("dm_pj", allp[i:i + 120])

# ── 팔로마울: 코오롱몰 8개 정가 · 글로벌몰 품번 꼴 ──
r, e = fetch("https://www.kolonmall.com/Brands/PALOMAWOOL/List/133020162660")
if r:
    t = r.text
    out("pw_km", {"names": re.findall(r'\(PALOMA WOOL\)[^"]{0,90}', t)[:20], "wish": re.findall(r'"price":(\d+),"wishPrice":(\d+)', t)[:12],
                  "gt": sn(t, r"GT2160", 3, 200, 200)})
pw = []
for pg in range(1, 4):
    r, e = fetch(f"https://www.palomawool.com/products.json?limit=250&page={pg}")
    if not r:
        out("pw_pj_err", e); break
    ps = (r.json() or {}).get("products") or []
    pw += [[p.get("title"), [v.get("sku") for v in (p.get("variants") or [])][:2]] for p in ps]
    if len(ps) < 250:
        break
out("pw_pj_n", len(pw)); out("pw_pj", pw[:150])
open("/tmp/pick.json", "w").write(json.dumps(pick[:3]))
out("done", {"sec": round(time.time() - T0), "blocked": sorted(pf._BLOCKED), "pick": pick})

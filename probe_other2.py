# 임시 시험(병합 안 함 · PR 전에 지움): 그 밖의 브랜드 7곳 국내 공식몰 구조 — 우리 봇 이름 · robots.txt 준수 · 봇 확인 화면이면 멈춤(우회 없음) · 공개 상품 정보만 모음 · 결과는 암호화해서만 찍음
import base64, contextlib, io, json, os, re, subprocess, tempfile, time, traceback, urllib.parse, zlib
from html import unescape
from concurrent.futures import ThreadPoolExecutor
import price_fetch as pf

PUB = """-----BEGIN PUBLIC KEY-----
MIIBojANBgkqhkiG9w0BAQEFAAOCAY8AMIIBigKCAYEAv/mmzIlXG45XqvFPyeSc
3i34K0csjndmr8SEWqALl8zSEpFPos+O4CqD+TKT+h+1vw/N6l1QpNKum3Mb++uI
BQ/G2wx3BTAa8vpJJ2rt0IJHJ7purLPGwHEzuq9VqY5lnhbsHGzlXlFrIv+PgcXm
JF87cyaCtOsLYN4PFQXcNq/lofJkVJ0y5iVFcnNWYxJb26QJy1acdOyYczkiALOS
NrxJrMKZBl+4sG3oqd9xx9d3LjSlatJNC91KJcmrZBs/lWNK6vRZ24kcoVX301r8
2ToLL1J97CiVrjYcZReWUP4v+elvhbts6H2Ek2+83OYU5gGoxv2o7BEpVfpT2wqY
/KwF8h2E85s/l3KQnVt8O8JuaTEetTPdfhvkOONO4UJRj8WDvJ5qCA8jdzsSy//0
pzPYLgzZxlsO5e/rIQeUbL0DCdZzNvTDXIk9KTCi0td8TI8d8+gFhNh7wfg5++vA
aGNMT3gNbjBTksBRHEqpb5RWAHpucURS8FwBITRkrEAzAgMBAAE=
-----END PUBLIC KEY-----"""
T_SITE = 330   # 초 — 사이트 하나 최대


def enc_out(obj):
    raw = zlib.compress(json.dumps(obj, ensure_ascii=False, default=str).encode(), 9)
    with tempfile.TemporaryDirectory() as d:
        open(f"{d}/pub.pem", "w").write(PUB)
        open(f"{d}/k", "w").write(os.urandom(32).hex())
        open(f"{d}/p", "wb").write(raw)
        subprocess.run(["openssl", "enc", "-aes-256-cbc", "-pbkdf2", "-salt", "-in", f"{d}/p", "-out", f"{d}/c", "-pass", f"file:{d}/k"], check=True)
        subprocess.run(["openssl", "pkeyutl", "-encrypt", "-pubin", "-inkey", f"{d}/pub.pem", "-pkeyopt", "rsa_padding_mode:oaep",
                        "-pkeyopt", "rsa_oaep_md:sha256", "-in", f"{d}/k", "-out", f"{d}/ek"], check=True)
        ek = base64.b64encode(open(f"{d}/ek", "rb").read()).decode()
        c = base64.b64encode(open(f"{d}/c", "rb").read()).decode()
    print("=== ENC-KEY ==="); print(ek); print("=== ENC-DATA ===")
    for i in range(0, len(c), 1500):
        print(c[i:i + 1500])
    print("=== ENC-END ===")


def tg(u):
    try:
        r = pf.get(u)
        return r, None
    except Exception as e:
        return None, f"{type(e).__name__}: {str(e)[:200]}"


def ld_all(t):
    out = []
    for n in pf._ld_nodes(t):
        ty = pf._types(n)
        if ty & {"product", "productgroup"}:
            offers = n.get("offers")
            ofl = offers if isinstance(offers, list) else [offers] if isinstance(offers, dict) else []
            if isinstance(offers, dict) and isinstance(offers.get("offers"), list):
                ofl = offers["offers"]
            out.append({"ty": sorted(ty), "name": str(n.get("name") or "")[:90], "sku": str(n.get("sku") or "")[:40], "mpn": str(n.get("mpn") or "")[:40],
                        "pid": str(n.get("productID") or n.get("productGroupID") or "")[:40],
                        "off": [[str((o or {}).get("sku") or "")[:30], str((o or {}).get("price") or (o or {}).get("lowPrice") or "")[:14],
                                 str((o or {}).get("priceCurrency") or "")[:5], str((o or {}).get("priceSpecification") or "")[:200]] for o in ofl[:8]],
                        "nvar": len(n.get("hasVariant") or [])})
            for v in (n.get("hasVariant") or [])[:6]:
                o = (v or {}).get("offers") or {}
                o = o[0] if isinstance(o, list) and o else o
                out[-1].setdefault("var", []).append([str(v.get("sku") or "")[:30], str((o or {}).get("price") or "")[:14], str((o or {}).get("priceCurrency") or "")[:5]])
    return out[:4]


def snips(t, rx, n=6, w=160):
    out = []
    for m in re.finditer(rx, t, re.I | re.S):
        s = re.sub(r"\s+", " ", t[max(0, m.start() - 20): m.start() + w])
        out.append(s)
        if len(out) >= n:
            break
    return out


PRICE_RX = r'class="[^"]*(?:price|sale|strike|list-price|old-price|special-price|consumer|custom)[^"]*"'


def page_info(u, code_rx=None):
    r, e = tg(u)
    if e:
        return {"u": u[-110:], "err": e}
    t = r.text
    d = {"u": u[-110:], "final": r.url[-110:], "len": len(t), "title": (re.search(r"<title[^>]*>([^<]{0,120})", t) or [None, ""])[1].strip(),
         "ld": ld_all(t), "krw": len(re.findall(r"\d{1,3}(?:,\d{3})+\s*원|₩|KRW", t)),
         "price_snips": snips(t, PRICE_RX, 8), "fields": snips(t, r"(?:품번|상품코드|모델명|모델 번호|자체상품코드|스타일 ?번호|Style|Product code|Article|Référence|REF\.?)\s*[:<]", 6, 200),
         "next": bool(re.search(r"__NEXT_DATA__", t)), "meta_price": snips(t, r'(?:product:price:amount|og:price:amount|itemprop="price")', 3, 140)}
    if code_rx:
        d["codes"] = sorted(set(re.findall(code_rx, t)))[:60]
    return d


def links(t, base, rx):
    out = []
    for h in re.findall(r'href="([^"#]+)"', t):
        h = unescape(h)
        u = urllib.parse.urljoin(base, h)
        if re.search(rx, u) and u not in out:
            out.append(u)
    return out


def shopify_full(base, pre, R, key):
    prods = []
    for page in range(1, 9):
        r, e = tg(f"{base}{pre}/products.json?limit=250&page={page}")
        if e:
            R[key + "_err"] = e; break
        try:
            ps = r.json().get("products") or []
        except Exception:
            R[key + "_err"] = "JSON 아님"; break
        for p in ps:
            prods.append({"h": p.get("handle"), "t": str(p.get("title") or "")[:70], "ty": str(p.get("product_type") or "")[:30],
                          "tags": [str(x)[:30] for x in (p.get("tags") or [])][:15] if isinstance(p.get("tags"), list) else str(p.get("tags") or "")[:300],
                          "v": [[v.get("sku"), v.get("price"), v.get("compare_at_price"), v.get("available"), str(v.get("title") or "")[:30]] for v in (p.get("variants") or [])]})
        if len(ps) < 250:
            break
    R[key] = prods


def site_stussy(R):
    shopify_full("https://kr.stussy.com", "", R, "prods")
    p = (R.get("prods") or [{}])[0].get("h")
    if p:
        R["page"] = page_info(f"https://kr.stussy.com/products/{p}", r"\b\d{7}\b")


def site_ami(R):
    shopify_full("https://www.amiparis.com", "/ko-kr", R, "prods")
    p = (R.get("prods") or [{}])[0].get("h")
    if p:
        R["page"] = page_info(f"https://www.amiparis.com/ko-kr/products/{p}")


def site_ganni(R):
    base = "https://www.ganni.com"
    r, e = tg(f"{base}/sitemap_index.xml")
    if e:
        R["smi_err"] = e; return
    kids = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", r.text)
    R["sm_kids"] = kids[:80]
    kr = [k for k in kids if re.search(r"en[-_]kr|/kr|_kr|-kr", k, re.I)]
    R["sm_kr"] = kr[:10]
    urls = []
    for k in (kr or kids)[:6]:
        rr, e2 = tg(k)
        if e2:
            R.setdefault("sm_err", []).append([k[-60:], e2]); continue
        locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", rr.text)
        urls += [unescape(x) for x in locs]
        if len(urls) > 20000:
            break
    R["sm_n"] = len(urls)
    R["sm_paths"] = sorted({urllib.parse.urlsplit(u).path.split("/")[1] for u in urls if urllib.parse.urlsplit(u).path.count("/") >= 2})[:40]
    kr_urls = [u for u in urls if "/en-kr/" in u]
    R["kr_urls"] = kr_urls[:6000]
    R["gb_urls"] = [u for u in urls if "/en-gb/" in u][:6000] if not kr_urls else []
    samp = (kr_urls or [u.replace("/en-gb/", "/en-kr/") for u in urls if "/en-gb/" in u])[:4]
    R["pages"] = [page_info(u, r"\b[A-Z]\d{7}\d{0,5}\b") for u in samp]
    # 검색(사이트에서 나온 품번)
    m = re.search(r"-([A-Z]\d{7})\.html", " ".join(samp))
    if m:
        R["search"] = page_info(f"{base}/en-kr/search?q={m.group(1)}", r"-[A-Z]\d{7}\.html")
    R["search_short"] = page_info(f"{base}/en-kr/search?q=keychain", r"-[A-Z]\d{4,7}\.html")


def site_converse(R):
    base = "https://www.converse.co.kr"
    r, e = tg(base + "/")
    if e:
        R["home_err"] = e; return
    t = r.text
    R["cats"] = links(t, r.url, r"cate_no=\d+|/category/")[:60]
    R["prod_links_home"] = links(t, r.url, r"/product/|product_no=")[:40]
    R["home_snips"] = snips(t, r"(?:품번|모델|상품코드)", 4)
    pl = []
    for cu in R["cats"][:3]:
        rr, e2 = tg(cu)
        if e2:
            R.setdefault("cat_err", []).append([cu, e2]); continue
        lk = links(rr.text, rr.url, r"/product/|product_no=")
        R.setdefault("cat_pages", []).append({"u": cu, "n": len(lk), "sample": lk[:8], "paging": links(rr.text, rr.url, r"[?&]page=\d+")[:6],
                                              "names": snips(rr.text, r'class="[^"]*name[^"]*"', 6, 160)})
        pl += lk
    pl = [u for u in dict.fromkeys(pl + R["prod_links_home"]) if re.search(r"/product/[^/]+/\d+|product_no=\d+", u)]
    R["pages"] = [page_info(u, r"\b\d{6}C\b|\b[A-Z]\d{5}C\b|\b\d{6}\b") for u in pl[:3]]
    codes = [c for p in R["pages"] for c in p.get("codes", []) if c.endswith("C")]
    if codes:
        R["search"] = page_info(f"{base}/product/search.html?keyword={codes[0]}", r"/product/[^\"]+/\d+")
    rr, e2 = tg(f"{base}/sitemap.xml")
    R["sitemap"] = e2 or {"len": len(rr.text), "head": rr.text[:300]}


def site_mk(R):
    base = "https://maisonkitsune.com"
    for nm in ("kr", "kr_ko", "ko", "kr_en", "ko_kr", "kr_kr"):
        rr, e = tg(f"{base}/media/sitemap/sitemap_{nm}_index.xml")
        R.setdefault("sm_try", []).append([nm, e or f"ok {len(rr.text)}"])
        if not e and "<loc>" in rr.text:
            R["sm_kr_idx"] = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", rr.text)[:20]
            break
    r, e = tg(base + "/kr/")
    if e:
        R["home_err"] = e; return
    t = r.text
    lk = links(t, r.url, r"maisonkitsune\.com/kr/.+\.html")
    R["home_links"] = lk[:120]
    cats = [u for u in lk if re.search(r"/kr/(?:man|woman|men|women|homme|femme)[^/]*\.html|/kr/(?:man|woman)/", u)][:3] or lk[:3]
    prod = []
    for cu in cats[:3]:
        rr, e2 = tg(cu)
        if e2:
            R.setdefault("cat_err", []).append([cu, e2]); continue
        pl = links(rr.text, rr.url, r"maisonkitsune\.com/kr/.+\.html")
        R.setdefault("cat_pages", []).append({"u": cu, "n": len(pl), "sample": pl[:15], "ld": ld_all(rr.text)[:1],
                                              "paging": links(rr.text, rr.url, r"[?&]p=\d+")[:5], "price_snips": snips(rr.text, PRICE_RX, 4)})
        prod += pl
    cand = [u for u in dict.fromkeys(prod) if u not in cats and not re.search(r"/(?:man|woman|men|women)\.html$", u)]
    R["pages"] = [page_info(u, r"\b[A-Z]{2,5}\d{5}[A-Z]{2}\d{4}\b") for u in cand[:4]]
    codes = [c for p in R["pages"] for c in p.get("codes", [])]
    if codes:
        R["search"] = page_info(f"{base}/kr/catalogsearch/result/?q={codes[0]}", r"\b[A-Z]{2,5}\d{5}[A-Z]{2}\d{4}\b")


def site_kolon(R, path, code_rx):
    base = "https://www.kolonmall.com"
    for u in path:
        rr, e = tg(base + u)
        if e:
            R.setdefault("list_err", []).append([u, e]); continue
        t = rr.text
        pl = links(t, rr.url, r"kolonmall\.com/Product/[A-Za-z0-9]+$")
        nd = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', t, re.S)
        R.setdefault("lists", []).append({"u": u, "final": rr.url[-90:], "len": len(t), "n": len(pl), "sample": pl[:10], "next_len": len(nd.group(1)) if nd else 0,
                                          "codes": sorted(set(re.findall(code_rx, t)))[:80], "paging": links(t, rr.url, r"[?&]page=\d+")[:6],
                                          "names": snips(t, r"(?:DROLE|PALOMA|드롤|팔로마)", 8, 140)})
        R.setdefault("plinks", []).extend(pl)
    R["pages"] = [page_info(u, code_rx) for u in list(dict.fromkeys(R.get("plinks", [])))[:4]]


SITES = {
    "STUSSY": site_stussy, "AMI": site_ami, "GANNI": site_ganni, "CONVERSE": site_converse, "MAISON KITSUNE": site_mk,
    "DROLE DE MONSIEUR": lambda R: site_kolon(R, ["/Brands/DROLEDEMONSIEUR", "/Search?keyword=drole%20de%20monsieur"], r"\b[A-Z]{2,4}\d{3}-[A-Z]{2}\d{3}(?:-[A-Z]{1,4})?\b"),
    "PALOMAWOOL": lambda R: site_kolon(R, ["/Brands/PALOMAWOOL", "/Search?keyword=palomawool", "/Search?keyword=%ED%8C%94%EB%A1%9C%EB%A7%88%EC%9A%B8"], r"\b[A-Z]{2}\d{4}(?:-\d{3})?\b"),
}


def work(R):
    pf._PACE.clear()
    def run(b):
        pf._TL.c = pf._Ctx()
        res = {"t0": time.time()}
        try:
            SITES[b](res)
        except Exception:
            res["fatal"] = traceback.format_exc()[-1500:]
        res["sec"] = round(time.time() - res.pop("t0"))
        return b, res
    with ThreadPoolExecutor(7) as ex:
        for b, res in ex.map(run, list(SITES)):
            R.setdefault("sites", {})[b] = res


def main():
    R, buf = {"start": time.time()}, io.StringIO()
    try:
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            work(R)
    except BaseException:
        R["fatal"] = traceback.format_exc()[-3000:]
    R["log"] = buf.getvalue()[-100000:]
    R["sec"] = round(time.time() - R["start"])
    enc_out(R)
    print("probe done", R["sec"])


if __name__ == "__main__":
    main()

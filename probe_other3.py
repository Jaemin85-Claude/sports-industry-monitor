# 임시 시험(병합 안 함 · PR 전에 지움): 글로벌몰 한국 페이지 가격 대조 · 국내 몰 robots.txt · 웹 보관소 시험 — 우리 봇 이름 · robots.txt 준수 · 봇 확인 화면이면 멈춤(우회 없음) · 공개 상품 정보만 모음 · 결과는 암호화해서만 찍음
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



def spread(lst, n):
    if len(lst) <= n:
        return list(lst)
    st = len(lst) / n
    return [lst[int(i * st)] for i in range(n)]


def site_ami(R):
    shopify_full("https://www.amiparis.com", "/ko-kr", R, "kr")
    for loc in ("/fr-fr", "/en-us", "/en-gb"):
        k = "x" + loc.replace("/", "_")
        shopify_full("https://www.amiparis.com", loc, R, k)
        if R.get(k):
            break


def site_mk(R):
    base = "https://maisonkitsune.com"
    r, e = tg(f"{base}/media/sitemap/sitemap_kr_en_product.xml")
    if e:
        R["sm_err"] = e; return
    us = [unescape(x) for x in re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", r.text)]
    R["sm_n"] = len(us); R["sm_head"] = us[:5]
    pages = []
    for u in spread([x for x in us if "/kr/" in x], 14):
        d = page_info(u, r"\b[A-Z]{2,5}\d{5}[A-Z]{2}\d{4}\b")
        fr = u.replace("/kr/", "/fr/", 1)
        d["fr"] = page_info(fr, r"\b[A-Z]{2,5}\d{5}[A-Z]{2}\d{4}\b") if len(pages) < 8 else None
        pages.append(d)
    R["pages"] = pages


def site_ganni(R):
    base = "https://www.ganni.com"
    us = []
    for k in ("https://www.ganni.com/en/sitemap-ganni-pdp-0.xml", "https://www.ganni.com/en/sitemap-ganni-pdp-1.xml"):
        r, e = tg(k)
        if e:
            R.setdefault("sm_err", []).append(e); continue
        us += [unescape(x) for x in re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", r.text)]
    us = [u for u in us if re.search(r"-[A-Z]\d{7}\.html$", u)]
    R["sm_n"] = len(us)
    out = []
    for u in spread(us, 14):
        kr = re.sub(r"/en-[a-z]{2}/", "/en-kr/", u, 1)
        d = page_info(kr, r"\b[A-Z]\d{7}\d{0,5}\b")
        d["krw_snips"] = None
        out.append(d)
        if len(out) <= 6:
            d["gb"] = page_info(re.sub(r"/en-[a-z]{2}/", "/en-gb/", u, 1))
            d["dk"] = page_info(re.sub(r"/en-[a-z]{2}/", "/en-dk/", u, 1))
    R["pages"] = out


HOSTS = [("https://www.29cm.co.kr", "/product/1000000"), ("https://www.wconcept.co.kr", "/Product/300000000"), ("https://www.musinsa.com", "/products/1000000"),
         ("https://www.ssfshop.com", "/Maison-Kitsune/GM0000000000/good"), ("https://www.sivillage.com", "/goods/initDetailGoods.siv?goods_no=1"),
         ("https://www.thehandsome.com", "/ko/p/AA0000000"), ("https://www.lotteon.com", "/p/product/LO1"), ("https://www.ssg.com", "/item/itemView.ssg?itemId=1"),
         ("https://www.hmall.com", "/pd/pda/itemPtc?slitmCd=1"), ("https://www.halfclub.com", "/product/1"), ("https://kream.co.kr", "/products/1"),
         ("https://prod.danawa.com", "/info/?pcode=1"), ("https://www.enuri.com", "/detail.jsp?modelno=1"), ("https://search.shopping.naver.com", "/catalog/1"),
         ("https://www.lfmall.co.kr", "/app/product/HZ0000000"), ("https://www.thehyundai.com", "/front/pda/itemPtc.thd?slitmCd=1"),
         ("https://www.akmall.com", "/goods/GoodsDetail.do?goods_id=1"), ("https://www.lotteimall.com", "/goods/viewGoodsDetail.lotte?goods_no=1"),
         ("https://www.cjonstyle.com", "/p/item/1"), ("https://www.gsshop.com", "/prd/prd.gs?prdid=1"), ("https://www.trenbe.com", "/product/1"),
         ("https://www.mustit.co.kr", "/product/product_detail/1"), ("https://www.balaan.co.kr", "/shop/goods/goods_view.php?goodsno=1"),
         ("https://www.29cm.co.kr", "/"), ("https://www.ably.co.kr", "/goods/1"), ("https://zigzag.kr", "/catalog/products/1"),
         ("https://www.kasina.co.kr", "/product/1"), ("https://www.worksout.co.kr", "/product/1"), ("https://www.coupang.com", "/vp/products/1"),
         ("https://smartstore.naver.com", "/x/products/1"), ("https://brand.naver.com", "/x/products/1"), ("https://www.idlookmall.com", "/goods/1"),
         ("https://www.boon.so", "/"), ("https://www.oco.co.kr", "/"), ("https://www.adekuver.com", "/product/1"), ("https://www.seoulstore.com", "/products/1")]


def robots_sweep(R):
    out = []
    for base, path in HOSTS:
        ok, why = pf.robots_ok(base + path)
        okh, whyh = pf.robots_ok(base + "/")
        out.append([base, path, ok, why[:80], okh, whyh[:60]])
    R["robots"] = out


def wayback(R):
    tests = ["kr.stussy.com/products/1905210-triple-crown-tee-rock", "www.converse.co.kr/", "www.amiparis.com/ko-kr", "maisonkitsune.com/kr/",
             "www.ganni.com/en-kr/home", "www.kolonmall.com/Brands/DROLEDEMONSIEUR", "www.nike.com/kr/", "www.crocs.co.kr/"]
    out = []
    for u in tests:
        r, e = tg("https://archive.org/wayback/available?url=" + urllib.parse.quote(u, safe=""))
        if e:
            out.append([u, e]); continue
        try:
            snap = (r.json().get("archived_snapshots") or {}).get("closest") or {}
            out.append([u, snap.get("timestamp"), snap.get("status"), (snap.get("url") or "")[-90:]])
        except Exception as ex:
            out.append([u, "json " + str(ex)[:60]])
    R["avail"] = out
    r, e = tg("http://web.archive.org/cdx/search/cdx?url=kr.stussy.com/products/*&output=json&limit=20&filter=statuscode:200&collapse=urlkey")
    R["cdx"] = e or r.text[:3000]
    r, e = tg("https://web.archive.org/web/2025/https://kr.stussy.com/products/1905210-triple-crown-tee-rock")
    R["snap"] = e or {"final": r.url[-120:], "len": len(r.text), "ld": ld_all(r.text)[:1]}


SITES = {"AMI": site_ami, "MAISON KITSUNE": site_mk, "GANNI": site_ganni, "ROBOTS": robots_sweep, "WAYBACK": wayback}


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
    with ThreadPoolExecutor(5) as ex:
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

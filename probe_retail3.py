# 임시 시험(병합 안 함 · 끝나면 바로 지움): 29CM 브랜드별 품번 꼴·검색·상품 페이지 정가 · 폴더 상품 페이지 정가 칸 — 우리 봇 이름 · robots.txt 준수 · 봇 확인 화면이면 멈춤(우회 없음) · 공개 상품 정보만 · 결과는 암호화해서만 찍음
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



def rawsnips(t, rx, n=6, w=220, back=80):
    return [re.sub(r"\s+", " ", t[max(0, m.start() - back): m.start() + w]) for m in list(re.finditer(rx, t))[:n]]




BRANDS = {   # 키워드 → (29CM 영문 브랜드, 이름 속 품번 꼴)
    "뉴발란스": ("NEW BALANCE", r"(?<![0-9A-Z])([A-Z]{1,3}\d{3,4}[A-Z]{1,4}\d?)(?![0-9A-Z])"),
    "아디다스": ("ADIDAS", r"(?<![0-9A-Z])([A-Z]{2}\d{4}|[A-Z]\d{5})(?![0-9A-Z])"),
    "반스": ("VANS", r"(?<![0-9A-Z])(VN0[0-9A-Z]{8,10})(?![0-9A-Z])"),
    "호카": ("HOKA", r"(?<![0-9A-Z])(\d{7}-[A-Z]{3,5})(?![0-9A-Z])"),
    "노스페이스": ("THE NORTH FACE", r"(?<![0-9A-Z])(N[A-Z]\d[A-Z0-9]{4,7})(?![0-9A-Z])"),
}
API = "https://search-api.29cm.co.kr/api/v4/products?keyword={}"
KEYS = ("itemNo", "itemName", "frontBrandNameEng", "frontBrandNameKor", "frontBrandNo", "consumerPrice", "lastSalePrice", "lastSalePercent", "isSoldOut")


def items_of(d):
    x = d.get("data")
    if isinstance(x, dict):
        for k in ("products", "items", "list", "content"):
            if isinstance(x.get(k), list):
                return x[k], {kk: (vv if not isinstance(vv, (list, dict)) else type(vv).__name__) for kk, vv in x.items()}
    return (x if isinstance(x, list) else []), {}


def page_info2(u, code):
    r, e = tg(u)
    if e:
        return {"err": e}
    t = r.text
    return {"final": r.url[-60:], "ld": ld_all(t)[:2], "code_in": bool(re.search(r"(?<![0-9A-Z])" + re.escape(code) + r"(?![0-9A-Z])", t)),
            "seller": rawsnips(t, r"(?:판매자|상호명|입점|공식 ?스토어|partnerName|sellerName|brandName|companyName)", 6, 200, 40),
            "price_keys": rawsnips(t, r'(?:consumerPrice|sellPrice|lastSalePrice|originalPrice|salePrice)"?\s*:', 6, 120, 20), "len": len(t)}


def c29b(R):
    rb, eb = tg("https://search-api.29cm.co.kr/robots.txt")
    R["robots_api"] = eb or rb.text[:300]
    rw, ew = tg("https://www.29cm.co.kr/robots.txt")
    R["robots_www"] = ew or rw.text[:1500]
    out = {}
    for kw, (eng, rx) in BRANDS.items():
        o = {}
        r, e = tg(API.format(urllib.parse.quote(kw)))
        if e:
            o["err"] = e; out[kw] = o; continue
        d = r.json()
        its, meta = items_of(d)
        o["top_keys"] = [k for k in d if k != "data"]; o["data_meta"] = meta; o["n"] = len(its)
        o["items"] = [{k: it.get(k) for k in KEYS} for it in its[:25]]
        codes = []
        for it in its:
            if str(it.get("frontBrandNameEng") or "").upper() != eng:
                continue
            for m in re.findall(rx, str(it.get("itemName") or "").upper()):
                if m not in codes:
                    codes.append(m)
        if kw == "반스":
            codes = ["VN000D3HY28", "VN000D3HY281"] + codes
        o["codes"] = codes[:12]
        tries = []
        for c in codes[:6]:
            rr, e2 = tg(API.format(urllib.parse.quote(c)))
            if e2:
                tries.append({"c": c, "err": e2}); continue
            its2, _ = items_of(rr.json())
            hit = [it for it in its2 if re.search(r"(?<![0-9A-Z])" + re.escape(c) + r"(?![0-9A-Z])", str(it.get("itemName") or "").upper())]
            t = {"c": c, "n": len(its2), "n_hit": len(hit), "hit": [{k: it.get(k) for k in KEYS} for it in hit[:6]],
                 "other": [{k: it.get(k) for k in ("itemName", "frontBrandNameEng", "consumerPrice")} for it in its2 if it not in hit][:4],
                 "cps": sorted({it.get("consumerPrice") for it in hit if it.get("consumerPrice")}),
                 "brands": sorted({str(it.get("frontBrandNameEng")) for it in hit}), "bnos": sorted({str(it.get("frontBrandNo")) for it in hit})}
            if hit and len(tries) < 4:
                t["page"] = page_info2(f"https://www.29cm.co.kr/products/{hit[0].get('itemNo')}", c)
            tries.append(t)
        o["tries"] = tries
        out[kw] = o
    R["brands"] = out


def folder2(R):
    base = "https://www.folderstyle.com"
    out = []
    for c in ("B75806", "MR530SG"):
        r, e = tg(f"{base}/shop/shopbrand.html?search={c}&type=Y")
        if e:
            out.append({"c": c, "err": e}); continue
        ls = list(dict.fromkeys(re.findall(r'href="(/shop/shopdetail\.html\?branduid=\d+)[^"]*"', r.text)))[:2]
        o = {"c": c, "links": ls}
        if ls:
            rr, e2 = tg(base + ls[0])
            if e2:
                o["page"] = e2
            else:
                t = rr.text
                o["page"] = {"len": len(t), "ld": ld_all(t)[:2], "code_in": c in t,
                             "price": rawsnips(t, r"(?:판매가|소비자가|정가|시중가|price|consumer)", 10, 220, 60),
                             "meta": re.findall(r'<meta[^>]+(?:price|og:title)[^>]+>', t)[:6]}
        out.append(o)
    R["folder"] = out


SITES = {"29CM": c29b, "FOLDER": folder2}


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
    with ThreadPoolExecutor(2) as ex:
        for b, res in ex.map(run, list(SITES)):
            R.setdefault("sites", {})[b] = res


def main():
    R, buf = {"start": time.time()}, io.StringIO()
    try:
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            work(R)
    except BaseException:
        R["fatal"] = traceback.format_exc()[-3000:]
    R["log"] = buf.getvalue()[-30000:]
    R["sec"] = round(time.time() - R["start"])
    enc_out(R)
    print("probe done", R["sec"])


if __name__ == "__main__":
    main()

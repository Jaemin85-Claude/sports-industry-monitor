# 임시 시험(병합 안 함 · 끝나면 바로 지움): 29CM 검색 결과 칸·상품 페이지 · ABC마트 검색 자료 주소 · 폴더 다시 — 우리 봇 이름 · robots.txt 준수 · 봇 확인 화면이면 멈춤(우회 없음) · 공개 상품 정보만 모음 · 결과는 암호화해서만 찍음
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


CODES = ["B75806", "MR530SG", "VN000D3HY28", "U9060MUS"]


def c29(R):
    out = []
    rb, eb = tg("https://search-api.29cm.co.kr/robots.txt")
    R["robots_api"] = eb or rb.text[:600]
    for c in CODES:
        u = f"https://search-api.29cm.co.kr/api/v4/products?keyword={c}"
        r, e = tg(u)
        if e:
            out.append({"c": c, "err": e}); continue
        try:
            d = r.json()
        except Exception:
            out.append({"c": c, "notjson": r.text[:300]}); continue
        items = (d.get("data") or [])[:5]
        o = {"c": c, "keys": sorted((items[0] or {}).keys()) if items else [], "items": [{k: it.get(k) for k in ("itemNo", "itemName", "frontBrandNameEng", "consumerPrice", "sellPrice", "lastSalePrice", "saleRate", "isSoldOut")} for it in items], "top": {k: v for k, v in d.items() if k != "data"}}
        if items:
            pu = f"https://www.29cm.co.kr/products/{items[0].get('itemNo')}"
            ok, why = pf.robots_ok(pu)
            if ok:
                rr, e2 = tg(pu)
                if e2:
                    o["page"] = e2
                else:
                    tt = rr.text
                    o["page"] = {"final": rr.url[-60:], "ld": ld_all(tt)[:2], "code": rawsnips(tt, re.escape(c), 3, 160), "next": bool(re.search("__NEXT_DATA__", tt)),
                                 "price_keys": rawsnips(tt, r'(?:consumerPrice|sellPrice|lastSalePrice|originalPrice)\?"?\s*:', 6, 120, 20)}
            else:
                o["page"] = why
        out.append(o)
    R["tries"] = out


def abc(R):
    base = "https://abcmart.a-rt.com"
    r, e = tg(f"{base}/display/search-word/result?searchWord=B75806")
    if e:
        R["err"] = e; return
    t = r.text
    R["scripts"] = re.findall(r'<script[^>]+src="([^"]+)"', t)[:40]
    R["search_urls"] = sorted(set(re.findall(r'["\'](/[A-Za-z0-9_\-/]*(?:search|Search|product|prdt)[A-Za-z0-9_\-/]*(?:\.json|list|ajax|result)[A-Za-z0-9_\-/]*)["\']', t)))[:60]
    R["ajax"] = rawsnips(t, r"(?:$\.ajax|ajax\(|url\s*:\s*['\"]|fetch\()", 12, 260, 20)
    # 스크립트 파일 안의 검색 주소
    found = set()
    for s in R["scripts"]:
        if "search" in s.lower() or "display" in s.lower():
            su = urllib.parse.urljoin(r.url, s)
            if urllib.parse.urlsplit(su).netloc.endswith("a-rt.com"):
                rr, e2 = tg(su)
                if not e2:
                    for m in re.findall(r'["\'](/[A-Za-z0-9_\-/]*search[A-Za-z0-9_\-/]*)["\']', rr.text):
                        found.add(m)
    R["js_search_urls"] = sorted(found)[:60]


def folder(R):
    base = "https://www.folderstyle.com"
    ok, why = pf.robots_ok(base + "/")
    R["robots"] = why or "ok"
    for u in (f"{base}/shop/shopbrand.html?search=B75806&type=Y", f"{base}/shop/search_result.html?search=B75806", f"{base}/m/search.html?search=B75806"):
        okp, whyp = pf.robots_ok(u)
        if not okp:
            R.setdefault("tries", []).append({"u": u, "robots": whyp}); continue
        r, e = tg(u)
        R.setdefault("tries", []).append({"u": u, "err": e} if e else {"u": u, "final": r.url[-80:], "len": len(r.text), "links": list(dict.fromkeys(re.findall(r'href="([^"]*shopdetail[^"]*)"', r.text)))[:5], "code": rawsnips(r.text, "B75806", 3, 160)})


SITES = {"29CM": c29, "ABC": abc, "FOLDER": folder}


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
    with ThreadPoolExecutor(3) as ex:
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

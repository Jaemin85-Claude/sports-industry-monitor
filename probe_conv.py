# 임시 시험(병합 안 함 · 끝나면 바로 지움): 컨버스 한국 공식몰 실제 상품 페이지로 converse_price 확인 — 우리 봇 이름 · robots.txt 준수 · 봇 확인 화면이면 멈춤(우회 없음) · 공개 상품 정보만 모음 · 결과는 암호화해서만 찍음
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



def work(R):
    pf._PACE.clear(); pf._TL.c = pf._Ctx()
    base = pf.CONVERSE_KR
    pls = []
    for cu in ("/category/women-sale/1907/", "/category/%EC%8B%A0%EB%B0%9C/1123/", "/category/best-seller/1043/"):
        r, e = tg(base + cu)
        if e:
            R.setdefault("cat_err", []).append([cu, e]); continue
        pls += [l for l in dict.fromkeys(re.findall(r'href="(/product/[^"?#]+?/\d+/)', r.text))][:8]
    out = []
    for l in list(dict.fromkeys(pls))[:16]:
        r, e = tg(base + l)
        if e:
            out.append({"l": l[-30:], "err": e}); continue
        m = re.search(r'ma_product_code[^"]*"[^>]*>\s*(?:스타일\s*:\s*)?([0-9A-Z]{4,8})\s*<', r.text)
        code = m.group(1) if m else None
        d = {"l": l[-40:], "code": code, "meta": re.findall(r'product:(?:sale_)?price:amount"\s+content="([0-9.,]+)"', r.text)[:2],
             "custom": bool(re.search(r'span_product_price_custom', r.text)), "del": len(re.findall(r'<(?:del|strike|s)\b', r.text))}
        try:
            d["res"] = list(pf.converse_price(r.text, code)) if code else "no code"
        except Exception as ex:
            d["res"] = "ERR " + str(ex)[:120]
            i = r.text.find('id="span_product_price_text"')
            d["blk"] = re.sub(r"\s+", " ", r.text[max(0, i - 1500): i + 300])[-1800:] if i > 0 else None
        out.append(d)
    R["pages"] = out
    # 검색: 사이트에서 읽은 품번으로
    if out and any(x.get("code") for x in out):
        c = next(x["code"] for x in out if x.get("code"))
        try:
            g, n = pf._sku_fetch("컨버스", "KR", c, {c}, None)
            R["fetch"] = {"code": c, "got": {k: (list(v) if isinstance(v, tuple) else sorted(v)) for k, v in g.items()}, "none": n}
        except Exception as ex:
            R["fetch"] = {"code": c, "err": str(ex)[:200]}


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

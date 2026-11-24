# 임시 시험(병합 안 함 · 끝나면 바로 지움): 국내 판매처 8곳(슈마커·ABC마트·그랜드스테이지·폴더·카시나·웍스아웃·크림·에스마켓) 접속·robots.txt·검색·공개 상품 페이지 정가 칸 — 우리 봇 이름 · robots.txt 준수 · 봇 확인 화면이면 멈춤(우회 없음) · 공개 상품 정보만 모음 · 결과는 암호화해서만 찍음
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
T_SITE = 240   # 초 — 사이트 하나 최대


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
            br = n.get("brand")
            out.append({"ty": sorted(ty), "name": str(n.get("name") or "")[:90], "sku": str(n.get("sku") or "")[:40], "mpn": str(n.get("mpn") or "")[:40],
                        "brand": str(br.get("name") if isinstance(br, dict) else br or "")[:30],
                        "off": [[str(o.get("@type", ""))[:20], str(o.get("price", ""))[:14], str(o.get("priceCurrency", ""))[:5],
                                 str(o.get("priceSpecification", ""))[:200]] for o in ofl[:4] if isinstance(o, dict)]})
    return out[:4]


def sn(t, rx, n=6, w=220, back=80):
    return [re.sub(r"\s+", " ", t[max(0, m.start() - back): m.start() + w]) for m in list(re.finditer(rx, t, re.I))[:n]]


FIELDS_RX = r"(?:정상가|판매가|소비자가|발매가|할인가|정가|스타일컬러|스타일 ?코드|스타일|모델명|모델번호|품번|상품코드|자체상품코드|제품번호|fixedPrice|normalAmt|sellAmt|prdtPrice|styleCode|modelNo|productCode|consumerPrice|retailPrice|originalPrice|regularPrice|listPrice|line-through|itemprop=\"price\")"
CODE_RX = r"(?<![A-Z0-9])(?:[A-Z]{2}\d{4}-\d{3}|[A-Z]{1,2}\d{4,5}|[A-Z]{1,3}\d{3,4}[A-Z]{2,3}\d?|VN0[0-9A-Z]{7,9}|N[A-Z]\d[A-Z0-9]{5,6})(?![A-Z0-9])"


def page(u, code=None, keep=0):
    r, e = tg(u)
    if e:
        return {"u": u[-140:], "err": e}
    t = r.text
    h = getattr(r, "headers", {}) or {}
    d = {"u": u[-140:], "final": r.url[-140:], "st": r.status_code, "len": len(t), "clen": h.get("Content-Length"), "cenc": h.get("Content-Encoding"),
         "ctype": h.get("Content-Type"), "setck": [c.split("=")[0] for c in str(h.get("Set-Cookie") or "").split(",") if "=" in c][:6],
         "title": (re.search(r"<title[^>]*>([^<]{0,140})", t) or [None, ""])[1].strip(), "ld": ld_all(t),
         "fields": sn(t, FIELDS_RX, 18, 170, 60), "codes": sorted(set(re.findall(CODE_RX, t)))[:40],
         "meta": sn(t, r"(?:og:price|product:price|og:title|og:description)", 5, 200, 10)}
    if code:
        d["code_hits"] = len(re.findall(re.escape(code), t, re.I)); d["code"] = sn(t, re.escape(code), 4, 220, 120)
    if keep:
        d["raw"] = t[:keep]
    return d, t


def P(u, code=None, keep=0):
    x = page(u, code, keep)
    return x[0] if isinstance(x, tuple) else x


def T(u):
    x = page(u)
    return x[1] if isinstance(x, tuple) else ""


def links(t, base, rx, n=10):
    out = []
    for h in re.findall(r'''(?:href|data-href)=["']([^"'#]+)["']''', t):
        u = urllib.parse.urljoin(base, unescape(h))
        if re.search(rx, u) and u not in out:
            out.append(u)
    return out[:n]


def smarket(R):
    b = "https://www.smarket.co.kr"
    R["search"] = []
    for c in ["B75806", "MR530SG", "DD1391-100", "VN000D3HY28", "삼바", "530"]:
        u = f"{b}/goods/goods_search.php?keyword={urllib.parse.quote(c)}"
        x = page(u, c)
        if not isinstance(x, tuple):
            R["search"].append(x); continue
        d, t = x
        d["plinks"] = links(t, u, r"goods_view\.php\?goodsNo=\d+", 8)
        d["near"] = [lu for lu in d["plinks"] if re.search(re.escape(c), t[max(0, t.find(lu.split('/')[-1]) - 800): t.find(lu.split('/')[-1]) + 800], re.I)][:3]
        d.pop("fields", None)
        R["search"].append(d)
    tried = 0
    for s in R["search"]:
        for lu in (s.get("near") or s.get("plinks") or [])[:1]:
            if tried < 4:
                R.setdefault("pages", []).append(P(lu, s.get("u", "").split("keyword=")[-1] if s.get("near") else None)); tried += 1
    R["godo_fields"] = [p.get("u") for p in R.get("pages", [])]


def shoemarker(R):
    b = "https://www.shoemarker.co.kr"
    R["search"] = []
    for c in ["삼바", "530", "덩크", "올드스쿨", "SAMBA"]:
        u = f"{b}/ASP/Product/SearchProductList.asp?SearchWord={urllib.parse.quote(c)}"
        x = page(u)
        if not isinstance(x, tuple):
            R["search"].append(x); continue
        d, t = x
        d["plinks"] = links(t, u, r"ProductDetail\.asp\?ProductCode=\d+", 8)
        d["nores"] = bool(re.search(r"SearchProductNone|검색결과가 없|검색 결과가 없", t))
        d["cnt"] = sn(t, r"검색결과\s*<strong>", 2, 160, 10)
        d.pop("fields", None)
        R["search"].append(d)
    R["pages"] = []
    for s in R["search"][:4]:
        for lu in (s.get("plinks") or [])[:1]:
            R["pages"].append(P(lu))
    R["js_search"] = sn(T(f"{b}/ASP/Product/JS/SearchProductList.js"), r"url\s*:|\.asp", 12, 200, 60)


def folder(R):
    b = "https://www.folderstyle.com"
    R["pages"] = [P(f"{b}/shop/shopdetail.html?branduid=1100275960"), P(f"{b}/m/product.html?branduid=1100275960"),
                  P(f"{b}/shop/shopbrand.html?search=B75806&type=Y")]


def art(R, host, ch):
    b = f"https://{host}"
    js = {}
    for p in ["/static/common/js/biz/search/abcmart.search.result.js", "/static/common/js/biz/search/abcmart.search.js"]:
        t = T(b + p)
        js[p] = {"len": len(t), "urls": sorted(set(re.findall(r"""["'](/(?:display|product|search|api)[A-Za-z0-9_\-/]*)["']""", t)))[:60],
                 "ajax": sn(t, r"url\s*:\s*|\.ajax\(|abc\.ajax|\$\.get\(|\$\.post\(", 16, 220, 40)}
    R["js"] = js
    cands = sorted({u for v in js.values() for u in v["urls"] if re.search(r"search", u, re.I)})
    R["tries"] = []
    for cnd in cands[:10]:
        u = f"{b}{cnd}?searchWord=B75806&page=1&perPage=20&tabGubun=total&chnnlNo={ch}"
        x = page(u, "B75806")
        d = x[0] if isinstance(x, tuple) else x
        if isinstance(x, tuple):
            d["plinks"] = links(x[1], u, r"prdtNo=\d+", 5); d["prdt"] = sn(x[1], r"prdtNo|data-product-no|productNo", 3, 140, 30)
            d.pop("fields", None)
        R["tries"].append(d)
        if isinstance(x, tuple) and d.get("code_hits"):
            break
    pl = [lu for tr in R["tries"] for lu in (tr.get("plinks") or [])]
    if pl:
        R["page"] = P(pl[0], "B75806")


def kasina(R):
    b = "https://www.kasina.co.kr"
    x = page(b + "/")
    t = x[1] if isinstance(x, tuple) else ""
    bid = (re.search(r'"buildId"\s*:\s*"([^"]+)"', t) or re.search(r"/_next/static/([^/]+)/_buildManifest\.js", t) or [None, None])[1]
    R["buildId"] = bid
    R["next_data_keys"] = sn(t, r"__NEXT_DATA__", 1, 600, 0)
    if bid:
        m = T(f"{b}/_next/static/{bid}/_buildManifest.js")
        R["routes"] = sorted(set(re.findall(r'"(/[^"]*)"\s*:', m)))[:120]
    R["sitemap"] = P(b + "/sitemap.xml")
    R["home_links"] = links(t, b + "/", r"/(?:product|products|goods|item|p)/", 10)
    rts = R.get("routes") or []
    R["search_tries"] = []
    for rt in [r for r in rts if "search" in r.lower()][:3]:
        u = b + rt.replace("[keyword]", "B75806") + ("?keyword=B75806" if "[" not in rt else "")
        R["search_tries"].append(P(u, "B75806"))
    if R["home_links"]:
        R["page"] = P(R["home_links"][0])


def worksout(R):
    b = "https://www.worksout.co.kr"
    R["page"] = P(b + "/products/158977", keep=0)
    t = T(b + "/products/158977")
    R["nd"] = sn(t, r"styleCode|modelCode|modelNo|productCode|productNo|manufactur|originalPrice|retailPrice|consumerPrice|listPrice|salePrice", 14, 200, 40)
    js = T(b + "/_next/static/chunks/pages/search-a97ec0165957c27c.js")
    R["js_search"] = sn(js, r"/v2/search|baseURL|api\.worksout|https://api", 10, 240, 120)
    app = T(b + "/_next/static/chunks/pages/_app-a203cfe84ba917de.js")
    R["app_api"] = sorted(set(re.findall(r"https://[a-z0-9.\-]*worksout[a-z0-9.\-]*\.[a-z.]+", app)))[:20]
    for h in R["app_api"][:4]:
        try:
            rr = pf.requests.get(h + "/robots.txt", headers=pf.HDR, timeout=15, allow_redirects=False)
            R.setdefault("api_robots", []).append([h, rr.status_code, rr.text[:300]])
        except Exception as e:
            R.setdefault("api_robots", []).append([h, f"{type(e).__name__}"])


def kream(R):
    b = "https://kream.co.kr"
    R["items"] = []
    for c in ["MR530SG", "DD1391-100", "VN000D3HY28", "U740BM2"]:
        x = page(f"{b}/search?keyword={urllib.parse.quote(c)}", c)
        if not isinstance(x, tuple):
            R["items"].append(x); continue
        d, t = x
        pl = []
        for m in re.finditer(r'href="(/products/\d+)"', t):
            near = t[max(0, m.start() - 1500): m.end() + 1500]
            if re.search(re.escape(c), near) and m.group(1) not in pl:
                pl.append(m.group(1))
        it = {"c": c, "st": d.get("st"), "len": d.get("len"), "code_hits": d.get("code_hits"), "plinks": pl[:4]}
        if pl:
            pp = page(b + pl[0], c)
            if isinstance(pp, tuple):
                dd, tt = pp
                it["page"] = {"title": dd["title"], "ld": dd["ld"], "rel": sn(tt, r"발매가|모델번호|출시일|대표 색상", 8, 120, 20), "code_hits": dd.get("code_hits")}
            else:
                it["page"] = pp
        R["items"].append(it)


SITES2 = {"에스마켓": smarket, "슈마커": shoemarker, "폴더": folder, "ABC마트": lambda R: art(R, "abcmart.a-rt.com", "10001"),
          "그랜드스테이지": lambda R: art(R, "grandstage.a-rt.com", "10002"), "카시나": kasina, "웍스아웃": worksout, "크림": kream}


def work(R):
    pf._PACE.clear()
    def run(b):
        pf._TL.c = pf._Ctx()
        res = {"t0": time.time()}
        try:
            SITES2[b](res)
        except Exception:
            res["fatal"] = traceback.format_exc()[-1500:]
        res["sec"] = round(time.time() - res.pop("t0"))
        return b, res
    with ThreadPoolExecutor(8) as ex:
        for b, res in ex.map(run, list(SITES2)):
            R.setdefault("sites", {})[b] = res
    R["blocked"] = sorted(pf._BLOCKED)


def main():
    R, buf = {"start": time.time(), "ua": pf.UA}, io.StringIO()
    try:
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            work(R)
    except BaseException:
        R["fatal"] = traceback.format_exc()[-3000:]
    R["log"] = buf.getvalue()[-60000:]
    R["sec"] = round(time.time() - R["start"])
    enc_out(R)
    print("probe done", R["sec"])


if __name__ == "__main__":
    main()

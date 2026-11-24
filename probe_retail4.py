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
                                 str(o.get("priceSpecification", ""))[:200], str(o.get("lowPrice", ""))[:12], str(o.get("highPrice", ""))[:12]] for o in ofl[:4] if isinstance(o, dict)]})
    return out[:4]


def rawsnips(t, rx, n=6, w=220, back=80):
    return [re.sub(r"\s+", " ", t[max(0, m.start() - back): m.start() + w]) for m in list(re.finditer(rx, t, re.I))[:n]]


CODES = ["B75806", "MR530SG", "DD1391-100", "VN000D3HY28"]   # 공개 대표 품번(아디다스 삼바 OG · 뉴발란스 530 · 나이키 덩크 로우 · 반스 올드스쿨)
SITES = {
    "슈마커": {"base": "https://www.shoemarker.co.kr", "search": ["/ASP/Product/SearchProductList.asp?SearchWord={c}", "/search?keyword={c}", "/search?searchWord={c}"]},
    "ABC마트": {"base": "https://abcmart.a-rt.com", "search": ["/display/search-word/result?searchWord={c}"]},
    "그랜드스테이지": {"base": "https://grandstage.a-rt.com", "search": ["/display/search-word/result?searchWord={c}&chnnlNo=10002"]},
    "폴더": {"base": "https://www.folderstyle.com", "search": ["/shop/shopbrand.html?search={c}&type=Y"]},
    "카시나": {"base": "https://www.kasina.co.kr", "search": ["/search?keyword={c}", "/search?q={c}", "/product/search.html?keyword={c}"]},
    "웍스아웃": {"base": "https://www.worksout.co.kr", "search": ["/search?keyword={c}", "/search?q={c}", "/search?searchWord={c}"]},
    "크림": {"base": "https://kream.co.kr", "search": ["/search?keyword={c}"]},
    "에스마켓": {"base": "https://www.smarket.co.kr", "search": ["/goods/goods_search.php?keyword={c}"]},
}
PROD_RX = re.compile(r"""(?:href|data-href|data-url)=["']([^"'#]*(?:prdtNo=\d+|shopdetail\.html\?branduid=\d+|goods_view\.php\?goodsNo=\d+|/goods/\d+|/products?/[0-9A-Za-z_\-]+|product/detail\.html\?product_no=\d+|/product/[^"'/]+/\d+|ProductDetail[^"']*|/p/[0-9A-Za-z_\-]+)[^"'#]*)["']""", re.I)
PLATFORM = {"godo": r"godomall|/data/skin/|set_goods_fixedPrice|gd_goods", "cafe24": r"cafe24|ec-base|/web/product/|EC_FRONT", "makeshop": r"makeshop|shopdetail\.html|MS_input",
            "shopify": r"cdn\.shopify|Shopify\.theme", "next": r"__NEXT_DATA__|/_next/static", "nuxt": r"__NUXT__|/_nuxt/", "shopby": r"shopby|e-ncp\.com|ncp-api|shop-api",
            "sixshop": r"sixshop", "imweb": r"imweb", "a-rt": r"image\.a-rt\.com|artfo", "asp": r"\.asp[\"'?]", "spa_root": r"<div id=\"(?:root|app|__next|__nuxt)\"", "angular": r"ng-version|ng-app"}
API_RX = [re.compile(r"""["'`](/(?:[A-Za-z0-9_\-]+/){0,6}[A-Za-z0-9_\-.]*(?:search|Search|api/|ajax|Ajax)[A-Za-z0-9_\-/.]*)["'`?]"""),
          re.compile(r"""https?://[a-z0-9.\-]*(?:api|search|gw|gateway)[a-z0-9.\-]*\.(?:co\.kr|com|kr|net|io)[A-Za-z0-9_\-/.]*""")]
BLK = lambda e: bool(e) and bool(re.search(r"차단|막음|못 받음|응답 없음", e))


def hinfo(r):
    h = getattr(r, "headers", None) or {}
    return {k: str(h.get(k))[:80] for k in ("Server", "X-Powered-By", "Content-Type", "cf-ray", "x-amz-cf-id", "x-cache", "Via") if h.get(k)}


def plat(t):
    return [k for k, rx in PLATFORM.items() if re.search(rx, t, re.I)]


def forms(t):
    out = []
    for m in re.finditer(r"<form\b([^>]*)>(.*?)</form>", t, re.I | re.S):
        attrs, inner = m.group(1), m.group(2)
        act = (re.search(r'action=["\']([^"\']*)', attrs) or [None, ""])[1]
        names = re.findall(r'<input[^>]*name=["\']([^"\']+)["\'][^>]*>', inner, re.I)
        if any(re.search(r"search|keyword|query|sword|word|^q$|kwd", n, re.I) for n in names):
            out.append({"action": act[:120], "method": (re.search(r'method=["\']([^"\']*)', attrs) or [None, ""])[1][:8], "names": names[:12]})
    return out[:6]


def page_info(u, code=None):
    r, e = tg(u)
    if e:
        return {"u": u[-120:], "err": e}
    t = r.text
    d = {"u": u[-120:], "final": r.url[-120:], "st": r.status_code, "len": len(t), "hdr": hinfo(r), "plat": plat(t),
         "title": (re.search(r"<title[^>]*>([^<]{0,140})", t) or [None, ""])[1].strip(), "ld": ld_all(t),
         "won": rawsnips(t, r"\d{1,3}(?:,\d{3})+\s*(?:원|<)", 10, 70, 160),
         "fields": rawsnips(t, r"(?:정상가|판매가|소비자가|발매가|할인가|최초 발매가|정가|스타일|모델명|모델번호|품번|상품코드|자체상품코드|fixedPrice|normalAmt|sellAmt|prdtPrice|consumer|retail_price|originalPrice|regularPrice|listPrice)", 16, 150, 50),
         "meta": rawsnips(t, r"(?:og:price|product:price|itemprop=\"price\"|og:title|og:description)", 6, 200, 10),
         "next": bool(re.search(r"__NEXT_DATA__", t)), "nuxt": bool(re.search(r"__NUXT__", t))}
    if code:
        d["code_hits"] = len(re.findall(re.escape(code), t, re.I))
        d["code"] = rawsnips(t, re.escape(code), 5, 220, 120)
    return d


def site_api(R, base, html, page_url):
    """화면 스크립트 속 검색·API 주소 후보(글자만 모음 — 호출은 'search'가 든 같은 사이트 검색 주소만, robots 허용일 때)"""
    cands, scripts = [], []
    for s in re.findall(r'<script[^>]*src=["\']([^"\']+)["\']', html, re.I):
        su = urllib.parse.urljoin(page_url, unescape(s))
        if re.search(r"jquery|plugins?/|polyfill|gtag|google|facebook|kakao|naver|criteo|channel\.io|braze|amplitude|sentry|datadog|appsflyer|onelink|adobe|hotjar|clarity|tiktok", su, re.I):
            continue
        scripts.append(su)
    R["scripts_n"] = len(scripts); R["scripts"] = [x[-110:] for x in scripts[:25]]
    texts = [html]
    pref = [x for x in scripts if re.search(r"search|result|display|main|app|index|page|common", x, re.I)][:6]
    R["scripts_read"] = []
    for su in pref:
        r, e = tg(su)
        R["scripts_read"].append([su[-100:], e or len(r.text)])
        if not e:
            texts.append(r.text[:3_000_000])
    for t in texts:
        for rx in API_RX:
            for m in rx.findall(t):
                if m not in cands and not re.search(r"\.(?:png|jpg|gif|svg|css|woff2?)$", m, re.I):
                    cands.append(m)
    R["api_cands"] = cands[:80]
    return cands


def search_try(R, cfg):
    base = cfg["base"]
    out, found = [], None
    for tmpl in cfg["search"] + R.get("form_tmpls", []):
        for c in CODES:
            u = base + tmpl.format(c=urllib.parse.quote(c))
            ok, why = pf.robots_ok(u)
            if not ok:
                out.append({"u": u[-120:], "robots": why}); break
            r, e = tg(u)
            if e:
                out.append({"u": u[-120:], "err": e})
                if BLK(e):
                    R["search"] = out; return None
                break
            t = r.text
            pl = []
            for m in PROD_RX.finditer(t):
                lu = urllib.parse.urljoin(r.url, unescape(m.group(1)))
                near = t[max(0, m.start() - 700): m.end() + 700]
                if lu not in [x[0] for x in pl]:
                    pl.append([lu, bool(re.search(re.escape(c), near, re.I))])
            out.append({"c": c, "u": u[-120:], "final": r.url[-120:], "st": r.status_code, "len": len(t), "hdr": hinfo(r), "plat": plat(t),
                        "code_hits": len(re.findall(re.escape(c), t, re.I)), "code": rawsnips(t, re.escape(c), 4, 220, 120),
                        "links": [[x[0][-120:], x[1]] for x in pl[:12]], "links_n": len(pl), "next": bool(re.search(r"__NEXT_DATA__", t)),
                        "won_n": len(re.findall(r"\d{1,3}(?:,\d{3})+\s*원", t)), "noresult": bool(re.search(r"검색\s*결과가\s*없|결과가 없습니다|no results", t, re.I))})
            near = [x for x in pl if x[1]]
            if near:
                found = (near[0][0], c); break
        if found:
            break
    R["search"] = out
    return found


def site(R, name):
    cfg = SITES[name]; base = cfg["base"]; t0 = time.time()
    try:
        rr = pf.requests.get(base + "/robots.txt", headers=pf.HDR, timeout=20, allow_redirects=False)
        R["robots_raw"] = {"st": rr.status_code, "loc": rr.headers.get("Location"), "txt": rr.text[:2500] if rr.status_code == 200 else rr.text[:200], "hdr": hinfo(rr)}
    except Exception as e:
        R["robots_raw"] = {"err": f"{type(e).__name__}: {str(e)[:150]}"}
    for p in ["/"] + [s.split("?")[0] for s in cfg["search"]] + ["/products/1", "/product/1", "/goods/goods_view.php?goodsNo=1", "/product/new?prdtNo=1", "/shop/shopdetail.html?branduid=1"]:
        ok, why = pf.robots_ok(base + p)
        R.setdefault("robots_paths", []).append([p, ok, why])
    hr, he = tg(base + "/")
    if he:
        R["home"] = {"err": he}
        if BLK(he):
            return
        html, hurl = "", base + "/"
    else:
        html, hurl = hr.text, hr.url
        R["home"] = {"final": hr.url[-100:], "st": hr.status_code, "len": len(html), "hdr": hinfo(hr), "plat": plat(html),
                     "title": (re.search(r"<title[^>]*>([^<]{0,140})", html) or [None, ""])[1].strip(), "forms": forms(html),
                     "meta_gen": rawsnips(html, r'name="generator"', 2, 120, 10), "prod_links": [m.group(1)[-100:] for m in list(PROD_RX.finditer(html))[:10]]}
        tm = []
        for f in R["home"]["forms"]:
            act = f["action"] or ""
            if act.startswith("http") and urllib.parse.urlsplit(act).netloc != urllib.parse.urlsplit(base).netloc:
                continue
            path = urllib.parse.urlsplit(act).path or "/"
            nm = next((n for n in f["names"] if re.search(r"keyword|search|query|sword|word|^q$|kwd", n, re.I)), None)
            if nm and (f["method"] or "get").lower() != "post":
                tm.append(f"{path}?{nm}={{c}}")
        R["form_tmpls"] = [x for x in dict.fromkeys(tm) if x not in cfg["search"]][:3]
    sm = re.findall(r"(?im)^\s*sitemap:\s*(\S+)", (R.get("robots_raw") or {}).get("txt") or "")
    R["sitemaps"] = sm[:6]
    if sm:
        r, e = tg(sm[0])
        R["sitemap0"] = {"u": sm[0][-100:], "err": e} if e else {"u": sm[0][-100:], "len": len(r.text), "locs": len(re.findall(r"<loc>", r.text)), "head": re.findall(r"<loc>([^<]{0,140})</loc>", r.text)[:8]}
    found = search_try(R, cfg)
    if found:
        R["product"] = page_info(found[0], found[1])
        return
    if time.time() - t0 > T_SITE - 60 or urllib.parse.urlsplit(base).netloc in pf._BLOCKED:
        return
    r, e = tg(base + cfg["search"][0].format(c=CODES[0]))
    if e:
        return
    cands = site_api(R, base, r.text, r.url)
    tries = []
    for cnd in [x for x in cands if re.search(r"search", x, re.I) and not x.startswith("http")][:8]:
        for prm in (["searchWord"] if "a-rt" in base else ["keyword", "q", "searchWord", "query"]):
            if time.time() - t0 > T_SITE - 30:
                break
            u = base + cnd + ("&" if "?" in cnd else "?") + f"{prm}={CODES[0]}"
            ok, why = pf.robots_ok(u)
            if not ok:
                tries.append([u[-120:], why]); break
            rr, ee = tg(u)
            if ee:
                tries.append([u[-120:], ee])
                if BLK(ee):
                    break
                continue
            tt = rr.text
            tries.append([u[-120:], rr.status_code, len(tt), (rr.headers.get("Content-Type") or "")[:40], len(re.findall(re.escape(CODES[0]), tt)),
                          rawsnips(tt, re.escape(CODES[0]), 2, 200, 100), [m.group(1)[-100:] for m in list(PROD_RX.finditer(tt))[:5]],
                          rawsnips(tt, r"prdtNo|goodsNo|productNo|itemNo|product_no", 3, 120, 20)])
            if len(re.findall(re.escape(CODES[0]), tt)):
                break   # 이 주소는 품번을 찾음 — 다른 이름 칸은 안 물음
        if len(tries) >= 12:
            break
    R["api_tries"] = tries
    pls = [x for tr in tries if len(tr) > 6 for x in tr[6]]
    if pls and time.time() - t0 < T_SITE - 20:
        R["product_from_api"] = page_info(urllib.parse.urljoin(base + "/", pls[0]), CODES[0])


def work(R):
    pf._PACE.clear()
    def run(b):
        pf._TL.c = pf._Ctx()
        res = {"t0": time.time()}
        try:
            site(res, b)
        except Exception:
            res["fatal"] = traceback.format_exc()[-1500:]
        res["sec"] = round(time.time() - res.pop("t0"))
        return b, res
    with ThreadPoolExecutor(8) as ex:
        for b, res in ex.map(run, list(SITES)):
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

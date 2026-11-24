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
    t = T(b + "/goods/brand.php")
    R["brands"] = sorted(set(re.findall(r'brandCd=\w+[^>]*>\s*([^<]{2,40}?)\s*<', t)))[:120]
    R["brand_names_any"] = [x for x in ["나이키", "NIKE", "아디다스", "ADIDAS", "뉴발란스", "NEW BALANCE", "반스", "VANS", "컨버스", "CONVERSE", "푸마", "PUMA", "아식스", "ASICS", "크록스", "CROCS", "호카", "HOKA"] if re.search(re.escape(x), t, re.I)]
    R["search"] = []
    for c in ["아디다스", "나이키", "뉴발란스", "반스"]:
        u = f"{b}/goods/goods_search.php?keyword={urllib.parse.quote(c)}"
        x = page(u)
        if not isinstance(x, tuple):
            R["search"].append(x); continue
        d, tt = x
        d["plinks"] = links(tt, u, r"goods_view\.php\?goodsNo=\d+", 12)
        d["nores"] = bool(re.search(r"검색결과가 없|검색된 상품이 없|0개의 상품", tt))
        d["cnt"] = sn(tt, r"검색결과|개의 상품|총\s*<", 3, 140, 30)
        d.pop("fields", None); d.pop("codes", None)
        R["search"].append(d)
    R["pages"] = []
    for s in R["search"][:3]:
        for lu in (s.get("plinks") or [])[:1]:
            R["pages"].append(P(lu))


def shoemarker(R):
    b = "https://www.shoemarker.co.kr"
    js = T(f"{b}/ASP/Product/JS/SearchProductList.js") + T(f"{b}/ASP/Product/JS/SearchProduct.js")
    R["ajax_urls"] = sorted(set(re.findall(r'url\s*:\s*["\']([^"\']+)["\']', js)))
    R["ajax_snips"] = sn(js, r'url\s*:\s*["\'][^"\']*(?:ProductList|List_Ajax|ListAjax|Search)', 8, 260, 120)
    u = f"{b}/ASP/Product/SearchProductList.asp?SearchWord=B75806"
    x = page(u)
    if isinstance(x, tuple):
        t = x[1]
        fm = re.search(r'<form[^>]*(?:name|id)="frm"[^>]*>(.*?)</form>', t, re.S | re.I)
        R["frm"] = re.findall(r'<input[^>]*name="([^"]+)"[^>]*value="([^"]*)"', fm.group(1))[:40] if fm else None
        R["list_markers"] = sn(t, r'id="SearchProductList"|id="SearchProductNone"|SearchProductList_Ajax|ProductList_Ajax', 4, 240, 60)
    cand = [a for a in R["ajax_urls"] if re.search(r"Product.*List|List.*Product", a, re.I) and not re.search(r"Category|Brand|Size|Color|Price", a, re.I)]
    R["cand"] = cand
    R["post"] = []
    for a in cand[:2]:
        pu = urllib.parse.urljoin(b + "/ASP/Product/", a)
        ok, why = pf.robots_ok(pu)
        if not ok:
            R["post"].append([pu, why]); continue
        data = dict(R.get("frm") or [])
        data["SearchWord"] = "B75806"
        try:
            time.sleep(1.5)
            rr = pf._ctx().sess.post(pu, data=data, headers=pf.HDR, timeout=25, allow_redirects=False)
            tt = rr.text
            pl = links(tt, pu, r"ProductDetail\.asp\?ProductCode=\d+", 6)
            R["post"].append({"u": pu[-100:], "st": rr.status_code, "len": len(tt), "hits": len(re.findall("B75806", tt)), "plinks": pl, "snip": sn(tt, r"B75806|ProductCode=", 3, 200, 80)})
            if pl:
                R["page"] = P(pl[0], "B75806")
                break
        except Exception as e:
            R["post"].append([pu, f"{type(e).__name__}: {str(e)[:120]}"])


def folder(R):
    b = "https://www.folderstyle.com"
    x = page(f"{b}/shop/shopbrand.html?search=B75806&type=Y")
    if isinstance(x, tuple):
        pl = links(x[1], b + "/shop/", r"shopdetail\.html\?branduid=\d+", 3)
        R["plinks"] = pl
        if pl:
            R["page_full"] = P(pl[0], "B75806")
            bu = re.search(r"branduid=(\d+)", pl[0]).group(1)
            R["page_bare"] = P(f"{b}/shop/shopdetail.html?branduid={bu}", "B75806")
    else:
        R["err"] = x


def art(R, host, ch):
    b = f"https://{host}"
    R["tries"] = []
    for path in ["/display/search-word/result-total/list", "/display/search-word/result/list"]:
        u = f"{b}{path}?searchWord=B75806&page=1&perPage=30&tabGubun=total&sort=&chnnlNo={ch}&channel={ch}"
        r, e = tg(u)
        if e:
            R["tries"].append([u[-120:], e]); continue
        t = r.text
        d = {"u": u[-120:], "st": r.status_code, "len": len(t), "ctype": r.headers.get("Content-Type"), "hits": len(re.findall("B75806", t)), "head": t[:600]}
        try:
            j = r.json()
            d["keys"] = list(j.keys())[:40] if isinstance(j, dict) else type(j).__name__
            def walk(o, path=""):
                if isinstance(o, dict):
                    for k, v in o.items():
                        if isinstance(v, list) and v and isinstance(v[0], dict) and any(re.search(r"prdt|product", kk, re.I) for kk in v[0].keys()):
                            return path + "/" + k, v
                        got = walk(v, path + "/" + k)
                        if got: return got
                return None
            got = walk(j)
            if got:
                d["list_path"], lst = got[0], got[1]
                d["n"] = len(lst); d["first_keys"] = list(lst[0].keys())[:80]
                d["first"] = {k: lst[0][k] for k in list(lst[0].keys()) if re.search(r"prdt|name|nm|amt|price|style|model|brand|code|no$|Rt|rate", k, re.I)}
                d["first"] = {k: str(v)[:80] for k, v in list(d["first"].items())[:40]}
                d["prdtNos"] = [str(x.get("prdtNo") or x.get("productNo") or "") for x in lst[:5]]
        except Exception as ee:
            d["json_err"] = f"{type(ee).__name__}"
            d["plinks"] = links(t, u, r"prdtNo=\d+", 5)
        R["tries"].append(d)
        if d.get("prdtNos") or d.get("plinks"):
            pn = (d.get("prdtNos") or [None])[0] or re.search(r"prdtNo=(\d+)", d["plinks"][0]).group(1)
            R["page"] = P(f"{b}/product/new?prdtNo={pn}", "B75806")
            break


def kasina(R):
    b = "https://www.kasina.co.kr"
    x = page(b + "/")
    t = x[1] if isinstance(x, tuple) else ""
    R["scripts"] = re.findall(r'<script[^>]*src="([^"]+)"', t)[:30]
    bid = (re.search(r'"buildId"\s*:\s*"([^"]+)"', t) or [None, None])[1]
    mf = [s for s in R["scripts"] if "_buildManifest" in s]
    mu = urllib.parse.urljoin(b + "/", mf[0]) if mf else f"{b}/_next/static/{bid}/_buildManifest.js"
    r, e = tg(mu)
    R["manifest"] = {"u": mu[-100:], "err": e, "len": len(r.text) if not e else None}
    if not e:
        R["routes"] = sorted(set(re.findall(r'"(/[^"]*)"\s*:', r.text)))[:150]
        R["routes2"] = sorted(set(re.findall(r'(/[a-z\-\[\]]+(?:/[a-z\-\[\]]+)*)', r.text)))[:150]
    rts = (R.get("routes") or []) + (R.get("routes2") or [])
    R["search_tries"] = []
    for rt in [r for r in dict.fromkeys(rts) if "search" in r.lower()][:3]:
        u = b + re.sub(r"\[[^\]]+\]", "B75806", rt) + ("" if "[" in rt else "?keyword=B75806")
        x = page(u, "B75806")
        d = x[0] if isinstance(x, tuple) else x
        if isinstance(x, tuple):
            d["plinks"] = links(x[1], u, r"/products?/\d+|/goods/\d+", 6); d.pop("fields", None)
        R["search_tries"].append(d)
    pl = [lu for s in R["search_tries"] for lu in (s.get("plinks") or [])]
    if pl:
        R["page"] = P(pl[0], "B75806")


def kream(R):
    b = "https://kream.co.kr"
    R["items"] = []
    for c in ["MR530SG", "DD1391-100", "U740BM2"]:
        x = page(f"{b}/search?keyword={urllib.parse.quote(c)}", c)
        if not isinstance(x, tuple):
            R["items"].append(x); continue
        d, t = x
        ids = list(dict.fromkeys(re.findall(r"/products/(\d+)", t)))[:6]
        it = {"c": c, "ids": ids}
        for pid in ids[:3]:
            pp = page(f"{b}/products/{pid}", c)
            if isinstance(pp, tuple):
                dd, tt = pp
                rel = sn(tt, r"발매가|모델번호", 6, 60, 0)
                if dd.get("code_hits"):
                    it["page"] = {"pid": pid, "title": dd["title"], "ld": dd["ld"], "rel": rel}
                    break
                it.setdefault("miss", []).append([pid, dd["title"][:60], rel[:2]])
            else:
                it.setdefault("miss", []).append([pid, pp])
        R["items"].append(it)


SITES2 = {"에스마켓": smarket, "슈마커": shoemarker, "폴더": folder, "ABC마트": lambda R: art(R, "abcmart.a-rt.com", "10001"),
          "그랜드스테이지": lambda R: art(R, "grandstage.a-rt.com", "10002"), "카시나": kasina, "크림": kream}

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

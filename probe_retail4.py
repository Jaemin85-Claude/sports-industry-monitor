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




def shoemarker(R):
    b = "https://www.shoemarker.co.kr"
    pu = b + "/ASP/Product/Ajax/SearchProductList.asp"
    x = page(f"{b}/ASP/Product/SearchProductList.asp?SearchWord=MR530SG")
    t = x[1] if isinstance(x, tuple) else ""
    fm = re.search(r'<form[^>]*(?:name|id)="frm"[^>]*>(.*?)</form>', t, re.S | re.I)
    base = dict(re.findall(r'<input[^>]*name="([^"]+)"[^>]*value="([^"]*)"', fm.group(1))) if fm else {}
    js = T(f"{b}/ASP/Product/JS/SearchProductList.js")
    R["list_fn"] = sn(js, r'SearchProductList\.asp', 3, 500, 400)
    R["post"] = []
    ok, why = pf.robots_ok(pu)
    if not ok:
        R["post"] = why; return
    for c in ["MR530SG", "U740BM2", "1203A243", "뉴발란스", "나이키"]:
        data = dict(base); data["SearchWord"] = c
        try:
            time.sleep(2)
            rr = pf._ctx().sess.post(pu, data=data, headers={**pf.HDR, "X-Requested-With": "XMLHttpRequest", "Referer": f"{b}/ASP/Product/SearchProductList.asp?SearchWord={urllib.parse.quote(c)}"}, timeout=25, allow_redirects=False)
            tt = rr.text
            pl = links(tt, pu, r"ProductDetail\.asp\?ProductCode=\d+", 6)
            R["post"].append({"c": c, "st": rr.status_code, "len": len(tt), "hits": len(re.findall(re.escape(c), tt)), "plinks": pl, "head": tt[:300]})
            if pl and "page" not in R and re.match(r"[A-Z0-9]", c):
                R["page"] = P(pl[0], c)
        except Exception as e:
            R["post"].append([c, f"{type(e).__name__}: {str(e)[:120]}"])
    if "page" not in R:
        for p in R["post"]:
            if isinstance(p, dict) and p.get("plinks"):
                R["page_kw"] = P(p["plinks"][0]); break


def art(R, host, ch):
    b = f"https://{host}"
    u = f"{b}/display/search-word/result-total/list?searchWord=B75806&page=1&perPage=30&tabGubun=total&sort=&chnnlNo={ch}&channel={ch}"
    r, e = tg(u)
    if e:
        R["err"] = e; return
    j = r.json()
    R["SEARCH"] = json.dumps(j.get("SEARCH"), ensure_ascii=False)[:3500]
    R["SEARCH_COUNT"] = j.get("SEARCH_COUNT"); R["GROUP"] = j.get("GROUP_COUNT_CHNNL_NO"); R["PAGE"] = str(j.get("PAGE"))[:300]
    R["SEARCH_VO"] = json.dumps(j.get("SEARCH_VO"), ensure_ascii=False)[:600]
    pn = re.findall(r'"(?:prdtNo|PRDT_NO|productNo)"\s*:\s*"?(\d+)', json.dumps(j))
    R["prdtNos"] = pn[:6]
    if pn:
        R["page"] = P(f"{b}/product/new?prdtNo={pn[0]}", "B75806")


def kasina(R):
    b = "https://www.kasina.co.kr"
    R["list"] = []
    for u in [f"{b}/products?keyword=B75806", f"{b}/products?searchKeyword=B75806", f"{b}/products"]:
        x = page(u, "B75806")
        if not isinstance(x, tuple):
            R["list"].append(x); continue
        d, t = x
        d["pd"] = list(dict.fromkeys(re.findall(r"/product-detail/(\d+)", t)))[:6]
        d["nd"] = sn(t, r"productNo|salePrice|immediateDiscount|productName|productManagementCd|hsCode|modelNo|styleCode", 8, 160, 30)
        d.pop("fields", None)
        R["list"].append(d)
        if d["pd"]:
            R["page"] = P(f"{b}/product-detail/{d['pd'][0]}")
            pt = T(f"{b}/product-detail/{d['pd'][0]}")
            R["page_nd"] = sn(pt, r"productManagementCd|productNo|salePrice|immediateDiscountAmt|listPrice|originPrice|modelNo|styleCode|productCode|optionManagementCd|consumerPrice", 14, 180, 40)
            break


SITES2 = {"슈마커": shoemarker, "ABC마트": lambda R: art(R, "abcmart.a-rt.com", "10001"),
          "그랜드스테이지": lambda R: art(R, "grandstage.a-rt.com", "10002"), "카시나": kasina}

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

# 임시 시험(병합 안 함 · PR 전에 지움): 국내 공식몰 접속 시험 — 우리 봇 이름 · robots.txt 준수 · 봇 확인 화면이면 멈춤(우회 없음) · 공개 상품 품번만 모음 · 결과는 암호화해서만 찍음
import base64, contextlib, io, json, os, re, subprocess, tempfile, threading, time, traceback, urllib.parse, zlib
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
-----END PUBLIC KEY-----
"""
PLAN = {
 "MAISON KITSUNE": [
  {
   "url": "https://www.ssfshop.com/"
  },
  {
   "url": "https://maisonkitsune.com/kr/"
  }
 ],
 "GANNI": [
  {
   "url": "https://www.ganni.com/en-kr/"
  }
 ],
 "NEW BALANCE": [
  {
   "url": "https://www.nbkorea.com/",
   "old_ua": true
  }
 ],
 "SPORTY AND RICH": [
  {
   "url": "https://www.kurly.com/"
  }
 ],
 "MELISSA": [
  {
   "url": "https://kream.co.kr/"
  },
  {
   "url": "https://www.29cm.co.kr/"
  }
 ],
 "ADIDAS": [
  {
   "url": "https://www.adidas.co.kr/",
   "old_ua": true
  }
 ],
 "WILD DONKEY": [
  {
   "url": "https://www.wconcept.co.kr/"
  }
 ],
 "CONVERSE": [
  {
   "url": "https://www.converse.co.kr/"
  }
 ],
 "STUSSY": [
  {
   "url": "https://kr.stussy.com/"
  }
 ],
 "UGG": [
  {
   "url": "https://www.sivillage.com/",
   "old_ua": true
  }
 ],
 "AMI": [
  {
   "url": "https://www.amiparis.com/ko-kr"
  }
 ],
 "DROLE DE MONSIEUR": [
  {
   "url": "https://www.kolonmall.com/Brands/DROLEDEMONSIEUR"
  }
 ],
 "PALOMAWOOL": [
  {
   "url": "https://www.kolonmall.com/Search?keyword=palomawool"
  }
 ],
 "ISABEL MARANT": [
  {
   "url": "https://www.lfmall.co.kr/"
  }
 ],
 "VANS": [
  {
   "url": "https://www.vans.co.kr/"
  }
 ],
 "OUR LEGACY": [
  {
   "url": "https://www.thehandsome.com/"
  }
 ],
 "APC": [
  {
   "url": "https://www.idlookmall.com/"
  }
 ]
}


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


def tryget(u):
    try:
        return pf.get(u), None
    except Exception as e:
        return None, f"{type(e).__name__}: {str(e)[:160]}"


def platform(t):
    marks = []
    for name, rx in (("shopify", r"cdn\.shopify\.com|Shopify\.theme|shopify-section"), ("cafe24", r"cafe24|/product/detail\.html|ec-base"),
                     ("godo", r"goods_view\.php|godomall"), ("magento", r"Magento|mage/|static/version"), ("sfcc", r"demandware|dwvar_"),
                     ("nextjs", r"__NEXT_DATA__|/_next/static"), ("makeshop", r"makeshop"), ("imweb", r"imweb"), ("sixshop", r"sixshop"),
                     ("wordpress", r"wp-content"), ("vtex", r"vtex"), ("salesforce", r"salesforce")):
        if re.search(rx, t, re.I):
            marks.append(name)
    return marks


def ld_bits(t):
    out = []
    for n in pf._ld_nodes(t):
        ty = pf._types(n)
        if ty & {"product", "productgroup"}:
            offers = n.get("offers")
            ofl = offers if isinstance(offers, list) else [offers] if isinstance(offers, dict) else []
            out.append({"name": str(n.get("name") or "")[:80], "sku": str(n.get("sku") or "")[:40], "mpn": str(n.get("mpn") or "")[:40],
                        "pid": str(n.get("productID") or "")[:40], "price": [str((o or {}).get("price"))[:20] for o in ofl[:3]],
                        "cur": [str((o or {}).get("priceCurrency"))[:6] for o in ofl[:3]]})
    return out[:3]


def probe_site(brand, url):
    R = {"url": url}
    sp = urllib.parse.urlsplit(url); base = f"{sp.scheme}://{sp.netloc}"
    ok, why = pf.robots_ok(url)
    R["robots_home"] = "ok" if ok else why
    r, err = tryget(url)
    if err:
        R["home"] = err; return R
    t = r.text
    R["home"] = {"final": r.url, "len": len(t), "title": (re.search(r"<title[^>]*>([^<]{0,100})", t) or [None, ""])[1].strip(), "platform": platform(t),
                 "krw": bool(re.search(r"\d{1,3}(?:,\d{3})+\s*원|₩|KRW", t))}
    base = "{0.scheme}://{0.netloc}".format(urllib.parse.urlsplit(r.url))
    fsp = urllib.parse.urlsplit(r.url)
    pre = fsp.path.rstrip("/") if re.match(r"^/(ko|kr|ko-kr|kr-ko|ko_kr)(/|$)", fsp.path, re.I) else ""
    codes, urls, titles, pages = set(), [], [], []
    # 쇼피파이 공개 상품 목록
    if "shopify" in R["home"]["platform"]:
        n = 0
        for page in range(1, 9):
            rr, e2 = tryget(f"{base}{pre}/products.json?limit=250&page={page}")
            if e2:
                R["products_json"] = e2; break
            try:
                ps = rr.json().get("products") or []
            except Exception:
                R["products_json"] = "JSON 아님"; break
            for p in ps:
                n += 1
                titles.append(str(p.get("title") or "")[:60]); urls.append(str(p.get("handle") or ""))
                for v in p.get("variants") or []:
                    if v.get("sku"): codes.add(str(v["sku"])[:40])
                if len(pages) < 3:
                    pages.append({"handle": p.get("handle"), "prices": sorted({(v.get("price"), v.get("compare_at_price")) for v in (p.get("variants") or [])[:5]}, key=str)[:3]})
            if len(ps) < 250:
                break
        R["shopify_n"] = n
    # 사이트맵
    maps = []
    rr, e2 = tryget(f"{base}/robots.txt")
    if not e2:
        maps = [l.split(":", 1)[1].strip() for l in rr.text.splitlines() if l.lower().startswith("sitemap:")]
        R["robots_maps"] = maps[:6]
    if not maps:
        maps = [f"{base}/sitemap.xml"]
    try:
        host = urllib.parse.urlsplit(base).netloc
        sm = pf._sm_walk(maps[:4], host, "/", max_maps=8, budget=60)
        prod = [u for u in sm if re.search(r"product|goods|/p/|/item|detail|/shop/", u, re.I)] or sm
        R["sitemap_n"] = len(sm); R["sitemap_prod_n"] = len(prod)
        urls += prod[:3000]
    except Exception as e:
        R["sitemap"] = f"{type(e).__name__}: {str(e)[:100]}"
    # 상품 페이지 3개 — JSON-LD 품번·가격
    samp = [u for u in urls if u.startswith("http")][:3] or ([f"{base}{pre}/products/{h}" for h in urls[:3]] if "shopify" in R["home"]["platform"] else [])
    for u in samp[:3]:
        rr, e2 = tryget(u)
        if e2:
            pages.append({"u": u[-80:], "err": e2}); continue
        pages.append({"u": u[-80:], "ld": ld_bits(rr.text), "len": len(rr.text), "krw": bool(re.search(r"\d{1,3}(?:,\d{3})+\s*원|₩|KRW", rr.text))})
    R["codes"] = sorted(codes)[:6000]; R["urls"] = urls[:4000]; R["titles"] = titles[:300]; R["pages"] = pages
    return R


def work(R):
    pf._PACE.clear()
    jobs = [(b, x["url"]) for b, us in PLAN.items() for x in us]
    def run(bu):
        pf._TL.c = pf._Ctx()
        b, u = bu
        try:
            return b, probe_site(b, u)
        except Exception:
            return b, {"url": u, "fatal": traceback.format_exc()[-1500:]}
    with ThreadPoolExecutor(6) as ex:
        for b, res in ex.map(run, jobs):
            R.setdefault("sites", {}).setdefault(b, []).append(res)
    # 11-23 전에 우리 봇을 막은 사이트 — 11-23 전 접속 이름(OLD_UA)으로도(봇 이름 규칙 · 첫 화면·robots만)
    pf.HDR["User-Agent"] = pf.OLD_UA
    pf._BLOCKED.clear(); pf._ROB.clear() if hasattr(pf, "_ROB") else None
    pf._TL.c = pf._Ctx()
    for b, us in PLAN.items():
        for x in us:
            if x.get("old_ua"):
                ok, why = pf.robots_ok(x["url"])
                r, err = tryget(x["url"]) if ok else (None, why)
                R.setdefault("old_ua", {})[b] = {"robots": "ok" if ok else why, "home": err or {"len": len(r.text), "final": r.url}}
    pf.HDR["User-Agent"] = pf.UA


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
    print("probe done")


if __name__ == "__main__":
    main()

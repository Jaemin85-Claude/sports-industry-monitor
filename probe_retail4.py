# 임시 시험(병합 안 함 · 끝나면 바로 지움): 그랜드스테이지·ABC마트 검색 목록 정상가·할인 상품 페이지 + 슈마커 플러스 정가 칸 — 우리 봇 이름 · robots.txt 준수 · 봇 확인 화면이면 멈춤(우회 없음) · 공개 상품 정보만 모음 · 결과는 암호화해서만 찍음
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



PRICE_KEYS = re.compile(r"AMT|PRICE|RATE|DSCNT|DC_|COUPON|BRAND|STYLE|MNFTR|PRDT_NO|PRDT_NAME|CHNNL", re.I)


def art_rows(host, ch, word):
    u = f"https://{host}/display/search-word/result-total/list?searchWord={urllib.parse.quote(word)}&page=1&perPage=30&tabGubun=total&sort=&chnnlNo={ch}&channel={ch}"
    r, e = tg(u)
    if e:
        return None, e
    try:
        j = r.json()
    except Exception as ee:
        return None, f"JSON 아님 {type(ee).__name__}"
    rows = j.get("SEARCH") if isinstance(j.get("SEARCH"), list) else []
    return {"count": j.get("SEARCH_COUNT"), "group": j.get("GROUP_COUNT_CHNNL_NO"), "rows": rows}, None


def art_page(host, row):
    pn = str(row.get("PRDT_NO") or "")
    u = f"https://{host}/product/new?prdtNo={pn}"
    r, e = tg(u)
    if e:
        return {"u": u, "err": e}
    t = r.text
    na, dc = str(row.get("NRMAL_AMT") or ""), str(row.get("PRDT_DC_PRICE") or "")
    fmt = lambda v: f"{int(float(v)):,}" if re.fullmatch(r"\d+(\.\d+)?", v or "") else "?"
    return {"u": u[-60:], "st": r.status_code, "len": len(t), "title": (re.search(r"<title[^>]*>([^<]{0,120})", t) or [None, ""])[1].strip(),
            "og_price": sn(t, r"product:price:amount|product:sale_price|og:price", 3, 120, 10),
            "normal_on_page": t.count(fmt(na)), "dc_on_page": t.count(fmt(dc)), "style_on_page": t.count(str(row.get("STYLE_INFO") or "@@")),
            "price_blocks": sn(t, r"price-normal-cost|price-cost|정상가|판매가|할인가|normalAmt|sellAmt|prdtDcPrice|nrmalAmt|dscntRate|class=\"price", 14, 220, 60),
            "challenge": bool(re.search(r"turnstile|cf-chl|netfunnel", t[:20000], re.I))}




def realrun(R):
    for h_ in pf.SKU_KR_HOSTS:
        pf.HOST_GAP[h_] = max(pf.HOST_GAP.get(h_, 0), pf.KR_GAP)
    pf._PACE.update(pf.pace_map(pf.PRODUCTS))
    out = []
    cases = [("art", "언더아머", "6005377"), ("art", "아디다스", "JR3732"), ("art", "아디다스", "IH3990"), ("art", "뉴발란스", "M10804O2"), ("art", "아식스", "1203A591"),
             ("art", "아식스", "2011D580"), ("art", "반스", "VN0010CDH89"), ("kr", "뉴발란스", "U740BM2"), ("kr", "언더아머", "6009509"), ("kr", "아식스", "1012C071")]
    for how, b, q in cases:
        t0 = time.time()
        try:
            got, none = (pf._art_fetch(b, q, {q}) if how == "art" else pf._sku_fetch(b, "KR", q, {q}, None))
            out.append([how, b, q, round(time.time() - t0, 1), {k: (sorted(v) if isinstance(v, set) else [v[0], v[1], v[2], v[3], v[4], v[5]]) for k, v in got.items()}, none])
        except Exception as e:
            out.append([how, b, q, round(time.time() - t0, 1), "ERR " + type(e).__name__ + " " + str(e)[:160]])
    R["out"] = out

SITES2 = {"real": realrun}

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

# 임시 시험(병합 안 함 · 끝나면 바로 지움): 슈마커 플러스 품번 검색·목록 쪽 넘김·상품 페이지 정가·품번 칸 — 우리 봇 이름 · robots.txt 준수 · 봇 확인 화면이면 멈춤(우회 없음) · 공개 상품 정보만 · 결과는 암호화해서만 찍음
import base64, contextlib, io, json, os, re, subprocess, tempfile, time, traceback, urllib.parse, zlib
from html import unescape
from concurrent.futures import ThreadPoolExecutor
import price_fetch as pf
import requests

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




B = "https://plus.shoemarker.co.kr"
CARD = re.compile(r'ProductCode=(\d+)"[^>]*>\s*<div class="product-card__info">\s*<span class="product-card__brand">([^<]*)</span>\s*<span class="product-card__name">([^<]*)</span>(.{0,700}?)</a>', re.S)


def sn(t, rx, n=6, w=220, back=80):
    return [re.sub(r"\s+", " ", t[max(0, m.start() - back): m.start() + w]) for m in list(re.finditer(rx, t, re.I))[:n]]


def T(u):
    r, e = tg(u)
    return (r.text, r.url, r.status_code) if r is not None else (None, e, None)


def cards(t):
    out = []
    for pc, br, nm, rest in CARD.findall(t or ""):
        nums = re.findall(r'class="price__num">([\d,]+)<', rest)
        out.append([pc, br.strip(), unescape(nm).strip(), nums, "origin" in rest or "price__rate" in rest])
    seen, uniq = set(), []
    for c in out:
        if c[0] not in seen:
            seen.add(c[0]); uniq.append(c)
    return uniq


def search(q, extra=""):
    t, u, st = T(f"{B}/Product/ProductSearchList?SWord={urllib.parse.quote(q)}{extra}")
    if t is None:
        return {"q": q, "err": u}
    cs = cards(t)
    return {"q": q, "x": extra, "st": st, "final": str(u)[-120:], "n": len(cs), "cards": cs[:8],
            "total": [re.sub(r"<[^>]+>", "", s) for s in sn(t, r"count-num|검색 결과|총\s*<", 3, 160, 30)],
            "noresult": "검색 결과가 없습니다" in t}


def product(pc):
    t, u, st = T(f"{B}/Product/ProductDetail?ProductCode={pc}")
    if t is None:
        return {"pc": pc, "err": u}
    d = {"pc": pc, "st": st, "final": str(u)[-120:], "len": len(t)}
    d["hidden"] = [(a, b[:120]) for a, b in re.findall(r'<input[^>]+type="hidden"[^>]+name="([^"]+)"[^>]*value="([^"]*)"', t)][:120]
    d["hidden2"] = [(a, b[:120]) for b, a in re.findall(r'<input[^>]+value="([^"]*)"[^>]+name="([^"]+)"[^>]*type="hidden"', t)][:40]
    i = t.find('class="brand_code"')
    d["brand_code_ctx"] = re.sub(r"\s+", " ", t[max(0, i - 900): i + 300]) if i >= 0 else ""
    d["brand_codes"] = re.findall(r'class="brand_code">([^<]*)<', t)
    j = t.find('<div class="price">')
    d["price_block"] = re.sub(r"\s+", " ", t[j: j + 2200]) if j >= 0 else ""
    d["price_blocks_n"] = t.count('<div class="price">')
    d["origin_all"] = re.findall(r'class="price__origin">\s*<span class="price__num">([\d,]+)<', t)
    d["current_all"] = re.findall(r'class="price__current">\s*(?:<span class="price__rate">[^<]*</span>\s*)?<span class="price__num">([\d,]+)<', t)
    d["th_td"] = [(re.sub(r"<[^>]+>|\s+", " ", a).strip()[:40], re.sub(r"<[^>]+>|\s+", " ", b).strip()[:160]) for a, b in re.findall(r"<th[^>]*>(.*?)</th>\s*<td[^>]*>(.*?)</td>", t, re.S)][:40]
    d["tit_txt"] = [(re.sub(r"\s+", " ", a).strip()[:40], re.sub(r"\s+", " ", b).strip()[:160]) for a, b in re.findall(r'<span class="tit">([^<]*)</span>\s*<span class="txt">([^<]*)</span>', t)][:40]
    d["meta"] = re.findall(r'<meta[^>]+(?:property|name)="((?:og|product|twitter)[^"]*)"[^>]+content="([^"]{0,160})"', t)[:20]
    d["ld"] = len(re.findall(r"application/ld\+json", t))
    d["num7"] = sorted(set(re.findall(r"(?<![\d])1\d{6}(?:-[0-9A-Z]{2,5})?(?![\d])", t)))[:12]
    d["num7_ctx"] = sn(t, r"(?<![\d])1\d{6}(?![\d])", 6, 160, 120)
    d["asics"] = sorted(set(re.findall(r"(?<![0-9A-Z])[1-3]\d{3}[A-Z]\d{3}[-.]?\d{3}(?![0-9A-Z])", t)))[:8]
    d["sold"] = sn(t, r"품절|soldout|sold-out|일시품절", 4, 120, 60)
    d["size_opts"] = re.findall(r'data-size(?:cd|code)?="([^"]{0,20})"', t)[:30]
    d["brand_links"] = sorted(set(re.findall(r'href="(/Product/Brand[^"]{0,120})"', t)))[:10]
    d["scripts_prod"] = sorted(set(re.findall(r"""['"](/Product/[A-Za-z]+)['"]""", t)))[:20]
    return d


def work(R):
    pf.HOST_GAP["plus.shoemarker.co.kr"] = pf.KR_GAP
    R["robots"] = T(f"{B}/robots.txt")[0]
    R["search"] = [search(q) for q in ["U740BM2", "U740-BM2", "M10804O2", "1203B049-021", "1203B049", "1203B049021", "1147833", "IQ4183", "FZ7372", "HQ2056", "VN000D3HY28"]]
    R["brand_search"] = [search(q) for q in ["호카", "HOKA", "아디다스"]]
    t, u, st = T(f"{B}/Product/ProductSearchList?SWord={urllib.parse.quote('아디다스')}")
    R["paging_ctx"] = sn(t or "", r"paging|pagination|goPage|fnPage|name=\"Page\"|PageSize|pageNo|PageNo|btn_more|더보기", 14, 260, 120)
    R["script_urls"] = sorted(set(re.findall(r"""['"](/Product/[A-Za-z]+[^'"]{0,60})['"]""", t or "")))[:30]
    R["page_tries"] = [search("아디다스", x) for x in ["&Page=2", "&page=2", "&PageNo=2", "&Page=6"]]
    pages = {}
    for pc in ["55850", "55849", "55824", "55623", "55428", "56205", "55982", "55974", "30801", "55919"]:
        pages[pc] = product(pc)
    R["pages"] = pages
    hk = R["brand_search"][0].get("cards") or []
    R["hoka_more"] = [product(c[0]) for c in hk[2:5]]
    R["blocked"] = sorted(pf._BLOCKED)


def main():
    R, buf = {"start": time.time(), "ua": pf.UA}, io.StringIO()
    try:
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            work(R)
    except BaseException:
        R["fatal"] = traceback.format_exc()[-3000:]
    R["log"] = buf.getvalue()[-20000:]
    R["sec"] = round(time.time() - R["start"])
    enc_out(R)
    print("probe done", R["sec"])


if __name__ == "__main__":
    main()

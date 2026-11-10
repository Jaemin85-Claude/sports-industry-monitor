# -*- coding: utf-8 -*-
# 임시 시험 4(병합하지 않음) — 온러닝: 한국·일본 상품 사이트맵의 클라우드몬스터·클라우드노바 전부(성별·모델 상관없이) → 5개 나라 공통 색상 → 정가 읽기
import gzip, html, json, re, time, urllib.parse
import price_fetch as pf
def out(k, **kw): print(k, json.dumps(kw, ensure_ascii=False)[:5000], flush=True)
def body(r):
    c = r.content
    if c[:2] == b"\x1f\x8b":
        try: c = gzip.decompress(c)
        except Exception: pass
    return c.decode("utf-8", "replace")
LOC = {"KR": "ko-kr", "US": "en-us", "GB": "en-gb", "DE": "de-de", "JP": "ja-jp"}
RX = re.compile(r"/products/((?:cloudmonster|cloudnova)[a-z0-9\-]*)/(mens|womens|unisex)/([a-z\-]+)-([0-9A-Z.]{8,})$")
got = {}
for cc, loc in LOC.items():
    try: t = body(pf.get(f"https://www.on.com/{loc}/products.xml"))
    except Exception as e: out("SM_ERR", cc=cc, err=str(e)[:200]); continue
    for u in re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", t):
        p = urllib.parse.urlsplit(html.unescape(u)).path; m = RX.search(p)
        if m: got.setdefault((m.group(1), m.group(2), m.group(4)), {})[cc] = p
for cc in ("KR", "JP"):
    out("LIST", cc=cc, v=sorted(f"{k[0]}|{k[1]}|{k[2]}" for k, v in got.items() if cc in v))
common = sorted(k for k, v in got.items() if len(v) == 5)
out("COMMON5", v=[f"{k[0]}|{k[1]}|{k[2]}" for k in common])
krjp = sorted(k for k, v in got.items() if "KR" in v and "JP" in v)
out("KRJP", v=[f"{k[0]}|{k[1]}|{k[2]}|{','.join(sorted(got[k]))}" for k in krjp])
def aeset(handle):
    try: return {(v.get("sku") or "")[:11] for v in pf.get(f"https://on.ae/products/{handle}.json").json()["product"]["variants"]}
    except Exception as e: out("AE_ERR", h=handle, err=str(e)[:120]); return set()
tested = 0
for k in common[:6] + [k for k in got if k[2] == "3MF30740553"]:
    slug = got[k]["US"].split("/products/", 1)[1]
    model = k[0]; hint = "cloudmonster" if "monster" in model else "cloudnova"
    ae_h = re.sub(r"-(m|w)?-?3[mw][a-z]\d{4}$|-3[mw][a-z]\d{4}$", "", model)
    ae = ae_h if k[2] in aeset(ae_h) else None
    urls = {cc: u for cc, u in pf._on(slug, ae).items() if cc in got[k] or cc == "AE"}
    prod = {"id": "on-test", "brand": "온러닝", "name": model, "code": k[2], "src": "page", "hint": hint, "urls": urls}
    for cc in urls:
        try:
            (p, ex), _ = pf.fetch_one(prod, cc); out("READ", code=k[2], model=model, cc=cc, p=p, by=ex.get("by"), now=ex.get("cur_price"))
        except Exception as e:
            out("READ_ERR", code=k[2], model=model, cc=cc, err=f"{type(e).__name__}: {e}"[:200])
    tested += 1
out("DONE", tested=tested)

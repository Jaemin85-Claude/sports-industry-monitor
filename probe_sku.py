# -*- coding: utf-8 -*-
# 임시 시험 3(병합하지 않음) — 온러닝 한국·일본에서 빠진 색상(클라우드몬스터 61.98434 · 클라우드노바 2 3ME30210108) 대신 쓸 색상:
# 나라별 상품 사이트맵(https://www.on.com/{loc}/products.xml)에서 5개 나라에 다 있는 색상 → price_fetch로 정가 읽기
import gzip, html, json, re, time, urllib.parse
import price_fetch as pf
def out(k, **kw): print(k, json.dumps(kw, ensure_ascii=False)[:4000], flush=True)
def body(r):
    c = r.content
    if c[:2] == b"\x1f\x8b":
        try: c = gzip.decompress(c)
        except Exception: pass
    return c.decode("utf-8", "replace")
LOC = {"KR": "ko-kr", "US": "en-us", "GB": "en-gb", "DE": "de-de", "JP": "ja-jp"}
MODELS = {"cm1": r"/products/(cloudmonster-1-m-3mf3074)/mens/([a-z\-]+)-(3MF3074\d{4})$",
          "cm61": r"/products/(cloudmonster-61)/mens/([a-z\-]+)-(61\.\d{5})$",
          "nova2": r"/products/(cloudnova-2-3me3021)/mens/([a-z\-]+)-(3ME3021\d{4})$"}
got = {m: {} for m in MODELS}
for cc, loc in LOC.items():
    try:
        r = pf.get(f"https://www.on.com/{loc}/products.xml"); t = body(r)
    except Exception as e:
        out("SM_ERR", cc=cc, err=str(e)[:200]); continue
    locs = [html.unescape(x) for x in re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", t)]
    out("SM", cc=cc, n=len(locs), index="<sitemapindex" in t[:2000])
    for u in locs:
        p = urllib.parse.urlsplit(u).path
        for m, rx in MODELS.items():
            mm = re.search(rx, p)
            if mm: got[m].setdefault(mm.group(3), {})[cc] = p
for m in MODELS:
    rows = {c: sorted(v) for c, v in got[m].items()}
    out("COLORS", model=m, n=len(rows), v=rows)
try:
    import requests
    j = pf.get("https://on.ae/products/cloudnova-2.json").json(); ae_nova = {(v.get("sku") or "")[:11] for v in j["product"]["variants"]}
except Exception as e:
    ae_nova = set(); out("AE_ERR", err=str(e)[:150])
try:
    j = pf.get("https://on.ae/products/cloudmonster-1.json").json(); ae_cm1 = {(v.get("sku") or "")[:11] for v in j["product"]["variants"]}
    out("AE_CM1", n=len(ae_cm1), v=sorted(ae_cm1)[:40])
except Exception as e:
    ae_cm1 = set(); out("AE_CM1_ERR", err=str(e)[:150])
PREF = ("1200", "1043", "0108", "0553")
for m, hint, ae, aeset in (("cm1", "cloudmonster", "cloudmonster-1", ae_cm1), ("nova2", "cloudnova", "cloudnova-2", ae_nova)):
    full = [c for c, v in got[m].items() if len(v) == 5]
    full.sort(key=lambda c: (next((i for i, s in enumerate(PREF) if c.endswith(s)), 9), c))
    out("CAND", model=m, full5=full[:12])
    for code in full[:3]:
        slug = got[m][code]["US"].split("/products/", 1)[1]
        urls = pf._on(slug, ae if code in aeset else None)
        prod = {"id": f"on-test-{m}", "brand": "온러닝", "name": m, "code": code, "src": "page", "hint": hint, "urls": urls}
        for cc in urls:
            try:
                (full_p, extra), u = pf.fetch_one(prod, cc)
                out("READ", model=m, code=code, cc=cc, p=full_p, cur=pf.MK[cc][2], by=extra.get("by"), now=extra.get("cur_price"))
            except Exception as e:
                out("READ_ERR", model=m, code=code, cc=cc, err=f"{type(e).__name__}: {e}"[:200])
out("DONE")

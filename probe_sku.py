# -*- coding: utf-8 -*-
# 임시 시험 2(병합하지 않음) — ② 온러닝 한국·일본에서 빠진 색상 대신 쓸 색상(5개 나라 같은 품번) · ③ 관세청 운송비용 공식 오픈 API(파일데이터 자동변환) 명세·키 승인 여부
# 우리 봇 이름 · robots.txt 확인(price_fetch.get) · 인증키는 출력하지 않음(dgk_mask)
import gzip, html, json, os, re, sys, time, urllib.parse
import requests
import price_fetch as pf
import logistics_fetch as lf
def out(k, **kw): print(k, lf.dgk_mask(json.dumps(kw, ensure_ascii=False))[:4000], flush=True)
def body(r):
    c = r.content
    if c[:2] == b"\x1f\x8b":
        try: c = gzip.decompress(c)
        except Exception: pass
    return c.decode("utf-8", "replace")
T0 = time.time()
# ② 온러닝 사이트맵
LOC = ("ko-kr", "ja-jp", "en-us", "en-gb", "de-de")
MODELS = ("cloudmonster-61", "cloudnova-2-3me3021", "cloudnova-2-3wd3020", "cloudmonster-1-m")
try:
    r = pf.get("https://www.on.com/sitemap.xml"); t = body(r)
    kids = [html.unescape(x) for x in re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", t)]
    out("ON_INDEX", n=len(kids), sample=[k[-70:] for k in kids[:40]])
except Exception as e:
    out("ON_INDEX_ERR", err=str(e)[:200]); kids = []
found = {}
for loc in LOC:
    cand = [k for k in kids if loc in k.lower() and "product" in k.lower() and "listing" not in k.lower()]
    out("ON_MAPS", loc=loc, n=len(cand), maps=[c[-80:] for c in cand[:8]])
    for sm in cand[:6]:
        if time.time() - T0 > 600: break
        try:
            r = pf.get(sm); t = body(r)
        except Exception as e:
            out("ON_SM_ERR", loc=loc, sm=sm[-80:], err=str(e)[:150]); continue
        locs = [html.unescape(x) for x in re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", t)]
        if "<sitemapindex" in t[:3000]:
            out("ON_SUBINDEX", loc=loc, n=len(locs), kids=[x[-80:] for x in locs[:10]])
            for sub in [x for x in locs if "product" in x.lower()][:4]:
                try:
                    t2 = body(pf.get(sub)); locs += [html.unescape(x) for x in re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", t2)]
                except Exception as e:
                    out("ON_SM_ERR", loc=loc, sm=sub[-80:], err=str(e)[:150])
        for u in locs:
            for m in ("cloudmonster", "cloudnova"):
                if f"/products/{m}" in u and f"/{loc}/" in u:
                    found.setdefault(loc, set()).add(urllib.parse.urlsplit(u).path)
    out("ON_FOUND", loc=loc, n=len(found.get(loc, ())), paths=sorted(found.get(loc, ()))[:80])
# 교집합(모델 폴더 + 품번이 같은 것)
def key(p):
    m = re.search(r"/products/([^/]+)/(mens|womens|unisex)/[^/]*?-([0-9A-Z.]{6,})$", p)
    return (m.group(1), m.group(2), m.group(3)) if m else None
sets = {loc: {key(p) for p in found.get(loc, ()) if key(p)} for loc in LOC}
allk = set.intersection(*[s for s in sets.values()]) if all(sets.values()) else set()
out("ON_COMMON5", n=len(allk), v=sorted(allk)[:60])
kr_jp = (sets.get("ko-kr") or set()) & (sets.get("ja-jp") or set())
out("ON_KRJP", n=len(kr_jp), v=sorted(kr_jp)[:60])
# on.ae 쇼피파이(두바이) — cloudnova-2 변형 품번
try:
    r = pf.get("https://on.ae/products/cloudnova-2.json"); j = r.json()
    skus = sorted({(v.get("sku") or "")[:11] for v in j["product"]["variants"]})
    out("ON_AE", n=len(j["product"]["variants"]), skus=skus[:40])
except Exception as e:
    out("ON_AE_ERR", err=str(e)[:200])

# ③ 관세청 공식 오픈 API(파일데이터 자동변환)
out("SEC", s="kcs-api")
key = os.environ.get("DATA_GO_KR_API_KEY", "").strip(); out("KEY", present=bool(key), has_pct="%" in key, n=len(key))
for ds in ("15116806", "15116850", "15116807"):
    try:
        r = requests.get("https://infuser.odcloud.kr/oas/docs", params={"namespace": f"{ds}/v1"}, headers=lf.UA, timeout=(10, 30))
        out("OAS", ds=ds, st=r.status_code, ct=r.headers.get("content-type", "")[:60], len=len(r.text))
        d = r.json()
        paths = d.get("paths") or {}
        rows = []
        for pth, v in paths.items():
            g = v.get("get") or {}
            rows.append({"path": pth, "summary": (g.get("summary") or "")[:80], "desc": (g.get("description") or "")[:80],
                         "params": [p.get("name") for p in g.get("parameters", [])][:8]})
        out("OAS_PATHS", ds=ds, host=d.get("host"), base=d.get("basePath"), servers=d.get("servers"), n=len(rows), rows=rows[:12],
            sec=list((d.get("securityDefinitions") or (d.get("components") or {}).get("securitySchemes") or {}).keys()))
        if key and rows:
            last = sorted(rows, key=lambda x: x["summary"])[-1]["path"]
            base = "https://api.odcloud.kr/api"
            r2 = requests.get(base + last, params={"page": 1, "perPage": 3, "serviceKey": key}, headers=lf.UA, timeout=(10, 30))
            t2 = r2.text
            out("API", ds=ds, path=last, st=r2.status_code, body=t2[:900])
    except Exception as e:
        out("OAS_ERR", ds=ds, err=lf.dgk_mask(f"{type(e).__name__}: {e}")[:300])
    time.sleep(2)
out("DONE", sec=int(time.time() - T0))

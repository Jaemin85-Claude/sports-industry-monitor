# -*- coding: utf-8 -*-
# 임시 시험(병합하지 않음) — 브랜드 대표 상품의 나라별 주소 찾기: robots.txt의 사이트맵(검색 엔진용 공개 목록)에서 품번·이름으로 찾고, 찾은 주소를 한 번씩 열어 정가를 읽음
import gzip, json, re, sys, time, urllib.parse, urllib.robotparser, requests
UA = "Mozilla/5.0 (compatible; sports-industry-monitor price probe; +https://github.com/Jaemin85-Claude/sports-industry-monitor)"
H = {"User-Agent": UA, "Accept": "text/html,application/xml,application/json;q=0.9,*/*;q=0.8"}
T0 = time.time(); LIMIT = 11 * 60
def get(url, **kw):
    time.sleep(0.8)
    return requests.get(url, headers=H, timeout=25, **kw)
def body(r):
    c = r.content
    if c[:2] == b"\x1f\x8b": c = gzip.decompress(c)
    return c.decode("utf-8", "replace")
ROB = {}
def allowed(url):
    p = urllib.parse.urlsplit(url); base = f"{p.scheme}://{p.netloc}"
    if base not in ROB:
        rp = urllib.robotparser.RobotFileParser(); sm = []
        try:
            r = get(base + "/robots.txt"); lines = r.text.splitlines() if r.status_code == 200 else []
            rp.parse(lines); sm = [l.split(":", 1)[1].strip() for l in lines if l.lower().startswith("sitemap:")]
        except Exception: rp.parse([])
        ROB[base] = (rp, sm)
    return ROB[base][0].can_fetch(UA, url), ROB[base][1]
def find(host, pats, want=3, max_maps=45, prefer=None):
    ok, maps = allowed(f"https://{host}/")
    found = {p: [] for p in pats}; seen = 0; queue = list(maps)
    print(f"[{host}] robots 사이트맵 {len(maps)}개", flush=True)
    while queue and seen < max_maps and time.time() - T0 < LIMIT:
        sm = queue.pop(0)
        if not allowed(sm)[0]: continue
        try: r = get(sm); seen += 1
        except Exception as e: print("   x", sm[:90], type(e).__name__); continue
        if r.status_code != 200: print("   ", r.status_code, sm[:90]); continue
        txt = body(r); locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", txt)
        if "<sitemapindex" in txt[:3000]:
            kids = locs
            if prefer: kids = sorted(kids, key=lambda u: (not any(k in u.lower() for k in prefer), u))
            queue = kids + queue; continue
        for u in locs:
            ul = u.lower()
            for p in pats:
                if p in ul and len(found[p]) < want and u not in found[p]: found[p].append(u)
        if all(len(v) >= want for v in found.values()): break
    print(f"   사이트맵 {seen}개 읽음 → " + json.dumps({p: len(v) for p, v in found.items()}, ensure_ascii=False), flush=True)
    return found
LIST_KEYS = ("compare_at_price", "originalPrice", "regularPrice", "listPrice", "basePrice", "fullPrice", "strikethrough")
def price(url):
    if not allowed(url)[0]: return {"url": url, "status": "robots 금지"}
    try: r = get(url, allow_redirects=True)
    except Exception as e: return {"url": url, "status": type(e).__name__}
    out = {"url": url[:140], "status": r.status_code, "final": r.url[:140] if r.url != url else ""}
    if r.status_code != 200: return out
    t = r.text; offers = []
    for m in re.finditer(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', t, re.S | re.I):
        try: d = json.loads(m.group(1).strip())
        except Exception: continue
        st = d if isinstance(d, list) else [d]
        while st:
            x = st.pop()
            if isinstance(x, dict):
                if str(x.get("@type", "")).lower() in ("offer", "aggregateoffer"):
                    offers.append((x.get("price") or x.get("lowPrice"), x.get("highPrice"), x.get("priceCurrency"), (x.get("priceSpecification") or {}).get("price") if isinstance(x.get("priceSpecification"), dict) else None))
                if x.get("@type") in ("Product", "ProductGroup") and x.get("name") and "name" not in out: out["name"] = str(x["name"])[:60]
                st.extend(v for v in x.values() if isinstance(v, (dict, list)))
            elif isinstance(x, list): st.extend(x)
    out["offers"] = sorted({str(o) for o in offers})[:4]
    lp = {}
    for k in LIST_KEYS:   # 정가 필드 옆 숫자 몇 개
        vals = re.findall(rf'"{k}"\s*:\s*\{{?[^0-9-]{{0,40}}?(-?[0-9][0-9.,]*)', t)
        if vals: lp[k] = sorted(set(vals))[:4]
    out["list"] = lp
    return out
if __name__ == "__main__":
    plan = json.load(open(sys.argv[1]))
    for job in plan:
        if time.time() - T0 > LIMIT: print("시간 제한 — 남은 작업 건너뜀"); break
        if job.get("urls"): urls = job["urls"]
        else:
            fd = find(job["host"], job["pats"], job.get("want", 2), job.get("max_maps", 45), job.get("prefer"))
            urls = [u for v in fd.values() for u in v]
            for p, v in fd.items(): print(f"   {p}: " + " | ".join(v), flush=True)
        for u in urls[: job.get("check", 6)]:
            print("   →", json.dumps(price(u), ensure_ascii=False), flush=True)

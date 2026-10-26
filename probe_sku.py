# -*- coding: utf-8 -*-
# 임시 시험(병합하지 않음) — 언더아머 멕시코 대체 상품 찾기(대표 지시 2026-10-26): 나라별 사이트맵에서 같은 품번 상품 찾기 + price_fetch로 정가 읽기 시험
# robots.txt·요청 간격·막힘 처리는 price_fetch.get(우리 봇 이름 · RFC 9309)을 그대로 씀
import gzip, json, re, sys, time, urllib.parse
import price_fetch as pf
T0 = time.time(); LIMIT = 17 * 60
def out(kind, **kw): print(kind, json.dumps(kw, ensure_ascii=False), flush=True)
def body(r):
    c = r.content
    if c[:2] == b"\x1f\x8b": c = gzip.decompress(c)
    return c.decode("utf-8", "replace")
def left(): return LIMIT - (time.time() - T0)
SM = {}
def sitemaps(host):
    if host not in SM:
        try:
            r = pf.get(f"https://{host}/robots.txt")
            SM[host] = [l.split(":", 1)[1].strip() for l in r.text.splitlines() if l.lower().startswith("sitemap:")]
        except Exception as e:
            out("ROBOTSERR", host=host, err=str(e)[:120]); SM[host] = []
    return SM[host]
def ua_codes(j):   # 나라별 사이트맵에서 상품 품번(7자리) 모아 겹치는 것 찾기
    sites, codes = j["sites"], {}
    for cc, host in sites.items():
        got, seen, queue = {}, 0, list(j.get("start", {}).get(cc) or sitemaps(host))
        out("ROBOTS_SM", cc=cc, host=host, maps=queue[:6])
        t0 = time.time()
        while queue and seen < j.get("max_maps", 40) and left() > 90 and time.time() - t0 < j.get("per_host", 170):
            sm = queue.pop(0)
            try: r = pf.get(sm); seen += 1
            except Exception as e: out("SMERR", cc=cc, sm=sm[:120], err=str(e)[:120]); continue
            txt = body(r); locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", txt)
            if "<sitemapindex" in txt[:3000]:
                kids = sorted(locs, key=lambda u: (not any(k in u.lower() for k in ("product", "pdp", "prod")), u))
                out("INDEX", cc=cc, sm=sm[-80:], kids=[k[-70:] for k in kids[:8]], n=len(kids))
                queue = kids + queue; continue
            for u in locs:
                m = re.search(r"/(\d{7})(?:\.html|/|\?|$)", u)
                if m and m.group(1) not in got: got[m.group(1)] = u
        codes[cc] = got
        out("CODES", cc=cc, host=host, maps_read=seen, n=len(got), sample=[urllib.parse.unquote(u)[-80:] for u in list(got.values())[:3]])
    for t in j.get("targets", []):
        out("TARGET", code=t, where={cc: urllib.parse.unquote(codes[cc].get(t) or "")[-110:] for cc in codes})
    base = codes.get("MX") or {}
    rows = [(sum(c in codes.get(cc, {}) for cc in ("US", "GB", "DE")), c, u) for c, u in base.items() if c in codes.get("KR", {})]
    rows.sort(key=lambda r: (-r[0], r[1]))
    out("INTERSECT", mx=len(base), mx_kr=len(rows), all5=sum(1 for r in rows if r[0] == 3))
    for n, c, u in rows[: j.get("show", 250)]:
        print("ROW", json.dumps({"code": c, "n": n, "mx": urllib.parse.unquote(u)[-95:], "kr": urllib.parse.unquote(codes["KR"][c])[-95:],
                                 "us": c in codes.get("US", {}), "gb": c in codes.get("GB", {}), "de": c in codes.get("DE", {})},
                                ensure_ascii=False), flush=True)
def fetch(j):
    for prod in j["prods"]:
        if left() < 30: out("TIMEOUT"); return
        for cc in list((prod.get("urls") or {}).keys()):
            try:
                (full, extra), src = pf.fetch_one(prod, cc)
                out("OK", id=prod["id"], cc=cc, full=full, cur=pf.MK[cc][2], extra=extra, src=src[:110])
            except Exception as e:
                out("FAIL", id=prod["id"], cc=cc, err=f"{type(e).__name__}: {str(e)[:160]}")
if __name__ == "__main__":
    pf.log = lambda m: print("  log:", m, flush=True)
    for j in json.load(open(sys.argv[1])):
        if left() < 30: print("시간 제한 — 남은 작업 건너뜀"); break
        {"ua_codes": ua_codes, "fetch": fetch}[j["t"]](j)
    print(f"끝 {int(time.time()-T0)}초")

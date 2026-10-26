# -*- coding: utf-8 -*-
# 임시 시험(병합하지 않음) — 해외 정가 SKU 늘리기(대표 상시 지시 2026-10-26): 나라별 몰 사이트맵에서 같은 품번 상품 찾기 + price_fetch로 정가 읽기 시험
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
SM = {}; CODES = {}
def sitemaps(host):
    if host not in SM:
        try:
            r = pf.get(f"https://{host}/robots.txt")
            SM[host] = [l.split(":", 1)[1].strip() for l in r.text.splitlines() if l.lower().startswith("sitemap:")]
        except Exception as e:
            out("ROBOTSERR", host=host, err=str(e)[:120]); SM[host] = []
    return SM[host]
def codes(j):   # 나라별 사이트맵 → {품번: 주소}, 겹치는 품번
    rx = re.compile(j["rx"]); key = j.get("key", "x"); CODES.setdefault(key, {})
    for cc, site in j["sites"].items():
        host, pre = site["host"], site.get("path", "/")
        got, seen, queue = {}, 0, list(site.get("start") or sitemaps(host))
        t0 = time.time()
        while queue and seen < j.get("max_maps", 40) and left() > 120 and time.time() - t0 < j.get("per_host", 150):
            sm = queue.pop(0)
            try: r = pf.get(sm); seen += 1
            except Exception as e: out("SMERR", cc=cc, sm=sm[:120], err=str(e)[:120]); continue
            txt = body(r); locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", txt)
            if "<sitemapindex" in txt[:3000]:
                kids = [k for k in locs if urllib.parse.urlsplit(k).netloc == host]
                kids.sort(key=lambda u: (not any(k in u.lower() for k in ("product", "pdp", "prod")), u))
                queue = kids + queue; continue
            for u in locs:
                sp = urllib.parse.urlsplit(u)
                if sp.netloc != host or not sp.path.startswith(pre): continue
                m = rx.search(sp.path)
                if m:
                    old = got.get(m.group(1))
                    if not old or sp.path.count("/") > urllib.parse.urlsplit(old).path.count("/"): got[m.group(1)] = u
        CODES[key][cc] = got
        out("CODES", key=key, cc=cc, host=host, maps_read=seen, n=len(got))
    cs = CODES[key]; base = cs.get(j.get("base", "KR")) or {}
    others = [cc for cc in cs if cc != j.get("base", "KR")]
    rows = [(sum(c in cs[cc] for cc in others), c) for c in base]
    rows.sort(key=lambda r: (-r[0], r[1]))
    out("INTERSECT", key=key, base=len(base), all=sum(1 for r in rows if r[0] == len(others)))
    for t in j.get("targets", []):
        out("TARGET", key=key, code=t, where={cc: urllib.parse.unquote(cs[cc].get(t) or "")[-120:] for cc in cs})
    for n, c in rows[: j.get("show", 0)]:
        print("ROW", json.dumps({"code": c, "n": n, "kr": urllib.parse.unquote(base[c])[-90:],
                                 "miss": [cc for cc in others if c not in cs[cc]]}, ensure_ascii=False), flush=True)
def try_codes(j):   # 후보 품번을 나라별 주소로 price_fetch에 넣어 정가 읽기 시험
    cs = CODES.get(j.get("key", "x"), {})
    for cand in j["cands"]:
        code = cand["code"]; urls = {cc: cs.get(cc, {}).get(code) for cc in j["ccs"]}
        urls = {cc: u for cc, u in urls.items() if u}
        prod = {"id": "try-" + code, "brand": j.get("brand", ""), "name": cand.get("name", code), "code": code, "src": "page",
                "hint": cand.get("hint", ""), "urls": urls}
        out("TRY", code=code, urls={cc: urllib.parse.unquote(u)[-110:] for cc, u in urls.items()}, missing=[cc for cc in j["ccs"] if cc not in urls])
        for cc in urls:
            if left() < 30: out("TIMEOUT"); return
            try:
                (full, extra), src = pf.fetch_one(prod, cc)
                out("OK", code=code, cc=cc, full=full, cur=pf.MK[cc][2], extra=extra)
            except Exception as e:
                out("FAIL", code=code, cc=cc, err=f"{type(e).__name__}: {str(e)[:160]}")
if __name__ == "__main__":
    pf.log = lambda m: print("  log:", m, flush=True)
    for j in json.load(open(sys.argv[1])):
        if left() < 30: print("시간 제한 — 남은 작업 건너뜀"); break
        {"codes": codes, "try": try_codes}[j["t"]](j)
    print(f"끝 {int(time.time()-T0)}초")

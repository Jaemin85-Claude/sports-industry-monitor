# -*- coding: utf-8 -*-
# 임시 시험(병합하지 않음 · PR 전에 지움) — 중국 공식몰 정가를 우리 봇(price_fetch.get — robots.txt·간격·차단 시 멈춤)으로 읽을 수 있는지 브랜드별로 확인.
# 공개 주소·공개 품번만 씀(ERP 목록 안 씀). 봇 확인 화면·403이면 '막힘'으로 적고 우회하지 않음.
import gzip, html, json, re, time, urllib.parse
import price_fetch as pf

T0 = time.time(); LIMIT = 15 * 60
def left(): return LIMIT - (time.time() - T0)
def say(*a): print(*a, flush=True)
def body(r):
    c = r.content
    if c[:2] == b"\x1f\x8b": c = gzip.decompress(c)
    return c.decode("utf-8", "replace")

SITES = [   # (브랜드, 후보 주소 — 공식몰 첫 화면)
    ("나이키", "https://www.nike.com.cn/"), ("푸마", "https://cn.puma.com/"), ("푸마", "https://www.puma.com.cn/"),
    ("온러닝", "https://www.on.com/zh-cn"), ("크록스", "https://www.crocs.com.cn/"), ("아크테릭스", "https://arcteryx.com.cn/"),
    ("아크테릭스", "https://www.arcteryx.cn/"), ("살로몬", "https://www.salomon.cn/"), ("닥터마틴", "https://www.drmartens.com.cn/"),
    ("언더아머", "https://www.underarmour.cn/"), ("킨(KEEN)", "https://www.keenfootwear.cn/"), ("버버리", "https://cn.burberry.com/"),
    ("톰브라운", "https://www.thombrowne.com/zh-cn"), ("톰브라운", "https://www.thombrowne.cn/"), ("오니츠카타이거", "https://www.onitsukatiger.com.cn/"),
    ("오니츠카타이거", "https://www.onitsukatiger.com/cn/zh-cn/"), ("미즈노", "https://www.mizuno.com.cn/"), ("써코니", "https://www.saucony.com.cn/"),
    ("써코니", "https://saucony.cn/"), ("브룩스", "https://www.brooksrunning.com.cn/"), ("헌터", "https://www.hunterboots.cn/"),
    ("우포스", "https://www.oofos.cn/"), ("드래곤디퓨전", "https://dragondiffusion.com/zh-cn"),
]

def probe_site(brand, url):
    p = urllib.parse.urlsplit(url); host = p.netloc
    t0 = time.time()
    try:
        rob = pf._robots_get(f"{p.scheme}://{host}")
        rob_s = "robots 없음/허용" if rob == [] else (rob if isinstance(rob, str) else f"robots 규칙 {len(rob)}줄")
    except Exception as e:
        rob_s = f"robots 오류 {type(e).__name__}"
    try:
        r = pf.get(url)
        txt = body(r)
        fin = r.url
        ld = [n for n in pf._ld_nodes(txt) if pf._types(n) & {"product", "productgroup", "organization", "website"}]
        cny = len(re.findall(r'"priceCurrency"\s*:\s*"CNY"', txt))
        title = (re.search(r"<title[^>]*>(.*?)</title>", txt, re.S | re.I) or [None, ""])[1].strip()[:40]
        say(f"  {brand} {url}: 200 · {time.time() - t0:.1f}초 · {len(txt) // 1000}KB · 최종 {fin[:60]} · 제목 '{html.unescape(title)}' · JSON-LD {len(ld)} · CNY 가격 {cny} · {rob_s}")
        return fin, txt
    except Exception as e:
        say(f"  {brand} {url}: 못 받음 — {str(e)[:90]} · {time.time() - t0:.1f}초 · {rob_s}")
        return None, None

def sitemap_products(host, scheme="https", limit=3):
    try:
        maps = [l.split(":", 1)[1].strip() for l in pf.get(f"{scheme}://{host}/robots.txt").text.splitlines() if l.lower().startswith("sitemap:")]
    except Exception:
        maps = []
    maps = maps or [f"{scheme}://{host}/sitemap.xml"]
    seen, urls = 0, []
    queue = list(maps)
    while queue and seen < 6 and left() > 120:
        sm = queue.pop(0)
        try:
            r = pf.get(sm); seen += 1; txt = body(r)
        except Exception as e:
            say(f"    사이트맵 못 받음 {sm[-60:]}: {str(e)[:60]}"); continue
        locs = [html.unescape(x) for x in re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", txt)]
        if "<sitemapindex" in txt[:3000]:
            kids = sorted(locs, key=lambda u: (not any(k in u.lower() for k in ("product", "pdp", "goods", "item")), u))
            queue = kids[:4] + queue; continue
        urls += [u for u in locs if any(k in u.lower() for k in ("/p/", "/pd/", "/product", "/goods", "/t/", "/item", ".html"))]
        if len(urls) >= 20: break
    say(f"    사이트맵 {seen}개 읽음 · 상품 같은 주소 {len(urls)}개" + (f" · 예 {urls[0][:90]}" if urls else ""))
    return urls[:limit]

def main():
    say("[나이키] 상품 정보(product_feed) 중국 marketplace")
    for m, l in (("CN", "zh-Hans"), ("CN", "zh_CN")):
        try:
            d = pf._json(pf.get(pf.NIKE_FEED.format(m=m, l=l, s="CW2288-111")))
            objs = d.get("objects") or []
            mp = (((objs or [{}])[0].get("productInfo") or [{}])[0].get("merchPrice") or {}) if objs else {}
            say(f"  {m}/{l}: 객체 {len(objs)} · 정가 {mp.get('fullPrice')} {mp.get('currency')} · 지금 {mp.get('currentPrice')}")
        except Exception as e:
            say(f"  {m}/{l}: 오류 {str(e)[:80]}")
    say("[중국 공식몰 첫 화면]")
    ok = []
    for brand, url in SITES:
        if left() < 120:
            say("시간 부족"); break
        fin, txt = probe_site(brand, url)
        if fin:
            ok.append((brand, fin))
    say("[열린 곳 — 상품 페이지 정가 읽기]")
    for brand, fin in ok:
        if left() < 120: break
        host = urllib.parse.urlsplit(fin).netloc
        for u in sitemap_products(host):
            try:
                r = pf.get(u); txt = body(r)
                nodes = [n for n in pf._ld_nodes(txt, pf.REL) if pf._types(n) & {"product", "productgroup"}]
                offers = re.findall(r'"price"\s*:\s*"?([0-9.]+)"?\s*,\s*"priceCurrency"\s*:\s*"([A-Z]{3})"', txt)[:3]
                say(f"    {brand} {u[:90]}: JSON-LD 상품 {len(nodes)} · 가격 {offers} · sku {[str(n.get('sku'))[:20] for n in nodes[:2]]}")
                break
            except Exception as e:
                say(f"    {brand} {u[:90]}: 못 받음 {str(e)[:60]}")
    say(f"끝 · {time.time() - T0:.0f}초")

if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""임시 시험(병합 안 함) 2회차 — 써코니·브룩스 상품 짝, 코오롱몰·언더아머 한국/멕시코 정가(할인 전) 표기 위치.
price_fetch.get()(우리 봇 이름 · robots.txt · 403/429면 그 사이트 그만)을 그대로 씀. 저장·커밋 안 함."""
import json, re, time, urllib.parse
import requests
import price_fetch as pf

pf.GAP = 0.8
T0 = time.time()


def tryget(url):
    try:
        r = pf.get(url)
        return r, r.text, ""
    except Exception as e:
        return None, "", str(e)[:90]


def big(u, cap=12_000_000):
    ok, why = pf.robots_ok(u)
    if not ok or urllib.parse.urlsplit(u).netloc in pf._BLOCKED:
        return "", f"robots/막힘 {why}"
    w = pf.GAP - (time.time() - pf._LAST[0])
    if w > 0: time.sleep(w)
    pf._LAST[0] = time.time()
    try:
        r = requests.get(u, headers=pf.HDR, timeout=30, stream=True)
        if r.status_code != 200: return "", f"HTTP {r.status_code}"
        b = b""
        for ch in r.iter_content(262144):
            b += ch
            if len(b) > cap: break
        r.close()
        return b.decode("utf-8", "replace"), ""
    except Exception as e:
        return "", str(e)[:60]


def snip(h, pat, n=10, w=120, flags=0):
    out = []
    for m in re.finditer(pat, h, flags):
        s = re.sub(r"\s+", " ", h[max(0, m.start() - w): m.end() + w])
        out.append(s)
        if len(out) >= n: break
    return out


def ld_names(h):
    out = []
    for n in pf._ld_nodes(h):
        if pf._types(n) & {"product", "productgroup"}:
            o = n.get("offers")
            o = o[0] if isinstance(o, list) and o else o
            out.append(f"{str(n.get('name'))[:45]!r} sku={str(n.get('sku'))[:40]} mpn={n.get('mpn')} price={(o or {}).get('price') if isinstance(o, dict) else None}")
    return out[:3]


def show(url, pats, n=8, w=120):
    r, h, e = tryget(url)
    if not r:
        print(f"  ✗ {urllib.parse.unquote(url)[:120]} {e}", flush=True); return ""
    print(f"  {r.status_code} {len(h)//1000}KB {urllib.parse.unquote(r.url)[:130]}", flush=True)
    for l in ld_names(h): print(f"    LD {l}")
    flat = h.replace('\\"', '"')
    for p in pats:
        for s in snip(flat, p, n, w): print(f"    [{p[:18]}] {s[:2 * w + 60]}")
    return h


def main():
    PR = r'(?i)(정상가|판매가|소비자가|정가|할인가|원가|consumer_?price|normal_?price|origin(al)?_?price|sale_?price|retail_?price|list_?price|strike|"price"\s*:\s*[0-9"])'
    # 1) 코오롱몰 정가(할인 전) — 헌터 블랙·드래곤디퓨전
    print("# 코오롱몰 가격 칸", flush=True)
    for u in ("https://www.kolonmall.com/Brands/HUNTER/Product/K1760508652696038BK01",
              "https://www.kolonmall.com/Brands/DRAGON_DIFFUSION/Product/W2BAS26025DBR"):
        show(u, [PR, r"209,?000|785,?000"], 14, 110)
    # 2) 언더아머 한국·멕시코 정가 표기
    print("\n# 언더아머 한국·멕시코 가격 칸", flush=True)
    show("https://www.underarmour.co.kr/ko-kr/p/%EC%83%81%EC%9D%98/ua_tech_2.0/1326413.html", [PR, r"39,?000"], 10, 110)
    show("https://www.underarmour.com.mx/es-mx/p/tops/ua_tech_2.0/1326413.html", [PR, r"499"], 10, 110)
    # 3) 써코니 한국 — 품번 위치 + 모델별 대표 상품
    print("\n# 써코니 한국", flush=True)
    x, e = big("https://saucony.co.kr/sitemap.xml")
    kr = [urllib.parse.unquote(l) for l in re.findall(r"<loc>\s*([^<\s]+)", x) if "/product/" in l]
    print(f"  KR 상품 {len(kr)}개")
    for kw in ("트라이엄프-23", "라이드-19", "엔돌핀-스피드-5", "킨바라-16", "가이드-19", "허리케인-26", "프로그리드-옴니-9", "재즈-오리지널", "트레이너-80", "섀도우|쉐도우", "엔돌핀-프로-5", "엑소더스-울트라-4"):
        hits = [l for l in kr if re.search(kw, l)]
        print(f"  {kw}: {len(hits)} · {[l.split('/product/')[1][:50] for l in hits[:8]]}")
    for kw in ("남성-트라이엄프-23-triple-black", "남성-라이드-19-whitecrimson", "남성-엔돌핀-스피드-5-whitegum", "공용-재즈-오리지널-45-black", "공용-트레이너-80-blackwhite"):
        hits = [l for l in kr if kw in l]
        for l in hits[:1]:
            show(urllib.parse.quote(l, safe=":/"), [r"S[0-9]{4,5}-[0-9]{1,3}[A-Z]?|S[0-9]{5}\b", PR], 6, 120)
    # 4) 써코니 미국 — 사이트맵 모델 + 가격 칸
    print("\n# 써코니 미국", flush=True)
    x, e = big("https://www.saucony.com/sitemap_0.xml")
    us = [l for l in re.findall(r"<loc>\s*([^<\s]+)", x)]
    for kw in ("triumph-23", "ride-19", "endorphin-speed-5", "kinvara-16", "guide-19", "hurricane-26", "omni-9", "jazz-original", "trainer-80", "shadow"):
        hits = [l for l in us if kw in l]
        print(f"  US {kw}: {len(hits)} · {[l.split('.com')[1][:60] for l in hits[:8]]}")
    for kw in ("triumph-23", "ride-19", "jazz-original"):
        hits = [l for l in us if kw in l and "/en/" in l]
        for l in hits[:1]:
            show(l, [r'itemprop="price"|itemprop="priceCurrency"|price-sales|price-standard|price-list|strike|"salePrice"|"listPrice"|"standardPrice"|data-price', r"S[0-9]{5}-[0-9]{1,3}"], 10, 140)
    # 5) 써코니 영국·독일 홈의 상품 주소
    print("\n# 써코니 영국·독일", flush=True)
    for home in ("https://www.saucony.com/UK/en_GB/", "https://www.saucony.com/DE/de_DE/"):
        r, h, e = tryget(home)
        if not r:
            print(f"  ✗ {home} {e}"); continue
        links = sorted(set(re.findall(r'href="([^"]+\.html)[^"]*"', h)))
        prods = [l for l in links if re.search(r"/[0-9A-Z]{5,8}\.html$", l)]
        print(f"  {home} → {r.url} · 링크 {len(links)} · 상품 같은 것 {len(prods)} {prods[:12]}")
        cand = [l for l in prods if re.search(r"triumph|ride|jazz|endorphin|kinvara|guide", l, re.I)][:1] or prods[:1]
        for l in cand:
            show(urllib.parse.urljoin(r.url, l), [r'itemprop="price"|itemprop="priceCurrency"|price-sales|price-standard|strike|"price"\s*:', r"S[0-9]{5}-[0-9]{1,3}"], 8, 120)
    # 6) 브룩스 한국 — 분류 쪽에서 고스트·글리세린
    print("\n# 브룩스 한국", flush=True)
    r, h, e = tryget("https://brooksrunning.co.kr/")
    if r:
        cates = sorted(set(re.findall(r'href="([^"]*(?:cate_no=\d+|/category/[^"/]+/\d+/)[^"]*)"', h)))
        print(f"  분류 링크 {len(cates)}: {[urllib.parse.unquote(c)[:70] for c in cates[:40]]}")
        prods = set(re.findall(r'href="(/product/[^"]+?/\d+/)', h))
        seen = set(prods)
        for c in cates[:14]:
            if time.time() - T0 > 20 * 60: break
            r2, h2, e2 = tryget(urllib.parse.urljoin("https://brooksrunning.co.kr/", c))
            if not r2:
                print(f"  ✗ {c[:60]} {e2}"); continue
            ps = set(re.findall(r'href="(/product/[^"]+?/\d+/)', h2))
            seen |= ps
            gl = [urllib.parse.unquote(p) for p in ps if re.search(r"ghost|고스트|glycerin|글리세린", urllib.parse.unquote(p), re.I)]
            print(f"  {urllib.parse.unquote(c)[:60]} → 상품 {len(ps)} · 고스트/글리세린 {gl[:10]}", flush=True)
        gl = sorted(p for p in seen if re.search(r"ghost|고스트|glycerin|글리세린", urllib.parse.unquote(p), re.I))
        print(f"  고스트/글리세린 모두 {len(gl)}: {[urllib.parse.unquote(p)[:70] for p in gl[:30]]}")
        for p in [p for p in gl if re.search(r"ghost-?18|고스트-?18", urllib.parse.unquote(p), re.I)][:3] or gl[:2]:
            show(urllib.parse.urljoin("https://brooksrunning.co.kr/", p), [r"1[12][0-9]{4}1[A-Z][0-9]{3}|1[12][0-9]{4}1[A-Z]", PR], 6, 110)
    print(f"\n걸린 시간 {time.time() - T0:.0f}초")


if __name__ == "__main__":
    main()

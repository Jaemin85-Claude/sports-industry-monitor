# -*- coding: utf-8 -*-
# 임시 시험(병합하지 않음 · PR 전에 지움) — ERP 판매·예정 상품(비공개 목록)을 브랜드 공식몰에서 몇 %나 찾을 수 있는지(나라별) 재기.
# 공개 저장소라 실행 기록이 공개 — ERP 품번·상품명·주소·토큰은 찍지 않음(비율·구간·요청 수·시간만). 공개 품번(price_fetch PRODUCTS)은 찍어도 됨.
# 요청은 price_fetch.get(우리 봇 이름 · robots.txt RFC 9309 · 사이트별 간격)만 씀 — 봇 차단 우회 없음.
import collections, gzip, html, json, os, re, sys, time, urllib.error, urllib.parse, urllib.request
import price_fetch as pf

T0 = time.time(); LIMIT = 16 * 60
def left(): return LIMIT - (time.time() - T0)
def say(*a): print(*a, flush=True)
def band(n): return "0" if n == 0 else "1~9" if n < 10 else "10~49" if n < 50 else "50~199" if n < 200 else "200~999" if n < 1000 else "1000+"
def pct(a, b): return f"{round(100 * a / b)}%" if b else "-"

# ---------- ERP 목록 ----------
def erp_list():
    url, tok = os.environ.get("ERP_SKU_URL", "").strip(), os.environ.get("ERP_SKU_TOKEN", "").strip()
    if not url or not tok:
        say("ERP 목록: Secrets 없음"); return []
    tok = tok[7:].strip() if tok.lower().startswith("bearer ") else tok
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {tok}", "Accept": "application/json", "User-Agent": pf.BOT})
    for n, w in enumerate((0, 15, 30, 60), 1):
        time.sleep(w)
        try:
            with urllib.request.urlopen(req, timeout=40) as r:
                d = json.loads(r.read())
            items = [it for it in d.get("items") or [] if isinstance(it, dict)]
            say(f"ERP 목록: {n}번째에 받음 · {band(len(items))}개"); return items
        except urllib.error.HTTPError as e:
            say(f"ERP 목록: {n}번째 HTTP {e.code}")
        except Exception as e:
            say(f"ERP 목록: {n}번째 {type(e).__name__}")
    return []

A = {"나이키": "nike", "푸마": "puma", "온러닝": "on|onrunning|온|on running", "아크테릭스": "arcteryx|arc'teryx",
     "써코니": "saucony|사코니", "살로몬": "salomon", "킨(KEEN)": "keen|킨", "우포스": "oofos", "크록스": "crocs",
     "오니츠카타이거": "onitsukatiger|onitsuka tiger|오니츠카", "미즈노": "mizuno", "닥터마틴": "drmartens|dr.martens|dr martens|닥터마틴스",
     "헌터": "hunter", "드래곤디퓨전": "dragondiffusion|dragon diffusion", "톰브라운": "thombrowne|thom browne",
     "버버리": "burberry", "언더아머": "underarmour|under armour", "브룩스": "brooks|brooksrunning"}
key = lambda s: re.sub(r"[\s\-_.'’()]+", "", str(s or "")).lower()
AL = {key(a): k for k, v in A.items() for a in [k] + v.split("|")}
def norm(c): return re.sub(r"\s+", "", str(c or "")).upper()

# ---------- 사이트맵 ----------
def body(r):
    c = r.content
    if c[:2] == b"\x1f\x8b": c = gzip.decompress(c)
    return c.decode("utf-8", "replace")
def robots_maps(host):
    try:
        return [l.split(":", 1)[1].strip() for l in pf.get(f"https://{host}/robots.txt").text.splitlines() if l.lower().startswith("sitemap:")]
    except Exception as e:
        say(f"  {host} robots.txt 못 받음: {str(e)[:80]}"); return []
def walk(host, start=None, path_pre="/", kid_pref=(), max_maps=40, per_host=150):
    """사이트맵 → 그 사이트 주소 목록"""
    queue, seen, out, t0 = list(start or robots_maps(host) or [f"https://{host}/sitemap.xml"]), 0, [], time.time()
    while queue and seen < max_maps and left() > 90 and time.time() - t0 < per_host:
        sm = queue.pop(0)
        try:
            r = pf.get(sm); seen += 1
        except Exception as e:
            say(f"  {host} 사이트맵 못 받음({sm[-60:]}): {str(e)[:80]}"); continue
        txt = body(r); locs = [html.unescape(x) for x in re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", txt)]
        if "<sitemapindex" in txt[:3000]:
            kids = [k for k in locs if urllib.parse.urlsplit(k).netloc == host]
            if kid_pref:
                kids = [k for k in kids if any(x in k.lower() for x in kid_pref)] or kids
            kids.sort(key=lambda u: (not any(k in u.lower() for k in ("product", "pdp", "prod")), u))
            queue = kids + queue; continue
        out += [u for u in locs if urllib.parse.urlsplit(u).netloc == host and urllib.parse.urlsplit(u).path.startswith(path_pre)]
    say(f"  {host}{path_pre}: 사이트맵 {seen}개 · 주소 {len(out)}개 · {time.time() - t0:.0f}초")
    return out

def report(brand, name, codes, found):
    """codes = ERP 품번(정규화) 목록 · found = 찾은 품번 집합 — 비율만"""
    hit = sum(1 for c in codes if c in found)
    say(f"  ▶ {brand} {name}: {pct(hit, len(codes))} 찾음 (목록 {band(len(codes))}개)")

# ---------- 브랜드별 ----------
def nike(codes):
    say("[나이키] product_feed 여러 품번 한 번에 — 공개 품번으로 먼저")
    pub = [p["code"] for p in pf.PRODUCTS if p["brand"] == "나이키"][:20]
    for n in (2, 10, 20):
        s = ",".join(pub[:n]); m, l, cur = pf.MK["KR"]
        for extra in ("", "&count=50"):
            try:
                d = pf._json(pf.get(pf.NIKE_FEED.format(m=m, l=l, s=s) + extra))
                objs = d.get("objects") or []
                got = {pi.get("merchProduct", {}).get("styleColor") for o in objs for pi in o.get("productInfo") or []}
                fp = sum(1 for o in objs for pi in o.get("productInfo") or [] if (pi.get("merchPrice") or {}).get("fullPrice"))
                say(f"  공개 {n}개{extra or ''}: 객체 {len(objs)} · 맞는 품번 {len(got & set(pub[:n]))}/{n} · 정가 있는 칸 {fp} · pages {json.dumps(d.get('pages') or {}, ensure_ascii=False)[:160]}")
            except Exception as e:
                say(f"  공개 {n}개{extra}: 오류 {str(e)[:100]}")
    if not codes:
        return
    cs = sorted(set(codes))
    for cc in ("KR", "US", "GB", "DE"):
        m, l, cur = pf.MK[cc]; found, nreq, t0 = set(), 0, time.time()
        for i in range(0, len(cs), 20):
            if left() < 200:
                say("  시간 부족 — 나머지 건너뜀"); break
            part = cs[i:i + 20]
            try:
                d = pf._json(pf.get(pf.NIKE_FEED.format(m=m, l=l, s=",".join(part)) + "&count=50")); nreq += 1
                for o in d.get("objects") or []:
                    for pi in o.get("productInfo") or []:
                        sc = norm((pi.get("merchProduct") or {}).get("styleColor"))
                        if sc in part and (pi.get("merchPrice") or {}).get("fullPrice") and (pi.get("merchPrice") or {}).get("currency") == cur:
                            found.add(sc)
            except Exception as e:   # 요청 주소에 ERP 품번이 들어가므로 오류 글은 찍지 않음(종류만)
                say(f"  {cc} 묶음 오류: {type(e).__name__}" + (f" {str(e)[:12]}" if str(e).startswith("HTTP") else ""))
        say(f"  {cc}: 요청 {nreq}번 · {time.time() - t0:.0f}초")
        report("나이키", cc, cs, found)

def crocs(codes):
    say("[크록스] 사이트맵 모델 번호(/p/…/모델.html) — ERP 품번 앞 모델")
    models = [c.split("-")[0] for c in codes]
    for cc, host in (("KR", "www.crocs.co.kr"), ("US", "www.crocs.com"), ("GB", "www.crocs.co.uk"), ("DE", "www.crocs.de")):
        if left() < 200: break
        us = walk(host, kid_pref=("product",), max_maps=20, per_host=90)
        found = {m.group(1) for u in us if (m := re.search(r"/p/[^/]+/(\d{5,6})\.html", urllib.parse.urlsplit(u).path))}
        report("크록스", cc + " 모델", models, found)

def puma(codes):
    say("[푸마] 사이트맵 모델 번호 — ERP 품번 앞 6자리")
    models = [c.split("-")[0] for c in codes]
    for cc, host, pre, start in (("KR", "kr.puma.com", "/kr/ko/", None), ("US", "us.puma.com", "/us/en/", None),
                                 ("GB", "uk.puma.com", "/uk/en/", None), ("DE", "eu.puma.com", "/de/de/", ["https://eu.puma.com/sitemaps/urls/de/sitemap_0.xml"])):
        if left() < 200: break
        us = walk(host, start=start, path_pre=pre, kid_pref=("product", "pdp"), max_maps=15, per_host=90)
        found = {m.group(1) for u in us if (m := re.search(r"/pd/[^/]+/(\d{6})(?:\.html)?$", urllib.parse.urlsplit(u).path))}
        report("푸마", cc + " 모델", models, found)

def ua(codes):
    say("[언더아머] 미국 사이트맵 모델 번호 — ERP 품번 앞 7자리(한국·영국·독일은 수집 멈춤)")
    models = [c.split("-")[0] for c in codes]
    us = walk("www.underarmour.com", path_pre="/en-us/", kid_pref=("product",), max_maps=20, per_host=120)
    found = {m.group(1) for u in us if (m := re.search(r"/p/[^/]+/(\d{7})(?:\.html)?$", urllib.parse.urlsplit(u).path))}
    report("언더아머", "US 모델", models, found)

def on(codes):
    say("[온러닝] 나라별 products.xml — 주소 끝 품번")
    for cc, loc in (("KR", "ko-kr"), ("US", "en-us"), ("GB", "en-gb"), ("DE", "de-de")):
        if left() < 200: break
        us = walk("www.on.com", start=[f"https://www.on.com/{loc}/products.xml"], path_pre=f"/{loc}/", max_maps=5, per_host=60)
        found = set()
        for u in us:
            t = urllib.parse.urlsplit(u).path.rsplit("-", 1)[-1].upper()
            found.add(t)
        report("온러닝", cc, codes, found)

def drm(codes):
    say("[닥터마틴] 한국 쇼피파이 products.json 변형 품번 앞 8자리 · 미국·영국 사이트맵 /p/품번")
    found, n = set(), 0
    for page in range(1, 9):
        if left() < 200: break
        try:
            d = pf._json(pf.get(f"https://www.drmartens.co.kr/products.json?limit=250&page={page}")); n += 1
        except Exception as e:
            say(f"  KR products.json 오류: {str(e)[:80]}"); break
        ps = d.get("products") or []
        for p in ps:
            for v in p.get("variants") or []:
                s = str(v.get("sku") or "")
                if len(s) >= 8: found.add(s[:8].upper())
        if len(ps) < 250: break
    say(f"  KR products.json {n}쪽")
    report("닥터마틴", "KR", codes, found)
    for cc, host, pre in (("US", "www.drmartens.com", "/us/en/"), ("GB", "www.drmartens.com", "/uk/en_gb/")):
        if left() < 200: break
        us = walk(host, path_pre=pre, kid_pref=("product",), max_maps=10, per_host=60)
        f2 = {m.group(1) for u in us if (m := re.search(r"/p/(\d{8})", urllib.parse.urlsplit(u).path))}
        report("닥터마틴", cc, codes, f2)

def salomon(codes):
    say("[살로몬] 한국 쇼피파이 products.json 변형 품번")
    found, n = set(), 0
    for page in range(1, 9):
        if left() < 200: break
        try:
            d = pf._json(pf.get(f"https://salomon.co.kr/products.json?limit=250&page={page}")); n += 1
        except Exception as e:
            say(f"  KR products.json 오류: {str(e)[:80]}"); break
        ps = d.get("products") or []
        for p in ps:
            found.add(str(p.get("handle") or "").upper())
            for v in p.get("variants") or []:
                s = norm(v.get("sku"))
                found.add(s); found.add(s[:9]); found.add(s[:6])
        if len(ps) < 250: break
    say(f"  KR products.json {n}쪽")
    report("살로몬", "KR", codes, found)

def shop_tags(brand, codes, hosts, cut=None):
    """쇼피파이 몰 products.json — 변형 품번·태그·handle에 ERP 품번이 있는지"""
    say(f"[{brand}] 쇼피파이 products.json(변형 품번·태그·주소)")
    for cc, host, pre in hosts:
        found, n = set(), 0
        for page in range(1, 13):
            if left() < 200: break
            try:
                d = pf._json(pf.get(f"https://{host}{pre}products.json?limit=250&page={page}")); n += 1
            except Exception as e:
                say(f"  {cc} products.json 오류: {str(e)[:80]}"); break
            ps = d.get("products") or []
            for p in ps:
                tags = p.get("tags") if isinstance(p.get("tags"), list) else str(p.get("tags") or "").split(",")
                blob = " ".join([str(p.get("handle") or "")] + [str(t) for t in tags] + [str(v.get("sku") or "") for v in p.get("variants") or []]).upper()
                for c in codes:
                    cc_ = (cut(c) if cut else c)
                    if cc_ and cc_ in blob.replace("-", "") or (cc_ and cc_ in blob):
                        found.add(c)
            if len(ps) < 250: break
        say(f"  {cc} products.json {n}쪽")
        report(brand, cc, codes, found)

def look(host, start=None, n=4):
    """사이트맵 구조 보기(공개 주소만)"""
    maps = start or robots_maps(host)
    say(f"  {host} robots 사이트맵: {[m[-70:] for m in maps[:5]]}")
    for sm in maps[:2]:
        try:
            r = pf.get(sm); txt = body(r)
        except Exception as e:
            say(f"   {sm[-60:]} 오류 {str(e)[:60]}"); continue
        locs = [html.unescape(x) for x in re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", txt)]
        say(f"   {sm[-60:]}: 최종 {r.url[-60:]} · index={'<sitemapindex' in txt[:3000]} · {len(locs)}개 · 예 {[l[-90:] for l in locs[:n]]}")

def nike2(codes):
    say("[나이키 2] 묻는 방식 비교(공개 품번)")
    pub = [p["code"] for p in pf.PRODUCTS if p["brand"] == "나이키"][:3]
    m, l, cur = pf.MK["KR"]
    base = pf.NIKE_FEED.split("&filter=productInfo")[0].format(m=m, l=l)
    tries = [("한 품번", pf.NIKE_FEED.format(m=m, l=l, s=pub[0])),
             ("한 품번+count=50", pf.NIKE_FEED.format(m=m, l=l, s=pub[0]) + "&count=50"),
             ("styleCode", base + f"&filter=productInfo.merchProduct.styleCode({pub[0].split('-')[0]})"),
             ("styleCode+count=50", base + f"&filter=productInfo.merchProduct.styleCode({pub[0].split('-')[0]})&count=50"),
             ("styleColor %2C", base + "&filter=productInfo.merchProduct.styleColor(" + "%2C".join(pub[:2]) + ")"),
             ("styleColor 두 칸", base + "".join(f"&filter=productInfo.merchProduct.styleColor({c})" for c in pub[:2]))]
    for name, u in tries:
        try:
            d = pf._json(pf.get(u)); objs = d.get("objects") or []
            got = sorted({(pi.get("merchProduct") or {}).get("styleColor") for o in objs for pi in o.get("productInfo") or []} - {None})
            say(f"  {name}: 객체 {len(objs)} · 품번 {len(got)}개 {got[:6]} · pages {json.dumps(d.get('pages') or {})[:120]}")
        except Exception as e:
            say(f"  {name}: 오류 {str(e)[:60]}")
    if not codes:
        return
    cs = sorted(set(codes)); styles = sorted({c.split("-")[0] for c in cs})
    say(f"  ERP 나이키: 품번 {band(len(cs))} · 스타일(앞자리) {band(len(styles))} · 스타일당 평균 {len(cs) / max(1, len(styles)):.1f}색")
    # 한 품번씩 — 표본(앞에서 40개)으로 비율·시간
    smp = cs[:40]; found = set(); t0 = time.time()
    for c in smp:
        if left() < 300: break
        try:
            d = pf._json(pf.get(pf.NIKE_FEED.format(m=m, l=l, s=c)))
            for o in d.get("objects") or []:
                for pi in o.get("productInfo") or []:
                    if norm((pi.get("merchProduct") or {}).get("styleColor")) == c and (pi.get("merchPrice") or {}).get("fullPrice"):
                        found.add(c)
        except Exception as e:
            say(f"  한 품번 오류: {type(e).__name__}" + (f" {str(e)[:12]}" if str(e).startswith("HTTP") else ""))
    say(f"  KR 한 품번씩 표본 {len(smp)}개: {pct(len(found), len(smp))} 찾음 · {time.time() - t0:.0f}초")
    # 스타일 단위 — 표본 스타일 15개로 그 스타일의 ERP 색상을 몇 %나 덮는지
    ss = styles[:15]; got = set(); t0 = time.time(); nobj = []
    for st in ss:
        if left() < 300: break
        try:
            d = pf._json(pf.get(base + f"&filter=productInfo.merchProduct.styleCode({st})&count=50"))
            objs = d.get("objects") or []; nobj.append(len(objs))
            for o in objs:
                for pi in o.get("productInfo") or []:
                    sc = norm((pi.get("merchProduct") or {}).get("styleColor"))
                    if sc in cs and (pi.get("merchPrice") or {}).get("fullPrice"):
                        got.add(sc)
        except Exception as e:
            say(f"  스타일 오류: {type(e).__name__}" + (f" {str(e)[:12]}" if str(e).startswith("HTTP") else ""))
    tgt = [c for c in cs if c.split("-")[0] in ss]
    say(f"  KR 스타일 단위 표본 {len(ss)}개(ERP 색상 {band(len(tgt))}): {pct(len(got), len(tgt))} 찾음 · 스타일당 객체 최대 {max(nobj or [0])} · {time.time() - t0:.0f}초")

def arc(codes):
    say("[아크테릭스] arcteryx.com 사이트맵 주소 끝 숫자(모델) ↔ ERP 품번 앞 숫자")
    nums = [str(int(c.split("-")[0])) if c.split("-")[0].isdigit() else "" for c in codes]
    us = walk("arcteryx.com", path_pre="/us/en/", kid_pref=("product",), max_maps=10, per_host=60)
    found = {m.group(1).lstrip("0") for u in us if (m := re.search(r"-(\d{4,6})/?$", urllib.parse.urlsplit(u).path))}
    report("아크테릭스", "US 모델 숫자", nums, found)

def main():
    items = erp_list()
    by = collections.defaultdict(list)
    for it in items:
        b = AL.get(key(it.get("brand")))
        if b and norm(it.get("code")):
            by[b].append(norm(it.get("code")))
    nk = [re.sub(r"^[A-Z]{2,4}_", "", c) for c in by.get("나이키", [])]
    nike2(nk)
    say("[크록스] 사이트맵 구조")
    for h in ("www.crocs.co.kr", "www.crocs.com", "www.crocs.de"):
        look(h)
    say("[푸마] 독일 사이트맵 주소 예")
    look("eu.puma.com", start=["https://eu.puma.com/sitemaps/urls/de/sitemap_0.xml"], n=6)
    try:
        arc(by.get("아크테릭스", []))
    except Exception as e:
        say(f"[아크테릭스] 오류 {type(e).__name__}")
    shop_tags("드래곤디퓨전", by.get("드래곤디퓨전", []), (("US", "dragondiffusion.com", "/"),), cut=lambda c: c.split("-")[0])
    shop_tags("킨(KEEN)", by.get("킨(KEEN)", []), (("GB", "www.keenfootwear.co.uk", "/"), ("DE", "www.keenfootwear.de", "/en/")))
    # 살로몬 6자리(L 없는 품번)도
    sal = by.get("살로몬", []); found, n = set(), 0
    for page in range(1, 9):
        try:
            d = pf._json(pf.get(f"https://salomon.co.kr/products.json?limit=250&page={page}")); n += 1
        except Exception as e:
            break
        ps = d.get("products") or []
        for p in ps:
            for v in p.get("variants") or []:
                s_ = norm(v.get("sku")); found |= {s_, s_[:9], s_[1:7], s_[:6]}
            found.add(str(p.get("handle") or "").upper())
        if len(ps) < 250: break
    report("살로몬", "KR(L 없는 6자리 포함)", sal, found)
    say(f"끝 · {time.time() - T0:.0f}초")

if __name__ == "__main__":
    main()

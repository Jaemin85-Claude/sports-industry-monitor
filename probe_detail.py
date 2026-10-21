# -*- coding: utf-8 -*-
# 임시 시험(병합하지 않음) — 정가(할인 전) 칸이 페이지 어디에 있는지 보기: JSON-LD 가격·정가 명세, 정가 낱말 주변 글자
import json, re, sys, time, urllib.parse, urllib.robotparser, requests
UA = "Mozilla/5.0 (compatible; sports-industry-monitor price probe; +https://github.com/Jaemin85-Claude/sports-industry-monitor)"
H = {"User-Agent": UA, "Accept": "text/html,application/json;q=0.9,*/*;q=0.8"}
ROB = {}
def ok(url):
    p = urllib.parse.urlsplit(url); b = f"{p.scheme}://{p.netloc}"
    if b not in ROB:
        rp = urllib.robotparser.RobotFileParser()
        try: r = requests.get(b + "/robots.txt", headers=H, timeout=20); rp.parse(r.text.splitlines() if r.status_code == 200 else [])
        except Exception: rp.parse([])
        ROB[b] = rp
    return ROB[b].can_fetch(UA, url)
KEYS = ["regularPrice", "listPrice", "originalPrice", "basePrice", "compare_at_price", "compareAtPrice", "strikethrough", "fullPrice", "salePrice", "priceSpecification", "ListPrice", "StrikethroughPrice"]
def run(t):
    url = t["url"]
    if not ok(url): print(t["id"], "robots 금지"); return
    time.sleep(1.2)
    try: r = requests.get(url, headers=H, timeout=25)
    except Exception as e: print(t["id"], type(e).__name__); return
    print(f"## {t['id']} {r.status_code} {len(r.content)}B final={r.url[:100]}")
    if r.status_code != 200: return
    txt = r.text
    if t.get("json"):
        try: d = r.json()
        except Exception: print("   JSON 아님"); return
        if "product" in d:   # Shopify 상품
            p = d["product"]; vs = p.get("variants", [])
            print("   shopify", p.get("title"), "| variants", len(vs), "| price/compare", sorted({(v.get("price"), v.get("compare_at_price")) for v in vs})[:6], "| sku", [v.get("sku") for v in vs[:3]])
        elif "products" in d:
            for p in d["products"]:
                sk = " ".join(str(v.get("sku")) for v in p.get("variants", []))
                if any(c.lower() in sk.lower() or c.lower() in p.get("handle", "").lower() for c in t.get("codes", [])):
                    vs = p["variants"]; print("   match", p["handle"], "|", p["title"][:40], "|", sorted({(v.get("price"), v.get("compare_at_price")) for v in vs})[:4], "| sku", vs[0].get("sku"))
            print("   products", len(d["products"]))
        elif "objects" in d:
            for o in d["objects"][:1]:
                for pi in o.get("productInfo", [])[:1]:
                    mp = pi.get("merchPrice", {}); print("   nike", pi.get("productContent", {}).get("title"), "|", {k: mp.get(k) for k in ("fullPrice", "currentPrice", "currency", "discounted")})
            if not d.get("objects"): print("   nike 결과 없음")
        return
    for m in re.finditer(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', txt, re.S | re.I):
        s = m.group(1)
        for k in ("price", "lowPrice", "highPrice", "priceSpecification", "priceType"):
            for mm in list(re.finditer(rf'"{k}"\s*:', s))[:3]:
                print(f"   ld {k}: {s[mm.start():mm.start()+160]!r}")
    for k in KEYS:
        occ = [mm.start() for mm in re.finditer(re.escape(k), txt)]
        if occ:
            print(f"   {k} ×{len(occ)}:", " ‖ ".join(repr(txt[max(0, i-60):i+90]) for i in occ[:3]))
    for k in t.get("near", []):   # 품번 주변
        occ = [mm.start() for mm in re.finditer(re.escape(k), txt)]
        print(f"   near {k} ×{len(occ)}")
if __name__ == "__main__":
    for t in json.load(open(sys.argv[1])): run(t)

# -*- coding: utf-8 -*-
"""임시 시험(병합 안 함) 3회차 — 써코니 라이드 19 미국·영국·독일 페이지 가격 칸(판매가·원래 가격) 모양 확인. 저장·커밋 안 함."""
import re, time
import price_fetch as pf

pf.GAP = 0.8


def main():
    for u in ("https://www.saucony.com/DE/de_DE/ride-19/60823M.html", "https://www.saucony.com/UK/en_GB/ride-19/60823M.html",
              "https://www.saucony.com/en/ride-19/60823M.html"):
        try:
            r = pf.get(u)
        except Exception as e:
            print(f"✗ {u} {e}"); continue
        h = r.text.replace('\\"', '"')
        print(f"\n# {u} → {r.status_code} {len(h)//1000}KB {r.url}", flush=True)
        stock = sorted(set(re.findall(r'data-stock-number="([^"]+)"', h)))
        print(f"  stock-number {stock[:10]}")
        for pat in (r'class="price-[a-z-]+[^"]*"', r'itemprop="(?:price|priceCurrency|priceincents|lowPrice|highPrice)"', r'(?i)strike|msrp|uvp|statt|was-price|list-price',
                    r'(?i)"(?:price|salePrice|listPrice|standardPrice|originalPrice)"\s*:'):
            ms = list(re.finditer(pat, h))
            print(f"  [{pat[:40]}] {len(ms)}개")
            for m in ms[:14]:
                s = re.sub(r"\s+", " ", h[max(0, m.start() - 90): m.end() + 150])
                print(f"    @{m.start()} {s[:260]}")
        try:
            print("  page_price →", pf.page_price(r.text, "라이드 19", {"/DE/": "EUR", "/UK/": "GBP", "/en/": "USD"}[re.search(r"/(DE|UK|en)/", u).group(0)], ["S21055"]))
        except Exception as e:
            print("  page_price ✗", e)


if __name__ == "__main__":
    main()

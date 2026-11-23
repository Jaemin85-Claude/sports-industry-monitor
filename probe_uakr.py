# 임시 시험(병합 안 함 · PR 전에 지움): 언더아머 국내 공식 판매처(대표 결정 11/23 '4 네') — robots.txt·상품 페이지 정가·품번 읽기 확인(우리 봇 이름 · 우회 없음)
import re, time, json, urllib.parse
import price_fetch as pf
SITES = {
  "SSG 판매자관": ["https://m.ssg.com/sellerhome/133919.ssg", "https://www.ssg.com/search.ssg?query=1326413-001"],
  "롯데ON 롯데백화점": ["https://www.lotteon.com/display/shop/seltBrdShop/2/P2874", "https://www.lotteon.com/p/product/LE1216206083"],
  "무신사": ["https://www.musinsa.com/brand/underarmour/products", "https://www.musinsa.com/search/goods?keyword=1326413-001"],
  "이랜드몰": ["https://www.elandmall.co.kr/i/item?itemNo=2209282526&lowerVendNo=LV21032699"],
  "더현대": ["https://www.thehyundai.com/front/sec/searchList.thd?searchTerm=1326413"],
}
def main():
    for name, urls in SITES.items():
        for u in urls:
            ok, why = pf.robots_ok(u)
            line = f"{name} | {urllib.parse.urlsplit(u).netloc}{urllib.parse.urlsplit(u).path[:50]} | robots {'허용' if ok else '막음 — ' + why}"
            if ok:
                try:
                    r = pf.get(u)
                    t = r.text
                    ld = [n for n in pf._ld_nodes(t, pf.REL) if pf._types(n) & {"product", "productgroup"}] if hasattr(pf, "_ld_nodes") else []
                    codes = sorted(set(re.findall(r"\b1\d{6}-\d{3}\b", t)))[:5]
                    lp = re.findall(r"(정상가[^0-9]{0,20}[0-9,]{4,9}|소비자가[^0-9]{0,20}[0-9,]{4,9}|\"(?:normalPrice|listPrice|orgPrice|originalPrice|sellPrc|normalPrc|consumerPrice|slPrc)\"\s*:\s*\"?[0-9,]+)", t)[:4]
                    line += f" | HTTP {r.status_code} · {len(t):,}자 · 봇 확인 화면 {'예' if pf.CHALLENGE.search(t[:30000]) else '아님'} · JSON-LD 상품 {len(ld)} · 품번 {codes} · 정가 단서 {lp}"
                except Exception as e:
                    line += f" | 실패 {type(e).__name__}: {str(e)[:100]}"
            print(line)
            time.sleep(2)
if __name__ == "__main__":
    main()

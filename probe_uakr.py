# 임시 시험(병합 안 함 · PR 전에 지움): 언더아머 국내 공식 판매처(대표 결정 11/23 '4 네') — robots.txt·상품 페이지 정가·품번 읽기 확인(우리 봇 이름 · 우회 없음)
import re, time, json, urllib.parse
import price_fetch as pf
SITES = {
  "LF몰(갤러리아)": ["https://m.lfmall.co.kr/app/product/E0TJXX03769", "https://www.lfmall.co.kr/app/product/E0TJXX03769"],
  "롯데아이몰": ["https://m.lotteimall.com/goods/viewGoodsDetail.lotte?goods_no=2872897689", "https://www.lotteimall.com/goods/viewGoodsDetail.lotte?goods_no=2872897689"],
  "현대H몰": ["https://www.hmall.com/pd/pda/itemPtc?slitmCd=2141234567", "https://www.hmall.com/p/dpa/searchSpexSectItem.do?searchTerm=1326413"],
  "AK몰": ["https://www.akmall.com/goods/GoodsDetail.do?goods_id=100000000"],
  "네이버 브랜드스토어": ["https://brand.naver.com/underarmour", "https://brand.naver.com/underarmour/products/1"],
  "갤러리아": ["https://www.galleria.co.kr/"],
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

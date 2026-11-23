# 임시 시험(병합 안 함 · PR 전에 지움): 국내 몰 SKU 색인 길 찾기 — 공개 목록·검색 페이지를 우리 봇이 읽을 수 있는지(robots.txt · 우회 없음)
import re, time, urllib.parse
import price_fetch as pf
T = [
  ("킨 검색", "https://www.keenfootwear.kr/goods/goods_search.php?keyword=1022258", r"goodsNo=(\d+)"),
  ("킨 첫 화면", "https://www.keenfootwear.kr/", r"goods_list\.php\?cateCd=(\d+)"),
  ("킨 목록", "https://www.keenfootwear.kr/goods/goods_list.php?cateCd=001", r"goodsNo=(\d+)"),
  ("우포스 검색", "https://www.oofos.co.kr/goods/goods_search.php?keyword=1000", r"goodsNo=(\d+)"),
  ("아크테릭스 검색", "https://arcteryx.co.kr/search?keyword=X000009556", r"products/view/(\d+)"),
  ("아크테릭스 첫 화면", "https://arcteryx.co.kr/", r"products/(?:view/)?(\d{5,7})"),
  ("코오롱 헌터 목록", "https://www.kolonmall.com/Brands/HUNTER/List/133010071605", r"/Product/(K\w+)"),
  ("코오롱 드래곤디퓨전", "https://www.kolonmall.com/Brands/DRAGON_DIFFUSION", r"/Product/(\w+)"),
  ("코오롱 검색", "https://www.kolonmall.com/Search?keyword=WFT1000RMA", r"/Product/(\w+)"),
]
def main():
    for name, u, rx in T:
        ok, why = pf.robots_ok(u)
        line = f"{name} | {urllib.parse.urlsplit(u).netloc}{urllib.parse.urlsplit(u).path} | robots {'허용' if ok else '막음 — ' + why}"
        if ok:
            try:
                r = pf.get(u); t = r.text
                hits = re.findall(rx, t)
                codes = sorted(set(re.findall(r"\b(?:WFT|WFS|W2BAS|AJ[A-Z]{3})\w{4,10}\b|\b1\d{6}\b", t)))[:6]
                line += f" | HTTP {r.status_code} · {len(t):,}자 · 봇 확인 {'예' if pf.CHALLENGE.search(t[:30000]) else '아님'} · 찾은 것 {len(set(hits))}개 {sorted(set(hits))[:5]} · 품번 모양 {codes} · 넘겨진 주소 {r.url[:80] if r.url != u else '-'}"
            except Exception as e:
                line += f" | 실패 {type(e).__name__}: {str(e)[:100]}"
        print(line)
        time.sleep(2)
if __name__ == "__main__":
    main()

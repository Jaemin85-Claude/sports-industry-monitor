# 임시 시험(병합 안 함 · 끝나면 바로 지움): v1.45 스투시·아미·가니 한국 공식몰 SKU 정가 — 공개 품번 시험 목록(ERP_SKU_TEST) · 우리 봇 이름 · robots.txt 준수
import datetime, json, os, time
import price_fetch as pf
C = [("STUSSY", "1905210-0001"), ("STUSSY", "1925103"), ("STUSSY", "1311209-0001"), ("STUSSY", "1999999-0001"),
     ("AMI", "UKC408-KN0150-185"), ("AMI", "UKS913-KN0220-A375"), ("AMI", "UKS913-KN0220-A374"), ("AMI", "USH906-CO0251-A254"), ("AMI", "UKC408-KN0150-999"),
     ("GANNI", "A1170016-683"), ("GANNI", "A1050257-252"), ("GANNI", "A1040422-591"), ("GANNI", "A1040422-06P"), ("GANNI", "A1010227-065"),
     ("GANNI", "A7161-943"), ("GANNI", "A6946-099"), ("GANNI", "A1060022-001"), ("GANNI", "C2100016-0RM"), ("GANNI", "A1234567-001")]
os.environ["ERP_SKU_TEST"] = json.dumps([{"brand": b, "code": c, "status": "selling"} for b, c in C])
pf._sku_slot = lambda *a: True
for u in ("https://kr.stussy.com/products.json?page=2", "https://kr.stussy.com/products/1905210-triple-crown-tee-rock.json", "https://www.amiparis.com/ko-kr/products.json?limit=250&page=1",
          "https://www.ganni.com/en-kr/polo-shirt-in-navy-jersey-A1170016.html", "https://www.ganni.com/sitemap_index.xml"):
    print("robots", u, pf.robots_ok(u))
t0 = time.time(); td = datetime.date.today()
items, meta = pf.sku_stage({"items": []}, time.time(), td, td.isoformat(), {}, [])
print("=== ITEMS ===")
for it in items:
    print(json.dumps({k: it.get(k) for k in ("id", "code", "name", "cat", "kr_status", "m")}, ensure_ascii=False))
print("blocked", sorted(pf._BLOCKED), "sec", round(time.time() - t0))

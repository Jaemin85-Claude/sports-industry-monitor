# 임시 시험(병합 안 함 · 끝나면 바로 지움): v1.46 메종키츠네 한국·팔로마울(코오롱몰) SKU 정가 — 공개 품번 시험 목록(ERP_SKU_TEST) · 우리 봇 이름 · robots.txt 준수
import datetime, json, os, time
import price_fetch as pf
C = [("MAISON KITSUNE", "PM00109KJ0119-H170"), ("MAISON KITSUNE", "PM00109KJ0119-P999"), ("MAISON KITSUNE", "MRMWP02WF4082-0553"), ("MAISON KITSUNE", "QW01650KA0033-P199"),
     ("MAISON KITSUNE", "PU00301KM0330-0472"), ("MAISON KITSUNE", "MRUKC00KT1006-P623"), ("MAISON KITSUNE", "QM00425WD4033-0603"), ("MAISON KITSUNE", "LM99999KM0001-P199"),
     ("MAISON KITSUNE", "LM00101KM0001-P199"),
     ("PALOMA WOOL", "RJ9022-247"), ("PALOMA WOOL", "RJ9022-135"), ("PALOMA WOOL", "RJ9022-999"), ("PALOMA WOOL", "TJ9005-135"), ("PALOMA WOOL", "TV4003-134"),
     ("PALOMA WOOL", "RJ9025-200"), ("PALOMA WOOL", "XP6002-246"), ("PALOMA WOOL", "TJ0810-120"), ("PALOMA WOOL", "RJ9023-203"), ("PALOMA WOOL", "TJ0813-248")]
os.environ["ERP_SKU_TEST"] = json.dumps([{"brand": b, "code": c, "status": "selling"} for b, c in C])
pf._sku_slot = lambda *a: True
for u in (pf.MK_SM_IDX, "https://maisonkitsune.com/kr/fox-head-oversize-tee-shirt-dark-grey-melange-6855fab7d56bc.html", "https://www.kolonmall.com/Brands/PALOMAWOOL/List/133020162660",
          "https://www.kolonmall.com/Product/W1WAX25213NYX"):
    print("robots", u, pf.robots_ok(u))
t0 = time.time(); td = datetime.date.today()
items, meta = pf.sku_stage({"items": []}, time.time(), td, td.isoformat(), {}, [])
print("=== ITEMS ===")
for it in items:
    print(json.dumps({k: it.get(k) for k in ("id", "code", "name", "cat", "kr_status", "m")}, ensure_ascii=False))
print("blocked", sorted(pf._BLOCKED), "sec", round(time.time() - t0))
# 2
# 3
# 4
# 5

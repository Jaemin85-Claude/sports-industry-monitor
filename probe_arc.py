# 임시 시험(병합 안 함 · 끝나면 바로 지움): price_fetch v1.41 아크테릭스 한국 — 실제 Firecrawl 검색 + 실제 공식몰 페이지(우리 봇) · 공개 품번(대표 상품 모델)만 · 키는 찍지 않음
import json, os, sys, time, datetime, io, contextlib
import price_fetch as pf
os.environ["ERP_SKU_TEST"] = json.dumps([{"brand": "ARC'TERYX", "code": c, "status": "selling"} for c in ["10276", "X000009556", "10481-BLACK", "10521"]])
pf._sku_slot = lambda *a: True
day = datetime.date.today()
buf = io.StringIO()
t0 = time.time()
with contextlib.redirect_stdout(buf):
    items, meta = pf.sku_stage({}, time.time(), day, day.isoformat(), {}, [])
log = buf.getvalue()
print("\n".join(l for l in log.splitlines() if "아크테릭스" in l or l.startswith("SKU 정가")))
for it in items:
    k = it["m"].get("KR") or {}
    print(it["id"], it.get("name"), k.get("p"), k.get("sp"), k.get("lvl"), (k.get("url") or "")[-40:])
print("Firecrawl 검색", pf._FC["n"], "번", pf._FC["stop"] or "", "· 키 있음" if os.environ.get("FIRECRAWL_API_KEY") else "· 키 없음", f"· {time.time()-t0:.0f}초")

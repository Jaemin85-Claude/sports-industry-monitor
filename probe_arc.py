# 임시 시험(병합 안 함 · 끝나면 바로 지움): price_fetch v1.41 아크테릭스 한국 — 대표 상품 모델(공개 품번)을 대표 상품 한국 주소로 받기(우리 봇 · Firecrawl 안 씀)
import json, os, time, datetime, io, contextlib
import price_fetch as pf
os.environ.pop("FIRECRAWL_API_KEY", None)
rep = [it for it in json.load(open("docs/prices.json"))["items"] if it.get("brand") == "아크테릭스" and it.get("kind") != "sku"]
codes = [pf._arc_norm(it["code"]) for it in rep[:6]]
os.environ["ERP_SKU_TEST"] = json.dumps([{"brand": "ARC'TERYX", "code": c, "status": "selling"} for c in codes])
pf._sku_slot = lambda *a: True
day = datetime.date.today()
rc = {"아크테릭스": {pf._sku_norm(it["code"]) for it in rep}}
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    items, meta = pf.sku_stage({}, time.time(), day, day.isoformat(), rc, rep)
print("\n".join(l for l in buf.getvalue().splitlines() if "아크테릭스" in l or l.startswith("SKU 정가")))
repp = {pf._arc_norm(it["code"]): (it["m"].get("KR") or {}).get("p") for it in rep}
for it in items:
    k = it["m"].get("KR") or {}
    print(it["id"], it.get("name"), "SKU", k.get("p"), "· 대표 상품", repp.get(it["code"]), "· 같음" if k.get("p") == repp.get(it["code"]) else "· 다름", k.get("lvl"), (k.get("url") or "")[-30:])
print("Firecrawl 검색", pf._FC["n"])

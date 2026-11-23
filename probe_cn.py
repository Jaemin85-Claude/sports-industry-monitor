# -*- coding: utf-8 -*-
# 임시 시험(병합하지 않음 · PR 전에 지움) — price_fetch v1.30 SKU 단계 일본(나이키·크록스·온러닝·킨) 읽기를 공개 품번 시험 목록으로 확인.
import datetime, json, os, time
TEST = [{"brand": "나이키", "code": "CW2288-111", "status": "selling"}, {"brand": "크록스", "code": "10001-001", "status": "selling"},
        {"brand": "온러닝", "code": "3MF10071200", "status": "selling"}, {"brand": "킨(KEEN)", "code": "1022258", "status": "selling"}]
os.environ["ERP_SKU_TEST"] = json.dumps(TEST, ensure_ascii=False)
import price_fetch as pf
today = datetime.datetime.now(pf.KST).date(); t0 = time.time()
rep = [it for it in json.load(open("docs/prices.json", encoding="utf-8"))["items"] if it.get("kind") != "sku"]
pf._sku_slot = lambda *a: True
pf.SKU_CC = ("JP",)   # 시험 — 일본만
for b, h in pf.SKU_BRANDS.items():
    h["cc"] = tuple(c for c in h["cc"] if c == "JP")
items, meta = pf.sku_stage({}, t0, today, today.isoformat(), {}, rep)
for it in items:
    print("ITEM", it["id"], it["name"], json.dumps({cc: {k: o.get(k) for k in ("p", "cur", "sale", "sp", "url")} for cc, o in it["m"].items()}, ensure_ascii=False))
print("held", [(it["id"], it.get("held")) for it in items if it.get("held")], f"{time.time() - t0:.0f}초")

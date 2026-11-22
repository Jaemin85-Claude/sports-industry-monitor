# -*- coding: utf-8 -*-
# 임시 시험(병합하지 않음 · PR 전에 지움) — price_fetch v1.29 SKU 단계를 공개 품번 시험 목록(ERP_SKU_TEST)으로 GitHub 서버에서 돌려 읽는 법 확인.
# 공개 품번(이미 공개된 대표 상품·공식몰 상품)만 씀 — ERP 목록(Secrets)은 이 시험에서 안 씀.
import datetime, json, os, time
TEST = [{"brand": "나이키", "code": c, "status": "selling"} for c in ("CW2288-111", "CW2288-001", "DD1391-100", "FD4116-001", "315122-111", "ZZ9999-999")] + [
    {"brand": "크록스", "code": c, "status": "selling"} for c in ("10001-001", "10001-100", "206991-001", "999999-001")] + [
    {"brand": "푸마", "code": "396463-01", "status": "selling"}, {"brand": "푸마", "code": "398846-01", "status": "selling"},
    {"brand": "언더아머", "code": "1372586-001", "status": "selling"}, {"brand": "온러닝", "code": "3MF10071200", "status": "selling"},
    {"brand": "닥터마틴", "code": "11838002", "status": "selling"}, {"brand": "닥터마틴", "code": "15265001", "status": "selling"},
    {"brand": "살로몬", "code": "L47450600", "status": "selling"}, {"brand": "킨(KEEN)", "code": "1022258", "status": "selling"},
    {"brand": "킨(KEEN)", "code": "1001907", "status": "planned"}, {"brand": "아크테릭스", "code": "9556-BLACK", "status": "selling"}]
os.environ["ERP_SKU_TEST"] = json.dumps(TEST, ensure_ascii=False)
import price_fetch as pf
today = datetime.datetime.now(pf.KST).date()
t0 = time.time()
items, meta = pf.sku_stage({}, t0, today, today.isoformat(), {})
for it in items:
    print("ITEM", it["id"], it["name"], it["cat"], json.dumps({cc: {k: o.get(k) for k in ("p", "cur", "sale", "sp", "lvl", "url")} for cc, o in it["m"].items()}, ensure_ascii=False))
print("sku_q", len(meta.get("sku_q") or {}), f"{time.time() - t0:.0f}초")
# rerun 1795335667

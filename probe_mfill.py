# 임시 시험(병합 안 함 · PR 전에 지움): v1.32 모델 단위 국내 정가 — 공개 품번(가짜 색상 포함)으로 실제 나이키·크록스 국내 몰에서 확인
import datetime, json, os, time
import price_fetch as pf
def main():
    test = [{"brand": "나이키", "code": "CW2288-999", "status": "selling"},   # 에어포스 1 — 없는 색상 → 모델 단위?
            {"brand": "나이키", "code": "DD1391-999", "status": "selling"},   # 덩크 로우 — 국내 색상 정가가 다르면 안 씀
            {"brand": "나이키", "code": "FD4116-999", "status": "selling"},   # 캄 슬라이드
            {"brand": "크록스", "code": "10001-ZZZ", "status": "selling"},     # 클래식 클로그
            {"brand": "크록스", "code": "206991-ZZZ", "status": "planned"}]    # 클래식 클로그 키즈? (모델 번호 그대로)
    os.environ["ERP_SKU_TEST"] = json.dumps(test)
    pf._sku_slot = lambda k, e, t: True
    pf.SKU_BRANDS = {b: dict(h, cc=("KR",)) for b, h in pf.SKU_BRANDS.items()}   # 국내만(요청 줄임)
    today = datetime.datetime.now(pf.KST).date()
    t = time.time()
    items, meta = pf.sku_stage({}, t, today, today.isoformat(), {}, [])
    for it in items:
        print("  결과", it["id"], it["code"], it.get("name"), {cc: (o.get("p"), o.get("lvl"), o.get("url", "")[-40:]) for cc, o in it["m"].items()})
    print(f"걸린 시간 {time.time() - t:.0f}초")
if __name__ == "__main__":
    main()

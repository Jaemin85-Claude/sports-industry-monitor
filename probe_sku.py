# -*- coding: utf-8 -*-
# 임시 시험 5(병합하지 않음) — 이 브랜치 price_fetch v1.20 PRODUCTS로 온러닝 바꾼 상품 정가 읽기 · 푸마 일본 PAUSED · 관세청 오픈 API 명세 전체(키 없이)
import json, time, requests
import price_fetch as pf
import logistics_fetch as lf
def out(k, **kw): print(k, json.dumps(kw, ensure_ascii=False)[:6000], flush=True)
P = {p["id"]: p for p in pf.PRODUCTS}
out("COUNT", products=len(pf.PRODUCTS), values=sum(len(pf.ccs(p)) for p in pf.PRODUCTS))
for pid in ("on-cloudmonster", "on-cloudmonster1wp"):
    for cc in pf.ccs(P[pid]):
        try:
            (p, ex), u = pf.fetch_one(P[pid], cc); out("READ", id=pid, cc=cc, p=p, cur=pf.MK[cc][2], by=ex.get("by"), now=ex.get("cur_price"))
        except Exception as e:
            out("READ_ERR", id=pid, cc=cc, err=f"{type(e).__name__}: {e}"[:200])
out("PAUSED", v={pid: pf.paused_of(P[pid], "JP") for pid in P if pid.startswith("puma-") and "JP" in pf.ccs(P[pid])})
for ds in ("15116807",):
    r = requests.get("https://infuser.odcloud.kr/oas/docs", params={"namespace": f"{ds}/v1"}, headers=lf.UA, timeout=(10, 30))
    out("OAS_FULL", ds=ds, doc=r.json())
out("DONE")

# 임시 시험(병합하지 않음) — IMF PortWatch 질의가 GitHub 서버에서 어떻게 실패하는지 잼
import datetime, json, sys, time
import requests

UA = {"User-Agent": "Mozilla/5.0 (sports-industry-monitor logistics; +https://github.com/Jaemin85-Claude/sports-industry-monitor)"}
BASE = "https://services9.arcgis.com/weJ1QsnbMYJlCHdG/arcgis/rest/services/{}/FeatureServer/0"
CH = "Daily_Chokepoints_Data"; PO = "Daily_Ports_Data"
ITEMS = [(CH, "chokepoint6", "호르무즈"), (CH, "chokepoint4", "바브엘만데브"), (CH, "chokepoint1", "수에즈"), (CH, "chokepoint7", "희망봉"),
         (PO, "port1065", "부산"), (PO, "port744", "제벨알리"), (PO, "port561", "코르파칸"), (PO, "port362", "푸자이라"),
         (PO, "port474", "홍콩"), (PO, "port1114", "로테르담"), (PO, "port57", "앤트워프"), (PO, "port1188", "상하이"), (PO, "port2027", "양산"),
         (PO, "port1201", "싱가포르"), (PO, "port824", "닝보"), (PO, "port1414", "옌톈"), (PO, "port1189", "서커우"), (PO, "port1069", "칭다오"),
         (PO, "port664", "LA/롱비치"), (PO, "port960", "포트클랑"), (PO, "port446", "함부르크")]
FIELDS = {CH: "date,n_total,n_container", PO: "date,portcalls,portcalls_container"}
T0 = time.monotonic()

def q(layer, where, fields, order=True, count=False, label=""):
    p = {"where": where, "outFields": fields, "resultOffset": 0, "resultRecordCount": 1000, "f": "json"}
    if order:
        p["orderByFields"] = "date ASC"
    if count:
        p = {"where": where, "returnCountOnly": "true", "f": "json"}
    t = time.monotonic()
    rec = {"label": label, "t": round(t - T0)}
    try:
        r = requests.get(BASE.format(layer) + "/query", params=p, headers=UA, timeout=(15, 60))
        rec["http"] = r.status_code
        rec["sec"] = round(time.monotonic() - t, 1)
        try:
            d = r.json()
        except ValueError:
            rec["err"] = "not json: " + r.text[:120]
            return rec
        if "error" in d:
            rec["err"] = json.dumps(d["error"], ensure_ascii=False)[:220]
        elif count:
            rec["count"] = d.get("count")
        else:
            fs = d.get("features") or []
            rec["n"] = len(fs)
            rec["xfer"] = d.get("exceededTransferLimit")
            if fs:
                ds = [f.get("attributes", {}).get("date") for f in fs]
                rec["first"], rec["last"] = str(ds[0])[:13], str(ds[-1])[:13]
            else:
                rec["keys"] = sorted(d.keys())
        rec["hdr"] = {k: r.headers.get(k) for k in ("x-esri-query-request-units", "x-esri-org-request-units", "x-cache", "age", "x-esri-ftiles-cache-compress") if r.headers.get(k)}
    except Exception as e:
        rec["sec"] = round(time.monotonic() - t, 1)
        rec["exc"] = f"{type(e).__name__}: {str(e)[:150]}"
    return rec

def show(tag, rec):
    print(tag, json.dumps(rec, ensure_ascii=False), flush=True)

def bad(rec):
    return "err" in rec or "exc" in rec or rec.get("n", 1) == 0 or rec.get("http", 200) != 200

# A: 메타데이터
for layer in (CH, PO):
    try:
        m = requests.get(BASE.format(layer), params={"f": "json"}, headers=UA, timeout=(15, 60)).json()
        flds = {f["name"]: f["type"] for f in m.get("fields", [])}
        print("META", layer, json.dumps({"maxRecordCount": m.get("maxRecordCount"), "standardMaxRecordCount": m.get("standardMaxRecordCount"),
              "date_type": flds.get("date"), "year_type": flds.get("year"), "portid_type": flds.get("portid"),
              "indexes": [(i.get("name"), i.get("fields")) for i in (m.get("indexes") or [])],
              "lastEdit": (m.get("editingInfo") or {}).get("lastEditDate"), "dataLastEdit": (m.get("editingInfo") or {}).get("dataLastEditDate"),
              "supportsPagination": (m.get("advancedQueryCapabilities") or {}).get("supportsPagination")}, ensure_ascii=False), flush=True)
    except Exception as e:
        print("META", layer, "fail", type(e).__name__, str(e)[:150], flush=True)
try:
    who = requests.get("https://ipinfo.io/json", timeout=5).json()
    print("RUNNER", ".".join(str(who.get("ip", "")).split(".")[:2]), who.get("region"), who.get("org"), flush=True)
except Exception:
    pass

def cur(layer, pid):
    return f"portid='{pid}' AND year>=2025"

def pass_all(tag):
    fails = []
    for layer, pid, nm in ITEMS:
        rec = q(layer, cur(layer, pid), FIELDS[layer], label=nm)
        show(tag, rec)
        if bad(rec):
            fails.append((layer, pid, nm))
        time.sleep(0.5)
    print(f"{tag} SUMMARY 실패 {len(fails)}/{len(ITEMS)}: {' '.join(x[2] for x in fails)}", flush=True)
    return fails

# B: 지금 질의 그대로 전부
f1 = pass_all("B")
# C: 실패한 것만 5초 뒤 다시, 그래도 실패면 30초 뒤 다시
f2 = []
for layer, pid, nm in f1:
    time.sleep(5)
    rec = q(layer, cur(layer, pid), FIELDS[layer], label=nm)
    show("C5", rec)
    if bad(rec):
        f2.append((layer, pid, nm))
print(f"C5 SUMMARY 다시 실패 {len(f2)}/{len(f1)}", flush=True)
if f2:
    time.sleep(30)
f3 = []
for layer, pid, nm in f2:
    rec = q(layer, cur(layer, pid), FIELDS[layer], label=nm)
    show("C30", rec)
    if bad(rec):
        f3.append((layer, pid, nm))
    time.sleep(3)
print(f"C30 SUMMARY 다시 실패 {len(f3)}/{len(f2)}", flush=True)
# D: 질의 모양 비교(6곳)
today = datetime.date.today()
recent = (today - datetime.timedelta(days=70)).isoformat()
SAMPLE = [x for x in ITEMS if x[2] in ("호르무즈", "부산", "홍콩", "상하이", "앤트워프", "함부르크")]
for layer, pid, nm in SAMPLE:
    vs = [("V1 지금", cur(layer, pid), True, False),
          ("V2 정렬 없음", cur(layer, pid), False, False),
          ("V3 date 조건", f"portid='{pid}' AND date >= timestamp '2025-01-01 00:00:00'", True, False),
          ("V4 최근 70일", f"portid='{pid}' AND date >= timestamp '{recent} 00:00:00'", True, False),
          ("V5 portid만", f"portid='{pid}'", True, False),
          ("V6 건수만", cur(layer, pid), False, True)]
    for vn, w, order, count in vs:
        rec = q(layer, w, FIELDS[layer], order=order, count=count, label=f"{nm} {vn}")
        show("D", rec)
        time.sleep(0.5)
# E: 다시 전부(시간이 지난 뒤)
pass_all("E")
print("TOTAL", round(time.monotonic() - T0), "s", flush=True)

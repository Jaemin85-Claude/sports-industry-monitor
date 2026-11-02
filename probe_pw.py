# -*- coding: utf-8 -*-
"""임시 시험(병합하지 않음) — PortWatch 항만 9곳이 10/28부터 빈 응답(0행)인 원인 확인. GitHub 서버에서 1회 실행."""
import json, time, requests

BASE = "https://services9.arcgis.com/weJ1QsnbMYJlCHdG/arcgis/rest/services"
UA = {"User-Agent": "sports-industry-monitor (+https://github.com/Jaemin85-Claude/sports-industry-monitor)"}
S = requests.Session()
S.headers.update(UA)

PORT_IDS = {"Busan": "port1065", "Jebel Ali": "port744", "Khor Fakkan": "port561", "Fujairah": "port362",
            "Hong Kong": "port474", "Rotterdam": "port1114", "Antwerp": "port57",
            "Shanghai": ("port1188", "port2027"), "Singapore": "port1201", "Ningbo": "port824",
            "Shenzhen": ("port1414", "port1189"), "Qingdao": "port1069", "Los Angeles-Long Beach": "port664",
            "Port Klang": "port960", "Hamburg": "port446"}
CHOKE = ["chokepoint6", "chokepoint4", "chokepoint1", "chokepoint7"]


def get(url, params=None, label=""):
    t0 = time.monotonic()
    try:
        r = S.get(url, params=params, timeout=(15, 60))
        dt = time.monotonic() - t0
        try:
            d = r.json()
        except ValueError:
            return {"_http": r.status_code, "_t": round(dt, 1), "_text": r.text[:200]}
        if isinstance(d, dict):
            d["_http"] = r.status_code
            d["_t"] = round(dt, 1)
        return d
    except Exception as e:
        return {"_exc": f"{type(e).__name__}: {str(e)[:150]}", "_t": round(time.monotonic() - t0, 1)}


def short(d):
    if not isinstance(d, dict):
        return str(d)[:200]
    if "_exc" in d:
        return d["_exc"]
    if "error" in d:
        e = d["error"]
        return f"ERR {e.get('code')} {str(e.get('message'))[:70]} {str(e.get('details'))[:80]} ({d['_t']}s)"
    if "count" in d:
        return f"count={d['count']} ({d['_t']}s)"
    if "features" in d:
        fs = d["features"]
        a = fs[0].get("attributes") if fs else {}
        z = fs[-1].get("attributes") if fs else {}
        return f"rows={len(fs)} exceeded={d.get('exceededTransferLimit')} first={a} last={z} ({d['_t']}s)"
    return json.dumps(d, ensure_ascii=False)[:200]


def q(layer, **params):
    params.setdefault("f", "json")
    return get(f"{BASE}/{layer}/FeatureServer/0/query", params)


print("=== A. 서비스 목록(Port·Choke 들어간 것)")
d = get(BASE, {"f": "json"})
for s in (d.get("services") or []):
    n = s.get("name", "")
    if any(k in n.lower() for k in ("port", "choke", "trade", "daily")):
        print("  ", n, s.get("type"))
print("  services 총", len(d.get("services") or []), short(d) if "error" in d or "_exc" in d else "")

print("=== B. 층 정보")
for layer in ("Daily_Ports_Data", "Daily_Chokepoints_Data", "PortWatch_ports_database"):
    m = get(f"{BASE}/{layer}/FeatureServer/0", {"f": "json"})
    if "error" in m or "_exc" in m:
        print("  ", layer, short(m))
        continue
    ei = m.get("editingInfo") or {}
    fl = {f["name"]: f["type"].replace("esriFieldType", "") for f in (m.get("fields") or [])}
    print("  ", layer, "| lastEdit", ei.get("lastEditDate"), "dataLastEdit", ei.get("dataLastEditDate"),
          "| maxRecordCount", m.get("maxRecordCount"), "| standardMaxRecordCount", m.get("standardMaxRecordCount"),
          "| indexes", [i.get("fields") for i in (m.get("indexes") or [])][:12])
    print("     fields", {k: fl[k] for k in list(fl)[:30]})
    svc = get(f"{BASE}/{layer}/FeatureServer", {"f": "json"})
    print("     service: currentVersion", svc.get("currentVersion"), "| serviceItemId", svc.get("serviceItemId"),
          "| layers", [(l.get("id"), l.get("name")) for l in (svc.get("layers") or [])], "| tables",
          [(l.get("id"), l.get("name")) for l in (svc.get("tables") or [])])
    time.sleep(1)

print("=== C. 항만 목록에서 이름으로 번호 찾기")
names = ["Busan", "Hong Kong", "Antwerp", "Shanghai", "Yangshan", "Singapore", "Ningbo", "Los Angeles", "Long Beach",
         "Port Klang", "Hamburg", "Jebel Ali", "Rotterdam", "Shenzhen", "Yantian", "Shekou", "Qingdao", "Khor Fakkan", "Fujairah"]
for nm in names:
    r = q("PortWatch_ports_database", where=f"portname LIKE '%{nm}%'", outFields="*", resultRecordCount=8)
    if "features" in r:
        rows = [f["attributes"] for f in r["features"]]
        print(f"  {nm}: " + " | ".join(f"{a.get('portid')} {a.get('portname')} {a.get('ISO3') or a.get('iso3') or a.get('country')}"
                                       for a in rows) + f" ({r['_t']}s)")
        if nm == "Busan" and rows:
            print("     Busan 행 전체 칸:", json.dumps(rows[0], ensure_ascii=False)[:600])
    else:
        print(f"  {nm}: {short(r)}")
    time.sleep(0.7)

print("=== D. 질의별 건수 — 항목마다 2번(오류가 우연인지 늘 그런지)")
items = [(k, v) for k, v in PORT_IDS.items()]
for name, ids in items:
    for pid in (ids if isinstance(ids, tuple) else (ids,)):
        res = []
        for where in (f"portid='{pid}' AND year>=2025", f"portid='{pid}'", f"portid='{pid}' AND year=2026"):
            for k in range(2):
                r = q("Daily_Ports_Data", where=where, returnCountOnly="true")
                res.append(f"[{where.replace(f'portid=' + chr(39) + pid + chr(39), 'id')}#{k+1}] {short(r)}")
                time.sleep(0.6)
        mx = q("Daily_Ports_Data", where=f"portid='{pid}'",
               outStatistics=json.dumps([{"statisticType": "max", "onStatisticField": "date", "outStatisticFieldName": "mx"},
                                         {"statisticType": "count", "onStatisticField": "date", "outStatisticFieldName": "n"}]))
        print(f"  {name} {pid}: " + " ; ".join(res) + f" ; max/count {short(mx)}")
        time.sleep(0.6)
for pid in CHOKE:
    res = []
    for k in range(2):
        r = q("Daily_Chokepoints_Data", where=f"portid='{pid}' AND year>=2025", returnCountOnly="true")
        res.append(f"#{k+1} {short(r)}")
        time.sleep(0.6)
    print(f"  {pid}: " + " ; ".join(res))

print("=== E. 지금 코드와 같은 질의(행 받기) — 부산·제벨알리 각 2번")
for pid in ("port1065", "port744"):
    for k in range(2):
        r = q("Daily_Ports_Data", where=f"portid='{pid}' AND year>=2025", outFields="date,portcalls,portcalls_container",
              orderByFields="date ASC", resultOffset=0, resultRecordCount=1000)
        print(f"  {pid}#{k+1}: {short(r)}")
        time.sleep(1)

print("=== F. 부산 이름으로(색인 없음 — 느릴 수 있음) 1번")
r = q("Daily_Ports_Data", where="portname='Busan' AND year=2026", returnCountOnly="true")
print("  portname='Busan':", short(r))
r = q("Daily_Ports_Data", where="year=2026 AND date>=DATE '2026-10-20'", outFields="portid,portname",
      returnDistinctValues="true", resultRecordCount=50, orderByFields="portid")
print("  10/20 이후 행이 있는 항만 예시:", short(r)[:400])
print("끝")

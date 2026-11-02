# -*- coding: utf-8 -*-
"""임시 시험 2(병합하지 않음) — 색인 있는 portid만으로 행 받기(연도는 받은 뒤 거름)가 안정적인지 · GitHub 서버에서 1회 실행."""
import json, time, requests

BASE = "https://services9.arcgis.com/weJ1QsnbMYJlCHdG/arcgis/rest/services"
S = requests.Session()
S.headers.update({"User-Agent": "sports-industry-monitor (+https://github.com/Jaemin85-Claude/sports-industry-monitor)"})
PORTS = ["port1065", "port744", "port561", "port362", "port474", "port1114", "port57", "port1188", "port2027", "port1201",
         "port824", "port1414", "port1189", "port1069", "port664", "port960", "port446"]
CHOKE = ["chokepoint6", "chokepoint4", "chokepoint1", "chokepoint7"]


def page(layer, where, fields, off, order):
    p = {"where": where, "outFields": fields, "resultOffset": off, "resultRecordCount": 1000, "f": "json"}
    if order:
        p["orderByFields"] = order
    t0 = time.monotonic()
    try:
        r = S.get(f"{BASE}/{layer}/FeatureServer/0/query", params=p, timeout=(15, 60))
        d = r.json()
    except Exception as e:
        return None, f"EXC {type(e).__name__} {str(e)[:60]}", time.monotonic() - t0
    dt = time.monotonic() - t0
    if "error" in d:
        return None, f"ERR {d['error'].get('code')} {str(d['error'].get('message'))[:40]}", dt
    return [f.get("attributes") or {} for f in d.get("features") or []], "", dt


def rows(layer, pid, fields, order):
    out, off, ts, errs = [], 0, [], []
    while True:
        fs, err, dt = page(layer, f"portid='{pid}'", fields, off, order)
        ts.append(round(dt, 1))
        if err:
            errs.append(err)
            return None, ts, errs
        out += fs
        if len(fs) < 1000 or off >= 9000:
            break
        off += 1000
        time.sleep(0.3)
    return out, ts, errs


def summ(rs):
    if rs is None:
        return "-"
    ds = sorted(str(a.get("date"))[:10] for a in rs if a.get("date"))
    y25 = [d for d in ds if d >= "2025-01-01"]
    dup = len(ds) - len(set(ds))
    return f"rows={len(rs)} {ds[0] if ds else ''}~{ds[-1] if ds else ''} 2025~={len(y25)} dup={dup}"


tot = {"ok": 0, "err": 0}
for rnd, order in ((1, "ObjectId ASC"), (2, None), (3, "ObjectId ASC")):
    print(f"=== 차례 {rnd} · 정렬 {order}")
    for pid in PORTS:
        rs, ts, errs = rows("Daily_Ports_Data", pid, "date,portcalls,portcalls_container", order)
        tot["err" if errs else "ok"] += 1
        print(f"  {pid}: {summ(rs)} · 쪽별 초 {ts} {' '.join(errs)}")
        time.sleep(0.5)
    for pid in CHOKE:
        rs, ts, errs = rows("Daily_Chokepoints_Data", pid, "date,n_total,n_container", order)
        tot["err" if errs else "ok"] += 1
        print(f"  {pid}: {summ(rs)} · 쪽별 초 {ts} {' '.join(errs)}")
        time.sleep(0.5)
print("합계", tot)
print("=== 비교: 지금 코드 질의(year>=2025 + date 정렬) 5곳 1번씩")
for pid in ("port744", "port1114", "port1069", "port1414", "port561"):
    p = {"where": f"portid='{pid}' AND year>=2025", "outFields": "date,portcalls", "orderByFields": "date ASC",
         "resultOffset": 0, "resultRecordCount": 1000, "f": "json"}
    t0 = time.monotonic()
    d = S.get(f"{BASE}/Daily_Ports_Data/FeatureServer/0/query", params=p, timeout=(15, 60)).json()
    print(f"  {pid}: {'ERR ' + str(d['error'].get('code')) if 'error' in d else 'rows=' + str(len(d.get('features') or []))} ({time.monotonic() - t0:.1f}s)")
    time.sleep(0.5)
print("끝")

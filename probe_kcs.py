# 임시 시험(병합하지 않음) — 공공데이터포털 새 화면(KRDS)의 파일 내려받기 함수 fn_fileDataDown이 부르는 주소 찾기
import re, json, requests
import logistics_fetch as lf

S = requests.Session()
S.headers.update(lf.UA)
B = "https://www.data.go.kr"
try:
    print("GitHub 서버:", requests.get("https://api.ipify.org", timeout=8).text[:7], flush=True)
except Exception as e:
    print("IP 확인 실패", type(e).__name__, flush=True)

ds = "15116807"
try:
    r = S.get(lf.KCS_PAGE.format(ds), timeout=(10, 40))
except Exception as e:
    print("화면 ERR", type(e).__name__, str(e)[:150]); raise SystemExit
t = r.text
print("화면", r.status_code, len(t), flush=True)
calls = re.findall(r"fn_fileDataDown\(([^)]*)\)", t)
print("호출:", calls[:3], flush=True)
srcs = re.findall(r'<script[^>]+src="([^"]+)"', t)
print("스크립트", len(srcs), [s for s in srcs if "/biz/" in s][:40], flush=True)
for name in ("fn_fileDataDown", "fileDetailObj"):
    for m in re.finditer(name, t):
        i = m.start()
        print(f"화면 안 '{name}' 근처:", re.sub(r"\s+", " ", t[max(0, i-200):i+600])[:800], flush=True)
        break
found = False
for s in srcs:
    if not s.startswith("/js/"):
        continue
    try:
        js = S.get(B + s.split("?")[0], timeout=(10, 30)).text
    except Exception as e:
        print("JS ERR", s, type(e).__name__); continue
    if "fn_fileDataDown" in js:
        i = js.find("fn_fileDataDown")
        print(f"[JS {s}] {len(js)}자 — fn_fileDataDown 정의 근처:", flush=True)
        print(js[max(0, i-300):i+3500], flush=True)
        for u in sorted(set(re.findall(r"[\"'](/[\w/]+\.do)[\"']", js))):
            print("  .do 주소:", u, flush=True)
        found = True
if not found:
    # 인라인 스크립트에 있을 수도
    for blk in re.findall(r"(?is)<script(?![^>]*src)[^>]*>(.*?)</script>", t):
        if "fileDataDown" in blk or "fileDetailObj" in blk:
            print("[인라인 스크립트]", re.sub(r"\s+", " ", blk)[:3500], flush=True)
# 예전 포털 방식 주소 시험(있으면 내려받기 번호를 JSON으로 줌)
if calls:
    a = [x.strip().strip("'\"") for x in calls[0].split(",")]
    for path in ("/tcs/dss/selectFileDataDownload.do",):
        for meth in ("GET", "POST"):
            try:
                p = {"publicDataPk": a[0], "publicDataDetailPk": a[1], "fileDetailSn": a[3] if len(a) > 3 else "1"}
                rr = S.request(meth, B + path, params=p if meth == "GET" else None, data=p if meth == "POST" else None, timeout=(10, 30))
                print(f"[{meth} {path}] HTTP {rr.status_code} · {rr.headers.get('content-type')} · {rr.text[:600]}", flush=True)
            except Exception as e:
                print(f"[{meth} {path}] ERR", type(e).__name__, str(e)[:150], flush=True)
print("끝", flush=True)

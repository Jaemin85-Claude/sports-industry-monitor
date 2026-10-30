# 임시 시험(병합하지 않음) — 관세청 운송비용 파일 화면(공공데이터포털)이 GitHub 서버에서 어떻게 보이는지
import re, json, requests
import logistics_fetch as lf

S = requests.Session()
S.headers.update(lf.UA)

def show(tag, url, **kw):
    try:
        r = S.get(url, timeout=(10, 40), allow_redirects=True, **kw)
    except Exception as e:
        print(tag, "ERR", type(e).__name__, str(e)[:200], flush=True); return None
    t = r.text
    print(f"{tag} HTTP {r.status_code} · 최종 {r.url[:120]} · {len(t)}자 · type {r.headers.get('content-type')}", flush=True)
    print(f"{tag} 넘겨짐: {[ (h.status_code, h.headers.get('location','')[:100]) for h in r.history]}", flush=True)
    print(f"{tag} title: {lf.clean((re.search(r'(?is)<title>(.*?)</title>', t) or [None,''])[1])[:150]}", flush=True)
    for name, rx in (("FILE_", r"FILE_\w{0,30}"), ("atchFileId", r"atchFileId[\"'=:\s]+[\w-]{0,40}"),
                     ("fileDownload", r"fileDownload[^\"'<>\s]{0,120}"), ("onclick down", r"onclick=\"[^\"]*[Dd]own[^\"]{0,120}\""),
                     ("fileDetailSn", r"fileDetailSn[\"'=:\s]+\w{0,10}"), ("csv", r"[\w가-힣_.-]{0,60}\.csv"),
                     ("수정일", r"수정일.{0,160}"), ("차기", r"차기 등록 예정일.{0,160}"), ("publicDataDetailPk", r"publicDataDetailPk[\"'=:\s]+[\w-]{0,40}"),
                     ("uddi", r"uddi:[\w-]{10,}"), ("dataSetId", r"(?:dataSetId|publicDataPk)[\"'=:\s]+[\w-]{0,30}")):
        ms = re.findall(rx, t, re.S)
        u = []
        for m in ms:
            m = re.sub(r"\s+", " ", m)
            if m not in u: u.append(m)
        print(f"{tag}   {name}: {len(ms)}건 {json.dumps(u[:6], ensure_ascii=False)[:600]}", flush=True)
    return r

for ds in ("15116806", "15116850", "15116807"):
    r = show(f"[{ds} 화면]", lf.KCS_PAGE.format(ds))
    if r is not None and "FILE_" not in r.text:
        body = lf.clean(re.sub(r"(?is)<(script|style)\b.*?</\1>", " ", r.text))
        print(f"[{ds} 화면] 본문 앞 1200자: {body[:1200]}", flush=True)
        # 내려받기 단추 근처
        for k in ("다운로드", "내려받기", "바로가기", "fileDown"):
            i = r.text.find(k)
            if i >= 0:
                near = re.sub(r"\s+", " ", r.text[max(0, i-500):i+300])
                print(f"[{ds} 화면] '{k}' 근처: {near}", flush=True)
    show(f"[{ds} 목록 JSON]", f"https://www.data.go.kr/catalog/{ds}/fileData.json")
print("끝", flush=True)

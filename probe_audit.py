# 임시 시험(병합 안 함 · PR 전에 지움): 정가 정확도 표본 검사 시험(대표 결정 11/23 '1 추천안대로') — 저장된 국내 정가가 공식몰 페이지에 보이는 가격인지
import collections, hashlib, json, re, time
import price_fetch as pf
def main():
    d = json.load(open("docs/prices.json", encoding="utf-8"))
    groups = collections.defaultdict(list)
    for it in d["items"]:
        o = (it.get("m") or {}).get("KR")
        if not o or not o.get("p") or o.get("paused") or o.get("stale_since") or o.get("cur") != "KRW":
            continue
        groups[(it.get("kind") or "rep", it["brand"])].append((it, o))
    sample = []
    for k, v in sorted(groups.items()):
        v.sort(key=lambda x: hashlib.sha1(x[0]["id"].encode()).hexdigest())
        sample += [(k, it, o) for it, o in v[:3]]
    res = collections.Counter(); byb = collections.defaultdict(collections.Counter); miss = []
    t0 = time.time()
    for k, it, o in sample:
        url = o.get("url") or ""
        if not url or "api.nike.com" in url:
            url = f"https://www.nike.com/kr/t/x/{it['code']}" if it["brand"] == "나이키" else ""
        if not url:
            res["주소 없음"] += 1; continue
        try:
            r = pf.get(url); t = r.text
        except Exception as e:
            res["못 받음"] += 1; byb[k]["못 받음"] += 1; miss.append((it["id"], o["p"], "못 받음 " + str(e)[:60])); continue
        p = int(round(o["p"])); s1 = f"{p:,}"; s2 = str(p)
        vis = s1 in t
        anyp = vis or re.search(rf"[\"':\s]{s2}(?:\.0+)?[\"',\s}}]", t) is not None
        code = str(it["code"]).split("-")[0].lower() in t.lower()
        if vis:
            res["일치(보이는 가격)"] += 1; byb[k]["일치"] += 1
        elif anyp:
            res["일치(화면 데이터)"] += 1; byb[k]["일치"] += 1
        else:
            near = re.findall(r"([0-9]{1,3}(?:,[0-9]{3})+)\s*원", t)[:6]
            res["불일치"] += 1; byb[k]["불일치"] += 1; miss.append((it["id"], o["p"], f"페이지 가격 {near} · 품번 {'있음' if code else '없음'} · {url[:70]}"))
    n = len(sample); ok = res["일치(보이는 가격)"] + res["일치(화면 데이터)"]
    print(f"표본 {n}개 · {dict(res)} · 일치 {ok}/{n - res['주소 없음'] - res['못 받음']} · {time.time() - t0:.0f}초")
    for k in sorted(byb): print("  ", k, dict(byb[k]))
    for m in miss: print("  확인:", m)
if __name__ == "__main__":
    main()

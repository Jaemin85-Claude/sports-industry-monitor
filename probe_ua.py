# 임시 시험(병합 안 함 · PR 전에 지움) 2차: 새 robots.txt 규칙(* + 옛 이름 + 새 이름 모두 지킴)이 지금 받는 상품 주소를 하나도 새로 막지 않는지 · 아디다스 IR robots.txt 다시
import re, time, urllib.parse, requests
import price_fetch as pf
def old_style(txt):   # v1.30까지: 우리 이름(sports-industry-monitor) 그룹이 있으면 그것만, 없으면 *
    pf.BOT = pf.OLD_BOT
    try:
        sets = pf._robots_rules(txt)
        return sets[1] if len(sets) > 1 else sets[0]
    finally: pf.BOT = "market-monitor"
def allowed(sets, path):
    for rs in sets:
        hit = [(n, a) for a, rx, n in rs if rx.match(path)]
        if hit and not max(hit)[1]: return False
    return True
def main():
    urls = {}
    for it in pf.PRODUCTS:
        for cc, u in (it.get("urls") or {}).items():
            if cc in pf.PAUSED_CC or not isinstance(u, str): continue
            p = urllib.parse.urlsplit(u)
            if p.netloc in pf.PAUSED: continue
            base = f"{p.scheme}://{p.netloc}"
            base = pf.ROBOTS_ALT.get(p.netloc, base)
            urls.setdefault(base, []).append(urllib.parse.unquote(p.path or "/") + ("?" + urllib.parse.unquote(p.query) if p.query else ""))
    n_url = changed = 0; fails = []
    for base in sorted(urls):
        try:
            r = requests.get(base + "/robots.txt", headers=pf.HDR, timeout=30)
        except requests.RequestException as e:
            fails.append(f"{base} {type(e).__name__}"); continue
        txt = r.content.decode("utf-8", "replace") if r.status_code == 200 else ""
        new_sets, old = pf._robots_rules(txt), old_style(txt)
        for path in urls[base]:
            n_url += 1
            a_new, a_old = allowed(new_sets, path), allowed([old], path)
            if a_new != a_old:
                changed += 1; print(f"  달라짐: {base}{path[:80]} 옛 {a_old} → 새 {a_new}")
        time.sleep(1)
    print(f"상품 주소 {n_url}개(사이트 {len(urls)}곳) — 새 규칙으로 허용이 달라진 주소 {changed}개 · robots.txt 못 받음 {len(fails)}곳 {fails}")
    for k in range(3):
        try:
            r = requests.get("https://www.adidas-group.com/robots.txt", headers={"User-Agent": "market-monitor"}, timeout=40)
            sets = pf._robots_rules(r.content.decode("utf-8", "replace")) if r.status_code == 200 else [[]]
            path = urllib.parse.urlsplit("https://www.adidas-group.com/en/investors/financial-reports").path
            print(f"아디다스 IR robots.txt: HTTP {r.status_code} · 새 이름으로 IR 목록 주소 {'허용' if allowed(sets, path) else '막음'} · 우리 이름 그룹 {'있음' if len(sets) > 1 else '없음'}")
            break
        except requests.RequestException as e:
            print(f"아디다스 IR robots.txt {k + 1}번째: {type(e).__name__}"); time.sleep(10)


if __name__ == "__main__":
    main()

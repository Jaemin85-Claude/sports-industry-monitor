# 임시 시험(병합 안 함 · PR 전에 지움): 봇 이름 바꾸기 전 확인 — robots.txt에 옛 이름·새 이름 그룹이 있는지, IR·뉴스 RSS가 새 이름으로 받아지는지
import time, urllib.parse, requests
import price_fetch as pf
OLD, NEW = "sports-industry-monitor", pf.BOT
hosts = set()
def add(u):
    p = urllib.parse.urlsplit(u)
    if p.scheme and p.netloc: hosts.add(f"{p.scheme}://{p.netloc}")
for it in pf.PRODUCTS:
    for cc, u in (it.get("urls") or {}).items():
        if cc in pf.PAUSED_CC or not isinstance(u, str): continue
        if urllib.parse.urlsplit(u).netloc in pf.PAUSED: continue
        add(u)
for h in pf.CROCS_HOST.values(): add("https://" + h)
for u in pf.KEEN_SHOP.values(): add(u)
for u in ("https://www.on.com", "https://www.nike.com", "https://www.adidas-group.com", "https://about.puma.com", "https://corp.asics.com", "https://news.google.com"):
    add(u)
for h in list(hosts):
    if urllib.parse.urlsplit(h).netloc in pf.ROBOTS_ALT: hosts.discard(h); add(pf.ROBOTS_ALT[urllib.parse.urlsplit(h).netloc])
def rules(txt, bot):
    pf.BOT = bot
    try: return [(a, rx.pattern) for a, rx, n in pf._robots_rules(txt)]
    finally: pf.BOT = NEW
named_old, named_new, diff, fail, ok = [], [], [], [], 0
for h in sorted(hosts):
    try:
        r = requests.get(h + "/robots.txt", headers=pf.HDR, timeout=20)
    except requests.RequestException as e:
        fail.append(f"{h} {type(e).__name__}"); continue
    if r.status_code != 200:
        fail.append(f"{h} HTTP {r.status_code}"); time.sleep(1); continue
    ok += 1
    txt = r.content.decode("utf-8", "replace")
    uas = {l.split(":", 1)[1].strip().lower() for l in txt.splitlines() if l.split("#")[0].strip().lower().startswith("user-agent:")}
    if any("sports" in u or "industry" in u for u in uas): named_old.append(f"{h} {sorted(u for u in uas if 'sports' in u or 'industry' in u)}")
    if any("market" in u or "monitor" in u for u in uas): named_new.append(f"{h} {sorted(u for u in uas if 'market' in u or 'monitor' in u)}")
    if rules(txt, OLD) != rules(txt, NEW): diff.append(h)
    time.sleep(1)
print(f"robots.txt 확인: 사이트 {len(hosts)}곳 · 받음 {ok} · 못 받음 {len(fail)}")
print("옛 이름(sports·industry) 그룹:", named_old or "없음")
print("새 이름(market·monitor) 그룹:", named_new or "없음")
print("옛 이름·새 이름 규칙이 다른 사이트:", diff or "없음")
for f in fail: print("  못 받음:", f)
import ir_fetch
for u in (ir_fetch.ADI_FIN, ir_fetch.PUMA_NEWS, ir_fetch.ASICS_DATA, ir_fetch.ASICS_SUMMARY):
    try:
        t = ir_fetch.fetch(u); print(f"IR {urllib.parse.urlsplit(u).netloc}: 받음 {len(t):,}자 · 봇 확인 화면 {'예' if pf.CHALLENGE.search(t[:30000]) else '아님'}")
    except Exception as e:
        print(f"IR {urllib.parse.urlsplit(u).netloc}: 실패 {type(e).__name__}: {str(e)[:120]}")
    time.sleep(2)
import news_monitor
got = news_monitor.fetch_rss("나이키", days=3)
print(f"뉴스 RSS(새 이름): {'실패' if got is None else f'{len(got)}건'} · UA {news_monitor.UA['User-Agent']}")
print("price UA:", pf.UA, "· IR UA:", ir_fetch.UA["User-Agent"])

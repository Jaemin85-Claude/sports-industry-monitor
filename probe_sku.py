# -*- coding: utf-8 -*-
# 임시 시험(병합하지 않음) — 11/10 대표 '추천 순서대로': ① 푸마 일본 403 ② 온러닝 한국·일본 가격 정보 없음 ③ 관세청 운송비용 화면 FILE_ 번호
# 우리 봇 이름 그대로 · robots.txt 확인 · 차단 우회 없음(사이트당 요청 몇 번만)
import gzip, html, json, re, sys, time, urllib.parse
import requests
import price_fetch as pf
import logistics_fetch as lf
def out(k, **kw): print(k, json.dumps(kw, ensure_ascii=False)[:4000], flush=True)
def body(r):
    c = r.content
    if c[:2] == b"\x1f\x8b":
        try: c = gzip.decompress(c)
        except Exception: pass
    return c.decode("utf-8", "replace")
CHAL = [("cf", r"cf-chl|challenge-platform|Just a moment|cf-ray"), ("akamai", r"Access Denied|errors\.edgesuite|_abck|bm-verify|Reference&#32;&#35;"),
        ("px", r"px-captcha|perimeterx|_pxAppId"), ("datadome", r"datadome|captcha-delivery"), ("captcha", r"captcha|robot"), ("incap", r"_Incapsula_Resource|incap_ses")]
KEEP = ("server", "content-type", "location", "x-cache", "cf-ray", "x-akamai-transformed", "akamai-grn", "x-served-by", "via", "x-amz-cf-id", "retry-after", "x-datadome", "x-iinfo")
def raw(url, redir=False):
    ok, why = pf.robots_ok(url)
    if not ok:
        out("ROBOTS_NO", url=url[:120], why=why); return None
    try:
        r = requests.get(url, headers=pf.HDR, timeout=(10, 25), allow_redirects=redir)
    except Exception as e:
        out("RAWERR", url=url[:120], err=repr(e)[:200]); return None
    t = body(r)
    out("RAW", url=url[:120], final=r.url[:140], st=r.status_code, hist=[h.status_code for h in r.history], len=len(t),
        hdr={k: v[:120] for k, v in r.headers.items() if k.lower() in KEEP}, cookies=sorted(r.cookies.keys())[:12],
        chal=[k for k, rx in CHAL if re.search(rx, t, re.I)], title=(re.search(r"(?is)<title>(.*?)</title>", t) or [None, ""])[1][:120].strip(),
        head=re.sub(r"\s+", " ", re.sub(r"(?is)<script.*?</script>|<style.*?</style>", " ", t))[:500] if r.status_code >= 400 else "")
    return r, t
lf.RUNNER = lf.runner_where(); out("RUNNER", where=lf.RUNNER)
P = {p["id"]: p for p in pf.PRODUCTS}
def one(pid, cc):
    try:
        v = pf.fetch_one(P[pid], cc); out("FETCH_OK", id=pid, cc=cc, v=str(v)[:300])
    except Exception as e:
        out("FETCH_ERR", id=pid, cc=cc, err=f"{type(e).__name__}: {e}"[:300])

# ① 푸마 일본
out("SEC", s="puma-jp")
raw("https://jp.puma.com/robots.txt"); time.sleep(3)
raw("https://jp.puma.com/jp/ja", redir=True); time.sleep(3)
raw(P["puma-speedcat"]["urls"]["JP"]); time.sleep(3)
raw(P["puma-speedcat"]["urls"]["KR"])   # 비교(되는 몰)
time.sleep(3); one("puma-dne4", "JP")

# ② 온러닝
out("SEC", s="on")
for pid, cc in (("on-cloudmonster", "KR"), ("on-cloudnova2", "KR"), ("on-cloudnova2", "JP"), ("on-cloud6", "KR"), ("on-cloudmonster", "US")):
    time.sleep(2); one(pid, cc)
for pid, cc in (("on-cloudmonster", "KR"), ("on-cloudnova2", "KR"), ("on-cloudnova2", "JP"), ("on-cloud6", "KR")):
    time.sleep(2)
    got = raw(P[pid]["urls"][cc], redir=True)
    if not got: continue
    r, t = got; code = P[pid]["code"]
    ld = re.findall(r'(?is)<script[^>]+application/ld\+json[^>]*>(.*?)</script>', t)
    out("ON_PAGE", id=pid, cc=cc, final=r.url[:140], ld_n=len(ld), ld_types=[(re.findall(r'"@type"\s*:\s*"(\w+)"', x) or ["?"])[:4] for x in ld][:6],
        code_n=t.count(code), next_data="__NEXT_DATA__" in t, soldout=bool(re.search(r"sold out|품절|販売終了|在庫切れ|no longer available|판매 종료", t, re.I)),
        prices=re.findall(r'"(?:price|amount|centAmount|value)"\s*:\s*"?[\d.]+', t)[:8],
        canon=(re.search(r'<link[^>]+rel="canonical"[^>]+href="([^"]+)"', t) or [None, ""])[1][:140],
        links=sorted(set(re.findall(r'/products/[a-z0-9\-]+/mens/[a-z0-9\-]+-' + re.escape(code.split(".")[0] if "." in code else code[:7]) + r'[\w.]*', t)))[:8])

# ③ 관세청 운송비용 화면
out("SEC", s="kcs")
out("TCP", ok=lf.tcp_ok("www.data.go.kr"))
for ds in ("15116806", "15116807"):
    try:
        r = lf.http(lf.KCS_PAGE.format(ds), tries=1); t = r.text
    except Exception as e:
        out("KCS_ERR", ds=ds, err=f"{type(e).__name__}: {e}"[:300]); continue
    out("KCS_PAGE", ds=ds, st=r.status_code, final=r.url[:140], len=len(t), title=(re.search(r"(?is)<title>(.*?)</title>", t) or [None, ""])[1][:160].strip(),
        file_ids=sorted(set(re.findall(r"FILE_\d{6,}", t)))[:6], meta=lf.kcs_page_meta(t))
    for kw in ("다운로드", "fileDown", "Down(", "down(", "atchFileId", "publicDataDetailPk", "uddi:", "활용신청", "로그인", "fileDetailSn", "selectFileDataDownload", "data-"):
        idx = [m.start() for m in re.finditer(re.escape(kw), t)][:4]
        for i in idx:
            out("KCS_SNIP", ds=ds, kw=kw, s=re.sub(r"\s+", " ", t[max(0, i - 160): i + 240]))
    out("KCS_ONCLICK", ds=ds, v=sorted(set(re.findall(r'onclick="([^"]{0,200})"', t)))[:30])
    out("KCS_SCRIPTS", ds=ds, v=sorted(set(re.findall(r'<script[^>]+src="([^"]+)"', t)))[:30])
    time.sleep(2)
out("DONE")

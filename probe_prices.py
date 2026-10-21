# -*- coding: utf-8 -*-
# 임시 시험(병합하지 않음)
# 나라별 브랜드 대표상품 소비자가격 — GitHub 서버에서 실제로 받아지는지 1회 확인(접속 차단·robots.txt·가격 표기 방식)
# 봇 차단은 우회하지 않는다: 정직한 User-Agent 하나로 한 번씩만 요청하고, 막히면 막힌 대로 기록한다.
import json, re, sys, time, urllib.parse, urllib.robotparser, requests

UA = "Mozilla/5.0 (compatible; sports-industry-monitor price probe; +https://github.com/Jaemin85-Claude/sports-industry-monitor)"
H = {"User-Agent": UA, "Accept": "text/html,application/json;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.8,ko;q=0.6"}
GUARD = {"akamai": ["_abck", "bm_sz", "ak_bmsc", "akamai"], "cloudflare": ["__cf_bm", "cf-ray", "cf_clearance", "cloudflare"],
         "datadome": ["datadome"], "perimeterx": ["_px", "perimeterx", "px-captcha"], "kasada": ["x-kpsdk"], "imperva": ["incap_ses", "visid_incap", "x-iinfo"]}
ROBOTS = {}

def robots_ok(url):
    p = urllib.parse.urlsplit(url); base = f"{p.scheme}://{p.netloc}"
    if base not in ROBOTS:
        rp = urllib.robotparser.RobotFileParser()
        try:
            r = requests.get(base + "/robots.txt", headers=H, timeout=15)
            rp.parse(r.text.splitlines() if r.status_code == 200 else [])
            ROBOTS[base] = (rp, r.status_code)
        except Exception as e:
            ROBOTS[base] = (None, type(e).__name__)
    rp, st = ROBOTS[base]
    return (rp.can_fetch(UA, url) if rp else None), st

def guard_of(r):
    blob = (" ".join(f"{k}:{v}" for k, v in r.headers.items()) + " " + " ".join(r.cookies.keys())).lower()
    return ",".join(g for g, keys in GUARD.items() if any(k in blob for k in keys)) or "-"

def jsonld_prices(html):
    out = []
    for m in re.finditer(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', html, re.S | re.I):
        try: data = json.loads(m.group(1).strip())
        except Exception: continue
        stack = data if isinstance(data, list) else [data]
        while stack:
            x = stack.pop()
            if isinstance(x, dict):
                if "@graph" in x: stack.extend(x["@graph"] if isinstance(x["@graph"], list) else [x["@graph"]])
                if str(x.get("@type", "")).lower() in ("product", "productgroup"):
                    offs = x.get("offers") or x.get("hasVariant") or []
                    offs = offs if isinstance(offs, list) else [offs]
                    for o in offs:
                        if isinstance(o, dict) and "offers" in o: o = o["offers"] if isinstance(o["offers"], dict) else (o["offers"] or [{}])[0]
                        if isinstance(o, dict):
                            pr = o.get("price") or o.get("lowPrice")
                            if pr is not None: out.append(f"{pr} {o.get('priceCurrency', '')}".strip())
                stack.extend(v for v in x.values() if isinstance(v, (dict, list)))
            elif isinstance(x, list): stack.extend(x)
    return out[:4]

def meta_prices(html):
    v = re.findall(r'<meta[^>]+(?:property|name|itemprop)=["\'](?:product:price:amount|og:price:amount|price)["\'][^>]+content=["\']([^"\']+)', html, re.I)
    c = re.findall(r'<meta[^>]+(?:property|name|itemprop)=["\'](?:product:price:currency|og:price:currency|priceCurrency)["\'][^>]+content=["\']([^"\']+)', html, re.I)
    return [f"{a} {c[0] if c else ''}".strip() for a in v[:3]]

def json_get(data, path):
    for part in [p for p in re.split(r"\.|\[(\d+)\]", path or "") if p]:
        if isinstance(data, list) and part.isdigit(): data = data[int(part)] if int(part) < len(data) else None
        elif isinstance(data, dict): data = data.get(part)
        else: return None
    return data

def probe(t):
    url = t["url"]; row = {"id": t["id"], "brand": t["brand"], "cc": t["country"]}
    ok, rst = robots_ok(url); row["robots"] = {True: "허용", False: "금지", None: f"모름({rst})"}[ok] if ok is not None else f"모름({rst})"
    if ok is False:   # robots.txt가 막은 주소는 요청하지 않음
        row["status"] = "건너뜀(robots)"; return row
    try:
        r = requests.get(url, headers=H, timeout=25, allow_redirects=True)
    except Exception as e:
        row["status"] = type(e).__name__; return row
    row.update(status=r.status_code, size=len(r.content), guard=guard_of(r), final=urllib.parse.urlsplit(r.url).netloc + urllib.parse.urlsplit(r.url).path[:60])
    body = r.text
    row["list_hint"] = [k for k in ("compare_at_price", "fullPrice", "listPrice", "originalPrice", "regularPrice", "basePrice", "strikethrough", "price-standard", "정가", "소비자가") if k in body][:5]
    if t["parse"] == "json":
        try: row["price"] = json_get(r.json(), t.get("json_path", ""))
        except Exception: row["price"] = "JSON 아님"
    elif t["parse"] in ("jsonld", "html-meta"):
        row["price"] = jsonld_prices(body) or meta_prices(body) or None
        row["captcha"] = bool(re.search(r"captcha|are you a robot|access denied|blocked|px-captcha|cf-chl", body[:20000], re.I))
    return row

if __name__ == "__main__":
    targets = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "probe_targets.json"))
    rows = []
    for t in targets:
        rows.append(probe(t)); print(json.dumps(rows[-1], ensure_ascii=False), flush=True)
        time.sleep(2)
    good = [r for r in rows if r.get("price")]
    print(f"\n요약: {len(rows)}곳 중 가격 읽힘 {len(good)} · 403/429 {sum(1 for r in rows if r.get('status') in (403, 429))} · robots 금지 {sum(1 for r in rows if r.get('status') == '건너뜀(robots)')}")

# -*- coding: utf-8 -*-
"""
sports-industry-monitor — Phase 7-A/B: 유럽·일본 브랜드 IR 지역·채널 분해 (v1.1)
v1.1: 아식스(7936.T) 추가 — 재무자료 페이지의 최신 결산단신 영문판(Consolidated Financial
      Statements … Japan GAAP) 세그먼트 표를 Claude 추출. 일본 결산단신은 누적 기준(Q2=1~6월)이라
      기간을 '6M 2026 (누적)'으로 표기. 한국은 별도 세그먼트가 아니라 'Others(South America, Korea)'에 포함
EDGAR 미대상인 아디다스(ADS.DE)·푸마(PUM.DE)의 지역·채널 매출을 IR 자료에서 추출한다.
  - 아디다스: 재무자료 페이지의 최신 Fact Sheet PDF → "Financial Highlights by Segment"·
    "Channels at a Glance" 표를 정규식으로 파싱 (Claude 불필요, 프로브 2026-09-29로 형식 확인)
  - 푸마: 투자자 뉴스의 최신 실적 보도자료(HTML) → Claude 추출 (지역·채널 금액과 전년 금액)
출력: docs/segments_ir.json — SEC 추출(segments.json)과 같은 스키마(schema_v 2)라
      build_dashboard가 병합해 기존 지역/채널 카드에 그대로 표시
캐시: 같은 자료 URL이면 재추출하지 않음
§29-D: 자료에 명시된 값만, 미기재는 null
"""

import os
import io
import re
import json
import datetime
import requests

ANTHROPIC_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
KST = datetime.timezone(datetime.timedelta(hours=9))
OUT_PATH = "docs/segments_ir.json"
UA = {"User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                     "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"),
      "Accept-Language": "en-US,en;q=0.9"}

ADI_FIN = "https://www.adidas-group.com/en/investors/financial-reports"
PUMA_NEWS = "https://about.puma.com/en/investor-relations/financial-news"
ASICS_DATA = "https://corp.asics.com/en/investor_relations/library/financial_data"
ASICS_REGIONS = ["Japan", "North America", "Europe", "Greater China", "Oceania",
                 "Southeast and South Asia", "Others (South America, Korea, etc.)"]

ADI_REGIONS = ["Europe", "North America", "Greater China", "Emerging Markets",
               "Latin America", "Japan/South Korea"]
ADI_CHANNELS = ["Wholesale", "Direct-to-Consumer (DTC)"]


def log(m):
    print(m, flush=True)


# ── Anthropic 호출 공통: 인증/크레딧 오류는 즉시 실패(워크플로우 빨간 X) ──
def anthropic_post(payload, timeout=180):
    resp = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={"x-api-key": ANTHROPIC_KEY, "anthropic-version": "2023-06-01",
                 "content-type": "application/json"},
        json=payload, timeout=timeout)
    if resp.status_code in (401, 403) or (resp.status_code == 400 and "credit" in resp.text.lower()):
        log(f"[FATAL] Anthropic API {resp.status_code}: {resp.text[:300]}")
        log("[FATAL] 키 만료/무효 또는 크레딧 소진 — console.anthropic.com 확인 후 "
            "GitHub Secret ANTHROPIC_API_KEY 갱신")
        raise SystemExit(2)
    if resp.status_code != 200:
        raise RuntimeError(f"Anthropic {resp.status_code}: {resp.text[:200]}")
    return resp.json()


def fetch(url, as_bytes=False, timeout=90):
    r = requests.get(url, headers=UA, timeout=timeout, allow_redirects=True)
    r.raise_for_status()
    return r.content if as_bytes else r.text


def links(html, base):
    out = []
    for m in re.finditer(r'href="([^"]+)"', html):
        u = m.group(1)
        if u.startswith("//"):
            u = "https:" + u
        elif u.startswith("/"):
            u = base + u
        elif not u.startswith("http"):
            u = base + "/" + u.lstrip("./")
        out.append(u)
    return list(dict.fromkeys(out))


def strip_html(html):
    html = re.sub(r"<script.*?</script>|<style.*?</style>", " ", html, flags=re.S | re.I)
    txt = re.sub(r"<[^>]+>", " ", html)
    txt = re.sub(r"&nbsp;|&#160;", " ", txt).replace("&amp;", "&")
    return re.sub(r"\s+", " ", txt)


def to_num(tok):
    tok = tok.replace(",", "")
    try:
        return float(tok)
    except ValueError:
        return None


# ══════════════════════════ 아디다스 ══════════════════════════
def adidas_latest_fact_sheet():
    html = fetch(ADI_FIN)
    pdfs = [u for u in links(html, "https://www.adidas-group.com")
            if u.lower().endswith(".pdf") and re.search(r"fact.?sheet", u, re.I) and re.search(r"_EN|EN_", u)]
    best, best_key = None, (0, 0)
    for u in pdfs:
        name = u.rsplit("/", 1)[-1]
        y = re.search(r"(20\d\d)", name)
        q = re.search(r"[Qq]([1-4])", name)
        if not y:
            continue
        key = (int(y.group(1)), int(q.group(1)) if q else 4)
        if key > best_key:
            best, best_key = u, key
    return best, best_key


def parse_quarter_series(tokens):
    """'Net sales' 뒤 토큰열에서 분기별 (당기, 전기) 추출.
    보고된 분기 = 숫자 숫자 %-토큰 %-토큰 / 미보고 분기 = — 숫자.  반환 [(cur|None, prior|None), ...]"""
    out, i = [], 0
    while i < len(tokens) and len(out) < 4:
        t = tokens[i]
        if t in ("—", "–", "-"):
            prior = to_num(tokens[i + 1]) if i + 1 < len(tokens) else None
            out.append((None, prior)); i += 2
            continue
        cur = to_num(t)
        if cur is None:
            break
        prior = to_num(tokens[i + 1]) if i + 1 < len(tokens) else None
        j = i + 2
        while j < len(tokens) and (tokens[j].endswith("%") or tokens[j].endswith("pp") or tokens[j] in ("—", "–")) and j < i + 4:
            j += 1
        out.append((cur, prior)); i = j
    return out


def adidas_extract(text, year, quarter):
    """Fact Sheet 텍스트 → regions/channels (해당 분기 열)"""
    text = re.sub(r"\s+", " ", text)

    def grab(label, next_labels):
        # label 뒤 'Net sales' 다음부터 다음 라벨(Gross profit 등) 전까지 토큰
        m = re.search(re.escape(label) + r"\s+Net sales\s+(.*?)\s+(?:" + "|".join(map(re.escape, next_labels)) + r")", text)
        if not m:
            return None
        return parse_quarter_series(m.group(1).split())

    regions, channels = [], []
    for r in ADI_REGIONS:
        ser = grab(r, ["Gross profit"])
        if not ser or quarter - 1 >= len(ser):
            regions.append({"name": r, "revenue": None, "prev_revenue": None, "yoy_pct": None}); continue
        cur, prior = ser[quarter - 1]
        regions.append({"name": r, "revenue": cur, "prev_revenue": prior,
                        "yoy_pct": ((cur / prior - 1) * 100) if (cur and prior) else None})
    # 채널: 'Wholesale 4,084 3,999 2% 8% — 3,604 — ...' (Net sales 라벨 없음)
    m = re.search(r"Channels at a Glance.*?Wholesale\s+(.*?)\s+Direct-to-Consumer \(DTC\)\s+(.*?)\s+Own retail", text)
    if m:
        for name, seg in (("Wholesale", m.group(1)), ("Direct-to-Consumer (DTC)", m.group(2))):
            ser = parse_quarter_series(seg.split())
            cur, prior = ser[quarter - 1] if quarter - 1 < len(ser) else (None, None)
            channels.append({"name": name, "revenue": cur, "prev_revenue": prior,
                             "yoy_pct": ((cur / prior - 1) * 100) if (cur and prior) else None})
    return {"schema_v": 2, "period": f"Q{quarter} {year}", "prev_period": f"Q{quarter} {year - 1}",
            "currency": "EUR", "unit": "millions", "regions": regions, "channels": channels,
            "sub_segments": [], "notes": "adidas Fact Sheet — Financial Highlights by Segment / Channels at a Glance"}


def run_adidas(cached):
    url, (y, q) = adidas_latest_fact_sheet()
    if not url:
        log("[ADS.DE] Fact Sheet 링크 미발견"); return None
    log(f"[ADS.DE] 최신 Fact Sheet Q{q} {y}: {url}")
    if cached and cached.get("url") == url and cached.get("extract"):
        log("  캐시 사용"); return cached
    from pypdf import PdfReader
    raw = fetch(url, as_bytes=True, timeout=120)
    pages = [(p.extract_text() or "") for p in PdfReader(io.BytesIO(raw)).pages]
    ex = adidas_extract(" ".join(pages), y, q)
    for r in ex["regions"]:
        log(f"  {r['name']}: {r['revenue']} / 전년 {r['prev_revenue']} ({r['yoy_pct'] and round(r['yoy_pct'],1)}%)")
    for c in ex["channels"]:
        log(f"  {c['name']}: {c['revenue']} / 전년 {c['prev_revenue']}")
    ok = sum(1 for r in ex["regions"] if r["revenue"] is not None)
    return {"accession": url.rsplit("/", 1)[-1], "source": "IR Fact Sheet (PDF)", "url": url,
            "error": None if ok else "지역 표 파싱 실패", "extract": ex if ok else None,
            "fetched_at": datetime.datetime.now(KST).strftime("%Y-%m-%d")}


# ══════════════════════════ 푸마 ══════════════════════════
def puma_latest_release():
    html = fetch(PUMA_NEWS)
    cands = [u for u in links(html, "https://about.puma.com")
             if "/newsroom/corporate-news/" in u and re.search(r"q[1-4]|quarter|half|result|year|outlook|sales|start", u, re.I)]
    # URL 앞의 dd-mm-yyyy 로 최신 선택
    def key(u):
        m = re.search(r"/(\d{2})-(\d{2})-(\d{4})-", u)
        return (int(m.group(3)), int(m.group(2)), int(m.group(1))) if m else (0, 0, 0)
    cands.sort(key=key, reverse=True)
    return (cands[0], key(cands[0])) if cands else (None, None)


def puma_period(d):
    y, mth, _ = d
    q = 1 if mth <= 5 else 2 if mth <= 8 else 3 if mth <= 11 else 4
    # 2월 말 발표는 전년 4분기·연간
    if mth <= 3:
        return f"Q4 {y - 1}", f"Q4 {y - 2}"
    return f"Q{q} {y}", f"Q{q} {y - 1}"


def claude_extract_puma(text, period, prev_period):
    prompt = f"""You are extracting figures from a PUMA quarterly results press release.
Target period: {period} (prior-year comparison: {prev_period}). Use QUARTERLY figures for the
quarter, not half-year or nine-month cumulative figures.

Extract net sales in € millions as explicitly stated:
- regions: EMEA, Americas, Asia/Pacific (and Greater China / North America / Latin America if a
  € amount is explicitly stated for the quarter)
- channels: Wholesale, Direct-to-Consumer (DTC)
For each, give the current-quarter € amount ("revenue"), the prior-year quarter € amount
("prev_revenue", usually in parentheses like "(Q2 2025: € 771.7 million)"), and the reported
currency-adjusted growth % if stated ("yoy_pct"). If an amount is not explicitly stated, use null.
Do not compute amounts from percentages.

Respond with ONLY JSON, no markdown fences:
{{
  "schema_v": 2, "period": "{period}", "prev_period": "{prev_period}", "currency": "EUR", "unit": "millions",
  "regions": [{{"name": "EMEA", "revenue": number|null, "prev_revenue": number|null, "yoy_pct": number|null}}],
  "channels": [{{"name": "Wholesale", "revenue": number|null, "prev_revenue": number|null, "yoy_pct": number|null}}],
  "sub_segments": [], "notes": "one line on basis (currency-adjusted vs reported) or null"
}}

PRESS RELEASE:
{text[:60000]}"""
    data = anthropic_post({"model": "claude-sonnet-4-6", "max_tokens": 1200,
                           "messages": [{"role": "user", "content": prompt}]})
    txt = "".join(p.get("text", "") for p in data.get("content", []) if p.get("type") == "text")
    return json.loads(re.sub(r"```json|```", "", txt).strip())


def run_puma(cached):
    url, d = puma_latest_release()
    if not url:
        log("[PUM.DE] 실적 보도자료 미발견"); return None
    period, prev = puma_period(d)
    log(f"[PUM.DE] 최신 보도자료 {period}: {url}")
    if cached and cached.get("url") == url and cached.get("extract"):
        log("  캐시 사용"); return cached
    if not ANTHROPIC_KEY:
        log("  [WARN] ANTHROPIC_API_KEY 미설정 → 추출 생략"); return cached
    text = strip_html(fetch(url))
    ex = claude_extract_puma(text, period, prev)
    ex.setdefault("schema_v", 2); ex.setdefault("sub_segments", [])
    for r in ex.get("regions", []):
        log(f"  {r.get('name')}: {r.get('revenue')} / 전년 {r.get('prev_revenue')} ({r.get('yoy_pct')}%)")
    for c in ex.get("channels", []):
        log(f"  {c.get('name')}: {c.get('revenue')} / 전년 {c.get('prev_revenue')}")
    ok = any(r.get("revenue") is not None for r in ex.get("regions", []))
    return {"accession": url.rsplit("/", 1)[-1], "source": "IR 보도자료 (HTML)", "url": url,
            "error": None if ok else "지역 금액 미추출", "extract": ex if ok else None,
            "fetched_at": datetime.datetime.now(KST).strftime("%Y-%m-%d")}


# ══════════════════════════ 아식스 ══════════════════════════
def asics_latest_statements():
    """재무자료 페이지에서 최신 결산단신 영문판(Japan GAAP) 선택 → (url, period, prev_period)"""
    html = fetch(ASICS_DATA)
    best, best_key, best_lbl = None, (0, 0), None
    for m in re.finditer(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', html, re.S):
        u, title = m.group(1), re.sub(r"<[^>]+>|\s+", " ", m.group(2)).strip()
        if u.startswith("//"):
            u = "https:" + u
        if not u.lower().endswith(".pdf") or "assets.asics.com" not in u:
            continue
        name = u.rsplit("/", 1)[-1]
        text = (title + " " + name).replace("%20", " ")
        if not re.search(r"Consolidated Financial Statements|Summary of Consolidated Financial Statements", text, re.I):
            continue
        y = re.search(r"(20\d\d)", text)
        if not y:
            continue
        year = int(y.group(1))
        if re.search(r"First Quarter|Three Months", text, re.I):
            q, lbl = 1, ("3M", "1~3월 누적")
        elif re.search(r"Second Quarter|Six Months", text, re.I):
            q, lbl = 2, ("6M", "1~6월 누적")
        elif re.search(r"Third Quarter|Nine Months", text, re.I):
            q, lbl = 3, ("9M", "1~9월 누적")
        elif re.search(r"Fiscal Year", text, re.I):
            q, lbl = 4, ("FY", "연간")
        else:
            continue
        key = (year, q)
        if key > best_key:
            best, best_key, best_lbl = u, key, lbl
    if not best:
        return None, None, None
    year, q = best_key
    period = f"{best_lbl[0]} {year} ({best_lbl[1]})"
    prev = f"{best_lbl[0]} {year - 1}"
    return best, period, prev


def asics_segment_text(pages):
    """세그먼트 표 부근만 잘라 Claude에 전달 (전체 결산단신은 길어서)"""
    full = re.sub(r"\s+", " ", " ".join(pages))
    idxs = [m.start() for m in re.finditer(r"[Ss]egment", full)]
    if not idxs:
        return full[:40000]
    windows, last_end = [], -1
    for i in idxs:
        s, e = max(0, i - 1500), min(len(full), i + 6000)
        if s < last_end:
            continue
        windows.append(full[s:e]); last_end = e
    return " … ".join(windows)[:60000]


def claude_extract_asics(text, period, prev_period):
    prompt = f"""You are extracting segment figures from an ASICS Corporation consolidated financial
statements summary (Japan GAAP, English). Target period: {period} — a CUMULATIVE year-to-date
period; the prior-year comparison is the same cumulative period {prev_period}.

From the reportable segment information table, extract "Net sales" (sales to external customers
if both are shown) for each segment: Japan, North America, Europe, Greater China, Oceania,
Southeast and South Asia, and Others. Give the current period amount ("revenue") and the same
period prior year ("prev_revenue") in millions of yen (convert if the table is in thousands or
billions). Use ONLY figures explicitly stated. If the table shows only the current period, set
prev_revenue to null. Do not include inter-segment eliminations or the consolidated total.

Respond with ONLY JSON, no markdown fences:
{{
  "schema_v": 2, "period": "{period}", "prev_period": "{prev_period}", "currency": "JPY", "unit": "millions",
  "regions": [{{"name": "Japan", "revenue": number|null, "prev_revenue": number|null, "yoy_pct": number|null}}],
  "channels": [], "sub_segments": [],
  "notes": "state whether figures are external sales or total incl. inter-segment, and the unit shown"
}}

DOCUMENT EXCERPTS:
{text}"""
    data = anthropic_post({"model": "claude-sonnet-4-6", "max_tokens": 1200,
                           "messages": [{"role": "user", "content": prompt}]})
    txt = "".join(p.get("text", "") for p in data.get("content", []) if p.get("type") == "text")
    ex = json.loads(re.sub(r"```json|```", "", txt).strip())
    for r in ex.get("regions", []):
        if r.get("yoy_pct") is None and r.get("revenue") and r.get("prev_revenue"):
            r["yoy_pct"] = (r["revenue"] / r["prev_revenue"] - 1) * 100
        if re.match(r"other", (r.get("name") or ""), re.I):
            r["name"] = "Others (South America, Korea, etc.)"
    return ex


def run_asics(cached):
    url, period, prev = asics_latest_statements()
    if not url:
        log("[7936.T] 결산단신 링크 미발견"); return None
    log(f"[7936.T] 최신 결산단신 {period}: {url}")
    if cached and cached.get("url") == url and cached.get("extract"):
        log("  캐시 사용"); return cached
    if not ANTHROPIC_KEY:
        log("  [WARN] ANTHROPIC_API_KEY 미설정 → 추출 생략"); return cached
    from pypdf import PdfReader
    raw = fetch(url, as_bytes=True, timeout=120)
    pages = [(p.extract_text() or "") for p in PdfReader(io.BytesIO(raw)).pages]
    ex = claude_extract_asics(asics_segment_text(pages), period, prev)
    ex.setdefault("schema_v", 2); ex.setdefault("channels", []); ex.setdefault("sub_segments", [])
    ex["notes"] = (ex.get("notes") or "") + " · 누적 기준(Japan GAAP 결산단신) · 한국은 Others에 포함"
    for r in ex.get("regions", []):
        log(f"  {r.get('name')}: {r.get('revenue')} / 전년 {r.get('prev_revenue')} ({r.get('yoy_pct') and round(r['yoy_pct'],1)}%)")
    ok = any(r.get("revenue") is not None for r in ex.get("regions", []))
    return {"accession": url.rsplit("/", 1)[-1][:80], "source": "IR 결산단신 (PDF)", "url": url,
            "error": None if ok else "세그먼트 표 미추출", "extract": ex if ok else None,
            "fetched_at": datetime.datetime.now(KST).strftime("%Y-%m-%d")}


def main():
    old = {}
    if os.path.exists(OUT_PATH):
        try:
            with open(OUT_PATH, encoding="utf-8") as f:
                old = json.load(f)
        except Exception:
            pass
    items = dict(old.get("items", {}))
    for tk, fn in (("ADS.DE", run_adidas), ("PUM.DE", run_puma), ("7936.T", run_asics)):
        try:
            res = fn(items.get(tk))
            if res:
                items[tk] = res
        except SystemExit:
            raise
        except Exception as e:
            log(f"[{tk}] 실패: {str(e)[:200]}")
            if tk in items:
                log("  이전 결과 유지")
    out = {"generated_at": datetime.datetime.now(KST).strftime("%Y-%m-%d %H:%M KST"), "items": items}
    os.makedirs("docs", exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    log(f"saved {OUT_PATH} — {sum(1 for v in items.values() if v.get('extract'))}/3 추출")


if __name__ == "__main__":
    main()

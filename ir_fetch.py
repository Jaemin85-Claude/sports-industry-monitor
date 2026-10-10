# -*- coding: utf-8 -*-
"""
sports-industry-monitor — Phase 7-A/B: 유럽·일본 브랜드 IR 지역·채널 분해 (v1.2)
v1.3: (대표 지시 2026-10-10) 푸마 보도자료에서 본사 발언(재고·할인·유통 통제 문장 원문 최대 3개, mgmt_notes) 추출 —
      원문에 글자 그대로 있는 문장만 남김. IR_VER=3으로 1회 재추출. 시험용 IR_ONLY(쉼표 구분 티커) — 저장 안 함
v1.2: 환율 효과를 뺀 성장률(cn_yoy_pct) 추가 — 아디다스 Fact Sheet 'Change (c.n.)' 열, 푸마 '(ca)',
      아식스 실적 설명자료(결산단신 엔화 성장률과 ±1.5%p 이내로 일치하는 쌍만 채택).
      yoy_pct는 보고 통화 기준으로 통일(푸마 기존 값은 (ca)였음). 괄호 음수 '(0%)' 파싱 보강. IR_VER=2로 1회 재추출
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
IR_VER = 3   # 추출 스키마 버전 — 바뀌면 같은 자료라도 1회 재추출 (v1.3 푸마 mgmt_notes)
UA = {"User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                     "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"),
      "Accept-Language": "en-US,en;q=0.9"}

ADI_FIN = "https://www.adidas-group.com/en/investors/financial-reports"
PUMA_NEWS = "https://about.puma.com/en/investor-relations/financial-news"
ASICS_DATA = "https://corp.asics.com/en/investor_relations/library/financial_data"
ASICS_SUMMARY = "https://corp.asics.com/en/investor_relations/library/financial_summary"
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


def cache_ok(cached, url):
    return bool(cached and cached.get("url") == url and cached.get("extract")
                and cached.get("ir_ver") == IR_VER)


PCT_RE = re.compile(r"^(\()?([+-]?\d[\d.,]*)(%|pp)(\))?$")


def is_pct(tok):
    return bool(PCT_RE.match(tok))


def pct_val(tok):
    """'5%'→5, '(3%)'→-3, '(0%)'→-0.0, 'pp' 단위는 None"""
    m = PCT_RE.match(tok)
    if not m or m.group(3) != "%":
        return None
    try:
        v = float(m.group(2).replace(",", ""))
    except ValueError:
        return None
    return -abs(v) if m.group(1) else v


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
    """'Net sales' 뒤 토큰열 → 분기별 (당기, 전기, 보고 증감%, 환율중립 증감%).
    보고된 분기 = 숫자 숫자 [% [%]] / 미보고 분기 = — 숫자.  괄호 음수 '(3%)' 처리."""
    out, i = [], 0
    while i < len(tokens) and len(out) < 4:
        t = tokens[i]
        if t in ("—", "–", "-"):
            prior = to_num(tokens[i + 1]) if i + 1 < len(tokens) else None
            out.append((None, prior, None, None)); i += 2
            continue
        cur = to_num(t)
        if cur is None:
            break
        prior = to_num(tokens[i + 1]) if i + 1 < len(tokens) else None
        j, pcts = i + 2, []
        while j < len(tokens) and len(pcts) < 2 and (is_pct(tokens[j]) or tokens[j].lower() in ("n.a.", "n/a")):
            pcts.append(pct_val(tokens[j])); j += 1
        out.append((cur, prior, pcts[0] if pcts else None, pcts[1] if len(pcts) > 1 else None))
        i = j
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
            regions.append({"name": r, "revenue": None, "prev_revenue": None, "yoy_pct": None, "cn_yoy_pct": None}); continue
        cur, prior, rep, cn = ser[quarter - 1]
        regions.append({"name": r, "revenue": cur, "prev_revenue": prior,
                        "yoy_pct": ((cur / prior - 1) * 100) if (cur and prior) else rep,
                        "cn_yoy_pct": cn})
    # 채널: 'Wholesale 4,084 3,999 2% 8% — 3,604 — ...' (Net sales 라벨 없음)
    m = re.search(r"Channels at a Glance.*?Wholesale\s+(.*?)\s+Direct-to-Consumer \(DTC\)\s+(.*?)\s+Own retail", text)
    if m:
        for name, seg in (("Wholesale", m.group(1)), ("Direct-to-Consumer (DTC)", m.group(2))):
            ser = parse_quarter_series(seg.split())
            cur, prior, rep, cn = ser[quarter - 1] if quarter - 1 < len(ser) else (None, None, None, None)
            channels.append({"name": name, "revenue": cur, "prev_revenue": prior,
                             "yoy_pct": ((cur / prior - 1) * 100) if (cur and prior) else rep,
                             "cn_yoy_pct": cn})
    return {"schema_v": 2, "period": f"Q{quarter} {year}", "prev_period": f"Q{quarter} {year - 1}",
            "currency": "EUR", "unit": "millions", "regions": regions, "channels": channels,
            "sub_segments": [], "notes": "adidas Fact Sheet — Financial Highlights by Segment / Channels at a Glance"}


def run_adidas(cached):
    url, (y, q) = adidas_latest_fact_sheet()
    if not url:
        log("[ADS.DE] Fact Sheet 링크 미발견"); return None
    log(f"[ADS.DE] 최신 Fact Sheet Q{q} {y}: {url}")
    if cache_ok(cached, url):
        log("  캐시 사용"); return cached
    from pypdf import PdfReader
    raw = fetch(url, as_bytes=True, timeout=120)
    pages = [(p.extract_text() or "") for p in PdfReader(io.BytesIO(raw)).pages]
    ex = adidas_extract(" ".join(pages), y, q)
    for r in ex["regions"]:
        log(f"  {r['name']}: {r['revenue']} / 전년 {r['prev_revenue']} ({r['yoy_pct'] and round(r['yoy_pct'],1)}%) · 환율 제외 {r['cn_yoy_pct']}%")
    for c in ex["channels"]:
        log(f"  {c['name']}: {c['revenue']} / 전년 {c['prev_revenue']} · 환율 제외 {c['cn_yoy_pct']}%")
    ok = sum(1 for r in ex["regions"] if r["revenue"] is not None)
    return {"accession": url.rsplit("/", 1)[-1], "source": "IR Fact Sheet (PDF)", "url": url,
            "error": None if ok else "지역 표 파싱 실패", "extract": ex if ok else None,
            "fetched_at": datetime.datetime.now(KST).strftime("%Y-%m-%d"), "ir_ver": IR_VER}


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
- regions: EMEA, Americas, Asia/Pacific (and Greater China / North America / Latin America — include
  them even if only a growth % is stated, with revenue null)
- channels: Wholesale, Direct-to-Consumer (DTC)
For each give:
  "revenue": current-quarter € amount; "prev_revenue": prior-year quarter € amount (usually in
  parentheses like "(Q2 2025: € 771.7 million)");
  "yoy_pct": the change in EURO terms if explicitly stated (e.g. "12.6% in euro"), else null;
  "cn_yoy_pct": the currency-adjusted change marked "(ca)", else null.
Decreases as negative numbers. If a figure is not explicitly stated, use null. Do not compute
amounts from percentages.

Respond with ONLY JSON, no markdown fences:
{{
  "schema_v": 2, "period": "{period}", "prev_period": "{prev_period}", "currency": "EUR", "unit": "millions",
  "regions": [{{"name": "EMEA", "revenue": number|null, "prev_revenue": number|null, "yoy_pct": number|null, "cn_yoy_pct": number|null}}],
  "channels": [{{"name": "Wholesale", "revenue": number|null, "prev_revenue": number|null, "yoy_pct": number|null, "cn_yoy_pct": number|null}}],
  "sub_segments": [], "notes": "one line on basis (currency-adjusted vs reported) or null",
  "mgmt_notes": [{{"topic": "inventory|discount|channel", "quote": "one sentence copied VERBATIM", "ko": "한국어 한 줄 요약(60자 이내)"}}]
}}
mgmt_notes: up to 3 sentences in which the company states an ACTION, PLAN, REASON or OUTLOOK about:
  "inventory" - clearing / liquidating / cleaning up / right-sizing inventory, inventory being elevated
                or "clean", tighter inventory management;
  "discount"  - promotions, markdowns, discounting, promotional environment, pricing actions
                (including margin impact explicitly attributed to promotions or markdowns);
  "channel"   - reducing or exiting wholesale accounts or doors, off-price / liquidation channel sales,
                limiting or tightening supply to the marketplace, distribution strategy changes.
EXCLUDE sentences that only report a figure or a change (e.g. "Inventories were $389 million",
"Wholesale revenues decreased 7.2%") unless the same sentence gives one of the reasons above.
EXCLUDE margin statements whose stated cause is not promotions/markdowns (e.g. logistics, freight, FX).
Copy each quote EXACTLY as written (same words and punctuation, no ellipsis, no paraphrase).
If no sentence qualifies, use an empty list - that is a valid and useful answer.

PRESS RELEASE:
{text[:60000]}"""
    data = anthropic_post({"model": "claude-sonnet-4-6", "max_tokens": 1800,
                           "messages": [{"role": "user", "content": prompt}]})
    txt = "".join(p.get("text", "") for p in data.get("content", []) if p.get("type") == "text")
    ex = json.loads(re.sub(r"```json|```", "", txt).strip())
    ex["mgmt_notes"] = verify_quotes(ex.get("mgmt_notes"), text[:60000])
    return ex


def _norm_q(s):
    """원문 대조용: 따옴표·대시·공백·대소문자 차이를 없앰"""
    s = str(s or "").replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", '"').replace("\u201d", '"')
    s = s.replace("\u2013", "-").replace("\u2014", "-").replace("\xa0", " ")
    return re.sub(r"\s+", " ", s).strip().lower()


def verify_quotes(notes, doc_text):
    """v1.3 본사 발언 — 원문에 글자 그대로 있는 문장만, 최대 3개(extract_segments v11과 같은 규칙)"""
    if not isinstance(notes, list):
        return []
    body, out, dropped = _norm_q(doc_text), [], 0
    for n in notes:
        if not isinstance(n, dict):
            continue
        q, topic = str(n.get("quote") or "").strip(), n.get("topic")
        if topic not in ("inventory", "discount", "channel") or len(q) < 30 or _norm_q(q) not in body:
            dropped += 1
            continue
        out.append({"topic": topic, "quote": q[:400], "ko": str(n.get("ko") or "").strip()[:80]})
        if len(out) == 3:
            break
    log(f"  본사 발언 {len(out)}건" + (f"(원문에 없는 문장 {dropped}건 버림)" if dropped else ""))
    return out


def run_puma(cached):
    url, d = puma_latest_release()
    if not url:
        log("[PUM.DE] 실적 보도자료 미발견"); return None
    period, prev = puma_period(d)
    log(f"[PUM.DE] 최신 보도자료 {period}: {url}")
    if cache_ok(cached, url):
        log("  캐시 사용"); return cached
    if not ANTHROPIC_KEY:
        log("  [WARN] ANTHROPIC_API_KEY 미설정 → 추출 생략"); return cached
    text = strip_html(fetch(url))
    ex = claude_extract_puma(text, period, prev)
    ex.setdefault("schema_v", 2); ex.setdefault("sub_segments", [])
    for r in ex.get("regions", []) + ex.get("channels", []):
        if r.get("revenue") and r.get("prev_revenue"):
            r["yoy_pct"] = (r["revenue"] / r["prev_revenue"] - 1) * 100   # 금액이 있으면 유로 기준 직접 계산
        r.setdefault("cn_yoy_pct", None)
    for r in ex.get("regions", []):
        log(f"  {r.get('name')}: {r.get('revenue')} / 전년 {r.get('prev_revenue')} (유로 {r.get('yoy_pct') and round(r['yoy_pct'],1)}%) · 환율 제외 {r.get('cn_yoy_pct')}%")
    for c in ex.get("channels", []):
        log(f"  {c.get('name')}: {c.get('revenue')} / 전년 {c.get('prev_revenue')} · 환율 제외 {c.get('cn_yoy_pct')}%")
    ok = any(r.get("revenue") is not None for r in ex.get("regions", []))
    return {"accession": url.rsplit("/", 1)[-1], "source": "IR 보도자료 (HTML)", "url": url,
            "error": None if ok else "지역 금액 미추출", "extract": ex if ok else None,
            "fetched_at": datetime.datetime.now(KST).strftime("%Y-%m-%d"), "ir_ver": IR_VER}


# ══════════════════════════ 아식스 ══════════════════════════
def _asics_classify(text):
    y = re.search(r"(20\d\d)", text)
    if not y:
        return None
    year = int(y.group(1))
    if re.search(r"First Quarter|Three Months", text, re.I):
        return year, 1, ("3M", "1~3월 누적")
    if re.search(r"Second Quarter|Six Months", text, re.I):
        return year, 2, ("6M", "1~6월 누적")
    if re.search(r"Third Quarter|Nine Months", text, re.I):
        return year, 3, ("9M", "1~9월 누적")
    if re.search(r"Fiscal Year", text, re.I):
        return year, 4, ("FY", "연간")
    return None


def _asics_anchors(html):
    for m in re.finditer(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', html, re.S):
        u, title = m.group(1), re.sub(r"<[^>]+>|\s+", " ", m.group(2)).strip()
        if u.startswith("//"):
            u = "https:" + u
        if not u.lower().split("?")[0].endswith(".pdf") or "assets.asics.com" not in u:
            continue
        yield u, (title + " " + u.rsplit("/", 1)[-1]).replace("%20", " ")


def asics_latest_statements():
    """재무자료 페이지에서 최신 결산단신 영문판(Japan GAAP) → (url, period, prev_period, (연도, 분기))"""
    best, best_key, best_lbl = None, (0, 0), None
    for u, text in _asics_anchors(fetch(ASICS_DATA)):
        if not re.search(r"Consolidated Financial Statements|Summary of Consolidated Financial Statements", text, re.I):
            continue
        k = _asics_classify(text)
        if k and (k[0], k[1]) > best_key:
            best, best_key, best_lbl = u, (k[0], k[1]), k[2]
    if not best:
        return None, None, None, None
    year, q = best_key
    return best, f"{best_lbl[0]} {year} ({best_lbl[1]})", f"{best_lbl[0]} {year - 1}", best_key


def asics_summary_pdf(key):
    """실적 설명자료(Consolidated Financial Summary) 중 같은 기간 — 스크립트 포함본 우선"""
    cands = []
    for u, text in _asics_anchors(fetch(ASICS_SUMMARY)):
        if not re.search(r"Consolidated Financial Summary", text, re.I):
            continue
        k = _asics_classify(text)
        if k and (k[0], k[1]) == tuple(key):
            cands.append((0 if re.search(r"script", text, re.I) else 1, u))
    cands.sort()
    return cands[0][1] if cands else None


def asics_region_text(pages):
    """'by region' 부근만 잘라 전달 (지역별 매출 슬라이드·스크립트)"""
    full = re.sub(r"\s+", " ", " ".join(pages))
    windows, last_end = [], -1
    for m in list(re.finditer(r"by region", full, re.I))[:6]:
        s, e = max(m.start() - 3000, last_end, 0), min(len(full), m.start() + 5000)
        if s >= e:
            continue
        windows.append(full[s:e]); last_end = e
    return " … ".join(windows)[:40000] if windows else full[:30000]


def _norm_region(n):
    n = (n or "").lower().replace("asics ", "").strip()
    return "others" if n.startswith("other") else n


def claude_asics_cn(text, period, anchors):
    anchor_txt = ", ".join(f"{n} {v:+.1f}%" for n, v in anchors)
    prompt = f"""You are reading an ASICS Corporation results presentation (Consolidated Financial Summary)
for {period} (cumulative year-to-date). The official yen-based net sales growth by region for this
period, from the financial statements, is: {anchor_txt}.

For each region find the CURRENCY-NEUTRAL net sales growth % for the same period, from the TOTAL net
sales by region (all categories combined). Ignore slides that break down a single category
(Performance Running, Core Performance Sports, SportStyle, Onitsuka Tiger, Apparel & Equipment) by
region. Growth is often shown as "+31.0% （ +15.6% ）" = yen-based ( currency-neutral ).
Return the yen-based % shown next to it ("yoy_pct") and the currency-neutral % ("cn_yoy_pct").
If currency-neutral is shown as "-" or is not applicable (e.g. domestic Japan), use null.
Only use figures explicitly shown; do not compute.

Respond with ONLY JSON, no markdown fences:
{{"regions": [{{"name": "Japan", "yoy_pct": number|null, "cn_yoy_pct": number|null}}], "notes": "slide/section used"}}

DOCUMENT EXCERPTS:
{text}"""
    data = anthropic_post({"model": "claude-sonnet-4-6", "max_tokens": 800,
                           "messages": [{"role": "user", "content": prompt}]})
    txt = "".join(p.get("text", "") for p in data.get("content", []) if p.get("type") == "text")
    return json.loads(re.sub(r"```json|```", "", txt).strip())


def attach_asics_cn(regions, cn_ex, tol=1.5):
    """결산단신 엔화 성장률과 ±tol%p 이내로 일치하는 쌍만 채택 (§29-D: 불일치는 버림)"""
    got = {_norm_region(r.get("name")): r for r in (cn_ex or {}).get("regions", [])}
    kept = 0
    for r in regions:
        g = got.get(_norm_region(r.get("name")))
        ok = (g and g.get("cn_yoy_pct") is not None and g.get("yoy_pct") is not None
              and r.get("yoy_pct") is not None and abs(g["yoy_pct"] - r["yoy_pct"]) <= tol)
        r["cn_yoy_pct"] = g["cn_yoy_pct"] if ok else None
        kept += 1 if ok else 0
        if g and not ok and g.get("cn_yoy_pct") is not None:
            log(f"    {r.get('name')}: 자료 엔화 {g.get('yoy_pct')}% ≠ 결산단신 {r.get('yoy_pct') and round(r['yoy_pct'],1)}% → 환율 제외 값 버림")
    return kept


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
    url, period, prev, key = asics_latest_statements()
    if not url:
        log("[7936.T] 결산단신 링크 미발견"); return None
    log(f"[7936.T] 최신 결산단신 {period}: {url}")
    if cache_ok(cached, url):
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
        r["cn_yoy_pct"] = None
    try:
        su = asics_summary_pdf(key)
        if su:
            log(f"  환율 제외 성장률: 실적 설명자료 {su}")
            raw2 = fetch(su, as_bytes=True, timeout=180)
            pages2 = [(p.extract_text() or "") for p in PdfReader(io.BytesIO(raw2)).pages]
            anchors = [(r["name"], r["yoy_pct"]) for r in ex.get("regions", []) if r.get("yoy_pct") is not None]
            kept = attach_asics_cn(ex.get("regions", []), claude_asics_cn(asics_region_text(pages2), period, anchors))
            log(f"    결산단신과 일치 {kept}/{len(anchors)}개 지역 채택")
        else:
            log("  실적 설명자료 미발견 — 환율 제외 생략")
    except SystemExit:
        raise
    except Exception as e:
        log(f"  환율 제외 추출 실패(지역 금액은 유지): {str(e)[:120]}")
    for r in ex.get("regions", []):
        log(f"  {r.get('name')}: {r.get('revenue')} / 전년 {r.get('prev_revenue')} (엔화 {r.get('yoy_pct') and round(r['yoy_pct'],1)}%) · 환율 제외 {r.get('cn_yoy_pct')}%")
    ok = any(r.get("revenue") is not None for r in ex.get("regions", []))
    return {"accession": url.rsplit("/", 1)[-1][:80], "source": "IR 결산단신 (PDF)", "url": url,
            "error": None if ok else "세그먼트 표 미추출", "extract": ex if ok else None,
            "fetched_at": datetime.datetime.now(KST).strftime("%Y-%m-%d"), "ir_ver": IR_VER}


def main():
    old = {}
    if os.path.exists(OUT_PATH):
        try:
            with open(OUT_PATH, encoding="utf-8") as f:
                old = json.load(f)
        except Exception:
            pass
    items = dict(old.get("items", {}))
    only = [x.strip() for x in os.environ.get("IR_ONLY", "").split(",") if x.strip()]
    if only:    # v1.3 시험 모드: 지정 종목만 캐시 무시하고 추출, 결과는 로그로만(저장 안 함)
        log(f"[시험 모드] IR_ONLY={','.join(only)} — 저장하지 않음")
        for tk, fn in (("ADS.DE", run_adidas), ("PUM.DE", run_puma), ("7936.T", run_asics)):
            if tk not in only:
                continue
            res = fn(None) or {}
            ex = res.get("extract") or {}
            log(f"[{tk}] {res.get('source')} · {ex.get('period')} · 지역 {len(ex.get('regions') or [])}")
            for n in ex.get("mgmt_notes") or []:
                log(f"    [{n['topic']}] {n['ko']} — \"{n['quote'][:200]}\"")
        return
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

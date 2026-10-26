# -*- coding: utf-8 -*-
"""
sports-industry-monitor — Phase 7-A/B: 유럽·일본 브랜드 IR 지역·채널 분해 (v1.2)
v1.6: (대표 지시 2026-10-26) ① 실패 알림 — 자료를 못 찾거나 표 해석·추출이 실패하면 이전 값을 지키고(전에는 빈 값으로 덮어씀)
      soft_fail.txt에 남김(ir.yml 'Check partial failures'가 빨간 X), 가장 최근 자료의 기간이 끝난 지 165일 넘어도 실패 표시,
      접속·Claude 일시 오류(429·5xx·연결)는 다시 시도 ② 본사 발언 빈칸 채우기 — 아디다스는 Fact Sheet과 같은 분기 폴더의
      보도자료·분기 보고서(Q2는 H1 Report), 아식스는 이미 받는 실적 설명자료(스크립트)에서 재고·할인·유통 문장(푸마와 같은 규칙).
      발언 문서 주소(notes_url)가 바뀔 때만 추출(지역 표 캐시는 그대로 — 재추출 없음) ③ 접속 이름을 브라우저 흉내 대신 우리 봇 이름
      sports-industry-monitor로(봇 차단 우회 안 함 원칙 — 세 사이트 모두 이 이름으로 받아지고 robots.txt 허용 확인)
      ④ 그 밖의 실패 표시 — 늘 나오던 지역·채널 금액·전년 금액·환율 제외 성장률이 빠짐(표 일부만 읽힘 · 나머지는 저장 · 같은 자료를 2번까지
      다시 추출 · 알림은 처음 나온 실행만, logistics odd_seen 방식), 전 분기까지 있던 발언을 새 분기에 21일 넘게 못 뽑음(사유 notes_err).
      이전 값을 지킨 종목은 failed·kept_failed·kept_reason, 그 밖의 실패 표시는 종목 warn(수집 상태 화면 '확인 필요').
      발언 문서를 못 받거나 못 읽으면 다음 후보 문서로(같은 서버 연결 오류면 다음 실행에 · 지역 표는 그대로 저장).
      시간: 다시 받기는 실행 9분까지, 발언·신호 분류는 12분까지, 새 요청은 18분까지(ir.yml 25분). 시험 모드(IR_ONLY)는 실패 표시 기록 안 함.
      같은 분기를 더 나은 문서(아식스 스크립트본 등)로 다시 뽑아 새 문장이 없으면 추출 시각·문서 날짜 그대로(주간 메일 중복 방지).
      같은 자료를 다시 추출할 때는 이미 뽑은 발언·신호·추출 시각을 그대로 옮김(carry_notes·merge_notes — 다시 분류 없음 · 푸마는
      Claude가 이번에 놓친 발언도 지키고 새 문장만 더함). 발언마다 처음 뽑힌 시각 at(weekly_digest v1.13 — 새 문장만 메일에).
      이미 이 분기 발언이 있는데 더 나은 문서(스크립트본 등)로 바꾸기만 못 하면 조용히 다음 주에.
      푸마 최신 보도자료에 지역 금액이 없으면(예비 실적·전망) 이전 값을 지키고 한 번 알린 뒤 같은 자료는 건너뜀(skipped_url).
      긴 문서는 재고·할인 낱말 묶음을 먼저, 가격·도매 낱말 묶음은 남은 자리에 6만 자 안(kw_windows) ·
      Claude 응답은 앞뒤 설명이 붙어도 JSON 부분만 읽음(json_obj)
v1.5: (대표 지시 2026-10-10, 브랜드 점검표) 본사 발언 신호 sig(more·less·neutral) — extract_segments v11.2와 같은 규칙, sig 없는 발언만 1회 분류
v1.4: (대표 지시 2026-10-10) 본사 발언 다듬기(extract_segments v11.1과 같은 규칙 — 주제 바로잡기·비슷한 문장 빼기, 캐시에도 적용),
      추출 시각 extracted_at·보도자료 날짜 doc_date(주간 메일 '이번 주 새 본사 발언'), 월별 Claude 사용량 claude_usage(수집 상태)
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
import time
import datetime
import requests

ANTHROPIC_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
KST = datetime.timezone(datetime.timedelta(hours=9))
OUT_PATH = "docs/segments_ir.json"
IR_VER = 3   # 추출 스키마 버전 — 바뀌면 같은 자료라도 1회 재추출 (v1.3 푸마 mgmt_notes)
# v1.6 우리 봇 이름으로(브라우저 흉내 안 함 — 봇 차단 우회 안 함 원칙). 2026-10-26 GitHub 서버 시험: 세 사이트 모두 200 ·
# robots.txt 허용(아디다스·푸마) / 없음(아식스 404 = 제한 없음, RFC 9309)
UA = {"User-Agent": "sports-industry-monitor", "Accept-Language": "en-US,en;q=0.9"}

ADI_FIN = "https://www.adidas-group.com/en/investors/financial-reports"
PUMA_NEWS = "https://about.puma.com/en/investor-relations/financial-news"
ASICS_DATA = "https://corp.asics.com/en/investor_relations/library/financial_data"
ASICS_SUMMARY = "https://corp.asics.com/en/investor_relations/library/financial_summary"
ASICS_REGIONS = ["Japan", "North America", "Europe", "Greater China", "Oceania",
                 "Southeast and South Asia", "Others (South America, Korea, etc.)"]

ADI_REGIONS = ["Europe", "North America", "Greater China", "Emerging Markets",
               "Latin America", "Japan/South Korea"]
ADI_CHANNELS = ["Wholesale", "Direct-to-Consumer (DTC)"]


SCRIPT = "ir_fetch"
STALE_DAYS = 165    # v1.6 가장 최근 자료의 기간이 끝난 지 이만큼 넘으면 실패 표시(분기 끝 → 다음 분기 발표는 길어야 약 140일)
RETRY_WAITS = (30, 90)   # v1.6 접속·Claude 일시 오류(429·5xx·연결) — 30초·90초 뒤 다시
RETRY_DEADLINE = 9 * 60  # v1.6 실행 9분이 지나면 다시 시도하지 않음(ir.yml 작업 25분 제한 안에 저장·커밋까지)
OPT_DEADLINE = 12 * 60   # v1.6 실행 12분이 지나면 덜 급한 요청(본사 발언 추출·신호 분류)은 다음 실행에
HARD_DEADLINE = 18 * 60  # v1.6 실행 18분이 지나면 새 요청을 시작하지 않음(요청 1건 최대 3분 → 21분 안에 저장, 작업 25분)
NOTES_LAG_DAYS = 21      # v1.6 새 분기 자료를 받은 뒤 이만큼 지나도 발언을 못 뽑으면(전 분기까지는 있었는데) 실패 표시
_T0 = time.time()
_NOW = {"tk": None, "test": False}   # v1.6 지금 처리 중인 종목(실패 표시를 그 종목 warn에 남김) · 시험 모드(IR_ONLY)
_WARN = {}                           # v1.6 {종목: [실패 표시 글]} — 저장할 때 종목의 warn(수집 상태 화면 '확인 필요')


def log(m):
    print(m, flush=True)


def soft_fail(msg):
    """v1.6 심각한 실패 표시 — 저장은 하되 워크플로우 마지막 단계가 빨간 X로 끝내 점검 알림이 가게 함.
    처리 중인 종목이 있으면 그 종목 warn에도 남김(수집 상태 화면). 시험 모드(IR_ONLY)는 로그만(저장 안 하는 실행이라 알림 안 감)"""
    if _NOW["test"]:
        print(f"실패 표시(시험 모드 — 기록 안 함): {msg}", flush=True)
        return
    print(f"실패 표시: {msg}", flush=True)
    with open("soft_fail.txt", "a", encoding="utf-8") as f:
        f.write(f"{SCRIPT}: {msg}\n")
    if _NOW["tk"]:
        _WARN.setdefault(_NOW["tk"], []).append(re.sub(r"^" + re.escape(_NOW["tk"]) + r"\s*", "", msg))


class OutOfTime(RuntimeError):
    """v1.6 실행 시간이 모자라 새 요청을 시작하지 않음"""


def _check_time():
    if time.time() - _T0 > HARD_DEADLINE:
        raise OutOfTime(f"실행 {HARD_DEADLINE // 60}분 넘어 남은 요청은 다음 실행에")


def _opt_ok(what):
    """덜 급한 요청(발언 추출·신호 분류)을 지금 해도 되는지 — 실행 12분이 지나면 다음 실행에(로그만)"""
    if time.time() - _T0 <= OPT_DEADLINE:
        return True
    log(f"  실행 시간이 길어져 {what}은 다음 실행에")
    return False


def _can_retry(wait):
    """다시 시도해도 실행 시간 안에 끝나는지 — 9분이 지나면 바로 실패로 넘김(남은 종목·저장이 작업 제한에 걸리지 않게)"""
    return wait is not None and time.time() - _T0 + wait < RETRY_DEADLINE


def _transient(e=None, status=None):
    """다시 시도할 만한 일시 오류 — 연결·시간 초과·429·5xx(529 과부하 포함). 403·404 등은 다시 해도 같음"""
    if status is not None:
        return status == 429 or status >= 500
    if isinstance(e, (requests.exceptions.ConnectionError, requests.exceptions.Timeout,
                      requests.exceptions.ChunkedEncodingError)):
        return True
    resp = getattr(e, "response", None)
    return isinstance(e, requests.exceptions.HTTPError) and resp is not None and _transient(status=resp.status_code)


def _kind(e):
    """오류 갈래만(다시 시도 줄에 오류 원문을 쓰지 않음 — 12:23 점검이 'Error:' 줄로 알리므로, 다시 해서 받으면 조용히)"""
    if isinstance(e, requests.exceptions.Timeout):
        return "시간 초과"
    resp = getattr(e, "response", None)
    if resp is not None:
        return f"HTTP {resp.status_code}"
    return "연결 안 됨"


# ── Anthropic 호출 공통: 인증/크레딧 오류는 즉시 실패(워크플로우 빨간 X) · v1.6 일시 오류는 2번 다시 ──
def anthropic_post(payload, timeout=180):
    for k, wait in enumerate(RETRY_WAITS + (None,)):
        _check_time()
        try:
            resp = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers={"x-api-key": ANTHROPIC_KEY, "anthropic-version": "2023-06-01",
                         "content-type": "application/json"},
                json=payload, timeout=timeout)
        except requests.exceptions.RequestException as e:
            if not _can_retry(wait) or not _transient(e):
                raise
            log(f"  Claude {_kind(e)} — {wait}초 뒤 다시({k + 1}/{len(RETRY_WAITS)})")
            time.sleep(wait)
            continue
        if _can_retry(wait) and _transient(status=resp.status_code):
            log(f"  Claude 응답 {resp.status_code} — {wait}초 뒤 다시({k + 1}/{len(RETRY_WAITS)})")
            time.sleep(wait)
            continue
        break
    if resp.status_code in (401, 403) or (resp.status_code == 400 and "credit" in resp.text.lower()):
        log(f"[FATAL] Anthropic API {resp.status_code}: {resp.text[:300]}")
        log("[FATAL] 키 만료/무효 또는 크레딧 소진 — console.anthropic.com 확인 후 "
            "GitHub Secret ANTHROPIC_API_KEY 갱신")
        raise SystemExit(2)
    if resp.status_code != 200:
        raise RuntimeError(f"Anthropic {resp.status_code}: {resp.text[:200]}")
    data = resp.json()
    count_usage(payload.get("model"), data)
    return data


# ── v1.4 Claude 사용량(수집 상태 '이번 달 Claude 사용액') — extract_segments v11.1과 같은 방식 ──
PRICE = {"claude-sonnet-4-6": (3.0, 15.0), "claude-haiku-4-5": (1.0, 5.0)}   # $/백만 토큰(입력, 출력), 2026-10 기준
_USAGE = {"calls": 0, "in": 0, "out": 0, "usd": 0.0}


def count_usage(model, data):
    """성공한 Claude 응답 1건의 토큰·금액을 이번 실행 합계에 더함"""
    u = (data or {}).get("usage") or {}
    tin, tout = int(u.get("input_tokens") or 0), int(u.get("output_tokens") or 0)
    pin, pout = PRICE.get(model, (3.0, 15.0))
    _USAGE["calls"] += 1
    _USAGE["in"] += tin
    _USAGE["out"] += tout
    _USAGE["usd"] += (tin * pin + tout * pout) / 1e6


def usage_months(old):
    """이전 파일의 월별 기록(claude_usage)에 이번 실행 사용량을 더함 — 최근 3개월만. since = 그 달 기록 시작일"""
    now = datetime.datetime.now(KST)
    m = now.strftime("%Y-%m")
    cu = (old or {}).get("claude_usage") if isinstance(old, dict) else None
    hist = {k: v for k, v in cu.items() if isinstance(v, dict)} if isinstance(cu, dict) else {}
    cur = dict(hist.get(m) or {"calls": 0, "in": 0, "out": 0, "usd": 0.0, "since": now.strftime("%Y-%m-%d")})
    for k in ("calls", "in", "out"):
        cur[k] = int(cur.get(k) or 0) + _USAGE[k]
    cur["usd"] = round(float(cur.get("usd") or 0) + _USAGE["usd"], 4)
    hist[m] = cur
    return {k: hist[k] for k in sorted(hist)[-3:]}


def fetch(url, as_bytes=False, timeout=90):
    for k, wait in enumerate(RETRY_WAITS + (None,)):
        _check_time()
        try:
            r = requests.get(url, headers=UA, timeout=timeout, allow_redirects=True)
            r.raise_for_status()
            return r.content if as_bytes else r.text
        except requests.exceptions.RequestException as e:   # v1.6 일시 오류만 다시(403·404는 바로 올림)
            if not _can_retry(wait) or not _transient(e):
                raise
            log(f"  접속 일시 오류({_kind(e)}) — {wait}초 뒤 다시({k + 1}/{len(RETRY_WAITS)})")
            time.sleep(wait)


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


def json_obj(txt):
    """v1.6 Claude 응답 → JSON 객체. 앞뒤에 설명·코드 울타리가 붙어도 첫 '{'부터 마지막 '}'까지로 다시 읽음
    (2026-10-26 브랜치 시험: 아식스 환율 제외 응답이 한 번 JSON으로 안 읽혀 그 분기 값이 빠질 뻔함)"""
    t = re.sub(r"```json|```", "", txt or "").strip()
    try:
        return json.loads(t)
    except ValueError:
        i, j = t.find("{"), t.rfind("}")
        if i < 0 or j <= i:
            raise
        return json.loads(t[i:j + 1])


def strip_html(html):
    html = re.sub(r"<script.*?</script>|<style.*?</style>", " ", html, flags=re.S | re.I)
    txt = re.sub(r"<[^>]+>", " ", html)
    txt = re.sub(r"&nbsp;|&#160;", " ", txt).replace("&amp;", "&")
    return re.sub(r"\s+", " ", txt)


PARTIAL_TRIES = 2   # v1.6 표 일부만 읽힌 추출은 같은 자료라도 이만큼까지 다시 추출(Claude가 한 번 놓친 값일 수 있음)


def cache_ok(cached, url):
    ok = bool(cached and cached.get("url") == url and cached.get("extract")
              and cached.get("ir_ver") == IR_VER)
    if ok and (cached.get("extract") or {}).get("cn_skipped"):
        log("  지난번 시간이 모자라 환율 제외 성장률을 건너뜀 — 같은 자료를 다시 추출")
        return False
    if ok and cached.get("partial") and int(cached.get("partial_tries") or 0) < PARTIAL_TRIES:
        log(f"  지난번 표 일부만 읽힘({' · '.join(cached['partial'])}) — 같은 자료를 다시 추출"
            f"({int(cached.get('partial_tries') or 0) + 1}/{PARTIAL_TRIES})")
        return False
    return ok


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
    _ADI["html"] = html     # v1.6 같은 분기 폴더의 발언 문서 찾기에 다시 씀
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


_ADI = {"html": ""}
# v1.6 발언 문서 고르는 순서(파일 이름) — 보도자료 > 분기 보고서 > 반기·연차 보고서(Q2 = H1_Report) > 실적 자료(…_Results_…) > 통화 녹취.
# 발표 자료·Fact Sheet·보충 자료(Financial_supplement·Alternative_Performance_Measures — 이름에 위 낱말이 없어 빠짐)는 뺌
ADI_NOTE_RANK = ((r"press|release", 0), (r"quarterly.?statement|statement", 1),
                 (r"half.?year|interim|annual.?report|report", 2), (r"results", 3), (r"transcript|call", 4))


def _cld_date(u):
    """cloudinary 주소의 올린 시각(v + 10자리 초) → KST 날짜 — 발표일에 가까움(주간 메일 '이번 주 새 본사 발언' 문서 날짜)"""
    m = re.search(r"/v(1\d{9})/", u or "")
    return datetime.datetime.fromtimestamp(int(m.group(1)), KST).strftime("%Y-%m-%d") if m else None


def adidas_notes_docs(fs_url):
    """v1.6 Fact Sheet과 같은 분기 폴더(…/2026/Q2/EN/)의 PDF 중 발언 문서 후보 — 고르는 순서대로(없으면 [])"""
    m = re.search(r"/upload/(?:v\d+/)?(.+/)[^/]+$", fs_url or "")
    if not m:
        return []
    folder = m.group(1)
    same = [u for u in links(_ADI["html"], "https://www.adidas-group.com")
            if folder in u and u.lower().endswith(".pdf") and u != fs_url]
    log("  같은 분기 자료: " + (", ".join(u.rsplit("/", 1)[-1][:50] for u in same) or "없음"))
    ranked = []
    for u in same:
        name = u.rsplit("/", 1)[-1]
        if re.search(r"fact.?sheet|presentation|slides", name, re.I):
            continue
        rk = next((r for pat, r in ADI_NOTE_RANK if re.search(pat, name, re.I)), None)
        if rk is not None:
            ranked.append((rk, u))
    return [u for _, u in sorted(ranked, key=lambda t: t[0])]


def adidas_notes(res, y, q):
    """v1.6 아디다스 본사 발언 — 고르는 순서대로 시도(받기·읽기가 안 되는 문서는 다음 후보로). 발언 문서 주소가
    그대로면(notes_url) 다시 안 뽑음. 어떤 경우에도 예외를 올리지 않음 — 지역 표(새 분기)는 그대로 저장되게"""
    docs = adidas_notes_docs(res.get("url"))
    if not docs:
        log("  본사 발언 문서 없음(보도자료·분기 보고서 PDF가 같은 분기 폴더에 없음) — 발언 없이")
        return
    if not ANTHROPIC_KEY:
        log("  [WARN] ANTHROPIC_API_KEY 미설정 → 발언 추출 생략"); return
    from pypdf import PdfReader
    miss = []
    for i, doc in enumerate(docs):
        if res.get("notes_url") == doc:
            log(f"  본사 발언 문서: {doc.rsplit('/', 1)[-1][:60]} — 발언 캐시 사용"); return
        if not _opt_ok("아디다스 본사 발언"):
            return
        try:
            raw = fetch(doc, as_bytes=True, timeout=120)
            text = kw_windows(" ".join((p.extract_text() or "") for p in PdfReader(io.BytesIO(raw)).pages))
        except SystemExit:
            raise
        except Exception as e:
            net = isinstance(e, requests.exceptions.RequestException)
            miss.append(f"{doc.rsplit('/', 1)[-1][:40]}({_kind(e) if net else ('시간 부족' if isinstance(e, OutOfTime) else 'PDF 읽기 안 됨')})")
            if isinstance(e, OutOfTime) or (net and _transient(e)):
                if res.get("notes_url") in docs[i + 1:]:     # 이 분기 발언은 뒤 순서 문서에서 이미 뽑아 둠 — 그대로(조용히)
                    log(f"  본사 발언: 앞 순서 문서 일시 오류({miss[-1]}) — 이미 뽑아 둔 발언 그대로"); return
                break       # 같은 서버(cloudinary)가 연결·시간 초과면 다른 후보도 같음 — 다음 실행에
            continue
        if len(text) < 500:
            miss.append(f"{doc.rsplit('/', 1)[-1][:40]}(글 없음)")
            continue
        log(f"  본사 발언 문서: {doc}" + (f" (앞 순서 못 받음: {', '.join(miss)})" if miss else ""))
        attach_notes(res, doc, text, "adidas", f"Q{q} {y}", "results document (press release or quarterly statement)",
                     doc_date=_cld_date(doc))
        return
    if res.get("notes_url") and (res.get("extract") or {}).get("mgmt_notes") is not None:
        # 이 분기 발언은 이미 있음 — 더 나은 문서로 바꾸기만 못 함: 조용히 다음 주에 다시
        log(f"  본사 발언: 다른 문서는 다음 실행에 다시({', '.join(miss)[:120]}) — 이미 뽑아 둔 발언 그대로"); return
    res["notes_err"] = "문서 받기 안 됨"
    soft_fail(f"ADS.DE 본사 발언 문서를 못 받음: {', '.join(miss)[:160]} — "
              + ("이전 발언 유지" if (res.get("extract") or {}).get("mgmt_notes") else "이번 분기 발언은 아직 없음")
              + ", 다음 실행에서 다시")


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
        log("  캐시 사용")
        adidas_notes(cached, y, q)      # v1.6 지역 표는 캐시, 발언은 문서가 바뀌었거나 아직 없을 때만
        return cached
    from pypdf import PdfReader
    raw = fetch(url, as_bytes=True, timeout=120)
    pages = [(p.extract_text() or "") for p in PdfReader(io.BytesIO(raw)).pages]
    ex = adidas_extract(" ".join(pages), y, q)
    for r in ex["regions"]:
        log(f"  {r['name']}: {r['revenue']} / 전년 {r['prev_revenue']} ({r['yoy_pct'] and round(r['yoy_pct'],1)}%) · 환율 제외 {r['cn_yoy_pct']}%")
    for c in ex["channels"]:
        log(f"  {c['name']}: {c['revenue']} / 전년 {c['prev_revenue']} · 환율 제외 {c['cn_yoy_pct']}%")
    ok = sum(1 for r in ex["regions"] if r["revenue"] is not None)
    res = {"accession": url.rsplit("/", 1)[-1], "source": "IR Fact Sheet (PDF)", "url": url,
           "error": None if ok else "지역 표 파싱 실패", "extract": ex if ok else None,
           "fetched_at": datetime.datetime.now(KST).strftime("%Y-%m-%d"), "ir_ver": IR_VER}
    if ok:
        carry_notes(res, cached)    # 같은 자료 다시 추출(표 일부만 읽힘)이면 이미 뽑은 발언 그대로
        adidas_notes(res, y, q)
    return res


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


# v1.6 본사 발언 고르는 규칙 — 푸마(지역 추출과 함께)·아디다스·아식스(발언만) 같은 글(v1.3 푸마 프롬프트 그대로)
MGMT_RULES = """mgmt_notes: up to 3 sentences in which the company states an ACTION, PLAN, REASON or OUTLOOK about:
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
If no sentence qualifies, use an empty list - that is a valid and useful answer."""


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
{MGMT_RULES}

PRESS RELEASE:
{text[:60000]}"""
    data = anthropic_post({"model": "claude-sonnet-4-6", "max_tokens": 1800,
                           "messages": [{"role": "user", "content": prompt}]})
    txt = "".join(p.get("text", "") for p in data.get("content", []) if p.get("type") == "text")
    ex = json_obj(txt)
    ex["extracted_at"] = datetime.datetime.now(KST).strftime("%Y-%m-%d %H:%M")   # v1.4 주간 메일 '이번 주 새 본사 발언'
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
    out = tidy_notes(out)[:3]      # v1.4 주제 바로잡기·비슷한 문장 빼기 뒤 최대 3개
    log(f"  본사 발언 {len(out)}건" + (f"(원문에 없는 문장 {dropped}건 버림)" if dropped else ""))
    return out


NOTE_KW = re.compile(r"inventor|promot|markdown|discount|pric(?:e|ing)|wholesale|off-price|"
                     r"distribut|marketplace|sell-in|clearance|liquidat|stock level", re.I)
# 재고·할인 쪽 낱말 — 이 낱말 묶음을 먼저 남김(긴 보고서에 흔한 가격·도매·유통 낱말(주가 share price 등) 묶음보다)
NOTE_STRONG = re.compile(r"inventor|promot|markdown|discount|off-price|clearance|liquidat|stock level", re.I)
SPAN_MAX = 6000     # 이어 붙인 묶음 하나의 최대 길이 — 낱말이 3천 자 안쪽으로 이어지는 긴 문서가 한 묶음이 되어 앞부분만 남지 않게


def kw_windows(text, limit=60000, half=1500):
    """v1.6 발언 찾기용 — 문서가 길면 낱말 앞뒤 1,500자 묶음만(겹치면 이어 붙이되 6천 자까지), 짧으면 통째로.
    ① 재고·할인 낱말(NOTE_STRONG) 묶음을 먼저(그 낱말끼리만 이어 붙여 — 가격·도매 글에 자리를 뺏기지 않게) ② 남은 자리에
    가격·도매·유통 낱말 묶음. 같은 단계 안에서는 촘촘한 순, 넘치는 묶음은 첫 낱말을 가운데에 두고 잘라 문서 순서로 이음(이음표까지 limit 안).
    낱말이 하나도 없으면 앞 6만 자"""
    text = re.sub(r"\s+", " ", text or "")
    if len(text) <= limit:
        return text
    SEP = " … "

    def spans_of(pat):      # [시작, 끝, 낱말 수, 첫 낱말 위치]
        out = []
        for m in pat.finditer(text):
            s, e = max(0, m.start() - half), min(len(text), m.end() + half)
            if out and s <= out[-1][1] and e - out[-1][0] <= SPAN_MAX:
                out[-1][1] = e
                out[-1][2] += 1
            else:
                out.append([s, e, 1, m.start()])
        return out

    def union(iv):      # 겹치거나 맞닿은 묶음은 하나로(같은 글이 두 번 나오지 않게)
        out = []
        for s, e in sorted(iv):
            if out and s <= out[-1][1]:
                out[-1][1] = max(out[-1][1], e)
            else:
                out.append([s, e])
        return out

    def size(iv):       # 이었을 때 글자 수(이음표 포함)
        return sum(e - s for s, e in iv) + len(SEP) * max(0, len(iv) - 1)

    take = []
    for group in (spans_of(NOTE_STRONG), spans_of(NOTE_KW)):
        for s, e, k, p in sorted(group, key=lambda t: (-t[2] / max(1, t[1] - t[0]), t[0])):
            if limit - size(union(take)) < half:
                break
            if size(union(take + [(s, e)])) > limit:      # 넘치면 첫 낱말을 가운데에 두고 남은 만큼만
                lo, hi = 0, e - s
                win = lambda L: (max(s, min(p - L // 2, e - L)), max(s, min(p - L // 2, e - L)) + L)
                while hi - lo > 1:
                    mid = (lo + hi) // 2
                    if size(union(take + [win(mid)])) <= limit:
                        lo = mid
                    else:
                        hi = mid
                if lo < half:
                    continue
                s, e = win(lo)
            take.append((s, e))
    if not take:        # 재고·할인·가격·도매 낱말이 하나도 없음(글자 사이가 띄워진 PDF 등) — 앞부분이라도
        return text[:limit]
    return SEP.join(text[s:e] for s, e in union(take))


def claude_mgmt_notes(text, label, period, kind):
    """v1.6 본사 발언만 뽑기(아디다스·아식스) — 푸마와 같은 규칙(MGMT_RULES)·원문 대조(verify_quotes). → 발언 목록"""
    prompt = f"""You are reading {label}'s {kind} for {period}.
Extract management statements only (no figures table).

Respond with ONLY JSON, no markdown fences:
{{"mgmt_notes": [{{"topic": "inventory|discount|channel", "quote": "one sentence copied VERBATIM", "ko": "한국어 한 줄 요약(60자 이내)"}}]}}
{MGMT_RULES}

DOCUMENT:
{text}"""
    data = anthropic_post({"model": "claude-sonnet-4-6", "max_tokens": 1200,
                           "messages": [{"role": "user", "content": prompt}]})
    txt = "".join(p.get("text", "") for p in data.get("content", []) if p.get("type") == "text")
    obj = json_obj(txt)
    return verify_quotes(obj.get("mgmt_notes") if isinstance(obj, dict) else None, text)


def _now_kst():
    return datetime.datetime.now(KST).strftime("%Y-%m-%d %H:%M")


def merge_notes(notes, old_notes, old_at=None):
    """v1.6 다시 뽑은 발언에 이전 발언의 신호(sig)·처음 뽑힌 시각(at)을 문장이 같으면 그대로 옮김(같은 문장을 Claude로 다시
    분류하지 않게 — 분류가 흔들려 '어제와 달라진 판정'이 생기지 않음 · 주간 메일은 문장별 at으로 새 문장만). 새 문장은 at = 지금.
    old_at = 이전 기록의 extracted_at(at 없는 옛 발언용). → (발언 목록, 새 문장 없음 여부)"""
    old = {_norm_q(n.get("quote")): n for n in old_notes or [] if isinstance(n, dict)}
    out = []
    for n in notes or []:
        if not isinstance(n, dict):
            continue
        n, o = dict(n), old.get(_norm_q(n.get("quote")))
        if o and o.get("sig") in SIGS and n.get("sig") not in SIGS:
            n["sig"] = o["sig"]
        n["at"] = (o.get("at") or old_at) if o and (o.get("at") or old_at) else (n.get("at") or _now_kst())
        out.append(n)
    new = {_norm_q(n.get("quote")) for n in out}
    return out, bool(old and new and new <= set(old))


def carry_notes(res, cached):
    """v1.6 같은 자료를 다시 추출할 때(표 일부만 읽힘 → PARTIAL_TRIES) 이미 뽑은 발언 상태를 새 결과로 옮김 —
    발언 문서가 그대로면 발언은 다시 뽑지 않고, 추출 시각·문서 날짜·신호도 그대로(주간 메일 중복·재분류 방지)"""
    if not (cached and res and cached.get("url") == res.get("url")):
        return
    ex, ox = res.get("extract"), cached.get("extract") or {}
    for k in ("notes_url", "doc_date", "notes_err"):
        if cached.get(k) and not res.get(k):
            res[k] = cached[k]
    if isinstance(ex, dict) and ox.get("mgmt_notes") is not None and "mgmt_notes" not in ex:
        ex["mgmt_notes"] = ox["mgmt_notes"]
        if ox.get("extracted_at"):
            ex["extracted_at"] = ox["extracted_at"]


def attach_notes(res, doc_url, text, label, period, kind, doc_date=None):
    """v1.6 발언을 res.extract에 붙임 — 실패하면 이전 발언 그대로 두고 실패 표시(다음 실행에서 다시: notes_url을 안 바꿈)"""
    ex = res.get("extract")
    if not isinstance(ex, dict):
        return
    try:
        notes = claude_mgmt_notes(text, label, period, kind)
    except SystemExit:
        raise
    except Exception as e:
        log(f"  [WARN] {label} 본사 발언 추출 안 됨 — 다음 실행에서 다시: {str(e)[:120]}")
        res["notes_err"] = "발언 추출 안 됨"
        soft_fail(f"{label} 본사 발언 추출 안 됨({str(e)[:80]}) — 다음 실행에서 다시")
        return
    notes, same = merge_notes(notes, ex.get("mgmt_notes"), ex.get("extracted_at"))
    ex["mgmt_notes"] = notes
    # 주간 메일 '이번 주 새 본사 발언' — 같은 분기를 더 나은 문서(스크립트본·보도자료)로 다시 뽑아 새 문장이 없으면
    # 추출 시각·문서 날짜를 그대로 둠(같은 발언이 다음 주 메일에 또 '새 발언'으로 나오지 않게)
    if not same:
        ex["extracted_at"] = datetime.datetime.now(KST).strftime("%Y-%m-%d %H:%M")
        if doc_date:
            res["doc_date"] = doc_date
    res["notes_url"] = doc_url
    res.pop("notes_err", None)


# v1.4 주제별 키워드 — extract_segments v11.1과 같음(붙은 주제 키워드가 없고 다른 주제 키워드만 있으면 그 주제로)
TOPIC_KW = {"inventory": re.compile(r"inventor", re.I),
            "discount": re.compile(r"promot|markdown|discount|(?<!off-)pric(?:e|ing)", re.I),
            "channel": re.compile(r"wholesale|\bdoors?\b|\baccounts?\b|off-price|distribut(?!ion (?:center|centre|cost))|"
                                  r"sell-in|marketplace|mass merchant", re.I)}
_STOP = {"this", "that", "with", "from", "into", "have", "been", "were", "their", "which", "also", "will",
         "more", "than", "over", "company", "quarter", "year"}
# 실적 문서 상투어(앞 5글자) — 'Gross margin decreased … basis points, primarily driven by …'가 겹친다고 같은 말로 보지 않게
_BOIL = {"gross", "margi", "basis", "point", "prima", "drive", "parti", "offse", "decre", "incre", "compa", "expec"}


def _words(q):
    """비슷한 문장 판정용 내용어 — 4글자 이상 영단어 앞 5글자"""
    return {w[:5] for w in re.findall(r"[a-z]+", _norm_q(q)) if len(w) >= 4 and w not in _STOP and w[:5] not in _BOIL}


SIGS = ("more", "less", "neutral")


def classify_notes(notes, label=""):
    """v1.5 본사 발언마다 병행수입 매입 관점 신호(sig) — extract_segments v11.2와 같음. 실패하면 그대로(다음 실행에서 다시)"""
    notes = [dict(n) for n in notes or [] if isinstance(n, dict)]
    todo = [i for i, n in enumerate(notes) if n.get("sig") not in SIGS]
    if not todo or not ANTHROPIC_KEY or not _opt_ok(f"{label} 발언 신호 분류"):
        return notes
    lines = "\n".join(f"{k + 1}. [{notes[i].get('topic')}] {notes[i].get('quote')}" for k, i in enumerate(todo))
    n = len(todo)
    prompt = f"""You advise a Korean parallel importer that buys branded footwear and apparel from overseas retailers, outlets and off-price channels.
Below {"is the only statement" if n == 1 else f"are all {n} statements"} taken from {label}'s latest earnings release (the list is complete). For each, decide what it implies for the next few months:
  "more"    - more discounted or excess product likely available (inventory elevated or being cleared/liquidated, more promotions or markdowns, off-price or liquidation channel sales)
  "less"    - less discounted product or tighter supply (lower discounting, full-price protection, fewer promotions, cutting wholesale accounts or doors, limiting supply, inventory already lean or clean)
  "neutral" - neither, or unclear
Respond with ONLY a JSON array of exactly {n} string(s), one per statement in the same order, e.g. {'["more"]' if n == 1 else '["more","neutral"]'}. No explanation.

{lines}"""
    try:
        txt = ""
        data = anthropic_post({"model": "claude-sonnet-4-6", "max_tokens": 200,
                               "messages": [{"role": "user", "content": prompt}]}, timeout=60)
        txt = "".join(p.get("text", "") for p in data.get("content", []) if p.get("type") == "text")
        m = re.search(r"\[[^\[\]]*\]", txt)      # 설명이 앞뒤에 붙어도 첫 JSON 배열만 읽음
        arr = json.loads(m.group(0) if m else txt.strip())
        if not isinstance(arr, list) or len(arr) != len(todo):
            raise ValueError(f"응답 개수 {len(arr) if isinstance(arr, list) else '?'} ≠ {len(todo)}")
    except SystemExit:
        raise
    except Exception as e:
        head = f" · 응답 앞부분: {txt[:80]!r}" if txt else ""
        log(f"  [WARN] {label} 본사 발언 신호 분류 실패 — 다음 실행에서 다시: {str(e)[:120]}{head}")
        return notes
    for k, i in enumerate(todo):
        v = str(arr[k]).strip().lower()
        notes[i]["sig"] = v if v in SIGS else "neutral"
    log(f"  {label} 본사 발언 신호: " + " · ".join(f"{notes[i].get('topic')}→{notes[i]['sig']}" for i in todo))
    return notes


def _same(n, w, o):
    """같은 주제이고 내용어가 6개 이상·짧은 쪽의 60% 넘게 겹치면 같은 말(브랜드·지역만 다른 문장은 남김)"""
    ow = _words(o.get("quote"))
    sh = len(w & ow)
    return o.get("topic") == n.get("topic") and sh >= 6 and sh / max(1, min(len(w), len(ow))) > 0.6


def tidy_notes(notes, label=""):
    """v1.4 본사 발언 다듬기 — ① 주제 바로잡기 ② 같은 주제에서 내용어가 6개 이상·60% 넘게 겹치는 문장은 앞의 것만. 몇 번 돌려도 결과가 같음"""
    out, fixed, dup = [], 0, 0
    for n in notes or []:
        if not isinstance(n, dict):
            continue
        q = str(n.get("quote") or "")
        hits = {t: len(p.findall(q)) for t, p in TOPIC_KW.items()}
        if not hits.get(n.get("topic")) and max(hits.values()) > 0:
            n = dict(n, topic=max(hits, key=lambda k: hits[k]))
            fixed += 1
        w = _words(q)
        if w and any(_same(n, w, o) for o in out):
            dup += 1
            continue
        out.append(n)
    if fixed or dup:
        log(f"  {label} 본사 발언 정리: 주제 바로잡음 {fixed}건 · 비슷한 문장 {dup}건 뺌")
    return out


def run_puma(cached):
    url, d = puma_latest_release()
    if not url:
        log("[PUM.DE] 실적 보도자료 미발견"); return None
    period, prev = puma_period(d)
    log(f"[PUM.DE] 최신 보도자료 {period}: {url}")
    if cache_ok(cached, url):
        cached.pop("skipped_url", None)     # 건너뛴 보도자료가 목록에서 내려감
        log("  캐시 사용"); return cached
    if cached and cached.get("skipped_url") == url and cached.get("extract"):
        log("  지역 금액이 없던 보도자료(예비 실적·전망 등, 지난번 확인) — 건너뛰고 이전 값"); return cached
    if not ANTHROPIC_KEY:
        log("  [WARN] ANTHROPIC_API_KEY 미설정 → 추출 생략")
        soft_fail("ANTHROPIC_API_KEY 없음 — 새 실적 자료 추출 생략(GitHub Secrets·ir.yml 확인)")
        return cached
    text = strip_html(fetch(url))
    ex = claude_extract_puma(text, period, prev)
    ox = (cached.get("extract") or {}) if cached and cached.get("url") == url else {}
    notes, same = merge_notes(ex.get("mgmt_notes"), ox.get("mgmt_notes"), ox.get("extracted_at"))
    if ox.get("mgmt_notes"):
        # v1.6 같은 자료 다시 추출(표 일부만 읽힘) — 이미 뽑아 둔 발언은 지키고(Claude가 이번엔 놓쳐도) 새 문장만 더함(최대 3개)
        olds = [dict(n, at=n.get("at") or ox.get("extracted_at") or _now_kst()) for n in ox["mgmt_notes"] if isinstance(n, dict)]
        keep = {_norm_q(n.get("quote")) for n in olds}
        add = [n for n in notes if _norm_q(n.get("quote")) not in keep]
        notes = tidy_notes(olds + add, "PUM.DE")[:3]
        kept_q = {_norm_q(n.get("quote")) for n in notes}
        same = not any(_norm_q(n.get("quote")) in kept_q for n in add)
        if same and ox.get("extracted_at"):
            ex["extracted_at"] = ox["extracted_at"]
    ex["mgmt_notes"] = notes
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
            # v1.6 예비 실적·전망 보도자료일 수 있음 — 이전 값을 지키고 같은 자료는 다음부터 건너뜀(화면에 쓰는 그 자료를 다시
            # 추출하다 못 읽은 경우는 아님 — 그때는 보통 실패 처리로 이전 값 유지·다음 주 다시)
            "skip_url": None if ok or (cached and cached.get("url") == url) else url,
            "doc_date": f"{d[0]:04d}-{d[1]:02d}-{d[2]:02d}" if d and d[0] else None,   # v1.4 보도자료 날짜(URL)
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
    return json_obj(txt)


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
    ex = json_obj(txt)
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
        log("  캐시 사용")
        # v1.6 발언을 아직 못 뽑았거나 스크립트 없는 설명자료에서 뽑았으면 — 스크립트 포함본은 며칠 늦게 올라오기도 함
        # (2026 Q2: 결산 8월 중순 → 스크립트본 PDF 8/21). 설명자료 주소가 그대로면 asics_notes가 다시 안 뽑음
        if not re.search(r"script", cached.get("notes_url") or "", re.I):
            asics_notes(cached, key, period)
        return cached
    if not ANTHROPIC_KEY:
        log("  [WARN] ANTHROPIC_API_KEY 미설정 → 추출 생략")
        soft_fail("ANTHROPIC_API_KEY 없음 — 새 실적 자료 추출 생략(GitHub Secrets·ir.yml 확인)")
        return cached
    from pypdf import PdfReader
    raw = fetch(url, as_bytes=True, timeout=120)
    pages = [(p.extract_text() or "") for p in PdfReader(io.BytesIO(raw)).pages]
    ex = claude_extract_asics(asics_segment_text(pages), period, prev)
    ex.setdefault("schema_v", 2); ex.setdefault("channels", []); ex.setdefault("sub_segments", [])
    ex["notes"] = (ex.get("notes") or "") + " · 누적 기준(Japan GAAP 결산단신) · 한국은 Others에 포함"
    for r in ex.get("regions", []):
        r["cn_yoy_pct"] = None
    su, pages2 = None, None
    try:
        if not _opt_ok("아식스 환율 제외 성장률"):
            raise OutOfTime("실행 시간")
        su = asics_summary_pdf(key)
        if su:
            log(f"  환율 제외 성장률: 실적 설명자료 {su}")
            raw2 = fetch(su, as_bytes=True, timeout=180)
            pages2 = [(p.extract_text() or "") for p in PdfReader(io.BytesIO(raw2)).pages]
            _ASX[su] = (pages2, _pdf_date(raw2))
            anchors = [(r["name"], r["yoy_pct"]) for r in ex.get("regions", []) if r.get("yoy_pct") is not None]
            kept = attach_asics_cn(ex.get("regions", []), claude_asics_cn(asics_region_text(pages2), period, anchors))
            log(f"    결산단신과 일치 {kept}/{len(anchors)}개 지역 채택")
        else:
            log("  실적 설명자료 미발견 — 환율 제외 생략")
    except SystemExit:
        raise
    except OutOfTime:
        ex["cn_skipped"] = True     # v1.6 시간이 모자라 건너뜀 — '표 일부만 읽힘' 알림 대신 다음 주에 같은 자료로 다시(조용히)
        log("  실행 시간이 길어져 환율 제외 성장률은 다음 실행에(지역 금액은 저장)")
    except Exception as e:
        # v1.6 갈래만(오류 원문·'실패' 낱말 없이) — 처음 빠진 실행은 '표 일부만 읽힘(환율 제외)'으로 알림, 다시 추출하는 주는 조용히
        kind = _kind(e) if isinstance(e, requests.exceptions.RequestException) else ("응답 형식" if isinstance(e, ValueError) else type(e).__name__)
        log(f"  환율 제외 성장률 못 읽음(지역 금액은 유지 · {kind})")
        if su and su not in _ASX:
            _ASX[su] = None     # v1.6 이번 실행에서 못 받은 설명자료 — asics_notes가 같은 PDF를 다시 받지 않게
    for r in ex.get("regions", []):
        log(f"  {r.get('name')}: {r.get('revenue')} / 전년 {r.get('prev_revenue')} (엔화 {r.get('yoy_pct') and round(r['yoy_pct'],1)}%) · 환율 제외 {r.get('cn_yoy_pct')}%")
    ok = any(r.get("revenue") is not None for r in ex.get("regions", []))
    res = {"accession": url.rsplit("/", 1)[-1][:80], "source": "IR 결산단신 (PDF)", "url": url,
           "error": None if ok else "세그먼트 표 미추출", "extract": ex if ok else None,
           "fetched_at": datetime.datetime.now(KST).strftime("%Y-%m-%d"), "ir_ver": IR_VER}
    if ok:
        carry_notes(res, cached)    # 같은 자료 다시 추출(표 일부만 읽힘)이면 이미 뽑은 발언 그대로(설명자료가 같으면 다시 안 뽑음)
        asics_notes(res, key, period, su or False)    # False = 설명자료를 이미 찾아봤는데 없음
    return res


_ASX = {}    # v1.6 이번 실행에서 받은 설명자료 {주소: (쪽 글, 문서 날짜)} — 환율 제외·발언에 같은 PDF를 한 번만 받음


def _pdf_date(raw):
    """PDF 만든 날(메타데이터) → 'YYYY-MM-DD' — 아식스 설명자료 발표일에 가까움(주간 메일 문서 날짜). 없으면 None"""
    try:
        from pypdf import PdfReader
        d = PdfReader(io.BytesIO(raw)).metadata.creation_date
        return d.strftime("%Y-%m-%d") if d else None
    except Exception:
        return None


def asics_notes(res, key, period, su=None):
    """v1.6 아식스 본사 발언 — 실적 설명자료(스크립트 포함본 우선)에서. 설명자료가 아직 없으면 다음 실행에서 다시,
    이미 뽑은 설명자료(notes_url)와 같으면 다시 안 뽑음. 예외를 올리지 않음(지역 표는 그대로 저장되게)"""
    if not ANTHROPIC_KEY or not _opt_ok("아식스 본사 발언"):
        return
    try:
        if su is None:
            su = asics_summary_pdf(key)
        if not su:
            log("  실적 설명자료 미발견 — 본사 발언은 다음 실행에서 다시"); return
        if su == res.get("notes_url"):
            log("  본사 발언: 같은 설명자료 — 발언 캐시 사용"); return
        if su in _ASX and _ASX[su] is None:
            raise RuntimeError("이번 실행에서 이미 못 받음")
        if su not in _ASX:
            from pypdf import PdfReader
            raw2 = fetch(su, as_bytes=True, timeout=180)
            _ASX[su] = ([(p.extract_text() or "") for p in PdfReader(io.BytesIO(raw2)).pages], _pdf_date(raw2))
    except SystemExit:
        raise
    except Exception as e:
        kind = _kind(e) if isinstance(e, requests.exceptions.RequestException) else type(e).__name__
        if res.get("notes_url") and (res.get("extract") or {}).get("mgmt_notes") is not None:
            # 이 분기 발언은 이미 있음(스크립트 없는 설명자료에서) — 스크립트본으로 바꾸기만 못 함: 조용히 다음 주에 다시
            log(f"  본사 발언: 스크립트본 설명자료는 다음 실행에 다시({kind}) — 이미 뽑아 둔 발언 그대로"); return
        log(f"  [WARN] 아식스 실적 설명자료를 못 받음 — 본사 발언은 다음 실행에서 다시: {str(e)[:120]}")
        res["notes_err"] = "설명자료 받기 안 됨"
        soft_fail(f"7936.T 실적 설명자료를 못 받음({str(e)[:80]}) — 본사 발언 다음 실행에서 다시")
        return
    pages2, dd = _ASX[su]
    log(f"  본사 발언: 실적 설명자료 {su.rsplit('/', 1)[-1][:80]}" + (f" ({dd})" if dd else ""))
    attach_notes(res, su, kw_windows(" ".join(pages2)), "ASICS", period,
                 "results presentation with speaker script (Consolidated Financial Summary)", doc_date=dd)


RUNS = (("ADS.DE", run_adidas), ("PUM.DE", run_puma), ("7936.T", run_asics))
NOTES_TK = ("ADS.DE", "7936.T")
SKIP_REASON = "최신 보도자료 건너뜀(지역 금액 없음 — 예비 실적·전망일 수 있음)"    # v1.6 발언을 지역 표와 다른 문서에서 뽑는 종목(notes_url)
# v1.6 늘 금액이 나오는 줄(이름 앞부분) — 하나라도 금액이 없으면 '표 일부만 읽힘'. 푸마 북미·중화권·중남미는 금액 없이 %만 나와 뺌
# (푸마 도매·직판은 분기마다 금액이 나옴 — 2024 Q1·Q3, 2025 Q4, 2026 Q1·Q2 확인)
WANT_ROWS = {"ADS.DE": (r"europe", r"north america", r"greater china", r"emerging", r"latin", r"japan", r"wholesale", r"direct|dtc"),
             "PUM.DE": (r"emea", r"americas", r"asia", r"wholesale", r"direct|dtc"),
             "7936.T": (r"japan", r"north america", r"europe", r"greater china", r"oceania", r"southeast", r"other")}


def missing_rows(tk, ex):
    """v1.6 표 일부만 읽힘 — WANT_ROWS 중 금액(revenue)이 있는 줄이 없는 것 + (아디다스·아식스) 전년 금액이 없는 줄 ·
    환율 제외 성장률이 하나도 없음(시간이 모자라 건너뛴 cn_skipped는 빼고 — 대신 같은 자료를 조용히 다시 추출)"""
    rows = [r for r in (ex.get("regions") or []) + (ex.get("channels") or [])
            if isinstance(r, dict) and r.get("revenue") is not None]
    names = [str(r.get("name") or "").lower() for r in rows]
    nr = [w.split("|")[0] for w in WANT_ROWS.get(tk, ()) if not any(re.match(w, n) for n in names)]
    miss = ["금액 없음: " + ", ".join(nr)] if nr else []
    if tk in ("ADS.DE", "7936.T"):
        # 두 회사 표는 금액이 있는 줄마다 전년 같은 기간 금액이 함께 나옴(푸마 채널은 전년 금액 없이 나오기도 해 뺌)
        np_ = [str(r.get("name") or "?").split(" (")[0] for r in rows if r.get("prev_revenue") is None]
        if np_:
            miss.append("전년 금액 없음: " + ", ".join(np_))
        if rows and not ex.get("cn_skipped") and not any(isinstance(r, dict) and r.get("cn_yoy_pct") is not None
                                                         for r in ex.get("regions") or []):
            miss.append("환율 제외 성장률 없음")      # 아디다스 Fact Sheet c.n. 열 · 아식스 설명자료(일본 말고는 늘 있음)
    return miss


def period_end(p):
    """v1.6 'Q2 2026'·'6M 2026 (1~6월 누적)'·'FY 2025' → 그 기간 끝날(date), 못 읽으면 None"""
    m = re.search(r"\b(Q[1-4]|3M|6M|9M|FY|H1|H2)\s+(20\d\d)\b", str(p or ""))
    if not m:
        return None
    mon = {"Q1": 3, "3M": 3, "Q2": 6, "6M": 6, "H1": 6, "Q3": 9, "9M": 9}.get(m.group(1), 12)
    y = int(m.group(2))
    nxt = datetime.date(y + (mon == 12), mon % 12 + 1, 1)
    return nxt - datetime.timedelta(days=1)


def main():
    _WARN.clear(); _NOW.update(tk=None)     # 한 프로세스에서 여러 번 불러도(시험) 지난 실행의 실패 표시가 섞이지 않게
    old = {}
    if os.path.exists(OUT_PATH):
        try:
            with open(OUT_PATH, encoding="utf-8") as f:
                old = json.load(f)
        except Exception:
            pass
    items = dict(old.get("items", {}))
    prev_items = json.loads(json.dumps(items))     # v1.6 이번 실행 전 상태(표 일부만 읽힘 — 처음 나온 실행만 알림)
    only = [x.strip() for x in os.environ.get("IR_ONLY", "").split(",") if x.strip()]
    if only:    # v1.3 시험 모드: 지정 종목만 캐시 무시하고 추출, 결과는 로그로만(저장 안 함 · v1.6 실패 표시도 기록 안 함)
        log(f"[시험 모드] IR_ONLY={','.join(only)} — 저장하지 않음")
        _NOW["test"] = True
        for tk, fn in RUNS:
            if tk not in only:
                continue
            res = fn(None) or {}
            ex = res.get("extract") or {}
            log(f"[{tk}] {res.get('source')} · {ex.get('period')} · 지역 {len(ex.get('regions') or [])}"
                + (f" · 표 일부만 읽힘({' · '.join(missing_rows(tk, ex))})" if ex and missing_rows(tk, ex) else ""))
            for n in classify_notes(ex.get("mgmt_notes") or [], tk):
                log(f"    [{n['topic']}·{n.get('sig', '?')}] {n['ko']} — \"{n['quote'][:200]}\"")
        return
    failed = []     # v1.6 수집 상태 화면 '일부 실패'(build_dashboard — extract_segments와 같은 failed·kept_failed·kept_reason)
    fresh = set()   # 이번 실행에서 새로 추출한 종목(캐시가 아닌)
    for tk, fn in RUNS:
        prev = items.get(tk)
        _NOW["tk"] = tk
        try:
            res = fn(prev)
            err = None if (res and res.get("extract")) else ((res or {}).get("error") or "자료 링크를 못 찾음")
        except SystemExit:
            raise
        except Exception as e:
            res, err = None, f"수집 안 됨: {str(e)[:160]}"
        if not err:
            res.pop("kept_failed", None); res.pop("kept_reason", None)
            if res is prev and res.get("skipped_url"):     # 지역 금액 없는 최신 보도자료를 건너뛰는 중(안내만 — 수집 상태 '최신 공시 건너뜀')
                res["kept_reason"] = SKIP_REASON
            if res is not prev:
                fresh.add(tk)
            if tk in NOTES_TK:      # 전 분기까지 발언이 있었는지(새 분기 발언 문서가 안 나오면 NOTES_LAG_DAYS 뒤 실패 표시)
                if res.get("notes_url"):
                    res.pop("notes_seen", None)
                elif prev and (prev.get("notes_url") or prev.get("notes_seen")):
                    res["notes_seen"] = True
            items[tk] = res
            continue
        # v1.6 실패 — 이전에 잘 받아 둔 값이 있으면 지킴(전에는 표 해석 실패 결과로 덮어써 화면에서 지역·발언이 사라짐)
        keep = bool(prev and prev.get("extract"))
        if keep and res and res.get("skip_url"):
            # 푸마 최신 보도자료에 지역 금액이 없음 — 예비 실적·전망 자료일 수 있어 이전 값을 지키고 같은 자료는 다음부터 건너뜀.
            # 알림은 이번 한 번(정말 실적 자료인데 형식이 바뀐 경우 대비) · 수집 상태에는 '최신 공시 건너뜀' 안내
            prev["skipped_url"], prev["kept_reason"] = res["skip_url"], SKIP_REASON
            prev.pop("kept_failed", None)
            soft_fail(f"{tk} 최신 보도자료에 지역 금액 없음({res['skip_url'].rsplit('/', 1)[-1][:70]}) — "
                      f"예비 실적·전망 자료일 수 있음, 이전 값({prev['extract'].get('period')}) 유지 · 같은 자료는 다음부터 건너뜀")
            continue
        log(f"[{tk}] {err}" + (" — 이전 값 유지" if keep else ""))
        soft_fail(f"{tk} {err}" + (f" — 이전 값({prev['extract'].get('period')}) 유지" if keep else ""))
        failed.append(tk)
        if keep:
            prev["kept_failed"], prev["kept_reason"] = True, err[:120]
            if prev.get("partial"):     # 표 일부만 읽힌 자료를 다시 추출하다 실패 — 다시 추출 횟수에 넣음(매주 되풀이하지 않게)
                prev["partial_tries"] = int(prev.get("partial_tries") or 0) + 1
        elif res:
            items[tk] = res     # 이전 값이 없으면 오류 기록이라도(수집 상태 '값 없음')
    today = datetime.datetime.now(KST).date()
    for tk, _ in RUNS:
        _NOW["tk"] = tk
        it = items.get(tk) or {}
        ex = it.get("extract") or {}
        if not ex:
            continue
        end = period_end(ex.get("period"))      # 새 분기 자료가 오래 안 들어오면(사이트 구조 바뀜 등) 실패 표시
        age = (today - end).days if end else None
        if age is not None and age > STALE_DAYS:
            soft_fail(f"{tk} 가장 최근 자료가 {ex.get('period')}(끝난 지 {age}일) — 새 분기 자료를 못 찾음, IR 사이트 확인")
            if tk not in failed:
                failed.append(tk)
                it["kept_failed"], it["kept_reason"] = True, f"새 분기 자료 못 찾음(끝난 지 {age}일)"
        # 표 일부만 읽힘 — 저장은 하고, 그 결과가 처음 나온 실행에만 알림(같은 자료는 PARTIAL_TRIES까지 다시 추출,
        # 그 뒤로는 조용히 — 수집 상태 화면 warn에는 계속 남음 · logistics odd_seen과 같은 방식)
        miss = missing_rows(tk, ex)
        p0 = prev_items.get(tk) or {}
        CN = "환율 제외 성장률 없음"
        if ex.get("cn_skipped") and p0.get("url") == it.get("url") and CN in (p0.get("partial") or []) and CN not in miss:
            miss.append(CN)     # 시간이 모자라 환율 제외를 이번에도 못 읽음 — 지난번 '표 일부만 읽힘' 그대로(다시 알리지 않음)
        if miss:
            same = p0.get("url") == it.get("url") and p0.get("partial") == miss
            if tk in fresh:
                it["partial_tries"] = int(p0.get("partial_tries") or 0) + 1 if p0.get("url") == it.get("url") else 1
            it["partial"] = miss
            msg = f"{tk} {ex.get('period')} 표 일부만 읽힘({' · '.join(miss)}) — 나머지는 저장, 표 형식 확인"
            if not same:        # 처음 나왔거나 빠진 줄이 바뀜(캐시로 이어 온 옛 자료라도 아직 알린 적 없으면)
                soft_fail(msg)
            else:
                log(f"  (이전 실행부터) {msg[len(tk) + 1:]}")
                _WARN.setdefault(tk, []).append(msg[len(tk) + 1:])
        else:
            it.pop("partial", None); it.pop("partial_tries", None)
        if it.get("notes_seen") and not it.get("notes_url"):    # 전 분기까지 있던 발언이 새 분기에 안 나옴
            try:
                nd = (today - datetime.date.fromisoformat(str(it.get("fetched_at"))[:10])).days
            except ValueError:
                nd = None
            if nd is not None and nd > NOTES_LAG_DAYS:
                why = (f"본사 발언을 {nd}일째 못 뽑음({it['notes_err']})" if it.get("notes_err")
                       else f"본사 발언 문서를 {nd}일째 못 찾음")
                soft_fail(f"{tk} {ex.get('period')} {why}(전 분기까지는 있었음) — IR 사이트 확인")
    _NOW["tk"] = None
    for tk, v in items.items():     # v1.4 캐시에도 같은 정리(새 추출은 이미 정리됨)
        ex = (v or {}).get("extract")
        if isinstance(ex, dict) and isinstance(ex.get("mgmt_notes"), list):
            ex["mgmt_notes"] = classify_notes(tidy_notes(ex["mgmt_notes"], tk), tk)   # v1.5 신호 없는 발언만 분류
    out = {"generated_at": datetime.datetime.now(KST).strftime("%Y-%m-%d %H:%M KST"), "items": items,
           "claude_usage": usage_months(old)}    # v1.4 월별 Claude 사용량(수집 상태 화면)
    if failed:
        out["failed"] = failed
    for tk, v in items.items():     # v1.6 실패 표시가 난 종목 — 수집 상태 화면 '확인 필요'(이전 값 유지는 failed·kept_failed로 따로)
        if not isinstance(v, dict):
            continue
        if _WARN.get(tk) and tk not in failed:
            v["warn"] = " · ".join(dict.fromkeys(_WARN[tk]))[:160]
        else:
            v.pop("warn", None)
    os.makedirs("docs", exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    log(f"saved {OUT_PATH} — {sum(1 for v in items.values() if v.get('extract'))}/3 추출")
    log(f"Claude 사용: 이번 실행 {_USAGE['calls']}회 · ${_USAGE['usd']:.3f} · 이번 달 누적 "
        f"${out['claude_usage'][max(out['claude_usage'])]['usd']:.2f}")


if __name__ == "__main__":
    main()

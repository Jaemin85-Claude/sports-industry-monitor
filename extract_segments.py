# -*- coding: utf-8 -*-
"""
sports-industry-monitor — Phase 2: 공시 추출 (v5.1)
v11: (대표 지시 2026-10-10) 본사 발언 — 실적 문서에서 재고·할인·유통 통제 문장을 원문 그대로 최대 3개(mgmt_notes: topic·quote·ko).
     원문에 글자 그대로 있는 문장만 남김(코드로 확인). SCHEMA_V=3으로 1회 재추출. 시험용 SEG_ONLY(쉼표 구분 티커) — 저장 안 함
v10: (대표 지시 2026-10-09) 투자자의 날·중기 목표·프로포마 자료는 실적 자료에서 빼고(파일명·제목·앞부분) 그 전 실적
      공시를 고름(온 9/22·딕스 9/21 오선택 해결, 잘못 저장된 공시는 다시 안 고름). 새 추출이 비었거나 실패하면 이전 실적
      추출 유지(kept_reason, 실패는 kept_failed·failed), 분해 없는 공시는 기록해 매주 Claude 재호출 안 함. SEC·Claude 일시
      오류는 1분·3분 뒤 재시도(연달아 실패하면 남은 호출 생략), 절반 넘게 실패하면 실패 표시(soft_fail.txt).
v9: Anthropic 401/403·크레딧 소진 시 즉시 실패(워크플로우 빨간 X)
v8: 실적자료 판별 강화 — EX-10(계약서) 계열 파일명 배제, 계약서 문구 감지 시
      제외, 실적 보도자료 고유 표현 요구(UAA가 계약 공시를 실적으로 오탐한 문제).
      대용량 문서 3MB 상한으로 지연 방지.
v7: 첨부 목록 3중 소스 — index.json → 공시 인덱스 페이지(-index.htm, /ix?doc= 접두어
      해제) → 디렉터리 목록(상대경로 href 지원). 최근 공시에서 index.json이 실제
      첨부를 반환하지 않는 문제(DKS·UAA·LULU·CROX·VFC) 해결.
v6: 후보 단위 오류 격리 — 첨부 1개가 404여도 공시 전체를 버리지 않고 다음 첨부로
      진행(DKS 8/25 2분기·ASO 최신 공시 누락 원인). 폴백 앵커를 해당 공시 폴더
      경로로 한정, 본문 길이 하한 1500자로 완화, 오류 로그 전체 URL 표시.
v5.1: 신규 종목 반영 — 울버린(WWW)·컬럼비아(COLM) 추출 대상 추가,
      미즈노·요넥스·골드윈(일본)·안타·리닝(홍콩)·푸마(독일)는 EDGAR 미대상 표기
v5: 전년 동기 수치(prev_revenue) 추출 — 공시 비교표에 명시된 경우만, 미기재는
    null(대시보드에서 YoY 역산 + [역산] 표기). schema_v=2로 캐시 자동 갱신.
v4: 첨부 목록 폴백(index.json 미비 공시 대응) / v3: 실적 문서 내용 검증
출력: docs/segments.json — §29-D: 명시 수치만 추출, 미기재는 null
동일 공시(accession)+동일 스키마는 재추출하지 않음(캐시)
"""

import os
import re
import json
import html
import time
import datetime
import requests

CONTACT_EMAIL = "nightsit7@gmail.com"   # 반드시 영문 이메일로 교체

_safe_email = CONTACT_EMAIL.encode("ascii", "ignore").decode() or "contact@example.com"
UA = {"User-Agent": f"sports-industry-monitor ({_safe_email})"}
API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
KST = datetime.timezone(datetime.timedelta(hours=9))
SCHEMA_V = 3   # 추출 스키마 버전 (필드 변경 시 +1 → 캐시 자동 무효화) — v11 mgmt_notes 추가

US_TICKERS = ["NKE", "ONON", "DECK", "AS", "LULU", "BIRK",
              "CROX", "VFC", "UAA", "WWW", "COLM",
              "DKS", "ASO"]
NON_US = {"ADS.DE": "EDGAR 미대상(독일 상장)",
          "PUM.DE": "EDGAR 미대상(독일 상장)",
          "7936.T": "EDGAR 미대상(일본 상장)",
          "8022.T": "EDGAR 미대상(일본 상장)",
          "7906.T": "EDGAR 미대상(일본 상장)",
          "8111.T": "EDGAR 미대상(일본 상장)",
          "2020.HK": "EDGAR 미대상(홍콩 상장)",
          "2331.HK": "EDGAR 미대상(홍콩 상장)",
          "JD.L": "EDGAR 미대상(영국 상장)"}

SEG_PATH = "docs/segments.json"
SCRIPT = "extract_segments"


MAX_DOC_BYTES = 3_000_000   # 대용량 문서 상한 (지연 방지)


def soft_fail(msg):
    """심각한 실패 표시 — 저장은 하되 워크플로우 마지막 단계가 빨간 X로 끝내 점검 알림이 가게 함"""
    print(f"실패 표시: {msg}", flush=True)
    with open("soft_fail.txt", "a", encoding="utf-8") as f:
        f.write(f"{SCRIPT}: {msg}\n")


# ── v10: 일시 오류 재시도(SEC 접속·Claude 과부하) ──
RETRY_WAITS = (60, 180)      # 1분 뒤·3분 뒤 두 번 재시도
RETRY_DEADLINE = 20 * 60     # 실행 20분이 지나면 재시도 생략(워크플로우 30분 제한)
RUN_DEADLINE = 22 * 60       # 실행 22분이 지나면 남은 종목은 SEC·Claude 호출 없이 이전 값 유지
ATTEMPT_MAX = {"sec": 90, "claude": 180}   # 한 번 시도에 걸릴 수 있는 최대 시간(요청 timeout)
_T0 = time.time()
# streak: 연달아 끝내 실패한 횟수(2번부터는 기다리지 않음). where: 그 실패가 난 종목들 — 서로 다른 2곳에서
# 연달아 끝내 실패하면(전면 장애) 그 뒤로는 호출을 아예 생략(회로 차단). 한 공시만 깨진 경우는 1곳으로 셈.
# sec.skipped: SEC 일시 오류 때문에 후보 공시·첨부를 실제로 건너뛴 횟수(더 새 공시를 놓쳤을 수 있음)
_RETRY = {"sec": {"streak": 0, "gave_up": 0, "skipped": 0, "where": set()},
          "claude": {"streak": 0, "gave_up": 0, "where": set()}}
_NOW = {"ticker": "시작"}   # 지금 처리 중인 종목(company_tickers.json은 '시작')


class TransientError(RuntimeError):
    """다시 시도할 만한 일시 오류(429·5xx·과부하)"""


def _is_transient(e):
    if isinstance(e, TransientError):
        return True
    if isinstance(e, (requests.exceptions.ConnectionError, requests.exceptions.Timeout,
                      requests.exceptions.ChunkedEncodingError)):
        return True
    resp = getattr(e, "response", None)
    if isinstance(e, requests.exceptions.HTTPError) and resp is not None:
        return resp.status_code == 429 or resp.status_code >= 500
    return False   # 404·403 등은 다시 해도 같음


def _ok(kind):
    st = _RETRY[kind]
    st["streak"] = 0
    st["where"].clear()


def _gave_up(kind):
    """끝내 실패 1회 기록 — 서로 다른 2곳에서 연달아면 이번 실행의 남은 호출은 생략"""
    st = _RETRY[kind]
    st["streak"] += 1
    st["gave_up"] += 1
    n0 = len(st["where"])
    st["where"].add(_NOW["ticker"])
    if n0 < 2 <= len(st["where"]):
        print(f"  [중단] {kind.upper()} 연달아 실패 — 이번 실행의 남은 {kind.upper()} 호출은 생략하고 "
              f"이전 값 유지", flush=True)


def _blocked(kind):
    """호출 생략 사유(실행 시간 상한·전면 장애), 없으면 None"""
    if time.time() - _T0 > RUN_DEADLINE:
        return f"실행 {RUN_DEADLINE // 60}분 넘음"
    if len(_RETRY[kind]["where"]) >= 2:
        return f"{kind.upper()} 연달아 실패"
    return None


def with_retry(kind, fn):
    """fn() 실행 — 일시 오류면 1분·3분 뒤 다시. 그 밖의 오류·SystemExit는 그대로 올림"""
    st = _RETRY[kind]
    n = 0
    while True:
        try:
            out = fn()
            _ok(kind)
            return out
        except Exception as e:
            if not _is_transient(e):
                raise
            wait = RETRY_WAITS[n] if n < len(RETRY_WAITS) else None
            if (wait is None or st["streak"] >= 2   # 다음 시도 시간까지 넣어 20분 상한 판단
                    or time.time() - _T0 + wait + ATTEMPT_MAX[kind] > RETRY_DEADLINE):
                _gave_up(kind)
                raise
            n += 1
            print(f"  [재시도 {n}/{len(RETRY_WAITS)}] {kind.upper()} 일시 오류 — "
                  f"{wait // 60}분 뒤 다시: {str(e)[:120]}", flush=True)
            time.sleep(wait)


# ── Anthropic 호출 공통: 인증/크레딧 오류는 즉시 실패(워크플로우 빨간 X) ──
def anthropic_post(payload, timeout=180):
    """401(키 무효/만료)·403·400 credit(잔액 소진) → SystemExit(2)로 즉시 종료.
    429·5xx(과부하 529 포함)·연결 오류는 1분·3분 뒤 재시도(v10).
    응답 시간 초과는 요청이 이미 처리됐을 수 있어(이중 과금) 재시도하지 않음.
    그 외 오류는 응답 본문을 포함해 예외로 올려 호출부가 처리."""
    blocked = _blocked("claude")
    if blocked:
        raise RuntimeError(f"{blocked} — 이번 실행에서 Claude 호출 생략")

    def _once():
        try:
            resp = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers={"x-api-key": API_KEY, "anthropic-version": "2023-06-01",
                         "content-type": "application/json"},
                json=payload, timeout=timeout)
        except requests.exceptions.ReadTimeout:
            _gave_up("claude")
            raise RuntimeError(f"Anthropic 응답 {timeout}초 넘음 — 이중 과금 막으려 재시도 안 함")
        if resp.status_code in (401, 403) or (resp.status_code == 400 and "credit" in resp.text.lower()):
            print(f"[FATAL] Anthropic API {resp.status_code}: {resp.text[:300]}", flush=True)
            print("[FATAL] 키 만료/무효 또는 크레딧 소진 — console.anthropic.com 확인 후 "
                  "GitHub Secret ANTHROPIC_API_KEY 갱신", flush=True)
            raise SystemExit(2)
        if resp.status_code == 429 or resp.status_code >= 500:
            raise TransientError(f"Anthropic {resp.status_code}: {resp.text[:200]}")
        if resp.status_code != 200:
            raise RuntimeError(f"Anthropic {resp.status_code}: {resp.text[:200]}")
        return resp.json()
    return with_retry("claude", _once)


def sec_get(url, is_json=True, retry=True):
    """SEC 요청 — 연결 오류·429·5xx는 1분·3분 뒤 재시도(v10).
    retry=False: 대체 경로가 있는 요청은 한 번만. 전면 장애·실행 시간 상한이면 호출 생략"""
    blocked = _blocked("sec")
    if blocked:
        raise TransientError(f"{blocked} — 이번 실행에서 SEC 호출 생략")
    if not retry:
        out = _sec_get_once(url, is_json)
        _ok("sec")
        return out
    return with_retry("sec", lambda: _sec_get_once(url, is_json))


def _sec_get_once(url, is_json=True):
    time.sleep(0.4)
    if is_json:
        r = requests.get(url, headers=UA, timeout=60)
        r.raise_for_status()
        return r.json()
    r = requests.get(url, headers=UA, timeout=90, stream=True)
    r.raise_for_status()
    buf = b""
    for chunk in r.iter_content(65536):
        buf += chunk
        if len(buf) >= MAX_DOC_BYTES:
            break
    r.close()
    return buf.decode(r.encoding or "utf-8", errors="ignore")


def load_cik_map():
    data = sec_get("https://www.sec.gov/files/company_tickers.json")
    m = {}
    for v in data.values():
        m[v["ticker"].upper()] = int(v["cik_str"])
    return m


def strip_html(text):
    text = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", text,
                  flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    return re.sub(r"[ \t\xa0]+", " ", text)


CONTRACT_TEXT_PAT = re.compile(
    r"witnesseth|hereinafter|the parties hereto|hereby amended|"
    r"in witness whereof|shall mean|governing law|counterparts", re.I)


def looks_like_earnings(txt):
    """실적자료 내용 검증 (§29-D: 문서 선택 오류 방어).
    v8: 계약서 문구가 다수면 배제, 실적 보도자료 고유 표현을 요구."""
    t = txt.lower()
    has_rev = re.search(r"net (sales|revenue)|total revenue|revenues", t)
    has_period = re.search(
        r"(first|second|third|fourth) quarter|fiscal (year|20)|quarter ended|"
        r"three months ended|six months ended|nine months ended|year ended", t)
    has_fin = re.search(
        r"gross (profit|margin)|operating income|income statement|"
        r"balance sheet|earnings per share|diluted", t)
    if not (has_rev and has_period and has_fin):
        return False
    # 계약서/약정서 신호가 2종 이상이면 실적자료 아님
    if len(set(m.group(0).lower()
               for m in CONTRACT_TEXT_PAT.finditer(t))) >= 2:
        return False
    # 실적 보도자료 고유 표현 요구
    reports = re.search(
        r"reports? (first|second|third|fourth|full|fiscal)|"
        r"announces? (its )?(first|second|third|fourth|full|fiscal|financial)|"
        r"results for the|financial results|compared to the prior year|"
        r"increased \d|decreased \d|versus the prior|year-over-year", t)
    return bool(reports)


# v10: 투자자의 날·중기 목표·프로포마 합산표 — 숫자는 많지만 분기 실적 자료가 아님.
# 'pro forma'라는 단어만으로 거르면 딕스 실제 실적(본문에 풋락커 pro forma comp)까지 걸러지므로
# 파일명과 문서 앞부분(제목·첫 문단)만 본다.
NON_EARN_NAME_PAT = re.compile(
    r"investor.?day|capital.?markets?.?day|analyst.?day|pro.?forma", re.I)
HEAD_ZONE = 500                      # 제목 부근(정리한 본문 앞 500자)
NON_EARN_TITLE_PAT = re.compile(     # 제목 부근
    r"investor day|capital markets day|analyst day|"
    r"(long|mid|medium)[- ]term (financial )?(targets|framework|algorithm)", re.I)
# 프로포마 '문서'를 가리키는 표현(앞 3,000자). 실적 본문의 'pro forma comparable sales'·'pro forma combined basis'는 제외
PRO_FORMA_DOC_PAT = re.compile(
    r"pro forma (condensed |combined |consolidated )*(financial|statements?|balance sheets?|information)|"
    r"supplemental pro forma", re.I)
# 제목이 실적 발표면 통과(실적 보도자료 안의 '투자자의 날 예정'·프로포마 언급 보호).
# 명사 'Annual/Quarterly/Current Report (on Form …)'는 실적 발표 제목이 아님
EARN_HEAD_PAT = re.compile(
    r"(?<!annual )(?<!quarterly )(?<!current )"
    r"\b(reports?|announces?|posts?|delivers?)\b(?! on form)[^.]{0,80}?"
    r"\b(quarter|q[1-4]|year|fiscal|annual)\b[^.]{0,40}?\bresults\b", re.I)
# 분기 손익표 기간 문구 — 있으면 첫 문단의 '투자자의 날·중기 목표' 언급만으로 거르지 않음
QUARTER_STMT_PAT = re.compile(r"\b(three|3|thirteen|13)[- ](months|weeks) ended\b", re.I)


def non_earnings_reason(name, txt=None):
    """투자자의 날·프로포마 자료면 사유(한국어), 아니면 None. txt 없으면 파일명만 봄."""
    if NON_EARN_NAME_PAT.search(name or ""):
        return "투자자의 날·프로포마 자료(파일명)"
    if txt is None:
        return None
    front = re.sub(r"\s+", " ", txt[:20000]).strip()
    head = front[:HEAD_ZONE]
    if EARN_HEAD_PAT.search(head):
        return None
    if NON_EARN_TITLE_PAT.search(head) and not QUARTER_STMT_PAT.search(txt):
        return "투자자의 날·중기 목표 자료(문서 앞부분)"
    if PRO_FORMA_DOC_PAT.search(front[:3000]):
        return "프로포마 합산표(문서 앞부분)"
    return None


# 실적 첨부로 보이는 이름(우선 허용 — 계약서 패턴보다 우선)
EARNINGS_NAME_PAT = re.compile(r"ex.?99|press|earn|release|result|mda", re.I)
# 계약서·부속서류로 보이는 이름
CONTRACT_NAME_PAT = re.compile(
    r"ex-?10|agreement|amend|indenture|guarant|pledge|"
    r"\blease|employ|severance|incentive|equityplan|bylaw|charter|"
    r"consent|opinion|certif|merger|purchaseagr", re.I)


def _bad_name(n):
    """index 파일·XBRL 렌더 파일·계약서(EX-10) 계열 제외.
    단, 실적 첨부로 보이는 이름은 계약서 패턴보다 우선 허용."""
    ln = n.lower()
    if ("index" in ln) or re.fullmatch(r"r\d+\.html?", ln):
        return True
    if EARNINGS_NAME_PAT.search(ln):
        return False
    if CONTRACT_NAME_PAT.search(ln):
        return True
    return False


def _href_to_name(href, base):
    """href에서 파일명 추출. /ix?doc=/Archives/... 형태와 상대경로 모두 지원.
    해당 공시 폴더의 파일이 아니면 None."""
    h = href.strip()
    m = re.search(r"doc=(/Archives/[^&\"']+)", h, re.I)   # iXBRL 뷰어 링크 해제
    if m:
        h = m.group(1)
    if "/" not in h:                                      # 상대경로(파일명만)
        name = h
    else:
        if base.lower() not in h.lower():
            return None                                   # 다른 폴더/페이지 링크
        name = h.rstrip("/").split("/")[-1]
    name = name.split("?")[0].split("#")[0]
    if not name.lower().endswith((".htm", ".html")):
        return None
    return name


def list_filing_docs(cik, nod, primary):
    """공시 첨부 htm 목록 [(이름, 크기)] — 3중 소스로 수집.
    1) index.json  2) 공시 인덱스 페이지(-index.htm)  3) 디렉터리 목록"""
    base = f"/Archives/edgar/data/{cik}/{nod}/"
    names = []
    trouble = []   # v10: SEC 일시 오류(재시도 후에도) — 목록을 못 얻으면 '오류로 건너뜀'으로 셈
    listed_ok = False   # 출처 하나라도 정상 응답 = 첨부 없음이 확인된 것(오류로 건너뜀 아님)

    def _add(n, size=0):
        if (n and n != primary and not _bad_name(n)
                and all(n != x for x, _ in names)):
            names.append((n, size))

    # 1) index.json — 대체 경로가 둘 있어 재시도 없이 한 번만(v10: 5xx마다 4분 기다리던 것 제거)
    try:
        idx = sec_get(f"https://www.sec.gov{base}index.json", retry=False)
        listed_ok = True
        for it in idx.get("directory", {}).get("item", []):
            n = it["name"]
            if n.lower().endswith((".htm", ".html")):
                _add(n, int(it.get("size") or 0))
    except Exception as e:
        trouble.append(_is_transient(e))
        print(f"  [index.json 실패] {str(e)[:120]}")

    # 2) 공시 인덱스 페이지 (문서 표에 실제 첨부 링크가 있음) — 재시도는 -index.htm만(-index.html은 같은 쪽의 변형)
    if not names:
        acc_dash = f"{nod[:10]}-{nod[10:12]}-{nod[12:]}"
        for idx_url in (f"https://www.sec.gov{base}{acc_dash}-index.htm",
                        f"https://www.sec.gov{base}{acc_dash}-index.html"):
            try:
                page = sec_get(idx_url, is_json=False, retry=idx_url.endswith(".htm") and not listed_ok)
            except Exception as e:
                trouble.append(_is_transient(e))
                continue
            listed_ok = True
            for href in re.findall(r'href=[\"\']([^\"\']+)[\"\']', page, re.I):
                _add(_href_to_name(href, base))
            if names:
                break

    # 3) 디렉터리 목록 — 앞에서 일시 오류로 이미 기다렸으면 한 번만
    if not names:
        try:
            listing = sec_get(f"https://www.sec.gov{base}", is_json=False, retry=not (any(trouble) or listed_ok))
            listed_ok = True
            for href in re.findall(r'href=[\"\']([^\"\']+)[\"\']', listing, re.I):
                _add(_href_to_name(href, base))
        except Exception as e:
            trouble.append(_is_transient(e))
            print(f"  [디렉터리 목록 실패] {str(e)[:120]}")

    if not names and any(trouble) and not listed_ok:   # 모든 출처가 일시 오류일 때만 '오류로 건너뜀'
        _RETRY["sec"]["skipped"] += 1
    return names


def find_latest_filing(cik, skip=()):
    """최신 '실적' 공시 반환. 최근 8-K/6-K 15건 최신순, 첨부 3개까지 내용 검증.
    v10: skip = 지난번 투자자의 날·프로포마로 잘못 추출된 공시(accession) — 다시 고르지 않음.
    결과에 notices(내용 판정으로 건너뛴 더 새 공시)·skipped_bad(skip으로 건너뛴 공시)를 붙임."""
    sub = sec_get(f"https://data.sec.gov/submissions/CIK{cik:010d}.json")
    rec = sub["filings"]["recent"]
    forms = rec["form"]
    accs = rec["accessionNumber"]
    dates = rec["filingDate"]
    docs = rec["primaryDocument"]
    notices, skipped_bad = [], []

    def _done(found):
        found["notices"], found["skipped_bad"] = notices, skipped_bad
        return found

    checked = 0
    for i in range(len(forms)):
        if forms[i] not in ("8-K", "6-K"):
            continue
        checked += 1
        if checked > 15:
            break
        acc = accs[i]
        nod = acc.replace("-", "")
        try:
            names = list_filing_docs(cik, nod, docs[i])
            if not names:
                print(f"  - {forms[i]} {dates[i]}: 첨부 htm 없음, 건너뜀")
                continue
            print(f"  · {forms[i]} {dates[i]} 첨부 후보 {len(names)}건: "
                  f"{', '.join(n for n, _ in names[:4])}")
            # v10: 투자자의 날·프로포마 파일은 내려받지 않고 제외 → 없으면 이전 공시로
            nonearn = [n for n, _ in names if non_earnings_reason(n)]
            if nonearn:
                names = [nm for nm in names if nm[0] not in nonearn]
                print(f"  - {forms[i]} {dates[i]} {', '.join(nonearn[:3])}: "
                      f"투자자의 날·프로포마 자료(파일명), 건너뜀"
                      f"{'' if names else ' → 이전 공시로'}")
                if not names:
                    continue
            prio = [nm for nm in names
                    if re.search(r"ex.?99|press|earn|release|result",
                                 nm[0], re.I)]
            pool = prio if prio else names
            pool.sort(key=lambda nm: nm[1], reverse=True)
            found, trouble, bad = None, False, False
            for nm, _sz in pool[:4]:
                url = (f"https://www.sec.gov/Archives/edgar/data/{cik}/{nod}/"
                       f"{nm}")
                try:
                    txt = strip_html(sec_get(url, is_json=False))
                except Exception as e:
                    # 후보 1개 실패가 공시 전체를 버리지 않도록 격리
                    trouble = trouble or _is_transient(e)
                    print(f"  - {forms[i]} {dates[i]} {nm}: "
                          f"내려받기 실패({str(e)[:160]}), 다음 첨부로")
                    continue
                if len(txt) < 1500:
                    print(f"  - {forms[i]} {dates[i]} {nm}: "
                          f"본문 짧음({len(txt)}자)")
                    continue
                if not looks_like_earnings(txt):
                    print(f"  - {forms[i]} {dates[i]} {nm}: "
                          f"실적자료 아님(내용 검증 불통과), 건너뜀")
                    continue
                why = non_earnings_reason(nm, txt)
                if why:
                    print(f"  - {forms[i]} {dates[i]} {nm}: {why}, 건너뜀")
                    notices.append((dates[i], why))
                    continue
                if acc in skip:   # 내용 판정은 통과했지만 지난번 이 공시에서 프로포마·목표 기간이 추출됨
                    print(f"  - {forms[i]} {dates[i]} {nm}: 지난번 투자자의 날·프로포마로 추출된 공시, "
                          f"건너뜀 → 이전 공시로")
                    skipped_bad.append((acc, f"{forms[i]} {dates[i]} {nm}"))
                    bad = True
                    break
                found = {"accession": acc, "text": txt, "url": url,
                         "date": dates[i],
                         "source": f"{forms[i]} {dates[i]} {nm}"}
                break
            if found:
                return _done(found)
            if trouble and not bad:   # 첨부를 SEC 오류로 못 읽어 이 공시를 건너뜀
                _RETRY["sec"]["skipped"] += 1
        except Exception as e:
            if _is_transient(e):
                _RETRY["sec"]["skipped"] += 1
            print(f"  - {forms[i]} {dates[i]}: 공시 목록 오류로 건너뜀: "
                  f"{str(e)[:200]}")
            continue

    for i in range(len(forms)):
        if forms[i] in ("10-Q", "10-K", "20-F"):
            acc = accs[i]
            nod = acc.replace("-", "")
            url = (f"https://www.sec.gov/Archives/edgar/data/{cik}/{nod}/"
                   f"{docs[i]}")
            txt = strip_html(sec_get(url, is_json=False))
            return _done({"accession": acc, "text": txt, "url": url,
                          "date": dates[i], "source": f"{forms[i]} {dates[i]}"})
    return None


def cap_text(txt):
    if len(txt) <= 160000:
        return txt
    return txt[:30000] + "\n...(중략)...\n" + txt[-130000:]


def claude_extract(ticker, name, doc_text):
    dks_extra = ""
    if ticker == "DKS":
        dks_extra = """
  "sub_segments": [
    {"name": "DICK'S", "revenue": number|null, "prev_revenue": number|null,
     "yoy_pct": number|null, "segment_profit": number|null,
     "inventory": number|null},
    {"name": "Foot Locker", "revenue": number|null, "prev_revenue": number|null,
     "yoy_pct": number|null, "segment_profit": number|null,
     "inventory": number|null, "proforma_comp_pct": number|null}
  ],"""
    prompt = f"""You are a financial data extractor. The following is text from the latest
SEC earnings-related filing of {name} ({ticker}).

Extract ONLY figures that are EXPLICITLY stated in the document. Never compute,
estimate, or infer missing values — use null instead. Revenue figures in
MILLIONS of the reporting currency. yoy_pct = year-over-year growth in percent
for the most recent quarter (or fiscal year if only annual data is present).
prev_revenue = the PRIOR-YEAR comparative figure for the same period, ONLY if
it is explicitly stated in a comparative table or the text; otherwise null.

Respond with ONLY a JSON object, no markdown fences, no commentary:
{{
  "period": "string describing the reported period, e.g. 'Q1 FY26 ended 2026-08-31'",
  "prev_period": "string describing the prior-year comparative period, or null",
  "currency": "USD/CHF/etc or null",
  "regions": [
    {{"name": "North America|EMEA|Greater China|Asia Pacific|etc",
      "revenue": number|null, "prev_revenue": number|null, "yoy_pct": number|null}}
  ],
  "channels": [
    {{"name": "DTC|Wholesale|etc",
      "revenue": number|null, "prev_revenue": number|null, "yoy_pct": number|null}}
  ],{dks_extra}
  "mgmt_notes": [
    {{"topic": "inventory|discount|channel",
      "quote": "one sentence copied VERBATIM from the document",
      "ko": "그 문장의 한국어 한 줄 요약(60자 이내)"}}
  ],
  "notes": "one short sentence in Korean about data caveats, or null"
}}
mgmt_notes: up to 3 sentences where management describes inventory levels or clearance
(topic "inventory"), markdowns / promotions / discounting / gross margin pressure from
promotions (topic "discount"), or off-price / liquidation channels, wholesale or account
reductions, distribution or supply control (topic "channel"). Copy each quote EXACTLY as
written (same words and punctuation, no ellipsis, no paraphrase). Prefer explicit or
forward-looking statements. If there are none, use an empty list.
If the document contains no regional breakdown, use an empty list for regions.
Same for channels. If the document is not an earnings report at all, return
{{"period": null, "prev_period": null, "currency": null, "regions": [],
"channels": [], "notes": "실적 문서 아님"}}

DOCUMENT:
{cap_text(doc_text)}"""

    data = anthropic_post({"model": "claude-sonnet-4-6",
              "max_tokens": 3000,
              "messages": [{"role": "user", "content": prompt}]}, timeout=180)
    parts = data.get("content", [])
    text = "".join(p.get("text", "") for p in parts if p.get("type") == "text")
    text = re.sub(r"```json|```", "", text).strip()
    obj = json.loads(text)
    obj["schema_v"] = SCHEMA_V
    obj["mgmt_notes"] = verify_quotes(obj.get("mgmt_notes"), doc_text, ticker)
    return obj


MGMT_TOPICS = ("inventory", "discount", "channel")


def _norm_q(s):
    """원문 대조용: 따옴표·대시·공백·대소문자 차이를 없앰"""
    s = str(s or "").replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", '"').replace("\u201d", '"')
    s = s.replace("\u2013", "-").replace("\u2014", "-").replace("\xa0", " ")
    return re.sub(r"\s+", " ", s).strip().lower()


def verify_quotes(notes, doc_text, label=""):
    """v11 본사 발언 — 원문에 글자 그대로 있는 문장만 남김(요약·지어낸 문장 차단), 최대 3개"""
    if not isinstance(notes, list):
        return []
    body = _norm_q(doc_text)
    out, dropped = [], 0
    for n in notes:
        if not isinstance(n, dict):
            continue
        q, topic = str(n.get("quote") or "").strip(), n.get("topic")
        if topic not in MGMT_TOPICS or len(q) < 30 or _norm_q(q) not in body:
            dropped += 1
            continue
        out.append({"topic": topic, "quote": q[:400], "ko": str(n.get("ko") or "").strip()[:80]})
        if len(out) == 3:
            break
    print(f"  {label} 본사 발언 {len(out)}건" + (f"(원문에 없는 문장 {dropped}건 버림)" if dropped else ""), flush=True)
    return out


# ── v10: 이전 값 유지 판단 ──
def _has_data(ex):
    """지역·채널·하위부문 중 하나라도 있으면 '분해 있음'"""
    return bool(ex and (ex.get("regions") or ex.get("channels")
                        or ex.get("sub_segments")))


def _filed(source):
    """'8-K 2026-08-25 xxx.htm' → '2026-08-25'"""
    m = re.search(r"\b(\d{4}-\d{2}-\d{2})\b", source or "")
    return m.group(1) if m else None


def _cik_from_url(url):
    """저장된 공시 주소에서 CIK(company_tickers.json 실패 대비)"""
    m = re.search(r"/edgar/data/(\d+)/", url or "")
    return int(m.group(1)) if m else None


BAD_EXTRACT_PAT = re.compile(r"investor.?day|capital.?markets?.?day|pro.?forma|targets", re.I)


def _is_bad_extract(source, ex):
    """투자자의 날·프로포마에서 뽑은 값인지(온 9/22·딕스 9/21) — 파일명·추출 기간 문구로 판단"""
    return bool(BAD_EXTRACT_PAT.search(f"{source or ''} {(ex or {}).get('period') or ''}"))


def _prev_is_earnings(prev):
    """저장된 이전 값이 '분해가 있는 실적 자료' 추출인지(투자자의 날·프로포마에서 뽑은 값은 지킬 값이 아님)"""
    px = prev.get("extract")
    return _has_data(px) and not _is_bad_extract(prev.get("source"), px)


def _tried(acc, source, reason):
    """다시 Claude에 보내지 않을 공시 기록(분해 없음·실적 자료 아님) — 사유도 함께 저장"""
    return {"accession": acc, "source": source, "schema_v": SCHEMA_V, "reason": reason}


def _tried_reason(tried):
    """기록된 공시의 사유 — 그 공시가 화면 값보다 새로운 동안 kept_reason으로 씀(지난주 실패 사유를 이어 쓰지 않음)"""
    return (tried.get("reason") or
            f"새 공시({_filed(tried.get('source')) or tried.get('source')})에 분해 없음 — 이전 실적 추출 유지")


def _keep(prev, why):
    """이전 추출을 그대로 둠 — accession도 이전 것(히스토리에 같은 값이 새 점으로 안 쌓임)"""
    e = {k: prev.get(k) for k in ("accession", "source", "url", "extract")}
    e["error"] = None
    e["kept_reason"] = why
    if prev.get("tried_empty"):
        e["tried_empty"] = prev["tried_empty"]
    return e


def process_ticker(t, prev, cik_map):
    """한 종목 → (저장할 항목, 상태). 상태: new(새 추출)·cache·kept(이전 값 유지)·failed(실패)"""
    skipped0 = _RETRY["sec"]["skipped"]

    def fail(msg, why, base=None):
        print(f"[WARN] {t}: {msg}")
        if prev.get("extract") is not None:
            print(f"  → 이전 추출 유지 ({prev.get('source')})")
            e = _keep(prev, f"{why} — 이전 추출 유지")
            e["kept_failed"] = True   # 수집 상태 '일부 실패' 집계용(문구가 아니라 이 표시·최상위 failed로 셈)
            return e, "failed"
        e = base or {"accession": None, "source": None, "url": None, "extract": None}
        e["error"] = msg[:200]
        return e, "failed"

    # 실행 시간 상한·SEC 전면 장애 → 호출 없이 이전 값 유지(워크플로우 30분 제한 보호)
    _NOW["ticker"] = t
    blocked = _blocked("sec")
    if blocked:
        return fail(f"{blocked} — 이번 실행에서 SEC 호출 생략",
                    "SEC 접속 실패" if "SEC" in blocked else "시간 부족으로 수집 실패")
    px = prev.get("extract") or {}
    # 저장된 값이 투자자의 날·프로포마 추출이면 그 공시는 다시 고르지 않음(내용 판정이 놓쳐도 바로잡힘)
    skip = ({prev["accession"]} if prev.get("accession") and prev.get("extract") is not None
            and _is_bad_extract(prev.get("source"), px) else set())
    try:
        cik = cik_map.get(t) or _cik_from_url(prev.get("url"))
        if not cik:
            return fail("CIK 미확인", "CIK 미확인")
        print(f"{t}: 공시 탐색 중 ...")
        filing = find_latest_filing(cik, skip)
    except Exception as e:
        return fail(f"SEC 접속 실패: {e}", "SEC 접속 실패")
    if not filing:
        return fail("실적 공시 미발견", "실적 공시 미발견")
    sec_trouble = _RETRY["sec"]["skipped"] > skipped0   # SEC 오류로 더 새 공시·첨부를 건너뜀
    entry = {"accession": filing["accession"], "source": filing["source"],
             "url": filing["url"], "extract": None, "error": None}
    tried = prev.get("tried_empty") or {}
    same = prev.get("accession") == filing["accession"] and px.get("schema_v") == SCHEMA_V
    same_tried = (tried.get("accession") == filing["accession"]
                  and tried.get("schema_v") == SCHEMA_V and prev.get("extract"))
    pf, nf = _filed(prev.get("source")), filing.get("date") or _filed(filing["source"])
    older = bool(pf and nf and nf < pf)
    # SEC 오류로 더 새 공시를 못 읽었을 수 있음 → 같은 공시·더 오래된 공시면 Claude 부르지 않고 실패로 셈
    # (이전 값이 실적이든 아니든. 이전 값이 없을 때만 찾은 공시로 추출)
    if sec_trouble and prev.get("extract") is not None and (same or same_tried or older):
        return fail(f"SEC 오류로 일부 공시를 못 읽음 — 찾은 공시 {filing['source']}", "SEC 접속 실패")
    # 내용 판정(제목·앞부분)으로 건너뛴 더 새 공시 → 화면에서 보이게 안내(판정이 틀렸을 때 조용히 멈추지 않게)
    notice = None
    if filing.get("notices"):
        d, why = filing["notices"][0]
        notice = f"최신 공시({d})를 {why.replace('(문서 앞부분)', '')}로 보고 건너뜀 — 확인 필요"
        print(f"[WARN] {t}: {notice}")

    # ① 같은 공시·같은 스키마 → 캐시(분해 없음 결과도 캐시 — 매주 같은 공시를 Claude에 다시 보내지 않음)
    if same:
        entry["extract"] = px
        print(f"{t}: 동일 공시({filing['accession']}) → 캐시 사용"
              f"{'' if _has_data(px) else '(분해 없음)'}")
        if tried and (_filed(tried.get("source")) or "") > (nf or ""):
            entry["tried_empty"] = tried   # 더 새 공시 기록은 이어 감(첨부가 다시 보여도 재호출 안 함)
            entry["kept_reason"] = _tried_reason(tried)
        elif notice:
            entry["kept_reason"] = notice
        return entry, "cache"
    # ② 지난번에 '분해 없음·실적 자료 아님'으로 확인한 공시 → 다시 보내지 않고 이전 실적 추출 유지
    if same_tried:
        print(f"{t}: 동일 공시({filing['accession']}) 지난번 확인(분해 없음·실적 자료 아님) → 이전 추출 유지")
        return _keep(prev, _tried_reason(tried)), "kept"
    # ③ 찾은 공시가 저장된 실적 공시보다 오래됨(최신 첨부가 없거나 내용 판정으로 건너뜀) → 이전 추출 유지
    if older and _prev_is_earnings(prev):
        print(f"[WARN] {t}: 찾은 공시({filing['source']})가 저장된 공시({pf})보다 오래됨 → 이전 추출 유지")
        return _keep(prev, notice or "최신 공시를 못 읽음 — 이전 추출 유지"), "kept"
    # ④ 새 추출
    print(f"{t}: 신규 공시 추출 중 ... ({filing['source']})")
    try:
        ex = claude_extract(t, t, filing["text"])
    except Exception as e:
        return fail(f"추출 실패: {e}", "Claude 추출 실패", base=entry)
    d_new = _filed(filing["source"]) or filing["source"]
    if _is_bad_extract(filing["source"], ex) and _prev_is_earnings(prev):
        why = f"새 공시({d_new})는 투자자의 날·프로포마 자료 — 그 전 실적 공시 기준"
        print(f"[WARN] {t}: 추출 기간 '{ex.get('period')}' — 실적 자료 아님 → 이전 추출 유지 ({prev.get('source')})")
        kept = _keep(prev, why)
        kept["tried_empty"] = _tried(filing["accession"], filing["source"], why)
        return kept, "kept"
    if not _has_data(ex) and _prev_is_earnings(prev):
        print(f"{t}: 새 공시에 지역·채널·부문 분해 없음 → 이전 추출 유지 ({prev.get('source')})")
        why = f"새 공시({d_new})에 분해 없음 — 이전 실적 추출 유지"
        kept = _keep(prev, why)
        kept["tried_empty"] = _tried(filing["accession"], filing["source"], why)
        return kept, "kept"
    entry["extract"] = ex
    if not _has_data(ex):
        print(f"{t}: 분해 없음 — 이 공시 기준으로 캐시(다음 주 재추출 안 함)")
    for acc, src in filing.get("skipped_bad") or []:   # 건너뛴 잘못된 공시 — 다음 주 다시 보내지 않게 기록
        why = f"새 공시({_filed(src) or src})는 투자자의 날·프로포마 자료 — 그 전 실적 공시 기준"
        entry["tried_empty"] = _tried(acc, src, why)
        entry["kept_reason"] = why
        break
    if notice and not entry.get("kept_reason"):
        entry["kept_reason"] = notice
    return entry, "new"


def main():
    if not API_KEY:
        print("[ERROR] ANTHROPIC_API_KEY 미설정")
        raise SystemExit(1)

    old = {"items": {}}
    if os.path.exists(SEG_PATH):
        try:
            with open(SEG_PATH, encoding="utf-8") as f:
                old = json.load(f)
        except Exception:
            pass
    old_items = old.get("items", {})

    out = {"generated_at":
           datetime.datetime.now(KST).strftime("%Y-%m-%d %H:%M KST"),
           "items": {}}

    for t, reason in NON_US.items():
        out["items"][t] = {"error": reason, "extract": None}

    try:
        cik_map = load_cik_map()
    except Exception as e:   # 저장된 공시 주소의 CIK로 대신 진행
        print(f"[WARN] company_tickers.json 실패 — 저장된 CIK로 진행: {str(e)[:160]}")
        cik_map = {}

    only = [x.strip() for x in os.environ.get("SEG_ONLY", "").split(",") if x.strip()]
    if only:    # v11 시험 모드: 지정 종목만 새로 추출해 결과를 로그로 보고 저장하지 않음
        print(f"[시험 모드] SEG_ONLY={','.join(only)} — 저장하지 않음")
        for t in only:
            prev = dict(old_items.get(t) or {})
            if prev.get("extract"):      # 같은 공시라도 다시 추출되게(캐시 무시)
                prev["extract"] = dict(prev["extract"], schema_v=-1)
            entry, st = process_ticker(t, prev, cik_map)
            ex = entry.get("extract") or {}
            print(f"[{t}] {st} · {entry.get('source')} · {ex.get('period')} · 지역 {len(ex.get('regions') or [])} · 채널 {len(ex.get('channels') or [])}")
            for n in ex.get("mgmt_notes") or []:
                print(f"    [{n['topic']}] {n['ko']} — \"{n['quote'][:200]}\"")
        return

    stat = {}
    for t in US_TICKERS:
        prev = old_items.get(t) or {}
        entry, st = process_ticker(t, prev, cik_map)
        out["items"][t] = entry
        stat[t] = st

    failed = [t for t in US_TICKERS if stat[t] == "failed"]
    if failed:
        out["failed"] = failed   # 수집 상태 화면 '일부 실패 n곳(이전 값)'
    if len(failed) == len(US_TICKERS):   # 새로 받은 게 없음 → 갱신일을 옮기지 않아 '지연' 경고가 뜨게
        out["generated_at"] = old.get("generated_at") or out["generated_at"]

    os.makedirs("docs", exist_ok=True)
    with open(SEG_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("saved", SEG_PATH)
    cnt = {k: sum(1 for v in stat.values() if v == k)
           for k in ("new", "cache", "kept", "failed")}
    print(f"추출 결과: 새 추출 {cnt['new']} · 캐시 {cnt['cache']} · "
          f"이전 값 유지 {cnt['kept']} · 실패 {cnt['failed']}")
    if failed:
        print(f"  [ERROR] 수집 실패 {len(failed)}곳(이전 값 유지): {', '.join(failed)}")
    if len(failed) * 2 > len(US_TICKERS):
        soft_fail(f"미국 공시 {len(failed)}/{len(US_TICKERS)}곳 수집 실패 — 이전 추출 유지")


if __name__ == "__main__":
    main()

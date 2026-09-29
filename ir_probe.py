# -*- coding: utf-8 -*-
"""
sports-industry-monitor — Phase 7-A 사전 검증: 아디다스·푸마 IR 프로브 (1회용)
① 두 IR 사이트가 GitHub Actions에서 접속되는지(봇 차단 여부·상태코드)
② 최신 실적 자료의 URL을 목록 페이지에서 규칙적으로 찾을 수 있는지
   - 아디다스: 보도자료(HTML) + 재무자료 페이지의 Fact Sheet PDF
   - 푸마: 투자자 뉴스(HTML 보도자료)
③ 텍스트 추출 표본: 지역(Europe/North America/Greater China/Japan/South Korea/EMEA/Asia-Pacific)
   ·채널(Wholesale/DTC) 문장이 잡히는지
Claude 호출 없음(비용 0). 로그를 Claude에게 전달 → 본 코드 설계.
"""

import re
import io
import requests

UA = {"User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                     "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"),
      "Accept-Language": "en-US,en;q=0.9"}

ADI_PR_LIST = "https://www.adidas-group.com/en/media/press-releases?year=2026"
ADI_FIN = "https://www.adidas-group.com/en/investors/financial-reports"
PUMA_NEWS = "https://about.puma.com/en/investor-relations/financial-news"

REGION_WORDS = ["Europe", "North America", "Greater China", "Emerging Markets", "Latin America",
                "Japan/South Korea", "Japan", "South Korea", "EMEA", "Asia/Pacific", "Asia-Pacific",
                "Americas", "Wholesale", "Direct-to-Consumer", "DTC"]


def log(m):
    print(m, flush=True)


def fetch(url, as_bytes=False, timeout=60):
    r = requests.get(url, headers=UA, timeout=timeout, allow_redirects=True)
    log(f"  GET {url} → {r.status_code} {r.headers.get('content-type','')[:40]} {len(r.content):,}B")
    r.raise_for_status()
    return r.content if as_bytes else r.text


def strip_html(html):
    html = re.sub(r"<script.*?</script>|<style.*?</style>", " ", html, flags=re.S | re.I)
    txt = re.sub(r"<[^>]+>", " ", html)
    txt = re.sub(r"&nbsp;|&#160;", " ", txt)
    txt = re.sub(r"&amp;", "&", txt)
    return re.sub(r"\s+", " ", txt)


def links(html, base):
    out = []
    for m in re.finditer(r'href="([^"]+)"', html):
        u = m.group(1)
        if u.startswith("/"):
            u = base + u
        out.append(u)
    return out


def show_regions(txt, label, width=220):
    log(f"  [{label}] 텍스트 {len(txt):,}자")
    for w in REGION_WORDS:
        i = txt.find(w)
        if i >= 0:
            log(f"    · '{w}' @{i}: …{txt[max(0, i-60):i+width].strip()}…")
        else:
            log(f"    · '{w}' 없음")


def pdf_text(raw):
    try:
        from pypdf import PdfReader
    except ImportError:
        return None, "pypdf 미설치"
    rd = PdfReader(io.BytesIO(raw))
    pages = [(p.extract_text() or "") for p in rd.pages]
    return pages, f"{len(pages)}쪽"


def probe_adidas():
    log("\n===== adidas — 보도자료 목록 =====")
    try:
        html = fetch(ADI_PR_LIST)
    except Exception as e:
        log(f"  실패: {str(e)[:150]}"); return
    cands = [u for u in links(html, "https://www.adidas-group.com")
             if "/press-releases/" in u and re.search(r"quarter|results|half|record|revenue|sales", u, re.I)]
    cands = list(dict.fromkeys(cands))
    log(f"  실적 보도자료 후보 {len(cands)}건:")
    for u in cands[:8]:
        log(f"    - {u}")
    if cands:
        try:
            pr = strip_html(fetch(cands[0]))
            show_regions(pr, "adidas 보도자료(최신)")
        except Exception as e:
            log(f"  보도자료 본문 실패: {str(e)[:150]}")

    log("\n===== adidas — 재무자료 페이지(Fact Sheet PDF) =====")
    try:
        html = fetch(ADI_FIN)
    except Exception as e:
        log(f"  실패: {str(e)[:150]}"); return
    pdfs = [u for u in links(html, "https://www.adidas-group.com") if u.lower().endswith(".pdf")]
    pdfs = list(dict.fromkeys(pdfs))
    log(f"  PDF 링크 {len(pdfs)}건 — 이름에 fact/sheet/quarter/Q 포함:")
    fact = [u for u in pdfs if re.search(r"fact|sheet", u, re.I)]
    for u in (fact or pdfs)[:10]:
        log(f"    - {u}")
    if fact:
        try:
            raw = fetch(fact[0], as_bytes=True, timeout=120)
            pages, info = pdf_text(raw)
            if pages is None:
                log(f"  PDF 추출 불가: {info}"); return
            log(f"  Fact Sheet {info}")
            full = " ".join(pages)
            full = re.sub(r"\s+", " ", full)
            show_regions(full, "adidas Fact Sheet", width=320)
            i = full.find("Segment")
            log(f"    · 'Segment' 부근: …{full[max(0,i-100):i+700]}…" if i >= 0 else "    · 'Segment' 없음")
        except Exception as e:
            log(f"  Fact Sheet 실패: {str(e)[:150]}")


def probe_puma():
    log("\n===== PUMA — 투자자 뉴스 목록 =====")
    try:
        html = fetch(PUMA_NEWS)
    except Exception as e:
        log(f"  실패: {str(e)[:150]}"); return
    cands = [u for u in links(html, "https://about.puma.com")
             if "/newsroom/corporate-news/" in u and re.search(r"q[1-4]|quarter|half|result|year|outlook|sales", u, re.I)]
    cands = list(dict.fromkeys(cands))
    log(f"  실적 보도자료 후보 {len(cands)}건:")
    for u in cands[:8]:
        log(f"    - {u}")
    if cands:
        try:
            pr = strip_html(fetch(cands[0]))
            show_regions(pr, "PUMA 보도자료(최신)")
            m = re.search(r"EMEA.{0,200}?\(Q[1-4] 20\d\d: € [\d.,]+ million\)", pr)
            log(f"    · 지역 금액 문장 예: {m.group(0) if m else '패턴 미발견'}")
        except Exception as e:
            log(f"  보도자료 본문 실패: {str(e)[:150]}")


def main():
    log("IR 프로브 시작 — 로그 전체를 Claude에게 전달해주세요")
    probe_adidas()
    probe_puma()
    log("\nIR 프로브 완료")


if __name__ == "__main__":
    main()

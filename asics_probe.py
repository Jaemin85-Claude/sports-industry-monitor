# -*- coding: utf-8 -*-
"""
sports-industry-monitor — Phase 7-B 사전 검증: 아식스 IR 프로브 (1회용)
① corp.asics.com IR 라이브러리 접속 가능 여부
② 최신 실적 자료 PDF 링크 탐색 — (a) 결산단신 영문 'Summary of Consolidated Financial Statements'
   (b) 실적 설명자료 'Consolidated Financial Summary'
③ 각 PDF 텍스트에서 지역(Japan/North America/Europe/Greater China/Oceania/
   Southeast and South Asia/Other) 매출 표 형식 확인 — 분기(3개월) vs 누적(6개월) 구분
Claude 호출 없음(비용 0). 로그를 Claude에게 전달.
"""

import re
import io
import requests

UA = {"User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                     "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"),
      "Accept-Language": "en-US,en;q=0.9"}
PAGES = ["https://corp.asics.com/en/investor_relations/library/financial_summary",
         "https://corp.asics.com/en/investor_relations/library/financial_data",
         "https://corp.asics.com/en/investor_relations/library",
         "https://corp.asics.com/en/investor_relations"]
REGIONS = ["Japan", "North America", "Europe", "Greater China", "Oceania",
           "Southeast and South Asia", "Other", "Reportable Segment", "by region", "Net sales by"]


def log(m):
    print(m, flush=True)


def fetch(url, as_bytes=False, timeout=90):
    r = requests.get(url, headers=UA, timeout=timeout, allow_redirects=True)
    log(f"  GET {url} → {r.status_code} {r.headers.get('content-type','')[:30]} {len(r.content):,}B")
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
        out.append(u)
    return list(dict.fromkeys(out))


def pdf_pages(raw):
    from pypdf import PdfReader
    return [(p.extract_text() or "") for p in PdfReader(io.BytesIO(raw)).pages]


def show(txt, label, width=260):
    log(f"  [{label}] 텍스트 {len(txt):,}자")
    for w in REGIONS:
        idxs = [m.start() for m in re.finditer(re.escape(w), txt)][:3]
        if not idxs:
            log(f"    · '{w}' 없음"); continue
        for i in idxs[:2]:
            log(f"    · '{w}' @{i}: …{txt[max(0, i-80):i+width].strip()}…")


def main():
    log("ASICS IR 프로브 시작 — 로그 전체를 Claude에게 전달해주세요")
    pdfs = []
    for pg in PAGES:
        try:
            html = fetch(pg)
        except Exception as e:
            log(f"  실패: {str(e)[:120]}"); continue
        ls = links(html, "https://corp.asics.com")
        got = [u for u in ls if u.lower().endswith(".pdf") or "assets.asics.com" in u]
        log(f"  PDF/자산 링크 {len(got)}건")
        for u in got[:25]:
            log(f"    - {u}")
        pdfs += got
        # 링크 주변 텍스트(제목)도 함께 — 파일명이 숫자뿐인 경우 대비
        for m in re.finditer(r'<a[^>]+href="([^"]*assets\.asics\.com[^"]*)"[^>]*>(.*?)</a>', html, re.S):
            title = re.sub(r"<[^>]+>|\s+", " ", m.group(2)).strip()
            if title:
                log(f"    · 제목: {title[:90]} → {m.group(1)}")
    pdfs = list(dict.fromkeys(pdfs))
    # 표본: 'Summary'·'Financial' 이름 또는 상위 2개
    picks = [u for u in pdfs if re.search(r"summary|financial|result", u, re.I)][:2] or pdfs[:2]
    for u in picks:
        log(f"\n===== 표본 PDF: {u} =====")
        try:
            raw = fetch(u, as_bytes=True, timeout=120)
            pages = pdf_pages(raw)
            full = re.sub(r"\s+", " ", " ".join(pages))
            log(f"  {len(pages)}쪽")
            show(full, "본문")
        except Exception as e:
            log(f"  실패: {str(e)[:150]}")
    log("\nASICS IR 프로브 완료")


if __name__ == "__main__":
    main()

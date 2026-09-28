# -*- coding: utf-8 -*-
"""
sports-industry-monitor — Phase 6 사전 검증: DART 프로브 2차
2차 수정: ① 이름 정규화 버그 수정(글자 단위 삭제 → '주식회사/유한회사/(주)/(유)' 단어 단위)
② 후보 정렬: 정확일치 > 접두일치 > 포함, 동률이면 수정일 최신 ③ 1차에서 확인된 코드는 직접 지정
④ 공시 유형 필터 제거(전체) 후 보고서명으로 감사보고서/사업보고서 선별 ⑤ 상위 3후보 모두 검사
⑥ 원본파일 표본: 푸마코리아·데상트코리아(1차 확인 법인)
① corpCode.xml에서 13개 법인명 매칭 후보 출력 (동명·유사명 확인)
② 후보 법인의 최근 공시(외부감사관련 F 유형) 목록 — 최신 감사보고서 접수번호 확인
③ 구조화 재무 API(fnlttSinglAcnt) 가능 여부 — 외감 법인은 013 예상
④ 감사보고서 원본파일(document.xml) 다운로드 → zip 구성·텍스트 파싱 가능 여부(2개 법인 표본)
Claude 호출 없음(비용 0). 로그를 Claude에게 전달 → 본 코드 확정. (§검증 우선)
"""

import os
import io
import re
import json
import zipfile
import requests
import xml.etree.ElementTree as ET

API_KEY = os.environ.get("DART_API_KEY", "")
BASE = "https://opendart.fss.or.kr/api"
UA = {"User-Agent": "sports-industry-monitor dart probe"}

# 법인명 검색어 (id: [표시명, 검색어 후보])
TARGETS = {
    # id: [표시명, 검색어 후보, 직접 지정 corp_code 목록(1차에서 확인, 우선 검사)]
    "nike_kr":     ["나이키코리아", ["나이키코리아", "나이키"], ["01503133", "00125257"]],
    "adidas_kr":   ["아디다스코리아", ["아디다스코리아", "아디다스"], ["00148133"]],
    "asics_kr":    ["아식스코리아", ["아식스코리아", "아식스"], []],
    "puma_kr":     ["푸마코리아", ["푸마코리아"], ["01471250"]],
    "descente_kr": ["데상트코리아", ["데상트코리아"], ["00411154"]],
    "nb_eland":    ["이랜드월드", ["이랜드월드"], ["00207108", "00179407"]],
    "abcmart_kr":  ["에이비씨마트코리아", ["에이비씨마트코리아", "에이비씨마트", "ABC마트"], []],
    "shoemarker":  ["슈마커", ["슈마커코리아", "슈마커"], ["00396402"]],
    "musinsa":     ["무신사", ["무신사"], ["01137727"]],
    "k2_kr":       ["K2코리아", ["케이투코리아", "K2코리아"], ["01312832"]],
    "blackyak":    ["비와이엔블랙야크", ["비와이엔블랙야크", "블랙야크"], ["00520850", "01718407"]],
    "nepa":        ["네파", ["네파"], ["00932930"]],
    "shinsung":    ["신성통상", ["신성통상"], ["00136341"]],
}
SAMPLE_DOC_IDS = ["puma_kr", "descente_kr"]   # ④ 원본파일 표본 (1차 확인 법인)본


def log(msg):
    print(msg, flush=True)


def get(url, params, as_bytes=False, timeout=60):
    params = dict(params, crtfc_key=API_KEY)
    r = requests.get(url, params=params, headers=UA, timeout=timeout)
    r.raise_for_status()
    return r.content if as_bytes else r.json()


def load_corp_codes():
    """corpCode.xml(zip) → [(corp_code, corp_name, stock_code, modify_date)]"""
    raw = get(f"{BASE}/corpCode.xml", {}, as_bytes=True, timeout=120)
    if raw[:2] != b"PK":
        # zip이 아니면 오류 JSON일 가능성
        log(f"[corpCode] zip 아님: {raw[:200]!r}")
        return []
    z = zipfile.ZipFile(io.BytesIO(raw))
    name = [n for n in z.namelist() if n.lower().endswith(".xml")][0]
    root = ET.fromstring(z.read(name))
    rows = []
    for el in root.iter("list"):
        rows.append((
            (el.findtext("corp_code") or "").strip(),
            (el.findtext("corp_name") or "").strip(),
            (el.findtext("stock_code") or "").strip(),
            (el.findtext("modify_date") or "").strip(),
        ))
    log(f"[corpCode] 전체 법인 {len(rows):,}건 로드")
    return rows


def norm(s):
    s = s or ""
    s = re.sub(r"주식회사|유한회사|유한책임회사|\(주\)|\(유\)|㈜|\s+|[()（）]", "", s)
    return s


def find_candidates(rows, keywords, limit=10):
    """정확일치(0) > 접두일치(1) > 포함(2), 동률이면 수정일 최신순"""
    out = []
    for code, name, stock, mod in rows:
        n = norm(name)
        best = None
        for k in keywords:
            nk = norm(k)
            if n == nk:
                rank = 0
            elif n.startswith(nk):
                rank = 1
            elif nk in n:
                rank = 2
            else:
                continue
            best = rank if best is None else min(best, rank)
        if best is not None:
            out.append((best, code, name, stock, mod))
    out.sort(key=lambda r: (r[0], -int(r[4] or 0), r[2]))
    return [(c, n, s, m) for _, c, n, s, m in out[:limit]]


def list_filings(corp_code, years_back=3):
    """외부감사관련(F) 공시 목록 — 최신순"""
    import datetime
    bgn = (datetime.date.today().replace(year=datetime.date.today().year - years_back)).strftime("%Y%m%d")
    data = get(f"{BASE}/list.json", {
        "corp_code": corp_code, "bgn_de": bgn,
        "page_count": 100, "sort": "date", "sort_mth": "desc",
    })
    if data.get("status") != "000":
        return None, f"{data.get('status')} {data.get('message')}"
    allitems = data.get("list", [])
    items = [(it.get("rcept_no"), it.get("rcept_dt"), it.get("report_nm"),
              it.get("flr_nm")) for it in allitems
             if re.search(r"감사보고서|사업보고서", it.get("report_nm") or "")]
    return items, f"전체 {len(allitems)}건 중 감사/사업보고서 {len(items)}건"


def try_structured(corp_code, year):
    data = get(f"{BASE}/fnlttSinglAcnt.json", {
        "corp_code": corp_code, "bsns_year": str(year), "reprt_code": "11011",
    })
    st = data.get("status")
    if st == "000":
        accs = [(it.get("account_nm"), it.get("thstrm_amount"))
                for it in data.get("list", [])[:6]]
        return f"✅ 가능 — 표본 {accs}"
    return f"불가 ({st} {data.get('message')})"


def probe_document(rcept_no):
    raw = get(f"{BASE}/document.xml", {"rcept_no": rcept_no}, as_bytes=True, timeout=120)
    if raw[:2] != b"PK":
        return f"zip 아님: {raw[:200]!r}"
    z = zipfile.ZipFile(io.BytesIO(raw))
    names = [(n, z.getinfo(n).file_size) for n in z.namelist()]
    biggest = max(names, key=lambda x: x[1])
    content = z.read(biggest[0])
    for enc in ("utf-8", "euc-kr", "cp949"):
        try:
            txt = content.decode(enc)
            break
        except Exception:
            txt = None
    if txt is None:
        return f"구성 {names} / 디코딩 실패"
    plain = re.sub(r"<[^>]+>", " ", txt)
    plain = re.sub(r"\s+", " ", plain)
    # 손익계산서 핵심 계정 존재 여부
    hits = {k: (k in plain) for k in ["매출액", "영업이익", "당기순이익", "손익계산서", "포괄손익"]}
    idx = plain.find("손익계산서")
    sample = plain[idx:idx + 600] if idx >= 0 else plain[:600]
    return (f"구성 {names}\n    인코딩 {enc} · 텍스트 {len(plain):,}자 · 계정 존재 {hits}\n"
            f"    표본: {sample}")


def main():
    if not API_KEY:
        log("[ERROR] DART_API_KEY 미설정")
        raise SystemExit(1)
    log("DART 프로브 시작 — 로그 전체를 Claude에게 전달해주세요\n")

    rows = load_corp_codes()
    if not rows:
        raise SystemExit(1)

    picked = {}
    for tid, (label, kws, known) in TARGETS.items():
        log(f"===== [{tid}] {label} — 검색어 {kws} =====")
        cands = find_candidates(rows, kws)
        name_of = {c: n for c, n, _, _ in rows}
        # 검사 대상: 직접 지정 코드 → 검색 상위 3 (중복 제거)
        check = []
        for c in known + [c for c, _, _, _ in cands[:3]]:
            if c not in check:
                check.append(c)
        if cands:
            log("  검색 후보(최대 10): " + " | ".join(
                f"{n}[{c}{'·상장' + s if s else ''}·{m[:4]}]" for c, n, s, m in cands))
        else:
            log("  검색 후보 없음")
        for code in check[:4]:
            nm = name_of.get(code, "?")
            items, info = list_filings(code)
            if items is None:
                log(f"  ▸ {nm} [{code}] 공시목록: {info}")
                continue
            log(f"  ▸ {nm} [{code}] {info}")
            for rn, dt, rnm, flr in items[:6]:
                log(f"      - {dt} {rnm} rcept_no={rn} ({flr})")
            if items and tid not in picked:
                picked[tid] = (code, nm)
        st = try_structured(check[0], 2025) if check else "후보 없음"
        log(f"  구조화 API(2025, {check[0] if check else '-'}): {st}")
        log("")

    log("===== ④ 원본파일 파싱 표본 =====")
    for tid in SAMPLE_DOC_IDS:
        if tid not in picked:
            continue
        code, name = picked[tid][0], picked[tid][1]
        items, err = list_filings(code)
        if not items:
            log(f"[{name}] 표본 건너뜀 ({err or '공시 없음'})")
            continue
        # 별도 감사보고서 우선(연결 제외)
        audit = [it for it in items if "감사보고서" in (it[2] or "") and "연결" not in (it[2] or "")]
        target = audit[0] if audit else items[0]
        log(f"[{name}] {target[1]} {target[2]} rcept_no={target[0]}")
        try:
            log("  " + probe_document(target[0]))
        except Exception as e:
            log(f"  원본파일 오류: {str(e)[:200]}")
        log("")

    log("DART 프로브 완료")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
sports-industry-monitor — Phase 6 사전 검증: DART 프로브 (1회용)
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
    "nike_kr":     ["나이키코리아", ["나이키"]],
    "adidas_kr":   ["아디다스코리아", ["아디다스"]],
    "asics_kr":    ["아식스코리아", ["아식스"]],
    "puma_kr":     ["푸마코리아", ["푸마"]],
    "descente_kr": ["데상트코리아", ["데상트"]],
    "nb_eland":    ["이랜드월드", ["이랜드월드"]],
    "abcmart_kr":  ["에이비씨마트코리아", ["에이비씨마트", "ABC마트", "에이비씨"]],
    "shoemarker":  ["슈마커", ["슈마커"]],
    "musinsa":     ["무신사", ["무신사"]],
    "k2_kr":       ["K2코리아", ["케이투코리아", "K2코리아", "케이투"]],
    "blackyak":    ["비와이엔블랙야크", ["블랙야크"]],
    "nepa":        ["네파", ["네파"]],
    "shinsung":    ["신성통상", ["신성통상"]],
}
SAMPLE_DOC_IDS = ["nike_kr", "abcmart_kr"]   # ④ 원본파일 표본


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
    return re.sub(r"[\s()（）주식회사유한회사㈜]", "", s or "")


def find_candidates(rows, keywords, limit=8):
    out = []
    for code, name, stock, mod in rows:
        n = norm(name)
        if any(norm(k) in n for k in keywords):
            out.append((code, name, stock, mod))
    # 짧은 이름(정확 매칭에 가까운) 우선
    out.sort(key=lambda r: (len(r[1]), r[1]))
    return out[:limit]


def list_filings(corp_code, years_back=3):
    """외부감사관련(F) 공시 목록 — 최신순"""
    import datetime
    bgn = (datetime.date.today().replace(year=datetime.date.today().year - years_back)).strftime("%Y%m%d")
    data = get(f"{BASE}/list.json", {
        "corp_code": corp_code, "bgn_de": bgn, "pblntf_ty": "F",
        "page_count": 20, "sort": "date", "sort_mth": "desc",
    })
    if data.get("status") != "000":
        return None, f"{data.get('status')} {data.get('message')}"
    items = [(it.get("rcept_no"), it.get("rcept_dt"), it.get("report_nm"),
              it.get("flr_nm")) for it in data.get("list", [])]
    return items, None


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
    for tid, (label, kws) in TARGETS.items():
        log(f"===== [{tid}] {label} — 검색어 {kws} =====")
        cands = find_candidates(rows, kws)
        if not cands:
            log("  후보 없음")
            continue
        for code, name, stock, mod in cands:
            log(f"  · {name}  corp_code={code}  stock={stock or '-'}  수정일={mod}")
        picked[tid] = cands[0]
        code = cands[0][0]
        items, err = list_filings(code)
        if err:
            log(f"  공시목록 오류: {err}")
        elif not items:
            log("  최근 3년 외부감사관련 공시 없음")
        else:
            log(f"  최근 외부감사 공시 {len(items)}건(최신순, 최대 6):")
            for rn, dt, nm, flr in items[:6]:
                log(f"    - {dt} {nm} rcept_no={rn} ({flr})")
        log(f"  구조화 API(2025): {try_structured(code, 2025)}")
        log("")

    log("===== ④ 원본파일 파싱 표본 =====")
    for tid in SAMPLE_DOC_IDS:
        if tid not in picked:
            continue
        code, name = picked[tid][0], picked[tid][1]
        items, err = list_filings(code)
        if err or not items:
            log(f"[{name}] 표본 건너뜀 ({err or '공시 없음'})")
            continue
        audit = [it for it in items if "감사보고서" in (it[2] or "")]
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

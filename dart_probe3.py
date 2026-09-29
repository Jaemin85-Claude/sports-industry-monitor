# -*- coding: utf-8 -*-
"""
sports-industry-monitor — DART 재조사 프로브 (1회용): 아디다스코리아 · 슈마커코리아
1차·2차 프로브에서 공시가 잡히지 않은 두 법인의 실체를 확인한다.
① corpCode 전체에서 유사명 후보 전부(한글·영문·부분 일치, 최대 30)
② 각 후보의 기업개황(company.json): 정식명·영문명·주소·설립일·결산월·법인구분
③ 각 후보의 공시 목록(유형 무관, 2015년 이후 전체) — 최근 10건
④ 검색어를 넓혀 '아디다스' 이외 표기(ADIDAS KOREA, 아디다스코리아유한회사 등) 탐색
Claude 호출 없음(비용 0). 로그를 Claude에게 전달.
"""

import os
import io
import re
import zipfile
import requests
import xml.etree.ElementTree as ET

API_KEY = os.environ.get("DART_API_KEY", "")
BASE = "https://opendart.fss.or.kr/api"
UA = {"User-Agent": "sports-industry-monitor dart probe3"}

TARGETS = {
    "아디다스코리아": ["아디다스", "adidas", "ADIDAS", "아디다스코리아", "아디다스 코리아"],
    "슈마커코리아":  ["슈마커", "SHOEMARKER", "shoemarker", "슈마카", "슈마커코리아"],
}
KNOWN = {"아디다스코리아": ["00148133"], "슈마커코리아": ["00396402"]}


def log(msg):
    print(msg, flush=True)


def get(url, params, as_bytes=False, timeout=60):
    params = dict(params, crtfc_key=API_KEY)
    r = requests.get(url, params=params, headers=UA, timeout=timeout)
    r.raise_for_status()
    return r.content if as_bytes else r.json()


def norm(s):
    return re.sub(r"주식회사|유한회사|유한책임회사|\(주\)|\(유\)|㈜|\s+|[()（）]", "", (s or "")).lower()


def load_corp_codes():
    raw = get(f"{BASE}/corpCode.xml", {}, as_bytes=True, timeout=180)
    z = zipfile.ZipFile(io.BytesIO(raw))
    name = [n for n in z.namelist() if n.lower().endswith(".xml")][0]
    root = ET.fromstring(z.read(name))
    rows = []
    for el in root.iter("list"):
        rows.append(((el.findtext("corp_code") or "").strip(), (el.findtext("corp_name") or "").strip(),
                     (el.findtext("corp_eng_name") or "").strip(), (el.findtext("stock_code") or "").strip(),
                     (el.findtext("modify_date") or "").strip()))
    log(f"[corpCode] {len(rows):,}건 · 영문명 필드 {'있음' if any(r[2] for r in rows[:2000]) else '없음(구버전)'}")
    return rows


def company(code):
    d = get(f"{BASE}/company.json", {"corp_code": code})
    if d.get("status") != "000":
        return f"기업개황 없음 ({d.get('status')} {d.get('message')})"
    keys = ["corp_name", "corp_name_eng", "stock_name", "corp_cls", "jurir_no", "bizr_no",
            "adres", "est_dt", "acc_mt", "ceo_nm", "induty_code"]
    return " · ".join(f"{k}={d.get(k)}" for k in keys if d.get(k))


def filings(code):
    d = get(f"{BASE}/list.json", {"corp_code": code, "bgn_de": "20150101", "end_de": "20261231",
                                  "page_count": 100, "sort": "date", "sort_mth": "desc"})
    if d.get("status") != "000":
        return None, f"{d.get('status')} {d.get('message')}"
    items = d.get("list", [])
    return items, f"2015년 이후 공시 {len(items)}건"


def main():
    if not API_KEY:
        log("[ERROR] DART_API_KEY 미설정")
        raise SystemExit(1)
    rows = load_corp_codes()
    for label, kws in TARGETS.items():
        log(f"\n===== {label} — 검색어 {kws} =====")
        nk = [norm(k) for k in kws]
        cands = [r for r in rows if any(k in norm(r[1]) or (r[2] and k in norm(r[2])) for k in nk)]
        cands.sort(key=lambda r: -int(r[4] or 0))
        codes = list(dict.fromkeys(KNOWN.get(label, []) + [c[0] for c in cands[:30]]))
        log(f"  후보 {len(cands)}건(최근 수정 순, 최대 30):")
        for c in cands[:30]:
            log(f"   · {c[1]}{' / ' + c[2] if c[2] else ''}  corp={c[0]}  stock={c[3] or '-'}  수정={c[4]}")
        for code in codes[:8]:
            log(f"  ▸ [{code}] {company(code)}")
            items, info = filings(code)
            if items is None:
                log(f"      공시목록: {info}")
                continue
            log(f"      {info}")
            for it in items[:10]:
                log(f"        - {it.get('rcept_dt')} {it.get('report_nm')} ({it.get('flr_nm')}) rcept={it.get('rcept_no')}")
    log("\n재조사 프로브 완료")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
sports-industry-monitor — Phase 5 사전 검증: KOSIS 프로브 (1회용)
목적: 통계표 ID를 추측으로 코드에 박지 않고, 실제 API 응답으로
      ① 키워드 검색 결과(orgId/tblId/표명) ② 후보 표의 최근 데이터 구조를
      로그로 확인한 뒤 본 코드를 확정한다. (§검증 우선 원칙)
실행: GitHub Actions 수동 1회 → 로그 전체를 Claude에게 전달
"""

import os
import json
import requests

API_KEY = os.environ.get("KOSIS_API_KEY", "")
UA = {"User-Agent": "sports-industry-monitor kosis probe"}

SEARCH_KEYWORDS = ["소매판매액지수", "온라인쇼핑 상품군", "소비자물가지수 지출목적"]

# 후보 표 (프로브가 실제 응답으로 검증 — 확정 아님)
CANDIDATES = [
    ("101", "DT_1KE10071", "소매판매액지수(상품군별) 후보1"),
    ("101", "DT_1K31013",  "소매판매액지수 후보2"),
    ("101", "DT_1KE10051", "온라인쇼핑 상품군별 거래액 후보1"),
    ("101", "DT_1KE10081", "온라인쇼핑 후보2"),
    ("101", "DT_1J20112",  "소비자물가지수(지출목적별) 후보1"),
    ("101", "DT_1J20003",  "소비자물가지수 후보2"),
]


def show(title, obj, limit=2500):
    txt = json.dumps(obj, ensure_ascii=False)[:limit] if not isinstance(obj, str) else obj[:limit]
    print(f"\n===== {title} =====\n{txt}\n")


def probe_search():
    """통합검색 API — 엔드포인트 변형 2종 시도"""
    for kw in SEARCH_KEYWORDS:
        ok = False
        for url in (
            "https://kosis.kr/openapi/statisticsSearch.do",
            "https://kosis.kr/openapi/statisticsList.do",
        ):
            try:
                r = requests.get(url, params={
                    "method": "getList", "apiKey": API_KEY,
                    "searchNm": kw, "format": "json", "jsonVD": "Y",
                    "startCount": 1, "resultCount": 8,
                }, headers=UA, timeout=30)
                body = r.text.strip()
                if r.status_code == 200 and body and body != "[]":
                    try:
                        data = r.json()
                    except Exception:
                        show(f"검색[{kw}] {url} → JSON 아님", body, 800)
                        continue
                    # 표 목록이면 orgId/tblId/표명만 추려서 출력
                    rows = data if isinstance(data, list) else [data]
                    slim = []
                    for row in rows[:8]:
                        if isinstance(row, dict):
                            slim.append({k: row.get(k) for k in
                                         ("ORG_ID", "TBL_ID", "TBL_NM",
                                          "STAT_NM", "VW_NM", "err", "errMsg")
                                         if k in row})
                    show(f"검색[{kw}] {url}", slim)
                    ok = True
                    break
                else:
                    show(f"검색[{kw}] {url} → status {r.status_code}", body, 500)
            except Exception as e:
                print(f"검색[{kw}] {url} 실패: {str(e)[:150]}")
        if not ok:
            print(f"[참고] '{kw}' 검색은 두 엔드포인트 모두 유효 응답 없음")


def probe_data():
    """후보 표의 최근 월 데이터 구조 확인 (항목/분류 코드가 로그에 찍힘)"""
    url = "https://kosis.kr/openapi/Param/statisticsParameterData.do"
    for org, tbl, label in CANDIDATES:
        try:
            r = requests.get(url, params={
                "method": "getList", "apiKey": API_KEY,
                "orgId": org, "tblId": tbl,
                "itmId": "ALL", "objL1": "ALL",
                "prdSe": "M", "newEstPrdCnt": "2",
                "format": "json", "jsonVD": "Y",
            }, headers=UA, timeout=40)
            body = r.text.strip()
            try:
                data = r.json()
            except Exception:
                show(f"[{label}] {org}/{tbl} → JSON 아님(status {r.status_code})", body, 600)
                continue
            if isinstance(data, dict) and ("err" in data or "errMsg" in data):
                show(f"[{label}] {org}/{tbl} → 오류", data, 400)
                continue
            rows = data if isinstance(data, list) else [data]
            slim = []
            for row in rows[:12]:
                if isinstance(row, dict):
                    slim.append({k: row.get(k) for k in
                                 ("TBL_NM", "PRD_DE", "ITM_NM", "C1_NM",
                                  "C2_NM", "UNIT_NM", "DT") if k in row})
            show(f"[{label}] {org}/{tbl} — 표본 {len(rows)}행 중 12행", slim, 3500)
        except Exception as e:
            print(f"[{label}] {org}/{tbl} 실패: {str(e)[:150]}")


def main():
    if not API_KEY:
        print("[ERROR] KOSIS_API_KEY 미설정 — GitHub Secret 등록 필요")
        raise SystemExit(1)
    print("KOSIS 프로브 시작 — 아래 로그 전체를 복사해 Claude에게 전달해주세요")
    probe_search()
    probe_data()
    print("\nKOSIS 프로브 완료")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
sports-industry-monitor — Phase 5 사전 검증: KOSIS 프로브 2차
1차에서 확보한 실제 표 ID의 ① 분류 축(objL1/objL2…) 구성과 항목 코드를
메타 API로 확인하고, ② 그 코드로 실제 데이터 조회를 시도한다.
여기서 나온 코드로 본 코드(kosis_fetch.py)를 확정한다. (§검증 우선)
실행: GitHub Actions 수동 1회 → 로그를 Claude에게 전달
"""

import os
import json
import requests

API_KEY = os.environ.get("KOSIS_API_KEY", "")
UA = {"User-Agent": "sports-industry-monitor kosis probe2"}

# 1차 검색으로 확인된 실제 표
TABLES = [
    ("101", "DT_1K41012", "재별 및 상품군별 소매판매액지수"),
    ("101", "DT_1K41013", "소매업태별 판매액지수"),
    ("101", "DT_1KE1007", "온라인쇼핑몰 판매매체별/상품군별 거래액"),
    ("101", "DT_1J22001", "지출목적별 소비자물가지수"),
]

META = "https://kosis.kr/openapi/statisticsData.do"
DATA = "https://kosis.kr/openapi/Param/statisticsParameterData.do"


def show(title, obj, limit=3000):
    txt = obj if isinstance(obj, str) else json.dumps(obj, ensure_ascii=False)
    print(f"\n===== {title} =====\n{txt[:limit]}\n")


def meta(org, tbl, label, meta_type, keep):
    """메타 조회: ITM(항목) / OBJ(분류) 목록"""
    try:
        r = requests.get(META, params={
            "method": "getMeta", "apiKey": API_KEY, "type": meta_type,
            "orgId": org, "tblId": tbl, "format": "json", "jsonVD": "Y",
        }, headers=UA, timeout=30)
        try:
            data = r.json()
        except Exception:
            show(f"[{label}] {tbl} META({meta_type}) JSON 아님", r.text, 600)
            return
        rows = data if isinstance(data, list) else [data]
        slim = []
        for row in rows[:40]:
            if isinstance(row, dict):
                slim.append({k: row.get(k) for k in keep if k in row})
        show(f"[{label}] {tbl} META({meta_type}) — {len(rows)}행 중 40행", slim)
    except Exception as e:
        print(f"[{label}] {tbl} META({meta_type}) 실패: {str(e)[:150]}")


def try_data(org, tbl, label, obj_levels):
    """objL 조합을 바꿔가며 최근 2개월 데이터 조회 시도"""
    params = {
        "method": "getList", "apiKey": API_KEY,
        "orgId": org, "tblId": tbl, "itmId": "ALL",
        "prdSe": "M", "newEstPrdCnt": "2",
        "format": "json", "jsonVD": "Y",
    }
    for lv in obj_levels:
        p = dict(params)
        for i in range(1, lv + 1):
            p[f"objL{i}"] = "ALL"
        try:
            r = requests.get(DATA, params=p, headers=UA, timeout=40)
            try:
                data = r.json()
            except Exception:
                show(f"[{label}] {tbl} objL1~{lv} → JSON 아님", r.text, 500)
                continue
            if isinstance(data, dict) and ("err" in data or "errMsg" in data):
                show(f"[{label}] {tbl} objL1~{lv} → 오류", data, 300)
                continue
            rows = data if isinstance(data, list) else [data]
            slim = []
            for row in rows[:15]:
                if isinstance(row, dict):
                    slim.append({k: row.get(k) for k in
                                 ("PRD_DE", "ITM_NM", "C1_NM", "C2_NM",
                                  "C3_NM", "UNIT_NM", "DT") if k in row})
            show(f"[{label}] {tbl} objL1~{lv} ✅ 성공 — 총 {len(rows)}행 중 15행",
                 slim, 4000)
            return
        except Exception as e:
            print(f"[{label}] {tbl} objL1~{lv} 실패: {str(e)[:150]}")


def main():
    if not API_KEY:
        print("[ERROR] KOSIS_API_KEY 미설정")
        raise SystemExit(1)
    print("KOSIS 프로브 2차 — 로그를 Claude에게 전달해주세요")
    for org, tbl, label in TABLES:
        meta(org, tbl, label, "ITM", ("ITM_ID", "ITM_NM", "UNIT_NM"))
        meta(org, tbl, label, "OBJ",
             ("OBJ_ID", "OBJ_NM", "OBJ_ID_SUB", "C1", "C1_NM", "ITM_NM"))
        try_data(org, tbl, label, [1, 2, 3])
    print("\nKOSIS 프로브 2차 완료")


if __name__ == "__main__":
    main()

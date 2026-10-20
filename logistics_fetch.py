# -*- coding: utf-8 -*-
"""
sports-industry-monitor — Phase 10: 물류 (운임·운송기간)
v1.3: (대표 지시 2026-10-20 '보완안 1·2·3 모두') 공공데이터포털(www.data.go.kr·apis.data.go.kr — 국가정보자원관리원 27.101.x)이 일부 GitHub
      서버(IP)에서만 연결이 안 됨(10/20 시험: 서버 7대 중 2대 — 미국 워싱턴주·멕시코, 해수부 홈페이지도 같이 막힘 · 같은 실행 안에서 다시 해도
      IP가 같아 소용없음) → ① 시작할 때 두 주소에 연결만 먼저 시험(6초 × 2번)해 막힌 서버면 그 주소의 자료는 기다리지 않고 바로 이전 값
      (2~3분 허비하던 것을) ② 연결 오류로 못 받은 공공데이터포털 자료(관세청 운송비용 3 · 물동량 2 · 부산 입항 선박)는 update.yml이 새 서버에서
      그 자료만 다시 받음(LOGI_ATTEMPT 2·3 — 최대 2번 더, GITHUB_OUTPUT retry_keys로 넘김 · 다른 자료는 1차 값 그대로) ③ 다시 받을 차례가
      남아 있으면 그 자료의 기준일 경고·'절반 이상' 셈은 마지막 차례로 미룸(연결 차단으로 못 받은 관세청 파일은 '절반 이상' 셈에서 늘 뺌 — 연결
      알림이 따로 있음) ④ 마지막 차례까지 막히면 dgk_conn.since(서버를 다 바꿔도 막힌 첫날)를 남기고, 이틀째(since 다음 날)부터 실패 표시
      '공공데이터포털 연결 안 됨 n일째 — 서버 n대 모두 막힘' · 받으면 since를 지움 ⑤ 실행마다 GitHub 서버 IP 앞 두 자리·지역(ipinfo.io)을 로그와
      dgk_conn.tries에 남김(공공데이터포털 문의용) · LOGI_TEST_BLOCK(브랜치 수동 실행 test_block — 막힌 서버로 가정할 차례, main에서는 무시)은 시험용
v1.2: (대표 지시 2026-10-17 '적출국별 부산향 · 에어는 인천 · 수입 수출 정보·추이 모두' + 공공데이터포털 인증키 등록) 공공데이터포털 오픈 API 3개 추가
      (인증키 GitHub Secrets DATA_GO_KR_API_KEY · 자동승인 · 이용허락 제한 없음 · 요청 주소에 키가 들어가 오류 글에서는 자르기 전에 가림):
      ⑤ 관세청 국가별 입항(수입 I)·출항(수출 E) 물동량(15151805·15151809, 월간 — 매월 15일께 전달까지, 적재화물목록 기준) 최근 36달 —
         바닷길 = 부산(신항 '부산신항' + 북항 '부산항' + '감천항' — 관세청 항구 이름) 컨테이너(TEU, 빈 컨테이너 제외)·톤, 항공 = 인천국제공항 톤·
         B/L 건수(특송·전자상거래 소포 포함). 인천항·평택항 등 다른 항구는 뺌. 나라 = 선적지(수입)·목적지(수출) — VOL_GROUPS 19곳(거점국 9 +
         원산지·생산국 10) + 최근 12달 많은 나라 12곳(한국·기타국은 합계에만). 출항 화물 구분은 E = 수출, R = 환적(10/17 GitHub 서버 시험 —
         포털 명세의 'R : 수출'은 틀림, T는 오류 99). 이상값(앞 12달 가운데값의 20배 넘고 그 달 전체의 2% 넘게 큼 — 26.09 인천공항→미국
         항공 773만 톤 같은 출처 입력 오류)은 저장은 그대로, odd 목록·total_clean(뺀 합)으로 화면이 전체·몫에서 뺌 · 전년 같은 달 대비는
         yoy(두 달 중 한 달이라도 이상값인 나라를 두 달 모두에서 뺀 합 — 같은 나라끼리). 항구 이름이 바뀌면(앞 12달에 있던 항구가 마지막
         달에 없음 — 비슷한 새 이름 후보를 오류 글에) 실패로 봐 이전 값 · 행 수가 totalCount보다 적어도 실패
      ⑥ 해양수산부 선박입출항(PORT-MIS 15006353, 부산 020 · 날짜 조건 = 입항일 · 쪽당 50건) — 부산 입항 컨테이너선(배 종류 이름 '컨테이너'
         또는 코드 41) 하루 척수·직전 출항지 나라·체류시간(입항→출항, 96시간 넘으면 96). 매일 어제까지 최근 7일을 다시 받고(늦게 들어오는
         신고 · 읽은 마지막 날이 사흘 넘게 앞이거나 컨테이너선 0척이면 실패 → 이전 값), 2025-10-01부터(보관 400일) 빈 날을 실행마다 약 90초
         거슬러 채움 — 1년 전 같은 때 먼저 · 묶음 크기는 남은 시간에 맞춤(처음 3일, 잰 속도로 7일까지 · 쪽 사이에서도 멈춤) · 연결 오류면
         멈추고, 다른 오류(XML·결과 코드·건수)는 그 묶음을 하루씩 다시 받아 문제 있는 날만 비움(XML에 못 쓰는 제어 글자는 지우고 읽음) ·
         결과 코드 03(자료 없음)은 첫 쪽만 0척, 둘째 쪽부터면 오류. 0척 묶음은 60일 앞도 0척이고 두 실행 연달아 같을 때만(그사이 더 앞
         날이 들어오지 않았을 때만) 보관 경계(no_data_before)로 확정
      공공데이터포털이 한 기관(관세청 1220000 · 해수부 1192000)에서 연결 안 되면 그 실행의 같은 기관 자료만 건너뜀(이전 값). 인증키 오류
      (등록 안 됨·기한 만료 등)는 일시 오류가 아니라 바로 실패 표시 · 키가 단계에 안 넘어오면 'GitHub Secrets·update.yml 확인' 알림.
      한 실행 '절반 이상' 실패 기준은 기존 자료 8개로만(공공데이터포털이 끊기면 파일 3개 + API 3개가 함께 실패해 매번 울리지 않게 —
      알림 글에는 API 자료를 따로 적음) — 새 자료는 기준일(관세청 월간 10일 · 선박 5일)로만 경고
v1.1:(대표 지시 2026-10-16 '부산발이 아니라 적출국별 부산향 · 1번부터 · 적출국은 홍콩, 로테르담, 두바이, 벨기에 외에 글로벌 주요
      물류 거점 순') 적출 거점 12곳 하루 입항(hubs, IMF PortWatch) 추가 — 홍콩·로테르담·두바이(제벨알리)·앤트워프(벨기에) 다음에
      세계 컨테이너 물동량 1~5위 상하이·싱가포르·닝보·선전·칭다오, 그 밖은 지역 대표 LA/롱비치(미국 서안)·포트클랑(동남아)·
      함부르크(독일). 상하이는 양산항을, 선전은 옌톈·서커우를 더함(PortWatch는 항만별 — 같은 날 값의 합, 모두 값이 있는 날만).
      화면은 더보기 › 물류 '수입' 묶음의 '적출 거점 → 부산' 카드(build_dashboard v33.5). PortWatch 연결이 안 되면 해협·항만·거점 모두 그 실행은
      기다리지 않고 이전 값(한 블록에서만 끊던 것을 실행 전체로 — 거점 12곳이 늘어 8분 제한을 다 쓰지 않게). 한 실행 실패 표시 기준은
      그대로 4개(자료 7개 중 '절반 넘게' → 8개 중 '절반 이상')
v1: (대표 지시 2026-10-16 '만들어줘') 지정학 리스크(2026-02-28 미국·이스라엘의 이란 공격 이후 호르무즈 봉쇄, 홍해·수에즈 우회)에 따른
    물류비·운송기간 추이를 한국향·중동 기준으로 모아 docs/logistics.json에 저장 — 화면은 더보기 › 물류(build_dashboard v33.4).
    ① 관세청 수출입 운송비용(월간, 공공데이터포털 파일 3개 — 인증키 없이 내려받기, 공공누리 1유형): 해상 수입·수출(40ft 1개당 천원 —
       미국 서부·동부·EU·중국·일본·베트남), 항공 수입(kg당 원 — 미국·EU·중국·일본·베트남). 수입 = FOB 조건 수입신고의 운임(할증료 포함) —
       한국으로 들어오는 화물의 실제 운임. 중동은 보도자료에만 있고 파일에는 없음. 지난 달 값은 다음 해 2월까지 고쳐질 수 있어 매번 파일 전체로 바꿈.
       공공데이터포털이 GitHub 서버에서 가끔 연결되지 않아(10/16 시험 실행) 연결 오류면 다른 자료를 다 받은 뒤 한 번 더 받음
    ② KCCI(한국해양진흥공사 컨테이너선운임지수, 매주 월 14시): 부산발 13개 항로 + 종합(항로는 40ft당 달러) — 중동·북유럽·지중해 등.
       첫 실행에 2022-11부터 시계열을 받아 두고 매일 최근 10주를 다시 받아 합침(이용허락 제한 없음)
    ③ IMF PortWatch(무료 API, 주 1회 갱신 · 약 1주 늦음): 해협 하루 통과 척수(전체·컨테이너선) — 호르무즈·바브엘만데브·수에즈·희망봉,
       항만 하루 입항 — 부산·제벨알리·코르파칸·푸자이라(항만 표는 portid로 찾음 — 이름으로는 너무 느려 서버가 거절).
       주별 평균 + 전쟁 전(2026-01-01~02-27) 평균. 배 위치 신호(AIS) 기준이라 신호를 끈 배는 빠짐(호르무즈는 실제보다 적게 잡힘).
       출처 'IMF PortWatch'
    ④ Sea-Intelligence 전 세계 정시율(월간 보도자료 GLP): 정시 도착 비율(%)·늦은 배 평균 지연(일) — 본문의
       'In <달> <연도>, … to <값>%' 문장에서 숫자만 읽음(제목 숫자는 안 씀 — '65%-68%' 같은 범위가 있음). 새 기사만 받고 최근 25달 보관
    못 받은 자료는 이전 값을 이어 쓰고 stale_since(마지막 정상 수집일) 표시 · 최상위 status(ok·kept·failed).
    한 실행 최대 8분(출처가 멈춰도 대시보드 갱신이 끝나게 — 넘으면 남은 자료는 이전 값).
    한 실행에서 절반 넘게(v1.1부터 절반 이상) 실패하거나, 한 자료(·해협·항만 항목)라도 기준일(월간 자료 10일 · KCCI 5일 · PortWatch 7일) 넘게
    이전 값이거나 값 없음(처음 실패한 날 = failed_since)이면 실패 표시(soft_fail.txt → 낮 점검 알림).
    정시율은 가장 최근 달이 125일 넘게 그대로면 실패로 봄(이전 값 → 기준일 경고). 형식이 달라 못 읽은 기사는 읽는 규칙 판(GLP_PARSER)이
    바뀌면 다시 읽음. 이전 파일이 손상돼 있어도(목록·글자·빠진 칸) 그 부분만 버리고 새로 받음
출력: docs/logistics.json
§29-D: 출처가 준 값만 저장(추정값·임의 값 없음)
"""

import csv
import datetime
import html as htmlmod
import io
import json
import os
import re
import socket
import time
import xml.etree.ElementTree as ET
from urllib.parse import quote, quote_plus, urlsplit

import requests

SCRIPT = "logistics_fetch"
OUT = "docs/logistics.json"
KST = datetime.timezone(datetime.timedelta(hours=9))
UA = {"User-Agent": "Mozilla/5.0 (sports-industry-monitor logistics; +https://github.com/Jaemin85-Claude/sports-industry-monitor)"}
TIMEOUT = (15, 40)             # (연결, 읽기) 초 — 연결이 안 되는 곳은 빨리 포기
RUN_LIMIT = 8 * 60             # 한 실행 최대 8분 — 넘으면 남은 요청은 바로 실패(이전 값 유지), 대시보드 갱신 작업(20분 제한)은 계속
T_END = float("inf")           # main()이 시작할 때 정함
PW_DOWN = ""                   # 이번 실행에서 PortWatch 연결이 안 된 첫 항목 — 남은 해협·항만·거점은 기다리지 않음(main이 비움)
DGK_DOWN = {}                  # v1.2 이번 실행에서 연결이 안 된 오픈 API 기관(주소의 기관 번호 1220000 관세청·1192000 해수부) → 처음 실패한 자료 —
                               # 같은 기관의 남은 자료는 기다리지 않음(기관이 다르면 계속 물음 · main이 비움)
DGK_AUTH = []                  # v1.2 인증키 오류가 난 자료 — 실행 끝에 바로 실패 표시(main이 비움)
DGK_NOKEY = False              # v1.2 인증키가 이 단계에 안 넘어옴(GitHub Secrets·update.yml env) — 따로 알림(main이 비움)
WAR_START = "2026-02-28"                       # 전쟁 시작(미국·이스라엘의 이란 공격) — '전쟁 전' 비교 기준
BASE_FROM, BASE_TO = "2026-01-01", "2026-02-27"   # 해협·항만 '전쟁 전 평균' 기간(일별 값 평균)
STALE_ALERT = {"kcs_sea_import": 10, "kcs_sea_export": 10, "kcs_air_import": 10,   # 이 일수 넘게 이전 값이면 실패 표시 —
               "glp": 10, "kcci": 5, "choke": 7, "ports": 7, "hubs": 7,             # 월간 자료는 열흘, 주간 자료는 5~7일
               "vol_in": 10, "vol_out": 10, "busan_calls": 5}                       # v1.2 관세청 물동량(월간) · 부산 입항 선박(매일)

# ① 관세청 수출입 운송비용 — 공공데이터포털 파일 데이터(월간)
KCS = [  # (블록 키, 데이터 번호, 이름, 단위)
    ("kcs_sea_import", "15116806", "관세청 해상 수입", "천원/40ft"),
    ("kcs_sea_export", "15116850", "관세청 해상 수출", "천원/40ft"),
    ("kcs_air_import", "15116807", "관세청 항공 수입", "원/kg"),
]
KCS_PAGE = "https://www.data.go.kr/data/{}/fileData.do"
KCS_DOWN = "https://www.data.go.kr/cmm/cmm/fileDownload.do?atchFileId={}&fileDetailSn=1&insertDataPrcus=N"

LABELS = {**{k: n for k, _, n, _ in KCS}, "kcci": "KCCI 부산발 운임", "choke": "해협 통과", "ports": "항만 입항",
          "hubs": "적출 거점 입항", "glp": "전 세계 정시율",
          "vol_in": "관세청 국가별 수입 물동량", "vol_out": "관세청 국가별 수출 물동량", "busan_calls": "부산 입항 선박"}   # 블록 키 → 이름(저장 순서)
DGK_BLOCKS = ("vol_in", "vol_out", "busan_calls")   # v1.2 공공데이터포털 오픈 API 자료 — 한 실행 '절반 이상' 실패 기준에서 뺌(기준일로만 경고)
DGK_ALL = tuple(k for k, *_ in KCS) + DGK_BLOCKS    # v1.3 공공데이터포털 자료 전부(파일 3 + API 3) — 연결 오류면 새 서버에서 다시 받는 대상
DGK_HOSTS = ("www.data.go.kr", "apis.data.go.kr")   # v1.3 시작할 때 연결만 시험하는 주소(파일 · 오픈 API)
DGK_BLOCKED = {}               # v1.3 이번 서버에서 연결 시험에 실패한 주소 → 사유(그 주소의 자료는 기다리지 않고 바로 NetError · main이 비움)
NETFAIL = []                   # v1.3 이번 실행에서 연결 오류(NetError)로 못 받은 공공데이터포털 자료 키 — 새 서버에서 다시 받을 대상(main이 비움)
RUNNER = ""                    # v1.3 이 GitHub 서버의 IP 앞 두 자리·지역(ipinfo.io) — 로그·dgk_conn.tries

# ② KCCI — 해양진흥공사 해양정보서비스
KCCI_CUR = "https://www.kobc.or.kr/ebz/shippinginfo/kcci/gridList.do?mId=0304000000"
KCCI_TS = "https://www.kobc.or.kr/ebz/shippinginfo/timeseries/gridList.do?mId=0304000000"
KCCI_FROM = "2022-11-01"       # 공식 발표 시작(2022-11-07) 전부터 요청
KCCI_REFRESH_DAYS = 70         # 매일 최근 10주를 다시 받아 합침(고쳐진 값 반영)
KCCI_NAMES = {"KCCI": "종합", "KUWI": "미주 서안", "KUEI": "미주 동안", "KNEI": "북유럽", "KMDI": "지중해",
              "KMEI": "중동", "KAUI": "호주", "KLEI": "남미 동안", "KLWI": "남미 서안", "KSAI": "남아프리카",
              "KWAI": "서아프리카", "KCI": "중국", "KJI": "일본", "KSEI": "동남아"}

# ③ IMF PortWatch — ArcGIS FeatureServer(무료, 키 없음)
PW = "https://services9.arcgis.com/weJ1QsnbMYJlCHdG/arcgis/rest/services/{}/FeatureServer/0/query"
PW_FROM_YEAR = 2025            # 주별 값은 2025년부터(작년 같은 때와 비교)
CHOKE = [("chokepoint6", "호르무즈 해협"), ("chokepoint4", "바브엘만데브 해협"),
         ("chokepoint1", "수에즈 운하"), ("chokepoint7", "희망봉")]
PORTS = [("Busan", "부산"), ("Jebel Ali", "제벨알리"), ("Khor Fakkan", "코르파칸"), ("Fujairah", "푸자이라")]
# v1.1 적출 거점(한국으로 실어 오는 출발 항만) — 대표가 정한 4곳 먼저, 그다음 세계 컨테이너 물동량 1~5위, 그 밖은 지역 대표
HUBS = [("Hong Kong", "홍콩"), ("Rotterdam", "로테르담"), ("Jebel Ali", "두바이"), ("Antwerp", "앤트워프"),
        ("Shanghai", "상하이"), ("Singapore", "싱가포르"), ("Ningbo", "닝보"), ("Shenzhen", "선전"), ("Qingdao", "칭다오"),
        ("Los Angeles-Long Beach", "LA/롱비치"), ("Port Klang", "포트클랑"), ("Hamburg", "함부르크")]
# 이름에 '·'를 쓰지 않음 — 상태 글 '적출 거점 입항(홍콩·상하이)'의 구분자(화면 lgMiss가 '·'로 나눔)
# 항만 일별 표는 portid에만 색인이 있음 — 이름(portname)으로 찾으면 40~55초 걸리다 서버가 거절(10/16 GitHub 서버 시험),
# portid로는 0.1~1초. 번호는 PortWatch 항만 목록(PortWatch_ports_database)에서 확인(10/16 GitHub 서버 시험). 둘 이상이면 같은 날 값을 더함
PORT_IDS = {"Busan": "port1065", "Jebel Ali": "port744", "Khor Fakkan": "port561", "Fujairah": "port362",
            "Hong Kong": "port474", "Rotterdam": "port1114", "Antwerp": "port57",
            "Shanghai": ("port1188", "port2027"),   # 상하이 + 상하이(양산) — 양산 심수항은 PortWatch에 따로
            "Singapore": "port1201", "Ningbo": "port824",
            "Shenzhen": ("port1414", "port1189"),   # 옌톈 + 서커우(선전)
            "Qingdao": "port1069", "Los Angeles-Long Beach": "port664", "Port Klang": "port960", "Hamburg": "port446"}

# ④ Sea-Intelligence 보도자료
GLP_LIST = "https://www.sea-intelligence.com/press-room"
GLP_SITE = "https://www.sea-intelligence.com"
GLP_MAX_FETCH = 30             # 한 실행에 새로 읽는 기사 수 상한
GLP_KEEP = 25                  # 보관하는 달 수(최근 2년)
GLP_PARSER = 2                 # 기사 읽는 규칙 판 — 올리면 '형식 다름'으로 건너뛴 기사를 다시 읽음
GLP_STALE_DAYS = 125           # 가장 최근 달(1일 기준)이 이보다 오래면 새 기사를 못 읽는 것(보통 60~95일) → 이전 값 + 경고 기준일
MONTHS = ["january", "february", "march", "april", "may", "june", "july", "august",
          "september", "october", "november", "december"]

# ⑤·⑥ v1.2 공공데이터포털 오픈 API — 인증키는 GitHub Secrets(DATA_GO_KR_API_KEY) · 응답 XML · 정상 결과 코드 '00'
DGK_KEY_ENV = "DATA_GO_KR_API_KEY"
DGK_AUTH_CODES = {"20", "30", "31", "32", "33"}   # 접근 거부 · 등록 안 된 키 · 활용 기간 만료 · 등록 안 된 IP · 서명 없음
VOL = [  # (블록 키, 데이터 번호, 주소, 화물 구분) — 입항: 선적지 나라(dptrPlcNm) → 한국 항구(arvlPlcNm), 출항은 반대
    ("vol_in", "15151805", "https://apis.data.go.kr/1220000/cntyperetprgtqtyacrs/getCntyPerEtprGtqtyAcrs", "I"),
    ("vol_out", "15151809", "https://apis.data.go.kr/1220000/cntyperportgtqtyacrs/getCntyPerPortGtqtyAcrs", "E"),
]
VOL_MONTHS = 36                # 최근 3년(이번 달 전까지) — 전년 같은 달 비교 + 추이
VOL_MODES = [  # (모드, 운송 구분, 한국 쪽 항구·공항 — 이 이름들의 합, 담는 값)
    ("sea", "10", ("부산신항", "부산항", "감천항"), ("teu", "ton")),
    ("air", "40", ("인천국제공항",), ("ton", "bl")),
]
VOL_GROUPS = [  # 늘 담는 나라(관세청 표기 그대로) — 화면 묶음 순서. 바꾸면 화면도 이 목록을 따름(logistics.json groups)
    ("거점", ["홍콩", "네덜란드", "아랍에미리트 연합", "벨기에", "중국", "싱가포르", "미국", "말레이시아", "독일"]),   # 적출 거점 카드의 나라
    ("원산지·생산국", ["일본", "베트남", "이탈리아", "프랑스", "영국", "스페인", "대만", "태국", "인도네시아", "인도"]),   # 병행수입 원산지·생산국
]
VOL_FIXED = [c for _, cs in VOL_GROUPS for c in cs]
VOL_ODD_X, VOL_ODD_SHARE = 20, 0.02   # 이상값: 앞 12달 가운데값의 20배 넘고 넘친 양이 그 달 전체 가운데값의 2% 넘음
VOL_TOP = 12                   # 그 밖에 최근 12달 많은 나라(바닷길 = TEU, 항공 = 톤)
VOL_SKIP = {"한국", "기타국"}   # 나라 목록에서 뺌(합계에는 들어감)
PM_URL = "https://apis.data.go.kr/1192000/VsslEtrynd5/Info5"   # 해양수산부 선박입출항(PORT-MIS) — sde·ede = 입항일(10/17 시험)
PM_PORT = "020"                # 부산
PM_FROM = "2025-10-01"         # 하루 값을 이 날부터 모음(1년 전 같은 주 비교) — 빈 날은 실행마다 거슬러 채움
PM_RECENT = 7                  # 매일 어제까지 최근 7일을 다시 받음(늦게 들어오는 신고·출항 시각)
PM_BACK_SEC = 90               # 한 실행에서 빈 날을 거슬러 받는 시간 상한(초) — 묶음 하나 걸리는 시간을 미리 셈해 넘지 않게(쪽 사이에서도 멈춤)
PM_STAY_CAP = 96               # 체류시간이 이보다 길면 이 값으로(수리·장기 대기 배가 평균을 흔들지 않게)
PM_MIN_DAY = 40                # 받은 묶음의 입항(모든 배)이 하루 평균 이 값의 절반보다 적으면 응답 이상으로 봄(부산은 하루 약 100척)
PM_KEEP_DAYS = 400             # 하루 값 보관 기간(일) — 1년 전 같은 때 비교 + 여유


def log(msg):
    print(msg, flush=True)


def soft_fail(msg):
    """심각한 실패 표시 — 저장은 하되 워크플로우 마지막 단계가 빨간 X로 끝내 점검 알림이 가게 함"""
    print(f"실패 표시: {msg}", flush=True)
    with open("soft_fail.txt", "a", encoding="utf-8") as f:
        f.write(f"{SCRIPT}: {msg}\n")


class NetError(RuntimeError):
    """연결 안 됨·시간 초과·5xx — 잠시 뒤 다시 해 볼 만한 오류(형식 오류와 구분)"""


def time_left():
    return T_END - time.monotonic()


def tcp_ok(host, port=443, timeout=6, tries=2):
    """v1.3 연결만 시험(요청은 안 보냄) — 막힌 서버는 응답이 없어 시간 초과. 프록시를 거치는 환경이면 시험하지 않고 True"""
    if any(os.environ.get(k) for k in ("HTTPS_PROXY", "https_proxy")):
        return True
    for k in range(tries):
        try:
            socket.create_connection((host, port), timeout=timeout).close()
            return True
        except OSError:
            if k + 1 < tries:
                time.sleep(2)
    return False


def runner_where():
    """v1.3 이 GitHub 서버의 공인 IP 앞 두 자리·지역·망(ipinfo.io) — '4.154.x.x · Washington · AS8075 Microsoft Corporation'. 못 읽으면 ''"""
    try:
        d = requests.get("https://ipinfo.io/json", headers=UA, timeout=5).json()
        ip = str(d.get("ip") or "").split(".")
        head = ".".join(ip[:2]) + ".x.x" if len(ip) == 4 else "?"
        return " · ".join(x for x in (head, str(d.get("region") or ""), str(d.get("org") or "")) if x)
    except Exception:
        return ""


def dgk_precheck(attempt):
    """v1.3 공공데이터포털 두 주소에 연결만 먼저 시험 — 막히면 DGK_BLOCKED(그 주소의 자료는 바로 이전 값). LOGI_TEST_BLOCK에
    이번 차례가 있으면 막힌 서버로 가정(시험용 — main 브랜치 실행에서는 무시)"""
    test = {x.strip() for x in os.environ.get("LOGI_TEST_BLOCK", "").split(",") if x.strip()}
    if test and os.environ.get("GITHUB_REF_NAME") == "main":
        log("  [WARN] LOGI_TEST_BLOCK은 main 실행에서 무시(시험은 브랜치에서)")
        test = set()
    for h in DGK_HOSTS:
        if str(attempt) in test:
            DGK_BLOCKED[h] = f"공공데이터포털({h}) 연결 안 됨 — 시험(LOGI_TEST_BLOCK): 막힌 서버로 가정"
        elif not tcp_ok(h):
            DGK_BLOCKED[h] = f"공공데이터포털({h}) 연결 안 됨 — 이 GitHub 서버({RUNNER or 'IP 확인 못 함'})에서 막힘"
        log(f"  연결 시험 {h}: {'막힘' if h in DGK_BLOCKED else '정상'}")


def http(url, params=None, data=None, timeout=TIMEOUT, tries=2, mask=None):
    """GET(또는 data가 있으면 POST) — 연결 오류·5xx는 5초 뒤 한 번 더(NetError). 4xx는 바로 RuntimeError.
    실행 시간(RUN_LIMIT)이 거의 다 되면 보내지 않고 NetError, 남은 시간보다 길게 기다리지 않음.
    mask = 오류 글에서 비밀값을 가리는 함수(v1.2 — 자르기 전에 가림: 잘린 키 조각이 남지 않게)"""
    err = None
    for k in range(tries):
        left = time_left()
        if left < 5:
            raise NetError(f"시간 초과 — 이번 실행의 물류 수집 시간({RUN_LIMIT // 60}분)을 다 씀")
        to = timeout if isinstance(timeout, tuple) else (timeout, timeout)
        to = (min(to[0], left), min(to[1], left))
        try:
            if data is None:
                r = requests.get(url, params=params, headers=UA, timeout=to)
            else:
                r = requests.post(url, params=params, data=data, headers=UA, timeout=to)
            if r.status_code >= 500:
                raise requests.HTTPError(f"HTTP {r.status_code}")
            if r.status_code != 200:   # v1.2 본문 앞부분도(공공데이터포털은 403 본문에 '등록되지 않은 서비스키' 같은 사유)
                body = clean(r.text)
                raise RuntimeError(f"HTTP {r.status_code} {(mask(body) if mask else body)[:120]}".rstrip())
            return r
        except (requests.ConnectionError, requests.Timeout, requests.HTTPError) as e:
            err = e
            if k + 1 < tries and time_left() > 15:
                time.sleep(5)
    raise NetError(f"{type(err).__name__}: {(mask(str(err)) if mask else str(err))[:150]}")


def clean(s):
    """HTML 조각 → 글자만(공백 하나로)"""
    return re.sub(r"\s+", " ", htmlmod.unescape(re.sub(r"<[^>]+>", " ", s or ""))).strip()


def table_rows(page):
    """표의 행 → 칸 글자 목록(머리·본문 모두). 스크립트·스타일은 뺌"""
    page = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", page)
    out = []
    for tr in re.findall(r"(?is)<tr\b.*?</tr>", page):
        cs = [clean(c) for c in re.findall(r"(?is)<t[hd]\b[^>]*>(.*?)</t[hd]>", tr)]
        if cs:
            out.append(cs)
    return out


def num(s):
    """'8,885' → 8885, '62.4' → 62.4, 빈칸·'-' → None"""
    s = (s or "").replace(",", "").strip()
    if not re.fullmatch(r"-?\d+(\.\d+)?", s):
        return None
    v = float(s)
    return int(v) if v.is_integer() and "." not in s else v


def today_kst():
    return datetime.datetime.now(KST).date()


# ───────────────────────── ① 관세청 수출입 운송비용 ─────────────────────────
def kcs_page_meta(page):
    """파일 데이터 화면 → (내려받기 번호 FILE_…, 파일 이름 날짜, 수정일, 차기 등록 예정일). 번호가 여럿이면 가장 큰(최신) 것"""
    ids = sorted(set(re.findall(r"FILE_\d{9,}", page)), key=lambda x: int(x[5:]))
    title = clean((re.search(r"(?is)<title>(.*?)</title>", page) or [None, ""])[1])
    fdate = re.search(r"_(\d{8})\b", title)
    mod = re.search(r"수정일</strong>\s*<div class=\"value\">\s*([\d-]{10})", page)
    nxt = re.search(r"차기 등록 예정일</strong>\s*<div class=\"value\">\s*([\d-]{10})", page)
    return (ids[-1] if ids else None,
            f"{fdate.group(1)[:4]}-{fdate.group(1)[4:6]}-{fdate.group(1)[6:]}" if fdate else None,
            mod.group(1) if mod else None, nxt.group(1) if nxt else None)


def parse_kcs_csv(raw):
    """관세청 운송비용 CSV(첫 칸 '기간', 다음 칸 = 지역) → (지역 목록, [[YYYY-MM, 값…], …]). 형식이 다르면 ValueError"""
    text = None
    for enc in ("utf-8-sig", "cp949"):
        try:
            text = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    if text is None:
        raise ValueError("글자 인코딩을 읽지 못함")
    rows = [r for r in csv.reader(io.StringIO(text)) if any(c.strip() for c in r)]
    if not rows or rows[0][0].strip() != "기간":
        raise ValueError(f"첫 칸이 '기간'이 아님: {str(rows[:1])[:120]}")
    cols = [c.strip() for c in rows[0][1:]]
    if len(cols) < 3 or not all(cols):
        raise ValueError(f"지역 칸 이상: {cols}")
    out = []
    for r in rows[1:]:
        p = r[0].strip()
        if not re.fullmatch(r"\d{4}-\d{2}", p):
            continue
        vals = [num(c) for c in (r[1:] + [""] * len(cols))[:len(cols)]]
        if any(v is not None and v < 0 for v in vals):
            raise ValueError(f"음수 값: {r}")
        out.append([p] + vals)
    out.sort(key=lambda x: x[0])
    if len(out) < 24:
        raise ValueError(f"달 수가 너무 적음({len(out)})")
    return cols, out


def fetch_kcs_one(ds, name, unit):
    if urlsplit(KCS_PAGE).hostname in DGK_BLOCKED:   # v1.3 이 서버에서 연결 시험 실패 — 기다리지 않음(새 서버에서 다시 받기)
        raise NetError(DGK_BLOCKED[urlsplit(KCS_PAGE).hostname])
    page = http(KCS_PAGE.format(ds), tries=1).text   # 연결이 안 되면 바로 넘김 — 실행 끝에 한 번 더(main)
    fid, fdate, mod, nxt = kcs_page_meta(page)
    if not fid:
        raise RuntimeError("화면에서 내려받기 번호(FILE_…)를 못 찾음")
    raw = http(KCS_DOWN.format(fid), timeout=(15, 60)).content
    cols, rows = parse_kcs_csv(raw)
    last = rows[-1]
    gap = (today_kst() - datetime.date.fromisoformat(last[0] + "-01")).days
    if gap > 100:   # 9월 자료는 10월 중순에 올라옴 — 석 달 넘게 새 달이 없으면 파일 갱신이 멈춘 것
        raise RuntimeError(f"마지막 달이 {last[0]} — {gap}일째 새 달 없음")
    log(f"  {name}: {len(rows)}달 · {rows[0][0]}~{last[0]} · {' · '.join(f'{c} {v:,}' for c, v in zip(cols, last[1:]) if v is not None)} ({unit})")
    return {"name": name, "unit": unit, "dataset": ds, "cols": cols, "rows": rows,
            "file_date": fdate, "updated": mod, "next": nxt}


# ───────────────────────── ② KCCI ─────────────────────────
def parse_kcci_current(page):
    """이번 주 KCCI 표 → {날짜: {코드: 값}} (이번 주·지난 주 2개). 'Current Index 2026-10-12' 머리에서 날짜"""
    rows = table_rows(page)
    dates = None
    for r in rows:
        j = " ".join(r)
        ds = re.findall(r"(?:Current|Previous)\s+Index\s+(\d{4}-\d{2}-\d{2})", j)
        if len(ds) == 2:
            dates = ds
            break
    if not dates:
        raise ValueError("이번 주·지난 주 날짜 머리를 못 찾음")
    out = {dates[0]: {}, dates[1]: {}}
    for r in rows:
        for i, c in enumerate(r):
            if c in KCCI_NAMES:
                nums = [num(x) for x in r[i + 1:]]
                vals = [v for v in nums if v is not None]
                # 칸: 코드 | 항로 | 비중(%) | 이번 주 | 지난 주 | 변화 → 비중 칸(%)은 숫자가 아님(num이 None)
                if len(vals) >= 2:
                    out[dates[0]][c], out[dates[1]][c] = vals[0], vals[1]
                break
    if "KCCI" not in out[dates[0]] or len(out[dates[0]]) < 10:
        raise ValueError(f"코드 {len(out[dates[0]])}개만 읽음")
    return out


def parse_kcci_series(page):
    """시계열 표 → {날짜: {코드: 값}}. 둘째 머리 줄(KUWI | KUEI | …) 앞에 종합(KCCI)"""
    rows = table_rows(page)
    codes = None
    for r in rows:
        if len(r) >= 10 and all(c in KCCI_NAMES for c in r):
            codes = r if r[0] == "KCCI" else ["KCCI"] + r
            break
    if not codes:
        raise ValueError("코드 머리 줄을 못 찾음")
    out = {}
    for r in rows:
        if r and re.fullmatch(r"\d{4}-\d{2}-\d{2}", r[0]) and len(r) == len(codes) + 1:
            vals = {c: num(v) for c, v in zip(codes, r[1:]) if num(v) is not None}
            if vals.get("KCCI") is not None:
                out[r[0]] = vals
    return out


def fetch_kcci(prev):
    """이번 주 표 + 시계열(처음엔 2022-11부터, 그 뒤엔 최근 10주) → 이전 값과 합쳐 날짜순"""
    cols0, rows0 = (prev or {}).get("cols"), (prev or {}).get("rows")
    ok_prev = isinstance(cols0, list) and isinstance(rows0, list)   # 손상된 이전 값은 없는 것으로(처음부터 다시 받음)
    have = {r[0]: dict(zip(cols0, r[1:])) for r in (rows0 if ok_prev else []) if isinstance(r, list) and r and isinstance(r[0], str)}
    have = {d: {c: v for c, v in vs.items() if v is not None} for d, vs in have.items()}
    today = today_kst()
    s_day = KCCI_FROM if len(have) < 52 else (datetime.date.fromisoformat(max(have)) - datetime.timedelta(days=KCCI_REFRESH_DAYS)).isoformat()
    got, how = {}, []
    try:
        cur = parse_kcci_current(http(KCCI_CUR).text)
        got.update(cur)
        how.append("이번 주 표")
    except Exception as e:
        log(f"  KCCI 이번 주 표 실패: {str(e)[:150]}")
    form = {"sDay": s_day, "eDay": today.isoformat(), "mId": "0304000000", "siteCode": "shippinginfo", "sources": "timeseries"}
    ser = {}
    want = (datetime.date.fromisoformat(s_day) + datetime.timedelta(days=21)).isoformat()
    for meth in ("GET", "POST"):   # 화면 검색 칸(sDay·eDay) — GET이 기간을 무시하면 POST(화면의 '검색'과 같음)
        try:
            r = http(KCCI_TS, params={k: form[k] for k in ("sDay", "eDay")} if meth == "GET" else None,
                     data=form if meth == "POST" else None)
            got_s = parse_kcci_series(r.text)
        except Exception as e:
            log(f"  KCCI 시계열({meth}) 실패: {str(e)[:150]}")
            continue
        if got_s and (not ser or min(got_s) < min(ser)):   # 더 오래전부터 온 쪽을 씀
            ser = got_s
        if ser and min(ser) <= want:
            break
    if ser:
        how.append(f"시계열 {len(ser)}주({min(ser)}~{max(ser)})")
        for d, vs in ser.items():
            got[d] = {**ser[d], **got.get(d, {})}   # 같은 날짜는 이번 주 표 값 우선
    if not got:
        raise RuntimeError("이번 주 표·시계열 모두 실패")
    merged = {**have}
    for d, vs in got.items():
        merged[d] = {**merged.get(d, {}), **vs}
    if s_day == KCCI_FROM and ser and min(ser) > "2023-06-30":
        log(f"  KCCI: 처음 받기에서 시계열이 {min(ser)}부터만 옴 — 이후 매일 쌓음")
    cols = list(KCCI_NAMES)
    rows = [[d] + [merged[d].get(c) for c in cols] for d in sorted(merged)]
    latest = rows[-1][0]
    if (today - datetime.date.fromisoformat(latest)).days > 16:
        raise RuntimeError(f"최신 주가 {latest} — 2주 넘게 새 값 없음")
    last = dict(zip(cols, rows[-1][1:]))
    f = lambda c: f"{last[c]:,}" if isinstance(last.get(c), (int, float)) else "―"
    log(f"  KCCI: {' · '.join(how)} · 모두 {len(rows)}주 · {latest} 종합 {f('KCCI')} · 중동 {f('KMEI')} · 북유럽 {f('KNEI')} · 지중해 {f('KMDI')} 달러/FEU")
    return {"cols": cols, "names": KCCI_NAMES, "rows": rows, "latest": latest}


# ───────────────────────── ③ IMF PortWatch ─────────────────────────
def pw_rows(layer, where, fields):
    """PortWatch 질의 — 1,000건씩 넘겨 받음. 날짜 오름차순"""
    out, off = [], 0
    while True:
        r = http(PW.format(layer), params={"where": where, "outFields": ",".join(fields), "orderByFields": "date ASC",
                                          "resultOffset": off, "resultRecordCount": 1000, "f": "json"}, timeout=(15, 60))
        d = r.json()
        if "error" in d:
            raise RuntimeError(f"PortWatch 오류: {str(d['error'])[:150]}")
        fs = d.get("features") or []
        out += [f.get("attributes") or {} for f in fs]
        if len(fs) < 1000 or off >= 9000:
            break
        off += 1000
    return out


def pw_date(v):
    """PortWatch 날짜 — 'YYYY-MM-DD' 글자 또는 밀리초 숫자"""
    if isinstance(v, (int, float)):
        return datetime.datetime.fromtimestamp(v / 1000, datetime.timezone.utc).date()
    return datetime.date.fromisoformat(str(v)[:10])


def weekly(rows, fields):
    """일별 → 주별(월요일 시작) 평균: [[주 시작일, 값1, 값2, 날 수], …]"""
    acc = {}
    for a in rows:
        d = pw_date(a.get("date"))
        wk = (d - datetime.timedelta(days=d.weekday())).isoformat()
        s = acc.setdefault(wk, [[0.0, 0] for _ in fields])
        for i, f in enumerate(fields):
            v = a.get(f)
            if isinstance(v, (int, float)):
                s[i][0] += v
                s[i][1] += 1
    out = []
    for wk in sorted(acc):
        s = acc[wk]
        out.append([wk] + [round(t / n, 1) if n else None for t, n in s] + [max(n for _, n in s)])
    return out


def period_avg(rows, field, d0, d1):
    vs = [a.get(field) for a in rows if d0 <= pw_date(a.get("date")).isoformat() <= d1 and isinstance(a.get(field), (int, float))]
    return round(sum(vs) / len(vs), 1) if vs else None


def pw_sum(parts, fields):
    """항만 여럿의 일별 값 → 날짜별 합(모든 항만에 그날 행이 있는 날만 · 한 곳이라도 빈 칸이면 그 칸은 빈 칸)"""
    by = [{pw_date(a.get("date")): a for a in p} for p in parts]
    out = []
    for d in sorted(set(by[0]).intersection(*by[1:])):
        a = {"date": d.isoformat()}
        for f in fields:
            vs = [b[d].get(f) for b in by]
            a[f] = sum(vs) if all(isinstance(v, (int, float)) for v in vs) else None
        out.append(a)
    return out


def pw_item(layer, wheres, fields, label):
    """wheres = 질의 조건 목록 — 둘 이상(상하이 + 양산 등)이면 같은 날 값을 더함"""
    parts = [pw_rows(layer, w, ["date"] + fields) for w in wheres]
    rows = parts[0] if len(parts) == 1 else pw_sum(parts, fields)
    if len(parts) > 1:   # 한 항만이 늦게 갱신되면 합은 그 날까지만 — 로그로 남김(30일 넘게 멈추면 아래 검사로 실패)
        ends = [max((pw_date(a.get("date")) for a in p), default=None) for p in parts]
        if len(set(ends)) > 1:
            log(f"  {label}: 더한 항만의 마지막 날이 다름({' · '.join(str(e) for e in ends)}) — 모두 있는 날까지만 더함")
    if len(rows) < 60:
        raise RuntimeError(f"{label}: 일별 값 {len(rows)}개뿐")
    last = max(pw_date(a.get("date")) for a in rows)
    if (today_kst() - last).days > 30:
        raise RuntimeError(f"{label}: 최신 날짜 {last} — 한 달 넘게 새 값 없음")
    return {"weeks": weekly(rows, fields), "base": [period_avg(rows, f, BASE_FROM, BASE_TO) for f in fields],
            "last_date": last.isoformat()}


def pw_ids(i):
    p = PORT_IDS[i]
    return list(p) if isinstance(p, (tuple, list)) else [p]


def fetch_pw(kind, prev):
    """해협(kind='choke') · 항만(kind='ports') · 적출 거점(kind='hubs') — 항목마다 따로: 못 받은 항목은 이전 값(stale_since).
    한 항목에서 연결이 안 되면(NetError) 같은 서버라 이번 실행의 남은 PortWatch 항목은 모두 기다리지 않음(PW_DOWN)"""
    global PW_DOWN
    if kind == "choke":
        layer, fields, items = "Daily_Chokepoints_Data", ["n_total", "n_container"], CHOKE
        where = lambda i: [f"portid='{i}' AND year>={PW_FROM_YEAR}"]
    else:
        layer, fields, items = "Daily_Ports_Data", ["portcalls", "portcalls_container"], HUBS if kind == "hubs" else PORTS
        where = lambda i: [f"portid='{p}' AND year>={PW_FROM_YEAR}" for p in pw_ids(i)]
    items0 = (prev or {}).get("items")
    old = {x.get("id"): x for x in (items0 if isinstance(items0, list) else []) if isinstance(x, dict)}
    out, bad, kept = [], [], []
    for iid, name in items:
        try:
            if PW_DOWN:
                raise NetError(f"{PW_DOWN}에서 연결 안 됨 — 이번 실행은 건너뜀")
            it = pw_item(layer, where(iid), fields, name)
            out.append({"id": iid, "name": name, **it})
            w = it["weeks"][-1]
            log(f"  {name}: 주 {len(it['weeks'])}개 · 마지막 주 {w[0]}({w[-1]}일) 하루 {w[1]}척(컨테이너선 {w[2]}) · 전쟁 전 {it['base'][0]}척({it['base'][1]})")
        except Exception as e:
            log(f"  {name}: 실패 — {str(e)[:150]}")
            if isinstance(e, NetError) and not PW_DOWN:
                PW_DOWN = name
            if iid in old:
                o = dict(old[iid])
                o["stale_since"] = o.get("stale_since") or (prev or {}).get("fetched") or today_kst().isoformat()
                out.append(o)
                kept.append(name)
            else:
                bad.append(name)
        time.sleep(0.5)
    if not [x for x in out if not x.get("stale_since")]:
        raise RuntimeError(f"모두 실패({', '.join(bad + kept)})")
    return {"fields": fields, "items": out, "kept": kept, "failed": bad}


# ───────────────────────── ④ Sea-Intelligence 정시율 ─────────────────────────
def glp_list(page):
    """보도자료 목록 → [(주소, 제목)] (같은 기사는 한 번, '계속 읽기' 링크 제외)"""
    out, seen = [], set()
    for m in re.finditer(r'(?is)<a[^>]+href="([^"]*press-room/\d+-[^"#?]*)"[^>]*>(.*?)</a>', page):
        u, t = m.group(1), clean(m.group(2))
        if not t or t.lower().startswith("continue reading") or u in seen:
            continue
        seen.add(u)
        out.append((u if u.startswith("http") else GLP_SITE + u, t))
    return out


def is_glp(title):
    return bool(re.search(r"global\s+schedule\s+reliability", title, re.I))


def parse_glp(page, title=""):
    """GLP 월간 보도자료 → (자료 달 YYYY-MM, 정시율 %, 늦은 배 평균 지연 일 또는 None). 못 읽으면 ValueError
    기사 제목 다음 본문의 전 세계 수치 첫 문장 — 'In August 2025, global industry schedule reliability … to 65.3%' ·
    '… in July 2026 to 56.4%' · '… taking the May 2026 figure to 64.7%' · '… dropping the August figure to 49.9%' ·
    'the January 2025 score of 51.5%'(선사·얼라이언스 문장, 제목·'Press Room' 머리는 뺌). 달 = 'the <달> (연도) figure/score'
    또는 'in <달> <연도>'('since March 2026' 같은 다른 달은 안 봄 · 연도가 없으면 발행일로 — 발행 달보다 뒤면 작년).
    지연 = 그 뒤 몇 문장 안의 'average delay … to/at <일> days'. 제목의 숫자는 쓰지 않음('65%-68%' 같은 범위가 있음)"""
    pm = (re.search(r'"datePublished"\s*:\s*"(\d{4}-\d{2}-\d{2})', page)
          or re.search(r'property="datePublished"\s+content="(\d{4}-\d{2}-\d{2})', page)
          or re.search(r'"dateModified"\s*:\s*"(\d{4}-\d{2}-\d{2})', page)
          or re.search(r'property="dateModified"\s+content="(\d{4}-\d{2}-\d{2})', page))
    if not pm:
        raise ValueError("발행일 없음")
    pub = datetime.date.fromisoformat(pm.group(1))
    body = clean(re.sub(r"(?is)<(script|style|head|nav|header|footer)[^>]*>.*?</\1>", " ", page))
    i = body.find(title[:30]) if title else -1
    if i < 0:
        i = max(body.lower().find("published issue"), 0)
    sents = re.split(r"(?<=[.!?;])\s+", body[i:i + 4000])   # 기사 앞부분만(옆·아래 다른 기사 소개 제외)
    mon = "|".join(MONTHS)
    ym = rel = None
    k = 0
    for k, snt in enumerate(sents):
        if re.search(r"press room|published issue|carrier|alliance|gemini", snt, re.I):
            continue
        if not re.search(r"schedule reliability|figure|score", snt, re.I):
            continue
        v = re.search(r"\b(?:to|of|reached|at)\s+(\d{2}(?:\.\d+)?)\s?%(?!\s?[-‑–]\s?\d)", snt)   # '65%-68%' 범위는 안 읽음
        m = (re.search(r"\bthe\s+(" + mon + r")(?:\s+(20\d\d))?\s+(?:figure|score)\b", snt, re.I)
             or re.search(r"\bin\s+(" + mon + r")\s+(20\d\d)\b", snt, re.I))
        if v and m:
            mo = MONTHS.index(m.group(1).lower()) + 1
            yr = int(m.group(2)) if m.group(2) else (pub.year if mo <= pub.month else pub.year - 1)
            ym, rel = f"{yr}-{mo:02d}", float(v.group(1))
            break
    delay = None
    for snt in sents[k:k + 8] if ym else []:
        d = re.search(r"\b(?:to|at)\s+(\d{1,2}\.\d+)\s+days", snt)
        if d and re.search(r"average delay", snt, re.I) and not re.search(r"carrier|alliance|gemini", snt, re.I):
            delay = float(d.group(1))
            break
    if ym is None or not 15 <= rel <= 95:
        raise ValueError(f"전 세계 정시율 문장을 못 찾음({rel})")
    if not (pub - datetime.timedelta(days=130)).isoformat()[:7] <= ym <= pub.isoformat()[:7]:
        raise ValueError(f"자료 달 {ym}이 발행일 {pub}와 맞지 않음")
    if delay is not None and not 1 <= delay <= 20:
        delay = None
    return ym, rel, delay


def fetch_glp(prev):
    """목록에서 'Global Schedule Reliability' 기사 중 아직 안 읽은 것만 읽음(처음엔 둘째 쪽까지 — 지난 2년, 한 번에 GLP_MAX_FETCH건까지)"""
    m0, s0, f0 = (prev or {}).get("months"), (prev or {}).get("skip"), (prev or {}).get("fmt_skip")
    old = {r[0]: r for r in (m0 if isinstance(m0, list) else []) if isinstance(r, list) and len(r) >= 4 and isinstance(r[0], str)}
    skip = [u for u in (s0 if isinstance(s0, list) else []) if isinstance(u, str)]   # 쓰지 않는 기사(같은 달 중복·보관 기간 지남) — 다시 받지 않음
    fmt = {u: v for u, v in (f0 if isinstance(f0, dict) else {}).items() if isinstance(u, str)}   # 형식 다름 {주소: 읽는 규칙 판}
    known = {r[3] for r in old.values()} | set(skip) | {u for u, v in fmt.items() if v == GLP_PARSER}   # 규칙 판이 바뀌면 다시 읽음
    arts = glp_list(http(GLP_LIST).text)
    if not arts:
        raise RuntimeError("보도자료 목록을 못 읽음")
    if len(old) < 10:
        try:
            arts += glp_list(http(GLP_LIST, params={"start": 100}).text)
        except Exception as e:
            log(f"  정시율 목록 둘째 쪽 실패: {str(e)[:120]}")
    todo = list(dict.fromkeys((u, t) for u, t in arts if is_glp(t) and u not in known))
    if len(todo) > GLP_MAX_FETCH:
        log(f"  정시율: 새 기사 {len(todo)}건 중 {GLP_MAX_FETCH}건만 읽음 — 나머지는 다음 실행에서")
        todo = todo[:GLP_MAX_FETCH]
    new = dict(old)
    for n, (url, title) in enumerate(todo):
        if time_left() < 30:
            log(f"  정시율: 시간이 모자라 새 기사 {len(todo) - n}건은 다음 실행에서")
            todo = todo[:n]
            break
        try:
            page = http(url).text
        except Exception as e:
            log(f"  정시율 기사 받기 실패({title[:50]}): {str(e)[:120]}")   # 일시 오류 — 다음 실행에서 다시
            continue
        try:
            ym, rel, delay = parse_glp(page, title)
        except ValueError as e:
            log(f"  정시율 기사 형식 다름({title[:50]}): {str(e)[:120]} — 건너뜀(읽는 규칙 판 {GLP_PARSER})")
            fmt[url] = GLP_PARSER
            continue
        fmt.pop(url, None)
        if ym in new and new[ym][3] != url:
            log(f"  정시율 {ym}: 이미 다른 기사로 있음 — 그대로 둠({title[:50]})")
            skip.append(url)
            continue
        new[ym] = [ym, rel, delay, url]
        log(f"  정시율 {ym}: {rel}% · 늦은 배 평균 지연 {delay if delay is not None else '―'}일 ({title[:60]})")
        time.sleep(1)
    if not new:
        raise RuntimeError("정시율 기사를 하나도 못 읽음")
    keys = sorted(new)
    for k in keys[:-GLP_KEEP]:   # 보관 기간(최근 GLP_KEEP달)이 지난 달 — 기사 주소를 skip에 넣어 다시 받지 않게
        if len(new[k]) > 3 and new[k][3] not in skip:
            skip.append(new[k][3])
    months = [new[k] for k in keys[-GLP_KEEP:]]
    log(f"  정시율: {len(months)}달 · {months[0][0]}~{months[-1][0]} · 새로 읽은 기사 {len(todo)}건")
    gap = (today_kst() - datetime.date.fromisoformat(months[-1][0] + "-01")).days
    if gap > GLP_STALE_DAYS:   # 매달 말 전달 자료가 나옴 — 한 달 넘게 밀리면 기사 형식·제목이 바뀌었을 수 있음
        raise RuntimeError(f"가장 최근 달이 {months[-1][0]} — {gap}일째 새 달을 못 읽음(정시율 기사 제목·형식 확인)")
    return {"months": months, "skip": skip[-200:], "fmt_skip": dict(list(fmt.items())[-100:])}


# ───────────────────────── ⑤·⑥ 공공데이터포털 오픈 API(v1.2) ─────────────────────────
def dgk_mask(s):
    """오류 글에서 인증키 가림 — 요청 주소(serviceKey=…)가 연결 오류 글에 그대로 들어감"""
    s = re.sub(r"(?i)(service_?key=)[^&\s'\"<>]+", r"\1***", str(s))
    k = os.environ.get(DGK_KEY_ENV, "").strip()
    for f in sorted({k, quote(k, safe=""), quote_plus(k)} - {""}, key=len, reverse=True):
        s = s.replace(f, "***")
    return s


def dgk_org(url):
    """오픈 API 주소의 기관 번호 — https://apis.data.go.kr/1220000/… → '1220000'(관세청) · '1192000'(해수부)"""
    m = re.match(r"https?://[^/]+/(\d+)/", url)
    return m.group(1) if m else url


def dgk_root(url, params, label, empty_codes=()):
    """오픈 API 한 번 — XML 뿌리. 연결 오류·5xx·시간 초과는 NetError(그 기관의 남은 자료는 이번 실행에서 건너뜀 — DGK_DOWN,
    기관이 다르면 계속 물음), 인증키 오류는 DGK_AUTH에 남기고 RuntimeError(키가 없으면 DGK_NOKEY), 결과 코드가 '00'이 아니면 RuntimeError.
    empty_codes의 결과 코드(예: '03' 자료 없음)는 오류가 아니라 None(빈 결과)"""
    global DGK_NOKEY
    org = dgk_org(url)
    if urlsplit(url).hostname in DGK_BLOCKED:   # v1.3 이 서버에서 연결 시험 실패 — 기다리지 않음(새 서버에서 다시 받기)
        raise NetError(DGK_BLOCKED[urlsplit(url).hostname])
    if org in DGK_DOWN:
        raise NetError(f"{DGK_DOWN[org]}에서 같은 기관 서버 연결 안 됨 — 이번 실행은 건너뜀")
    key = os.environ.get(DGK_KEY_ENV, "").strip()
    if not key:
        DGK_NOKEY = True
        raise RuntimeError(f"인증키 없음 — GitHub Secrets {DGK_KEY_ENV}를 이 단계(update.yml 물류 단계 env)에 넘겨야 함")
    try:
        r = http(url, params={"serviceKey": key, **params}, timeout=(15, 90), mask=dgk_mask)
    except NetError as e:
        DGK_DOWN[org] = label
        raise NetError(dgk_mask(e)) from None
    except Exception as e:
        msg = dgk_mask(e)
        if re.search(r"SERVICE_KEY|SERVICE_ACCESS_DENIED|DEADLINE_HAS_EXPIRED|UNREGISTERED_IP|등록되지 않은", msg):
            DGK_AUTH.append(label)
            msg = "인증키 오류 — " + msg
        raise RuntimeError(msg) from None
    try:   # XML 1.0에 못 쓰는 제어 글자(배 이름 등에 섞여 옴)는 지우고 읽음 — 한 건 때문에 그 기간 전체를 못 읽지 않게
        root = ET.fromstring(re.sub(rb"[\x00-\x08\x0b\x0c\x0e-\x1f]", b"", r.content))
    except ET.ParseError:
        raise RuntimeError(f"XML 아님: {dgk_mask(clean(r.text))[:150]}") from None
    code = (root.findtext("header/resultCode") or root.findtext(".//returnReasonCode") or "").strip()
    if code != "00":   # 공공데이터포털 게이트웨이 오류는 HTTP 200 + OpenAPI_ServiceResponse 본문으로 오기도 함
        if code in empty_codes:
            return None
        msg = dgk_mask((root.findtext("header/resultMsg") or root.findtext(".//returnAuthMsg") or root.findtext(".//errMsg") or "").strip())
        if code in DGK_AUTH_CODES:
            DGK_AUTH.append(label)
            raise RuntimeError(f"인증키 오류 — 결과 코드 {code} {msg[:100]}")
        raise RuntimeError(f"결과 코드 {code or '없음'} {msg[:100]}")
    return root


def xml_items(root):
    """<item> → {칸: 글자}(앞뒤 공백 없앰). 하위 <details><detail>…은 'details' 목록으로"""
    out = []
    for it in root.iter("item"):
        d = {c.tag: (c.text or "").strip() for c in it if c.tag != "details"}
        d["details"] = [{c.tag: (c.text or "").strip() for c in dt} for dt in it.iter("detail")]
        out.append(d)
    return out


def vol_month(v):
    """관세청 기간 '2025.01'(또는 202501) → '2025-01', 이상하면 None"""
    m = re.fullmatch(r"(20\d\d)\D?(0[1-9]|1[0-2])", (v or "").strip())
    return f"{m.group(1)}-{m.group(2)}" if m else None


def vol_odd(ser_c, tot):
    """나라 한 곳의 달 값 → 이상값(출처 입력 오류로 보이는 값)인 달 위치. 앞 12달(6달 이상) 가운데값의 VOL_ODD_X배를 넘고,
    넘친 양이 그 달 전체 가운데값(앞 12달)의 VOL_ODD_SHARE를 넘을 때 — 가운데값이 0이면(새 길) 그 달 전체 가운데값의 20%를 넘을 때만.
    (예: 26.09 인천공항→미국 항공 수출 773만 톤 · 평소 1만 톤)"""
    out = []
    for i in range(6, len(ser_c)):
        prev = sorted(ser_c[max(0, i - 12):i])
        tp = sorted(tot[max(0, i - 12):i])
        md, tmd, v = prev[len(prev) // 2], tp[len(tp) // 2], ser_c[i]
        if (md > 0 and v > VOL_ODD_X * md and v - md > VOL_ODD_SHARE * tmd) or (md == 0 and tmd > 0 and v > 0.2 * tmd):
            out.append(i)
    return out


def vol_mode(items, inbound, ports, metrics):
    """한 운송 구분(바닷길·항공)의 행 → 달 목록 + 나라별 달 값. 한국 쪽 항구는 ports의 합,
    TEU = FCL + LCL(빈 컨테이너 제외) · 톤 = 총중량 · bl = B/L 건수. 행이 없는 달·나라는 0(그 달 그 나라 화물 없음).
    이상값(vol_odd)은 저장은 그대로 두고 odd 목록에 적고, total_clean(이상값을 뺀 합)과 많은 나라 고르기에서는 뺌"""
    pk, ck = ("arvlPlcNm", "dptrPlcNm") if inbound else ("dptrPlcNm", "arvlPlcNm")
    acc, months, bad, seen_ports = {}, set(), 0, {}
    for it in items:
        ym = vol_month(it.get("yyyymm"))
        if not ym:
            bad += 1
            continue
        months.add(ym)
        pn = (it.get(pk) or "").strip()
        seen_ports.setdefault(pn, set()).add(ym)
        if pn not in ports:
            continue
        v = {"teu": (num(it.get("teuFclGcnt")) or 0) + (num(it.get("teuLclGcnt")) or 0),
             "ton": num(it.get("blWght")) or 0, "bl": num(it.get("blCnt")) or 0}
        a = acc.setdefault((it.get(ck) or "").strip() or "기타국", {}).setdefault(ym, {m: 0 for m in metrics})
        for m in metrics:
            a[m] += round(v[m] * 10)   # 0.1 단위 정수로 더함(소수 TEU를 많이 더해도 반올림이 흔들리지 않게)
    if bad:
        log(f"    기간 칸을 못 읽은 행 {bad}개 — 뺌")
    months = sorted(months)[-VOL_MONTHS:]
    if len(months) < 13:
        raise RuntimeError(f"달 수가 너무 적음({len(months)})")
    last = months[-1]
    odd_names = sorted(n for n in seen_ports if n not in ports and re.search(r"부산|감천" if "부산신항" in ports else r"인천", n)
                       and last in seen_ports[n])
    for pn in ports:   # 항구 이름이 바뀌면(관세청 표기) 부산 합계가 조용히 줄어듦 — 앞 12달에 있던 항구가 마지막 달에 없으면 실패(이전 값)
        had = seen_ports.get(pn, set())
        if had & set(months[-13:-1]) and last not in had:
            raise RuntimeError(f"마지막 달 {last}에 '{pn}' 행이 없음 — 항구 이름이 바뀌었는지 확인"
                               + (f"(새 이름 후보: {', '.join(odd_names)})" if odd_names else ""))
    if odd_names:
        log(f"    [참고] 합에 넣지 않은 비슷한 이름: {', '.join(odd_names)}")
    ser = {c: {m: [round(by.get(ym, {}).get(m, 0) / 10) for ym in months] for m in metrics} for c, by in acc.items()}
    total = {m: [round(sum(by.get(ym, {}).get(m, 0) for by in acc.values()) / 10) for ym in months] for m in metrics}   # 반올림 전 값의 합
    if not total[metrics[0]][-1]:
        raise RuntimeError(f"마지막 달 {last}에 {'·'.join(ports)} 값이 없음")
    odd, clean = [], {m: list(total[m]) for m in metrics}
    for c in sorted(ser):
        for m in metrics:
            for i in vol_odd(ser[c][m], total[m]):
                odd.append([c, months[i], m, ser[c][m][i]])
                clean[m][i] -= ser[c][m][i]
    lead = metrics[0]   # 많은 나라 고르는 기준(바닷길 TEU · 항공 톤) — 최근 12달 합(이상값 뺌)
    oddi = {(o[0], o[1]) for o in odd if o[2] == lead}
    s12 = lambda c: sum(v for ym, v in zip(months[-12:], ser[c][lead][-12:]) if (c, ym) not in oddi)
    keep = [c for c in VOL_FIXED if c in ser and any(ser[c][lead])]
    rest = sorted((c for c in ser if c not in keep and c not in VOL_SKIP and s12(c) > 0), key=lambda c: -s12(c))
    keep += rest[:VOL_TOP]
    # 지정 나라가 없어졌으면(이름 바뀜 의심) — 응답에 아예 없거나, 앞 12달 중 9달 넘게 있던 나라가 마지막 달에 0(원래 거의 0인 길은 빼고)
    miss = [c for c in VOL_FIXED if c not in ser or (not ser[c][lead][-1] and sum(1 for v in ser[c][lead][-13:-1] if v) >= 9)]
    if miss:
        log(f"    [참고] 마지막 달 {last}에 값이 없는 지정 나라: {', '.join(miss)}(나라 이름이 바뀌었으면 VOL_GROUPS 확인)")
    out = {"ports": list(ports), "metrics": list(metrics), "months": months, "total": total, "total_clean": clean, "odd": odd,
           "items": [{"c": c, **ser[c]} for c in keep], "others": max(0, len(rest) - VOL_TOP),
           "groups": [[g, [c for c in cs if c in keep]] for g, cs in VOL_GROUPS]}
    ya = f"{int(last[:4]) - 1}{last[4:]}"
    if ya in months:   # 전년 같은 달 대비 — 두 달 중 한 달이라도 이상값인 나라는 두 달 모두에서 뺌(같은 나라끼리 비교 · 목록 밖 나라도)
        out["yoy"] = {}
        for m in metrics:
            ex = sorted({o[0] for o in odd if o[2] == m and o[1] in (last, ya)})
            out["yoy"][m] = [round(sum(by.get(ym, {}).get(m, 0) for c, by in acc.items() if c not in ex) / 10) for ym in (last, ya)] + [ex]
    return out


def fetch_vol(key, ds, url, carg):
    """관세청 국가별 입항·출항 물동량 — 바닷길·항공 각각 최근 VOL_MONTHS달(한 번에 모두 옴, 쪽 나눔 없음).
    정정·취하가 지난 달에도 반영돼(매월 15일께) 매번 기간 전체를 다시 받음"""
    today = today_kst()
    end = today.replace(day=1)
    start = end
    for _ in range(VOL_MONTHS):
        start = (start - datetime.timedelta(days=1)).replace(day=1)
    inbound = key == "vol_in"
    out = {"dataset": ds, "carg": carg}
    for mode, flag, ports, metrics in VOL_MODES:
        root = dgk_root(url, {"strtYymm": start.strftime("%Y%m"), "endYymm": end.strftime("%Y%m"),
                              "cargTpcd": carg, "seaFlghTpcd": flag}, LABELS[key])
        items = xml_items(root)
        if not items:
            raise RuntimeError(f"{mode}: 행이 없음")
        tc = int(num(root.findtext(".//totalCount")) or 0)
        if tc and len(items) < tc:   # 지금은 한 번에 모두 옴 — 나눠 주기 시작하면 모자란 채로 저장하지 않게
            raise RuntimeError(f"{mode}: 총 {tc:,}행 중 {len(items):,}행만 받음")
        m = vol_mode(items, inbound, ports, metrics)
        last = m["months"][-1]
        gap = (today - datetime.date.fromisoformat(last + "-01")).days
        if gap > 100:   # 9월 자료는 10월 15일께 — 석 달 넘게 새 달이 없으면 갱신이 멈춘 것
            raise RuntimeError(f"{mode}: 마지막 달이 {last} — {gap}일째 새 달 없음")
        unit = {"teu": "TEU", "ton": "톤", "bl": "건"}
        for c, ym, k, v in m["odd"]:   # 출처 입력 오류로 보이는 값 — 저장은 그대로(화면은 '출처 값 확인 필요' · 전체·비교에서 뺌)
            if ym == last:
                log(f"    [WARN] {c} {last} {k} {v:,} — 출처 값 확인 필요(앞 12달보다 지나치게 큼 · 화면 전체·비교에서 뺌)")
        top = sorted(m["items"], key=lambda x: -x[metrics[0]][-1])[:5]
        log(f"  {LABELS[key]} {mode}: 행 {len(items):,} · {len(m['months'])}달 {m['months'][0]}~{last} · {last} 합계 "
            + " · ".join(f"{m['total'][k][-1]:,}{unit[k]}" for k in metrics)
            + f" · 나라 {len(m['items'])}곳(그 밖 {m['others']}곳) · 상위 " + ", ".join(f"{x['c']} {x[metrics[0]][-1]:,}" for x in top)
            + (f" · 이상값 {len(m['odd'])}건" if m["odd"] else ""))
        out[mode] = m
        time.sleep(0.5)
    return out


def pm_time(it, kind, field):
    """선박입출항 상세 중 kind('입항'·'출항')의 시각 — '최종' 신고를 우선(없으면 마지막 신고)"""
    ds = [d for d in it.get("details") or [] if d.get("etryndNm") == kind and d.get(field)]
    if not ds:
        return None
    fin = [d for d in ds if d.get("reqstSeNm") == "최종"] or ds
    try:
        t = datetime.datetime.fromisoformat(fin[-1][field])
    except ValueError:
        return None
    return t if t.tzinfo else t.replace(tzinfo=KST)


class Budget(Exception):
    """거슬러 받기 시간 상한에 닿음 — 이번 실행은 여기까지(연결 오류가 아님)"""


def pm_items(d0, d1, deadline=None):
    """부산 입항일 d0~d1(포함) 모든 배 — 50건씩 쪽을 넘겨 받음(쪽당 최대 50건). 받은 건수가 총 건수와 다르면 RuntimeError.
    결과 코드 03(자료 없음)은 0척. deadline(time.monotonic 기준)을 넘으면 다음 쪽을 받지 않고 Budget"""
    out, page, total = [], 1, 0
    while True:
        if deadline is not None and page > 1 and time.monotonic() > deadline:
            raise Budget(f"{d0}~{d1}: 시간 상한 — {page - 1}쪽까지만 받음")
        root = dgk_root(PM_URL, {"prtAgCd": PM_PORT, "sde": d0.strftime("%Y%m%d"), "ede": d1.strftime("%Y%m%d"),
                                 "numOfRows": "50", "pageNo": str(page)}, LABELS["busan_calls"], empty_codes=("03",))
        if root is None:   # NODATA — 첫 쪽이면 그 기간 자료 없음, 둘째 쪽부터면 덜 받은 것(오류 — 일부만 저장하지 않게)
            if page == 1:
                return [], 0
            raise RuntimeError(f"{d0}~{d1}: {page}쪽 결과 코드 03 — 총 {total}건 중 {len(out)}건만 받음")
        total = int(num(root.findtext(".//totalCount")) or 0)
        its = xml_items(root)
        out += its
        if not its or len(out) >= total or page >= 80:
            break
        page += 1
        time.sleep(0.2)
    if len(out) < total:
        raise RuntimeError(f"{d0}~{d1}: 총 {total}건 중 {len(out)}건만 받음")
    return out, total


def pm_is_box(it):
    """컨테이너선 — 배 종류 이름에 '컨테이너'(풀컨테이너선 등) 또는 배 종류 코드 41(풀컨테이너선 · 10/14 시험)"""
    return "컨테이너" in (it.get("vsslKndNm") or "") or (it.get("vsslKndCd") or "").strip() == "41"


def pm_days(items, d0, d1):
    """입항일별 컨테이너선 — {날짜: [척수, {직전 출항지 나라: 척수}, 체류시간 합, 체류 잰 척수]}. d0~d1 중 입항한 배(모든 종류)가
    한 척이라도 있는 날만 — 부산은 매일 약 100척이라 0척인 날은 자료가 없는 것(빈 날로 두고 다음 실행에서 다시)"""
    days, seen, anyship = {}, set(), set()
    d = d0
    while d <= d1:
        days[d.isoformat()] = [0, {}, 0.0, 0]
        d += datetime.timedelta(days=1)
    for it in items:
        arr = pm_time(it, "입항", "etryptDt")
        if not arr:
            continue
        rec = days.get(arr.astimezone(KST).date().isoformat())
        if rec is None:   # 날짜 조건(입항일) 밖 — 받은 기간 밖 날은 세지 않음
            continue
        anyship.add(arr.astimezone(KST).date().isoformat())
        if not pm_is_box(it):
            continue
        k = (it.get("clsgn"), it.get("etryptYear"), it.get("etryptCo"))   # 호출부호 + 연도 + 그해 입항 횟수 = 입항 한 번
        if k in seen:
            continue
        seen.add(k)
        rec[0] += 1
        cc = re.sub(r"[^A-Z]", "", (it.get("prvsDpmprtNatPrtCd") or "").upper())[:2] or "??"
        rec[1][cc] = rec[1].get(cc, 0) + 1
        dep = pm_time(it, "출항", "tkoffDt")
        if dep and dep > arr:
            rec[2] += min((dep - arr).total_seconds() / 3600, PM_STAY_CAP)
            rec[3] += 1
    return {k: [v[0], dict(sorted(v[1].items(), key=lambda x: -x[1])), round(v[2], 1), v[3]] for k, v in days.items() if k in anyship}


def fetch_portmis(prev):
    """부산 입항 컨테이너선(입항일별) — 어제까지 최근 PM_RECENT일은 매번 다시, 빈 날은 약 PM_BACK_SEC초(묶음 하나 걸리는 시간을
    미리 셈) 동안 거슬러 채움. 최근 묶음을 못 받거나 읽은 날·컨테이너선이 없으면 블록 실패(이전 값 유지 → 기준일 경고).
    거슬러 받기는 연결 오류면 멈추고, 다른 오류면 그 묶음만 건너뛰고 다음 묶음으로(다음 실행에서 다시)"""
    d0 = (prev or {}).get("days")
    days = {r[0]: r[1:] for r in (d0 if isinstance(d0, list) else [])
            if isinstance(r, list) and len(r) == 5 and isinstance(r[0], str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", r[0])
            and isinstance(r[1], int) and isinstance(r[2], dict)}
    nb0, pend = (prev or {}).get("no_data_before"), (prev or {}).get("nd_pending")
    no_before = nb0 if isinstance(nb0, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", nb0) else None
    pend = pend if isinstance(pend, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", pend) else None
    yday = today_kst() - datetime.timedelta(days=1)
    lo = max(PM_FROM, no_before or PM_FROM, (yday - datetime.timedelta(days=PM_KEEP_DAYS)).isoformat())   # 모으는 첫날(보관 기간 상한)
    first = datetime.date.fromisoformat(lo)
    r0 = yday - datetime.timedelta(days=PM_RECENT - 1)
    t0 = time.monotonic()
    items, total = pm_items(r0, yday)
    per_day = (time.monotonic() - t0) / PM_RECENT   # 하루치 받는 데 걸린 시간 — 거슬러 받기 묶음 시간 어림
    if total < PM_MIN_DAY * PM_RECENT / 2:
        raise RuntimeError(f"최근 {PM_RECENT}일 입항이 {total}척뿐 — 응답 이상으로 봄")
    new = pm_days(items, r0, yday)
    n7 = sum(v[0] for v in new.values())
    if not new or max(new) < (yday - datetime.timedelta(days=2)).isoformat():
        raise RuntimeError(f"최근 {PM_RECENT}일 입항 {total}척인데 읽은 마지막 날이 {max(new) if new else '없음'} — 응답 형식 확인(etryndNm·etryptDt·details)")
    if n7 == 0:
        raise RuntimeError(f"최근 {PM_RECENT}일 컨테이너선 0척(모든 배 {total}척) — 배 종류 이름·코드(vsslKndNm·vsslKndCd) 확인")
    days.update(new)
    cc7 = {}
    for v in new.values():
        for c, k in v[1].items():
            cc7[c] = cc7.get(c, 0) + k
    st = [v for v in new.values() if v[3]]
    log(f"  부산 입항 선박: 최근 {PM_RECENT}일({r0}~{yday}) 모든 배 {total}척 · 컨테이너선 {n7}척(하루 {n7 / PM_RECENT:.0f}) · 직전 출항지 "
        + ", ".join(f"{c} {k}" for c, k in sorted(cc7.items(), key=lambda x: -x[1])[:8])
        + (f" · 체류 평균 {sum(v[2] for v in st) / sum(v[3] for v in st):.0f}시간" if st else ""))
    # 빈 날 채우기 — 1년 전 같은 때(화면 '1년 전 같은 7일' 비교 · 앞뒤 1주)를 먼저, 그다음 최근 쪽부터 최대 7일 묶음(연속한 빈 날만)
    back_end, n_back, new_pend = time.monotonic() + PM_BACK_SEC, 0, None
    spd, learned = per_day, False   # 하루치 받는 시간(초) 어림 — 최근 7일 속도로 시작, 지난 날 묶음을 받을 때마다 느린 쪽으로 고침
    solo, n_bad = set(), 0          # 오류가 난 묶음의 날 — 하루씩 다시(문제 있는 날만 비게 · 한 실행 오류 3번까지)
    miss = []
    d = r0 - datetime.timedelta(days=1)
    while d >= first:
        if d.isoformat() not in days:
            miss.append(d)
        d -= datetime.timedelta(days=1)
    ya_hi, ya_lo = yday - datetime.timedelta(days=357), yday - datetime.timedelta(days=371)
    miss = [x for x in miss if ya_lo <= x <= ya_hi] + [x for x in miss if not ya_lo <= x <= ya_hi]
    while miss:
        room = min(back_end - time.monotonic(), time_left() - 60) - 2   # 이번 실행에 남은 거슬러 받기 시간(8분 제한의 마지막 1분은 남김)
        cap = min(7 if learned else 3, int(room / spd)) if spd > 0 else 3   # 끝낼 수 있는 날 수만큼만 묶음(속도를 재기 전엔 3일) — 받다 버리지 않게
        if cap < 1:
            break
        e = miss[0]
        grp = [e]
        for x in miss[1:]:
            if e in solo or len(grp) >= cap or x != grp[-1] - datetime.timedelta(days=1):
                break
            grp.append(x)
        s = grp[-1]
        miss = miss[len(grp):]
        t_g = time.monotonic()
        try:
            its, tot = pm_items(s, e, deadline=min(back_end, time.monotonic() + max(0.0, time_left() - 60)))
        except Budget as ex:   # 어림보다 느림(쪽 사이에서 멈춤) — 이 묶음은 저장 안 함
            log(f"  부산 입항 선박: {str(ex)[:120]} — 나머지는 다음 실행에서")
            break
        except NetError as ex:
            log(f"  부산 입항 선박 지난 날({s}~{e}) 연결 안 됨 — 다음 실행에서: {str(ex)[:150]}")
            break
        except Exception as ex:   # 그 묶음만 이상(XML·결과 코드·건수) — 하루씩 다시 받아 문제 있는 날만 비움(뒤 묶음이 막히지 않게)
            n_bad += 1
            again = len(grp) > 1 and n_bad <= 3
            log(f"  부산 입항 선박 지난 날({s}~{e}) 받기 실패 — {'하루씩 다시' if again else '건너뛰고 다음 실행에서 다시'}: {str(ex)[:150]}")
            if again:
                solo.update(grp)
                miss = grp + miss
            continue
        spd, learned = max(spd, (time.monotonic() - t_g) / len(grp)), True
        got = pm_days(its, s, e)
        older = e.isoformat() < min(days, default="9999")   # 모은 날보다 앞(보관 기간 경계 쪽)
        if tot == 0 and older:   # 0척 — 보관 기간이 끝난 것인지 60일 앞 하루로 확인, 두 실행 연달아 같으면 경계로 확정
            chk = s - datetime.timedelta(days=60)
            try:
                tot2 = pm_items(chk, chk)[1]
            except Exception as ex:
                log(f"  부산 입항 선박 {s}~{e} 0척 — 확인 요청 실패, 다음 실행에서: {str(ex)[:120]}")
                continue
            if tot2 == 0 and pend and min(days, default="9999") >= pend:   # 지난 실행에서도 경계 후보(그사이 더 앞 날이 들어오지 않음) → 여기부터 자료 없음 · 다시 안 물음
                no_before = (e + datetime.timedelta(days=1)).isoformat()
                log(f"  부산 입항 선박: {s}~{e} 자료 없음(60일 앞도 없음 · 두 번째) — {no_before}부터만 모음")
                miss = [x for x in miss if x > e]
                continue
            if tot2 == 0:   # 처음 본 경계 후보 — 한 번은 넘겨 두고 다음 실행에서 확인(한때의 빈 응답으로 앞 기록을 잃지 않게)
                new_pend = (e + datetime.timedelta(days=1)).isoformat()
                log(f"  부산 입항 선박: {s}~{e} 자료 없음(60일 앞도 없음) — 경계 후보 {new_pend}, 다음 실행에서 확인")
                miss = [x for x in miss if x > e]
                continue
            log(f"  부산 입항 선박 {s}~{e} 0척인데 60일 앞({chk})은 {tot2}척 — 응답 이상으로 봐 다음 실행에서")
            continue
        if tot < PM_MIN_DAY * len(grp) / 2 and not (older and got and tot >= PM_MIN_DAY * len(got) / 2):
            # 사이에 낀 빈 날·응답 이상 — 저장 안 하고 다음 실행에서 다시(경계에 걸친 묶음은 자료 있는 날만 저장)
            log(f"  부산 입항 선박 지난 날({s}~{e}) 입항이 {tot}척뿐 — 응답 이상으로 봐 저장 안 함(다음 실행에서)")
            continue
        days.update(got)
        n_back += len(got)
    keep_lo = max(lo, no_before or lo)
    keep = sorted(k for k in days if keep_lo <= k <= yday.isoformat())
    if not keep:
        raise RuntimeError("모은 날이 없음")
    f0 = datetime.date.fromisoformat(keep_lo)
    miss_n = sum(1 for k in range((yday - f0).days + 1) if (f0 + datetime.timedelta(days=k)).isoformat() not in days)   # 아직 빈 날(시작일~어제)
    if n_back or miss_n:
        log(f"  부산 입항 선박: 이번에 지난 날 {n_back}일 채움 · 아직 빈 날 {miss_n}일 · 모은 날 {len(keep)}일({keep[0]}~{keep[-1]})")
    out = {"days": [[k] + days[k] for k in keep], "from": keep_lo, "missing": miss_n, "stay_cap": PM_STAY_CAP}
    if no_before:
        out["no_data_before"] = no_before
    if new_pend and not no_before:
        out["nd_pending"] = new_pend
    return out


# ───────────────────────── 실행 ─────────────────────────
def run_block(key, label, fn, prev_all, out, status, fails, defer=False):
    """블록 하나 — 성공하면 새 값(fetched = 오늘), 실패하면 이전 값 + stale_since(마지막 정상 수집일).
    이전 값도 없으면(값 없음) fails[1][key]에 처음 실패한 날을 남김(해협·항만은 항목별 'key:이름') — 기준일이 지나면 경고.
    defer=True면 연결 오류(NetError)일 때 아무것도 기록하지 않고 False — main이 다른 자료를 다 받은 뒤 한 번 더 부름"""
    prev = prev_all.get(key)
    prev = prev if isinstance(prev, dict) else None   # 손상된 이전 값(목록·글자)은 없는 것으로
    fs_old, fs_new = fails
    today = today_kst().isoformat()
    log(f"[{label}]")
    try:
        blk = fn(prev)
    except Exception as e:
        if defer and isinstance(e, NetError):
            log(f"  {label}: 연결 안 됨 — 다른 자료를 받은 뒤 한 번 더 ({str(e)[:150]})")
            return False
        log(f"  [WARN] {label} 실패 — {str(e)[:200]}" + (" · 이전 값 유지" if prev else " · 값 없음"))
        if key in DGK_ALL and isinstance(e, NetError) and key not in NETFAIL:
            NETFAIL.append(key)   # v1.3 새 서버에서 다시 받을 대상
        carry = {k: v for k, v in fs_old.items() if k.startswith(key + ":")}   # 값 없는 해협·항만 항목 — 처음 실패한 날 유지
        fs_new.update(carry)
        if prev:
            blk = dict(prev)
            if "items" in blk and not isinstance(blk["items"], list):
                blk["items"] = []   # 손상된 이전 값
            blk["stale_since"] = prev.get("stale_since") or prev.get("fetched") or today
            out[key] = blk
            status["kept"].append(label)
            if carry:   # 화면 '값 없음' 줄이 이 날도 보이게
                status["failed"].append(f"{label}({'·'.join(k.split(':', 1)[1] for k in carry)})")
        else:
            status["failed"].append(label)
            fs_new[key] = fs_old.get(key) or today
        return True
    inner = blk.pop("kept", []) or []
    bad = blk.pop("failed", []) or []
    blk["fetched"] = today
    blk["label"] = label
    out[key] = blk
    if inner:   # 해협·항만: 일부 항목만 이전 값
        status["kept"].append(f"{label}({'·'.join(inner)})")
    if bad:     # 해협·항만: 일부 항목은 값 없음
        status["failed"].append(f"{label}({'·'.join(bad)})")
        for nm in bad:
            fs_new[f"{key}:{nm}"] = fs_old.get(f"{key}:{nm}") or fs_old.get(key) or today   # 블록째 값 없던 날부터
    if not inner and not bad:
        status["ok"].append(label)
    return True


def env_int(name, default):
    try:
        return max(1, int(os.environ.get(name, "") or default))
    except ValueError:
        return default


def main():
    global T_END, PW_DOWN, DGK_NOKEY, RUNNER
    T_END = time.monotonic() + RUN_LIMIT
    PW_DOWN, DGK_NOKEY = "", False
    DGK_DOWN.clear()
    DGK_AUTH.clear()
    DGK_BLOCKED.clear()
    NETFAIL.clear()
    # v1.3 몇 번째 차례인지(update.yml: 1차 작업 1/3 → 새 서버 다시 받기 2/3·3/3). 환경 변수가 없으면 1/1(혼자 실행 — 경고를 바로 셈)
    attempt, attempts = env_int("LOGI_ATTEMPT", 1), env_int("LOGI_ATTEMPTS", 1)
    attempts = max(attempts, attempt)
    final = attempt >= attempts
    retry_keys = None
    if attempt > 1:   # 다시 받기 — 앞 차례가 연결 오류로 못 받은 공공데이터포털 자료만
        want = {x.strip() for x in os.environ.get("LOGI_RETRY_KEYS", "").split(",") if x.strip()}
        retry_keys = [k for k in LABELS if k in want and k in DGK_ALL]
        if not retry_keys:
            log(f"[다시 받기 {attempt}/{attempts}] 다시 받을 자료 없음(LOGI_RETRY_KEYS 비어 있음) — 끝")
            return
    RUNNER = runner_where()
    log(f"GitHub 서버: {RUNNER or 'IP 확인 못 함'} · 차례 {attempt}/{attempts}"
        + (f" · 다시 받기: {', '.join(LABELS[k] for k in retry_keys)}" if retry_keys else ""))
    dgk_precheck(attempt)
    prev_all = {}
    if os.path.exists(OUT):
        try:
            with open(OUT, encoding="utf-8") as f:
                prev_all = json.load(f)
        except Exception as e:
            log(f"[WARN] 이전 {OUT} 읽기 실패: {str(e)[:120]}")
    if not isinstance(prev_all, dict):
        log(f"[WARN] 이전 {OUT} 형식이 다름 — 이전 값 없이 받음")
        prev_all = {}
    run_id = os.environ.get("GITHUB_RUN_ID", "")
    pc = prev_all.get("dgk_conn") if isinstance(prev_all.get("dgk_conn"), dict) else {}
    if retry_keys and run_id and pc.get("run") != run_id:
        log("  [WARN] 1차 작업 결과가 아직 main에 없음(커밋 실패?) — 지금 main 파일 위에 다시 받은 자료만 바꿈")
    fs0 = prev_all.get("failed_since")
    fs_old = {k: v for k, v in fs0.items() if isinstance(v, str)} if isinstance(fs0, dict) else {}
    fails = (fs_old, {})
    out = {"generated_at": datetime.datetime.now(KST).strftime("%Y-%m-%d %H:%M KST"), "war_start": WAR_START,
           "base_period": [BASE_FROM, BASE_TO]}
    status = {"ok": [], "kept": [], "failed": []}
    fns = {}
    for key, ds, name, unit in KCS:
        fns[key] = (name, lambda p, ds=ds, name=name, unit=unit: fetch_kcs_one(ds, name, unit))
    for key, ds, url, carg in VOL:   # v1.2 공공데이터포털 오픈 API
        fns[key] = (LABELS[key], lambda p, key=key, ds=ds, url=url, carg=carg: fetch_vol(key, ds, url, carg))
    fns["busan_calls"] = (LABELS["busan_calls"], fetch_portmis)
    if retry_keys:
        # 다시 받기 — 다른 자료·상태·'값 없음' 날짜는 1차 작업이 저장한 그대로 두고, 다시 받는 자료만 바꿈
        rl = {LABELS[k] for k in retry_keys}
        for k in LABELS:
            if k not in retry_keys and isinstance(prev_all.get(k), dict):
                out[k] = prev_all[k]
        pst = prev_all.get("status") if isinstance(prev_all.get("status"), dict) else {}
        for g in status:
            status[g] = [x for x in (pst.get(g) or []) if isinstance(x, str) and x.split("(")[0] not in rl]
        fails[1].update({k: v for k, v in fs_old.items() if k.partition(":")[0] not in retry_keys})
        log(f"[다시 받기 {attempt}/{attempts}] 새 서버에서 공공데이터포털 자료 {len(retry_keys)}개")
        for key in retry_keys:
            run_block(key, fns[key][0], fns[key][1], prev_all, out, status, fails)
    else:
        later = []
        kcs_up = urlsplit(KCS_PAGE).hostname not in DGK_BLOCKED   # v1.3 연결 시험에서 막힌 서버면 실행 끝에 한 번 더 받지 않음(같은 IP)
        for key, ds, name, unit in KCS:
            if not run_block(key, name, fns[key][1], prev_all, out, status, fails, defer=kcs_up):
                later.append(key)
        run_block("kcci", LABELS["kcci"], fetch_kcci, prev_all, out, status, fails)
        run_block("choke", LABELS["choke"], lambda p: fetch_pw("choke", p), prev_all, out, status, fails)
        run_block("ports", LABELS["ports"], lambda p: fetch_pw("ports", p), prev_all, out, status, fails)
        run_block("hubs", LABELS["hubs"], lambda p: fetch_pw("hubs", p), prev_all, out, status, fails)
        run_block("glp", LABELS["glp"], fetch_glp, prev_all, out, status, fails)
        for key, *_ in VOL:
            run_block(key, *fns[key], prev_all, out, status, fails)
        run_block("busan_calls", *fns["busan_calls"], prev_all, out, status, fails)
        if later:
            log(f"[다시 받기] 처음에 연결되지 않은 관세청 자료 {len(later)}개")
            for key in later:
                run_block(key, *fns[key], prev_all, out, status, fails)
    out = {k: out[k] for k in ["generated_at", "war_start", "base_period"] + list(LABELS) if k in out}   # 다시 받은 자료도 원래 순서로
    out["status"] = status
    out["failed_since"] = fails[1]
    # v1.3 공공데이터포털 연결 기록 — tries = 이번 워크플로우 실행의 차례별 서버(같은 실행이면 이어 붙임) · since = 서버를 다 바꿔도 막힌 첫날
    today = today_kst()
    net = [k for k in LABELS if k in NETFAIL]
    ptries = pc.get("tries") if attempt > 1 and run_id and pc.get("run") == run_id and isinstance(pc.get("tries"), list) else []
    tries = [t for t in ptries if isinstance(t, dict)][-4:] + [
        {"n": attempt, "where": RUNNER, "ok": not net, "at": datetime.datetime.now(KST).strftime("%m-%d %H:%M")}]
    since = pc.get("since") if isinstance(pc.get("since"), str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", pc["since"]) else None
    if not net:
        since = None                       # 이번 차례에 받음 — 연결 문제 풀림
    elif final:
        since = since or today.isoformat()   # 마지막 차례까지 막힘 — 처음 막힌 날(이미 있으면 그대로)
    conn = {"run": run_id, "tries": tries}
    if since:
        conn["since"] = since
    if net:
        conn["keys"] = net
    out["dgk_conn"] = conn
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    retry = bool(net) and not final
    if retry and os.environ.get("GITHUB_OUTPUT"):   # update.yml 다음 작업(새 서버)이 이 자료만 다시 받음
        with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as f:
            f.write(f"retry_keys={','.join(net)}\n")
    mine = (lambda x: x.split("(")[0] in {LABELS[k] for k in retry_keys}) if retry_keys else (lambda x: True)
    blk_kept = [x for x in status["kept"] if "(" not in x and mine(x)]
    blk_failed = [x for x in status["failed"] if "(" not in x and mine(x)]
    n_part = len({x.split("(")[0] for x in status["kept"] + status["failed"] if "(" in x and mine(x)} - set(blk_kept) - set(blk_failed))   # 블록 수
    n_ok = len([x for x in status["ok"] if mine(x)])
    log(f"수집 결과{f'(다시 받기 {attempt}/{attempts})' if retry_keys else ''}: 정상 {n_ok} · 이전 값 {len(blk_kept)} · 일부 항목 실패 {n_part} · 값 없음 {len(blk_failed)}")
    log(f"saved {OUT}")
    if net:
        log(f"공공데이터포털 연결 오류로 못 받음: {', '.join(LABELS[k] for k in net)} — "
            + (f"새 서버에서 다시 받기({attempt + 1}/{attempts})" if retry else
               (f"서버 {len(tries)}대 모두 막힘" if len(tries) > 1 else "이 서버에서 막힘") + f" · {since}부터"))
    defer = set(net) if retry else set()   # 다음 차례가 다시 받을 자료 — 이번 차례에서는 경고를 셈하지 않음
    if not retry_keys:
        # 한 실행 '절반 이상' — 기존 8개(오픈 API 3개 빼고). v1.3 연결 차단으로 못 받은 관세청 파일은 늘 뺌(연결 알림이 따로 · 분모는 8 그대로)
        base = [LABELS[k] for k in LABELS if k not in DGK_BLOCKS]
        skip = {LABELS[k] for k in net}
        n_all, n_bad = len(base), len([x for x in blk_kept + blk_failed if x in base and x not in skip])
        if n_bad * 2 >= n_all:   # 8개 중 4개 이상(v1의 7개 중 '절반 넘게'와 같은 4개)
            bad_all = status["kept"] + status["failed"]
            extra = [x for x in bad_all if x.split("(")[0] not in base or x in skip]   # 기준 밖 — 따로 적음
            soft_fail(f"물류 자료 {n_all}개 중 {n_bad}개 못 받음 — " + ", ".join(x for x in bad_all if x not in extra)
                      + (f" (기준 밖 공공데이터포털도 못 받음: {', '.join(extra)})" if extra else ""))
    if DGK_NOKEY:   # v1.2 키가 이 단계에 안 넘어옴 — 저장소 설정 문제(포털 문제 아님)
        soft_fail(f"공공데이터포털 인증키 없음 — GitHub Secrets {DGK_KEY_ENV} 등록과 update.yml 물류 단계 env 줄 확인")
    elif DGK_AUTH:   # v1.2 인증키 오류는 기다려도 안 풀림 — 바로 알림(공공데이터포털 마이페이지에서 활용신청·기간 확인)
        soft_fail("공공데이터포털 인증키 오류(" + ", ".join(dict.fromkeys(DGK_AUTH)) + ") — 마이페이지 활용신청 상태·기간 확인")
    if net and final and since:   # v1.3 서버를 다 바꿔도 막힌 날이 이틀째 — 하루는 운이 나쁠 수 있어 기다림
        nd = (today - datetime.date.fromisoformat(since)).days
        if nd >= 1:
            wh = "; ".join(t.get("where") or "IP 확인 못 함" for t in tries)
            soft_fail(f"공공데이터포털 연결 안 됨 {nd + 1}일째({since}부터) — 오늘 GitHub 서버 "
                      + (f"{len(tries)}대 모두 막힘" if len(tries) > 1 else "에서 막힘") + f"({wh}) · "
                      f"이전 값 유지: {', '.join(LABELS[k] for k in net)}")

    def days_since(d):
        try:
            return (today - datetime.date.fromisoformat(str(d)[:10])).days
        except ValueError:
            return None   # 날짜 모양이 틀림 — 오래된 것으로 봄

    def judged(key):   # 이번 차례가 기준일 경고를 셈하는 자료 — 다시 받기는 자기 자료만, 다음 차례로 넘긴 자료는 빼고
        return (not retry_keys or key in retry_keys) and key not in defer

    old = []
    for key, blk in out.items():
        if key not in STALE_ALERT or not isinstance(blk, dict) or not judged(key):
            continue
        its = blk.get("items")
        ss = [blk.get("stale_since")] + [x.get("stale_since") for x in (its if isinstance(its, list) else []) if isinstance(x, dict)]
        ss = sorted(str(x) for x in ss if x)
        n = days_since(ss[0]) if ss else 0
        if n is None or n > STALE_ALERT[key]:
            old.append(f"{LABELS[key]}({ss[0]}부터 · 기준 {STALE_ALERT[key]}일)")
    for k, d in sorted(fails[1].items()):
        key, _, item = k.partition(":")
        if not judged(key):
            continue
        n, lim = days_since(d), STALE_ALERT.get(key, 7)
        if n is None or n > lim:
            old.append(f"{LABELS.get(key, key)}{f'({item})' if item else ''} 값 없음({d}부터 · 기준 {lim}일)")
    if old:
        soft_fail("오래된 이전 값·값 없음: " + ", ".join(old))


if __name__ == "__main__":
    main()

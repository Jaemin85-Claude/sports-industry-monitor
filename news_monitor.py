# -*- coding: utf-8 -*-
"""
sports-industry-monitor — Phase 4: 뉴스 모니터링 (v2)
v2.15: (대표 지시 2026-10-19 '2순위 새 종목 추가') 명품·패션 브랜드 뉴스 2곳 — 톰브라운(thombrowne · 본사 제냐 실적 뉴스 포함)·랄프로렌(ralphlauren).
       몽클레르 검색에 '몽클레어'(국내 표기가 더 많음). 브랜드 점검표 브랜드 상세 '최근 뉴스'·기업 상세 뉴스와 같은 키
v2.14: (대표 지시 2026-10-16 '만들어줘' — 물류비·운송기간 추이) 산업 '물류·운임'(logistics) 검색어 5개 + 선별 기준 — 해상·항공 운임(KCCI·SCFI·
      관세청 운송비용), 호르무즈·홍해·수에즈·희망봉 우회와 중동 하늘길, 선사 할증료, 항만 적체·정시율처럼 한국 수입 원가·운송기간에 걸리는
      소식만(해운사 주가·조선 수주·유가만 다룬 기사·국내 택배는 제외). 화면 = 시장 › 뉴스 '산업 › 물류·운임' 칩 · 더보기 › 물류 아래 5건.
      검색어는 '(앞 묶음) (주제 묶음)' 꼴 — 구글 뉴스는 OR을 바로 옆 낱말끼리만 묶고 띄어쓰기를 AND로 읽어('항공화물 운임 OR 항공
      화물 유류할증료' = 항공화물 AND (운임|항공) AND …) 여러 낱말 대안이 좁은 AND 검색이 됨(리뷰 2026-10-16). 영어 검색어는 한국판에서
      거의 안 나와 뺌
v2.13: (대표 지시 2026-10-15 '전체 점검') 옛 기사 거르기 — 구글 뉴스가 몇 년 전 기사를 새 날짜로 다시 내보냄(패션포스트 지난 기사
      대량: 2019년 '나이키, 존 도나호 영입'이 10/8 기사로 들어옴). 오늘 선별 기사 + 보관 중 기사(news.json·1년 보관)를
      ① 원문 날짜 — 구글 링크를 원문 주소로 풀어 원문 페이지 발행일(메타·'입력' 표시·주소 속 날짜 중 가장 이른 것, 5분 안에서 —
        구글이 막거나 일시 오류가 이어지면 다음 실행에서). 원문 날짜가 구글 날짜보다 14일 넘게 앞서면 뺌(구글 날짜보다 늦은 원문
        날짜는 안 믿음). 원문은 날짜만 읽음(내용 저장·AI 전송 없음)
      ② 그누보드 글 번호 — 원문이 봇 확인 화면이라 날짜를 못 읽는 그누보드 게시판(패션포스트 fpost.co.kr·미주조선일보
        chosundaily.com, 봇 확인은 우회 안 함)은 주소의 글 번호(wr_id)가 같은 게시판 최신 번호보다 10%(300개) 넘게 뒤면 뺌
        (구글 날짜가 며칠 전이면 그동안 늘었을 번호(하루 40개)만큼 넉넉히 — 1년 보관분 점검 때 수집 당시 최신 기사 보호,
        boards에 최신 번호·오른 날·본 글 수·처음 번호·처음 날 기억, 기사에 글 번호(wr) 저장 — 게시판 최신 번호를 아직 모르면 다음 실행에서 다시 판정).
        믿을 만한 게시판(글 5건 넘게 봄·7일 넘게 지켜보며 최신 번호가 하루 1개 넘게 늘고 최근 7일 안에 오름 — 새 글이 안 올라오는
        옛 게시판은 최신 번호 자체가 옛 글이라 제외)에서 번호로 최근 글이면 dchk 'n' — 그 뒤로도 Claude에 안 물음.
        3주 넘게 안 오른 최신 번호보다 여러 글이 모두 한참 아래면 번호를 새로 매긴 것으로 보고 다시 잡음(실패 표시)
      ③ Claude 짧은 확인(선별 지시문은 그대로) — 원문 날짜·글 번호로 못 가린 것만, 그 매체에 옛 기사가 몰려 있을 때(이번 판단 +
        최근 60일 기억 3건 이상)만 뺌(한두 건은 미리 발표된 일·비슷한 옛 사건 착각일 수 있어 — 10/15 시험에서 최근 기사 3건 오판).
        근거가 부족해 남긴 판단은 기사 ai_old(시기@판단일)에 두고 7일 동안만 다시 판정(몇 달 뒤 다른 근거 하나로 정상 기사를 늦게 빼지 않게)
      뺀 제목은 1년 기억(stale_titles — 새 구글 주소로 다시 와도 막음, 원문 날짜로 확인된 같은 제목 원본은 남김), 1년 보관 제목은 다시
      받지 않음. 남은 기사엔 원문 날짜(orig_date — 화면 날짜)·확인 방법(dchk). 1년 보관분은 처음 몇 번의 실행에 나눠 점검.
      status.date_check. 구글 링크를 하나도 못 풀면(한 실행 5건 넘게 실패, 또는 3회 연속) 실패 표시. 확인 중 오류면 그 실행의 확인
      표시를 되돌리고 실패 표시. 원문 받기는 1MB·25초까지(넘으면 잘린 페이지로 판정하지 않고 다음 실행에서 다시). news.yml 수동 실행 입력 probe(매체 이름·기사 id) = 원문 날짜 진단만(Claude 안 씀·저장 안 함)
v2.12: (대표 승인 2026-10-14 '추천대로') 지난 뉴스 검색용 1년 보관 — 선별한 기사를 docs/news_archive.json에 365일 쌓음
      (같은 제목·같은 브랜드/산업으로 다시 잡힌 기사는 최신 1건 + 별점은 그중 가장 높은 것, 한 줄에 기사 1건). 파일이 없거나 복구가
      덜 끝났으면 news.json의 git 기록(8/31~)에서 되살림. news.json status.archive에 건수·시작일(일부만 복구면 partial — 수집 상태 표시).
      보관 저장이 실패해도 news.json은 저장하고 실패 표시
v2.11: (대표 승인 2026-10-13 — Claude API 비용 연 $20 이하 목표) 비교 선별 모델을 Haiku 5.5(effort low)로 바꿔 10/21까지
      본 선별(Sonnet 4.6)과 같은 헤드라인을 따로 골라 model_compare에 기록(화면·본 선별은 그대로) → 결과 보고 뒤 전환 결정.
      Haiku 5.5 가격($0.10/$0.50, 10만 토큰 넘는 요청은 $0.50/$2.50) 추가, 비교 선별만 생각(thinking) 토큰 몫으로 max_tokens 12000
v2.10: (대표 지시 2026-10-10) Claude 사용량을 월별로 news.json에 저장(claude_usage — 수집 상태 '이번 달 Claude 사용액',
      본 선별·비교 선별 모두, 응답 토큰 × 공식 가격). 선별 지시문·검색어·★ 기준은 그대로
v2.9: (대표 지시 2026-10-09) 조용히 깨지는 것 막기 — 구글 뉴스가 한 건도 안 들어오면(전체 RSS 실패) news.json을 덮지 않고
     '실패 표시'(soft_fail.txt → 워크플로우 마지막 단계 빨간 X → 낮 점검 알림). 검색어 절반 넘게 실패해도 실패 표시(받은 기사는 반영).
     Claude 선별이 일시 오류(429·5xx·연결·시간 초과)면 1분·3분 뒤 두 번 다시 시도, 그래도 실패하면 실패 표시(신규는 다음 회차 재판정).
     news.json에 수집 결과 status(검색어 수·실패 수·헤드라인 수·선별 결과) 추가. 선별 지시문·검색어·★ 기준은 그대로
v2.8: 국내 유통사 8곳 뉴스 보완(대표 지시 2026-10-09) — 검색어 정리(렉스몬드 새 상호·REXMONDE, 대표 이름, 동명 회사 거르기:
     대림코퍼레이션은 신발 관련어와 함께·DL그룹 제외, 티원글로벌은 병행수입·운동화 등과 함께, 스타인터내셔널은 르까프·스코노 등과 함께),
     국내 유통사만 검색 창 30일·보관 90일(SLOW_GROUPS), 로그에 회사별 검색 건수. '이미 본 기사' 목록을 오래된 것부터 지우게 수정.
     업계지 RSS는 약관(재배포·AI 이용 금지) 때문에 넣지 않음. 판정한 기사 제목을 35일 기억(seen_titles) — 30일 창이 다른 그룹에서
     이미 보여 준 기사(14일 보관 끝)를 '신규'로 다시 가져오지 않게. 기억이 덮는 기간까지만 30일 창을 씀(첫 실행 14일부터 하루씩)
     선별 결과가 '0건'이어도 판정 완료로 기록(전엔 실패와 같이 취급해 같은 기사를 다음 회차에 다시 Claude로 보냄)
v2.7: 네이버 뉴스 검색 제거(대표 지시 2026-10-09) — 네이버 검색 API 특약 개정(2026-09 시행)이 검색 결과를 AI에 넣는 것을
     금지해, 국내 유통사 8곳도 구글 뉴스 RSS만 사용. 네이버 키는 데이터랩(검색어 트렌드, naver_trend.py)에만 씀
v2.6: ① 국내 유통사 8곳은 네이버 뉴스 검색(NAVER API HUB, 검색어 트렌드와 같은 키)도 함께 수집 — 구글 뉴스에 작은 국내 회사 기사가
     적어서(10/6 신규 2건). 권한·키 오류면 [WARN] 후 구글만 사용. ② 산업 '통관·상표권'(customs) 검색어 5개 + 선별 기준
     (병행수입 판례·관세청 단속·상표권 분쟁·직구 통관 규정은 포함). ③ 같은 사건 중복 방지 — 최근 3일 선별 요약을 함께 보내
     같은 사건은 다시 고르지 않게 하고, 제목이 같은 기사(출처만 다른 경우 포함)는 수집 단계에서 하나만 남김
v2.5: ① 국내 비교 회사 21곳 추가 — 유통사 8곳(kr_peer, 트렉시 제외)·국내 패션 브랜드 13곳(kr_fb), 키 = DART 법인 id.
     선별 기준에 국내 비교 회사용 안내(동명 회사 제외, 사업 소식은 포함) 추가. 로그에 국내 비교 그룹별 신규→선별 건수
     ② Haiku 4.5 품질 비교(대표 요청, ~10/13) — 선별은 지금처럼 Sonnet, 같은 헤드라인을 Haiku로도 한 번 더 선별해
     건수·겹침·비용을 news.json model_compare에 남김(화면 반영 없음). 기간이 지나면 자동으로 멈춤
v2.4: 브랜드 21개 추가 — 뉴발란스·우포스·킨·CEP·노르다(스포츠), 드래곤디퓨전·메종키츠네·가니·헌터·
     닥터마틴·핏플랍·락포트·피레넥스·클락스·파라부트·와일드동키·휴먼메이드·에코·단톤·샤카웨어(패션),
     비비안웨스트우드(명품). 호카 검색어에 어그(UGG, 같은 데커스) 포함
v2.3: 소싱 지도 지역 패널용 현지 유통 뉴스 — 프레이저스·잘란도·그루포 SBF, 중동(랜드마크·세노미·
     중동 유통 일반), 남미 유통 일반 검색어 추가
v2.2: Anthropic 401/403·크레딧 소진 시 즉시 실패(워크플로우 빨간 X) — 조용한 무선별 방지
v2.1: 브랜드 그룹(스포츠·아웃도어/패션/명품/유통·그외) 태그 → 대시보드 필터
v2: 범위 확장 — 감시 브랜드 31개사 + 명품 12개 + 산업 카테고리 3종.
    매일 수집, 14일 롤링 보관, 신규 헤드라인만 Claude 선별(비용·일관성),
    카테고리 태그 + 중요도 + 최초 수집일(대시보드 '오늘 신규' 배지).
소스: Google News RSS(무료, 키 불필요) — 한국어/영어 동시 검색
출력: docs/news.json · docs/news_archive.json(v2.12 지난 뉴스 1년 보관 — 대시보드가 검색할 때만 내려받음)
§29-D: 실제 기사 헤드라인만 사용, 관련 뉴스 없으면 빈 목록(임의 생성 금지)
"""

import os
import re
import sys
import json
import time
import base64
import hashlib
import datetime
import subprocess
import email.utils
import urllib.parse
import xml.etree.ElementTree as ET
import requests

API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
KST = datetime.timezone(datetime.timedelta(hours=9))
UA = {"User-Agent": "Mozilla/5.0 (sports-industry-monitor news bot)"}

# ────────────────────────────────────────────────
# ① 브랜드 뉴스 — 감시 대상 (slug: [표시명, 검색어])
#    검색어는 "영문 OR 한글" 한 줄로 (호출 수 절감). 가감 자유.
# ────────────────────────────────────────────────
BRANDS = {
    # ── 스포츠·아웃도어 (sports) ──
    "nike":       ["나이키", "sports", '"Nike" OR 나이키 브랜드'],
    "adidas":     ["아디다스", "sports", '"adidas" OR 아디다스'],
    "on":         ["온홀딩", "sports", '"On Running" OR "On Holding" OR 온러닝'],
    "hoka":       ["호카·어그(데커스)", "sports", '"HOKA" OR "Deckers" OR 호카 OR "UGG" OR 어그부츠'],
    "amer":       ["아머스포츠", "sports", '"Amer Sports" OR "Arc\'teryx" OR "Salomon" OR 아크테릭스 OR 살로몬'],
    "lululemon":  ["룰루레몬", "sports", '"lululemon" OR 룰루레몬'],
    "asics":      ["아식스", "sports", '"ASICS" OR 아식스'],
    "ua":         ["언더아머", "sports", '"Under Armour" OR 언더아머'],
    "vf":         ["VF Corp", "sports", '"VF Corp" OR "The North Face" OR "Vans" OR 노스페이스 OR 반스'],
    "mizuno":     ["미즈노", "sports", '"Mizuno" OR 미즈노'],
    "yonex":      ["요넥스", "sports", '"Yonex" OR 요넥스'],
    "goldwin":    ["골드윈", "sports", '"Goldwin" OR 골드윈'],
    "anta":       ["안타스포츠", "sports", '"Anta Sports" OR 안타스포츠'],
    "lining":     ["리닝", "sports", '"Li-Ning" OR 리닝'],
    "puma":       ["푸마", "sports", '"Puma" OR 푸마 브랜드'],
    "saucony":    ["새코니(울버린)", "sports", '"Saucony" OR "Wolverine World Wide" OR 새코니'],
    "columbia":   ["컬럼비아", "sports", '"Columbia Sportswear" OR 컬럼비아스포츠웨어'],
    "patagonia":  ["파타고니아", "sports", '"Patagonia" OR 파타고니아'],
    "brooks":     ["브룩스", "sports", '"Brooks Running" OR 브룩스러닝'],
    "descente":   ["데상트", "sports", '"Descente" OR 데상트'],
    "skechers":   ["스케쳐스", "sports", '"Skechers" OR 스케쳐스'],
    "newbalance": ["뉴발란스", "sports", '"New Balance" OR 뉴발란스'],
    "oofos":      ["우포스", "sports", '"OOFOS" OR 우포스'],
    "keen":       ["킨(KEEN)", "sports", '"KEEN Footwear" OR "KEEN shoes" OR 킨샌들'],
    "cep":        ["CEP", "sports", '"CEP compression" OR "CEP Sportswear"'],
    "norda":      ["노르다", "sports", '"norda" running OR 노르다'],
    # ── 패션·라이프스타일 (fashion) ──
    "birkenstock":["버켄스탁", "fashion", '"Birkenstock" OR 버켄스탁'],
    "crocs":      ["크록스", "fashion", '"Crocs" OR 크록스'],
    "dragondiffusion": ["드래곤디퓨전", "fashion", '"Dragon Diffusion" OR 드래곤디퓨전'],
    "kitsune":    ["메종키츠네", "fashion", '"Maison Kitsune" OR "Maison Kitsuné" OR 메종키츠네'],
    "ganni":      ["가니", "fashion", '"Ganni"'],
    "hunter":     ["헌터", "fashion", '"Hunter Boots" OR 헌터부츠'],
    "drmartens":  ["닥터마틴", "fashion", '"Dr. Martens" OR "Dr Martens" OR 닥터마틴'],
    "fitflop":    ["핏플랍", "fashion", '"FitFlop" OR 핏플랍'],
    "rockport":   ["락포트", "fashion", '"Rockport shoes" OR "Rockport Group" OR 락포트'],
    "pyrenex":    ["피레넥스", "fashion", '"Pyrenex" OR 피레넥스'],
    "clarks":     ["클락스", "fashion", '"Clarks shoes" OR "Clarks Originals" OR 클락스'],
    "paraboot":   ["파라부트", "fashion", '"Paraboot" OR 파라부트'],
    "wilddonkey": ["와일드동키", "fashion", '"Wild Donkey" OR 와일드동키'],
    "humanmade":  ["휴먼메이드", "fashion", '"Human Made" OR 휴먼메이드'],
    "ecco":       ["에코(ECCO)", "fashion", '"ECCO" 신발 OR "ECCO shoes" OR 에코슈즈'],
    "danton":     ["단톤", "fashion", '"Danton" OR 단톤'],
    "shakawear":  ["샤카웨어", "fashion", '"Shaka Wear" OR 샤카웨어'],
    "ralphlauren":["랄프로렌", "fashion", '"Ralph Lauren" OR 랄프로렌'],   # v2.15 폴로 랄프로렌(RL)
    # ── 명품 (luxury) ──
    "moncler":    ["몽클레르", "luxury", '"Moncler" OR 몽클레르 OR 몽클레어'],   # v2.15 '몽클레어' 표기가 더 많음
    "burberry":   ["버버리", "luxury", '"Burberry" OR 버버리'],
    "prada":      ["프라다/미우미우", "luxury", '"Prada" OR "Miu Miu" OR 프라다 OR 미우미우'],
    "gucci":      ["구찌", "luxury", '"Gucci" OR 구찌'],
    "lv":         ["루이비통", "luxury", '"Louis Vuitton" OR 루이비통'],
    "dior":       ["디올", "luxury", '"Dior" fashion OR 디올'],
    "hermes":     ["에르메스", "luxury", '"Hermès" OR "Hermes" fashion OR 에르메스'],
    "ysl":        ["생로랑", "luxury", '"Saint Laurent" OR 생로랑'],
    "balenciaga": ["발렌시아가", "luxury", '"Balenciaga" OR 발렌시아가'],
    "goldengoose":["골든구스", "luxury", '"Golden Goose" OR 골든구스'],
    "stoneisland":["스톤아일랜드", "luxury", '"Stone Island" OR 스톤아일랜드'],
    "margiela":   ["메종마르지엘라", "luxury", '"Maison Margiela" OR 마르지엘라'],
    "viviennewestwood": ["비비안웨스트우드", "luxury", '"Vivienne Westwood" OR 비비안웨스트우드'],
    "thombrowne": ["톰브라운(제냐)", "luxury", '"Thom Browne" OR "Ermenegildo Zegna" OR 톰브라운'],   # v2.15 본사 제냐(ZGN) 실적 뉴스도(새코니(울버린)처럼)
    # ── 유통·그외 (retail) ──
    "dks":        ["딕스+풋락커", "retail", '"Dick\'s Sporting Goods" OR "Foot Locker" OR 풋락커'],
    "jd":         ["JD스포츠", "retail", '"JD Sports" OR JD스포츠'],
    "academy":    ["아카데미스포츠", "retail", '"Academy Sports"'],
    "taf":        ["애슬릿풋", "retail", '"The Athlete\'s Foot"'],
    "gosport":    ["GO Sport", "retail", '"GO Sport" retail'],
    "gmg":        ["GMG(Sun&Sand)", "retail", '"GMG" Dubai OR "Sun and Sand Sports"'],
    "apparelgrp": ["Apparel Group", "retail", '"Apparel Group" UAE'],
    "alshaya":    ["Alshaya", "retail", '"Alshaya" retail'],
    # ── 소싱 지도 지역 패널용 현지 유통 (v2.3) ──
    "frasers":    ["프레이저스(스포츠다이렉트)", "retail", '"Frasers Group" OR "Sports Direct"'],
    "zalando":    ["잘란도", "retail", '"Zalando"'],
    "sbf":        ["그루포 SBF(센타우로)", "retail", '"Grupo SBF" OR Centauro OR Fisia'],
    "landmark":   ["Landmark Group", "retail", '"Landmark Group" Dubai retail'],
    "cenomi":     ["Cenomi Retail", "retail", '"Cenomi Retail" OR "Alhokair"'],
    "me_retail":  ["중동 유통", "retail", '"Middle East" sportswear retail OR "GCC" fashion retail OR "Saudi" sports retail'],
    "sa_retail":  ["남미 유통", "retail", '"Latin America" sportswear retail OR "Brazil" sneaker market'],
    # ── 국내 비교 유통사 (kr_peer, v2.5) — 키 = DART 법인 id, 트렉시(자사)는 제외 ──
    # v2.8 국내 유통사: 새 상호·대표 이름 추가, 흔한 이름은 업종어와 함께 나올 때만(DART 기업정보로 대표·상호 확인)
    "daelim_corp": ["대림코퍼레이션", "kr_peer", '"대림코퍼레이션" (신발 OR 슈즈 OR 운동화 OR 스니커즈 OR 심건섭) -이해욱 -대림산업 -DL'],
    "rexmond":    ["렉스몬드(오케이몰)", "kr_peer", '렉스몬드 OR REXMONDE OR "오케이몰" OR "장성덕 대표"'],
    "bazig":      ["베이지그", "kr_peer", '"베이지그" OR 뷰라브 OR VURAV'],
    "creed":      ["크리드네트웍스", "kr_peer", '"크리드네트웍스" OR "금윤섭"'],
    "hana_int":   ["한아아이앤티(하하몰)", "kr_peer", '"한아아이앤티" OR "하하몰"'],
    "t1global":   ["티원글로벌", "kr_peer", '"티원글로벌" (병행수입 OR 유경안 OR 운동화 OR 스니커즈 OR 이커머스)'],
    "bbluein":    ["비블루아이앤", "kr_peer", '"비블루아이앤" OR "비블루멀티샵" OR "전명섭 대표"'],
    "starintl":   ["스타인터내셔널", "kr_peer", '"스타인터내셔널" (르까프 OR LECAF OR 스코노 OR 본더치 OR 엘르스포츠 OR 차윤복)'],
    # ── 국내 패션 브랜드 (kr_fb, v2.5) — 더보기 › 패션 브랜드 비교 13곳 ──
    "aubrandz":   ["에이유브랜즈(락피쉬)", "kr_fb", '"에이유브랜즈" OR 락피쉬웨더웨어'],
    "piecepeace": ["피스피스스튜디오(마르디)", "kr_fb", '"피스피스스튜디오" OR 마르디메크르디 OR "마르디 메크르디"'],
    "sjgroup":    ["에스제이그룹(캉골)", "kr_fb", '"에스제이그룹" OR 캉골코리아 OR 캉골'],
    "matinkim":   ["마뗑킴", "kr_fb", '마뗑킴 OR "Matin Kim"'],
    "layer":      ["레이어(마리떼)", "kr_fb", '마리떼프랑소와저버 OR "마리떼 프랑소와 저버"'],
    "highlight":  ["하이라이트브랜즈(코닥)", "kr_fb", '"하이라이트브랜즈" OR 코닥어패럴'],
    "hagohouse":  ["하고하우스", "kr_fb", '"하고하우스"'],
    "bcave":      ["비케이브(커버낫)", "kr_fb", '비케이브 OR 커버낫 OR 와키윌리'],
    "fivespace":  ["파이브스페이스(아더에러)", "kr_fb", '아더에러 OR "Ader Error"'],
    "koza":       ["코자(스탠드오일)", "kr_fb", '스탠드오일 OR "Stand Oil"'],
    "andar":      ["안다르", "kr_fb", '안다르 OR 에코마케팅'],
    "sisun":      ["시선인터내셔널(미샤)", "kr_fb", '"시선인터내셔널" OR 잇미샤'],
    "lowclassic": ["로우클래식", "kr_fb", '로우클래식 OR "Low Classic"'],
}
GROUP_LABEL = {"sports": "스포츠·아웃도어", "fashion": "패션", "luxury": "명품",
               "retail": "유통·그외", "kr_peer": "국내 유통사", "kr_fb": "국내 패션",
               "customs": "통관·상표권", "logistics": "물류·운임"}

# ────────────────────────────────────────────────
# ② 산업 뉴스 — 카테고리별 검색어
# ────────────────────────────────────────────────
INDUSTRY = {
    "sports": ["스포츠·아웃도어 트렌드", [
        '러닝화 시장 OR "running shoe market"',
        '"sportswear industry" OR 스포츠웨어 시장',
        '아웃도어 브랜드 OR "outdoor apparel market"',
        '테니스 OR 골프 OR 피클볼 용품 시장 OR "racket sports boom"',
    ]],
    "fashion": ["패션·명품 시장", [
        '명품 소비 OR "luxury market" OR "luxury demand"',
        '"LVMH" OR "Kering" OR "Richemont" results',
        '패션 브랜드 트렌드 OR "streetwear collaboration"',
        '"sneaker resale" OR 리셀 시장',
    ]],
    "retail": ["멀티브랜드 유통", [
        'ABC마트 OR 슈마커 OR 무신사 스포츠',
        '"sneaker retail" OR "athletic retail" store',
        '"off-price" OR "TJX" OR 오프프라이스 의류',
        '백화점 스포츠 OR 패션 매출',
    ]],
    # v2.6 병행수입 사업에 직접 걸리는 법·통관 소식
    "customs": ["통관·상표권", [
        '병행수입 판결 OR 병행수입 소송 OR 병행수입 상표권',
        '관세청 위조상품 적발 OR 짝퉁 적발 OR 지식재산권 침해 단속',
        '상표권 침해 소송 패션 OR 상표권 분쟁 브랜드',
        '해외직구 통관 OR 목록통관 OR 특송 통관 OR 직구 면세한도',
        '"parallel import" OR "grey market" trademark ruling',
    ]],
    # v2.14 수입 원가·운송기간에 걸리는 물류 소식(더보기 › 물류)
    "logistics": ["물류·운임", [
        '해상운임 OR "컨테이너 운임" OR KCCI OR SCFI',
        '(항공화물 OR 항공운임 OR "항공 화물") (운임 OR 유류할증료 OR 적체)',
        '(호르무즈 OR 홍해 OR 수에즈 OR 희망봉) (컨테이너선 OR 선사 OR 운임 OR 우회)',
        '(선사 OR 해운 OR 수출입) (할증료 OR 운송비용 OR 물류비)',
        '(항만 OR 컨테이너선 OR 선사) (적체 OR 정시율)',
    ]],
}

MAX_PER_QUERY = 10
KEEP_DAYS = 14
# v2.8 국내 유통사는 기사가 드물어(렉스몬드만 월 1~3건) 30일 창으로 찾고 90일 보관 — 이미 본 기사는 다시 판정하지 않음
SLOW_GROUPS = {"kr_peer": (30, 90)}   # group: (검색 창 일, 보관 일)
SEEN_MAX = 8000
SEEN_TITLE_DAYS = 35   # 제목 기억(seen_titles) — 30일 창보다 길게: 다른 그룹에서 이미 보여 준 기사가 14일 보관이 끝난 뒤 다시 들어오지 않게   # 하루 신규 약 80~230건 × 30일 창(국내 유통사)을 덮도록 5000 → 8000
NEWS_PATH = "docs/news.json"
# v2.12 지난 뉴스 검색용 1년 보관 — 선별 기사만(거른 기사 없음), 수집일(first_seen) 기준 365일
ARCHIVE_PATH = "docs/news_archive.json"
ARCHIVE_DAYS = 365
ARCH_KEYS = ("id", "scope", "key", "label", "group", "summary", "importance",
             "title", "link", "source", "pubDate", "first_seen")   # 화면이 쓰는 칸만(category는 안 씀)
ARCH_OPT = ("orig_date", "dchk", "ai_old", "wr")   # v2.13 있을 때만 넣는 칸 — 원문 날짜(화면 날짜)·옛 기사 확인 방법(a Claude·
                                                    # n 글 번호·p 원문)·Claude가 말한 옛 사건 시기@판단일·그누보드 글 번호(호스트/게시판#번호)

# v2.13 옛 기사 거르기 — 구글 뉴스가 지난 기사(몇 년 전 것 포함)를 새 날짜로 다시 내보내는 경우
STALE_GAP = 14        # 원문 날짜가 구글 날짜보다 이 일수 넘게 앞서면 옛 기사(보관 14일과 같음)
STALE_KEEP = 365      # 뺀 기사 제목 기억(일) — 같은 기사가 새 구글 주소로 다시 와도 막음
DATE_BUDGET = 300     # 원문 날짜 확인에 쓰는 시간(초)
DATE_PAUSE = 1.2      # 구글 요청 사이 쉬는 시간(초) — 빠르게 연달아 부르면 429
RUN_LIMIT = 18 * 60   # 실행 시작 뒤 이 시간(초)이 지나면 새 확인을 시작하지 않음(워크플로우 25분 한도 안에 저장)
AI_CHECK_MAX = 1000   # 한 실행에 Claude로 확인할 기사 수(처음 1년 보관분 약 1,500건 점검은 두 번의 실행에 나눔)
AI_CHUNK = 200        # Claude 1회 요청에 넣는 기사 수
SUS_MIN = 2           # 옛 기사가 이만큼(최근 60일) 나온 매체는 남은 기사도 원문 날짜 확인
# 그누보드 게시판(board.php?bo_table=…&wr_id=…) 글 번호 — 글마다 1씩 느는 번호라, 같은 게시판의 최신 번호보다 한참 뒤면 옛 글
# (원문 페이지가 막혀 날짜를 못 읽는 패션포스트 fpost.co.kr·미주조선일보 chosundaily.com이 그누보드 — 2026-10-15 진단)
BOARD_LAG = 0.1       # 최신 번호의 10% 넘게 뒤(그리고 BOARD_LAG_MIN개 넘게)면 옛 글 — 글이 늘어나는 빠르기를 몰라 넉넉히
BOARD_LAG_MIN = 300
BOARD_RATE_MAX = 40   # 게시판 하루 최대 글 수(넉넉히) — 구글 날짜가 며칠 전인 기사는 그동안 늘었을 번호만큼 기준을 넓힘
                      # (1년 보관분 점검 때 수집 당시엔 최신이던 기사를 지금 번호로 옛 글로 보지 않게 — 패션포스트 하루 20~30건)
BOARD_MIN_MAX = 1000  # 최신 번호가 이보다 작은(글이 적은) 게시판은 번호로 판단하지 않음
BOARD_KEEP = 180      # 게시판 최신 번호 기억(일, news.json boards)
BOARD_FRESH_OBS = 5   # '믿을 만한 게시판' = 글을 모두 이만큼 넘게 봤고, BOARD_GROW_DAYS일 넘게 지켜보는 동안 최신 번호가 하루 1개 넘게
                      # 늘었고, 최근 BOARD_GROW_DAYS일 안에 올랐음(새 글이 꾸준히 올라오는 게시판) — 그 게시판에서 번호로 최근 글이면
                      # Claude가 옛 사건이라 해도 남김. 1~2건만 본 게시판이나 새 글이 안 올라오는 옛 게시판은 최신 번호 자체가 옛 글일 수
                      # 있어(10/15 시험 카녜이·구찌 가옥) Claude·매체 근거 규칙으로
BOARD_GROW_DAYS = 7
BOARD_STALE_DAYS = 21 # 최신 번호가 이만큼 안 올랐는데 여러 글이 모두 한참 아래면 번호를 새로 매긴 것으로 보고 다시 잡음(실패 표시)
HOST_SKIP = 3         # 한 실행에서 날짜를 하나도 못 읽고 봇 확인 화면(날짜 없음·403)만 이만큼 나온 곳은 원문 받기를 건너뜀(글 번호만 봄)
TRANSIENT_MAX = 3     # 구글 일시 오류(연결·5xx)가 이만큼 연달아 나면 이번 실행 원문 확인을 멈춤(남은 기사는 다음 실행에서)
NODECODE_ALERT = 3    # 구글 링크를 하나도 못 푼 실행이 이만큼 이어지면 실패 표시(막힘·방식 변경)
AI_REJUDGE_DAYS = 7   # 근거가 부족해 남긴 Claude 판단(ai_old)은 이 기간만 다시 판정(그 뒤엔 남김으로 끝 — 몇 달 뒤 다른 근거 하나로
                      # 정상 기사를 늦게 빼지 않게)
WAVE_MIN = 3          # 원문 날짜 없이 Claude 판단만으로 빼려면 그 매체의 옛 기사 근거(이번 Claude 옛 사건 + 최근 60일 기억)가 이만큼
T0 = time.monotonic()
BROWSER_UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/128.0.0.0 Safari/537.36",
              "Accept-Language": "ko-KR,ko;q=0.9,en;q=0.8"}

# 선별 모델. SHADOW_MODEL은 SHADOW_UNTIL(KST, 포함)까지 같은 헤드라인을 따로 선별해 비교 기록만 남김
MODEL = "claude-sonnet-4-6"
SHADOW_MODEL = "claude-haiku-5-5"   # v2.11 비교 대상(effort low) — 10/21까지
SHADOW_UNTIL = "2026-10-21"
PRICE = {"claude-sonnet-4-6": (3.0, 15.0), "claude-haiku-4-5": (1.0, 5.0), "claude-haiku-5-5": (0.10, 0.50)}   # $/백만 토큰 (입력, 출력)
PRICE_LONG = {"claude-haiku-5-5": (0.50, 2.50)}   # v2.11 입력 10만 토큰 넘는 요청 가격(Haiku 5.5)
EFFORT = {"claude-haiku-5-5": "low"}   # v2.11 모델별 생각 깊이(선별은 분류 작업이라 low)
RETRY_WAITS = (60, 180)   # v2.9 Claude 일시 오류 재시도 간격(초) — 1분·3분 뒤 두 번
SCRIPT = "news_monitor"


def soft_fail(msg):
    """심각한 실패 표시 — 저장은 하되 워크플로우 마지막 단계가 빨간 X로 끝내 점검 알림이 가게 함"""
    print(f"실패 표시: {msg}", flush=True)
    with open("soft_fail.txt", "a", encoding="utf-8") as f:
        f.write(f"{SCRIPT}: {msg}\n")


class TransientAPI(RuntimeError):
    """일시 오류(429·5xx·연결 끊김·시간 초과) — 잠시 뒤 다시 시도할 만한 것"""


# ── Anthropic 호출 공통: 인증/크레딧 오류는 즉시 실패(워크플로우 빨간 X) ──
def _anthropic_once(payload, timeout):
    try:
        resp = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={"x-api-key": API_KEY, "anthropic-version": "2023-06-01",
                     "content-type": "application/json"},
            json=payload, timeout=timeout)
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout,
            requests.exceptions.ChunkedEncodingError) as e:
        raise TransientAPI(f"연결 오류·시간 초과: {type(e).__name__} {str(e)[:150]}") from e
    if resp.status_code in (401, 403) or (resp.status_code == 400 and "credit" in resp.text.lower()):
        print(f"[FATAL] Anthropic API {resp.status_code}: {resp.text[:300]}", flush=True)
        print("[FATAL] 키 만료/무효 또는 크레딧 소진 — console.anthropic.com 확인 후 "
              "GitHub Secret ANTHROPIC_API_KEY 갱신", flush=True)
        raise SystemExit(2)
    if resp.status_code == 429 or resp.status_code >= 500:
        raise TransientAPI(f"Anthropic {resp.status_code}: {resp.text[:200]}")
    if resp.status_code != 200:
        raise RuntimeError(f"Anthropic {resp.status_code}: {resp.text[:200]}")
    data = resp.json()
    count_usage(payload.get("model"), data)
    return data


# ── v2.10 Claude 사용량(수집 상태 '이번 달 Claude 사용액') — 성공한 응답의 토큰 수 × PRICE ──
_USAGE = {"calls": 0, "in": 0, "out": 0, "usd": 0.0}


def count_usage(model, data):
    """성공한 Claude 응답 1건의 토큰·금액을 이번 실행 합계에 더함"""
    u = (data or {}).get("usage") or {}
    tin, tout = int(u.get("input_tokens") or 0), int(u.get("output_tokens") or 0)
    pin, pout = PRICE_LONG[model] if tin > 100_000 and model in PRICE_LONG else PRICE.get(model, (3.0, 15.0))   # v2.11
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


def anthropic_post(payload, timeout=180, waits=RETRY_WAITS):
    """401(키 무효/만료)·403·400 credit(잔액 소진) → SystemExit(2)로 즉시 종료.
    v2.9 일시 오류(429·5xx·연결·시간 초과)는 waits(초) 간격으로 다시 시도. 그 외 오류는 예외로 올려 호출부가 처리."""
    for n in range(len(waits) + 1):
        try:
            return _anthropic_once(payload, timeout)
        except TransientAPI as e:
            if n >= len(waits):
                raise
            print(f"  [WARN] Claude 일시 오류 — {waits[n] // 60}분 뒤 재시도({n + 1}/{len(waits)}): {str(e)[:150]}",
                  flush=True)
            time.sleep(waits[n])


def fetch_rss(query, days=3):
    """Google News RSS: 최근 N일 헤드라인 (한국어 우선, 영문 포함). v2.9 요청·형식 실패면 None(0건과 구분)"""
    q = urllib.parse.quote(f"{query} when:{days}d")
    url = f"https://news.google.com/rss/search?q={q}&hl=ko&gl=KR&ceid=KR:ko"
    items = []
    try:
        r = requests.get(url, headers=UA, timeout=30)
        r.raise_for_status()
        root = ET.fromstring(r.content)
        for it in root.iter("item"):
            title = (it.findtext("title") or "").strip()
            link = (it.findtext("link") or "").strip()
            pub = (it.findtext("pubDate") or "").strip()
            src_el = it.find("source")
            src = (src_el.text or "").strip() if src_el is not None else ""
            if title and link:
                items.append({"title": title, "link": link,
                              "pubDate": pub, "source": src})
            if len(items) >= MAX_PER_QUERY:
                break
    except Exception as e:
        print(f"  [WARN] RSS 실패({query[:30]}): {str(e)[:100]}")
        return None
    return items


def item_id(title, link):
    return hashlib.md5((title.strip().lower() + "|" + link).encode()).hexdigest()[:12]


def title_key(title):
    """같은 기사 판별용 제목 키 — 구글 뉴스의 ' - 매체명' 꼬리와 기호·공백을 뺀 앞 40자"""
    t = re.sub(r"\s+-\s+[^-]{1,40}$", "", title or "")
    return re.sub(r"[^0-9a-z가-힣]", "", t.lower())[:40]


def collect(known_titles=frozenset(), slow_days=None):
    """수집 → {id: {…, scope, key}} (scope=brand/industry, key=slug/category).
    known_titles: 보관 중·최근 판정한 기사 제목 키 — 같은 제목은 출처가 달라도 다시 넣지 않음.
    slow_days: 느린 그룹(국내 유통사) 검색 창 — 제목 기억이 덮는 기간을 넘지 않게 호출 쪽에서 줄임.
    v2.9 반환 (raw, st) — st = {queries: 검색어 수, failed: 실패한 검색어, headlines: 중복 제거 전 받은 헤드라인 수}"""
    raw, titles = {}, set(known_titles)
    st = {"queries": 0, "failed": [], "headlines": 0}

    def rss(q, days=3):
        st["queries"] += 1
        got = fetch_rss(q, days=days)
        if got is None:
            st["failed"].append(q)
            return []
        st["headlines"] += len(got)
        return got

    def add(it, **meta):
        tk = title_key(it["title"])
        if tk and tk in titles:
            return False
        iid = item_id(it["title"], it["link"])
        if iid in raw:
            return False
        titles.add(tk)
        raw[iid] = {**it, "id": iid, **meta}
        return True

    slow = []
    for slug, (name, grp, q) in BRANDS.items():
        got = rss(q, days=min(SLOW_GROUPS[grp][0], slow_days or SLOW_GROUPS[grp][0]) if grp in SLOW_GROUPS else 3)
        added = sum(add(it, scope="brand", key=slug, label=name, group=grp) for it in got)
        if grp in SLOW_GROUPS:
            slow.append(f"{name} {len(got)}건(새 제목 {added})")
        time.sleep(0.7)
    if slow:
        print(f"국내 유통사 검색(최근 {min(SLOW_GROUPS['kr_peer'][0], slow_days or 99)}일): " + " · ".join(slow), flush=True)
    for cat, (label, queries) in INDUSTRY.items():
        for q in queries:
            for it in rss(q):
                add(it, scope="industry", key=cat, label=label, group=cat)
            time.sleep(0.7)
    print(f"수집 {len(raw)}건 (중복 제거 후)"
          + (f" · 검색어 {st['queries']}개 중 실패 {len(st['failed'])}개" if st["failed"] else ""), flush=True)
    return raw, st


def claude_curate(new_items, model=MODEL, recent=(), waits=RETRY_WAITS):
    """신규 헤드라인만 선별·요약. recent: 최근 선별 요약(같은 사건 재선별 방지). waits: 일시 오류 재시도 간격(초).
    반환 ({id: {summary, importance, category}}, 사용량 {model, in, out, usd})"""
    lines = []
    for it in new_items.values():
        lines.append(f"[{it['id']}] ({it['scope']}/{it['key']}/{it.get('group', '')}) {it['title']} "
                     f"— {it['source']}, {it['pubDate'][:16]}")
    corpus = "\n".join(lines)
    recent_txt = "\n".join(f"- {r}" for r in recent) or "(none)"
    prompt = f"""You curate daily news for a Korean company that does parallel import
and multi-brand distribution of sports, outdoor, fashion and luxury brands.

Below are headlines collected in the last few days, each tagged with
(scope/key/group): scope is brand or industry.

SELECT only items that matter for that business: brand distribution/licensing
changes, market entry/exit (especially Korea/Asia), store expansion/closures,
ownership/management changes, restructuring, earnings or demand signals,
pricing/discount pressure, inventory issues, notable collaborations or category
strategy, retail channel shifts, consumer trend shifts.
EXCLUDE: product reviews, promotions/sales ads, sports match results, celebrity
outfit gossip, unrelated namesakes, tariff/FX/policy items (handled elsewhere) —
except items tagged industry/customs or industry/logistics (below).

Items tagged industry/customs matter directly to a parallel importer: include
court rulings or disputes on parallel imports and trademarks (fashion, sports,
luxury, eyewear brands), customs enforcement (counterfeit seizures, inspections
of imported goods), and changes to import clearance or overseas direct-purchase
rules (duty-free limits, list clearance). Exclude trademark cases in unrelated
industries (food, pharma, IT) and general trade/tariff policy.

Items tagged industry/logistics matter because the company imports goods into
Korea by sea and air: include ocean or air freight rate moves (KCCI, SCFI,
Drewry, Korea Customs monthly freight-cost releases), disruptions on routes to
Korea (Strait of Hormuz, Red Sea / Bab el-Mandeb, Suez vs Cape of Good Hope
rerouting, Middle East airspace closures), carrier surcharges (war-risk,
emergency, fuel), port congestion and schedule reliability. Exclude shipping or
airline stock-price and earnings items without freight-rate content,
shipbuilding orders, crude-oil price items without a freight angle, domestic
parcel/courier labor news, and general geopolitics without a logistics impact.

DUPLICATES: when several headlines report the same event, select only the most
informative one. Do not select an event that already appears in RECENTLY
SELECTED below, unless the headline adds a material new development.

Korean peer companies (group kr_peer = small Korean parallel-import / online
distributors competing directly with this company; group kr_fb = Korean fashion
brand companies it benchmarks): include genuine business news about that exact
company or its brands (earnings, funding/IPO, new brand deals, mall or store
launches, overseas expansion, M&A, management changes, lawsuits, customs or
trademark issues). Exclude other companies that merely share the name, and pure
product promotions or celebrity items.

For each selected item: one-sentence Korean summary faithful to the headline
(never invent facts), importance 1-3 (3 = strategic/urgent), and a category
from: brand, sports, fashion, retail, customs, logistics.

Respond with ONLY a JSON object, no markdown fences:
{{
  "<id>": {{"summary": "한국어 한 문장", "importance": 1|2|3,
            "category": "brand|sports|fashion|retail|customs|logistics"}}
}}
Omit ids that should not be selected. If nothing qualifies, return {{}}.

RECENTLY SELECTED (last 3 days, for duplicate checking only):
{recent_txt}

HEADLINES:
{corpus}"""
    payload = {"model": model, "max_tokens": 12000 if model in EFFORT else 6000,   # v2.11 Haiku 5.5는 생각 토큰도 max_tokens에 들어감
               "messages": [{"role": "user", "content": prompt}]}
    if model in EFFORT:
        payload["output_config"] = {"effort": EFFORT[model]}
    data = anthropic_post(payload, timeout=240, waits=waits)
    parts = data.get("content", [])
    text = "".join(p.get("text", "") for p in parts if p.get("type") == "text")
    text = re.sub(r"```json|```", "", text).strip()
    try:
        picked = json.loads(text)
    except json.JSONDecodeError:
        # 앞뒤에 설명 문장이 붙은 경우: 첫 '{'부터 JSON 객체 하나만 읽음
        picked, _ = json.JSONDecoder().raw_decode(text[text.index("{"):])
    if not isinstance(picked, dict):
        raise ValueError("선별 응답이 JSON 객체가 아님")
    u = data.get("usage") or {}
    tin, tout = int(u.get("input_tokens") or 0), int(u.get("output_tokens") or 0)
    pin, pout = PRICE_LONG[model] if tin > 100_000 and model in PRICE_LONG else PRICE.get(model, (0.0, 0.0))
    usage = {"model": model, "in": tin, "out": tout,
             "usd": round((tin * pin + tout * pout) / 1e6, 4),
             "stop": data.get("stop_reason", "")}
    if usage["stop"] == "max_tokens":
        print(f"  [WARN] {model} 응답이 max_tokens에서 잘림 — 일부 선별 누락 가능", flush=True)
    return picked, usage


def compare_models(new_items, picked, usage, today, recent=()):
    """SHADOW_MODEL로 같은 헤드라인을 한 번 더 선별해 비교 기록(화면 반영 없음). 실패해도 본 선별에는 영향 없음.
    v2.9 비교용이라 재시도하지 않음(실행 시간 25분 한도 안에 본 선별 재시도 몫을 남김)"""
    try:
        shadow, su = claude_curate(new_items, SHADOW_MODEL, recent, waits=())
    except (Exception, SystemExit) as e:
        print(f"  [WARN] 모델 비교({SHADOW_MODEL}) 실패 — 건너뜀: {str(e)[:150]}", flush=True)
        return None
    a = {k for k in picked if k in new_items}
    b = {k for k in shadow if k in new_items}
    imp = lambda sel, ids: [sum(1 for k in ids if int((sel.get(k) or {}).get("importance", 1) or 1) == n)
                            for n in (1, 2, 3)]
    row = lambda k, sel: {"id": k, "key": new_items[k]["key"], "title": new_items[k]["title"][:120],
                          "summary": str((sel.get(k) or {}).get("summary", ""))[:120],
                          "importance": int((sel.get(k) or {}).get("importance", 1) or 1)}
    rec = {"date": today.isoformat(), "new": len(new_items), "both": len(a & b),
           "primary": {**usage, "n": len(a), "imp": imp(picked, a)},
           "shadow": {**su, "n": len(b), "imp": imp(shadow, b)},
           "only_primary": [row(k, picked) for k in sorted(a - b)][:25],
           "only_shadow": [row(k, shadow) for k in sorted(b - a)][:25],
           "imp_diff": sum(1 for k in a & b if int(picked[k].get("importance", 1) or 1)
                           != int(shadow[k].get("importance", 1) or 1))}
    print(f"모델 비교: {MODEL} {len(a)}건(${usage['usd']}) · {SHADOW_MODEL} {len(b)}건(${su['usd']}) · "
          f"겹침 {len(a & b)}건 · 중요도 다름 {rec['imp_diff']}건", flush=True)
    return rec


# ── v2.13 옛 기사 거르기 ──
# 구글 뉴스 RSS 날짜(pubDate)는 구글이 다시 색인한 날이라, 사이트를 옮긴 매체의 지난 기사가 '최근 기사'로 들어옴.
# 구글 링크 → 원문 주소(구글 뉴스 내부 요청 — 공식 방법 아님) → 원문 페이지 발행일. 못 읽으면 Claude가 옛 사건이라고 확신한 것만 옛 기사
GN_RPC = "https://news.google.com/_/DotsSplashUi/data/batchexecute"
GN_CTX = [["X", "X", ["X", "X"], None, None, 1, 1, "US:en", None, 1, None, None, None, None, None, 0, 1],
          "X", "X", 1, [1, 1, 1], 1, 1, None, 0, 0, None, 0]
# 발행일 메타 — 수정일(article:modified_time·dateModified)과 뜻이 모호한 name="date"는 안 씀
PUB_META = {"article:published_time", "og:article:published_time", "og:published_time", "og:regdate", "datepublished",
            "pubdate", "publishdate", "publish_date", "publish-date", "dc.date.issued", "dcterms.created",
            "parsely-pub-date", "sailthru.date"}
# 기사 머리의 '입력 2019.10.23 10:00' 같은 표시(사이에 태그 4개까지) — 등록·승인·작성은 시각이 붙은 것만
# (바닥글 '등록일 2008.04.01'·'등록 승인 2008.04.01'은 신문 등록일). 머리의 '오늘 날짜'처럼 이름표 없는 날짜는 안 봄
PUB_LABEL = re.compile(r"(입력|송고|승인|등록|작성)\s*(?:일시|시간|일자|일)?\s*[:：]?\s*(?:<[^>]{0,200}>\s*){0,4}"
                       r"((?:19|20)\d\d\s*[-./년]\s*\d\d?\s*[-./월]\s*\d\d?)"
                       r"(\s*(?:일|\.)?\s*(?:\([월화수목금토일]\))?\s*(?:오전|오후)?\s*\d\d?:\d\d)?")


class GBlocked(Exception):
    """구글이 막음(429·google.com/sorry·consent) — 이번 실행은 원문 확인을 멈춤(다음 실행에서 다시)"""


class GTransient(Exception):
    """구글 일시 오류(5xx 등) — 이 기사는 확인 안 한 것으로 두고 다음 실행에서 다시"""


class SlowRead(Exception):
    """받는 데 total초가 넘음(조금씩 흘려보내는 곳) — 잘린 페이지를 다 받은 것처럼 쓰지 않게"""


def _get_capped(url, cap, total=25):
    """GET(연결 5초·읽기 15초, 넘겨주기 따라감) — 본문은 cap 바이트·전체 total초까지만(조금씩 흘려보내는 곳 대비) → (응답, 본문 바이트)"""
    t0 = time.monotonic()
    with requests.get(url, headers=BROWSER_UA, timeout=(5, 15), stream=True) as r:
        buf = bytearray()
        if hasattr(r.raw, "read1"):   # 한 번에 받은 만큼만 읽어 시간 제한을 자주 확인(길이를 미리 알리는 느린 곳도)
            while len(buf) < cap:
                if time.monotonic() - t0 > total:
                    raise SlowRead(f"{total}초 넘음({len(buf):,}바이트)")
                chunk = r.raw.read1(16384, decode_content=True)
                if not chunk:
                    break
                buf += chunk
        else:
            for chunk in r.iter_content(16384):
                buf += chunk
                if len(buf) >= cap:
                    break
                if time.monotonic() - t0 > total:
                    raise SlowRead(f"{total}초 넘음({len(buf):,}바이트)")
        return r, bytes(buf[:cap])


def _gn_old(aid):
    """2024년 전 형식 구글 링크 — base64 안에 원문 주소(08 13 22 <길이> <주소>). 새 형식(AU_yqL…)이면 None"""
    try:
        b = base64.urlsafe_b64decode(aid + "=" * (-len(aid) % 4))
    except ValueError:
        return None
    m = re.match(rb"(?:\x08[\x80-\xff]*[\x00-\x7f])?\x22([\x80-\xff]*[\x00-\x7f])", b)
    if not m:
        return None
    n = sum((c & 0x7F) << 7 * k for k, c in enumerate(m.group(1)))
    u = b[m.end():m.end() + n].decode("utf-8", "ignore")
    return u if u.startswith("http") else None


def is_gn_link(link):
    return bool(re.search(r"news\.google\.com/(?:rss/)?(?:articles|read)/[\w-]+", link or ""))


def gn_resolve(link):
    """구글 뉴스 링크 → 원문 주소(못 풀면 None, 구글이 막으면 GBlocked). 새 형식은 /rss/articles/ 페이지(약 600KB — 끝부분)의
    서명(data-n-a-sg)·시각(data-n-a-ts)으로 batchexecute 요청. /articles/·/read/ 주소는 google.com/sorry로 보내서 안 씀.
    서명은 매번 바뀌어 저장하지 않음"""
    m = re.search(r"news\.google\.com/(?:rss/)?(?:articles|read)/([\w-]+)", link or "")
    if not m:
        return None
    aid = m.group(1)
    old = _gn_old(aid)
    if old:
        return old
    try:
        r, page = _get_capped(f"https://news.google.com/rss/articles/{aid}?hl=ko&gl=KR&ceid=KR:ko", 2_000_000)
    except SlowRead as e:   # 잘린 구글 페이지는 서명이 끝부분에 있어 '모르는 기사'로 오판 — 일시 오류로 다음 실행에서 다시
        raise GTransient(str(e)) from e
    host = (urllib.parse.urlparse(r.url).hostname or "").lower()
    if r.status_code == 429 or (host != "news.google.com" and (host == "google.com" or host.endswith(".google.com"))):
        raise GBlocked(f"{r.status_code} {host}")
    if host != "news.google.com":
        return r.url   # 구글이 바로 원문으로 넘겨줌(원문 쪽 오류는 page_date가 처리)
    if r.status_code == 404:
        return None   # 구글이 모르는 기사 — 다시 해도 같음
    if r.status_code != 200:
        raise GTransient(f"HTTP {r.status_code}")
    sg, ts = re.search(rb'data-n-a-sg="([^"]+)"', page), re.search(rb'data-n-a-ts="(\d+)"', page)
    if not (sg and ts):
        return None
    inner = json.dumps(["garturlreq", GN_CTX, aid, int(ts.group(1)), sg.group(1).decode()], separators=(",", ":"))
    p = requests.post(GN_RPC, timeout=(5, 15),
                      headers={**BROWSER_UA, "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"},
                      data="f.req=" + urllib.parse.quote(json.dumps([[["Fbv4je", inner, None, "generic"]]],
                                                                    separators=(",", ":"))))
    if p.status_code == 429:
        raise GBlocked("batchexecute 429")
    if p.status_code != 200:
        raise GTransient(f"batchexecute HTTP {p.status_code}")
    for line in p.text.splitlines():   # )]}' 다음 줄: [["wrb.fr","Fbv4je","[\"garturlres\",\"<원문 주소>\",1]",…],…]
        if not (line.startswith("[[") and "garturlres" in line):
            continue
        try:
            rows = json.loads(line)
        except ValueError:
            continue
        for row in rows:
            if not (isinstance(row, list) and len(row) > 2 and isinstance(row[2], str) and "garturlres" in row[2]):
                continue
            try:
                res = json.loads(row[2])
            except ValueError:
                continue
            if isinstance(res, list) and len(res) > 1 and isinstance(res[1], str) and res[1].startswith("http"):
                return res[1]
    return None


def _to_date(s, today=None):
    """날짜 글자 → 한국 날짜(1995년 전·내일 뒤·못 읽으면 None). ISO 8601(Z·+09:00)·2019.10.23 10:00·2019년 10월 23일·
    20191023100035(다음 og:regDate)·RFC 2822·유닉스 초. 시간대가 없으면 한국 시각으로 봄"""
    s = (s or "").strip()
    today = today or datetime.datetime.now(KST).date()
    try:
        if re.fullmatch(r"\d{10}(\d{3})?", s):
            t = datetime.datetime.fromtimestamp(int(s[:10]), KST)
        elif re.match(r"[A-Za-z]{3},", s):
            t = email.utils.parsedate_to_datetime(s)
        else:
            y, mo, d, hh, mi, tz = re.search(
                r"((?:19|20)\d\d)\s*[-./년]?\s*(\d\d?)\s*[-./월]?\s*(\d\d?)(?:[^\d+Z-]{0,4}(\d\d?):?(\d\d)(?::?\d\d)?"
                r"(?:\.\d+)?\s*(Z|[+-]\d\d:?\d\d)?)?", s).groups()
            z = (datetime.timezone.utc if tz == "Z" else
                 datetime.timezone(datetime.timedelta(hours=int(tz[:3]), minutes=int(tz[0] + tz[-2:]))) if tz else KST)
            t = datetime.datetime(int(y), int(mo), int(d), int(hh or 0), int(mi or 0), tzinfo=z)
        day = (t if t.tzinfo else t.replace(tzinfo=KST)).astimezone(KST).date()
    except (ValueError, TypeError, OverflowError, AttributeError, IndexError):
        return None
    return day if datetime.date(1995, 1, 1) <= day <= today + datetime.timedelta(days=1) else None


def _date_in_url(u):
    """주소 속 날짜 — /2019/10/23/ · AKR20191023… · NISX20191023_… · no=2019102310… (8자리 기사 번호만 있는 것은 안 봄)"""
    m = (re.search(r"/((?:19|20)\d\d)[/-](\d\d)[/-](\d\d)(?:[/_.-]|$)", u or "")
         or re.search(r"(?:[/=_-]|[A-Za-z])((?:19|20)\d\d)(\d\d)(\d\d)(?:\d{2,14}(?!\d)|_\d)", u or ""))
    return _to_date("-".join(m.groups())) if m else None


def _page_html(r, raw):
    """응답 바이트 → 글자(헤더·<meta charset>의 문자 집합, EUC-KR 계열은 cp949)"""
    cs = re.search(r"charset=[\"']?([\w-]+)", (r.headers.get("content-type") or "") + raw[:4096].decode("ascii", "ignore"))
    enc = (cs.group(1) if cs else "utf-8").lower()
    try:
        return raw.decode("cp949" if enc in ("euc-kr", "ks_c_5601-1987", "ksc5601", "x-windows-949") else enc, "replace")
    except (LookupError, UnicodeError):   # 모르는 문자 집합·charset=undefined 같은 잘못된 이름
        return raw.decode("utf-8", "replace")


def _html_dates(html):
    """페이지 속 발행일 후보 [(어디서, 날짜 글자)] — 발행일 메타 1개(없으면 JSON-LD datePublished) + 처음 나온 이름표 1개"""
    found = []
    for tag in re.findall(r"<meta\b[^>]{0,600}>", html, re.I):   # 속성 순서는 제각각(content=가 먼저 오기도)
        a = {k.lower(): v for k, v in re.findall(r'([\w:.-]+)\s*=\s*["\']([^"\']*)["\']', tag)}
        if (a.get("property") or a.get("name") or a.get("itemprop") or "").lower() in PUB_META and _to_date(a.get("content")):
            found.append(("meta", a["content"]))
            break
    if not found:   # JSON-LD는 메타가 없을 때만(관련 기사 목록의 날짜가 섞일 수 있음)
        m = re.search(r'"datePublished"\s*:\s*"([^"]{8,40})"', html)
        if m:
            found.append(("jsonld", m.group(1)))
    for lb in PUB_LABEL.finditer(re.sub(r"\s+", " ", html)):   # 페이지에서 처음 나온 이름표 1개(긴 공백은 하나로 — 정규식이 오래 돌지 않게)
        if lb.group(1) in ("입력", "송고") or lb.group(3):
            found.append(("label", lb.group(2)))
            break
    return found


def page_date(url, cap=1_000_000, info=None):
    """원문 페이지 발행일(한국 날짜) — 발행일 메타(없으면 JSON-LD datePublished)와 첫 '입력·송고(등록·승인·작성은 시각까지)' 표시 중
    이른 것(사이트를 옮겨 메타만 옮긴 날로 바뀐 경우). 둘 다 없거나 못 받으면 주소 속 날짜, 그것도 없으면 None.
    info(dict)를 주면 못 읽은 까닭(why: err:오류 이름·http상태·url(주소 날짜)·nodate)·최종 주소를 적음 — 로그의 매체별 요약용"""
    info = {} if info is None else info
    try:
        r, raw = _get_capped(url, cap)
    except Exception as e:
        info.update(why=f"err:{type(e).__name__}", host=urllib.parse.urlparse(url).hostname or "")
        return _date_in_url(url)
    info.update(host=urllib.parse.urlparse(r.url or url).hostname or "", status=r.status_code, bytes=len(raw))
    if not r.ok:
        info["why"] = f"http{r.status_code}"
        return _date_in_url(r.url or url)
    try:
        days = [d for d in (_to_date(v) for _, v in _html_dates(_page_html(r, raw))) if d]
    except Exception as e:   # 페이지 하나가 이상해도 전체 확인은 계속
        info["why"] = f"err:parse:{type(e).__name__}"
        return _date_in_url(r.url or url)
    if days:
        info["why"] = "page"
        return min(days)
    d = _date_in_url(r.url or url)
    info["why"] = "url" if d else "nodate"
    return d


def rss_day(it):
    """구글이 붙인 날짜(pubDate)의 한국 날짜 — 못 읽으면 수집일"""
    try:
        t = email.utils.parsedate_to_datetime(str(it.get("pubDate") or ""))
        return (t if t.tzinfo else t.replace(tzinfo=datetime.timezone.utc)).astimezone(KST).date()
    except (TypeError, ValueError, IndexError, OverflowError):
        pass
    try:
        return datetime.date.fromisoformat(str(it.get("first_seen") or "")[:10])
    except ValueError:
        return datetime.datetime.now(KST).date()


def ai_old_check(items, today, model=MODEL):
    """Claude 짧은 확인(선별 지시문과 따로) — 헤드라인이 그해 전에 이미 일어난 '그 사건'인지.
    반환 {id: (사건 시기 'YYYY-MM' 또는 'YYYY', 근거)} — 확신하는 것만. 실패하면 예외(다음 실행에서 다시)"""
    ids = {it["id"] for it in items}
    lines = "\n".join(f"[{it['id']}] {str(it.get('title', ''))[:200]} — {str(it.get('source', ''))[:40]}" for it in items)
    prompt = f"""Today is {today.isoformat()} (KST). Google News listed the headlines below as published in
the last few days, but it sometimes re-dates articles that are months or years old.

Flag a headline only if it reports one specific event (the same company AND the same people, deal,
store or figures) that you know for certain already happened before {today.year} - for example an
executive appointment or departure, an acquisition or sale, a store opening, a court ruling, or a
quarterly result with the same figures that you remember from an earlier year.
Do NOT flag recurring kinds of news that could happen again (price increases, collaborations,
openings, results) unless the details match a specific past event you remember.
Your knowledge may end well before today: an event that was announced or planned earlier (a store
closing on a set date, an executive leaving later, a deal closing later, a board appointment) may be
happening only now - do not flag a headline about it taking place. If unsure, do not flag.

Respond with ONLY a JSON object, no markdown fences:
{{"old": [{{"id": "<id>", "when": "YYYY-MM or YYYY (when that event happened)", "why": "짧은 한국어 근거(30자 이내)"}}]}}
Return {{"old": []}} if none.

HEADLINES:
{lines}"""
    payload = {"model": model, "max_tokens": 12000 if model in EFFORT else 4000,
               "messages": [{"role": "user", "content": prompt}]}
    if model in EFFORT:
        payload["output_config"] = {"effort": EFFORT[model]}
    data = anthropic_post(payload, timeout=150, waits=())   # 재시도 없음 — 실패하면 다음 실행에서 다시
    if data.get("stop_reason") == "max_tokens":
        raise ValueError("옛 기사 확인 응답이 max_tokens에서 잘림")
    text = "".join(p.get("text", "") for p in data.get("content", []) if p.get("type") == "text")
    text = re.sub(r"```json|```", "", text).strip()
    try:
        d = json.loads(text)
    except json.JSONDecodeError:
        d, _ = json.JSONDecoder().raw_decode(text[text.index("{"):])
    if not isinstance(d, dict) or not isinstance(d.get("old", []), list):
        raise ValueError("옛 기사 확인 응답이 {old: [...]} 모양이 아님")
    out = {}
    for o in d.get("old") or []:
        if not isinstance(o, dict) or o.get("id") not in ids:
            continue
        m = re.match(r"((?:19|20)\d\d)(?:[-./](\d\d?))?", str(o.get("when") or o.get("year") or "").strip())
        if not m or int(m.group(1)) > today.year:
            continue
        mo = int(m.group(2)) if m.group(2) and 1 <= int(m.group(2)) <= 12 else None
        out[o["id"]] = (f"{m.group(1)}-{mo:02d}" if mo else m.group(1), str(o.get("why") or "").strip()[:60])
    return out


def ai_stale(when, gday):
    """Claude가 말한 사건 시기(YYYY-MM 또는 YYYY)가 구글 날짜보다 STALE_GAP+31일 넘게 앞서면 옛 기사
    (달 단위라 한 달 넉넉히 — 달이 없으면 그해 마지막 날로 봄)"""
    y, _, mo = str(when).partition("-")
    try:
        ev = datetime.date(int(y), int(mo), 1) if mo else datetime.date(int(y), 12, 31)
    except ValueError:
        return False
    return (gday - ev).days > STALE_GAP + 31


def load_stale(old, today):
    """옛 기사 제목 기억(news.json stale_titles) {제목 키: [원문 날짜·사건 시기·글 번호, 찾은 날, 방법(p 원문·n 글 번호·a Claude), 매체,
    원문 호스트]}
    — STALE_KEEP일 지난 것·모양이 틀린 것은 뺌"""
    cut = (today - datetime.timedelta(days=STALE_KEEP)).isoformat()
    st = old.get("stale_titles") if isinstance(old, dict) else None
    out = {}
    for k, v in (st.items() if isinstance(st, dict) else ()):
        if (isinstance(k, str) and k and isinstance(v, list) and len(v) >= 4 and isinstance(v[1], str)
                and re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", v[1]) and v[1] >= cut):
            out[k] = [str(x) for x in v[:5]]   # [원문 날짜·사건 시기·글 번호, 찾은 날, 방법, 매체(, 원문 호스트)]
    return out


def board_post(url):
    """그누보드 게시판 주소(…/board.php?bo_table=게시판&wr_id=글 번호) → ('호스트/게시판', 글 번호), 아니면 None"""
    u = urllib.parse.urlparse(url or "")
    if not u.path.endswith("board.php"):
        return None
    q = urllib.parse.parse_qs(u.query)
    bo, wr = (q.get("bo_table") or [""])[0], (q.get("wr_id") or [""])[0]
    if not (re.fullmatch(r"[\w-]{1,40}", bo) and re.fullmatch(r"[1-9][0-9]{0,8}", wr)):
        return None
    return f"{(u.hostname or '').lower().removeprefix('www.')}/{bo}", int(wr)


def load_boards(old, today):
    """게시판 최신 글 번호 기억(news.json boards) {'호스트/게시판': [최신 번호, 그 번호로 오른 날, 지금까지 본 글 수,
    처음 기억한 번호, 처음 기억한 날]} — 처음 값과 비교해 새 글이 꾸준히 올라오는 게시판인지 봄. BOARD_KEEP일 지난 것·이상한 값은 뺌"""
    cut = (today - datetime.timedelta(days=BOARD_KEEP)).isoformat()
    b = old.get("boards") if isinstance(old, dict) else None
    isint = lambda v: isinstance(v, int) and not isinstance(v, bool)
    out = {}
    for k, v in (b.items() if isinstance(b, dict) else ()):
        isday = lambda d: isinstance(d, str) and re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", d)
        if (isinstance(k, str) and "/" in k and isinstance(v, list) and len(v) in (2, 3, 5) and isint(v[0]) and v[0] > 0
                and isday(v[1]) and v[1] >= cut and (len(v) == 2 or (isint(v[2]) and v[2] >= 0))
                and (len(v) < 5 or (isint(v[3]) and 0 < v[3] <= v[0] and isday(v[4]) and v[4] <= v[1]))):
            out[k] = [v[0], v[1], v[2] if len(v) >= 3 else 0] + ([v[3], v[4]] if len(v) == 5 else [v[0], v[1]])
    return out


def verified_fresh(it):
    """원문 날짜로 수집 때 최근 기사였음이 확인된 기사(수집일 - 원문 날짜 ≤ STALE_GAP+1일) — 같은 제목의 옛 사본을 뺄 때 함께 빼지 않음"""
    try:
        od = datetime.date.fromisoformat(str(it.get("orig_date") or ""))
        fs = datetime.date.fromisoformat(str(it.get("first_seen") or ""))
    except ValueError:
        return False
    return 0 <= (fs - od).days <= STALE_GAP + 1


def _imp(it):
    try:
        return min(3, max(1, int(it.get("importance") or 1)))
    except (TypeError, ValueError, OverflowError):
        return 1


def date_check(kept, base, today, stale, boards=None):
    """오늘·최근 선별 기사와 보관 중 기사(news.json·1년 보관)의 옛 기사 확인 → (옛 기사 id 집합, 상태).
    기사에 dchk(확인한 방법: a = Claude, p = 원문 페이지)·orig_date(원문 날짜)·ai_old(Claude가 말한 옛 사건 시기 — 아직 못 가린 것)를
    적고, 옛 기사는 stale(제목 키 기억)에 넣음. boards(그누보드 게시판 최신 번호)도 고침.
    ① Claude(지난 기사): 최근 이틀 선별이 아니고 a도 원문 날짜도 없는 기사 — news.json → 1년 보관 순, 한 실행 AI_CHECK_MAX건
    ② 원문: p가 없는 기사 중 오늘 선별 → Claude 옛 사건 → 최근 이틀 선별 → 옛 기사가 나온 매체(이름·원문 호스트), DATE_BUDGET초 안에서.
       원문 날짜가 구글 날짜보다 STALE_GAP일 넘게 앞서면 옛 기사(원문 날짜가 Claude보다 우선, 구글 날짜보다 늦은 원문 날짜는 안 믿음)
    ②-2 원문 날짜를 못 읽은 그누보드 게시판 글은 글 번호로 — 최신 번호보다 BOARD_LAG 넘게 뒤면 옛 기사. 믿을 만한 게시판에서
       번호로 옛 글이 아니면 Claude 판단은 쓰지 않음
    ③ Claude(최근 선별): 원문 날짜를 못 읽은 것만(비용 — 원문 날짜가 있으면 묻지 않음)
    ④ 남은 Claude 옛 사건(지난 실행 것 포함)은 그 매체에 옛 기사 근거가 WAVE_MIN건 넘을 때만 뺌(한두 건은 Claude 착각일 수 있어 남김)"""
    pool = {}   # id → 같은 기사의 사본들(news.json·보관 파일 — 확인 결과를 모두에 적음)
    for it in list(kept) + list(base or []):
        if isinstance(it, dict) and isinstance(it.get("id"), str) and isinstance(it.get("title"), str):
            pool.setdefault(it["id"], []).append(it)
    ck = lambda i: {c for x in pool[i] for c in str(x.get("dchk") or "") if c in "anp"}
    has_od = lambda i: any(isinstance(x.get("orig_date"), str) and x["orig_date"] for x in pool[i])
    src = lambda i: str(pool[i][0].get("source") or "")
    norm = lambda h: str(h or "").lower().removeprefix("www.")

    def mark(i, c=None, **kv):
        for x in pool[i]:
            if c:
                x["dchk"] = "".join(sorted(({ch for ch in str(x.get("dchk") or "") if ch in "anp"}) | {c}))
            for k2, v2 in kv.items():
                if v2 is None:
                    x.pop(k2, None)
                else:
                    x[k2] = v2

    in_kept = {it["id"] for it in kept if isinstance(it, dict)}
    tod = today.isoformat()
    rcut = (today - datetime.timedelta(days=2)).isoformat()
    tier = {i: 0 if i in in_kept and str(pool[i][0].get("first_seen") or "") >= rcut else 1 if i in in_kept else 2
            for i in pool}
    order = sorted(sorted(pool), key=lambda i: (str(pool[i][0].get("first_seen") or ""), _imp(pool[i][0])), reverse=True)
    order.sort(key=lambda i: tier[i])   # 최근 선별 → news.json → 1년 보관(각각 최신·별점 순, 같으면 id 순)
    pos = {i: k for k, i in enumerate(order)}
    st = {"ai": 0, "ai_old": 0, "page": 0, "dated": 0, "tries": 0, "decoded": 0, "gn": 0, "transient": 0,
          "blocked": False, "broken": False, "stale": 0, "stale_shown": 0}
    out, logs, hosts = set(), [], {}   # hosts: id → 원문 주소의 호스트(www. 뺌)
    new_flags = {}   # 이번 실행 Claude 옛 사건 {id: (시기, 근거)}
    old_flags = {}   # 지난 실행에서 Claude가 옛 사건이라 했지만 아직 못 가린 것(기사 ai_old)
    rjcut = (today - datetime.timedelta(days=AI_REJUDGE_DAYS)).isoformat()
    for i in pool:
        ao = next((x.get("ai_old") for x in pool[i] if isinstance(x.get("ai_old"), str)), None)
        m_ao = re.fullmatch(r"((?:19|20)[0-9]{2}(?:-[0-9]{2})?)@([0-9]{4}-[0-9]{2}-[0-9]{2})", ao or "")
        if m_ao and m_ao.group(2) >= rjcut and not has_od(i) and "n" not in ck(i):
            old_flags[i] = (m_ao.group(1), f"{m_ao.group(2)} 판단")
        elif ao:
            mark(i, ai_old=None)   # 다시 판정하는 기간이 지났거나 원문 날짜·글 번호로 가려진 것 — 남김으로 끝

    def ai_pass(todo):
        """Claude 확인(AI_CHUNK건씩) → 확인 못 하고 남긴 건수. 실패하면 멈추고 다음 실행에서 다시"""
        for n in range(0, len(todo), AI_CHUNK):
            chunk = todo[n:n + AI_CHUNK]
            if time.monotonic() - T0 > RUN_LIMIT:
                print("  [WARN] 실행 시간이 길어 Claude 옛 기사 확인 일부를 다음 실행으로 미룸", flush=True)
                return len(todo) - n
            try:
                got = ai_old_check([pool[i][0] for i in chunk], today)
            except (Exception, SystemExit) as e:
                print(f"  [WARN] Claude 옛 기사 확인 실패 — 다음 실행에서 다시: {str(e)[:150]}", flush=True)
                if isinstance(e, SystemExit):   # 키·크레딧 문제 — 선별은 이미 끝남, 저장은 하고 알림
                    soft_fail("Claude 옛 기사 확인 실패(키·크레딧) — 이번 실행은 원문 날짜·글 번호로만 거름")
                return len(todo) - n
            new_flags.update(got)
            for i in chunk:
                mark(i, "a")
            st["ai"] += len(chunk)
        return 0

    def drop(i, rec, why):
        x = pool[i][0]
        out.add(i)
        tk = title_key(x["title"])
        if len(tk) >= 8:   # 너무 짧은 제목 키는 다른 기사와 겹칠 수 있어 기억하지 않음(id로만 뺌)
            stale[tk] = rec + [hosts.get(i, "")]   # 5번째 = 원문 호스트(매체 이름이 달라도 같은 곳이면 묶음)
        logs.append(f"  옛 기사 제외{'(지금 보이는 기사)' if i in in_kept else ''}: {x['title'][:70]} — {why}")

    # ① Claude — 지난 기사(처음 몇 번의 실행은 1년 보관분 점검)
    todo = [i for i in order if tier[i] and not ({"a", "n"} & ck(i)) and not has_od(i)]
    left_ai = max(0, len(todo) - AI_CHECK_MAX) + ai_pass(todo[:AI_CHECK_MAX])
    flagged = {**old_flags, **new_flags}

    # ② 원문 날짜 — 옛 기사가 나온 매체(최근 60일 기억 + 이번 Claude 판단)는 남은 기사도
    cnt, hcnt = {}, {}
    mcut = (today - datetime.timedelta(days=60)).isoformat()
    for v in stale.values():
        if v[1] >= mcut:
            cnt[v[3]] = cnt.get(v[3], 0) + 1
            if len(v) > 4 and v[4]:
                hcnt[v[4]] = hcnt.get(v[4], 0) + 1
    for i in new_flags:
        cnt[src(i)] = cnt.get(src(i), 0) + 1
    sus = {k for k, c in cnt.items() if k and c >= SUS_MIN}
    mem_hosts = {h for h, c in hcnt.items() if c >= SUS_MIN}   # 최근 60일 옛 기사가 나온 원문 호스트
    sus_item = lambda i: src(i) in sus or norm(src(i)) in mem_hosts
    rank = lambda i: (0 if tier[i] == 0 and pool[i][0].get("first_seen") == tod else 1 if i in flagged
                      else 2 if tier[i] == 0 else 3)   # 오늘 선별 → Claude가 옛 사건이라 한 것 → 최근 이틀 선별 → 옛 기사 나온 매체
    queue = sorted((i for i in order if "p" not in ck(i) and not has_od(i) and (tier[i] == 0 or i in flagged or sus_item(i))),
                   key=lambda i: (rank(i), pos[i]))
    deadline = min(time.monotonic() + DATE_BUDGET, T0 + RUN_LIMIT)
    res, gfail, why, posts, hstat = {}, [], {}, {}, {}   # hstat: 호스트 → [날짜 읽음, 봇 확인 화면]
    boards = {} if boards is None else boards
    for bk, v in list(boards.items()):   # 옛 모양([최신 번호, 오른 날(, 본 글 수)])은 본 글 수 0·처음 값 = 지금 값으로
        if isinstance(v, list) and len(v) in (2, 3):
            boards[bk] = [v[0], v[1], v[2] if len(v) == 3 else 0, v[0], v[1]]
    streak = [0]   # 구글 일시 오류 연속 횟수

    def check_one(i):
        """기사 1건 원문 확인 — 이번 실행 원문 확인을 멈춰야 하면 False(구글이 막음·일시 오류 연속)"""
        link = str(pool[i][0].get("link") or "")
        gn = is_gn_link(link)
        st["gn"] += gn
        try:
            url = gn_resolve(link) if gn else (link if link.startswith("http") else None)
        except GBlocked as e:
            st["blocked"] = True
            print(f"  [WARN] 구글이 원문 주소 풀기를 막음({e}) — 남은 기사는 다음 실행에서", flush=True)
            return False
        except Exception as e:   # 연결 오류·5xx — 이 기사는 확인 안 한 것으로 두고 다음 실행에서 다시
            st["transient"] += 1
            streak[0] += 1
            print(f"  [WARN] 구글 링크 풀기 일시 오류: {type(e).__name__} {str(e)[:100]}", flush=True)
            if streak[0] >= TRANSIENT_MAX:
                st["blocked"] = True
                print(f"  [WARN] 구글 일시 오류 {streak[0]}회 연속 — 남은 기사는 다음 실행에서", flush=True)
                return False
            if gn:
                time.sleep(DATE_PAUSE)
            return True
        streak[0] = 0
        if gn:
            st["tries"] += 1
            st["decoded"] += bool(url)
        if url:
            bp = board_post(url)
            if bp:
                posts[i] = bp
                mark(i, wr=f"{bp[0]}#{bp[1]}")   # 글 번호를 기사에 저장 — 게시판 최신 번호를 아직 모르면 다음 실행에서 다시 판정
            h = hosts[i] = norm(urllib.parse.urlparse(url).hostname)
            if hstat.get(h, [0, 0])[0] == 0 and hstat.get(h, [0, 0])[1] >= HOST_SKIP:
                res[i], why[i] = None, {"host": h, "why": "skip"}   # 봇 확인 화면만 나오는 곳 — 원문 받기 건너뜀(글 번호만)
            else:
                info = {}
                try:
                    res[i] = page_date(url, info=info)
                except Exception as e:   # 뜻밖의 오류 — 이 기사만 다음 실행에서 다시(확인 표시 안 함)
                    print(f"  [WARN] 원문 날짜 읽기 오류: {type(e).__name__} {str(e)[:100]}", flush=True)
                    posts.pop(i, None)
                    hosts.pop(i, None)
                    return True
                if not res[i]:
                    why[i] = info
                hs = hstat.setdefault(h, [0, 0])
                w = str(info.get("why") or "")
                if res[i]:
                    hs[0] += 1
                elif w in ("nodate", "http401", "http403"):   # 봇 확인 화면 모양만 셈(접속 오류·5xx는 그때뿐일 수 있음)
                    hs[1] += 1
        else:
            gfail.append(i)
        if gn:
            time.sleep(DATE_PAUSE)
        return True

    k, n0, inq = 0, len(queue), set(queue)
    while k < len(queue) and time.monotonic() <= deadline:
        if not check_one(queue[k]):
            break
        k += 1
        if k == n0:   # 옛 기사 매체의 원문 호스트를 매체 이름으로 쓰는 기사도(예: '패션포스트' 원문이 fpost.co.kr → 'fpost.co.kr' 이름 기사)
            hot = {hosts[j] for j in hosts if src(j) in sus} | mem_hosts
            queue += [j for j in order if j not in inq and "p" not in ck(j) and not has_od(j) and norm(src(j)) in hot]
    for i in list(res):   # 구글 날짜보다 늦은 원문 날짜(첫 화면으로 넘어감·최신 기사 목록 등)는 못 믿음
        if res[i] and res[i] > rss_day(pool[i][0]) + datetime.timedelta(days=1):
            why[i] = {"host": hosts.get(i, ""), "why": "later"}
            res[i] = None
    for i in res:
        mark(i, "p")
    # 구글 링크가 풀리는 날 '구글이 모르는 기사'는 그 기사 문제라 다시 하지 않음 — 하나도 안 풀리면 방식이 바뀐 것일 수 있어 다음 실행에서
    if st["decoded"] or not st["tries"]:
        for i in gfail:
            mark(i, "p")
    st["page"] = len(res) + len(gfail)
    st["dated"] = sum(1 for d in res.values() if d)
    left_page = max(0, len(queue) - st["page"])
    if why:   # 원문 날짜를 못 읽은 곳 — 매체(주소)별 까닭(err:접속 오류·http상태·nodate 날짜 표시 없음·skip 건너뜀·later 늦은 날짜)
        agg = {}
        for v in why.values():
            hk = (v.get("host") or "?").removeprefix("www.")
            agg.setdefault(hk, {})
            agg[hk][v.get("why") or "?"] = agg[hk].get(v.get("why") or "?", 0) + 1
        top = sorted(agg.items(), key=lambda kv: -sum(kv[1].values()))
        print(f"  원문 날짜 못 읽음 {len(why)}건: " + " · ".join(
            f"{h} {sum(c.values())}({', '.join(f'{w} {n}' for w, n in sorted(c.items(), key=lambda x: -x[1]))})"
            for h, c in top[:8]) + (f" 외 {len(top) - 8}곳" if len(top) > 8 else ""), flush=True)
    if st["tries"] >= 5 and not st["decoded"]:
        st["broken"] = True
        soft_fail(f"구글 뉴스 링크를 하나도 못 풂(0/{st['tries']}) — 원문 날짜·글 번호 확인 안 됨(구글 방식 변경 가능), "
                  "옛 기사는 Claude 확인으로만 거름")
    for i in sorted((i for i in res if res[i]), key=lambda i: pos[i]):
        x, real = pool[i][0], res[i]
        g = rss_day(x)
        if (g - real).days > STALE_GAP:
            drop(i, [real.isoformat(), tod, "p", src(i)], f"{src(i)} · 원문 {real} / 구글 {g}")
        else:
            mark(i, orig_date=real.isoformat(), ai_old=None)
            if i in flagged:
                logs.append(f"  (원문 날짜가 최근이라 남김 — Claude는 {flagged[i][0]}) {x['title'][:60]} · 원문 {real}")

    # ②-2 그누보드 글 번호 — 이번에 본 번호로 게시판 최신 번호를 올리고, 원문 날짜를 못 읽은 글은 번호로 판정
    bmax, bobs = {}, {}   # 이번 실행에서 본 게시판별 최대 번호·글 수
    for bk, wr in posts.values():
        bmax[bk], bobs[bk] = max(bmax.get(bk, 0), wr), bobs.get(bk, 0) + 1
    scut = (today - datetime.timedelta(days=BOARD_STALE_DAYS)).isoformat()
    reset = set()   # 이번 실행에서 최신 번호를 다시 잡은 게시판 — 이번엔 '믿을 만한 게시판'으로 보지 않음
    for bk, wr in bmax.items():
        prev = boards.get(bk)
        if prev and wr < (1 - BOARD_LAG) * prev[0] and bobs[bk] >= BOARD_FRESH_OBS:
            if prev[1] <= scut:   # 기억한 최신 번호가 3주 넘게 안 올랐는데 여러 글이 모두 한참 아래 — 번호를 새로 매긴 것으로 봄
                soft_fail(f"게시판 {bk} 글 번호가 줄었음({prev[0]} → {wr}, {BOARD_STALE_DAYS}일 넘게 더 큰 번호 없음) — "
                          "번호를 새로 매긴 것으로 보고 최신 번호를 다시 잡음(확인 필요)")
                boards[bk] = [wr, tod, bobs[bk], wr, tod]
                reset.add(bk)
                continue
            print(f"  [WARN] 게시판 {bk}: 이번에 본 글 {bobs[bk]}건이 모두 최신 번호({prev[0]})보다 한참 아래 — 옛 글 묶음으로 봄",
                  flush=True)
        n = min((prev[2] if prev else 0) + bobs[bk], 10 ** 6)
        first = [prev[3], prev[4]] if prev else [wr, tod]
        boards[bk] = ([wr, tod, n] if not prev or wr > prev[0] else [prev[0], prev[1], n]) + first
    gcut = (today - datetime.timedelta(days=BOARD_GROW_DAYS)).isoformat()

    def board_ok(bk):
        """믿을 만한 게시판 — 글을 충분히 봤고, 7일 넘게 지켜보는 동안 최신 번호가 하루 1개 넘게 늘었고, 최근 7일 안에 오름"""
        b = boards.get(bk)
        if not b or bk in reset or b[0] < BOARD_MIN_MAX or b[2] < BOARD_FRESH_OBS or b[1] < gcut or b[4] > gcut:
            return False
        days = (datetime.date.fromisoformat(b[1]) - datetime.date.fromisoformat(b[4])).days
        return days >= BOARD_GROW_DAYS and b[0] - b[3] >= days
    # 이번에 본 글 + 지난 실행에서 번호를 저장해 둔 글(그때 게시판 최신 번호를 몰라 못 가린 것 — 10/15 시험 카녜이) — 원문 날짜 없는 것만
    judge = dict(posts)
    for i in pool:
        if i in judge or i in out or res.get(i) or has_od(i) or "n" in ck(i):
            continue
        m_wr = next((re.fullmatch(r"([\w.-]{1,100}/[\w-]{1,40})#([1-9][0-9]{0,8})", str(x.get("wr") or ""))
                     for x in pool[i] if x.get("wr")), None)
        if m_wr and m_wr.group(1) in boards:
            judge[i] = (m_wr.group(1), int(m_wr.group(2)))
    board_young = set()   # 믿을 만한 게시판에서 번호로 최근 글인 것 — Claude 판단은 쓰지 않음
    for i in sorted((i for i in judge if not res.get(i) and i not in out), key=lambda i: pos[i]):
        (bk, wr), x = judge[i], pool[i][0]
        if x.get("group") in SLOW_GROUPS:   # 국내 유통사(30일 창·90일 보관)는 원래 몇 주 된 글도 받으므로 번호로 판단 안 함
            continue
        mx, g = boards[bk][0], rss_day(x)
        lag, base_lag = mx - wr, max(BOARD_LAG_MIN, BOARD_LAG * mx)
        if mx >= BOARD_MIN_MAX and lag >= base_lag + BOARD_RATE_MAX * max(0, (today - g).days):
            st["board"] = st.get("board", 0) + 1
            drop(i, [f"#{wr}/{mx}", tod, "n", src(i)], f"{src(i)} · 게시판 글 번호 {wr}(최신 {mx}) / 구글 {g}")
        elif board_ok(bk) and lag < base_lag:
            board_young.add(i)
            mark(i, "n", ai_old=None)   # 글 번호로 최근 글 — 다음 실행에서도 Claude에 묻지 않음

    # ③ Claude — 최근 선별 중 원문 날짜를 못 읽은 것
    todo3 = [i for i in order if tier[i] == 0 and not ({"a", "n"} & ck(i)) and not has_od(i) and i not in out
             and i not in board_young]
    left_ai += ai_pass(todo3)
    flagged = {**old_flags, **new_flags}
    st["ai_old"] = len(new_flags)

    # ④ 원문 날짜·글 번호로 못 가린 Claude 옛 사건 — 그 매체에 옛 기사가 몰려 있을 때만(이번 Claude 옛 사건 + 최근 60일 기억 ≥ WAVE_MIN,
    #    원문 날짜·글 번호로 밝혀진 옛 기사는 WAVE_MIN만큼). 한두 건만 걸린 매체는 Claude 착각(미리 발표된 일·비슷한 옛 사건)일 수 있어 남김
    #    (2026-10-15 시험: Claude만 옛 사건이라 한 기사 중 시부야 세이부 폐점·아르노 나이키 이사·글렌 마틴스 디젤 퇴임은 최근 기사)
    wave = {}   # 매체 이름·원문 호스트 → 옛 기사 근거 수(원문 날짜로 아니라고 밝혀진 Claude 판단은 세지 않음)
    for i in new_flags:   # 원문 날짜·글 번호로 최근 글인 것은 근거로 안 셈
        if not res.get(i) and i not in board_young and ai_stale(new_flags[i][0], rss_day(pool[i][0])):
            for key in {src(i), hosts.get(i, "")} - {""}:
                wave[key] = wave.get(key, 0) + 1
    for v in stale.values():
        if v[1] >= mcut:
            for key in {v[3], v[4] if len(v) > 4 else ""} - {""}:
                wave[key] = wave.get(key, 0) + (WAVE_MIN if v[2] in ("p", "n") else 1)   # 원문 날짜·글 번호로 밝혀진 것은 확실한 근거
    for i in sorted((i for i in flagged if not res.get(i) and i not in out), key=lambda i: pos[i]):
        x = pool[i][0]
        g, (when, why_), s = rss_day(x), flagged[i], src(i)
        if i in board_young:
            if i in new_flags:
                logs.append(f"  (게시판 글 번호로는 옛 글이 아니라 남김 — Claude는 {when}) {x['title'][:60]}")
            mark(i, ai_old=None)
            continue
        if not ai_stale(when, g):
            continue
        if max(wave.get(s, 0), wave.get(hosts.get(i, ""), 0) if hosts.get(i) else 0) >= WAVE_MIN:
            drop(i, [when, tod, "a", s], f"{s} · Claude {when} {why_} / 구글 {g}")
        else:
            if i in new_flags:   # 다음 실행들(AI_REJUDGE_DAYS일)에서 근거가 쌓이거나 원문·글 번호로 가려지면 다시 판정
                mark(i, ai_old=f"{when}@{tod}")
            if i in new_flags:
                st["ai_kept"] = st.get("ai_kept", 0) + 1
                logs.append(f"  (Claude만 옛 사건({when})이라 함 — {s} 옛 기사 근거 부족해 남김) {x['title'][:60]}")
    st["stale"], st["stale_shown"] = len(out), len(out & in_kept)
    st["left_ai"], st["left_page"] = left_ai, left_page
    for ln in logs[:200]:
        print(ln, flush=True)
    if len(logs) > 200:
        print(f"  … 외 {len(logs) - 200}줄", flush=True)
    print(f"옛 기사 확인: Claude {st['ai']}건(옛 사건 {st['ai_old']}) · 원문 페이지 {st['page']}건(날짜 읽음 {st['dated']} · "
          f"구글 링크 풀기 {st['decoded']}/{st['tries']}{' · 일시 오류 ' + str(st['transient']) + '건' if st['transient'] else ''}"
          f"{' · 구글이 막아 멈춤' if st['blocked'] else ''}"
          f"{' · 게시판 글 번호로 ' + str(st['board']) + '건' if st.get('board') else ''}) → "
          f"옛 기사 {st['stale']}건 제외(지금 보이는 기사 {st['stale_shown']}건)"
          + (f" · 남은 확인 Claude {left_ai}건·원문 {left_page}건" if left_ai or left_page else ""), flush=True)
    return out, st


# ── v2.12 지난 뉴스 1년 보관(docs/news_archive.json) — 대시보드 시장 › 뉴스 검색창이 검색할 때만 내려받음 ──
def _arch_item(it):
    """보관용 기사 1건(news.json 기사의 화면용 칸) — id·제목·주소·수집일이 없거나 깨진 것은 None"""
    if not isinstance(it, dict):
        return None
    iid, title, link, fs = it.get("id"), it.get("title"), it.get("link"), it.get("first_seen")
    if not (isinstance(iid, str) and iid and isinstance(title, str) and title.strip() and isinstance(link, str)
            and link and isinstance(fs, str) and re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", fs)):
        return None
    try:
        datetime.date.fromisoformat(fs)
    except ValueError:
        return None
    try:
        imp = min(3, max(1, int(it.get("importance") or 1)))
    except (TypeError, ValueError, OverflowError):
        imp = 1
    a = {k: ("" if it.get(k) is None else str(it.get(k))) for k in ARCH_KEYS}
    a["importance"] = imp
    od, ck = it.get("orig_date"), it.get("dchk")   # v2.13 있을 때만
    if isinstance(od, str) and re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", od):
        a["orig_date"] = od
    if isinstance(ck, str) and ck and set(ck) <= set("anp"):
        a["dchk"] = "".join(sorted(set(ck)))
    ao = it.get("ai_old")
    if isinstance(ao, str) and re.fullmatch(r"(19|20)[0-9]{2}(-[0-9]{2})?@[0-9]{4}-[0-9]{2}-[0-9]{2}", ao):
        a["ai_old"] = ao
    wr = it.get("wr")
    if isinstance(wr, str) and re.fullmatch(r"[\w.-]{1,100}/[\w-]{1,40}#[1-9][0-9]{0,8}", wr):
        a["wr"] = wr
    return a


def load_archive():
    """기존 보관 파일 → (기사 목록, 복구 기록). 없으면 (None, {}), 깨졌으면 [WARN] 후 (None, {}) — git 기록에서 다시 만듦"""
    if not os.path.exists(ARCHIVE_PATH):
        return None, {}
    try:
        with open(ARCHIVE_PATH, encoding="utf-8") as f:
            d = json.load(f)
        if not isinstance(d, dict) or not isinstance(d.get("items"), list):
            raise ValueError("items 목록 없음")
    except Exception as e:
        print(f"  [WARN] 뉴스 보관 파일을 못 읽음 — git 기록에서 다시 만듦: {str(e)[:120]}", flush=True)
        return None, {}
    bf = d.get("backfill")
    return d["items"], (bf if isinstance(bf, dict) else {})


def backfill_git(today):
    """news.json의 지난 git 기록(커밋마다 그때 보관 중이던 14일치)에서 선별 기사를 모음 → (기사 목록, 복구 기록).
    done = 기록 전체를 읽음(얕은 복제·git 없음이면 False → 다음 실행에서 다시). 같은 id는 나중 기록이 덮음"""
    def git(*a):
        return subprocess.run(["git", *a], capture_output=True, timeout=120, check=True).stdout
    try:
        shallow = git("rev-parse", "--is-shallow-repository").decode().strip() != "false"
        shas = git("log", "--format=%H", "--", NEWS_PATH).decode().split()
    except Exception as e:
        print(f"  [WARN] git 기록을 못 읽음: {str(e)[:120]}", flush=True)
        return [], {"done": False, "versions": 0, "at": today.isoformat()}
    found, bad = {}, 0
    for sha in reversed(shas):   # 오래된 커밋부터
        try:
            d = json.loads(git("show", f"{sha}:{NEWS_PATH}"))
        except Exception:
            bad += 1
            continue
        items = d.get("items") if isinstance(d, dict) else None
        if not isinstance(items, list):
            bad += 1
            continue
        for it in items:
            a = _arch_item(it)
            if a:
                found[a["id"]] = a
    return list(found.values()), {"done": not shallow and bool(shas), "versions": len(shas), "bad": bad,
                                  "at": today.isoformat()}


def merge_archive(base, add, today, drop_keys=frozenset(), drop_ids=frozenset()):
    """보관 기사 합치기 — 같은 id는 add(이번 news.json 보관분)가 덮음(별점은 둘 중 높은 것) · 수집일 365일 넘은 것은 뺌 ·
    같은 제목 + 같은 구분(scope·key — 구글 뉴스가 며칠 뒤 다시 내보낸 같은 기사)은 최신 1건, 별점은 그중 가장 높은 것.
    다른 브랜드·산업으로 잡힌 같은 제목은 따로 둠(칩 안에서도 찾게 — 화면이 검색할 때 1건으로 보여 줌) → 최신순(수집일·중요도).
    v2.13 옛 기사(제목 키 drop_keys·id drop_ids)는 뺌(git 기록에서 되살린 것도 — 단 원문 날짜로 수집 때 최근 기사였음이 확인된
    같은 제목 사본은 남김) · 원문 날짜·확인 방법·Claude 옛 사건 시기는 어느 쪽에 있든 남김"""
    by = {}
    for it in list(base) + list(add):
        a = _arch_item(it)
        if a and a["id"] not in drop_ids and (title_key(a["title"]) not in drop_keys or verified_fresh(a)):
            p = by.get(a["id"])
            if p and p["importance"] > a["importance"]:
                a["importance"] = p["importance"]
            if p:
                for k2 in ("orig_date", "ai_old", "wr"):
                    if k2 not in a and p.get(k2):
                        a[k2] = p[k2]
                ck = set(a.get("dchk", "")) | set(p.get("dchk", ""))
                if ck:
                    a["dchk"] = "".join(sorted(ck))
            by[a["id"]] = a
    cut = (today - datetime.timedelta(days=ARCHIVE_DAYS)).isoformat()
    rows = sorted((a for a in by.values() if a["first_seen"] >= cut),
                  key=lambda a: (a["first_seen"], a["importance"], a["id"]), reverse=True)
    out, keep = [], {}
    for a in rows:
        tk = title_key(a["title"])
        g = (tk, a["scope"], a["key"]) if tk else None
        if g in keep:
            keep[g]["importance"] = max(keep[g]["importance"], a["importance"])
            continue
        if g:
            keep[g] = a
        out.append(a)
    out.sort(key=lambda a: (a["first_seen"], a["importance"], a["id"]), reverse=True)   # 별점을 올린 뒤 다시 정렬(다음 실행과 순서 같게)
    return out


def _backfill_info(b):
    """복구 기록 — 알려진 칸·형식만(이전 파일의 이상한 값이 그대로 다시 쓰이지 않게)"""
    b = b if isinstance(b, dict) else {}
    out = {"done": b.get("done") is True}
    for k in ("versions", "bad"):
        v = b.get(k)
        out[k] = v if isinstance(v, int) and not isinstance(v, bool) and v >= 0 else 0
    at = b.get("at")
    out["at"] = at if isinstance(at, str) and re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", at) else None
    return out


def save_archive(items, backfill, today):
    """보관 파일 저장 — 머리(갱신 시각·건수·시작일·복구 기록) + 한 줄에 기사 1건(매일 git 차이가 작게).
    다 만든 뒤 JSON 확인 → 임시 파일 → 바꿔치기(중간에 멈춰도 옛 파일 그대로)"""
    meta = {"generated_at": datetime.datetime.now(KST).strftime("%Y-%m-%d %H:%M KST"), "today": today.isoformat(),
            "keep_days": ARCHIVE_DAYS, "n": len(items), "since": items[-1]["first_seen"] if items else None,
            "backfill": _backfill_info(backfill)}
    dump = lambda o: json.dumps(o, ensure_ascii=False, separators=(",", ":"), allow_nan=False)   # NaN은 브라우저가 못 읽음
    head = dump(meta)
    body = ",\n".join(dump(a) for a in items)
    txt = head[:-1] + ',\n"items":[\n' + body + "\n]}\n"
    json.loads(txt)
    tmp = ARCHIVE_PATH + ".tmp"
    with open(tmp, "wb") as f:
        f.write(txt.encode("utf-8", "replace"))   # 짝 없는 대리 문자(깨진 글자)는 '?'로
    os.replace(tmp, ARCHIVE_PATH)
    return meta


def archive_base(today):
    """보관 파일 읽기(없거나 복구가 덜 끝났으면 git 기록에서 되살림) → (기사 목록, 복구 기록).
    v2.13 옛 기사 확인이 보관 기사도 보므로 저장 전에 따로 읽음. 실패하면 실패 표시 후 (None, None) — 보관 파일은 그대로 둠"""
    try:
        base, bf = load_archive()
        if base is None or not bf.get("done"):
            got, info = backfill_git(today)
            print(f"뉴스 보관 복구: git 기록 {info['versions']}개 버전에서 {len(got)}건"
                  + ("" if info["done"] else " — 기록이 얕거나 없어 일부만(다음 실행에서 다시)"), flush=True)
            base, bf = (base or []) + got, info
        return base, bf
    except Exception as e:
        soft_fail(f"뉴스 보관 파일 읽기 실패 — {type(e).__name__}: {str(e)[:120]}")
        return None, None


def update_archive(kept, today, base, bf, drop_keys=frozenset(), drop_ids=frozenset()):
    """1년 보관 갱신 → news.json status.archive {ok, n, since}. 실패하면 실패 표시(news.json 저장은 계속).
    base·bf = archive_base() 결과(None이면 읽기 실패 — 저장 안 함). v2.13 옛 기사(제목 키·id)는 빼고 저장"""
    if base is None:
        return {"ok": False}
    try:
        items = merge_archive(base, kept, today, drop_keys, drop_ids)
        meta = save_archive(items, bf, today)
        print(f"saved {ARCHIVE_PATH} (보관 {meta['n']}건 · {meta['since'] or '―'}부터)", flush=True)
        res = {"ok": True, "n": meta["n"], "since": meta["since"]}
        if not bf.get("done"):
            res["partial"] = True   # 수집 상태에 '일부만 복구' 표시(빨간 X·점검 알림과 맞춤)
            soft_fail("뉴스 보관 파일을 git 기록 일부로 만듦 — 지난 기사가 빠졌을 수 있음(다음 실행에서 다시 복구)")
        return res
    except Exception as e:
        soft_fail(f"뉴스 보관 파일 저장 실패 — {type(e).__name__}: {str(e)[:120]}")
        return {"ok": False}


PROBE_MAX = 15   # 원문 날짜 진단 1회 기사 수


def probe(spec):
    """원문 날짜 진단(news.yml 수동 실행 입력 probe) — 매체 이름·기사 id(쉼표 구분)에 맞는 보관 기사(news.json·1년 보관, 최신순)
    최대 PROBE_MAX건의 구글 링크 풀기·원문 페이지 날짜 단서를 로그로 보여 줌. Claude 안 씀·저장 안 함(날짜 형식을 모르는 매체 확인용)"""
    keys = [k.strip() for k in str(spec).split(",") if k.strip()]
    items = {}
    for path in (NEWS_PATH, ARCHIVE_PATH):
        try:
            with open(path, encoding="utf-8") as f:
                for it in json.load(f).get("items") or []:
                    if isinstance(it, dict) and isinstance(it.get("id"), str):
                        items.setdefault(it["id"], it)
        except Exception as e:
            print(f"  [WARN] {path} 못 읽음: {str(e)[:100]}", flush=True)
    pick = [items[k] for k in keys if k in items]   # 기사 id를 먼저, 그다음 매체 이름에 맞는 기사(최신순)
    pick += [it for it in sorted(items.values(), key=lambda x: str(x.get("first_seen") or ""), reverse=True)
             if it not in pick and str(it.get("source") or "") in keys]
    pick = pick[:PROBE_MAX]
    print(f"원문 날짜 진단: {', '.join(keys)} — {len(pick)}건", flush=True)
    near = re.compile(r"(?:19|20)?\d\d\s*[-./년]\s*\d\d?\s*[-./월]\s*\d\d?(?:\s*일)?(?:\s*\(?[월화수목금토일]?\)?\s*(?:오전|오후)?\s*\d\d?:\d\d)?")
    for it in pick:
        print(f"\n[{it['id']}] {str(it.get('source') or '')} · 구글 {rss_day(it)} · {str(it.get('title') or '')[:60]}", flush=True)
        t = time.monotonic()
        try:
            url = gn_resolve(str(it.get("link") or "")) if is_gn_link(it.get("link")) else it.get("link")
        except GBlocked as e:
            print(f"  구글이 막음({e}) — 진단 멈춤", flush=True)
            break
        except Exception as e:
            url = None
            print(f"  구글 링크 풀기 오류: {type(e).__name__} {str(e)[:120]}", flush=True)
        print(f"  원문 주소: {url} ({time.monotonic() - t:.1f}초)", flush=True)
        time.sleep(DATE_PAUSE)
        if not url:
            continue
        try:
            r, raw = _get_capped(url, 1_000_000)
        except Exception as e:
            print(f"  원문 받기 오류: {type(e).__name__} {str(e)[:160]}", flush=True)
            continue
        html = _page_html(r, raw)
        print(f"  HTTP {r.status_code} · {len(raw):,}바이트 · {r.headers.get('content-type', '')} · 최종 {r.url}", flush=True)
        if len(raw) < 8000:   # 작은 페이지(알림·넘겨주기·차단 화면)는 앞부분을 그대로
            head = re.sub(r"\s+", " ", html)[:500]
            print(f"  페이지 앞부분: {head}", flush=True)
        metas = []
        for tag in re.findall(r"<meta\b[^>]{0,600}>", html, re.I):
            m = {k.lower(): v for k, v in re.findall(r'([\w:.-]+)\s*=\s*["\']([^"\']*)["\']', tag)}
            nm = (m.get("property") or m.get("name") or m.get("itemprop") or "").lower()
            if re.search(r"date|time|publish|regdate|created", nm):
                metas.append(f"{nm}={m.get('content', '')[:40]}")
        print(f"  날짜 메타: {' | '.join(metas[:8]) or '없음'}", flush=True)
        jl = re.findall(r'"date(?:Published|Created|Modified)"\s*:\s*"([^"]{8,40})"', html)
        print(f"  JSON-LD: {' | '.join(jl[:4]) or '없음'}", flush=True)
        text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", re.sub(r"(?is)<(script|style)\b.*?</\1>", " ", html)))
        ctx = [text[max(0, m.start() - 24):m.end()].strip() for m in near.finditer(text)][:6]
        print(f"  본문 속 날짜(앞 24자 포함): {' | '.join(ctx) or '없음'}", flush=True)
        print(f"  이름표 후보: {_html_dates(html) or '없음'} · 주소 속 날짜: {_date_in_url(r.url or url)}", flush=True)
        print(f"  → 원문 날짜 판정: {page_date(url)}", flush=True)


def main():
    if len(sys.argv) > 2 and sys.argv[1] == "--probe":   # v2.13 원문 날짜 진단(Claude 안 씀·저장 안 함)
        probe(sys.argv[2])
        return
    if not API_KEY:
        print("[ERROR] ANTHROPIC_API_KEY 미설정")
        raise SystemExit(1)

    today = datetime.datetime.now(KST).date()
    old = {"items": []}
    if os.path.exists(NEWS_PATH):
        try:
            with open(NEWS_PATH, encoding="utf-8") as f:
                old = json.load(f)
        except Exception:
            pass
    kept = []
    for it in old.get("items", []):
        try:
            fs = datetime.date.fromisoformat(it.get("first_seen", "1970-01-01"))
        except Exception:
            fs = datetime.date(1970, 1, 1)
        if (today - fs).days <= SLOW_GROUPS.get(it.get("group"), (0, KEEP_DAYS))[1]:
            kept.append(it)
    stale = load_stale(old, today)   # v2.13 옛 기사 제목 기억(1년) — 지난 실행에서 뺀 기사가 다시 보이지 않게
    boards = load_boards(old, today)   # v2.13 그누보드 게시판 최신 글 번호
    kept = [it for it in kept if title_key(it.get("title", "")) not in stale or verified_fresh(it)]
    base, bf = archive_base(today)   # v2.12 1년 보관 — v2.13 수집 전에 읽어 1년 안에 고른 기사 제목은 다시 받지 않음(옛 기사 재게시 대비)
    arch_titles = {tk for tk in (title_key(str(x.get("title") or "")) for x in (base or []) if isinstance(x, dict))
                   if len(tk) >= 8}   # 너무 짧은 제목 키는 다른 기사와 겹칠 수 있어 빼고
    known = {it["id"] for it in kept}
    old_seen = list(old.get("seen_ids", []))
    seen_ids = set(old_seen) | known

    recent_days = {(today - datetime.timedelta(days=d)).isoformat() for d in range(3)}
    recent = [it.get("summary") or it.get("title", "") for it in kept
              if it.get("first_seen") in recent_days][:120]
    # 제목 기억: 보관 중 기사 + 최근 35일 판정한 기사. 처음 실행(기억 없음)엔 보관 중 기사(14일)만 덮으므로
    # 국내 유통사 검색 창을 기억이 덮는 기간까지만(14일 → 하루씩 늘어 30일)
    cut = (today - datetime.timedelta(days=SEEN_TITLE_DAYS)).isoformat()
    seen_titles = {k: d for k, d in (old.get("seen_titles") or {}).items() if d >= cut}
    for it in kept:
        seen_titles.setdefault(title_key(it.get("title", "")), it.get("first_seen") or today.isoformat())
    since = old.get("seen_since") or (today - datetime.timedelta(days=KEEP_DAYS)).isoformat()
    mem_days = (today - datetime.date.fromisoformat(since)).days
    raw, st = collect(set(seen_titles) | {title_key(it.get("title", "")) for it in kept} | set(stale) | arch_titles,
                      slow_days=max(3, mem_days))
    nfail = len(st["failed"])
    # v2.9 구글 뉴스가 한 건도 안 들어오면(전체 RSS 실패·형식 변경) 저장하지 않음 — 갱신 시각을 옮기지 않아 이틀 넘으면 수집 상태 '지연'
    if st["headlines"] == 0:
        soft_fail(f"구글 뉴스 수집 0건(검색어 {st['queries']}개 중 실패 {nfail}개) — news.json 그대로 둠")
        return
    if nfail * 2 > st["queries"]:
        soft_fail(f"구글 뉴스 검색어 {st['queries']}개 중 {nfail}개 실패 — 받은 기사만 반영")
    new_items = {k: v for k, v in raw.items() if k not in seen_ids}
    print(f"신규 {len(new_items)}건 → Claude 선별")

    picked, usage, curate = {}, None, "none"
    if new_items:
        try:
            picked, usage = claude_curate(new_items, MODEL, recent)
            curate = "ok"
            print(f"선별 {MODEL}: {len(picked)}건 · 입력 {usage['in']:,} · 출력 {usage['out']:,} 토큰 · ${usage['usd']}",
                  flush=True)
        except Exception as e:
            print(f"[WARN] 선별 실패(이번 회차 신규 미반영): {str(e)[:150]}")
            picked, curate = {}, "failed"
            # 신규는 seen에 넣지 않아 다음 회차에 다시 판정(손실 없음) — 오늘 뉴스가 비므로 알림
            soft_fail(f"Claude 선별 실패({str(e).split(':')[0][:40]}) — 신규 {len(new_items)}건은 다음 실행에서 다시 선별")

    compare = old.get("model_compare", [])[-19:]
    if usage and SHADOW_MODEL and today.isoformat() <= SHADOW_UNTIL:
        rec = compare_models(new_items, picked, usage, today, recent)
        if rec:
            compare.append(rec)

    for iid, sel in picked.items():
        src = new_items.get(iid)
        if not src:
            continue
        kept.append({
            "id": iid,
            "scope": src["scope"], "key": src["key"], "label": src["label"],
            "group": src.get("group", ""),
            "category": str(sel.get("category",
                                    src["key"] if src["scope"] == "industry" else "brand")),
            "summary": str(sel.get("summary", "")).strip(),
            "importance": int(sel.get("importance", 1)),
            "title": src["title"], "link": src["link"],
            "source": src["source"], "pubDate": src["pubDate"],
            "first_seen": today.isoformat(),
        })

    # v2.13 옛 기사 거르기 — 오늘 선별 + 보관 중 기사(news.json·1년 보관), 뺀 기사는 아래 seen에 남아 다시 판정하지 않음
    keys3 = ("dchk", "orig_date", "ai_old", "wr")
    snap = [(x, {k: x[k] for k in keys3 if k in x}) for x in list(kept) + list(base or []) if isinstance(x, dict)]
    snap_stale, snap_boards = dict(stale), {k: list(v) for k, v in boards.items()}
    try:
        stale_ids, dcs = date_check(kept, base, today, stale, boards)
    except Exception as e:   # 확인 중 뜻밖의 오류 — 이번 실행의 확인 표시를 되돌리고(다음 실행에서 다시) 오늘 선별은 저장, 알림
        for x, saved in snap:
            for k in keys3:
                x.pop(k, None)
            x.update(saved)
        stale.clear()
        stale.update(snap_stale)
        boards.clear()
        boards.update(snap_boards)
        soft_fail(f"옛 기사 확인 오류 — {type(e).__name__}: {str(e)[:120]} (이번 실행은 거르지 않음)")
        stale_ids, dcs = set(), {"error": True}
    # 구글 링크를 하나도 못 푼 실행이 이어지면(막힘·방식 변경) 실패 표시 — 그동안 원문 날짜·글 번호 확인이 조용히 멈추지 않게
    prev_dc = (old.get("status") or {}).get("date_check") if isinstance(old.get("status"), dict) else None
    prev_nd = prev_dc.get("nodecode_runs") if isinstance(prev_dc, dict) else 0
    prev_nd = prev_nd if isinstance(prev_nd, int) and not isinstance(prev_nd, bool) and prev_nd >= 0 else 0
    if dcs.get("gn") and not dcs.get("decoded"):
        dcs["nodecode_runs"] = prev_nd + 1
    elif dcs.get("decoded"):
        dcs["nodecode_runs"] = 0
    else:
        dcs["nodecode_runs"] = prev_nd   # 확인할 구글 링크가 없던 날은 그대로
    if dcs["nodecode_runs"] >= NODECODE_ALERT and not dcs.get("broken"):
        dcs["broken"] = True
        soft_fail(f"구글 링크를 {dcs['nodecode_runs']}회 연속 하나도 못 풂(막힘·방식 변경) — 원문 날짜·글 번호 확인 안 됨, "
                  "옛 기사는 Claude 확인으로만 거름")
    kept = [it for it in kept if it["id"] not in stale_ids and (title_key(it.get("title", "")) not in stale or verified_fresh(it))]
    n_new = sum(1 for k in picked if k in new_items and k not in stale_ids)

    for g in ("kr_peer", "kr_fb"):
        nn = [v for v in new_items.values() if v.get("group") == g]
        pk = [k for k in picked if (new_items.get(k) or {}).get("group") == g]
        print(f"  {GROUP_LABEL[g]}: 신규 {len(nn)}건({len({v['key'] for v in nn})}곳) → 선별 {len(pk)}건"
              + (f" — {', '.join(sorted({new_items[k]['label'] for k in pk}))}" if pk else ""), flush=True)

    # 선별 실패 시에는 seen에 넣지 않아 다음 회차에 재판정. v2.8 오래된 것부터 지움(전엔 집합→목록 변환 순서라 무작위로
    # 잘려 이미 본 기사가 다시 Claude로 가던 문제) — 보관 중인 기사 id는 항상 남김
    # 보관 중인 기사(known)는 매 실행 kept에서 다시 더해지므로 목록엔 '거른 기사'까지 들어온 순서대로만 둠
    add_ids = list(new_items.keys()) if usage is not None else []   # v2.8 선별 '0건'도 판정 완료(전엔 실패와 같이 취급해 다음 회차 재판정)
    seen_list = list(dict.fromkeys(old_seen + add_ids))[-SEEN_MAX:]
    for iid in add_ids:   # 판정한 기사 제목도 35일 기억(고른 것·거른 것 모두)
        seen_titles[title_key(new_items[iid].get("title", ""))] = today.isoformat()
    seen_titles.pop("", None)

    kept.sort(key=lambda x: (x["first_seen"], x["importance"]), reverse=True)
    arch = update_archive(kept, today, base, bf, set(stale), stale_ids)   # v2.12 지난 뉴스 1년 보관(검색용) — 실패해도 news.json은 저장
    dcs["memory"] = len(stale)
    out = {"generated_at":
           datetime.datetime.now(KST).strftime("%Y-%m-%d %H:%M KST"),
           "today": today.isoformat(),
           "items": kept, "seen_ids": seen_list, "seen_titles": seen_titles, "seen_since": since,
           "stale_titles": stale,   # v2.13 옛 기사 제목 기억(1년, 화면에는 안 넣음)
           "boards": boards,   # v2.13 그누보드 게시판 최신 글 번호(글 번호로 옛 글 판정, 화면에는 안 넣음)
           # v2.9 이번 실행 수집 결과(수집 상태·점검용): 검색어 수·실패 수·받은 헤드라인·신규·선별 결과(ok/failed/none)
           # v2.12 archive = 1년 보관 {ok, n(건수), since(가장 오래된 수집일), partial(git 기록 일부로 만듦)} — 검색창 안내·수집 상태
           # v2.13 date_check = 옛 기사 확인 {ai·ai_old: Claude 확인·옛 사건, page·dated: 원문 페이지·날짜 읽음, tries·decoded: 구글 링크
           #       풀기, blocked: 구글이 막음, broken: 하나도 못 풂, stale·stale_shown: 이번에 뺀 기사(그중 보이던 것), left_ai·left_page:
           #       다음 실행으로 넘긴 확인, memory: 옛 기사 제목 기억 수}
           "status": {"queries": st["queries"], "failed_queries": nfail, "headlines": st["headlines"],
                      "new": len(new_items), "curate": curate, "archive": arch, "date_check": dcs}}
    if compare:
        out["model_compare"] = compare
    out["claude_usage"] = usage_months(old)   # v2.10 월별 Claude 사용량(수집 상태 화면)
    os.makedirs("docs", exist_ok=True)
    with open(NEWS_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(f"saved {NEWS_PATH} (보관 {len(kept)}건, 오늘 신규 {n_new}건)")
    print(f"Claude 사용: 이번 실행 {_USAGE['calls']}회 · ${_USAGE['usd']:.3f} · 이번 달 누적 "
          f"${out['claude_usage'][max(out['claude_usage'])]['usd']:.2f}")


if __name__ == "__main__":
    main()

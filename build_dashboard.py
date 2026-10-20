# -*- coding: utf-8 -*-
"""
sports-industry-monitor — 단일 HTML 대시보드 빌드
v33.10: (대표 지시 2026-10-20 '보완안 1·2·3 모두') 공공데이터포털·통계청이 일부 GitHub 서버에서만 막히는 문제 — 수집 상태 줄에
       '공공데이터포털 연결 안 됨(GitHub 서버 n대 모두 막힘 · 날짜부터)'(logistics.json dgk_conn · logistics_fetch v1.3)·'통계청 연결 안 됨(…)'
       (kosis.json conn · kosis_fetch v5.2) — 연결 시험은 통과했는데 못 받았으면 '연결 오류(GitHub 서버 n대에서 시도)'. 물류 화면 '이번 수집
       일부 실패' 줄 끝에도 같은 사유. 화면 구성·판정 규칙은 그대로
v33.9: (대표 지시 2026-10-19 '텍스트가 너무 많다 — 표 해석을 돕는 글 일부 제외 · 물류·기업 상세 둘 다') 표·그래프를 읽는 데 돕는 긴 설명을
       '읽는 법'으로 접음(누르면 펼침, why()) — 물류: 맨 위 읽는 법 상자·카드 설명 11개·부산 입항 설명·출처 자세히(출처 한 줄·수집 실패 표시·
       '지난 자료 채우는 중'·'목록 밖 n개 나라'는 그대로 보임),
       '전쟁 길목 없음' 반복 줄 삭제(길목 있는 거점만 표시 · 펼친 줄의 '한국까지 길목'은 그대로), 머리 줄은 '갱신'만. 기업 상세: 지역 막대 범례·
       본사 발언 설명·한국 시장 신호 설명은 접고 '기준' 줄은 그대로, 국내 법인 비교·재무 기준 줄은 짧게. 숫자·판정·출처 한 줄은 그대로
v33.8: (대표 지시 2026-10-19 '2순위 새 종목 추가') 본사 4곳(몽클레르 MONC.MI·제냐 ZGN·버버리 BRBY.L·랄프로렌 RL, fetch_data v4.16) 로고·
       나라·뉴스 연결, 감시 브랜드 5개(naver_trend v1.9) 원산지 통화 CHK_CUR — 몽클레르·스톤아일랜드 유로, 버버리 파운드, 폴로 랄프로렌 달러,
       톰브라운 달러(뉴욕 브랜드 — 본사 제냐 재무는 유로라 표시). 판정 규칙은 그대로. 랄프로렌 'Asia' 지역을 한국 지역으로(KOREA_PAT),
       제냐 반기(H1) 추출은 지역·채널 카드에 '최근 공시 기간(누적)', 기간 이름 'FY26 상반기'(perKo) · 톰브라운 통화 설명에 '달러' ·
       브랜드 상세 최근 뉴스는 한글 검색어를 띄어쓰기 없이도 맞춤(chkNewsList — '톰 브라운'·'스톤 아일랜드' 기사)
v33.7: (대표 지시 2026-10-19 '바로 추가 7개' + '써코니도') 네이버 감시 브랜드 8개 추가(naver_trend v1.8)에 맞춰 원산지 통화 CHK_CUR — 아식스·
       오니츠카타이거·미즈노 엔, 살로몬 유로(프랑스), 아크테릭스·룰루레몬 달러(캐나다 브랜드 — 캐나다 달러는 받지 않아 본사 실적 통화인
       미국 달러로 대신, 노르다처럼 표시), 온러닝 스위스 프랑(fetch_data v4.15부터 1년 평균 대비), 써코니 달러. 판정 규칙은 그대로.
       '판매 vs 검색' 설명에 네이버 선 범위(추가 8개는 월간 합계에서 뺌)를 적음
v33.6: (대표 지시 2026-10-17 '적출국별 부산향 · 에어는 인천 · 수입 수출 정보·추이 모두' + 공공데이터포털 인증키) 더보기 › 물류에 logistics_fetch v1.2
       새 자료 3개 — 수입 묶음: '나라별 → 부산항(바닷길 TEU)·인천공항(항공 톤) 도착 물동량'(관세청 국가별 입항, 칩으로 바꿈 · 제목도 칩 따라 ·
       인천·평택·광양항 등은 빠짐을 적음 · 적출 거점 나라 먼저 + 원산지·생산국·그 밖 많은 나라는 '나라 더 보기' — 묶음은 logistics_fetch가 저장한
       groups(VOL_GROUPS) · 최근 12달 기록 없는 지정 나라는 목록 밖 한 줄 · 전년 같은 달 대비 · 눌러서 최근 36달 추이) + '부산항 입항 컨테이너선'
       (해수부 입항 신고 · 수출 선적·환적 배 포함 · 어제까지 최근 7일 하루 평균 · 지난 4주·1년 전 같은 7일 대비 · 직전 출항지 나라 · 체류시간 ·
       주별 그래프). 수출 묶음: '나라별 ← 부산항·인천공항 출발 물동량'(관세청 국가별 출항 · 수출만 · 목적지 = 화물목록상 내리는 곳(허브 나라로
       잡힐 수 있음) · 항공 B/L 설명은 방향별(수입 해외직구 · 수출 역직구)). 출처 입력 오류로 보이는 값(odd)은 logistics_fetch가 찾아 저장 —
       화면은 그 나라·달에 '출처 값 확인 필요'(보조 값 톤·B/L도), 전체·몫은 이상값을 뺀 합(total_clean), 전년 같은 달 대비는 두 달 중 한 달이라도
       이상값인 나라를 두 달 모두에서 뺀 yoy(같은 나라끼리 — 'OO 빼고'). 작은 선 그래프는 빈 값을 제자리에 비워
       둠(마지막 달이 비면 끝 점 없음 · 끝 점이 잘리지 않게 overflow). 화면에 안 쓰는 보조 시계열·오래된 선박 상세는 넣지 않음(첫 화면 무게).
       나라별 물동량은 색 없음(늘고 줄어도 좋고 나쁨이 아님) · 입항 척수는 늘면 파랑 · 체류시간은 늘면 주황
v33.5:(대표 지시 2026-10-16 '부산발이 아니라 적출국별 부산향 · 에어는 인천 · 수입 수출 시 필요한 정보·추이는 모두 · 1번부터, 적출국은 홍콩·
       로테르담·두바이·벨기에 외에 글로벌 주요 물류 거점 순') 더보기 › 물류를 수입(적출 거점 → 부산 · 항공 → 인천) · 수출(부산 → 해외) ·
       공통 위험 신호(해협 · 중동 항만 · 정시율 · 뉴스) 세 묶음으로(맨 위 칩으로 바로 가기). 수입 = 적출 거점 12곳(logistics_fetch v1.1 hubs —
       대표 지정 홍콩·로테르담·두바이·앤트워프 → 세계 1~5위 상하이·싱가포르·닝보·선전·칭다오 → 지역 대표 LA/롱비치·포트클랑·함부르크)
       그 항만 컨테이너선 하루 입항(한국행만 아님 · 전쟁 전·1년 전 같은 주 대비, 눌러서 추이·한국까지 길목(유럽 = 전 세계 수에즈 쪽 비율,
       두바이 = 호르무즈)·관세청 그 지역 한국향 운임) + 부산 입항 + 한국향 운임(관세청 수입, 바닷길 부산 등 전국·항공 인천공항 도착).
       수출 = KCCI 부산발 + 관세청 해상 수출(한국발 운임, 이미 받던 자료). 항만 입항 카드는 '중동 항만'(걸프 안 제벨알리 ↔ 해협 밖 우회
       코르파칸·푸자이라, 부산은 수입 위로). 맨 위 6칸 이름 정리(유럽→인천 항공 · 부산→중동 수출)
v33.4: (대표 지시 2026-10-16 '만들어줘' — 지정학 리스크로 물류비·운송기간 추이를 한국향·중동 기준으로) 더보기 › '물류'(환율 아래, #/more/logi) —
       docs/logistics.json(logistics_fetch v1): 맨 위 6칸(유럽→한국 바닷길 40ft·항공 kg당 · 부산→중동 KCCI · 호르무즈 컨테이너선 · 수에즈 쪽 비율 · 정시율),
       한국향 운임(관세청 수입신고 운임, 출발지별 전월·전쟁 전 2월·1년 전 대비 + 24달 그래프 · 바닷길/항공 칩), 부산발 운임(KCCI 중동·북유럽·지중해·미주·종합 52주),
       해협 통과(호르무즈·바브엘만데브·수에즈·희망봉 컨테이너선 하루 평균 · 수에즈 ÷ (수에즈+희망봉) = 수에즈 쪽 비율), 항만 입항(부산·제벨알리·코르파칸·푸자이라),
       전 세계 정시율(13달 막대), 물류·운임 뉴스 5건. 색 = 트렉시에 좋은 쪽 파랑(운임·지연 내림, 통과·정시율 오름). 수집 상태에 '물류 운임·바닷길' 줄.
       시장 › 뉴스 칩 '산업 › 물류·운임'(news_monitor v2.14). 선 아이콘 'ship'
v33.3: (대표 지시 2026-10-15 — 2019년 기사가 최근 나이키 뉴스로 보임) 뉴스 날짜를 원문 날짜(news_monitor v2.13 orig_date — 원문 페이지에서
       확인한 발행일)로 먼저 보이고, 올해가 아닌 날짜엔 연도('2025.12.30(화)'). 지난 뉴스 검색에도 원문 날짜. 수집 상태 뉴스 줄에 옛 기사
       제외 건수(구글이 새 날짜로 다시 낸 지난 기사)·구글 링크 풀기 실패. news.json stale_titles·boards(옛 기사 기억)는 페이지에서 뺌
v33.2: (대표 승인 2026-10-14) '어제와 달라진 판정' — 브랜드 점검표 판정을 파이썬으로도 계산(chk_verdicts, 화면 chkModel과 같은 규칙·
       CHK_CUR 한 곳에서 화면에 넣음)해 history_append v1.2가 매일 history.json verdicts에 기록. 화면은 지금 판정을 바로 전 기록과 비교:
       오늘 ① 매입 검토에 '어제와 달라진 판정 n곳 · 클락스 관망 → 지금 검토(환율 0 → +1)'(없으면 머리에 '어제와 같음'),
       브랜드 목록 행·판정 안 함 행에 '어제 관망' 꼬리표, 브랜드 상세에 판정 기록 한 줄(바뀐 점수 또는 같은 판정이 이어진 첫 날).
       규칙 판(CHK_RULE)이나 비교 기준(chk_sig: 감시 브랜드·본사 연결·원산지 통화표)이 다른 기록과는 비교하지 않음 — 목록이 바뀐 날 생긴
       판정 변화를 '어제와 달라진 판정'으로 보이지 않게(화면에는 비교할 수 있는 기록의 최근 60개만 · verdicts_start = 첫 기록일).
       오늘 기록이 화면 판정과 다르거나 기록 모양이 틀린 브랜드는 비교에서 빼고 더보기 › 수집 상태에 '판정 기록 비교 제외 n곳'.
       환율 화면 '알림 없이 표시만'의 파운드에 1년 평균 대비(fetch_data v4.14, 점수 기준이라 먼저)
v33.1: (대표 승인 2026-10-14 '추천대로') 시장 › 뉴스 맨 위 지난 뉴스 검색창 — 요약·원문 제목·브랜드·매체에서 찾음(띄어 쓴 낱말은 모두 들어간 기사,
       대소문자·악센트 무시). 최근 기사는 바로, 1년 보관(news_archive.json, news_monitor v2.12)은 검색창을 처음 누를 때 한 번 내려받아 나눠 합침.
       결과 = 최신순·월별 30건씩(같은 제목은 1건 — 별점은 그중 가장 높은 것), 찾은 낱말 강조, 고른 칩(구분) 안에서, 맨 아래 'Google 뉴스에서 더 찾기'.
       검색어·펼친 수는 화면 기록에(뒤로·새로고침에도 그대로), 한글 조합 중 0건은 깜빡이지 않게. 기사 날짜 형식기는 한 번만 만듦(뉴스 목록도 빨라짐).
       수집 상태 뉴스 줄에 보관 건수(저장 실패·일부만 복구면 일부 실패)
v33: (대표 승인 2026-10-12 'A안 · 오늘의 결정') 하단 탭 6개 → 4개(오늘·브랜드·시장·더보기). 오늘 = 수집 지연 띠 + 결정 카드 4장(① 매입 검토 ② 환율 타이밍
     ③ 다가오는 일정 ④ 오늘 중요 뉴스) + 트렉시 위치 + 갱신·수집 상태·이번 달 Claude 사용액. 브랜드 = 점검표 탭(판정 필터·한 줄 이유·점수 4칸·판정 기준(i)·
     판정 안 함 접기) + 브랜드 상세(판정 이유·근거 4장·최근 8주 검색·다음 일정·뉴스·본사 기업 상세). 시장 = 칩 6개(뉴스 · 캘린더 · 실적·재고 · 기업 · 국내 ·
     소싱 지도)에 옛 종합·기업·캘린더·뉴스·국내 화면. 더보기 = 유통사 비교·패션 브랜드·환율·해외직구·수집 상태·화면 테마(전역 머리 대신 — 밝게·어둡게).
     휴대폰·화면 '뒤로' = 들어온 화면·스크롤(브라우저 기록), #/brand/아디다스 같은 주소. 화면 = IBM Plex Sans KR(구글 글꼴 — 첫 화면을 그린 뒤 한 번에 적용, 그 전·못 받으면 시스템 글꼴 그대로, 바꿀 때 크게 밀리는 화면은 다음 화면 이동 때)·흰 바탕·잉크·
     파랑 하나(#0043FF, v21 CI 블루)·판정 배지 3종·+ 파랑/− 짙은 주황(주가는 색 없음)·선 아이콘(이모지·국기 대신 글자)·글자 13px·누르는 곳 44px·키보드(Esc·Enter·패널 안 Tab·화면 이동 뒤 초점)·
     다크 모드 유지(더보기 '화면 테마'). 버그: 캘린더 '오늘' 하루 밀림 · 지도 표 머리글 · 딕스 부문 표 잘림 · 'FYnfinity' · 내장 데이터 '</' · 화면 요소 하나 빠지면 전체 빈 화면
v32.17: (대표 지시 2026-10-10, 8번 ①) 더보기 '🧭 브랜드 점검표' — 네이버 감시 브랜드 중 본사가 상장사로 연결된 곳을
        '지금 검토 / 관망 / 주의'로 판정: 국내 수요(검색 전년 대비, 감시 브랜드 중앙값 ±10%p) + 매입 조건(본사 재고 압력 ±5%p ·
        본사 발언 신호(extract_segments v11.2 sig) · 원산지 통화 1년 평균 대비 ±5%/±10%). 다음 세일·최근 뉴스는 참고 줄.
        본사 재고·발언 자료가 둘 다 없는 브랜드는 검색·환율만 표로(판정 안 함). 신호 분류 전 발언은 '분류 전'으로(중립과 구분),
        재고 줄에 '새 실적 반영 대기'·이전 값 표시, 뉴스는 브랜드 이름이 있는 기사만. 소싱 지도에 바로가기, 본사 발언 카드에 신호 표시
v32.16: (대표 지시 2026-10-10) 더보기 › 수집 상태에 '🤖 Claude 사용액' — 이번 달(지난달) 작업별 금액·호출 수·원화 환산.
        각 수집 스크립트가 저장한 월별 claude_usage(news_monitor v2.10 · extract_segments v11.1 · ir_fetch v1.4 · dart_fetch v3.6) 합.
        기록을 이번 달에 시작했으면 시작일 표시. 더보기 메뉴의 수집 상태 줄에도 이번 달 금액
v32.15: (대표 지시 2026-10-10) 기업 상세에 '🗣️ 본사 발언' — 실적 문서의 재고·할인·유통 통제 문장(원문 + 한국어 요약, 최대 3개).
        extract_segments v11·ir_fetch v1.3이 원문에 있는 문장만 저장. 새 형식으로 추출되기 전엔 카드 없음
v32.14: (대표 지시 2026-10-10) 재고 증감을 같은 기간끼리 비교 — 분기 재고·같은 분기 매출이 있으면 최근 분기 vs 1년 전 같은 분기
        (fetch_data v4.13), 없으면 연간 결산끼리. 재고 경고·기업 목록·소싱 지도·상세에 비교 기간('26.06 vs '25.06) 표시
v32.13: (2026-10-09) 분기 실적 판정은 기간 문구의 첫 구절만 봄 — 딕스 추출 'Q2 … (13 weeks); also 26 weeks …'가 누적으로 잘못 판정돼
        '본체 +5.6%'·'딕스(본체)' 표가 안 나오던 문제. 부문 표 YoY가 비면 당기·전년 매출로 계산
v32.12: (대표 지시 2026-10-09) ① 순위 숫자 바로잡기 — 성장 순위에 기준(분기 '26.06 / 연간 FY25, 오래된 결산도 연도만 붙여 둠),
        공시(SEC·IR) 분기가 야후보다 45일 넘게 새로우면 '새 실적 반영 대기', 딕스는 인수 효과 기간(ACQ)엔 순위·재고 경고에서 빼고 각주,
        삼성물산(전사 수치)은 순위·재고 경고·KPI에서 뺌. ② 휴대폰 화면 다듬기(KPI·이름 2줄·그래프·뉴스·지표 추이·소싱 칩·DART 링크 등).
        ③ 수집 상태에 일부 실패 수(이전 값 + 값 없음, 각 수집 스크립트의 실패 목록 기준), 이전 값 쓴 종목·환율에 '이전 값(MM/DD)'
v32.11: (대표 지시 2026-10-09) ① 종합 탭 맨 위 '오늘 볼 것' 4줄 — 환율(감시 통화 중 1년 평균 대비 가장 싼 통화) · 다음 해외 세일
        2개(진행 중/D-day) · 오늘 ★3 뉴스 · 트렉시 유통사 비교 위치, 누르면 해당 화면. 이미 페이지에 있는 데이터만 씀.
        ② 뉴스 탭 기본 보기 = 오늘 전체 + 최근 7일 ★3(날짜마다 '★1~2 N건 더 보기', 8일 이전은 맨 아래 펼치기) — 칩으로
        거르면 지금처럼 전체. NEW 배지 제거(날짜 머리글에 '오늘'), 날짜 '10/7(수)', 칩 한 줄 가로 넘김, 뉴스는 탭을 처음 열 때 그림,
        화면에 안 쓰는 news.json 항목(seen_ids·seen_titles·model_compare)은 페이지에서 뺌. '오늘' 표기는 보는 사람의 한국 날짜 기준
v32.10: (대표 지시 2026-10-09) ① 재고 증감은 늘면 빨강·줄면 초록(fmtInv) — 재고 경고 카드에서 늘어난 재고가 초록으로 덮이던 버그,
        기업 표·상세·비교 표의 재고 색 반대 문제. 재고 경고: 9곳 이상이면 전체 보기, 기준 문구, KPI 설명을
        '재고가 매출보다 빨리 느는 곳'으로. ② 재무 지표 '확인 필요' 각주를 '값 확인(…)'으로(dart_fetch v3.5 capex·lease 포함).
        ③ 스케쳐스코리아(krd:skechers_kr) 로고·뉴스 연결
v32.9: 기준·통화 표기(대표 요청 2026-10-09, dart_fetch v3.4·fetch_data v4.11) — ① 국내 법인 카드에 회계기준(K-IFRS/일반기업회계기준,
       연도별 전환 표시)·보고서 종류(사업보고서/감사보고서) 태그, 사업보고서 6곳은 '🔗 연결 기준 요약'(비교 화면은 별도 유지), 연결감사보고서만
       있는 곳은 DART 원문 링크. 상장사 출처 줄의 '연결' 고정 문구 → 실제 기준. 야후(연결) 매출이 DART와 20% 넘게 다른 종목(LS네트웍스)은
       분기 매출 증감을 순위에서 빼고 상세에 '야후 연결' 표기. 플랫폼 카드 각주를 회사별 기준으로. ② 금액에 통화 항상 표기 — 원화 '조원/억원',
       외화 'B USD', 기업 목록 외화 매출은 ≈원화 환산 + 원래 통화, 지역·채널 금액에 공시 통화, 현재가 펜스·원·엔 표기, 재무·주가 통화가 다르면 안내.
       ③ 재무 지표 카드: 회사명 아래 회계기준 배지, 안정성에 '순차입금(리스·RCPS 제외)', 기준이 섞인 비교군에서 순부채·부채비율 등에 안내
       리뷰 반영: 기업 목록 매출 단위 '원'은 머리글로(휴대폰 폭 v32.8과 같게, 넘치면 가로 스크롤), 엔화 환산은 100엔 기준, 배지·'회계기준
       미확인'은 dart v3.4 수집 후에만, 순차입금(리스·RCPS 제외)은 순부채와 겹쳐 '중앙값보다 나은 지표' 점수에서 뺌.
       수집 상태: DART 일부 법인 실패(이전 값 유지)면 '일부 실패 N곳' 표시
v32.8: (대표 요청 2026-10-06) ① 더보기 › 패션 브랜드: 국내 패션 13곳·아이웨어 6곳도 유통사와 같은 재무 지표 카드(그룹·지표 선택은
       카드마다 따로), 맨 아래 '📊 검색 관심도 vs 실적'(같은 해 네이버 검색 증감 vs 매출 증감 · 올해 1월~지난달 · 최근 4주).
       ② 캘린더 탭: 해외 세일 시즌(블프·유럽 법정 세일·광군제·618·박싱데이 등) — 달력에 기간 표시 + '🛍️ 해외 세일 시즌' 카드.
       ③ 뉴스 탭 '산업 ▸ 통관·상표권' 칩. ④ 네이버 카드: 검색량 적은 브랜드는 순위 맨 아래
v32.7: 뉴스 탭에 '국내 비교 ▸ 유통사 · 패션 브랜드' 칩(news_monitor v2.5, 대표 요청 2026-10-06) — 국내 법인 상세의 최근 뉴스도
       DART 법인 id로 연결. 네이버 검색 관심도 카드에 '아이웨어' 버튼(naver_trend v1.4 글로벌 아이웨어 11개 + 젠틀몬스터·
       블루엘리펀트, 중앙값은 이 13개끼리). 연결 기업·뉴스가 없는 브랜드 줄은 누를 수 없게
v32.6: 더보기 '👕 패션 브랜드' 한 화면에 국내 패션 브랜드 비교 + 그 아래 아이웨어 비교(대표 요청 2026-10-05) — 아이웨어 메뉴 줄 삭제.
       기업 탭 '패션 브랜드 비교'·'아이웨어 비교' 칩 삭제(중복). 더보기에서 연 상세에서 돌아오면 보던 위치로 스크롤
v32.5: 국내 탭 정리(대표 요청 2026-10-05) — 🛒 국내 온라인 플랫폼 카드는 기업 탭 '🛒 온라인 플랫폼' 칩으로 이동(칩을 누르면
       표 대신 이 카드), 👕 국내 패션 브랜드 비교·🕶️ 아이웨어 비교는 더보기 별도 화면으로 이동. 국내 탭에서는 셋 다 삭제
v32.4: 🏷️ 수입 브랜드 유통사 비교를 국내 탭에서 더보기 › 유통사 비교로 이동(대표 요청 2026-10-05) — 메뉴 줄에 트렉시
       '중앙값보다 나은 지표' 수 표시. 기업 탭 '유통사 비교' 칩 삭제(중복). 더보기에서 연 기업 상세의 '뒤로'는 그 더보기 화면으로
v32.3: 트렉시(자사)는 '🏷️ 수입 브랜드 유통사 비교' 카드와 그 상세에만 표시(대표 요청 2026-10-05, 나중에 합침) —
       기업 탭 목록·종합 탭 신호·🛒 국내 온라인 플랫폼 카드에서 제외(PEER_ONLY 한 곳에서 관리)
v32.2: 순부채 정의에 RCPS 부채 포함(대표 결정, dart_fetch v3.2) — 식 문구 수정, '확인 필요' 사유에 부채 항목 누락 추가
v32.1: 유통사 재무 지표 — 보고서 간 값이 다른 항목(dart_fetch v3.1 fin.bad)을 쓰는 지표만 '확인 필요'로 표시
       (예: 차입금이 다르면 순부채·순부채/EBITDA만), 기업 상세에 다른 항목 이름 표시
v32: 🏷️ 수입 브랜드 유통사 비교 카드를 재무 분석 지표 카드로 교체(2026-10-03 목업 승인) — 그룹 탭 5개(손익·성장/수익성/
     운전자본/현금/안정성) + 지표 칩 17개(매출·성장률·매출총이익률·영업이익률·ROE·재고·매출채권·매입채무일수·현금전환주기·
     OCF·FCF·이익의 현금화·순부채·순부채/EBITDA·부채비율·현금·순자산), 3개년 표(트렉시 맨 위·중앙값 행)·최근 연도 순위 막대·
     식/좋은 방향 상자. OCF·FCF는 매출 대비, 순부채는 순자산 대비 비율로 순위. 현금·순자산은 순위 없는 참고 지표.
     추출 검증 실패 연도는 '확인 필요'. 기업 상세에 재무 지표 3개년 표. 패션·아이웨어 카드는 기존 그대로(dart_fetch v3.0)
v31.2: 아이웨어 비교에 케어링아이웨어코리아·시원아이웨어 추가(dart_fetch v2.9) — 6곳
v31.1: 국내 탭 '👕 국내 패션 브랜드 비교' 카드(dart_fetch v2.8 13곳: 에이유브랜즈·피스피스스튜디오·에스제이그룹·마뗑킴·
       레이어·하이라이트브랜즈·하고하우스·비케이브·파이브스페이스·코자·안다르·시선인터내셔널·로우클래식) — 수입 브랜드
       유통사 비교 카드를 공통 비교 카드로 바꿔 함께 사용(자사 강조는 유통사 비교에만). 기업 탭 칩 '패션 브랜드 비교'.
       네이버 검색 관심도에 '수입·해외 / 국내 패션' 전환(naver_trend v1.3 group) — 중앙값은 그룹 안에서만 계산.
       '🕶️ 아이웨어 비교' 카드(국내 브랜드 젠틀몬스터·블루엘리펀트 vs 룩소티카코리아 vs 다비치안경체인) + 기업 탭 칩,
       글로벌 아이웨어 에실로룩소티카(EL.PA)·사필로(SFL.MI) 표시 정보
v31: 하단 탭에 '더보기'(6번째) — 새 지표는 탭을 늘리지 않고 여기에 쌓음.
     ① 💱 환율: 엔·유로·달러 1% 칸 알림(1년 평균 대비 %, 다음 내림·오름 알림 가격, 1% 칸 막대, 1년 추이와
        알림 날짜 점, 최근 알림 목록) + 파운드·헤알은 값만 + 내릴 때·오를 때 참고 상자 (fetch_data v4.9)
     ② 🌏 해외직구: 통계청 해외직접구매액(분기) 요약 3칸·나라별 막대(의류·패션/스포츠)·최근 8분기 (kosis v5)
     ③ ⚙️ 수집 상태: 종합 탭 맨 아래에서 이동(지연 시 종합 상단 경고 띠는 유지 → 누르면 여기로)
     소싱 지도 지역 패널(유럽·북미·일본)에 '한국 소비자 직구' 한 줄, 환율 줄에 1년 평균 대비 %
v30.5: 소싱 지도에 북미·일본 추가(5개 지역) — 지도(worldmap v2: 기타에서 미국·캐나다·일본 분리, 서쪽 확장)·
       브랜드 지역 대응(북미: 나이키·아디다스·아식스·언더아머 직접, 크록스·데커스 추가 / 일본: 아식스 직접·아디다스
       일본+한국, 나머지 아시아·태평양 합산 → 추정 표시)·현지 유통 재고(북미 딕스·아카데미·TJX·로스·벌링턴, 일본 ABC마트)·
       환율(북미 달러, 일본 엔 — 100엔 단위 표시)
v30.4: 국내 탭에 "🏷️ 수입 브랜드 유통사 비교" 카드 — 트렉시 + DART 감사보고서 공시 유통사 8곳.
       ① 순위 요약(트렉시가 앞서는 지표를 먼저·강조) ② 재무 비교표(트렉시 맨 위 고정·지표별 순위 배지·비교군 중앙값 행)
       ③ 성장성 비교 막대(전년 대비 / 2년 연평균, 트렉시 강조색·나머지 회색·중앙값 점선, 누르면 값 표시).
       수치는 공시 그대로(가공 없음). 기업 탭에 "유통사 비교" 칩. 로고: 오케이몰·하하몰·비블루
v30.3: 국내 온라인 플랫폼 카드 — 발란은 결산월 대신 상태(2026.2 회생 폐지 · 청산 절차) 표기
v30.2: 국내 탭에 "🛒 국내 온라인 플랫폼" 카드 — 쿠팡·무신사·크림·트렌비·발란·머스트잇·트렉시(자사)를 한 표로
       (매출 원화 기준 큰 순, 전년 대비·영업이익률·재고 증감, 누르면 상세). 국내 그룹의 외화 실적(쿠팡 달러)은
       최근 환율로 원화 환산(≈)해 기업 목록·상세에 함께 표시 — 옆 기업의 조·억 단위와 맞춤
v30.1: 15곳 추가 연결 — 상장 10곳(휴먼메이드·비바굿즈(클락스)·불카브라스·ABC마트·탑스포츠·TJX·로스·벌링턴·
       럭스익스피리언스·쿠팡) 로고·국기·뉴스, 국내 법인 5곳(크림·트렌비·발란·머스트잇·트렉시) 로고.
       소싱 지도 현지 재고에 유럽 럭스익스피리언스·남미 불카브라스 추가. 재무 금액 통화는 재무제표 통화
       (fin_currency) 우선 — 홍콩 상장 중국 기업은 위안(CNY), 마이테레사는 유로로 표시
v30: 국내 탭 — ① 국내 수요 한눈에(판매 vs 검색): KOSIS 온라인 신발·의복 거래액과 네이버 브랜드 검색량 합계의
     전년 대비(%)를 한 축에 겹친 그래프(눌러서 월별 값, 범례로 선 켜고 끄기) ② 브랜드 검색 관심도(네이버):
     전년 대비순/규모순, 상위 10개·전체 보기, 1년 추이(전년 점선), 중앙값 대비 색. 브랜드 상세에 검색 관심도 카드,
     연결 없는 브랜드는 눌러서 그 브랜드 뉴스만 보기. 수집 상태에 네이버 검색 관심도 추가
v29.3: 소싱 지도 지역 판정에 현지 유통 재고(재고 과잉형)·환율 반영 — 점수제(브랜드 최대 2 + 유통 ±1 + 환율 ±1,
       3점 이상 높음), 지역 패널에 점수 내역 표시. 중동 현지 유통사에 세노미 리테일(4240.SR) 연결
v29.2: 영국 상장사(JD·프레이저스·닥터마틴) 재무 통화 표기 GBp(펜스)→GBP(파운드) 수정 — 주가는 펜스 그대로
v29.1: 닥터마틴(DOCS.L) 로고·국기·뉴스 연결, 뉴발란스(이랜드월드) 국내 법인 상세에 뉴발란스 뉴스 연결
v29: 소싱 지도 2단계 (뉴스 3건 표시는 같은 기사 다른 출처 중복 제거 — 기업 상세 최근 뉴스 카드 포함)
v29.0: 소싱 지도 2단계 — 지역 패널에 ① 현지 유통사 재고(유럽 JD·프레이저스·잘란도, 남미 그루포 SBF)
     ② 환율(현지 통화→원화 1년 변동, 매입 부담 판정) ③ 현지 유통 뉴스(최근 14일 선별 3건). 기회 수준 계산에는 아직 미반영
v28.1: 지도의 지역 도형(유럽·중동·남미)도 누르면 패널 열림, PC는 마우스 올리면 강조
v28: 🌍 소싱 기회 지도 — 종합에 지도 카드(새 탭 없이), 지역 위 브랜드 로고 배지 → 하단 패널(브랜드 목록·근거),
     가정 2종(재고 과잉형=보완안 / 시장 확대형=원안) 전환, 브랜드×지역 표·계산 방식은 패널.
     종합의 '한국이 속한 지역 성장' 카드는 지도 표의 '한국 수요' 열로 통합(중복 제거·길이 유지).
     지도 경계: docs/worldmap.json (world-atlas 110m 단순화)
v27: ① 🇰🇷 한국 시장 신호 — 브랜드 상세 첫 카드(국내 법인 DART · 본사 공시의 한국이 속한 지역 · 국내 소매 KOSIS),
       종합에 '한국이 속한 지역 성장' 카드(본사 공시 기준, 환율 제외 우선)
     ② 수집 상태 — 소스별 마지막 갱신·주기·지연 판정(열람 시점 기준), 지연 시 종합 상단 경고 띠
v26.1: '환율 제외'를 막대 아래 별도 줄로 이동(막대 위 겹침 해소), 막대 위 수치에 옅은 바탕
v26: 지역·채널 카드에 '환율 제외' 성장률 병기(IR 자료의 현지 통화 기준), 금액 없이 증감률만 공시된
     지역(푸마 북미·라틴·중화권 등)을 카드 하단에 별도 표기
v25.2: 지역·채널 카드 제목을 공시 기간 성격에 맞게(분기 / 누적) 표기 — 아식스 결산단신(누적) 대응
v25.1: 기업 펼침 행 가로 넘침 수정 — 펼침 셀은 줄바꿈 허용(nowrap 예외), 모바일은 1열 목록,
       지역 요약에서 합계(Total) 항목 제외
v25: Phase 7-A — docs/segments_ir.json(아디다스 Fact Sheet·푸마 보도자료) 병합.
     IR 출처는 태그 'IR 추출'로 구분, 기업 펼침의 지역·채널 요약에도 반영
v24: ① 재고일수(재고÷매출원가×365) — 기업 펼침·상세 재고 카드·종합 재고 경고에 표시
     ② 글로벌 본사 vs 국내 법인 대비 카드(매출 성장·영업이익률·재고 증감·재고일수) — 양쪽 상세에
     ③ 상세 하단 '최근 뉴스' 3건(뉴스 탭 브랜드 키 연결)
v23.1: 상세 표 줄바꿈 금지(법인 실적 7열·수익성·국내 13개월 표) — 셀 nowrap, 결산 열 'FY25' 한 줄,
       표가 카드보다 넓으면 표만 가로 스크롤(화면 전체는 고정)
v23: 국내 상장 19개사 재무를 DART 연결 재무제표(docs/kr_listed_fin.json)로 교체(빌드 시 병합 —
     3개년 매출·매출총이익률·영업률·재고·재고 증감), 야후는 주가·분기YoY·실적일만. 국내 법인 카드에
     재고·재고 증감 열 추가, 종합 재고 경고에 국내 법인 포함. 상세에 '재무: DART 연결' 출처 표기
v22.3: 기업 표 줄꺾임 수정 — 헤더·수치 줄바꿈 금지, 기업명은 말줄임, 라벨 축약(총이익률)
v22.2: 로고 표기 통일 — 종합·기업 표·캘린더·상세 모두 브랜드명 앞에 로고(실패 시 이니셜 배지),
       국기는 상세 헤더에만 보조 표기. 국내 법인 13개 로고 도메인 추가
v22.1: 가로 넘침 수정 — KPI 격자 minmax(0,1fr)·min-width:0·줄바꿈 허용, 내용 영역 overflow-x 차단,
       모바일 KPI 수치 크기 축소. 성장 순위에서 ±100% 초과(기저·인수 효과)는 제외하고 각주 표기
v22: 상단 탭 → 하단 탭바(앱 형태). 100dvh 세로 배치(헤더 고정·내용 스크롤·탭바 하단 밀착,
     iOS 홈화면 안전영역 반영), 아이콘+라벨 5탭
v21.1: 종합 KPI 칩 동작 — 성장 1위→해당 기업 상세, 재고 경고→재고 경고 카드로 스크롤·강조
v21: A안 레이아웃 — 종합(신호 KPI 4·올해vs작년 꺾은선·성장 상하위·재고 경고·실적 일정) /
     기업(검색·그룹 칩·압축 표·행 펼침·전체 상세) / 캘린더(2개월 달력 + 90일 목록) /
     영문 약어 우리말화(매출총이익률·전년 대비) · CI 블루 적용
v20: 국내 법인 카드 문구를 DART 자동 수집(dart_fetch.py) 기준으로 갱신, 공시 미발견 법인 사유 표기
v19: Phase 6 국내 법인(비상장, DART 반자동) — docs/kr_domestic.json 표시.
     서머리 '국내 법인(비상장)' 그룹, 글로벌 브랜드 상세에 '국내 법인 실적' 카드 연결,
     비상장 법인 자체 상세(드롭다운 그룹), 수치 미입력은 '미확인'
v18: 타이포 스케일 통일 — 6단계 변수(--fs-2xs 10 / xs 11 / sm 12 / base 13 / lg 15 / xl 17px)로
     모든 요소 크기 일괄 정리, 인라인 font-size 제거
v17: 국내 상장 20개사 편입 — 6그룹(글로벌 브랜드/글로벌 유통/국내 브랜드/국내 패션대기업/
     국내 OEM/국내 유통) 헤더로 구분, 원화 억원·조원 표기, 상세 드롭다운 그룹 분리,
     상세 헤더에 그룹 태그·종목 주석, 한국 상장은 '공시 추출 미대상' 표기
v16: 브랜드 상세에 '지표 추이' 카드 — docs/history.json(일별 스냅샷 누적) 기반
     재고YoY·GM·분기YoY·매출YoY 스파크라인, 3점 미만이면 '축적 중' 안내
v15: buildKR() 초기 호출 누락 수정 — 국내 탭이 비어 보이던 원인(호출문이 뉴스 칩
     클릭 핸들러에 잘못 삽입되어 있었음)
v14: 국내 탭 금액 단위 환산 수정(백만원 → 억/조)
v13: 국내 수요 탭 추가 — KOSIS 월별 지표(소매판매·업태·온라인 거래액·CPI)
     스파크라인 + 최근값·YoY, 지표 클릭 시 최근 13개월 표
v12: 기간 라벨 명시(연간/최근 분기) + 지역 분해가 Total 단독인 경우
     '지역별 매출액 미공시' 안내로 표시(룰루레몬 케이스 혼동 방지)
v11: 뉴스 탭 — 브랜드(스포츠·아웃도어/패션/명품/유통·그외)·산업(스포츠/패션·명품/유통)
     필터 칩, 오늘 신규 NEW 배지, 날짜별 그룹, 14일 롤링(news.json v2)
v9: 브랜드 로고 앞 국기(브랜드 본사 국가) 표시 + 신규 8종목 로고 도메인 추가
v8: 서머리 한 줄 셀(FY매출/YoY 분리, 52주比→상세, 행 클릭 시 기준 시점·통화)
    + 지역/채널 당기vs전년 페어 바(비중 변화 병기, 전년 미기재 시 [역산])
docs/data.json + docs/segments.json(있으면) → docs/index.html
"""

import json
import re
import os
import hashlib
import datetime

TEMPLATE = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>스포츠 산업 모니터</title>
<meta name="theme-color" content="#ffffff" id="themeColor">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<style>
/* v33 A안 토큰 — 흰 종이 · 검정 잉크 · 파랑 하나(#0043FF, v21 CI 블루). 옛 이름(--pos·--neg·--up·--down·--barbg 등)은 새 값을 가리켜
   옛 화면이 그대로 따라옴. 다크 = [data-theme="dark"](더보기 '화면 테마'). 글자는 13px 바닥(옛 6단계 2xs~sm도 13px) */
:root{color-scheme:light;
 --bg:#ffffff;--card:#ffffff;--fill:#f3f4f6;--line:#e5e7eb;--line2:#f0f1f3;
 --tx:#111111;--tx2:#374151;--sub:#4b5563;--muted:#6b7280;
 --accent:#0043FF;--accent-fill:#0043FF;--on-accent:#ffffff;--accent-weak:#eef3ff;
 --bad:#9a3412;--warn-bg:#f6ad72;--warn-fg:#5a1f08;--hold-bd:#6b7280;--hold-fg:#374151;
 --pos:var(--accent);--neg:var(--bad);--up:var(--accent);--down:var(--bad);
 --barbg:var(--fill);--accent-prev:#b2c6ff;--chart-prev:#9ca3af;--s-naver:var(--accent);--s-shoe:#9a3412;--s-apparel:#6b7280;
 --lv2-bg:#0043FF;--lv2-fg:#ffffff;--lv1-bg:#becfff;--lv1-fg:#0b1a4a;--lv0-bg:#e9edf5;--lv0-fg:#374151;
 --lv2-map:#0043FF;--lv1-map:#90adff;--lv0-map:#c3cfe9;--lv2-ring:#0043FF;--lv1-ring:#799dff;--lv0-ring:#b9c4de;
 --map-sea:#f9fbfe;--map-land:#e8ebf0;--map-kr:#111111;
 --fs-2xs:13px;--fs-xs:13px;--fs-sm:13px;--fs-base:13px;--fs-lg:15px;--fs-xl:17px;
 --fs-name:17px;--fs-title:20px;--fs-page:22px;--fs-dhead:26px;--fs-tile:28px;--fs-hero:30px}
[data-theme="dark"]{color-scheme:dark;
 --bg:#0f1115;--card:#16191f;--fill:#1f232b;--line:#2b313b;--line2:#232831;
 --tx:#f3f4f6;--tx2:#d1d5db;--sub:#9ca3af;--muted:#9ca3af;
 --accent:#7aa2ff;--accent-fill:#3b6cf0;--accent-weak:#1b2440;
 --bad:#fb923c;--hold-bd:#9ca3af;--hold-fg:#e5e7eb;
 --accent-prev:#3a4a78;--chart-prev:#6b7280;--s-shoe:#fb923c;--s-apparel:#9ca3af;
 --lv2-bg:#3b6cf0;--lv1-bg:#2c437f;--lv1-fg:#e5e7eb;--lv0-bg:#232831;--lv0-fg:#9ca3af;
 --lv2-map:#3b6cf0;--lv1-map:#3456a8;--lv0-map:#394254;--lv2-ring:#7aa2ff;--lv1-ring:#4b64a8;--lv0-ring:#3a414d;
 --map-sea:#121620;--map-land:#21252d;--map-kr:#f3f4f6}
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html,body{height:100%}
body{background:var(--bg);color:var(--tx);font-family:-apple-system,'Apple SD Gothic Neo','Malgun Gothic',sans-serif;font-size:var(--fs-base);line-height:1.45;letter-spacing:-.01em;overflow:hidden}
/* 단추·입력은 글꼴을 물려받음(Plex) · 브라우저 기본 모양 지움 — 모양은 클래스마다 */
button,input,select,textarea{font:inherit;color:inherit;letter-spacing:inherit}
/* 글꼴 IBM Plex Sans KR: 첫 화면을 그린 뒤 필요한 조각을 받아 html.wf로 한 번에 적용(webFont) — 받기 전·못 받으면 시스템 글꼴 그대로 */
.wf body{font-family:'IBM Plex Sans KR',-apple-system,'Apple SD Gothic Neo','Malgun Gothic',sans-serif}
.wf-pre{position:absolute;left:-9999px;top:0;visibility:hidden;white-space:nowrap;font-family:'IBM Plex Sans KR';font-size:16px}
button{margin:0;padding:0;border:0;background:none;-webkit-appearance:none;appearance:none;cursor:pointer}
b,strong{font-weight:700}   /* 굵기는 400·600·700만(<b>의 'bolder'가 600 안에서 900이 되지 않게) */
[hidden]{display:none!important}
.sr{position:absolute;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}
:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.ic{display:inline-block;flex:none;fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round;vertical-align:-.2em}
.ic.s2{stroke-width:2}
.nw{white-space:nowrap}   /* '6.3% 쌈'처럼 끝의 짧은 말이 혼자 다음 줄로 가지 않게 */
.app{display:flex;flex-direction:column;height:100vh;height:100dvh}
.content{flex:1;overflow-y:auto;overflow-x:hidden;-webkit-overflow-scrolling:touch;scroll-padding-bottom:8px}   /* 아래 끝 초점 테두리가 잘리지 않게(위는 phSync가 머리 높이로) */
/* 좌우 여백 = max(16px, 안전 영역 — 아이폰 가로) */
:root{--gl:max(16px,env(safe-area-inset-left,0px));--gr:max(16px,env(safe-area-inset-right,0px))}
/* 하단 탭 4개 = 선 아이콘(24px) + 13px 이름 */
.tabs{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));flex:none;border-top:1px solid var(--line);background:var(--card);
padding:2px max(4px,env(safe-area-inset-right,0px)) calc(4px + env(safe-area-inset-bottom,0px)) max(4px,env(safe-area-inset-left,0px))}
.tab{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;min-height:56px;color:var(--sub);font-size:13px;line-height:1.2}
.tab.on{color:var(--accent);font-weight:700}
@media(min-width:760px){.tabs{grid-template-columns:repeat(4,120px);justify-content:center}}
.tab:focus-visible,.mk-chip:focus-visible{outline-offset:-2px}
/* 틀: 칸(.pane) 옆 16px · 탭마다 고정 머리(.phead) · 시장 칩 줄(밑줄 탭, 44px, 위에 고정) */
.pane{display:none;padding:0 var(--gr) 16px var(--gl);min-height:100%}
.pane.on{display:block}
.mk-chips{position:sticky;top:0;z-index:20;display:flex;gap:2px;height:44px;margin:0 calc(-1*var(--gr)) 12px calc(-1*var(--gl));padding:0 max(8px,env(safe-area-inset-right,0px)) 0 max(8px,env(safe-area-inset-left,0px));background:var(--bg);box-shadow:inset 0 -1px 0 var(--line);overflow-x:auto;overflow-y:hidden;scrollbar-width:none}
.mk-chips::-webkit-scrollbar{display:none}
.mk-chip{flex:none;height:44px;min-width:44px;padding:0 8px;border-bottom:2px solid transparent;color:var(--sub);font-size:14px;white-space:nowrap}
.mk-chip.on{color:var(--tx);font-weight:700;border-bottom-color:var(--tx)}
.mk{display:none}.mk.on{display:block}
/* 고정 머리·칩 줄 안 단추에 초점이 가도 내용 창이 튀지 않게(scroll-padding이 머리 자신까지 덮음) */
.phead :is(button,a,[tabindex]),.mk-chips .mk-chip{scroll-margin-top:-100vh}
#p-market.det #mkChips{display:none}   /* 기업 상세 = 칩 줄 대신 상세 머리(뒤로 + 회사 이름) */
.boot-err{margin:0 0 10px;font-size:13px;color:var(--bad)}
/* 표 */
table{width:100%;border-collapse:collapse;font-size:var(--fs-sm)}
th{color:var(--sub);font-weight:600;padding:8px 4px;text-align:right;border-bottom:1px solid var(--line)}
th:first-child,td:first-child{text-align:left}
td{padding:9px 4px;text-align:right;border-bottom:1px solid var(--line)}
.pos{color:var(--pos)}.neg{color:var(--neg)}.na{color:var(--sub)}
.stars{color:var(--tx2)}
.nm{font-weight:600;white-space:nowrap}
.ref{font-size:var(--fs-2xs);color:var(--sub);font-weight:400;margin-top:2px}
/* 로고(구글 파비콘 — 흰 받침은 의도) · 못 받으면 이니셜 */
.logo{width:18px;height:18px;border-radius:4px;vertical-align:-4px;margin-right:6px;background:#fff;border:1px solid var(--line);object-fit:contain}
.lg{display:inline-flex;align-items:center;vertical-align:middle;margin-right:6px}
.lg .logo,.lg .logo-lg{margin-right:0;vertical-align:baseline}
.lgfb{display:inline-flex;align-items:center;justify-content:center;width:18px;height:18px;border-radius:4px;background:var(--fill);color:var(--tx);border:1px solid var(--line);font-size:var(--fs-2xs);font-weight:700;font-style:normal;line-height:1}
.lgfb-lg{width:28px;height:28px;border-radius:6px;font-size:var(--fs-base)}
.logo-lg{width:28px;height:28px;border-radius:6px;vertical-align:-8px;margin-right:8px;background:#fff;border:1px solid var(--line);object-fit:contain}
/* 카드 */
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px;margin-bottom:12px}
.card h3{font-size:var(--fs-base);color:var(--sub);margin-bottom:10px;font-weight:600}
.det-head{font-size:var(--fs-xl);font-weight:700;margin-bottom:12px}
.det-head .tk{font-size:var(--fs-sm);color:var(--sub);font-weight:400}
.tag{display:inline-block;font-size:var(--fs-2xs);color:var(--accent);border:1px solid var(--accent);border-radius:6px;padding:0 6px;margin-left:6px;vertical-align:1px;font-weight:400}
.tag2{display:inline-block;font-size:var(--fs-2xs);color:var(--sub);border:1px solid var(--sub);border-radius:6px;padding:0 5px;margin-left:4px;font-weight:400}
/* 카드 머리 오른쪽 '… ›' 이동 단추 — 글자는 작게, 누르는 곳은 44px(줄 높이는 그대로) */
button.go{display:inline-flex;align-items:center;justify-content:center;min-width:44px;min-height:44px;margin:-14px 0 -14px 2px;padding:0 4px;color:var(--accent);font-size:var(--fs-sm);font-weight:600;vertical-align:middle;white-space:nowrap}
/* 바 */
.bar-row{display:flex;align-items:center;margin-bottom:8px;font-size:var(--fs-sm)}
.bar-row .lb{width:72px;color:var(--sub);flex-shrink:0;word-break:keep-all;overflow-wrap:anywhere}   /* v33 잘라 두고 눌러 펼치던 칸 → 처음부터 다 보이게(키보드로 못 누르는 클릭 div 없앰) */
.bar-wrap{flex:1;background:var(--barbg);border-radius:4px;height:22px;position:relative;min-width:60px}
.bar{height:100%;border-radius:4px;background:var(--accent);opacity:.85}
.bar.cb-oth{background:var(--muted);opacity:.6}
.bar-val,.prow .pv{position:absolute;right:3px;white-space:nowrap;color:var(--tx);border-radius:4px;padding:0 4px;background:var(--card);background:color-mix(in srgb,var(--card) 82%,transparent)}
.bar-val{top:2px;line-height:18px;font-size:var(--fs-xs)}
.pair{margin-bottom:14px}
.pair .pname{font-size:var(--fs-sm);font-weight:600;margin-bottom:4px;word-break:keep-all;overflow-wrap:break-word}   /* v33 긴 지역 이름은 줄바꿈(눌러 펼치기 없앰) */
.pair .pname .na{white-space:nowrap}   /* '(전년 19%)'는 한 덩어리로 */
.prow{display:flex;align-items:center;margin-bottom:3px;font-size:var(--fs-xs)}
.prow .yr{width:38px;color:var(--sub);font-size:var(--fs-2xs);flex-shrink:0}
.prow .pw{flex:1;background:var(--barbg);border-radius:4px;height:18px;position:relative;min-width:50px}
.prow .pb{height:100%;border-radius:4px}
.pb.now{background:var(--accent);opacity:.9}
.pb.prev{background:var(--accent-prev)}
.prow .pv{top:0;line-height:18px;font-size:var(--fs-2xs)}
.cnline{font-size:var(--fs-xs);color:var(--sub);margin:2px 0 0 38px}
/* 키-값 */
.kv{display:flex;justify-content:space-between;gap:8px;padding:6px 0;border-bottom:1px solid var(--line);font-size:var(--fs-base)}
.kv:last-child{border-bottom:none}
.kv .k{color:var(--sub)}
.note{color:var(--sub);font-size:var(--fs-xs);margin-top:10px;line-height:1.6}
.note,.src-desc,.sl-row .t2,.calday,.fplain,.fuse ul,.frules,.cb-read,.sh-row .t1,.sh-row .t3,.sh-fx .t1,.sh-fx .t3,.sh-warn,.fi-warn,.nv-sum,.nv-sub,.ksig .ks,.krmeta,.mini div,.mn-b,.sh-mt p,
.nitem .nsum,.nitem .nmeta,.hd-sub2,.card h3,.td-foot,.ref,div.na,.fi-def dd,.fleg span,.fxmeta span{word-break:keep-all;overflow-wrap:break-word}   /* 한국어는 낱말 단위로 줄바꿈(한 글자 줄 방지) — 표 칸에는 걸지 않음(넘침) */
.src{color:var(--sub);font-size:var(--fs-2xs);margin-top:8px;overflow-wrap:anywhere}   /* 긴 주소만 아무 데서나 끊고 낱말('FY25')은 띄어쓰기에서(옛 break-all은 'FY2|5') */
/* 한국 시장 신호 · 수집 상태 */
.ksig{padding:8px 0;border-bottom:1px solid var(--line)}
.ksig:last-of-type{border-bottom:none}
.ksig .kh{display:flex;justify-content:space-between;align-items:center;font-size:var(--fs-xs);color:var(--sub)}
.ksig .kb{display:flex;justify-content:space-between;align-items:baseline;gap:8px;margin-top:3px;font-size:var(--fs-base)}
.ksig .kb .d{min-width:0;word-break:keep-all;overflow-wrap:anywhere}
.ksig .kb .v{flex:none;white-space:nowrap;font-weight:600}
.ksig .ks{font-size:var(--fs-xs);color:var(--sub);margin-top:2px}
#statusTbl td,#statusTbl th,#claudeTbl td,#claudeTbl th{white-space:nowrap;padding:7px 4px}
#statusTbl td:first-child,#claudeTbl td:first-child{white-space:normal;word-break:keep-all;overflow-wrap:break-word}   /* break-word: 'update-dashboard'가 'dashboa·rd'로 끊기지 않게(anywhere는 첫 칸을 너무 좁힘) */
.cl-tot{font-size:var(--fs-lg);margin:2px 0 8px}.cl-tot b{font-size:var(--fs-xl)}
.st-ok{color:var(--accent);font-weight:600;white-space:nowrap}
.st-late{display:inline-block;padding:0 7px;border-radius:999px;background:var(--warn-bg);color:var(--warn-fg);font-weight:700;white-space:nowrap}
/* 소싱 기회 지도 */
.src-wrap{display:grid;gap:10px;grid-template-columns:minmax(0,1fr);grid-template-areas:"seg" "map" "regs" "btns"}
.src-seg{grid-area:seg}.src-mapbox{grid-area:map}.src-regs{grid-area:regs}.src-btns{grid-area:btns}
.seg2{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:6px}
.seg2 button{min-height:44px;border-radius:10px;border:1px solid var(--line);background:var(--card);color:var(--tx);font-size:var(--fs-sm);font-weight:600}
.seg2 button.on{background:var(--accent-fill);border-color:var(--accent-fill);color:var(--on-accent)}
.src-desc{font-size:var(--fs-xs);color:var(--sub);margin-top:6px;line-height:1.5}
.src-map{position:relative}
.src-svg{width:100%;height:auto;display:block;border-radius:10px;cursor:pointer}
.mp-sea{fill:var(--map-sea)}.mp-other{fill:var(--map-land);stroke:var(--card);stroke-width:.25}
.mp-reg{stroke:var(--card);stroke-width:.25}
.mp-click{transition:opacity .12s}.mp-click:hover{opacity:.78}
.mp-flow{fill:none;stroke:var(--map-kr);stroke-width:.7;stroke-dasharray:2 1.4}
.mp-kr{fill:var(--map-kr);stroke:var(--map-kr);stroke-width:.8}
.src-cl{position:absolute;transform:translate(-50%,-50%);display:flex;flex-direction:column;align-items:center;gap:3px;padding:4px;min-width:44px;min-height:44px}
.src-cl .bs{display:flex;align-items:center}
.src-bd{width:26px;height:26px;border-radius:13px;background:#fff;border:2px solid;display:inline-flex;align-items:center;justify-content:center;overflow:hidden;box-sizing:border-box;flex:none}
.src-bd+.src-bd{margin-left:-7px}
.src-bd img{width:16px;height:16px;object-fit:contain}
.src-bd i{font-style:normal;font-size:var(--fs-2xs);font-weight:700;color:#111}
.src-bd.lg{width:34px;height:34px;border-radius:17px}.src-bd.lg img{width:20px;height:20px}
@media(max-width:480px){.src-cl .src-bd{width:22px;height:22px;border-radius:11px}.src-cl .src-bd img{width:14px;height:14px}.src-cl .src-bd+.src-bd{margin-left:-6px}.src-cl .src-more{min-width:20px;height:20px}}
.src-more{margin-left:-6px;min-width:24px;height:24px;padding:0 5px;border-radius:12px;background:var(--tx);color:var(--bg);font-size:var(--fs-2xs);font-weight:700;display:inline-flex;align-items:center;justify-content:center;box-sizing:border-box}
.src-pill{font-size:var(--fs-xs);font-weight:700;background:var(--card);border:1px solid var(--line);border-radius:999px;padding:0 8px;color:var(--tx);white-space:nowrap}
.src-legend{display:flex;flex-wrap:wrap;gap:4px 10px;font-size:var(--fs-xs);color:var(--sub);margin-top:6px}
.src-legend span{display:inline-flex;align-items:center;gap:4px}
.src-legend i{width:11px;height:11px;border-radius:3px;display:inline-block;box-sizing:border-box}
.src-regs{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:6px}
.src-regs button{min-height:52px;border-radius:12px;border:1px solid var(--line);background:var(--card);color:var(--tx);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3px;padding:6px 2px}
.src-regs b{font-size:var(--fs-base)}
.src-regs .rl{display:flex;flex-direction:column;align-items:center;gap:2px;min-width:0}
.src-regs .tops{display:none;font-size:var(--fs-xs);color:var(--sub);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:100%}
.lvchip{font-size:var(--fs-xs);font-weight:700;padding:0 8px;border-radius:999px;white-space:nowrap}
.src-regs .lvw{display:flex;flex-direction:column;align-items:center;gap:1px}
.src-regs .hin{font-size:var(--fs-2xs);color:var(--sub);white-space:nowrap}
.src-btns{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:6px}
.src-btns button{min-height:44px;border-radius:12px;border:1px solid var(--line);background:var(--card);color:var(--accent);font-size:var(--fs-sm);font-weight:600;padding:4px}
/* PC: 지도 왼쪽 · 오른쪽 열이 지도 높이를 채움(빈 공간 없음) — 기본 규칙 뒤에 둬야 적용됨 */
@media(min-width:760px){.src-wrap{grid-template-columns:minmax(0,1.2fr) minmax(0,1fr);grid-template-rows:auto 1fr auto;grid-template-areas:"map seg" "map regs" "map btns";align-items:stretch}
  .src-regs{grid-template-columns:minmax(0,1fr);grid-auto-rows:1fr}
  .src-regs button{flex-direction:row;justify-content:space-between;padding:0 14px}
  .src-regs .rl{align-items:flex-start}.src-regs .tops{display:block}}
/* 하단 패널 */
.sheet{position:fixed;top:0;right:0;bottom:0;left:0;z-index:60;display:none}
.sheet.on{display:block}
.sh-bd{position:absolute;top:0;right:0;bottom:0;left:0;width:100%;height:100%;background:rgba(10,14,22,.45)}
.sh-pn{position:absolute;left:0;right:0;bottom:0;max-width:760px;margin:0 auto;max-height:80vh;max-height:80dvh;overflow-y:auto;scroll-padding-block:8px;background:var(--card);border-radius:16px 16px 0 0;padding:8px max(14px,env(safe-area-inset-right,0px)) calc(18px + env(safe-area-inset-bottom,0px)) max(14px,env(safe-area-inset-left,0px))}
.sh-grip{width:36px;height:4px;border-radius:2px;background:var(--line);margin:2px auto 8px}
.sh-hd{display:flex;justify-content:space-between;align-items:center;gap:8px}
.sh-tt{display:flex;align-items:center;flex-wrap:wrap;gap:4px 8px;font-size:var(--fs-lg);font-weight:700;min-width:0}
.sh-x{width:44px;height:44px;display:inline-flex;align-items:center;justify-content:center;flex:none;color:var(--sub)}
.sh-warn{font-size:var(--fs-sm);line-height:1.5;background:var(--fill);color:var(--tx);border-left:3px solid var(--warn-bg);border-radius:8px;padding:8px 10px;margin:4px 0}
.sh-row{display:flex;gap:10px;width:100%;padding:10px 0;border-bottom:1px solid var(--line);text-align:left}
.sh-row .bx{flex:1;min-width:0;display:flex;flex-direction:column;gap:2px}
.sh-row .t1{display:flex;justify-content:space-between;align-items:center;gap:8px;font-size:var(--fs-base);font-weight:600}
.sh-row .t2{font-size:var(--fs-base);color:var(--tx)}
.sh-row .t3,.sh-fx .t3{display:block;font-size:var(--fs-xs);color:var(--sub);margin-top:2px}
.sh-sub{font-size:var(--fs-sm);font-weight:700;color:var(--tx);margin:14px 0 2px;display:flex;flex-wrap:wrap;gap:2px 6px;align-items:baseline}
.sh-sub span{font-size:var(--fs-xs);font-weight:400;color:var(--sub)}
.sh-empty{font-size:var(--fs-sm);color:var(--sub);padding:8px 0;border-bottom:1px solid var(--line)}
.sh-fx{display:block;width:100%;padding:9px 0;border-bottom:1px solid var(--line);text-align:left}
.sh-fx .t1{display:flex;justify-content:space-between;align-items:baseline;gap:8px;font-size:var(--fs-base)}
#srcTbl th,#srcTbl td{text-align:center;padding:6px 2px;white-space:nowrap}
#srcTbl th:first-child,#srcTbl td:first-child{text-align:left;white-space:normal;min-width:96px}
#srcTbl td .cv{min-width:54px;border-radius:8px;padding:4px 3px;font-weight:700;font-size:var(--fs-sm);line-height:1.25}
#srcTbl td .cv small{display:block;font-size:var(--fs-2xs);font-weight:400}
.sh-mt p{font-size:var(--fs-base);line-height:1.55;margin:2px 0 10px}.sh-mt b{font-size:var(--fs-base)}
/* 표 줄바꿈 금지 — 표가 넓으면 표만 가로 스크롤 */
.tblwrap{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:0 -4px}
table.nowrap th,table.nowrap td{white-space:nowrap;padding-left:3px;padding-right:3px}
#detBody .card table th,#detBody .card table td{white-space:nowrap}
#krBody .krtbl table th,#krBody .krtbl table td{white-space:nowrap}
.card.flash{outline:2px solid var(--accent);transition:outline .3s}
#sheet .tblwrap:focus-visible{outline-offset:-2px}   /* 패널 '브랜드 × 지역' 표 상자(키보드로 가로 넘김) */
/* 시장 › 실적·재고: KPI 4칸 · 순위 줄 */
.kpis{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:6px;margin-bottom:10px}
.kpi{display:block;width:100%;min-width:0;overflow:hidden;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:10px 4px;text-align:center}
.kpi .l,.kpi .v{display:block;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.kpi .l{font-size:var(--fs-xs);color:var(--sub)}
.kpi .v{font-size:var(--fs-lg);font-weight:700;margin:2px 0}
.kpi .s{font-size:var(--fs-2xs);color:var(--sub);line-height:1.3;display:-webkit-box;-webkit-box-orient:vertical;-webkit-line-clamp:2;overflow:hidden;word-break:keep-all;overflow-wrap:anywhere}   /* 휴대폰에서 2줄까지(띄어쓰기에서 줄바꿈) */
@media(max-width:389px){.kpi .s{-webkit-line-clamp:3}}   /* 360·375: 긴 회사 이름 뒤 기간('26.06)까지 */
.kpis.cbk{grid-template-columns:repeat(3,minmax(0,1fr))}
@media(min-width:480px){.kpi .v{font-size:var(--fs-xl)}}
.hgrid{display:grid;grid-template-columns:minmax(0,1fr);gap:10px}
.hgrid>.card{min-width:0}
@media(min-width:760px){.hgrid{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}.span2{grid-column:1/3}}
.rk{display:flex;justify-content:space-between;align-items:center;gap:8px;width:100%;min-width:0;min-height:44px;padding:6px 0;border-bottom:1px solid var(--line);font-size:var(--fs-base);text-align:left}
.rk>span:first-child{min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.rk>span:last-child,.rk>b{flex:none;white-space:nowrap}
.rk:last-child{border-bottom:none}
/* 순위 줄: 윗줄 법인명 · 아랫줄 브랜드·그룹·기준 */
.rk-n{display:flex;align-items:center;min-width:0}
.rk-t{display:flex;flex-direction:column;min-width:0;line-height:1.3}
.rk-t>span{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.rk-s{font-size:var(--fs-2xs);color:var(--sub)}
#warnCard .rk-s{white-space:normal}
.rk-v2{display:flex;flex-direction:column;align-items:flex-end;line-height:1.35}
.rk-v2 small{font-size:var(--fs-2xs);color:var(--sub)}
.wm-tog{display:flex;align-items:center;gap:4px;min-height:44px;margin-top:2px;color:var(--accent);font-size:var(--fs-sm);font-weight:600}
.cal-dot{display:inline-block;width:8px;height:8px;border-radius:50%;border:1.5px solid var(--muted);margin-right:5px;vertical-align:1px}
.cal-dot.on{background:var(--accent);border-color:var(--accent)}
/* 본사 발언 */
.mn-row{display:flex;gap:8px;align-items:flex-start;padding:7px 0;border-top:1px solid var(--line)}.mn-row:first-of-type{border-top:0}
.mn-t{flex:none;font-size:var(--fs-2xs);font-weight:600;border-radius:6px;padding:0 6px;background:var(--fill);color:var(--sub)}
.mn-inventory{color:var(--bad)}.mn-discount{color:var(--accent)}
.mn-b{min-width:0;font-size:var(--fs-sm);line-height:1.45}
.mn-b summary{display:inline-flex;align-items:center;min-height:44px;min-width:44px;font-size:var(--fs-2xs);color:var(--accent);cursor:pointer}
.mn-b q{display:block;font-size:var(--fs-2xs);color:var(--sub);margin:0 0 6px;overflow-wrap:anywhere}
.mn-s{display:inline-block;font-size:var(--fs-2xs);font-weight:600;border-radius:6px;padding:0 5px;margin-left:4px;vertical-align:1px;white-space:nowrap}
.mn-more{color:var(--accent);border:1px solid var(--accent)}.mn-less{color:var(--bad);border:1px solid var(--bad)}
/* 이전 값 · 새 실적 반영 대기 */
.wait-b,.stl{display:inline-block;font-size:var(--fs-2xs);font-weight:600;border-radius:6px;padding:0 4px;margin-left:4px;white-space:nowrap;line-height:1.45;vertical-align:1px;color:var(--bad);border:1px solid var(--bad)}   /* 새 화면 꼬리표(.tg)와 같은 색·굵기 */
/* 시장 › 기업 */
.search{width:100%;min-height:44px;padding:9px 12px;border:1px solid var(--line);border-radius:10px;font-size:16px;margin-bottom:8px;background:var(--card);color:var(--tx);-webkit-appearance:none;appearance:none}   /* 16px = 휴대폰에서 눌러도 확대되지 않음 */
.search::placeholder{color:var(--sub);opacity:1}   /* 안내 글 대비 4.5 이상(기본 회색은 다크에서 3.8) */
#coTbl th{white-space:nowrap;font-size:var(--fs-2xs);padding:7px 3px}
#coTbl td{white-space:nowrap;padding:12px 3px}
#coTbl tr.cx td{white-space:normal;overflow-wrap:anywhere;max-width:0}
@media(max-width:480px){#coTbl th:nth-child(4),#coTbl tr.co td:nth-child(4){display:none}#coTbl .mini{grid-template-columns:1fr}}   /* 휴대폰: 총이익률은 펼친 줄에(13px에서 표가 넘치지 않게) */
.mini{display:grid;grid-template-columns:1fr 1fr;gap:6px 14px;font-size:var(--fs-sm)}
.mini div{white-space:normal;overflow-wrap:anywhere}
.mini b{font-weight:600}
tr.co>td,tr[onclick]>td{height:44px}   /* 누르는 줄은 44px 이상 */
tr[tabindex]:focus-visible{outline-offset:-2px}   /* 표 줄 초점 테두리는 안쪽에(가로 스크롤 상자에 잘리지 않게) */
tr.co{cursor:pointer}tr.co td:first-child{font-weight:600;max-width:150px;overflow:hidden;text-overflow:ellipsis}
tr.co td:first-child .lg{vertical-align:-4px}
.nm-sub{display:block;font-size:var(--fs-2xs);color:var(--sub);font-weight:400;margin-left:24px;white-space:normal;line-height:1.5}
.nm-sub .wait-b,.nm-sub .stl{margin-left:0}
@media(max-width:400px){tr.co td:first-child{max-width:132px;white-space:normal;word-break:keep-all;overflow-wrap:anywhere}}   /* 긴 이름은 줄바꿈 */
@media(max-width:374px){#coTbl th,#coTbl td{padding-left:2px;padding-right:2px}}   /* 360폭: 칸 좌우 여백 3→2px로 표가 폭 안에(마지막 열 '재고 증감'이 3px 잘리던 것 · 이름 칸·'새 실적 반영 대기' 배지는 그대로) */
@media(max-width:374px){#coPlat th,#coPlat td{padding-left:2px;padding-right:2px}#coPlat th{white-space:normal;word-break:keep-all}#coPlat td:first-child{min-width:80px;overflow-wrap:break-word}}   /* 360폭 플랫폼 표: 머리글 두 줄 → 이름 칸 80px */
tr.cx td{background:var(--barbg);padding:10px 8px;text-align:left}
.co-more{display:flex;align-items:center;min-height:44px;margin:2px 0 -6px;color:var(--accent);font-weight:600}
/* 시장 › 캘린더 */
.cal{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:10px 6px}
.cal h3{font-size:var(--fs-base);color:var(--sub);font-weight:600;margin:0 4px 6px}
.cgrid{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:2px 0}
.cgrid .wd{font-size:var(--fs-2xs);color:var(--sub);text-align:center;padding:2px 0}
.cd{min-height:48px;min-width:0;overflow:hidden;border-radius:6px;padding:3px;font-size:var(--fs-2xs);border:1px solid transparent}
.cd .dn{color:var(--sub);text-align:right}
.cd.has{background:var(--barbg);cursor:pointer}
.cd.sale{background:var(--accent-weak);cursor:pointer}
.cd.today{border:2px solid var(--accent);padding:2px}
.cd.today .dn{color:var(--accent);font-weight:700}
.cd .ev{line-height:1.25;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;color:var(--tx)}
.cd .ev.sl{color:var(--accent);font-weight:700}
.cd.sel{outline:2px solid var(--accent);outline-offset:-2px}
.calday{font-size:var(--fs-sm);margin:8px 4px 0;color:var(--sub)}
.cl{display:flex;justify-content:space-between;align-items:center;gap:8px;width:100%;min-height:44px;padding:6px 0;border-bottom:1px solid var(--line);font-size:var(--fs-base);text-align:left}
.cl:last-child{border-bottom:none}
.cl>span:first-child{min-width:0}
.sl-row{padding:8px 0;border-bottom:1px solid var(--line)}
.sl-row:last-child{border-bottom:0}
.sl-row .t1{display:flex;justify-content:space-between;gap:8px;font-size:var(--fs-base)}
.sl-row .t1>span:first-child{min-width:0}.sl-row .t1>span:last-child{flex:none;white-space:nowrap}
.sl-row .t2{font-size:var(--fs-xs);color:var(--sub);margin-top:2px}
.sl-k{font-size:var(--fs-2xs);border:1px solid var(--line);border-radius:6px;padding:0 4px;margin-left:4px;color:var(--sub);font-weight:400;white-space:nowrap}
.sl-live{color:var(--accent);font-weight:700}
.sv-tbl td:first-child{white-space:normal;min-width:96px;max-width:132px;word-break:keep-all;overflow-wrap:break-word}   /* 회사 이름은 낱말 단위('하이라이트브랜즈'의 '즈'가 혼자 줄에 가지 않게 — 표는 원래 가로 스크롤) */
.sv-tbl td:first-child .pg-rk{display:block;margin-left:0}
/* 알약 칩(뉴스·기업 그룹·지표) — 한 줄 가로 넘김 */
.chips{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:12px}
.chip{display:inline-flex;align-items:center;min-height:44px;padding:0 12px;border-radius:999px;border:1px solid var(--line);background:var(--card);color:var(--sub);font-size:var(--fs-sm);white-space:nowrap}
.chip.on{background:var(--accent-fill);border-color:var(--accent-fill);color:var(--on-accent)}
.chip.sep{border:0;background:transparent;padding:0 2px;cursor:default}
#newsChips,#coChips{flex-wrap:nowrap;overflow-x:auto;-webkit-overflow-scrolling:touch;scrollbar-width:none;padding:4px;margin:-4px -4px 10px;scroll-padding-inline:8px}   /* 가로 스크롤 상자 — 안쪽 4px(바깥은 같은 만큼 당김)이라 키보드 초점 테두리(칩 바깥 4px)가 위·아래·맨 앞에서 잘리지 않음 · Tab으로 간 칩은 상자 안으로 스크롤(chipRowFocus) */
#newsChips::-webkit-scrollbar,#coChips::-webkit-scrollbar{display:none}
/* 뉴스 */
.ndate{font-size:var(--fs-sm);color:var(--sub);margin:14px 0 6px;font-weight:600}
.nmore{display:flex;align-items:center;gap:4px;width:100%;min-height:44px;margin:0 0 4px;color:var(--accent);font-size:var(--fs-sm);text-align:left}
.hc-leg{display:flex;gap:12px;font-size:var(--fs-xs);color:var(--sub);margin:-4px 0 4px}
.hc-leg i{display:inline-block;width:14px;height:3px;border-radius:2px;vertical-align:3px;margin-right:4px}
.hc-svg{display:block;width:100%;height:auto}
/* 뉴스 한 건: 제목 링크가 한 줄(18px)이어도 기사 칸 전체(44px 이상)를 누르면 열림 — 링크의 ::after를 칸 위에 펼침 */
.nitem{position:relative;padding:10px 0;border-bottom:1px solid var(--line)}
.nitem:last-child{border-bottom:none}
.nitem .nsum{font-size:var(--fs-base);line-height:1.5}
.nitem .nsum a{color:var(--tx);text-decoration:none}
.nitem .nsum a::after{content:'';position:absolute;inset:0}
.nitem .nmeta{font-size:var(--fs-xs);color:var(--sub);margin-top:3px}
.ntag{display:inline-block;font-size:var(--fs-2xs);color:var(--accent);border:1px solid var(--accent);border-radius:6px;padding:0 5px;margin-right:5px}
/* v33.1 지난 뉴스 검색 — 찾은 낱말 강조 · 요약에 없는 낱말로 찾았으면 원문 제목 한 줄 · 결과 머리 줄 */
#newsBody mark{background:var(--accent-weak);color:inherit;font-weight:600;border-radius:3px;padding:0 1px}
.nitem .ntitle{font-size:var(--fs-xs);color:var(--sub);margin-top:3px;word-break:keep-all;overflow-wrap:break-word}
.ns-st{display:flex;flex-wrap:wrap;align-items:center;gap:4px 8px;margin:0 0 6px}
a.nmore{text-decoration:none}
/* 시장 › 국내: KOSIS·추이 카드 */
.krcard{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 14px;margin-bottom:10px;cursor:pointer}
.krhead{display:flex;align-items:baseline;gap:8px}
.krname{font-size:var(--fs-base);font-weight:600}
.krval{margin-left:auto;font-size:var(--fs-lg);font-weight:700;white-space:nowrap}
.kryoy{font-size:var(--fs-sm);font-weight:600}
.krmeta{font-size:var(--fs-xs);color:var(--sub);margin-top:2px}
.krtbl{display:none;margin-top:10px}
.krtbl.open{display:block}
.trend .krname{font-weight:400}
.trend .krval{font-size:var(--fs-base)}
/* 판매 vs 검색 교차 그래프 · 네이버 검색 관심도 */
.xc-legend{display:flex;flex-wrap:wrap;gap:6px;margin:8px 0}
.xc-leg{display:inline-flex;align-items:center;gap:6px;min-height:44px;border:1px solid var(--line);border-radius:999px;padding:0 12px;font-size:var(--fs-sm);background:var(--card);color:var(--tx)}
.xc-leg i{width:14px;height:3px;border-radius:2px;display:inline-block}
.xc-leg.off{color:var(--sub);text-decoration:line-through}.xc-leg.off i{opacity:.3}
.xc-wrap{position:relative}
@media(min-width:760px){.xc-wrap{max-width:560px}}
.xc-svg{width:100%;height:auto;display:block;touch-action:pan-y}
.xc-tip{position:absolute;top:2px;pointer-events:none;background:var(--card);color:var(--tx);border:1px solid var(--line);border-radius:8px;padding:6px 8px;font-size:var(--fs-xs);line-height:1.55;white-space:nowrap;font-variant-numeric:tabular-nums}
.nv-sum{background:var(--barbg);border-radius:10px;padding:10px 12px;font-size:var(--fs-sm);line-height:1.6;margin-bottom:8px}
.nv-row{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:3px 10px;padding:9px 0;border-top:1px solid var(--line);cursor:pointer}
.nv-nm{display:flex;align-items:center;gap:6px;min-width:0;font-weight:700;font-size:var(--fs-base)}
.nv-nm span{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.nv-low{font-style:normal;font-size:var(--fs-2xs);color:var(--sub);border:1px solid var(--line);border-radius:6px;padding:0 5px;font-weight:400;flex:none}
.nv-pill{justify-self:end;align-self:center;border-radius:999px;padding:1px 9px;font-size:var(--fs-sm);font-weight:700;font-variant-numeric:tabular-nums;white-space:nowrap}
.nv-pill.up{background:var(--accent-fill);color:var(--on-accent)}.nv-pill.down{background:var(--warn-bg);color:var(--warn-fg)}.nv-pill.mid{background:var(--fill);color:var(--tx)}
.nv-bar{display:flex;align-items:center;gap:8px;min-width:0}
.nv-bar .tr{flex:1;height:6px;background:var(--barbg);border-radius:3px;overflow:hidden}
.nv-bar .tr i{display:block;height:100%;background:var(--sub);opacity:.55}
.nv-bar b{font-size:var(--fs-sm);min-width:34px;text-align:right;font-variant-numeric:tabular-nums}
.nv-sub{grid-column:1/-1;font-size:var(--fs-xs);color:var(--sub)}
.nv-more{width:100%;margin-top:8px;min-height:44px;border-radius:10px;border:1px solid var(--line);background:var(--card);color:var(--accent);font-weight:700;font-size:var(--fs-sm);display:flex;align-items:center;justify-content:center;gap:4px}
.nv-det+.nv-det{margin-top:12px;padding-top:12px;border-top:1px solid var(--line)}
/* 유통사·패션 재무 지표 */
.fi-top{display:flex;align-items:baseline;gap:6px;flex-wrap:wrap}
.fi-big{font-size:var(--fs-lg)}
.fi-gsum{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:4px;margin-top:8px}
.fi-gsum button{border:1px solid var(--line);background:var(--card);border-radius:8px;padding:5px 1px;color:var(--tx);min-width:0;min-height:44px}
.fi-gsum button.on{border-color:var(--accent);box-shadow:inset 0 0 0 1px var(--accent)}
.fi-gsum .l{display:block;font-size:var(--fs-2xs);line-height:1.3;color:var(--sub);word-break:keep-all;overflow-wrap:anywhere}   /* 좁으면 '손익·' / '성장' 두 줄(말줄임 대신) */
.fi-gsum .v{display:block;font-size:var(--fs-sm);font-weight:700}
.fi-dots{display:flex;justify-content:center;gap:2px;margin-top:2px}
.fi-dots i{width:6px;height:6px;border-radius:50%;background:var(--line)}
.fi-dots i.b{background:var(--accent)}
.fi-dots i.x{background:transparent;border:1px solid var(--line)}
.fi-seg{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:4px;background:var(--barbg);border-radius:10px;padding:3px}
.fi-seg button{min-height:44px;border-radius:8px;color:var(--sub);font-size:var(--fs-sm);font-weight:600;padding:0 2px;white-space:nowrap}
.fi-seg button.on{background:var(--card);color:var(--tx);box-shadow:0 1px 2px rgba(0,0,0,.08)}
.fi-chips{margin:8px 0 0}
.fi-mhead{display:flex;align-items:baseline;gap:6px;flex-wrap:wrap;margin:10px 0 6px;font-size:var(--fs-xs)}
.fi-mhead b{font-size:var(--fs-base)}
.fi-mbox{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:6px;margin-bottom:8px}
.fi-mbox div{background:var(--barbg);border-radius:8px;padding:6px 8px;min-width:0}
.fi-mbox .l{display:block;font-size:var(--fs-2xs);color:var(--sub);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.fi-mbox .v{display:block;font-size:var(--fs-base);font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.fi-mbox .s{display:block;font-size:var(--fs-2xs);color:var(--sub);white-space:nowrap}
.fi-tbl td{vertical-align:top;font-variant-numeric:tabular-nums;padding:7px 3px}
.fi-tbl td:first-child{max-width:124px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
@media(min-width:356px){.fi-tbl td:not(:first-child){white-space:nowrap}}   /* '2,026억원'의 '원'이 혼자 다음 줄로 가지 않게(355px 이하는 줄바꿈 — 최근 연도 칸이 가로 스크롤 뒤로 숨지 않게) */
@media(max-width:389px){.fi-tbl td:first-child{max-width:108px}}@media(max-width:372px){.fi-tbl td:first-child{max-width:92px}}   /* 375·360: 이름 칸을 줄여 3개년 값이 한 줄에 */
.fi-nm{display:inline-block;vertical-align:top;max-width:100px;white-space:normal;text-wrap:balance}   /* 비교 표 법인명: 칸보다 길면 말줄임 대신 두 줄(휴대폰은 title이 안 보임) */
@media(max-width:389px){.fi-nm{max-width:84px}}@media(max-width:372px){.fi-nm{max-width:68px}}
.fi-tbl tr.me td{background:var(--barbg)}
.std-b{display:inline-block;font-size:var(--fs-2xs);line-height:1.45;border-radius:4px;padding:0 4px;margin-left:4px;border:1px solid var(--line);color:var(--sub);font-weight:400;vertical-align:middle}
.std-b.ifrs{color:var(--accent);border-color:var(--accent)}
.fi-tbl td:first-child .fi-nsub{display:block;font-size:var(--fs-2xs);color:var(--sub);font-weight:400;margin:1px 0 0 24px;line-height:1.4}
.fi-nsub .std-b{margin-left:0}.fi-nsub .std-b:not(:first-child){margin-left:4px}
.fi-warn{font-size:var(--fs-xs);color:var(--sub);background:var(--barbg);border-radius:8px;padding:8px 10px;margin:6px 0 8px;line-height:1.5}
.fi-warn .chip{margin-top:6px}
.fi-tbl tr.me td:first-child{font-weight:700}
.fi-tbl tr.fi-med td{color:var(--sub);border-bottom:none}
.fi-tbl tr.fi-gh td{background:var(--barbg);font-size:var(--fs-xs);color:var(--sub);font-weight:700;padding:4px 6px}
.fi-sub{display:block;font-size:var(--fs-2xs);color:var(--sub);font-weight:400}
.fi-b{display:block;margin-top:2px}
.fi-def{border:1px solid var(--line);border-radius:10px;padding:8px 10px;margin-top:12px;font-size:var(--fs-xs);line-height:1.6}
.fi-def dl{display:grid;grid-template-columns:60px minmax(0,1fr);gap:2px 8px;margin:0}
.fi-def dt{color:var(--sub)}
.fi-def dd{margin:0}
/* 비교 카드 순위 배지·막대 */
.pg-badge{display:inline-block;padding:0 6px;border-radius:999px;background:var(--accent-fill);color:var(--on-accent);font-size:var(--fs-2xs);font-weight:700;line-height:1.5;margin:1px 2px 1px 0}
.pg-rk{display:block;font-size:var(--fs-2xs);color:var(--sub)}
.pg-bars{display:flex;flex-direction:column;gap:2px}
.pg-row{display:grid;grid-template-columns:96px minmax(0,1fr) minmax(56px,auto);align-items:center;gap:8px;min-height:44px;cursor:pointer;font-size:var(--fs-sm)}
.pg-nm{overflow:hidden;color:var(--sub);line-height:1.25;display:-webkit-box;-webkit-box-orient:vertical;-webkit-line-clamp:2;overflow-wrap:anywhere}   /* 긴 이름은 2줄 */
.pg-row.me .pg-nm{color:var(--tx);font-weight:700}
.pg-tr{position:relative;height:14px}
.pg-bar{position:absolute;top:2px;height:10px;background:var(--sub);opacity:.4;border-radius:0 4px 4px 0}
.pg-bar.neg{border-radius:4px 0 0 4px}
.pg-row.me .pg-bar{background:var(--accent);opacity:1}
.pg-zero{position:absolute;top:-3px;bottom:-3px;width:1px;background:var(--line)}
.pg-med{position:absolute;top:-4px;bottom:-4px;border-left:1.5px dashed var(--sub)}
.pg-v{text-align:right;font-variant-numeric:tabular-nums;color:var(--tx)}
.pg-row.me .pg-v{font-weight:700}
.pg-tip{min-height:20px;font-size:var(--fs-xs);color:var(--sub);margin-top:8px}
/* 더보기 — 환율 · 해외직구 */
.mbadge{display:inline-block;font-size:var(--fs-2xs);font-weight:700;border-radius:999px;padding:0 7px;line-height:1.7;color:var(--on-accent);background:var(--accent-fill)}
.mbadge.up,.mbadge.late{background:var(--warn-bg);color:var(--warn-fg)}
.fxgrid{display:grid;grid-template-columns:minmax(0,1fr);gap:10px;margin-bottom:10px}
@media(min-width:760px){.fxgrid{grid-template-columns:repeat(3,minmax(0,1fr))}}
.fxc{border:1px solid var(--line);border-radius:12px;padding:12px;background:var(--card);min-width:0}
.fxc.dn{border-color:var(--accent)}.fxc.up{border-color:var(--warn-bg)}
.fxtop{display:flex;align-items:center;flex-wrap:wrap;gap:4px 6px;font-size:var(--fs-sm)}
.fpill{margin-left:auto;font-size:var(--fs-2xs);font-weight:700;border-radius:999px;padding:0 8px;line-height:1.7;white-space:nowrap}
.fpill.dn{background:var(--accent-fill);color:var(--on-accent)}.fpill.up{background:var(--warn-bg);color:var(--warn-fg)}
.fpill.wait{border:1px solid var(--line);color:var(--sub);font-weight:400}
.fxv{font-size:var(--fs-lg);font-weight:700;margin-top:2px}
.fxv small{font-size:var(--fs-xs);font-weight:400;color:var(--sub);margin-left:4px}
.fxmeta{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:4px;margin-top:6px;font-size:var(--fs-sm)}
.fxmeta span{display:block;color:var(--sub);font-size:var(--fs-2xs)}
.fgauge{position:relative;height:40px;margin-top:8px}
.fg-trk{position:absolute;left:0;right:0;top:9px;height:6px;background:var(--barbg);border-radius:3px}
.fg-tk{position:absolute;top:7px;width:1px;height:10px;background:var(--line)}
.fg-tk.z{background:var(--sub);top:4px;height:16px}
.fg-seen{position:absolute;top:9px;height:6px;background:var(--accent);opacity:.3;border-radius:3px}
.fg-me{position:absolute;top:4px;width:10px;height:16px;margin-left:-5px;border-radius:3px;background:var(--tx)}
.fg-lb{position:absolute;top:20px;font-size:var(--fs-2xs);color:var(--sub);transform:translateX(-50%);white-space:nowrap}
.fg-lb.l0{transform:none}.fg-lb.l1{transform:translateX(-100%)}   /* 처음·끝 라벨은 안쪽으로(카드 밖으로 나가지 않게) */
.fxsv{display:block;width:100%;height:52px;margin-top:6px}
.fxcnt{font-size:var(--fs-2xs);color:var(--sub);margin-top:4px}
.fleg{display:flex;gap:4px 10px;flex-wrap:wrap;font-size:var(--fs-2xs);color:var(--sub);margin:0 0 10px}
.fleg i{display:inline-block;width:14px;height:0;border-top:1.5px solid var(--sub);vertical-align:3px;margin-right:4px}
.fleg i.avg{border-top-style:dashed}.fleg i.ldn{border-top-color:var(--pos)}.fleg i.lup{border-top-color:var(--neg)}
.fleg i.dn,.fleg i.up{width:7px;height:7px;border:none;border-radius:50%;vertical-align:0}
.fleg i.dn{background:var(--pos)}.fleg i.up{background:var(--neg)}
.frec>div{display:grid;grid-template-columns:40px 10px minmax(0,1fr);gap:6px;align-items:baseline;font-size:var(--fs-sm);padding:6px 0;border-bottom:1px solid var(--line)}
.frec>div:last-child{border-bottom:none}
.frec .d{color:var(--sub);font-size:var(--fs-xs)}
.frec i{width:8px;height:8px;border-radius:50%;display:inline-block}
.frec i.dn{background:var(--pos)}.frec i.up{background:var(--neg)}
.fplain{display:flex;justify-content:space-between;gap:8px;font-size:var(--fs-sm);padding:7px 0;border-bottom:1px solid var(--line)}
.fplain:last-child{border-bottom:none}
.fplain>span:last-child{text-align:right}
.fuse{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}
.fuse>div{border-radius:10px;padding:8px 10px;background:var(--barbg);min-width:0}
.fuse b{display:block;font-size:var(--fs-sm);margin-bottom:2px}
.fuse ul,.frules{margin:0;padding-left:16px;font-size:var(--fs-xs);display:flex;flex-direction:column;gap:2px}
.cb-row{display:grid;grid-template-columns:62px minmax(0,1fr) 60px;gap:8px;align-items:center;font-size:var(--fs-sm);margin-bottom:8px}
.cb-row .lb{color:var(--sub);white-space:nowrap}
.cb-row .yy{text-align:right;font-size:var(--fs-xs);font-variant-numeric:tabular-nums}
.cb-trend{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}
@media(min-width:760px){.cb-trend{grid-template-columns:repeat(4,minmax(0,1fr))}}
.cb-tr{border:1px solid var(--line);border-radius:10px;padding:6px 8px;min-width:0}
.cb-tr .h{display:flex;justify-content:space-between;flex-wrap:wrap;gap:0 4px;font-size:var(--fs-xs)}
.cb-tr svg{display:block;width:100%;height:36px;margin-top:2px}
.cb-tr .ax{display:flex;flex-wrap:wrap;justify-content:space-between;gap:0 4px;font-size:var(--fs-2xs);color:var(--sub)}.cb-tr .ax span{white-space:nowrap}.cb-tr .ax span:last-child{margin-left:auto}   /* 좁으면 끝 분기는 다음 줄 오른쪽(낱말 중간에서 끊지 않음) */
.cb-read{background:var(--barbg);border-radius:10px;padding:8px 10px;font-size:var(--fs-xs);margin-bottom:10px}
/* v33.4 더보기 — 물류 */
.kpis.lgk{grid-template-columns:repeat(2,minmax(0,1fr))}
@media(min-width:480px){.kpis.lgk{grid-template-columns:repeat(3,minmax(0,1fr))}}
.kpi .v small{font-size:var(--fs-xs);font-weight:400;margin-left:1px}
.lg-tbl td,.lg-tbl th{white-space:nowrap}
.lg-tbl td:first-child,.lg-tbl th:first-child{text-align:left}
.lg-tbl tr.lg-me td:first-child{font-weight:700}
.lg-tr{margin-top:8px}
.cb-trend.lg-tr.k3{grid-template-columns:repeat(3,minmax(0,1fr))}
.lg-sub{font-size:var(--fs-2xs);color:var(--sub);margin-top:1px;word-break:keep-all;overflow-wrap:anywhere}
.lg-share{display:grid;grid-template-columns:auto minmax(0,1fr);gap:4px 12px;align-items:center;background:var(--barbg);border-radius:10px;padding:8px 10px;margin-bottom:8px}
.lg-share>div:first-child{display:flex;flex-direction:column;min-width:0}
.lg-share>div:first-child span{font-size:var(--fs-2xs);color:var(--sub)}
.lg-share>div:first-child .stl{color:var(--bad)}   /* v33.6 위 줄(회색)보다 우선 — '출처 값 확인 필요' 꼬리표는 주황 */
.lg-share b{font-size:var(--fs-xl);line-height:1.2}
.lg-shx{font-size:var(--fs-xs);min-width:0;word-break:keep-all;overflow-wrap:anywhere}
.lg-bars{display:flex;align-items:flex-end;gap:4px;margin:8px 0 2px}
.lg-bars>div{flex:1;min-width:0;display:flex;flex-direction:column;align-items:center;gap:2px}
.lg-bars .bw{display:flex;align-items:flex-end;justify-content:center;width:100%;height:56px}
.lg-bars .b{display:block;width:100%;max-width:22px;background:var(--sub);opacity:.4;border-radius:3px 3px 0 0}
.lg-bars .b.on{background:var(--accent);opacity:1}
.lg-bars .v,.lg-bars .m{font-size:var(--fs-2xs);white-space:nowrap}
.lg-bars .m{color:var(--sub)}
/* v33.5 물류 세 묶음(수입·수출·공통 위험) + 적출 거점 줄 */
.lg-h2{display:flex;align-items:baseline;flex-wrap:wrap;gap:2px 8px;margin:20px 2px 8px;font-size:16px;font-weight:700;line-height:1.3;word-break:keep-all;overflow-wrap:break-word}
.lg-h2 span{font-size:13px;font-weight:400;color:var(--sub)}
.lg-jump{margin:-2px 0 10px}
.lg-jump .chip{gap:2px;color:var(--tx)}
.lh{border-top:1px solid var(--line)}
.lh:first-child{border-top:none}
.lh>summary{display:flex;align-items:center;gap:8px;min-height:52px;padding:6px 0;cursor:pointer;list-style:none}
.lh>summary::-webkit-details-marker{display:none}
.lh>summary:focus-visible{outline-offset:-2px}
.lh-ms{display:flex;align-items:center;justify-content:space-between;gap:8px;min-height:52px;padding:6px 0}
.lh-a{display:flex;flex-direction:column;flex:1 1 auto;min-width:0}
.lh-a .t{font-size:15px;font-weight:600}
.lh-a .s,.lh-b .s{font-size:var(--fs-2xs);color:var(--sub);word-break:keep-all;overflow-wrap:anywhere}
.lh-b{display:flex;flex-direction:column;align-items:flex-end;text-align:right;flex:none}
.lh-b b{font-size:15px}
.lh-b b small,.lg-share b small{font-size:var(--fs-xs);font-weight:400;margin-left:1px}   /* v33.6 단위(TEU·톤·척/일) 13px */
.lh-b .s{white-space:nowrap}
.lg-bu .lg-bux{grid-column:1/-1;font-size:var(--fs-xs);color:var(--sub);word-break:keep-all;overflow-wrap:break-word}
.lh-ic{flex:none;color:var(--tx2);transition:transform .15s}
.lh[open] .lh-ic{transform:rotate(180deg)}
.lh-in{padding:0 0 10px}
.lh-in svg{display:block;width:100%;height:40px}
.lh-in .ax{display:flex;justify-content:space-between;gap:0 4px;font-size:var(--fs-2xs);color:var(--sub)}
.lh-in p{margin:6px 0 0;font-size:var(--fs-xs);line-height:1.5;word-break:keep-all;overflow-wrap:anywhere}
/* v33.6 나라별 물동량 '나라 더 보기' · 부산항 입항 선박(직전 출항지 막대·주별 그래프) */
.lg-more{border-top:1px solid var(--line)}
/* v33.9 '읽는 법' 접기 — 표·그래프 해석 설명(누르는 곳 44px) */
.why{margin-top:4px}
.why>summary{display:inline-flex;align-items:center;gap:4px;min-height:44px;padding:0 2px;cursor:pointer;list-style:none;font-size:var(--fs-xs);color:var(--accent)}
.why>summary::-webkit-details-marker{display:none}
.why-ic{transition:transform .15s}
.why[open] .why-ic{transform:rotate(180deg)}
.why>.note{margin-top:0}
.lg-more>summary{display:flex;align-items:center;gap:8px;min-height:48px;cursor:pointer;list-style:none;font-weight:600}
.lg-more>summary::-webkit-details-marker{display:none}
.lg-more>summary:focus-visible{outline-offset:-2px}
.lg-more>summary>span:first-child{white-space:nowrap}
.lg-more>summary .na{flex:1 1 auto;min-width:0;font-weight:400;font-size:var(--fs-2xs);word-break:keep-all;overflow-wrap:anywhere}
.lg-more[open]>summary .lh-ic{transform:rotate(180deg)}
.lg-grp{margin:10px 0 2px;font-size:var(--fs-2xs);color:var(--sub);word-break:keep-all;overflow-wrap:anywhere}
.lg-more .lh:first-child{border-top:none}
.lg-hb{display:grid;grid-template-columns:minmax(4.5em,auto) minmax(0,1fr) auto;align-items:center;gap:6px 8px;margin:4px 0 8px;font-size:var(--fs-xs)}
.lg-hb>div{display:contents}   /* 한 격자 — 모든 줄의 막대 길이가 같은 기준(숫자 자리 수와 무관) */
.lg-hb .t{word-break:keep-all;overflow-wrap:anywhere}
.lg-hb .bw{display:block;height:8px;background:var(--barbg);border-radius:4px;overflow:hidden;min-width:24px}
.lg-hb .b{display:block;height:100%;background:var(--accent);border-radius:4px}
.lg-hb .num{white-space:nowrap;text-align:right}
.lg-pmtr{margin-top:4px}
.lg-pmtr svg{display:block;width:100%;height:40px}
.lg-pmtr .ax{display:flex;justify-content:space-between;gap:0 4px;font-size:var(--fs-2xs);color:var(--sub)}
/* ── v33 A안 새 화면 부품(탭별 머리·오늘 결정 카드·브랜드 탭·브랜드 상세·더보기 메뉴) ── */
/* 줄·카드 단추(브라우저 기본 가운데 정렬 대신 왼쪽) */
.dc-hd,.dc-row,.dc-more,.dc-ev,.dc-peer,.dc-xmore,.hd-pill,.hd-back,.br-row,.br-rest-row,.br-link,.bd-nx,.bd-link,.bd-hq,.mi,.warnbar{text-align:left}
/* 둥근 상자(overflow:hidden)를 꽉 채운 줄 단추는 초점 테두리를 안쪽에 — 바깥에 그리면 좌우가 잘림 */
.dc-hd:focus-visible,.dc-row:focus-visible,.dc-more:focus-visible,.br-row:focus-visible,.br-rest>summary:focus-visible,.br-rest-row:focus-visible,.mi:focus-visible{outline-offset:-2px}
.dc-row:active,.dc-ev:active,.dc-more:active,.br-row:active,.br-rest-row:active,.bd-nx:active,.mi:active,.tab:active,.rk:active,.cl:active,.sh-row:active{background:var(--fill)}
.phead{position:sticky;top:0;z-index:20;margin:0 calc(-1*var(--gr)) 12px calc(-1*var(--gl));padding:10px var(--gr) 10px var(--gl);background:var(--bg);border-bottom:1px solid var(--line);word-break:keep-all;overflow-wrap:break-word}
.phead h1:focus{outline:none}   /* 화면을 바꾼 뒤 제목에 준 초점(키보드·화면 읽기 — 다음 Tab 출발점)은 테두리 없이 */
.phead h1{margin:0;font-size:var(--fs-page);font-weight:700;line-height:1.3;letter-spacing:-.02em}
.hd-row{display:flex;align-items:center;justify-content:space-between;gap:12px}
.hd-tt{display:flex;flex-direction:column;gap:1px;min-width:0}
.hd-kick,.hd-sub{display:block;font-size:13px;color:var(--sub)}
.hd-pill{display:inline-flex;align-items:center;gap:6px;flex:none;min-height:44px;padding:0 12px;border:1px solid var(--line);border-radius:999px;background:var(--card);font-size:13px;font-weight:600;white-space:nowrap}
.hd-pill .ic{color:var(--accent)}.hd-pill.late .ic{color:var(--bad)}
.phead.dethead{display:grid;grid-template-columns:minmax(44px,1fr) minmax(0,max-content) minmax(44px,1fr);align-items:center;column-gap:4px;min-height:56px;padding:0 max(8px,env(safe-area-inset-right,0px)) 0 max(8px,env(safe-area-inset-left,0px))}
.dethead h1{font-size:var(--fs-name);text-align:center;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;min-width:0;letter-spacing:-.01em}
.hd-back{display:inline-flex;align-items:center;justify-self:start;gap:2px;max-width:100%;min-width:44px;min-height:44px;padding:0 8px 0 2px;font-size:15px;white-space:nowrap}
.hd-back>span{overflow:hidden;text-overflow:ellipsis;min-width:0}
.hd-sub2{margin:-4px 0 12px;font-size:13px;color:var(--sub);line-height:1.5}
.icbtn{width:44px;height:44px;display:inline-flex;align-items:center;justify-content:center;flex:none;border:1px solid var(--line);border-radius:12px;background:var(--card)}
.icbtn[aria-expanded="true"]{background:var(--accent-weak)}
/* 판정 배지 3종 + 판정 안 함 · 새 화면 꼬리표(13px) */
.vb{display:inline-flex;align-items:center;gap:4px;height:26px;padding:0 9px 0 7px;border-radius:999px;font-size:13px;font-weight:700;line-height:1;white-space:nowrap;flex:none}
.vb.go{background:var(--accent-fill);color:var(--on-accent)}
.vb.warn{background:var(--warn-bg);color:var(--warn-fg)}
.vb.wait{background:var(--card);color:var(--hold-fg);border:1.5px solid var(--hold-bd)}
.vb.none{background:var(--card);color:var(--sub);border:1.5px dashed var(--hold-bd)}
.vb.lg{height:30px;padding:0 11px 0 8px;font-size:14px;gap:5px}
.tg{display:inline-block;font-size:13px;font-weight:600;line-height:1.4;border:1px solid var(--bad);color:var(--bad);border-radius:6px;padding:0 5px;white-space:nowrap;vertical-align:1px}
.sc-p{color:var(--accent);font-weight:700}.sc-n{color:var(--bad);font-weight:700}.sc-z{color:var(--tx2);font-weight:600}.sc-na{color:var(--sub);font-weight:400}.sc-tx{color:var(--tx);font-weight:600}
.t-p{color:var(--accent)}.t-n{color:var(--bad)}
/* 오늘: 수집 지연 띠 · 결정 카드 4장 · 트렉시 위치 · 맺음 줄 */
.warnbar{display:flex;align-items:center;gap:8px;width:100%;min-height:44px;margin:0 0 12px;padding:8px 12px;border-radius:12px;background:var(--warn-bg);color:var(--warn-fg);font-size:13px;font-weight:600;line-height:1.45;word-break:keep-all;overflow-wrap:break-word}
.dc{margin:0 0 12px;border:1px solid var(--line);border-radius:16px;background:var(--card);overflow:hidden;word-break:keep-all;overflow-wrap:break-word}
.dc.dc1{border:1.5px solid var(--tx)}
.dc-hh{margin:0;font-size:inherit;font-weight:inherit}
.dc-hd{display:flex;align-items:center;gap:8px;width:100%;min-height:44px;padding:0 12px 0 16px}
div.dc-hd{cursor:default}
.dc-no{width:22px;height:22px;flex:none;border-radius:999px;background:var(--tx);color:var(--bg);font-size:13px;font-weight:700;display:inline-flex;align-items:center;justify-content:center;font-variant-numeric:tabular-nums}
.dc-t{font-size:14px;font-weight:600}.dc1 .dc-t{white-space:nowrap}
.dc-meta{margin-left:auto;font-size:13px;color:var(--sub);text-align:right}
.chev{color:var(--muted)}
.dc-h{margin:0;padding:0 16px 10px;font-size:var(--fs-title);font-weight:700;line-height:1.35;letter-spacing:-.02em}
.dc-p{margin:0;padding:0 16px 12px;font-size:13px;color:var(--sub);line-height:1.5}
.dc-row{display:flex;align-items:center;gap:10px;width:100%;min-height:60px;padding:9px 12px 9px 16px;border-top:1px solid var(--line)}
.dc-rb{flex:1;min-width:0;display:flex;flex-direction:column;gap:3px}
.dc-rt{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.dc-nm{font-size:var(--fs-name);font-weight:700}
.dc-why{font-size:14px;color:var(--tx2);line-height:1.45}
.dc-hint{font-size:13px;color:var(--sub)}
.dc-chg{margin:0;padding:0 16px 10px;font-size:13px;color:var(--tx2);line-height:1.5;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.dc-chg b{color:var(--tx);font-weight:600}
.tg.chg{border-color:var(--hold-bd);color:var(--tx2);font-weight:500}
.dc-more{display:flex;align-items:center;gap:10px;width:100%;min-height:52px;padding:8px 12px 8px 16px;border-top:1px solid var(--line);color:var(--accent)}
.dc-mt{flex:1;min-width:0;display:flex;flex-direction:column;gap:1px}
.dc-mt .t{font-size:15px;font-weight:700}.dc-mt .s{font-size:13px;color:var(--sub)}
.dc-in{padding:0 16px 12px}
.fx-hero{display:flex;align-items:baseline;flex-wrap:wrap;gap:2px 8px;margin:2px 0 0;font-weight:700}
.fx-hero .nm,.fx-hero .d{font-size:16px}
.fx-hero .v{font-size:var(--fs-hero);line-height:1.15;letter-spacing:-.02em;font-variant-numeric:tabular-nums}
.dc-s{margin:4px 0 0;font-size:13px;color:var(--sub);line-height:1.5}
.dc-s+.dc-s{margin-top:0}
.fx-rows{margin-top:10px;border-top:1px solid var(--line)}
.fx-r{display:grid;grid-template-columns:76px 72px minmax(0,1fr);align-items:center;gap:2px 8px;min-height:40px;padding:2px 0;border-bottom:1px solid var(--line2)}
.fx-r .fx-st{grid-column:1/-1;padding-bottom:6px;line-height:1}
.fx-r .nm,.fx-r .v{font-size:15px;font-weight:600}
.fx-r .v{text-align:right;font-variant-numeric:tabular-nums}
.fx-r .d{font-size:14px;text-align:right}
.fx-al{margin:8px 0 0;font-size:13px;color:var(--sub);line-height:1.5}
.fx-ai{margin:2px 0 0;font-size:14px;color:var(--tx);line-height:1.5}
.dc-evs,.dc-nws{padding:0 16px 6px}
.dc-ev{display:grid;grid-template-columns:52px minmax(0,1fr) auto;align-items:center;gap:10px;width:100%;min-height:54px;padding:7px 0;border-top:1px solid var(--line)}
.dc-ev:first-child{border-top:0}
.dc-ev .d,.bd-nx .d{font-size:16px;font-weight:700;font-variant-numeric:tabular-nums}
.ev-tt{display:flex;flex-direction:column;gap:1px;min-width:0}
.ev-tt .t{font-size:15px;font-weight:600}.ev-tt .s{font-size:13px;color:var(--sub)}
.kind{font-size:13px;font-weight:600;padding:2px 8px;border-radius:6px;background:var(--fill);color:var(--tx2);white-space:nowrap}
.kind.sale{background:var(--accent-weak);color:var(--accent)}
.dc-news{display:flex;flex-direction:column;gap:4px;padding:10px 0;border-top:1px solid var(--line);color:var(--tx);text-decoration:none}
.dc-news:first-child{border-top:0}
.dc-news .t{font-size:15px;font-weight:600;line-height:1.5}.dc-news .s{font-size:13px;color:var(--sub)}
.dc-xmore{display:flex;align-items:center;width:100%;min-height:44px;border-top:1px solid var(--line);font-size:13px;color:var(--accent)}
.dc-peer{display:flex;align-items:center;gap:12px;width:100%;min-height:60px;margin:0 0 12px;padding:10px 12px 10px 16px;border:1px solid var(--line);border-radius:16px;background:var(--card)}
.dc-peer .tt,.bd-hq .tt,.bd-link .tt{flex:1;min-width:0;display:flex;flex-direction:column;gap:1px}
.dc-peer .s,.bd-hq .s,.bd-link .s{font-size:13px;color:var(--sub)}
.dc-peer .t,.bd-hq .t,.bd-link .t{font-size:15px;font-weight:600}
.td-foot{display:block;width:100%;min-height:44px;padding:2px 4px;font-size:13px;color:var(--sub);line-height:1.5;text-align:center}
/* 브랜드 탭: 머리(제목·(i)·판정 필터) · 판정 기준 · 압축 행 · 판정 안 함 접기 */
#brHead{display:flex;flex-direction:column;gap:10px}
.seg4{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:4px;padding:4px;border-radius:12px;background:var(--fill)}
.seg4 button{min-height:44px;padding:0 2px;border-radius:9px;color:var(--tx2);font-size:14px;white-space:nowrap}
.seg4 button[aria-pressed="true"]{background:var(--tx);color:var(--bg);font-weight:700}
@media(max-width:359px){.seg4 button{font-size:13px;letter-spacing:-.04em;padding:0}}   /* 아주 좁은 폭: '지금 검토 2'가 알약 안에 */
/* 다크: 반전 강조(번호 원·고른 필터)가 밝은 칸으로 남지 않게 — 번호 원은 테두리 원, 고른 필터는 파랑 채움 + 흰 글자 */
[data-theme="dark"] .dc-no{background:transparent;color:var(--tx);box-shadow:inset 0 0 0 1.5px var(--tx)}
[data-theme="dark"] .seg4 button[aria-pressed="true"]{background:var(--accent-fill);color:var(--on-accent)}
[data-theme="dark"] .src-more{background:var(--fill);color:var(--tx);box-shadow:inset 0 0 0 1.5px var(--sub)}   /* 지도 '+N' — 다크에서 밝은 알약이 되지 않게 */
.tn{font-variant-numeric:tabular-nums}
.br-info{display:flex;flex-direction:column;gap:8px;margin:0 0 10px;padding:12px 14px;border-radius:14px;background:var(--fill);font-size:14px;line-height:1.55;word-break:keep-all;overflow-wrap:break-word}
.br-info p{margin:0}.br-info .bi-t{font-size:15px;font-weight:700}.br-info .bi-s{font-size:13px;color:var(--sub)}
.br-fnote,.br-foot{margin:0 0 10px;padding:0 2px;font-size:13px;color:var(--sub);line-height:1.5;word-break:keep-all;overflow-wrap:break-word}
.br-list,.br-rest{margin:0 0 10px;border:1px solid var(--line);border-radius:16px;overflow:hidden;background:var(--card);word-break:keep-all;overflow-wrap:break-word}
.br-row{display:flex;align-items:center;gap:8px;width:100%;padding:12px 10px 12px 14px;border-top:1px solid var(--line)}
.br-row:first-child{border-top:0}
.br-m{flex:1;min-width:0;display:flex;flex-direction:column;gap:4px}
.br-l1{display:flex;align-items:center;justify-content:space-between;gap:8px}
.br-nm{display:flex;align-items:baseline;flex-wrap:wrap;gap:2px 8px;min-width:0}
.br-name{font-size:var(--fs-name);font-weight:700}
.br-hq{font-size:13px;color:var(--sub)}
.br-why{font-size:14px;color:var(--tx2);line-height:1.45}
.br-cells{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:4px;margin-top:2px}
.br-c{display:flex;align-items:baseline;gap:5px;font-size:13px;color:var(--sub);white-space:nowrap}
.br-c b{font-size:15px;font-variant-numeric:tabular-nums}
.br-empty{margin:0 0 10px;padding:14px;border:1px solid var(--line);border-radius:16px;background:var(--card);font-size:14px;color:var(--sub);line-height:1.5}
.br-rest>summary{display:flex;align-items:center;justify-content:space-between;gap:12px;min-height:60px;padding:8px 12px 8px 14px;cursor:pointer;list-style:none}
.br-rest>summary::-webkit-details-marker{display:none}
.br-rest>summary .tt{display:flex;flex-direction:column;gap:1px;min-width:0}
.br-rest>summary .t{font-size:15px;font-weight:700}.br-rest>summary .s{font-size:13px;color:var(--sub)}
.br-rest>summary .ic{color:var(--tx2);transition:transform .15s}
.br-rest[open]>summary .ic{transform:rotate(180deg)}
.br-rest-in{padding:0 14px 6px}
.br-rest-row{display:flex;align-items:center;justify-content:space-between;gap:12px;width:100%;min-height:48px;padding:6px 0;border-top:1px solid var(--line)}
.br-rest-row .tt{display:flex;flex-direction:column;min-width:0}
.br-rest-row .t{font-size:15px;font-weight:600}.br-rest-row .t .tg{margin-left:6px}.br-rest-row .s{font-size:13px;color:var(--sub)}
.br-rest-row .y{font-size:14px;color:var(--tx2);white-space:nowrap}.br-rest-row .y b{font-size:15px;font-variant-numeric:tabular-nums}
.br-rest-cur{margin:0;padding:10px 0 6px;border-top:1px solid var(--line);font-size:13px;color:var(--sub);line-height:1.5}
.br-link{display:flex;align-items:center;width:100%;min-height:44px;padding:0 2px;font-size:13px;color:var(--accent)}
/* 브랜드 상세 */
.bd{display:flex;flex-direction:column;gap:14px;padding:4px 0 8px;word-break:keep-all;overflow-wrap:break-word}
.bd h2{margin:0;font-size:16px;font-weight:700}
.bd-sec,.bd-top,.bd-evs{display:flex;flex-direction:column;gap:8px}
.bd-vr{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.bd-meta{font-size:13px;color:var(--sub)}
.bd .bd-head{font-size:var(--fs-dhead);line-height:1.3;letter-spacing:-.02em}
.bd-say{margin:0;font-size:15px;line-height:1.6}
.bd-chg{margin:0;font-size:13px;color:var(--tx2);line-height:1.5}
.bd-tiles{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;margin-top:4px}
.bd-tile{display:flex;flex-direction:column;gap:2px;min-width:0;padding:12px 14px;border:1px solid var(--line);border-radius:14px}
.bd-tile.acc{border:1.5px solid var(--accent)}.bd-tile.acc .tv{color:var(--accent)}
.bd-tile.warn{border:1.5px solid var(--warn-bg)}.bd-tile.warn .tv{color:var(--bad)}
.bd-tile .tl{font-size:13px;color:var(--sub)}
.bd-tile .tv{font-size:var(--fs-tile);font-weight:700;line-height:1.2;font-variant-numeric:tabular-nums}
.bd-tile .tc{font-size:13px;color:var(--tx2);line-height:1.4}
.bd-ev{display:flex;flex-direction:column;gap:4px;min-width:0;padding:12px 14px;border:1px solid var(--line);border-radius:14px}
.bd-ev-hd{display:flex;align-items:center;justify-content:space-between;gap:8px}
.bd-ev-l{font-size:14px;font-weight:600;color:var(--tx2)}
.bd-pt{display:inline-flex;align-items:baseline;gap:4px;flex:none;padding:2px 9px;border-radius:8px;font-size:13px;font-weight:600;white-space:nowrap;background:var(--fill);color:var(--tx2)}
.bd-pt b{font-size:15px;font-weight:700}
.bd-pt.p{background:var(--accent-weak);color:var(--accent)}.bd-pt.n{background:var(--warn-bg);color:var(--warn-fg)}
.bd-ev-v{margin:0;font-size:var(--fs-name);font-weight:700;line-height:1.4}
.bd-ev-v .tg{margin-left:6px}
.bd-ev-x{margin:0;font-size:14px;line-height:1.55;color:var(--tx2)}
.bd-sp{display:flex;flex-direction:column;gap:2px;margin-top:6px;max-width:480px}   /* PC 폭에서 그래프가 커지지 않게 */
.bd-sp .cap,.bd-sp .ends{font-size:13px;color:var(--sub)}
.bd-sp .ends{display:flex;justify-content:space-between;gap:8px}.bd-sp .ends b{font-weight:600;color:var(--tx)}
.bd-spark{display:block;width:100%;height:auto}
.bd-spark .sl{fill:none;stroke:var(--muted);stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
.bd-spark .sd{fill:var(--accent);stroke:var(--card);stroke-width:2}
.bdq{display:flex;flex-direction:column;margin-top:4px}
.bdq-row{display:flex;gap:8px;align-items:flex-start;padding:8px 0 0;border-top:1px solid var(--line2)}
.bdq-t{flex:none;font-size:13px;font-weight:600;line-height:1.5;border-radius:6px;padding:0 6px;background:var(--fill);color:var(--tx2)}
.bdq-b{min-width:0;font-size:14px;line-height:1.5}
.bdq-s{display:inline-block;font-size:13px;font-weight:600;line-height:1.4;border-radius:6px;padding:0 5px;margin-left:4px;white-space:nowrap;border:1px solid var(--sub);color:var(--sub)}
.bdq-s.more{border-color:var(--accent);color:var(--accent)}.bdq-s.less{border-color:var(--bad);color:var(--bad)}
.bdq-b summary{display:inline-flex;align-items:center;min-height:44px;min-width:44px;font-size:13px;color:var(--accent);cursor:pointer}
.bdq-b q{display:block;margin-bottom:8px;font-size:13px;color:var(--sub);line-height:1.5;overflow-wrap:anywhere}
.bd-next,.bd-nws{border:1px solid var(--line);border-radius:14px;padding:0 14px}
.bd-nx{display:grid;grid-template-columns:52px minmax(0,1fr) auto;align-items:center;gap:10px;width:100%;min-height:60px;padding:8px 0;border-top:1px solid var(--line)}
.bd-nx:first-child{border-top:0}
div.bd-nx{cursor:default}
.bd-news{display:flex;flex-direction:column;gap:2px;padding:12px 0;border-top:1px solid var(--line);color:var(--tx);text-decoration:none}
.bd-news:first-child{border-top:0}
.bd-news .t{font-size:15px;font-weight:600;line-height:1.5}.bd-news .s{font-size:13px;color:var(--sub)}
.bd-link{display:flex;align-items:center;gap:8px;width:100%;min-height:52px;padding:8px 0;border-top:1px solid var(--line)}
.bd-link .t{color:var(--accent)}
.bd-none{margin:0;padding:12px 0;font-size:14px;color:var(--sub)}
.bd-hq{display:flex;align-items:center;gap:12px;width:100%;min-height:56px;padding:8px 12px 8px 14px;border:1px solid var(--line);border-radius:14px;background:var(--card)}
/* 더보기 메뉴(머리 '더보기' + 줄 5개 + 화면 테마) */
.mmenu{margin:0 0 10px;border:1px solid var(--line);border-radius:16px;overflow:hidden;background:var(--card);word-break:keep-all;overflow-wrap:break-word}
.mi{display:grid;grid-template-columns:30px minmax(0,1fr) auto;gap:10px;align-items:center;width:100%;min-height:60px;padding:8px 12px 8px 14px;border-top:1px solid var(--line)}
.mi:first-child{border-top:0}
.mi .mic{display:inline-flex;justify-content:center;color:var(--tx2)}
.mi .mtt{display:flex;flex-direction:column;gap:1px;min-width:0}
.mi .mt{font-size:15px;font-weight:700}.mi .md{font-size:13px;color:var(--sub);line-height:1.4}
.mi .mr{font-size:13px;color:var(--sub);text-align:right;line-height:1.45}
.mi .mr b{font-weight:600;color:var(--tx)}
.mi .mr .wn{display:inline-block;padding:0 7px;border-radius:999px;background:var(--warn-bg);color:var(--warn-fg);font-weight:700;white-space:nowrap}
.mi .mr .ok{color:var(--accent)}
.mnote{margin:0 2px 10px;font-size:13px;color:var(--sub);line-height:1.5;word-break:keep-all;overflow-wrap:break-word}
.co-hq{margin:0 0 12px}   /* 국내 법인 상세 '글로벌 본사' 줄(브랜드 상세 본사 줄과 같은 모양 · 44px 이상) */
/* PC·태블릿: 환율 표 값·차이 글이 벌어지지 않게 · 점수 4칸 폭 상한 */
@media(min-width:760px){.fx-r{grid-template-columns:76px 72px auto;justify-content:start}.br-cells{max-width:480px}}
/* '움직임 줄이기' 설정(스크롤은 smoothB) */
@media(prefers-reduced-motion:reduce){*,*::before,*::after{transition:none!important;animation:none!important}}
</style>
</head>
<body>
<!-- v33 A안: 선 아이콘 스프라이트 — ic('이름', 크기)로 <use href="#i-이름">. 색은 글자색(currentColor)이라 다크 모드 자동 -->
<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>
<symbol id="i-home" viewBox="0 0 24 24"><path d="M3.5 10.5 12 3.5l8.5 7"/><path d="M5.5 9v11.5h13V9"/><path d="M10 20.5v-6h4v6"/></symbol>
<symbol id="i-tag" viewBox="0 0 24 24"><path d="M3.5 3.5h7.8l9.2 9.2-7.8 7.8-9.2-9.2z"/><circle cx="8" cy="8" r="1.6"/></symbol>
<symbol id="i-chart" viewBox="0 0 24 24"><path d="M4 4v16h16"/><path d="m7.5 14.5 3.5-4 3 2.5 5-6"/></symbol>
<symbol id="i-grid" viewBox="0 0 24 24"><rect x="4" y="4" width="6.5" height="6.5" rx="1.5"/><rect x="13.5" y="4" width="6.5" height="6.5" rx="1.5"/><rect x="4" y="13.5" width="6.5" height="6.5" rx="1.5"/><rect x="13.5" y="13.5" width="6.5" height="6.5" rx="1.5"/></symbol>
<symbol id="i-go" viewBox="0 0 16 16"><circle cx="8" cy="8" r="6.2"/><path d="m5.3 8.2 1.9 1.9 3.6-3.9"/></symbol>
<symbol id="i-wait" viewBox="0 0 16 16"><circle cx="8" cy="8" r="6.2"/><path d="M6.5 5.7v4.6"/><path d="M9.5 5.7v4.6"/></symbol>
<symbol id="i-warn" viewBox="0 0 16 16"><path d="M8 2.3 14.2 13.2H1.8z"/><path d="M8 6.5v3"/><path d="M8 11.3v.1"/></symbol>
<symbol id="i-info" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 11v5.5"/><path d="M12 7.6v.1"/></symbol>
<symbol id="i-left" viewBox="0 0 24 24"><path d="m15 6-6 6 6 6"/></symbol>
<symbol id="i-right" viewBox="0 0 24 24"><path d="m9 6 6 6-6 6"/></symbol>
<symbol id="i-down" viewBox="0 0 24 24"><path d="m6 9 6 6 6-6"/></symbol>
<symbol id="i-up" viewBox="0 0 24 24"><path d="m6 15 6-6 6 6"/></symbol>
<symbol id="i-arrow" viewBox="0 0 24 24"><path d="M5 12h14"/><path d="m13 6 6 6-6 6"/></symbol>
<symbol id="i-close" viewBox="0 0 24 24"><path d="M6 6l12 12"/><path d="M18 6 6 18"/></symbol>
<symbol id="i-alert" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 7.5v5.5"/><path d="M12 16.3v.1"/></symbol>
<symbol id="i-sun" viewBox="0 0 24 24"><circle cx="12" cy="12" r="4"/><path d="M12 2.5v2"/><path d="M12 19.5v2"/><path d="M2.5 12h2"/><path d="M19.5 12h2"/><path d="m5.3 5.3 1.4 1.4"/><path d="m17.3 17.3 1.4 1.4"/><path d="m5.3 18.7 1.4-1.4"/><path d="m17.3 6.7 1.4-1.4"/></symbol>
<symbol id="i-moon" viewBox="0 0 24 24"><path d="M19.5 14.6A8 8 0 0 1 9.4 4.5a8 8 0 1 0 10.1 10.1z"/></symbol>
<symbol id="i-store" viewBox="0 0 24 24"><path d="M4.5 10.5v10h15v-10"/><path d="M3 9.5 5 4h14l2 5.5"/><path d="M3 9.5a3 3 0 0 0 6 0 3 3 0 0 0 6 0 3 3 0 0 0 6 0"/><path d="M10 20.5v-5h4v5"/></symbol>
<symbol id="i-shirt" viewBox="0 0 24 24"><path d="M9 4 4.5 6.5l1.5 4 2-.8V20h8V9.7l2 .8 1.5-4L15 4a3 3 0 0 1-6 0z"/></symbol>
<symbol id="i-fx" viewBox="0 0 24 24"><path d="M4 8.5h13.5"/><path d="m14 5 3.5 3.5L14 12"/><path d="M20 15.5H6.5"/><path d="m10 12-3.5 3.5L10 19"/></symbol>
<symbol id="i-globe" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3c2.5 2.6 3.8 5.6 3.8 9s-1.3 6.4-3.8 9c-2.5-2.6-3.8-5.6-3.8-9S9.5 5.6 12 3z"/></symbol>
<symbol id="i-pulse" viewBox="0 0 24 24"><path d="M3 12h4l2.5-6 5 12 2.5-6H21"/></symbol>
<symbol id="i-ship" viewBox="0 0 24 24"><path d="M3 14.5h18l-2.8 5.5H5.8z"/><path d="M6 14.5V10h12v4.5"/><path d="M9.5 10V6.5h5V10"/><path d="M12 6.5V3.5"/></symbol>
</defs></svg>
<div class="app">
<main class="content" id="content">
<!-- v33 A안: 하단 탭 4개(오늘·브랜드·시장·더보기). 전역 머리 없이 탭마다 고정 머리(.phead). 옛 종합·기업·캘린더·뉴스·국내 화면은 시장 탭 칩 6개로 그대로 옮김 -->
<div class="pane on" id="p-today">
  <div class="phead" id="tdHead"></div>
  <div id="statusWarn"></div>
  <div id="todayCard"></div>
</div>

<div class="pane" id="p-brand">
  <div id="brandList">
    <div class="phead" id="brHead"></div>
    <div id="brandBody"></div>
  </div>
  <div id="brandDetail" style="display:none">
    <div class="phead dethead"><button type="button" class="hd-back" id="brBack" aria-label="점검표로 돌아가기"><svg class="ic s2" width="24" height="24" aria-hidden="true" focusable="false"><use href="#i-left"/></svg><span id="brBackLbl">점검표</span></button><h1 id="brTitle"></h1><span aria-hidden="true"></span></div>
    <div id="brDetBody"></div>
  </div>
</div>

<div class="pane" id="p-market">
  <h1 class="sr">시장</h1>
  <div class="mk-chips" id="mkChips" role="group" aria-label="시장 화면">
    <button type="button" class="mk-chip on" data-c="news" aria-pressed="true">뉴스</button>
    <button type="button" class="mk-chip" data-c="cal" aria-pressed="false">캘린더</button>
    <button type="button" class="mk-chip" data-c="sig" aria-pressed="false">실적·재고</button>
    <button type="button" class="mk-chip" data-c="co" aria-pressed="false">기업</button>
    <button type="button" class="mk-chip" data-c="kr" aria-pressed="false">국내</button>
    <button type="button" class="mk-chip" data-c="map" aria-pressed="false">소싱 지도</button>
  </div>

  <div class="mk on" id="mk-news">
    <input class="search" id="newsSearch" type="search" enterkeyhint="search" autocomplete="off" maxlength="60" aria-label="지난 뉴스 검색" placeholder="지난 뉴스 검색 (예: 아디다스 재고)">
    <div class="sr" id="newsSrchLive" aria-live="polite"></div>
    <div class="chips" id="newsChips"></div>
    <div id="newsBody"></div>
    <div class="note">매일 03:17 수집 · 최근 14일 보관(국내 유통사 90일) · ★=중요도 · 기본 보기는 그날 수집 전체 + 최근 7일 ★3(칩으로 거르면 전체) · 날짜 머리글 = 수집일, 기사 줄 날짜 = 게재일<br>
    검색창 = 요약·원문 제목·브랜드·매체에서 지난 1년 선별 기사까지 찾음(검색창을 처음 누르면 지난 기사를 한 번 내려받음 · 고른 칩 안에서) · 실제 기사 헤드라인 기반 선별 · 관세·환율·정책 뉴스는 제외 · 헤드라인을 누르면 원문</div>
  </div>

  <div class="mk" id="mk-cal">
    <div class="hgrid" id="calGrid"></div>
    <div class="card" style="margin-top:10px"><h3>90일 이내 실적 발표</h3><div id="calList"></div></div>
    <div class="card" style="margin-top:10px"><h3>해외 세일 시즌 <span class="na" style="font-weight:400">150일 이내 · 매입 시점 참고</span></h3><div id="saleList"></div></div>
    <div class="note">달력의 날짜를 누르면 그 날 발표 기업·진행 중인 세일이 표시됩니다 · 연한 파랑 칸 = 해외 세일 기간 · 굵은 파랑 글자 = 세일 시작일 · 파란 점 = 7일 안 실적 발표 · 일정 미표시 종목은 소스 미제공(미확인)</div>
  </div>

  <div class="mk" id="mk-sig">
    <div class="kpis" id="kpis"></div>
    <div class="hgrid" id="sigBody"></div>
  </div>

  <div class="mk" id="mk-co">
    <div id="coList">
      <input class="search" id="coSearch" type="search" aria-label="기업명 검색" placeholder="기업명 검색 (예: 나이키, 아식스)">
      <div class="chips" id="coChips"></div>
      <div id="coPlat"></div>
      <div class="card" id="coTblCard" style="padding:4px 8px"><div class="tblwrap"><table id="coTbl"></table></div><div class="note" style="margin:6px 4px 4px">외화 매출은 ≈원화 환산(최근 환율, 참고용) · 작은 글씨가 원래 통화</div></div>
      <div class="note">행을 누르면 핵심 지표가 펼쳐지고(휴대폰은 매출총이익률도 여기에), "전체 상세 ›"로 3개년·지역/채널·추이를 봅니다 · "―" = 미확인 · 국내 법인은 연간 자료</div>
    </div>
    <div id="coDetail" style="display:none">
      <div class="phead dethead"><button type="button" class="hd-back" id="coBack" aria-label="기업 목록으로 돌아가기"><svg class="ic s2" width="24" height="24" aria-hidden="true" focusable="false"><use href="#i-left"/></svg><span id="coBackLbl">기업 목록</span></button><h1 id="coTitle"></h1><span aria-hidden="true"></span></div>
      <div id="detBody"></div>
    </div>
  </div>

  <div class="mk" id="mk-kr">
    <div id="hcBox"></div>
    <div id="krBody"></div>
    <div class="note">출처: KOSIS(통계청) — 서비스업동향조사·온라인쇼핑동향조사·소비자물가조사 · 월 1회 갱신<br>
    지수는 2020=100 기준 · 전년 대비 = 전년 같은 달 대비 · 지표를 누르면 최근 13개월 수치 표</div>
  </div>

  <div class="mk" id="mk-map">
    <div id="mapBody"></div>
  </div>
</div>

<div class="pane" id="p-more">
  <div id="moreBody"></div>
</div>

</main>
<nav class="tabs" aria-label="주 메뉴">
  <button type="button" class="tab on" data-p="today" aria-current="page"><svg class="ic" width="24" height="24" aria-hidden="true" focusable="false"><use href="#i-home"/></svg><span>오늘</span></button>
  <button type="button" class="tab" data-p="brand"><svg class="ic" width="24" height="24" aria-hidden="true" focusable="false"><use href="#i-tag"/></svg><span>브랜드</span></button>
  <button type="button" class="tab" data-p="market"><svg class="ic" width="24" height="24" aria-hidden="true" focusable="false"><use href="#i-chart"/></svg><span>시장</span></button>
  <button type="button" class="tab" data-p="more"><svg class="ic" width="24" height="24" aria-hidden="true" focusable="false"><use href="#i-grid"/></svg><span>더보기</span></button>
</nav>
<div class="sheet" id="sheet"></div>
</div>
<script>
/* v33 A안: 테마 — 더보기 '화면 테마' 줄(id="themeBtn", 저장 키 'sim-theme' 그대로). 스크립트 맨 앞(데이터 전)에서 적용 — 스크립트가 문서 끝에 있어
   그 전에 그려지는 빈 틀은 다크 저장 상태에서도 잠깐 밝게 보일 수 있음(head에는 스크립트를 넣지 않음 — check.yml). 버튼이 없어도(메뉴를 아직 안 그렸거나 다른 화면) 멈추지 않음 */
let theme='light';
try{ theme=localStorage.getItem('sim-theme')||'light'; }catch(e){}
function applyTheme(t){
  if(t==='dark') document.documentElement.setAttribute('data-theme','dark'); else document.documentElement.removeAttribute('data-theme');
  const m=document.getElementById('themeColor'); if(m) m.setAttribute('content',t==='dark'?'#0f1115':'#ffffff');   // 휴대폰 상태 표시줄 색
  const b=document.getElementById('themeBtn'); if(!b) return;
  b.setAttribute('aria-pressed',t==='dark'?'true':'false');
  const v=b.querySelector('.mr'); if(v) v.innerHTML=`<b>${t==='dark'?'어둡게':'밝게'}</b>`;
  const u=b.querySelector('.mic use'); if(u) u.setAttribute('href',t==='dark'?'#i-moon':'#i-sun');
}
function toggleTheme(){ theme=theme==='dark'?'light':'dark'; applyTheme(theme); try{ localStorage.setItem('sim-theme',theme); }catch(e){} }
applyTheme(theme);
/* v33 A안: 선 아이콘(스프라이트) · 로컬 날짜 'YYYY-MM-DD'(toISOString은 한국 시간에서 하루 당겨짐) */
/* v33 글꼴(IBM Plex Sans KR, 구글 글꼴 display=swap — 한글은 굵기마다 조각 94개): 첫 화면을 그린 뒤 글꼴 CSS를 붙이고, 들어오면 지금 보이는 글자에
   필요한 조각만 받아(fonts.load) 굵기·크기 한 쌍씩 숨은 글로 글꼴 자료를 미리 만든 뒤 html.wf로 한 번에 바꿈. 숨은 글 배치로 조각을 받고 한꺼번에
   바꾸면 화면이 멈춤(CPU×4 실측 약 0.9초 → 쌍마다 0.02초 안팎) · 조각이 올 때마다 다시 그리지 않음(<head>에서 바로 적용하면 첫 열기가 늦어짐).
   글꼴을 못 받으면(차단·오프라인) 시스템 글꼴 그대로(글자 간격 보정 없음) · 8초가 넘으면 받은 만큼만 적용 */
let WF_GO=false;
function webFont(){
  if(!WF_GO||webFont.on) return;
  if(navigator.onLine===false){ window.addEventListener('online',webFont,{once:true}); return; }   // 오프라인이면 요청하지 않음(실패한 요청은 콘솔 오류) — 연결되면 그때
  webFont.on=1;
  const l=document.createElement('link'); l.rel='stylesheet'; l.id='plexCss';
  l.href='https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+KR:wght@400;600;700&display=swap';
  l.onload=webFontLoad; document.head.appendChild(l);   // 못 받으면(차단) 시스템 글꼴 그대로
}
/* v33 글꼴 바꾸기(wfSwap): 열고 2초 안·아직 화면을 만지지 않았으면(누름·키·스크롤) 바로 바꿈(읽기 전 — 보정 없는 시스템 글꼴은 줄이 다르게 접혀도 됨).
   그 뒤엔 html.wf를 붙여 보고(같은 틀 안 — 그려지지 않음) 지금 보이는 화면이 크게 밀리면(움직인 넓이 비율 × 거리 비율 > 0.1, CLS와 같은 셈)
   되돌렸다가 다음 화면 이동(render) 때 바꿈. 잼: 오늘 0.05~0.1초 · 시장 뉴스·기업 0.2~0.4초(CPU×4) — 바꾼 뒤엔 화면 근처 요소만 */
let WF_DEFER=0, WF_TOUCH=false;
const wfTouch=()=>{ WF_TOUCH=true; ['pointerdown','keydown','wheel','scroll'].forEach(t=>document.removeEventListener(t,wfTouch,true)); };
['pointerdown','keydown','wheel','scroll'].forEach(t=>document.addEventListener(t,wfTouch,{capture:true,passive:true}));
function wfSwap(now){
  const de=document.documentElement; if(de.classList.contains('wf')) return;
  let sc=0;
  if(!now&&!document.hidden&&(WF_TOUCH||performance.now()>2000)) try{
    const vw=innerWidth, vh=innerHeight, G=8, cw=Math.ceil(vw/G), ch=Math.ceil(vh/G), g=new Uint8Array(cw*ch);   // 움직인 넓이 = 8px 칸으로 합침(겹침 한 번만)
    const all=[...document.querySelectorAll('.pane.on *,nav.tabs *,#sheet.on *')], a0=all.map(e=>e.getBoundingClientRect());   // 보이는 화면·하단 탭·열린 패널
    const keep=[]; all.forEach((e,i)=>{ const r=a0[i]; if((r.width||r.height)&&!(r.top>2*vh||r.bottom<-vh)) keep.push(i); });
    const els=keep.map(i=>all[i]), a=keep.map(i=>a0[i]);
    de.classList.add('wf');
    let d=0, n=0;
    els.forEach((e,i)=>{ const p=a[i], q=e.getBoundingClientRect(), m=Math.max(Math.abs(q.left-p.left),Math.abs(q.top-p.top)); if(m<3) return;
      for(const r of [p,q]){ const x0=Math.max(0,Math.floor(r.left/G)), x1=Math.min(cw,Math.ceil(r.right/G)), y0=Math.max(0,Math.floor(r.top/G)), y1=Math.min(ch,Math.ceil(r.bottom/G));
        if(!r.width||!r.height||x1<=x0||y1<=y0) continue; d=Math.max(d,m);
        for(let y=y0;y<y1;y++) for(let x=x0;x<x1;x++) if(!g[y*cw+x]){ g[y*cw+x]=1; n++; } } });
    sc=n/g.length*d/Math.max(vw,vh);
    if(sc>.1){ de.classList.remove('wf'); WF_DEFER=1; try{ performance.mark('wf-defer',{detail:sc}); }catch(e){} return; }
  }catch(e){}
  WF_DEFER=0; de.classList.add('wf'); try{ performance.mark('wf',{detail:sc}); }catch(e){}
}
function webFontLoad(){
  const de=document.documentElement, F=document.fonts, t0=Date.now();
  const by={400:new Set(),600:new Set(),700:new Set()}, wOf=w=>w>=650?700:w>=550?600:400, pairs=new Map();   // pairs: '굵기 크기' → 그 글자 하나
  for(const root of document.querySelectorAll('.pane.on,nav.tabs')){
    const tw=document.createTreeWalker(root,NodeFilter.SHOW_TEXT); let n, last=null, w=400, k='';
    while((n=tw.nextNode())){ const p=n.parentElement; if(!p) continue;
      if(p!==last){ last=p; const cs=getComputedStyle(p); w=wOf(parseInt(cs.fontWeight,10)||400); k=p.closest('svg')?'':(cs.fontStyle!=='normal'?cs.fontStyle+' ':'')+cs.fontWeight+' '+cs.fontSize; }
      for(const ch of n.nodeValue) if(ch.trim()){ by[w].add(ch); if(k&&!pairs.has(k)) pairs.set(k,ch); } }
  }
  const parts=Object.keys(by).filter(w=>by[w].size).map(w=>[w,[...by[w]].join('')]), warm=[...pairs];
  const done=()=>{ if(de.classList.contains('wf')||WF_DEFER) return;
    let ok=true, pend=false;   // Plex 조각을 하나라도 받았나(차단이면 바꾸지 않음 — 시스템 글꼴 그대로라 밀림 없음) · 아직 받는 중이면 들어올 때까지
    try{ const fs=[...F].filter(f=>/Plex/.test(f.family)); ok=fs.some(f=>f.status==='loaded'); pend=fs.some(f=>f.status==='loading'); }catch(e){}
    if(!ok&&pend&&Date.now()-t0<30000){ setTimeout(done,300); return; }
    if(ok) wfSwap(); };
  if(!F||!F.load){ wfSwap(1); return; }
  const step=()=>{ if(de.classList.contains('wf')) return;   // 한 쌍씩 다른 틀에서(그 사이 누름·스크롤 처리) → 다 만들면 바꿈(가벼움)
    const it=warm.shift(); if(!it){ done(); return; }
    const s=document.createElement('span'); s.className='wf-pre'; s.setAttribute('aria-hidden','true'); s.style.font=it[0]+' "IBM Plex Sans KR"'; s.textContent=it[1];
    document.body.appendChild(s); void s.offsetWidth; s.remove(); setTimeout(step,0); };
  let started=0; const start=()=>{ if(!started){ started=1; setTimeout(step,0); } };
  const ld=([w,t])=>{ try{ return F.load(w+' 16px "IBM Plex Sans KR"',t).catch(()=>null); }catch(e){ return null; } };
  const wait=()=>{ if(started) return;   // @font-face 등록(size>0)을 기다렸다가 보이는 글자에 필요한 조각만 받음(못 받은 조각은 시스템 글꼴)
    if(F.size>0) Promise.all(parts.map(ld)).then(start,start); else if(Date.now()-t0>8000) start(); else setTimeout(wait,60); };
  wait(); setTimeout(start,8000);
}
const ic=(n,s=20,c='')=>`<svg class="ic${c?' '+c:''}" width="${s}" height="${s}" aria-hidden="true" focusable="false"><use href="#i-${n}"/></svg>`;
// v33.9 표·그래프 해석을 돕는 긴 설명은 '읽는 법'으로 접어 둠(누르면 펼침) — 숫자·판정·수집 실패 표시는 접지 않음
const why=(html,lb)=>`<details class="why"><summary>${ic('info',15)}<span>${lb||'읽는 법'}</span>${ic('down',14,'why-ic')}</summary><div class="note">${html}</div></details>`;
const ymdL=d=>`${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;
const refocus=(on,sel)=>{ if(!on) return; const n=document.querySelector(sel); if(n) try{ n.focus({preventScroll:true}); }catch(e){} };   // v33 다시 그린 뒤 같은 단추에 초점(키보드)
const nb=s=>String(s).replace(/(\S+) ([가-힣]{1,2})(?=$| ·)/g,'<span class="nw">$1 $2</span>');   // v33 '… 6.3% 쌈'의 '쌈'처럼 끝의 1~2글자가 혼자 다음 줄로 가지 않게 앞 말과 묶음(글자는 그대로) — esc() 뒤 글자에만
const DATA = __DATA__;
const SEGS = __SEGS__;
const SEGS_IR = __SEGS_IR__;
const SEGS_SEC = Object.assign({}, (SEGS&&SEGS.items)||{});   // v32.12 IR로 덮기 전 SEC 추출 — '새 실적 반영 대기' 판정용
if(SEGS_IR&&SEGS_IR.items){ SEGS.items=SEGS.items||{}; Object.entries(SEGS_IR.items).forEach(([k,v])=>{ if(v&&v.extract) SEGS.items[k]=v; }); }
const NEWS = __NEWS__;
const KR = __KR__;
const NAVER = __NAVER__;   // 네이버 데이터랩 검색 관심도(docs/naver_trend.json)
const HIST = __HIST__;
const KRD = __KRD__;
const STATUS = __STATUS__;
const LOGI = __LOGI__;   // v33.4 물류(docs/logistics.json · logistics_fetch v1) — 없으면 null
const WMAP = __WMAP__;   // 소싱 지도 경계(docs/worldmap.json)   // 수집 상태(소스별 마지막 갱신)   // 국내 법인(비상장) — 연 1회 수동 갱신

/* ── 브랜드 로고 도메인 ── */
const DOMAINS = {
  "FRAS.L":"frasers.group", "ZAL.DE":"zalando.com", "SBFG3.SA":"gruposbf.com.br", "4240.SR":"cenomiretail.com",
  "NKE":"nike.com", "ADS.DE":"adidas.com", "ONON":"on.com",
  "DECK":"hoka.com", "AS":"amersports.com", "LULU":"lululemon.com",
  "7936.T":"asics.com", "BIRK":"birkenstock.com", "CROX":"crocs.com",
  "VFC":"vfc.com", "UAA":"underarmour.com",
  "8022.T":"mizuno.com", "7906.T":"yonex.com", "8111.T":"goldwin.co.jp",
  "2020.HK":"anta.com", "2331.HK":"lining.com", "PUM.DE":"puma.com",
  "WWW":"wolverineworldwide.com", "COLM":"columbia.com", "DOCS.L":"drmartens.com",
  "456A.T":"humanmade.jp", "0933.HK":"clarks.com", "VULC3.SA":"vulcabras.com",
  "LUXE":"mytheresa.com", "2670.T":"abc-mart.co.jp", "6110.HK":"topsports.com.cn",
  "TJX":"tjx.com", "ROST":"rossstores.com", "BURL":"burlington.com", "CPNG":"coupang.com",
  "DKS":"dickssportinggoods.com", "JD.L":"jdplc.com", "ASO":"academy.com",
  "081660.KS":"fila.co.kr", "383220.KS":"fnf.co.kr", "298540.KQ":"thenatureholdings.com",
  "120110.KS":"kolonindustries.com", "337930.KQ":"xexymix.com", "000680.KS":"lsnetworks.co.kr",
  "036620.KQ":"gamsung.co.kr", "278470.KS":"apr-in.com",
  "031430.KS":"sikorea.co.kr", "020000.KS":"handsome.co.kr", "093050.KS":"lfcorp.com",
  "028260.KS":"samsungcnt.com", "005390.KS":"shinsung.co.kr",
  "111770.KS":"youngone.co.kr", "241590.KS":"hsenterprise.co.kr", "105630.KS":"hansae.com",
  "009970.KS":"youngonecorporation.com",
  "023530.KS":"lotteshopping.com", "004170.KS":"shinsegae.com", "069960.KS":"ehyundai.com",
  "krd:nike_kr":"nike.com", "krd:adidas_kr":"adidas.co.kr", "krd:asics_kr":"asics.com", "krd:puma_kr":"puma.com",
  "krd:descente_kr":"descentekorea.co.kr", "krd:skechers_kr":"skechers.com", "krd:arena_kr":"arena.co.kr", "krd:nb_eland":"newbalance.co.kr", "krd:abcmart_kr":"abcmart.co.kr",
  "krd:shoemarker":"shoemarker.co.kr", "krd:musinsa":"musinsa.com", "krd:k2_kr":"k2group.co.kr",
  "krd:blackyak":"blackyak.com", "krd:nepa":"nepa.co.kr", "krd:shinsung":"shinsungtongsang.com",
  "krd:kream":"kream.co.kr", "krd:trenbe":"trenbe.com", "krd:balaan":"balaan.co.kr", "krd:mustit":"mustit.co.kr",
  "krd:rexmond":"okmall.com", "krd:hana_int":"hahamall.net", "krd:bbluein":"bblue.co.kr",
  "EL.PA":"essilorluxottica.com", "SFL.MI":"safilogroup.com", "krd:iicombined":"gentlemonster.com", "krd:luxottica_kr":"luxottica.com", "krd:kering_ey_kr":"keringeyewear.com",
  "krd:fivespace":"adererror.com", "krd:andar":"andar.co.kr", "krd:matinkim":"matinkim.com", "krd:piecepeace":"mardimercredi.com",
  "MONC.MI":"moncler.com", "ZGN":"zegna.com", "BRBY.L":"burberry.com", "RL":"ralphlauren.com"   // v33.8
};
/* ── 브랜드 본사 나라(v33: 국기 대신 이름 — 상세 머리 '미국 · NKE') ── */
const FLAGS = {
  "NKE":"미국", "ADS.DE":"독일", "ONON":"스위스", "DECK":"미국", "AS":"핀란드",
  "LULU":"캐나다", "7936.T":"일본", "BIRK":"독일", "CROX":"미국", "VFC":"미국",
  "UAA":"미국", "8022.T":"일본", "7906.T":"일본", "8111.T":"일본",
  "2020.HK":"중국", "2331.HK":"중국", "PUM.DE":"독일", "WWW":"미국",
  "COLM":"미국", "DOCS.L":"영국", "EL.PA":"프랑스", "SFL.MI":"이탈리아", "DKS":"미국", "JD.L":"영국", "ASO":"미국",
  "FRAS.L":"영국", "ZAL.DE":"독일", "SBFG3.SA":"브라질", "4240.SR":"사우디",
  "456A.T":"일본", "0933.HK":"홍콩", "VULC3.SA":"브라질", "LUXE":"독일", "2670.T":"일본", "6110.HK":"중국",
  "TJX":"미국", "ROST":"미국", "BURL":"미국", "CPNG":"한국",
  "MONC.MI":"이탈리아", "ZGN":"이탈리아", "BRBY.L":"영국", "RL":"미국"   // v33.8
};
const GROUPS = (DATA.group_order && DATA.group_order.length) ? DATA.group_order
  : ["글로벌 브랜드","글로벌 유통","국내 브랜드","국내 패션대기업","국내 OEM","국내 유통"];
const isKR = t => /\.K[SQ]$/.test(t);
const NEWS_KEY = {"FRAS.L":"frasers","ZAL.DE":"zalando","SBFG3.SA":"sbf","4240.SR":"cenomi","NKE":"nike","ADS.DE":"adidas","ONON":"on","DECK":"hoka","AS":"amer","LULU":"lululemon","7936.T":"asics",
  "BIRK":"birkenstock","CROX":"crocs","VFC":"vf","UAA":"ua","8022.T":"mizuno","7906.T":"yonex","8111.T":"goldwin",
  "2020.HK":"anta","2331.HK":"lining","PUM.DE":"puma","WWW":"saucony","COLM":"columbia","DOCS.L":"drmartens","456A.T":"humanmade","0933.HK":"clarks","DKS":"dks","JD.L":"jd","ASO":"academy",
  "MONC.MI":"moncler","ZGN":"thombrowne","BRBY.L":"burberry","RL":"ralphlauren",   // v33.8
  "krd:nike_kr":"nike","krd:adidas_kr":"adidas","krd:asics_kr":"asics","krd:puma_kr":"puma","krd:descente_kr":"descente","krd:skechers_kr":"skechers",
  "krd:nb_eland":"newbalance"};
/* 재고일수 = 재고 ÷ 매출원가 × 365 (연간 원가 기준, 재고는 최근 잔액) */
function dioOf(inv, rev, gp, cogs){
  const c = (cogs!=null) ? cogs : ((rev!=null && gp!=null) ? rev-gp : null);
  if(inv==null || !c || c<=0) return null;
  return inv / c * 365;
}
/* ── 한국 시장 신호 (v27) ── */
/* 한국이 속한 지역 찾기: 지역명에 Korea 명시 > 나이키 APLA > 아시아태평양 > Rest of World > International */
const KOREA_PAT=[[/korea/i,true],[/asia pacific & latin america|\bapla\b/i,false],
  [/asia[\s\/-]*pacific|\bapac\b|\bapma\b/i,false],[/^asia\b(?![\s\/-]*pacific)/i,false],[/rest of world/i,false],[/international/i,false]];   // v33.8 'Asia…'(태평양 빼고) = 랄프로렌 'Asia'
function koreaRegion(t){
  const s=(SEGS.items||{})[t]; const ex=s&&s.extract;
  if(!ex||!ex.regions) return null;
  const regs=ex.regions.filter(r=>(r.revenue!=null||r.yoy_pct!=null||r.cn_yoy_pct!=null)&&!/total|합계|전체/i.test(r.name||''));
  for(const [re,explicit] of KOREA_PAT){
    const r=regs.find(z=>re.test(z.name||''));
    if(r) return {name:r.name, yoy:r.yoy_pct, cn:r.cn_yoy_pct, period:ex.period||'', explicit, src:/^IR/.test(s.source||'')?'IR':'SEC'};
  }
  return null;
}
function ksigRow(label, tag, desc, val, sub){
  return `<div class="ksig"><div class="kh"><span>${label}</span>${tag?`<span class="tag2">${tag}</span>`:''}</div>
    <div class="kb"><span class="d">${desc}</span>${val?`<span class="v">${val}</span>`:''}</div>${sub?`<div class="ks">${sub}</div>`:''}</div>`;
}
function koreaMarketLine(){
  if(!KR||!KR.series) return null;
  const pick=[['retail_apparel','의복 소매'],['retail_shoesbag','신발·가방 소매'],['online_sports','온라인 스포츠·레저']];
  let last=null; const parts=[];
  pick.forEach(([k,lab])=>{
    const s=KR.series[k]; if(!s||!s.values) return;
    const ps=Object.keys(s.values).sort(); const p=ps[ps.length-1]; last=last&&last>p?last:p;
    const y=s.yoy?s.yoy[p]:null; parts.push(`${lab} ${fmt(y,1,true)}`);
  });
  return parts.length?{txt:parts.join(' · '), prd:last}:null;
}
function koreaCard(x){
  const t=x.ticker;
  let h=`<div class="card"><h3>한국 시장 신호</h3>`;
  // ① 국내 법인 (DART)
  const kd=((KRD&&KRD.entities)||[]).find(e=>e.link===t);
  if(kd){
    const ys=(kd.years||[]).filter(y=>y.rev!=null), l=ys[ys.length-1], p=ys[ys.length-2];
    if(l){
      const yoy=(p&&p.rev)?(l.rev/p.rev-1)*100:null, iy=(p&&l.inv&&p.inv)?(l.inv/p.inv-1)*100:null;
      const dio=dioOf(l.inv,l.rev,null,l.cogs);
      h+=ksigRow('국내 법인','DART',`${logoImg('krd:'+kd.id,false,kd.name)}${esc(kd.name)}`,
        `매출 ${fmt(yoy,1,true)} · 재고 ${fmtInv(iy)}`,
        `${dio!=null?`재고일수 ${Math.round(dio)}일 · `:''}FY ${ym(l.end)} 결산 · 원화`);
    } else {
      h+=ksigRow('국내 법인','DART',`${esc(kd.name)}`,'<span class="na">공시 없음</span>',esc((kd.note||'').split(' — ')[0]));
    }
  } else {
    h+=ksigRow('국내 법인','',`<span class="na">추적 중인 국내 법인 없음</span>`,'');
  }
  // ② 본사 공시의 한국이 속한 지역
  const rg=koreaRegion(t);
  if(rg){
    const val=rg.cn!=null?`<span class="na" style="font-weight:400">환율 제외</span> ${fmt(rg.cn,1,true)}`:`${fmt(rg.yoy,1,true)}`;
    const sub=[rg.cn!=null&&rg.yoy!=null?`보고 통화 ${fmt(rg.yoy,1,true)}`:(rg.cn==null?'보고 통화 기준':''),
               rg.explicit?'한국 명시':'한국이 속한 지역', esc(rg.period)].filter(Boolean).join(' · ');
    h+=ksigRow('본사 지역',rg.src,esc(rg.name),val,sub);
  } else {
    h+=ksigRow('본사 지역','',`<span class="na">지역 분해 미공시 또는 미추출</span>`,'');
  }
  // ③ 국내 시장 (KOSIS)
  const km=koreaMarketLine();
  if(km) h+=ksigRow(`국내 시장 <span class="na">· ${fmtPrd(km.prd)} 전년 동월 대비</span>`,'KOSIS',km.txt,'');
  h+=why('본사 지역 수치는 한국 단독이 아니라 한국이 속한 지역 합계 · 환율 제외 = 현지 통화 기준(회사 공시값) · 국내 법인은 연간(별도 재무제표)')+`</div>`;   // v33.9 접음
  return h;
}
/* ── 소싱 기회 지도 (v28) ── */
/* 브랜드별로 유럽·중동·남미에 대응하는 공시 지역(정규식, 표기)
   중동은 대부분 EMEA 합산값을 빌려 씀(차용) — 화면에 추정으로 표시 */
const SRC_CFG={
  'ADS.DE':{europe:[/^europe$/i,null],middleeast:[/emerging markets/i,'신흥시장 합산'],samerica:[/^latin america$/i,null],
            namerica:[/^north america$/i,null],japan:[/japan\/south korea/i,'일본+한국 합산']},
  'PUM.DE':{europe:[/^emea$/i,'유럽·중동·아프리카 합산'],middleeast:[/^emea$/i,'유럽·중동·아프리카 값 차용'],samerica:[/^latin america$/i,null],
            namerica:[/^north america$/i,null],japan:[/^asia\/pacific$/i,'아시아·태평양 합산']},
  '7936.T':{europe:[/^europe$/i,null],middleeast:null,samerica:[/^others/i,'남미+한국 합산'],
            namerica:[/^north america$/i,null],japan:[/^japan$/i,null]},
  'NKE':{europe:[/europe, middle east/i,'유럽·중동·아프리카 합산'],middleeast:[/europe, middle east/i,'유럽·중동·아프리카 값 차용'],samerica:[/latin america/i,'아시아+남미 합산'],
            namerica:[/^north america$/i,null],japan:[/asia pacific & latin america/i,'아시아·태평양+남미 합산']},
  'AS':{europe:[/^emea$/i,'유럽·중동·아프리카 합산'],middleeast:[/^emea$/i,'유럽·중동·아프리카 값 차용'],samerica:null,
            namerica:[/^americas$/i,'미주(남미 포함) 합산'],japan:[/^asia pacific$/i,'아시아·태평양 합산']},
  'BIRK':{europe:[/^emea$/i,'유럽·중동·아프리카 합산'],middleeast:[/^emea$/i,'유럽·중동·아프리카 값 차용'],samerica:null,
            namerica:[/^americas$/i,'미주(남미 포함) 합산'],japan:[/^apac$/i,'아시아·태평양 합산']},
  'COLM':{europe:[/europe, middle east/i,'유럽·중동·아프리카 합산'],middleeast:[/europe, middle east/i,'유럽·중동·아프리카 값 차용'],samerica:[/latin america and asia/i,'남미+아시아 합산'],
            namerica:[/^united states$/i,'미국만'],japan:[/latin america and asia/i,'남미+아시아 합산']},
  'UAA':{europe:[/^emea$/i,'유럽·중동·아프리카 합산'],middleeast:[/^emea$/i,'유럽·중동·아프리카 값 차용'],samerica:[/^latin america$/i,null],
            namerica:[/^north america$/i,null],japan:[/^asia-pacific$/i,'아시아·태평양 합산']},
  'VFC':{europe:[/^emea$/i,'유럽·중동·아프리카 합산'],middleeast:[/^emea$/i,'유럽·중동·아프리카 값 차용'],samerica:null,
            namerica:[/^americas$/i,'미주(남미 포함) 합산'],japan:[/^apac$/i,'아시아·태평양 합산']},
  'CROX':{europe:null,middleeast:null,samerica:null,namerica:[/north america/i,null],japan:null},
  'DECK':{europe:null,middleeast:null,samerica:null,namerica:[/^domestic$/i,'미국 내수'],japan:null},
};
const SRC_KEYS=['europe','namerica','japan','middleeast','samerica'];
const SRC_NAMES={europe:'유럽',namerica:'북미',japan:'일본',middleeast:'중동',samerica:'남미'};
const SRC_EST={middleeast:1,japan:1};   // 합산값을 빌려 쓴 추정 지역(빗금·'추정' 표시)
const SRC_LV={2:{bg:'var(--lv2-bg)',fg:'var(--lv2-fg)',txt:'높음',ring:'var(--lv2-ring)',map:'var(--lv2-map)'},   // v33 색은 토큰(라이트·다크)
              1:{bg:'var(--lv1-bg)',fg:'var(--lv1-fg)',txt:'보통',ring:'var(--lv1-ring)',map:'var(--lv1-map)'},
              0:{bg:'var(--lv0-bg)',fg:'var(--lv0-fg)',txt:'낮음',ring:'var(--lv0-ring)',map:'var(--lv0-map)'}};
const SRC_RNAME=[[/^europe$/i,'유럽'],[/^emea$|europe, middle east/i,'유럽·중동·아프리카'],[/emerging markets/i,'신흥시장'],
  [/asia pacific & latin america/i,'아시아·남미'],[/latin america and asia/i,'남미·아시아'],[/latin america/i,'중남미'],[/^others/i,'남미·한국 등'],
  [/japan\/south korea/i,'일본·한국'],[/^japan$/i,'일본'],[/north america/i,'북미'],[/^americas$/i,'미주'],[/^united states$/i,'미국'],
  [/^domestic$/i,'미국 내수'],[/^asia[\s\/-]*pacific$|^apac$/i,'아시아·태평양']];
const srcRegName=n=>{ for(const [re,k] of SRC_RNAME) if(re.test(n||'')) return k; return n; };
const pp=v=>{ const r=+v.toFixed(1); return (r>0?'+':r<0?'−':'')+Math.abs(r).toFixed(1)+'%'; };   // v33 음수 '−'
const ppp=v=>pp(v)+'p';   // %p
const mnum=(v,d=1)=>{ const r=+v.toFixed(d); return (r<0?'−':'')+Math.abs(r).toFixed(d); };   // 부호 없는 자리의 음수만 '−'
let SRC_PRESET='A', SRC_SHEET=null, SRC_CACHE=null, LAST_SHEET=null, LAST_SHEET_Y=0;   // v33 A안: LAST_SHEET(_Y) = 패널 안에서 다른 화면으로 갈 때 닫은 패널과 그 안 스크롤(돌아오면 다시 엶)
function srcModel(){
  if(SRC_CACHE) return SRC_CACHE;
  const g=r=>r.cn_yoy_pct!=null?r.cn_yoy_pct:r.yoy_pct;
  const out=[];
  Object.entries(SRC_CFG).forEach(([t,cfg])=>{
    const x=DATA.items.find(i=>i.ticker===t); const s=(SEGS.items||{})[t]; const ex=s&&s.extract;
    const ip=x?invPick(x):null;   // v32.14 재고 압력 = 같은 기간 재고 증감 − 같은 기간 매출 증감
    if(!x||!ex||!ex.regions||ip.inv==null||ip.rev==null) return;
    const regs=ex.regions.filter(r=>g(r)!=null&&!/total|합계|corporate|global brand|converse/i.test(r.name||''));
    if(!regs.length) return;
    const vs=regs.map(g).sort((a,b)=>a-b), n=vs.length, med=n%2?vs[(n-1)/2]:(vs[n/2-1]+vs[n/2])/2;
    const P=ip.inv-ip.rev, cells={};
    SRC_KEYS.forEach(k=>{
      const spec=cfg[k]; const r=spec?regs.find(z=>spec[0].test(z.name||'')):null;
      if(!r){ cells[k]=null; return; }
      const v=g(r), excess=P>=5, weak=v<0||(v<10&&v<med);
      const why=[]; if(excess) why.push(`재고 압력 ${ppp(P)}`); if(weak) why.push(v<0?'지역 역성장':'지역 성장 둔화');
      cells[k]={g:v, basis:r.cn_yoy_pct!=null?'환율 제외':'보고 통화', rname:srcRegName(r.name), proxy:spec[1],
        A:(excess&&weak)?2:((excess||weak)?1:0), B:(v>=15||ip.inv>=15)?2:((v>=5||ip.inv>=5)?1:0), why:why.join(' · ')||'해당 없음'};
    });
    out.push({t, name:x.name, inv:ip.inv, rev:ip.rev, invLbl:ip.lbl, period:perKo((ex.period||'').split(/;| ended/)[0]), cells, kr:koreaRegion(t)});
  });
  return (SRC_CACHE=out);
}
function srcRanked(k){
  return srcModel().filter(b=>b.cells[k]).map(b=>({b, c:b.cells[k], lvl:b.cells[k][SRC_PRESET]}))
    .sort((x,y)=>(y.lvl-x.lvl)||(Math.abs(y.c.g)-Math.abs(x.c.g)));
}
/* 지역 판정(v29.3) = 기회 높은 브랜드 수(최대 2점) + 현지 유통 재고(재고 과잉형만 ±1) + 환율(±1)
   → 3점 이상 높음 · 1~2점 보통 · 0점 이하 낮음 */
function srcRetailSig(k){
  const rs=(SRC_RETAIL[k]||[]).map(t=>{ const x=DATA.items.find(i=>i.ticker===t); if(!x) return null;
    const ip=invPick(x);
    return (ip.inv==null||ip.rev==null)?null:{name:x.name, d:ip.inv-ip.rev}; }).filter(Boolean);
  if(!rs.length) return {pt:0, txt:'현지 유통사 자료 없음'};
  const heavy=rs.filter(r=>r.d>=5);
  if(heavy.length) return {pt:1, txt:'현지 유통 재고 무거움 '+heavy.map(r=>r.name).join('·')};
  if(rs.every(r=>r.d<=-5)) return {pt:-1, txt:'현지 유통 재고 가벼움'};
  return {pt:0, txt:'현지 유통 재고 보통'};
}
function srcFxSig(k){
  const fx=(SRC_FXMAP[k]||[]).map(c=>(DATA.fx||{})[c]).filter(f=>f&&f.chg_pct!=null);
  if(!fx.length) return {pt:0, txt:'환율 자료 없음'};
  const avg=fx.reduce((a,f)=>a+f.chg_pct,0)/fx.length, lst=fx.map(f=>`${f.name} ${pp(f.chg_pct)}`).join('·')+'(1년 전 대비)';
  if(avg<=-2) return {pt:1, txt:`${lst} — 매입 부담 줄어듦`};
  if(avg>=2) return {pt:-1, txt:`${lst} — 매입 부담 커짐`};
  return {pt:0, txt:`${lst} — 환율 비슷`};
}
function srcSumm(k){
  const hi=srcRanked(k).filter(o=>o.lvl===2), br=Math.min(hi.length,2);
  const rt=SRC_PRESET==='A'?srcRetailSig(k):null, fx=srcFxSig(k);
  const score=br+(rt?rt.pt:0)+fx.pt;
  return {hi, score, level:score>=3?2:(score>=1?1:0), parts:[{pt:br, txt:`기회 높은 브랜드 ${hi.length}곳`}, ...(rt?[rt]:[]), fx]};
}
function srcBadge(t,name,ring,large){
  const d=DOMAINS[t]; const init=d?d.replace(/^www\./,'').slice(0,2).toUpperCase():String(name||t).replace(/[^가-힣A-Za-z0-9]/g,'').slice(0,1);
  const fb=`<i style="${d?'display:none':''}">${init}</i>`;
  return `<span class="src-bd${large?' lg':''}" style="border-color:${ring}">${d?`<img loading="lazy" alt="" src="https://www.google.com/s2/favicons?domain=${d}&sz=64" onerror="this.style.display='none';this.nextSibling.style.display='inline'">`:''}${fb}</span>`;
}
function srcMapSvg(){
  const W=WMAP; if(!W) return '<div class="na">지도 데이터 없음 — docs/worldmap.json 확인</div>';
  const vb=W.viewBox.split(' ').map(Number), K=W.korea_pt;
  const fill=k=>SRC_LV[srcSumm(k).level].map;
  // v33 지역을 누르면 패널(지도 한 곳에서 받음 — 작은 지역도 지도 전체가 누르는 곳, 지역 단추·배지는 아래에 따로)
  return `<svg class="src-svg" viewBox="${W.viewBox}" role="img" aria-label="유럽·북미·일본·중동·남미 소싱 기회 지도" onclick="srcMapTap(event)">
    <defs><pattern id="srcHatch" width="2.6" height="2.6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="2.6" stroke="var(--card)" stroke-width="0.9"/></pattern></defs>
    <rect class="mp-sea" x="${vb[0]}" y="${vb[1]}" width="${vb[2]}" height="${vb[3]}"/>
    <path class="mp-other" d="${W.other}"/>
    ${SRC_KEYS.map(k=>`<path class="mp-reg mp-click" fill="${fill(k)}" d="${W[k]}" data-k="${k}"><title>${SRC_NAMES[k]} — 눌러서 브랜드 목록</title></path>`).join('')}
    ${Object.keys(SRC_EST).filter(k=>W[k]).map(k=>`<path fill="url(#srcHatch)" d="${W[k]}" pointer-events="none"/>`).join('')}
    <path class="mp-kr" d="${W.korea}"/>
    ${W.flows.map(f=>`<path class="mp-flow" d="${f}"/>`).join('')}
    <circle cx="${K[0]}" cy="${K[1]}" r="2.2" fill="var(--map-kr)" stroke="var(--card)" stroke-width="0.6"/>
  </svg>`;
}
function srcMapTap(e){ const p=e.target&&e.target.closest?e.target.closest('[data-k]'):null; if(p) openSheet(p.dataset.k); }
function sourcingCard(){
  if(!srcModel().length) return '';
  const W=WMAP;
  let cl='';
  if(W) SRC_KEYS.forEach(k=>{
    const list=srcRanked(k), top=list.slice(0,3), lv=SRC_LV[srcSumm(k).level];
    cl+=`<button type="button" class="src-cl" style="left:${W.anchors[k][0]};top:${W.anchors[k][1]}" onclick="openSheet('${k}')" aria-label="${SRC_NAMES[k]} 브랜드 목록 열기">
      <span class="bs">${top.map(o=>srcBadge(o.b.t,o.b.name,SRC_LV[o.lvl].ring)).join('')}${list.length>3?`<span class="src-more">+${list.length-3}</span>`:''}</span>
      <span class="src-pill">${SRC_NAMES[k]} · ${lv.txt}${SRC_EST[k]?'*':''}</span></button>`;
  });
  const desc=SRC_PRESET==='A'?'재고가 매출보다 빨리 늘었고 그 지역 판매가 약하면 처분 물량이 나온다고 봅니다. 현지 유통 재고와 환율도 함께 반영합니다.'
                             :'지역 성장이 빠르거나 재고가 많이 늘면 유통 물량 자체가 커진다고 봅니다. 환율도 함께 반영합니다.';
  return `<div class="card span2" id="srcCard"><h3>소싱 기회 지도 — 유럽 · 북미 · 일본 · 중동 · 남미 <span class="tag2">공시 기반</span></h3>
  <div class="src-wrap">
    <div class="src-seg"><div class="seg2">
      <button type="button" class="${SRC_PRESET==='A'?'on':''}" aria-pressed="${SRC_PRESET==='A'}" onclick="setSrcPreset('A')">재고 과잉형</button>
      <button type="button" class="${SRC_PRESET==='B'?'on':''}" aria-pressed="${SRC_PRESET==='B'}" onclick="setSrcPreset('B')">시장 확대형</button></div>
      <div class="src-desc">${desc}</div></div>
    <div class="src-mapbox"><div class="src-map">${srcMapSvg()}${cl}</div>
      <div class="src-legend"><span><i style="background:var(--lv2-map)"></i>높음</span><span><i style="background:var(--lv1-map)"></i>보통</span><span><i style="background:var(--lv0-map)"></i>낮음</span>
      <span><i style="background:var(--lv1-map);border:1px dashed var(--sub)"></i>빗금·* = 추정(합산값 차용)</span><span><i style="background:var(--map-kr);border-radius:6px"></i>한국(판매처)</span></div></div>
    <div class="src-regs">${SRC_KEYS.map(k=>{const sm=srcSumm(k), lv=SRC_LV[sm.level];
      const tops=(sm.hi.length?sm.hi:srcRanked(k)).slice(0,3).map(o=>o.b.name).join(' · ');
      return `<button type="button" onclick="openSheet('${k}')"><span class="rl"><b>${SRC_NAMES[k]}</b><span class="tops">${sm.hi.length?'기회 높음: ':'상위: '}${esc(tops)}</span></span><span class="lvw"><span class="lvchip" style="background:${lv.bg};color:${lv.fg}">${lv.txt}</span><span class="hin">기회 높음 ${sm.hi.length}곳</span></span></button>`;}).join('')}</div>
    <div class="src-btns"><button type="button" onclick="openSheet('matrix')">브랜드 × 지역 전체 표</button><button type="button" onclick="openSheet('method')">가정과 계산 방식</button><button type="button" onclick="sw('brand')">브랜드 점검표 ›</button></div>
  </div></div>`;
}
function setSrcPreset(p){ SRC_PRESET=p; const c=document.getElementById('srcCard'); if(c) c.outerHTML=sourcingCard(); if(SRC_SHEET) openSheet(SRC_SHEET,true); }   // v33 다시 열기는 기록 안 함
const SRC_RETAIL={europe:['JD.L','FRAS.L','ZAL.DE','LUXE'],namerica:['DKS','ASO','TJX','ROST','BURL'],japan:['2670.T'],middleeast:['4240.SR'],samerica:['SBFG3.SA','VULC3.SA']};
const SRC_FXMAP={europe:['EUR','GBP'],namerica:['USD'],japan:['JPY'],middleeast:['USD'],samerica:['BRL']};
const SRC_NEWSKEYS={europe:['jd','frasers','zalando','gosport'],namerica:['dks','academy'],japan:[],middleeast:['gmg','apparelgrp','alshaya','landmark','cenomi','me_retail'],samerica:['sbf','sa_retail']};
function srcRetailHtml(k){
  let h=`<div class="sh-sub">현지 유통·브랜드 재고 <span>재고가 매출보다 빨리 늘수록 처분 물량 가능성</span></div>`;
  const tks=SRC_RETAIL[k]||[];
  if(!tks.length) return h+`<div class="sh-empty">상장 유통사 없음 — 알샤야·어패럴그룹·GMG 등 대형 유통은 비상장(아래 뉴스로 보완)</div>`;
  let any=false;
  tks.forEach(t=>{
    const x=DATA.items.find(i=>i.ticker===t); if(!x) return;
    const ip=invPick(x), inv=ip.inv, rev=ip.rev; any=true;
    let chip='<span class="lvchip" style="background:var(--barbg);color:var(--sub)">미확인</span>', t3='재고 또는 매출 미공시';
    if(inv!=null&&rev!=null){ const d=inv-rev, lv=d>=5?2:(d<=-5?0:1), L=SRC_LV[lv];
      chip=`<span class="lvchip" style="background:${L.bg};color:${L.fg}">재고 ${lv===2?'무거움':(lv===0?'가벼움':'보통')}</span>`;
      t3=`재고 압력 ${ppp(d)} · ${ip.lbl}`; }
    h+=`<button type="button" class="sh-row" onclick="closeSheet();goDetail('${t}')">${srcBadge(t,x.name,'var(--line)',true)}
      <span class="bx"><span class="t1"><span>${esc(x.name)} <span class="na">${esc(flagOf(t))}</span></span>${chip}</span>
      <span class="t2">재고 ${inv!=null?pp(inv):'―'} · 매출 ${rev!=null?pp(rev):'―'}</span><span class="t3">${esc(t3)}</span></span></button>`;
  });
  return any?h:h+`<div class="sh-empty">유통사 자료 수집 전 — 다음 갱신 후 표시</div>`;
}
function srcFxHtml(k){
  let h=`<div class="sh-sub">환율 <span>현지 통화 1단위의 원화 값 · 1년 전 대비</span></div>`;
  const FXD=DATA.fx||{}; const codes=(SRC_FXMAP[k]||[]).filter(c=>FXD[c]);
  if(!codes.length) return h+`<div class="sh-empty">환율 수집 전 — 다음 갱신 후 표시</div>`;
  codes.forEach(c=>{ const f=FXD[c], ch=f.chg_pct;
    const rate=c==='JPY'?Math.round(f.rate*100).toLocaleString('ko-KR'):(f.rate>=100?Math.round(f.rate).toLocaleString('ko-KR'):f.rate.toFixed(1));
    const verdict=ch==null?'':(ch>=2?'<span class="neg">매입 부담 커짐</span>':(ch<=-2?'<span class="pos">매입 부담 줄어듦</span>':'<span class="na">비슷</span>'));
    h+=`<div class="sh-fx"><div class="t1"><span>${esc(f.name)} <span class="na">${c==='JPY'?'100엔':c}</span>${staleTag(f.stale_since)}</span><b>${rate}원</b></div>
      <div class="t3">${ch!=null?`1년 전보다 ${pp(ch)} · `:''}${f.dev_pct!=null?`1년 평균 대비 ${pp(f.dev_pct)} · `:''}${verdict}${c==='USD'&&k==='middleeast'?' · 디르함·리얄은 달러에 고정':''}${f.via?' · '+esc(f.via):''} · ${esc(f.asof||'')} 기준</div></div>`; });
  return h;
}
const SRC_CBMAP={europe:'eu',namerica:'us',japan:'jp'};   // v31 지역 → 해외직구 나라
function srcCbHtml(k){
  const ck=SRC_CBMAP[k]; if(!ck) return '';
  const CB=KR&&KR.cross_border;
  let h=`<div class="sh-sub">한국 소비자 직구 <span>이 지역 → 한국 의류·패션 · 전년 같은 분기 대비</span></div>`;
  if(!CB||!CB.series) return h+`<div class="sh-empty">해외직구 자료 수집 전 — 다음 갱신 후 표시</div>`;
  const s=CB.series[ck+'|fashion'], v=s&&s.values?s.values[CB.last]:null, y=s&&s.yoy?s.yoy[CB.last]:null;
  if(v==null) return h+`<div class="sh-empty">이 지역 자료 없음</div>`;
  const nm=((CB.names||{})[ck+'|fashion']||'').split(' / ')[0]||SRC_NAMES[k];
  return h+`<button type="button" class="sh-fx" onclick="closeSheet();goMore('cb')"><span class="t1"><span>${esc(nm)}</span><b>${cbMoney(v)}원</b></span>
    <span class="t3">${y!=null?`${pp(y)} · `:''}${cbPrd(CB.last)} · 누르면 더보기 › 해외직구</span></button>`;
}
function srcNewsHtml(k){
  let h=`<div class="sh-sub">현지 유통 뉴스 <span>최근 14일 선별</span></div>`;
  const keys=SRC_NEWSKEYS[k]||[];
  const list=((NEWS&&NEWS.items)||[]).filter(it=>it.scope==='brand'&&keys.indexOf(it.key)>=0)
    .sort((a,b)=>(b.first_seen||'').localeCompare(a.first_seen||'')||(b.importance||0)-(a.importance||0));
  const list3=newsDedupe(list,3);
  if(!list3.length) return h+`<div class="sh-empty">최근 14일 선별된 뉴스 없음</div>`;
  list3.forEach(it=>{ h+=`<div class="nitem"><div class="nsum"><span class="stars">${'★'.repeat(Math.max(1,Math.min(3,it.importance||1)))}</span> <a href="${esc(safeUrl(it.link))}" target="_blank" rel="noopener">${esc(it.summary||it.title)}</a></div>
    <div class="nmeta">${[it.label,it.source,newsDay(it)].filter(Boolean).map(esc).join(' · ')}</div></div>`; });
  return h;
}
function openSheet(kind,quiet){   // v33 A안: 열 때 기록 1개(휴대폰 뒤로로 닫힘) · quiet = 기록 없이(뒤로 복원·가정 전환)
  if(!SRC_NAMES[kind]&&kind!=='matrix'&&kind!=='method') return;
  const sh=document.getElementById('sheet'); if(!sh) return;
  SRC_SHEET=kind;
  let title='', chip='', body='';
  if(SRC_NAMES[kind]){
    const sm=srcSumm(kind), lv=SRC_LV[sm.level];
    title=`${SRC_NAMES[kind]} 브랜드`; chip=`<span class="lvchip" style="background:${lv.bg};color:${lv.fg}">기회 ${lv.txt}</span>`;
    if(kind==='middleeast') body+=`<div class="sh-warn">중동은 대부분 브랜드가 유럽·중동·아프리카 또는 신흥시장으로 묶어 공시합니다. 그 합산값을 빌려 쓴 추정치입니다.</div>`;
    if(kind==='japan') body+=`<div class="sh-warn">일본을 따로 공시하는 곳은 아식스뿐이고, 아디다스는 일본+한국 합산입니다. 나머지는 아시아·태평양 합산값을 빌려 쓴 추정치입니다.</div>`;
    body+=`<div class="note" style="margin:2px 0 8px"><b>기회 ${lv.txt} (${sm.score}점)</b> — ${sm.parts.map(p=>`${esc(p.txt)}${p.pt?` ${p.pt>0?'+':'−'}${Math.abs(p.pt)}`:''}`).join(' · ')}</div>`;   // '판정'은 브랜드 용어라 '기회'
    srcRanked(kind).forEach(o=>{ const l=SRC_LV[o.lvl], c=o.c;
      const t2=SRC_PRESET==='A'?`${c.rname} ${pp(c.g)}(${c.basis}) · 재고 ${pp(o.b.inv)} vs 매출 ${pp(o.b.rev)}(${o.b.invLbl})`:`${c.rname} ${pp(c.g)} · 재고 ${pp(o.b.inv)}(${o.b.invLbl})`;
      const t3=(SRC_PRESET==='A'?'근거: '+c.why:'기준: '+o.b.period)+(c.proxy&&c.proxy.indexOf('차용')>=0?' · 추정(유럽·중동·아프리카 값 차용)':(c.proxy&&kind!=='europe'?' · '+c.proxy:''));
      body+=`<button type="button" class="sh-row" onclick="closeSheet();goDetail('${o.b.t}')">${srcBadge(o.b.t,o.b.name,l.ring,true)}
        <span class="bx"><span class="t1"><span>${esc(o.b.name)}</span><span class="lvchip" style="background:${l.bg};color:${l.fg}">${l.txt}</span></span>
        <span class="t2">${esc(t2)}</span><span class="t3">${esc(t3)}</span></span></button>`; });
    body+=srcRetailHtml(kind)+srcFxHtml(kind)+srcCbHtml(kind)+srcNewsHtml(kind);
  } else if(kind==='matrix'){
    title='브랜드 × 지역';
    body=`<div class="note" style="margin:2px 0 6px">칸 = 지역 성장률(환율 제외 우선) · 색 = 선택한 가정의 기회 수준 · 한국 수요 = 한국이 속한 지역 성장률</div>
    <div class="tblwrap" tabindex="0" role="region" aria-label="브랜드 × 지역 표 — 좌우로 넘겨 보기"><table id="srcTbl"><tr><th>브랜드</th>${SRC_KEYS.map(k=>`<th>${SRC_NAMES[k]}</th>`).join('')}<th>한국 수요</th></tr>`;   // v33 머리글 = SRC_KEYS(행과 같은 7칸)
    srcModel().forEach(b=>{
      body+=`<tr><td>${logoImg(b.t,false,b.name)}${esc(b.name)}<div class="ref">${esc(b.period)}</div></td>`;
      SRC_KEYS.forEach(k=>{ const c=b.cells[k];
        if(!c){ body+=`<td><div class="cv" style="background:var(--barbg);color:var(--sub)">―<small>자료 없음</small></div></td>`; return; }
        const l=SRC_LV[c[SRC_PRESET]], bor=c.proxy&&c.proxy.indexOf('차용')>=0;
        body+=`<td><div class="cv" style="background:${l.bg};color:${l.fg};${bor?'border:1px dashed var(--sub)':''}">${pp(c.g)}<small>${bor?l.txt+' · 추정':l.txt}</small></div></td>`; });   // 추정 칸도 수준 글자(색만으로 구분하지 않게)
      const kr=b.kr, kv=kr?(kr.cn!=null?kr.cn:kr.yoy):null;
      body+=`<td>${kv!=null?fmt(kv,1,true):'―'}<div class="ref">${kr?(kr.cn!=null?'환율 제외':'보고 통화'):''}</div></td></tr>`;
    });
    body+=`</table></div>`;
  } else if(kind==='method'){
    title='가정과 계산 방식';
    body=`<div class="sh-mt"><b>재고 과잉형 (보완안)</b><p>브랜드 재고 증가율이 같은 기간 매출 증가율보다 5%p 이상 높고(재고 압력 — 분기 자료가 있으면 최근 분기 vs 1년 전 같은 분기, 없으면 연간 결산), 그 지역이 역성장하거나 +10% 미만이면서 브랜드의 지역 중 하위권이면 높음. 둘 중 하나만 맞으면 보통.</p>
      <b>시장 확대형 (원안)</b><p>지역 성장률 +15% 이상 또는 브랜드 재고 증가 +15% 이상이면 높음, +5% 이상이면 보통.</p>
      <b>지도 배지</b><p>지역마다 기회 수준이 높은 순으로 최대 3개 브랜드를 표시하고 나머지는 +숫자로 묶습니다. 테두리 색이 기회 수준이며, 브랜드를 누르면 기업 상세로 이동합니다.</p>
      <b>지역 판정 (지도 색·지역 칩)</b><p>점수 = 기회 높은 브랜드 수(최대 2점) + 현지 유통 재고(재고 과잉형만: "무거움"인 유통사가 하나라도 있으면 +1, 모두 "가벼움"이면 −1) + 환율(현지 통화 원화 값이 1년 전보다 평균 2% 이상 내리면 매입 부담이 줄어 +1, 2% 이상 오르면 −1). 3점 이상 높음, 1~2점 보통, 0점 이하 낮음. 지역 패널 맨 위에 점수 내역을 표시합니다.</p>
      <b>현지 유통사·환율·뉴스</b><p>유통사는 재고 증가율이 매출 증가율보다 5%p 이상 높으면 "무거움"(처분 물량 가능성), 5%p 이상 낮으면 "가벼움". 환율은 현지 통화 1단위의 원화 값 1년 변동입니다(북미는 달러, 일본은 엔(100엔 단위 표시), 중동은 달러 고정 통화라 달러로 대신). 뉴스는 참고 정보로만 붙입니다.</p>
      <b>데이터 한계</b><p>지역별 재고는 공시되지 않아 브랜드 전체 재고를 씁니다. 국가가 아닌 지역 단위이며, 중동은 유럽·중동·아프리카 또는 신흥시장 합산값을 빌려 쓰고 상장 유통사도 없어 뉴스로 보완합니다.</p></div>`;
  } else return;
  sh.innerHTML=`<button type="button" class="sh-bd" tabindex="-1" aria-hidden="true" onclick="dismissSheet()"></button>
    <div class="sh-pn" role="dialog" aria-modal="true" aria-label="${title}"><div class="sh-grip"></div>
    <div class="sh-hd"><div class="sh-tt">${title} ${chip}</div><button type="button" class="sh-x" aria-label="닫기" onclick="dismissSheet()">${ic('close',22)}</button></div>${body}</div>`;
  sh.classList.add('on'); sheetInert(true);
  if(!quiet){ if(!SHEET_FROM||!sh.contains(document.activeElement)) SHEET_FROM=document.activeElement; sheetPush(kind); const x=sh.querySelector('.sh-x'); if(x) x.focus({preventScroll:true}); }   // v33 열면 닫기 단추로 초점(키보드·화면 읽기)
}
let SHEET_FROM=null;   // 패널을 연 단추 — 닫기·Esc·배경으로 닫으면 초점을 돌려줌
function closeSheetRaw(){ SRC_SHEET=null; sheetInert(false); const sh=document.getElementById('sheet'); if(sh){ sh.classList.remove('on'); sh.innerHTML=''; } }
function sheetInert(on){ document.querySelectorAll('#content,nav.tabs').forEach(el=>el.toggleAttribute('inert',on)); }   // v33 패널이 열린 동안 뒤 화면은 초점·누르기 없음
const sheetScrollY=()=>{ const pn=document.querySelector('#sheet .sh-pn'); return pn?pn.scrollTop:0; };   // 패널 안 스크롤(유럽 패널은 화면보다 김)
function sheetScrollTo(y){ const pn=document.querySelector('#sheet .sh-pn'); if(pn&&y>0) pn.scrollTop=y; }
/* v33 A안: 패널 안 이동(closeSheet();goDetail()) — 닫은 패널과 그 안 스크롤을 기억했다가 그 화면 기록에 저장 → 뒤로 오면 같은 패널을 같은 자리로 다시 엶.
   이어서 이동하지 않으면(코드에서 그냥 닫기) 기억은 바로 지움 */
function closeSheet(){
  if(SRC_SHEET){ LAST_SHEET=SRC_SHEET; LAST_SHEET_Y=sheetScrollY(); SHEET_FOCUS=focusDesc(document.activeElement); Promise.resolve().then(()=>{ LAST_SHEET=null; SHEET_FOCUS=null; }); }   // SHEET_FOCUS = 패널 안 누른 줄(뒤로 오면 초점)
  closeSheetRaw();
  const s=history.state; if(s&&s.sheet) hRep({...s,sheet:null});
}
function dismissSheet(){   // 닫기·배경·Esc: 패널 기록이면 뒤로(기록도 같이 닫힘), 아니면 그냥 닫기
  const s=history.state, f=SHEET_FROM; LAST_SHEET=null; SHEET_FROM=null; closeSheetRaw();
  if(f&&f.isConnected&&f.offsetParent!==null) try{ f.focus({preventScroll:true}); }catch(e){}
  if(s&&s.sheet) histBack();
}
/* v33 키보드: Esc = 패널 닫기 · role="button"인 div(네이버 줄·순위 막대·국내 지표 카드·달력 날짜)와 누르는 표 줄(tr tabindex)은 Enter·Space로 누름 */
document.addEventListener('keydown',e=>{
  if(e.key==='Escape'&&SRC_SHEET){ e.preventDefault(); dismissSheet(); return; }
  if(e.key==='Tab'&&SRC_SHEET){   // v33 패널 안에서만 돌기(inert를 모르는 옛 브라우저 포함)
    const pn=document.querySelector('#sheet .sh-pn'), f=pn?[...pn.querySelectorAll('a[href],button,input,select,textarea,[tabindex="0"]')].filter(x=>!x.disabled&&x.getClientRects().length):[];
    if(f.length){ const a=f[0], z=f[f.length-1], c=document.activeElement; if(!pn.contains(c)||c===(e.shiftKey?a:z)){ e.preventDefault(); (e.shiftKey?z:a).focus(); } }
    return;
  }
  const t=e.target;
  if((e.key==='Enter'||e.key===' ')&&t&&t.matches&&t.matches('[role="button"]:not(button),tr[tabindex="0"]')){ e.preventDefault(); t.click(); }
});

/* ── 수집 상태 (v27) — 열람 시점 기준으로 지연 판정 ── */
function statusRows(){
  const now=Date.now();
  return ((STATUS&&STATUS.sources)||[]).map(s=>{
    const age=s.ts?(now-new Date(s.ts).getTime())/86400000:null;
    return {...s, age, late:(age==null||age>s.limit)};
  });
}
function statusCard(){
  const rows=statusRows();
  let h=`<div class="card" id="statusCard"><h3>자료별 마지막 갱신</h3><table id="statusTbl"><tr><th>자료</th><th>마지막 갱신</th><th>주기</th><th>상태</th></tr>`;
  rows.forEach(r=>{
    const when=r.ts?(r.ts.slice(5,7)+'/'+r.ts.slice(8,10)+(r.date_only?'':' '+r.ts.slice(11,16))):'―';   // 기록된 한국 시각 그대로
    const dd=r.ts?Math.round((new Date(kstToday()+'T00:00:00Z')-new Date(r.ts.slice(0,10)+'T00:00:00Z'))/86400000):null;   // 한국 날짜 차(24시간 안이라도 날짜가 다르면 '어제')
    const ageTxt=dd==null||isNaN(dd)?'':(dd<=0?'오늘':dd===1?'어제':`${dd}일 전`);
    h+=`<tr><td>${esc(r.label)}<div class="ref">${esc(r.wf)}</div></td><td>${when}<div class="ref">${ageTxt}</div></td><td>${esc(r.cadence)}</td>
      <td>${r.late?'<span class="st-late">● 지연</span>':'<span class="st-ok">● 정상</span>'}${r.failed?`<div class="ref"><span class="stl" style="margin-left:0">일부 실패 ${r.failed}곳${(r.notes||[]).length?'':'(이전 값)'}</span></div>`:''}${(r.notes||[]).length?`<div class="ref" style="white-space:normal">${(r.notes||[]).map(esc).join(' · ')}</div>`:''}</td></tr>`;
  });
  h+=`</table><div class="note">지연 = 주기보다 오래 갱신되지 않음 → GitHub Actions에서 해당 워크플로우 실행 기록 확인 · 일부 실패 = 그날 못 받은 항목 — 이전 값이 있으면 그대로 보여 줌(해당 종목·환율에 '이전 값(날짜)' 표시), 없으면 '값 없음'</div>`;
  // v33.2 판정 기록 비교에서 뺀 브랜드 — 화면 판정과 기록(파이썬)이 다르거나 기록 모양이 틀림 → 판정 규칙 두 곳(build_dashboard JS·파이썬) 확인
  try{ const sk=chkHist().skip; if(sk.length) h+=`<div class="note"><span class="stl" style="margin-left:0">판정 기록 비교 제외 ${sk.length}곳</span> ${esc(sk.join(', '))} — 화면 판정과 기록이 다르거나 기록 모양이 틀려 '어제와 달라진 판정'에서 뺌(판정 규칙 두 곳 확인 필요)</div>`; }catch(e){ console.error('[수집 상태 · 판정 기록] 확인 실패:',e); }
  h+=`</div>`;
  return h;
}
const usdTxt=v=>(v>0&&v<0.01)?'<$0.01':'$'+Number(v||0).toFixed(2);   // Claude 금액(카드·메뉴·맺음 줄 같게)
function claudeCard(){   // v32.16 이번 달 Claude 사용액 — 수집 스크립트가 저장한 월별 기록의 합
  const C=STATUS&&STATUS.claude; if(!C) return '';
  const usd=v=>v==null?'―':usdTxt(v);
  const tot=C.rows.reduce((a,r)=>a+(r.usd||0),0), hasPrev=C.rows.some(r=>r.prev!=null), ptot=C.rows.reduce((a,r)=>a+(r.prev||0),0);
  const k=krwOf(tot,'USD'), mm=+C.month.slice(5,7), pm=+C.prev.slice(5,7), since=C.rows.some(r=>r.since||r.prev_since), psin=C.rows.some(r=>r.prev_since);
  let h=`<div class="card" id="claudeCard"><h3>Claude 사용액 — ${mm}월</h3>
    <div class="cl-tot"><b>${usd(tot)}</b>${k!=null?` <span class="na">≈ ${Math.round(k).toLocaleString()}원</span>`:''}${hasPrev?` <span class="na">· ${pm}월 ${usd(ptot)}${psin?'(일부)':''}</span>`:''}</div>
    <table id="claudeTbl"><tr><th>작업</th><th>${mm}월</th><th>호출</th>${hasPrev?`<th>${pm}월</th>`:''}</tr>`;
  C.rows.forEach(r=>{
    h+=`<tr><td>${esc(r.label)}<div class="ref">${esc(r.cad)}</div></td><td>${r.rec?usd(r.usd||0):'<span class="na">기록 전</span>'}${r.since?`<div class="ref">${r.since.slice(5).replace('-','/')}부터</div>`:''}</td><td>${r.rec?(r.calls||0)+'회':''}</td>${hasPrev?`<td>${usd(r.prev)}${r.prev_since?`<div class="ref">${r.prev_since.slice(5).replace('-','/')}부터</div>`:''}</td>`:''}</tr>`;
  });
  return h+`</table><div class="note">GitHub 워크플로우가 부른 Claude API 사용량(응답 토큰 × 공식 가격)으로 계산한 추정치${since?` · 'MM/DD부터' = 그날 기록 시작(그 전 사용은 빠짐)`:''} · Claude 앱 세션(점검·작업)과 작업 브랜치 시험 실행은 빠짐 · 정확한 청구액은 Anthropic Console(Usage)</div></div>`;
}
function claudeMonthTxt(){   // 더보기 메뉴 줄용 '10월 Claude $1.23'
  const C=STATUS&&STATUS.claude; if(!C) return '';
  const tot=C.rows.reduce((a,r)=>a+(r.usd||0),0);
  return ` · <span class="nw">${+C.month.slice(5,7)}월 Claude ${esc(usdTxt(tot))}</span>`;
}
function statusWarn(){   // v33 오늘 맨 위 수집 지연 띠(지연 있을 때만) — 누르면 더보기 › 수집 상태
  const el=document.getElementById('statusWarn'); if(!el) return;
  const late=statusRows().filter(r=>r.late);
  el.innerHTML=late.length?
    `<button type="button" class="warnbar" data-go="more:status">${ic('alert',20)}<span>수집 지연: ${late.map(r=>`${esc(r.label)} ${r.age==null?'자료 없음':Math.floor(r.age)+'일'}`).join(' · ')} — 눌러서 확인</span></button>`:'';
}

/* 같은 기사가 출처만 달리 여러 번 잡히면 하나만 (요약 앞부분 비교) */
function newsDedupe(list, n){
  const seen=new Set(), out=[];
  for(const it of list){
    const k=(it.summary||it.title||'').replace(/[\s.,·'"“”‘’!?()\[\]~-]/g,'').slice(0,18);
    if(seen.has(k)) continue; seen.add(k); out.push(it);
    if(out.length>=n) break;
  }
  return out;
}
const newsKeyOf=key=>NEWS_KEY[key] || (String(key).startsWith('krd:') ? String(key).slice(4) : null);   // v32.7 국내 비교 회사 = DART 법인 id
function newsFor(key, n=3){
  const k = newsKeyOf(key);
  if(!k || !NEWS || !NEWS.items) return [];
  return newsDedupe(NEWS.items.filter(it=>it.scope==='brand' && it.key===k)
    .sort((a,b)=>(b.first_seen||'').localeCompare(a.first_seen||'') || (b.importance||0)-(a.importance||0)), n);
}
function newsCard(key){
  const list=newsFor(key), nk=newsKeyOf(key);
  // v33 A안: '뉴스 ›' = 시장 › 뉴스, 그 회사 뉴스만(k: 필터 — 위 3건과 같은 키). 보관 기간 안에 없으면 전체
  let h=`<div class="card"><h3>최근 뉴스 <button type="button" class="go" onclick="goNews('${list.length&&nk?'k:'+esc(nk):'all'}')">뉴스 ›</button></h3>`;
  if(!list.length){ h+=`<div class="na">보관 기간 내 선별 뉴스 없음</div></div>`; return h; }
  list.forEach(it=>{
    h+=`<div class="nitem"><div class="nsum"><span class="stars">${'★'.repeat(Math.max(1,Math.min(3,it.importance||1)))}</span> <a href="${esc(safeUrl(it.link))}" target="_blank" rel="noopener">${esc(it.summary||it.title)}</a></div>
      <div class="nmeta">${[it.source,newsDay(it)].filter(Boolean).map(esc).join(' · ')}</div></div>`;
  });
  return h+`</div>`;
}
const flagOf=t=>FLAGS[t]||(isKR(t)?'한국':'');   // v33 국기 대신 나라 이름(글자)
function logoImg(t, large, name){
  const d = DOMAINS[t];
  const cls = large ? "logo-lg" : "logo";
  const init = String(name||t).replace(/[^가-힣A-Za-z0-9]/g,'').slice(0,1) || '·';
  const fb = `<i class="lgfb ${large?'lgfb-lg':''}" style="display:none">${init}</i>`;
  if(!d) return `<span class="lg">${fb.replace('display:none','')}</span>`;
  return `<span class="lg"><img class="${cls}" loading="lazy" alt="" onerror="this.style.display='none';this.nextSibling.style.display='inline-flex'"
    src="https://www.google.com/s2/favicons?domain=${d}&sz=64">${fb}</span>`;
}

/* 테마(applyTheme·toggleTheme)는 스크립트 맨 앞(v33) */

const esc=s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;')
  .replace(/>/g,'&gt;').replace(/"/g,'&quot;');
const safeUrl=u=>/^https?:\/\//i.test(String(u||''))?String(u):'#';   // 주소는 http(s)만 — esc()와 함께
/* Claude 추출 메모 화면용 — 내부 용어(mgmt_notes·JSON·null·필드명)·영어로만 된 문장은 빼고 '(Phase …)' 지움 */
function noteClean(t){
  t=String(t||'').replace(/\s*\(Phase[^)]*\)/gi,'').replace(/본 JSON은/g,'이 화면은').replace(/null 처리됨/g,'미확인').replace(/regions\/channels/g,'지역·채널');
  return t.replace(/([.。])\s+/g,'$1\n').split('\n').map(x=>x.replace(/^[\s·,;:—-]+/,'')).filter(x=>x.trim()&&/[가-힣]/.test(x)&&!/mgmt_notes|\bJSON\b|\bnull\b|\b[a-z]+_[a-z_]+\b/i.test(x)).join(' ').trim();   // 뒤보기 정규식 없이(옛 사파리)
}
/* 기간 'Q1 FY27'·'Q1 FY2027' → 'FY27 1분기', 'Q2 2026' → ''26년 2분기' */
const perKo=p=>{ p=String(p||'').trim(); let m=p.match(/^Q([1-4])\s+FY\s?(\d{2}|\d{4})$/i); if(m) return `FY${m[2].slice(-2)} ${m[1]}분기`;
  m=p.match(/^(?:H([12])|([12])H)\s+(FY\s?)?(\d{2}|\d{4})$/i); if(m){ const h=(m[1]||m[2])==='1'?'상반기':'하반기'; return m[3]?`FY${m[4].slice(-2)} ${h}`:`'${m[4].slice(-2)}년 ${h}`; }   // v33.8 제냐 반기 실적
  m=p.match(/^Q([1-4])\s+(\d{4})$/); return m?`'${m[2].slice(2)}년 ${m[1]}분기`:p; };
const smoothB=()=>{ try{ return matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'; }catch(e){ return 'smooth'; } };
// v33 성장률·이익률 = + 파랑(pos) / − 짙은 주황(neg), 부호 항상. 보이는 자리에서 0이면 색·부호 없음(옛 '+0.0%' 초록), 음수는 '−'(U+2212)
const sgnPct=(v,d)=>{ const r=+v.toFixed(d); return [r>0?1:r<0?-1:0, Math.abs(r).toFixed(d)+'%']; };
const fmt=(v,d=1,sign=false)=>{
  if(v===null||v===undefined) return '<span class="na">―</span>';
  if(!sign) return v.toFixed(d);
  const [g,s]=sgnPct(v,d); return g>0?`<span class="pos">+${s}</span>`:g<0?`<span class="neg">−${s}</span>`:`<span>${s}</span>`;
};
// 재고 증감 — 늘면 짙은 주황(재고 부담), 줄면 파랑. 매출·이익률과 색이 반대(v32.10)
const fmtInv=(v,d=1)=>{
  if(v===null||v===undefined) return '<span class="na">―</span>';
  const [g,s]=sgnPct(v,d); return g>0?`<span class="neg">+${s}</span>`:g<0?`<span class="pos">−${s}</span>`:`<span>${s}</span>`;
};
const fmtS=(v,d=1)=>{ if(v==null) return '<span class="na">―</span>'; const [g,s]=sgnPct(v,d); return (g>0?'+':g<0?'−':'')+s; };   // 색 없이 부호만(주가 — 한국 증권 앱 색과 반대로 읽히지 않게)
/* 재무제표 통화: 야후 currency는 주가 통화라 영국 상장사는 GBp(펜스) — 재무 수치는 GBP(파운드) */
const finCur=c=>c==='GBp'?'GBP':(c||'');
const finCurOf=x=>finCur(x.fin_currency||x.currency);   // 재무제표 통화 우선(v30.1)
/* 외화 금액의 원화 근사(v30.2) — data.json fx의 최근 환율, 환율 없으면 null */
const krwOf=(v,cur)=>{ if(v==null) return null; if(cur==='KRW') return v; const f=(DATA.fx||{})[cur]; return (f&&f.rate)?v*f.rate:null; };
/* 국내 그룹의 외화 실적: "≈46.9조" + 작은 글씨로 원래 통화 */
function revKrwCell(rev,cur,short){   // short = 기업 목록(폭 좁음): 단위 '원'은 머리글로, ≈조 소수 1자리
  const k=krwOf(rev,cur), w=x=>short?x.replace(/원$/,''):x;
  if(cur==='KRW'||k==null) return w(moneyShort(rev,cur));
  return `≈${w(short&&k>=1e12?(k/1e12).toFixed(1)+'조원':moneyShort(k,'KRW'))}<span class="na" style="display:block">${short&&rev>=1e11?Math.round(rev/1e9)+'B '+cur:moneyShort(rev,cur)}</span>`;
}
const money=(v,cur)=>{   // v33 음수는 '−'(U+2212)
  if(v===null||v===undefined) return '―';
  const a=Math.abs(v), m=a/1e6;
  const t=cur==='KRW'?(a>=1e12?(a/1e12).toFixed(2)+'조원':(a/1e8).toLocaleString(undefined,{maximumFractionDigits:0})+'억원')
    :(m>=1000?(m/1000).toFixed(2)+'B '+(cur||''):m.toFixed(0)+'M '+(cur||''));
  return (v<0&&/[1-9]/.test(t)?'−':'')+t;
};
// v32.9 통화 표기: 원화는 '조원/억원', 외화는 'B USD'처럼 통화 코드를 항상 붙임(통화가 다른 금액이 같은 단위로 보이지 않게)
const moneyShort=(v,cur)=>{   // v33 음수는 '−'(U+2212)
  if(v===null||v===undefined) return '―';
  const a=Math.abs(v), m=a/1e6;
  const t=cur==='KRW'?(a>=1e12?(a/1e12).toFixed(2)+'조원':(a/1e8).toLocaleString(undefined,{maximumFractionDigits:0})+'억원')
    :(m>=1000?(m/1000).toFixed(1)+'B':m.toFixed(0)+'M')+(cur?' '+cur:'');
  return (v<0&&/[1-9]/.test(t)?'−':'')+t;
};
const curCode=c=>((String(c||'').match(/[A-Z]{3}/)||[])[0])||'';   // 'EUR millions' → 'EUR'
const segMoney=(v,cur)=>{   // 공시 추출 금액(백만 단위) · v33 음수는 '−'
  if(v===null||v===undefined) return '―';
  const a=Math.abs(v), t=(a>=1000?(a/1000).toFixed(2)+'B':a.toFixed(0)+'M')+(cur?' '+cur:'');
  return (v<0&&/[1-9]/.test(t)?'−':'')+t;
};
/* 현재가: 원·엔은 소수점 없이, 영국 펜스(GBp)는 파운드 환산 병기 */
function priceTxt(x){
  if(x.price==null) return '―';
  const c=x.currency||'';
  if(c==='GBp') return `${x.price.toFixed(2)}펜스 <span class="na">(${(x.price/100).toFixed(2)} GBP)</span>`;
  const n=(c==='KRW'||c==='JPY')?Math.round(x.price).toLocaleString():x.price.toLocaleString(undefined,{minimumFractionDigits:2,maximumFractionDigits:2});
  return `${n} ${esc(c)}`;
}
const ym=d=>d?("'"+d.slice(2,4)+"."+d.slice(5,7)):null;
function segOf(t){
  const e=(SEGS.items||{})[t];
  return (e&&e.extract)?e:null;
}
/* ── v32.12 (대표 지시 2026-10-09) 순위 기준 표시·예외 — weekly_digest.py v1.4와 같은 규칙 ── */
// 인수 효과 기간: 성장 순위·재고 경고에서 빼고 각주로(값은 기업 탭·상세에 그대로). core = 본체 부문 이름(분기 실적일 때 본체 증가율)
const ACQ={"DKS":{until:"2026-11-30",why:"풋락커 인수(2025-09) 효과 포함",core:"DICK'S"}};
// 회사 전체 수치(패션 외 사업 포함): 성장 순위·재고 경고·KPI에서 뺌(기업 탭·상세는 그대로)
const WHOLE_CO={"028260.KS":"삼성물산은 건설·상사 포함 전사 수치라 제외"};
const PEND_DAYS=45;   // 공시 분기가 야후 분기보다 이만큼 넘게 새로우면 '새 실적 반영 대기'
const kstToday=()=>new Date().toLocaleDateString('sv-SE',{timeZone:'Asia/Seoul'});
const kstMid=()=>new Date(kstToday()+'T00:00:00');   // v33 S2: 한국 날짜 자정 — D-day·세일이 머리 날짜(KST) 기준(기기 시간대 무관)
const acqOn=t=>{ const a=ACQ[t]; return a&&kstToday()<=a.until?a:null; };
const fyLbl=d=>d?'FY'+String(d).slice(2,4):'';
const nmSplit=n=>{ const m=String(n||'').match(/^(.+?)\s*\((.+)\)\s*$/); return (m&&m[2]!=='자사')?{main:m[1],brand:m[2]}:{main:String(n||''),brand:''}; };   // '에스제이그룹(캉골)' → 법인명·브랜드('트렉시(자사)'는 그대로)
const NM_NOT_BRAND=new Set(['이랜드월드','패션부문','KREAM']);   // 괄호 속이 브랜드가 아닌 이름 — 좁은 칸엔 앞 이름
const NM_KO={HOKA:'호카'};   // 화면용 브랜드 이름(브랜드 탭과 같게)
const nmBrand=n=>{ const s=nmSplit(n), b=(s.brand&&!NM_NOT_BRAND.has(s.brand))?s.brand:s.main; return NM_KO[b]||b; };   // 아주 좁은 칸(순위 막대·KPI·달력)은 브랜드만
const mdOf=d=>d?`${d.slice(5,7)}/${d.slice(8,10)}`:'';
const staleTag=d=>d?`<span class="stl" title="${esc(d)} 수집분 — 그 뒤 수집 실패">이전 값(${mdOf(d)})</span>`:'';
// 오늘 수집 실패 + 이전 값도 없는 종목(fetch_data v4.12 fetch_status.failed)
const failTag=t=>(((DATA.fetch_status||{}).failed)||[]).includes(t)?'<span class="stl" title="오늘 수집 실패 — 이전 값 없음">값 없음</span>':'';
const MON3={jan:1,feb:2,mar:3,apr:4,may:5,jun:6,jul:7,aug:8,sep:9,oct:10,nov:11,dec:12};
function periodEnd(p){   // 공시 기간 문자열의 종료일 'ended 2026-08-31' / 'ended August 1, 2026' → 'YYYY-MM-DD' (없거나 실적 기간이 아니면 null)
  p=String(p||''); if(/pro ?forma|target|investor/i.test(p)) return null;
  let m=p.match(/ended\s+(\d{4}-\d{2}-\d{2})/i); if(m) return m[1];
  m=p.match(/ended\s+([A-Za-z]{3})[a-z]*\.?\s+(\d{1,2}),?\s+(\d{4})/i);
  const mo=m&&MON3[m[1].toLowerCase()];
  return mo?`${m[3]}-${String(mo).padStart(2,'0')}-${m[2].padStart(2,'0')}`:null;
}
function pendOf(x){   // 야후 분기(q_end)보다 공시(SEC·IR) 분기 종료일이 45일 넘게 새로우면 {end, src} — 값은 그대로 두고 표시만
  if(!x||!x.q_end) return null;
  let best=null;
  [[SEGS_SEC[x.ticker],'SEC'],[((SEGS_IR&&SEGS_IR.items)||{})[x.ticker],'IR']].forEach(([e,src])=>{
    const d=(e&&e.extract)?periodEnd(e.extract.period):null;
    if(d&&(!best||d>best.end)) best={end:d,src};
  });
  return (best&&(new Date(best.end)-new Date(x.q_end))/86400000>PEND_DAYS)?best:null;
}
// 기간 문구의 첫 구절만 봄 — 'Q2 … (13 weeks); also 26 weeks …'처럼 분기와 누적을 함께 적은 추출(딕스)도 분기로(v32.13)
const isQtrPeriod=p=>{ const q=String(p||'').split(/;|\balso\b/i)[0];
  return /\bQ[1-4]\b|quarter|thirteen weeks|13 weeks|three months|분기/i.test(q)&&!/pro ?forma|누적|six months|nine months|26 weeks|39 weeks|twenty-six|thirty-nine/i.test(q); };
function acqCore(t){   // 인수 회사의 본체 매출 증가율 — 공시 추출이 분기 실적이고 본체 부문에 당기·전년 매출이 있을 때만
  const a=ACQ[t], s=segOf(t), ex=s&&s.extract; if(!a||!ex||!isQtrPeriod(ex.period)) return null;
  const c=(ex.sub_segments||[]).find(z=>z.name===a.core);
  return (c&&c.revenue!=null&&c.prev_revenue)?(c.revenue/c.prev_revenue-1)*100:null;
}
const pendTag=p=>p?`<span class="wait-b" title="${esc(p.src)} 공시 ${esc(p.end)} 분기 발표됨 — 야후 미반영, 값은 이전 분기">새 실적 반영 대기</span>`:'';
// v33 A안 새 화면(오늘·브랜드·브랜드 상세)용 꼬리표(13px) — 이전 값 · 새 실적 반영 대기 · 오래된 자료
const tagA=(t,title)=>`<span class="tg"${title?` title="${esc(title)}"`:''}>${esc(t)}</span>`;
const staleA=d=>d?tagA(`이전 값(${mdOf(d)})`,`${d} 수집분 — 그 뒤 수집 실패`):'';
const pendA=p=>p?tagA('새 실적 반영 대기',`${p.src} 공시 ${p.end} 분기 발표됨 — 야후 미반영, 값은 이전 분기`):'';

/* ── 공통: 기업 행 데이터(상장 41 + 국내 법인) ── */
// 유통사 비교 카드(와 상세)에만 보이는 법인 — 기업 목록·종합·플랫폼 카드에서 제외(대표 요청 2026-10-05, 나중에 합칠 때 여기서 삭제)
const PEER_ONLY=new Set(['krd:trexi']);
/* v32.14 재고 증감은 같은 기간끼리(대표 지시 2026-10-10): 분기 재고와 같은 분기 매출이 모두 있으면
   '최근 분기 vs 1년 전 같은 분기'(fetch_data v4.13), 없으면 연간 결산끼리. lbl = 화면에 붙이는 비교 기간 */
function invPick(x){
  const fy=x.fy&&x.fy.length?x.fy[x.fy.length-1]:{};
  if(x.q_inv_yoy!=null&&x.q_inv_rev_yoy!=null&&!x.yahoo_cfs_diff)
    return {inv:x.q_inv_yoy, rev:x.q_inv_rev_yoy, q:true, end:x.q_inv_date, lbl:`분기 ${ym(x.q_inv_date)} vs ${ym(x.q_inv_prev_date)}`};
  return {inv:x.inv_yoy, rev:fy.rev_yoy, q:false, end:x.inv_date, lbl:x.inv_date?`결산 ${ym(x.inv_date)}${x.inv_prev_date?' vs '+ym(x.inv_prev_date):''}`:'연간'};
}
function rows_all(){
  const out=[];
  DATA.items.forEach(x=>{
    const fy=x.fy.length?x.fy[x.fy.length-1]:{};
    out.push({key:x.ticker, name:x.name, group:x.group, logo:logoImg(x.ticker,false,x.name), listed:true,
      rev:fy.rev, cur:finCurOf(x), rev_yoy:fy.rev_yoy, gm:fy.gm_pct, q_yoy:x.latest_q_yoy, dio:dioOf(x.inventory,fy.rev,fy.gp,null),
      ...(ip=>({inv_yoy:ip.inv, inv_rev:ip.rev, inv_q:ip.q, inv_end:ip.end, inv_lbl:ip.lbl}))(invPick(x)), earn:x.earn_date, note:x.note, item:x,
      q_end:x.q_end||null, fy_end:fy.end||null, stale:x.stale_since||null, pend:pendOf(x)});   // v32.12 기준 표시·이전 값·반영 대기
  });
  ((KRD&&KRD.entities)||[]).filter(e=>!PEER_ONLY.has('krd:'+e.id)).forEach(e=>{
    const ys=(e.years||[]).filter(y=>y.rev!=null); const last=ys[ys.length-1], prev=ys[ys.length-2];
    const yoy=(last&&prev&&prev.rev)?(last.rev/prev.rev-1)*100:null;
    const opm=(last&&last.op!=null&&last.rev)?last.op/last.rev*100:null;
    const gmk=(last&&last.cogs!=null&&last.rev)?(last.rev-last.cogs)/last.rev*100:null;
    const invy=(last&&prev&&last.inv&&prev.inv)?(last.inv/prev.inv-1)*100:null;
    const diok=last?dioOf(last.inv,last.rev,null,last.cogs):null;
    out.push({key:'krd:'+e.id, name:e.name, group:'국내 법인', logo:logoImg('krd:'+e.id,false,e.name), listed:false,
      rev:last?last.rev:null, cur:'KRW', rev_yoy:yoy, gm:gmk, opm, q_yoy:null, inv_yoy:invy, earn:null, dio:diok,
      inv_rev:yoy, inv_q:false, inv_end:last?last.end:null, inv_lbl:last?`결산 ${ym(last.end)}${prev?' vs '+ym(prev.end):''}`:'연간',
      note:e.note, route:e.route, std:e.acct_std||null, fy_end:last?last.end:null});
  });
  return out;
}
const CO_GROUPS = [...GROUPS, '국내 법인'];

/* ── 종합 (A안: 신호) ── */
/* ── v33 A안 S2: 오늘 = 수집 지연 띠 + 결정 카드 4장(① 매입 검토 ② 환율 타이밍 ③ 다가오는 일정 ④ 오늘 중요 뉴스) + 트렉시 위치 + 맺음 줄 ──
   모두 이미 페이지에 있는 값(chkModel·DATA.fx·fx_push·saleAll·NEWS·fiScore·STATUS)만 씀. '오늘'·D-day·지연은 보는 사람의 한국 날짜·시각 기준 */
function todayModel(){
  const out={fail:{}}, today=kstMid();
  const kst=kstToday(), g=String(DATA.generated_at||''), dataDay=g.slice(0,10);
  // 카드마다 따로 계산 — 한 카드(또는 트렉시·맺음 줄)가 실패해도 나머지는 그림(실패한 카드만 그 자리에 안내 한 줄 — todayHtml)
  const calc=(k,fn)=>{ try{ out[k]=fn(); }catch(e){ console.error('[오늘 볼 것 · '+k+'] 계산 실패:',e); out[k]=null; out.fail[k]=1; } };
  let M=null; try{ M=chkModel(); }catch(e){ console.error('[오늘 볼 것 · 점검표] 계산 실패:',e); }
  // ① 매입 검토 — 지금 검토 → 주의 순(점검표 정렬 그대로) 최대 4줄
  calc('buy',()=>{
    if(!M) throw new Error('점검표 모델 없음');
    const gos=M.main.filter(r=>r.lv===2), warn=M.main.filter(r=>r.lv===0), hold=M.main.filter(r=>r.lv===1);
    const holdByDem=hold.slice().sort((a,c)=>((c.dem.rel??-999)-(a.dem.rel??-999)));   // 관망 중 국내 검색이 강한 순(끝 줄 이름)
    const pick=[...gos,...warn];
    if(!M.main.length) return M.rest.length?{n:0,empty:'판정할 브랜드 없음',emptySub:`본사 재고·발언 자료 수집 전 — 판정 안 함 ${M.rest.length}곳은 점검표에서 검색·환율만`,more:`판정 안 함 ${M.rest.length}곳`}
      :{n:0,empty:'네이버 검색 자료 수집 전'};
    // v33.2 어제와 달라진 판정(판정 기록이 있을 때) — 계산이 실패해도 카드는 그대로
    // 한 줄(넘치면 …, 전체는 title) — 한 곳이면 바뀐 점수까지, 두 곳이면 판정만, 세 곳 이상이면 이름만 4곳까지(꼬리표·상세에 판정·점수) — 첫 화면에서 ②가 덜 밀리게.
    // 지금 검토·주의로 바뀐 곳 먼저
    let chg=null; try{ const C=chkHist(), pri=c=>(c.to===2||c.to===0)?0:1, L=C.list.slice().sort((a,c)=>pri(a)-pri(c)), k=L.length, mx=k>2?4:2;
      if(C.prev) chg={vs:chkLbl(C).vs, n:k, list:L.slice(0,mx).map(c=>k===1?chkChgTxt(c):k===2?`${c.name} ${lvT(c.from)} → ${lvT(c.to)}`:c.name), sep:k>2?'·':' · ', more:Math.max(0,k-mx), skip:C.skip.length,
        full:L.map(chkChgTxt).join(' · ')}; }catch(e){ console.error('[오늘 볼 것 · 판정 기록] 비교 실패:',e); }
    return {n:M.main.length, chg,
      head:pick.length?`지금 검토 ${gos.length}곳 · 주의 ${warn.length}곳`:`오늘은 지금 검토·주의 없음 · 관망 ${hold.length}곳`,
      rows:(pick.length?pick.slice(0,4):hold.slice(0,2)).map(r=>({name:r.b.name, lv:r.lv, why:chkWhy(r).short,
        hint:pick.length?'':(r.dem.pt>=0?`지금 검토까지 매입 조건 +${2-r.buy}`:'국내 수요 약함')})),
      more:pick.length>4?`외 ${pick.length-4}곳 · 관망 ${hold.length}곳`
        :(hold.length?`관망 ${hold.length}곳 · ${holdByDem.slice(0,3).map(r=>r.b.name).join(', ')}${hold.length>3?` 외 ${hold.length-3}곳`:''}`:`판정 안 함 ${M.rest.length}곳`)};
  });
  // ② 환율 타이밍 — 감시 통화(엔·유로·달러) 중 1년 평균 대비 가장 싼 통화가 큰 숫자, 나머지 둘 + 파운드(v33.2 1년 평균 대비 · 없으면 1년 전 대비)
  calc('fx',()=>{
    const FXD=DATA.fx||{}, fxs=FX_ALERT.map(c=>({c,f:FXD[c]})).filter(o=>o.f&&o.f.rate&&o.f.dev_pct!=null);
    const fxNm=o=>o.c==='JPY'?'엔(100엔)':(o.f.name||o.c);
    if(!fxs.length) return {empty:'환율 수집 전 — 다음 갱신 후 표시'};
    const h=fxs.slice().sort((a,c)=>a.f.dev_pct-c.f.dev_pct)[0], others=[...fxs.filter(o=>o!==h), ...(FXD.GBP&&FXD.GBP.rate?[{c:'GBP',f:FXD.GBP}]:[])];
    const rows=others.map(o=>{ const dv=o.f.dev_pct!=null, v=dv?o.f.dev_pct:o.f.chg_pct;
      return {name:fxNm(o), value:wonR(o.f.rate*fxMul(o.c))+'원', diff:v==null?'―':`${dv?'1년 평균':'1년 전'}보다 ${p1(v)}% ${v<0?'쌈':'비쌈'}`, tone:v==null?'':(v<0?'t-p':'t-n'), stale:o.f.stale_since||null}; });
    const asof=[h,...others].map(o=>o.f.asof).filter(Boolean).sort();
    const nB=M?[...M.main,...M.rest].filter(r=>r.cur===h.c):[], ptH=chkFx(h.c).pt;   // 점검표가 실패해도 환율은 그림(브랜드 줄만 빠짐)
    const push=(DATA.fx_push&&DATA.fx_push.items)||[], la=fxAlertsAll()[0];
    return {asof:asof.length?(asof[0]===asof[asof.length-1]?mdTxt(asof[0]):`${mdTxt(asof[0])}~${mdTxt(asof[asof.length-1])}`)+' 기준':'',
      hero:{name:fxNm(h), value:wonR(h.f.rate*fxMul(h.c))+'원', dev:`1년 평균보다 ${p1(h.f.dev_pct)}% ${h.f.dev_pct<0?'쌈':'비쌈'}`, tone:h.f.dev_pct<0?'t-p':'t-n',
        chg:h.f.chg_pct!=null?`1년 전보다 ${p1(h.f.chg_pct)}% ${h.f.chg_pct<0?'쌈':'비쌈'}`:'', stale:h.f.stale_since||null,
        brands:nB.length>1?`${h.f.name} 원산지 감시 브랜드 ${nB.length}곳 모두 환율 점수 ${sg0(ptH)}`:(nB.length?`${h.f.name} 원산지 감시 브랜드 ${nB[0].b.name} 환율 점수 ${sg0(ptH)}`:'')},
      rows,
      // 새 알림 = 휴대폰 알림과 같은 기준(DATA.fx_push — 처음 잡힌 날 first_seen, fetch_data가 만듦)
      alert:push.length?{n:push.length, day:(DATA.fx_push.date===kst?'오늘':mdTxt(DATA.fx_push.date)), list:push.map(a=>fxAlertTxt({...a,c:a.code}))}
        :{n:0, day:(!dataDay||dataDay===kst?'오늘':mdTxt(dataDay)), last:la?`마지막 알림 ${mdTxt(la.date)} ${fxAlertTxt(la)}`:'지난 1년 알림 없음'}};
  });
  // ③ 다가오는 일정 — 점검표 감시 브랜드의 상장 본사 실적(0~90일, 같은 날 묶어 앞 2묶음) + 해외 세일(150일 안, 같은 시작일 묶어 앞 2묶음)
  calc('events',()=>{
    const nvBy={}; nvAll().filter(b=>b.group==='global'&&b.link&&!String(b.link).startsWith('krd:')).forEach(b=>{ (nvBy[b.link]=nvBy[b.link]||[]).push(b.name); });
    const eg={}; DATA.items.filter(x=>nvBy[x.ticker]&&x.earn_date).forEach(x=>{ const dd=new Date(x.earn_date+'T00:00:00'), dn=Math.round((dd-today)/86400000);
      if(!(dn>=0&&dn<=90)) return; (eg[x.earn_date]=eg[x.earn_date]||{dn,dd,xs:[]}).xs.push(x); });
    const earn=Object.values(eg).sort((a,c)=>a.dn-c.dn).slice(0,2).map(gr=>{
      const hq=gr.xs.map(x=>nmSplit(x.name).main), notes=[];
      gr.xs.forEach(x=>{ const bs=nvBy[x.ticker]; if(bs.some(nm=>nm!==nmSplit(x.name).main)) notes.push(`${bs.join('·')} 본사`);
        (M?M.main:[]).filter(r=>r.x&&r.x.ticker===x.ticker&&r.lv!==1).forEach(r=>notes.push(`${r.b.name} ${r.lv===2?'지금 검토 중':'주의 판정'}`)); });
      return {dn:gr.dn, d:gr.dn===0?'오늘':'D-'+gr.dn, title:`${hq.join('·')} 실적`, sub:[md2(gr.dd),...notes].join(' · '), kind:'실적', go:gr.xs.length===1?'co:'+gr.xs[0].ticker:'mk:cal:day:'+ymdL(gr.dd)}; });   // 여러 곳 = 캘린더 그 날
    const sgp={}; saleAll(today).filter(e=>e.e>=today&&Math.round((e.s-today)/86400000)<=150).forEach(e=>{ const k=+e.s; (sgp[k]=sgp[k]||[]).push(e); });
    const left=z=>{ const n=Math.round((z.e-today)/86400000); return n>0?`${n}일 남음`:'오늘 끝'; };
    const sale=Object.values(sgp).sort((a,c)=>a[0].s-c[0].s).slice(0,2).map(es=>{ const e=es[0], live=e.s<=today, dn=Math.round(((live?e.e:e.s)-today)/86400000);
      // 끝 날이 다르면 행사마다 기간·남은 날(코세페 ~11/30)
      const one=es.every(z=>+z.e===+e.e), est=z=>z.k==='예상'?' 예상':'';
      const sub=one?[`${md2(e.s)}~${md2(e.e)}`+(live?` · ${left(e)}`:''), ...es.filter(z=>z.k==='예상').map(z=>`${z.sh} 예상`)].join(' · ')
        :es.map(z=>live?`${z.sh} ~${md2(z.e)}(${left(z)})${est(z)}`:`${z.sh} ${md2(z.s)}~${md2(z.e)}${est(z)}`).join(' · ');
      return {dn:live?0:dn, d:live?'진행 중':'D-'+dn, title:es.map(z=>z.nm.replace(/\(.*?\)/g,'').trim()).join(' · '), sub, kind:'세일', go:'mk:cal:saleList'}; });
    return [...earn,...sale].sort((a,c)=>a.dn-c.dn);
  });
  // ④ 오늘 중요 뉴스 — 그날(뉴스 수집일) 처음 잡힌 ★3, 최대 3건(목록 순서)
  calc('news',()=>{
    const NI=(NEWS&&NEWS.items)||[], td=(NEWS&&NEWS.today)||'';
    if(!NI.length) return {empty:'뉴스 수집 전'};
    const dayW=(!td||td===kst)?'오늘':newsDateLbl(td), all=NI.filter(i=>i.first_seen===td), top=all.filter(i=>(i.importance||1)>=3);
    const recent=top.length?null:NI.find(i=>(i.importance||1)>=3);
    return {head:top.length?`${dayW} 중요 뉴스 ${top.length}건`:`${dayW} ★3 없음`, sub:`${dayW} ${all.length}건 중`,
      items:(top.length?top.slice(0,3):(recent?[recent]:[])).map(i=>({t:i.summary||i.title||'', link:i.link||'',
        meta:top.length?[i.label||i.key,i.source].filter(Boolean).join(' · '):[`최근 ${newsDateLbl(i.first_seen)}`,i.label||i.key].filter(Boolean).join(' · ')})),
      more:top.length>3?top.length-3:0, none:!top.length&&!recent};
  });
  // 트렉시 위치 — fiScore 값이 이상하면(연도 없음 → 'FYnfinity') 줄 숨김
  calc('peer',()=>{ const fs=fiScore(); return (fs&&fs.na&&isFinite(fs.L))?{sub:`${CMP.peer.selfName} 위치 · 유통사 ${fs.n}곳 재무 비교 (FY${String(fs.L).slice(2)})`, main:`중앙값보다 나은 지표 ${fs.nb}/${fs.na}`}:null; });
  // 맺음 줄 — 갱신 시각 · 수집 상태 · Claude 사용액(수집 상태 카드와 같은 규칙: 1센트 미만 '<$0.01')
  calc('foot',()=>{
    const st=statusRows(), late=st.filter(r=>r.late).length, part=st.reduce((a,r)=>a+(r.failed||0),0), C=STATUS&&STATUS.claude;
    const usd=C?(C.rows||[]).reduce((a,r)=>a+(r.usd||0),0):null, mon=C&&C.month?(C.month===kst.slice(0,7)?'이번 달':`${+C.month.slice(5,7)}월`):'이번 달';
    return {t:`데이터 ${g?`${mdTxt(dataDay)} ${g.slice(11,16)}`:'―'} 갱신 · 수집 ${late?`지연 ${late}`:'정상'}${part?` · 일부 실패 ${part}곳`:''}`,
      c:usd!=null?`${mon} Claude 사용액 ${usdTxt(usd)}`:''};
  });
  return out;
}
function todayHeadHtml(){   // 머리: 보는 날짜 · '오늘 볼 것 4가지' · 갱신 시각 단추(지연 있으면 경고 아이콘 + '지연 n') → 수집 상태
  const g=String(DATA.generated_at||''), gd=g.slice(0,10), late=statusRows().filter(r=>r.late).length;
  const upd=g?`${gd!==kstToday()?mdTxt(gd)+' ':''}${g.slice(11,16)} 갱신`:'갱신 시각 없음', vis=upd+(late?` · 지연 ${late}`:'');
  const date=new Date().toLocaleDateString('ko-KR',{timeZone:'Asia/Seoul',month:'long',day:'numeric',weekday:'long'});
  return `<div class="hd-row"><div class="hd-tt"><span class="hd-kick">${esc(date)}</span><h1>오늘 볼 것 4가지</h1></div>
    <button type="button" class="hd-pill${late?' late':''}" id="tdStatus" data-go="more:status" aria-label="${esc(vis)}, 수집 상태 ${late?`지연 ${late}곳`:'정상'}">${ic(late?'alert':'go',16)}<span>${esc(vis)}</span></button></div>`;
}
const dcNo=n=>`<span class="dc-no" aria-hidden="true">${n}</span>`;
const dcHd=(n,t,meta,dest)=>`<h2 class="dc-hh"><button type="button" class="dc-hd" data-go="${dest}">${dcNo(n)}<span class="dc-t">${esc(t)}</span><span class="dc-meta">${esc(meta)}</span>${ic('right',16,'s2 chev')}</button></h2>`;   // 카드 머리 = 해당 화면으로(결정 D10)
function todayHtml(m){   // 카드마다 따로 그림 — 계산·그리기가 실패한 카드만 머리 + 안내 한 줄(나머지는 그대로), 트렉시·맺음 줄은 실패하면 숨김
  const X=m.fail||{};
  const card=(k,n,t,dest,fn)=>{
    if(!X[k]){ if(m[k]==null) return ''; try{ return fn(m[k]); }catch(e){ console.error('[오늘 볼 것 · '+t+'] 그리기 실패:',e); } }
    return n?`<section class="dc" aria-label="${esc(t)}">${dcHd(n,t,'',dest)}<div class="dc-in">${bootErr(t)}</div></section>`:'';
  };
  return card('buy',1,'매입 검토','brand-all',tdBuyHtml)+card('fx',2,'환율 타이밍','more:fx',tdFxHtml)+card('events',3,'다가오는 일정','mk:cal',tdEvHtml)+card('news',4,'중요 뉴스','news:all',tdNewsHtml)
    +card('peer',0,'트렉시 위치','',p=>`<button type="button" class="dc-peer" data-go="more:peer"><span class="tt"><span class="s">${esc(p.sub)}</span><span class="t">${esc(p.main)}</span></span>${ic('right',20,'s2 chev')}</button>`)
    +card('foot',0,'맺음 줄','',f=>`<button type="button" class="td-foot" data-go="more:status">${esc(f.t)}${f.c?` · ${esc(f.c).replace(/(Claude 사용액 \S+)$/,'<span class="nw">$1</span>')}`:''}</button>`);
}
function tdBuyHtml(B){   // ① 매입 검토(머리는 글자만 — 아래 '점검표 전체 보기'가 링크)
  const G=B.chg, same=G&&!G.n&&!G.skip;   // v33.2 판정 기록 비교 — 바뀐 곳이 있으면 머리 아래 한 줄, 없으면 머리 끝에 '어제와 같음'
  let h=`<section class="dc dc1" aria-label="매입 검토"><div class="dc-hd">${dcNo(1)}<span class="dc-t">매입 검토</span><span class="dc-meta">${same?`${B.n}곳 판정 · ${esc(G.vs)} 같음`:`브랜드 점검표 · ${B.n}곳 판정`}</span></div>`;
  if(B.empty) h+=`<h2 class="dc-h">${esc(B.empty)}</h2>${B.emptySub?`<p class="dc-p">${esc(B.emptySub)}</p>`:''}`;
  else { h+=`<h2 class="dc-h">${esc(B.head)}</h2>`;
    // 한 곳이면 '1곳'을 빼서 '클락스 관망 → 지금 검토'가 좁은 화면(360px)에서도 한 줄에 — 넘치는 끝(바뀐 점수)부터 …
    if(G&&G.n) h+=`<p class="dc-chg" title="${esc(G.full)}"><b>${esc(G.vs)} 달라진 판정${G.n>1?` ${G.n}곳`:''}</b> · ${esc(G.list.join(G.sep))}${G.more?` 외 ${G.more}곳`:''}</p>`;
    h+=B.rows.map(r=>`<button type="button" class="dc-row" data-go="brand:${esc(r.name)}"><span class="dc-rb"><span class="dc-rt"><span class="dc-nm">${esc(r.name)}</span>${vbadge(r.lv)}${chgTag(r.name)}</span><span class="dc-why">${nb(esc(r.why))}</span>${r.hint?`<span class="dc-hint">${esc(r.hint)}</span>`:''}</span>${ic('right',20,'s2 chev')}</button>`).join(''); }
  // '점검표 전체 보기' = 판정 필터 '전체'로(전에 고른 필터가 남아 글자와 결과가 달라지지 않게 — goKey 'brand-all')
  if(B.more) h+=`<button type="button" class="dc-more" data-go="brand-all"><span class="dc-mt"><span class="t">점검표 전체 보기</span><span class="s">${esc(B.more)}</span></span>${ic('arrow',20,'s2')}</button>`;
  return h+`</section>`;
}
function tdFxHtml(F){   // ② 환율 타이밍
  let h=`<section class="dc" aria-label="환율 타이밍">${dcHd(2,'환율 타이밍',F.asof||'','more:fx')}<div class="dc-in">`;
  if(F.empty) h+=`<p class="dc-s">${esc(F.empty)}</p>`;
  else { const H=F.hero, A=F.alert;
    h+=`<p class="fx-hero"><span class="nm">${esc(H.name)}</span><span class="v">${esc(H.value)}</span><span class="d ${H.tone}">${nb(esc(H.dev))}</span>${staleA(H.stale)}</p>`;
    if(H.chg) h+=`<p class="dc-s">${nb(esc(H.chg))}</p>`;
    if(H.brands) h+=`<p class="dc-s">${esc(H.brands)}</p>`;
    // 이전 값 꼬리표는 이름 칸(76px)을 넘쳐 줄 아래 한 칸에
    if(F.rows.length) h+=`<div class="fx-rows">${F.rows.map(o=>`<div class="fx-r"><span class="nm">${esc(o.name)}</span><span class="v">${esc(o.value)}</span><span class="d ${o.tone}">${nb(esc(o.diff))}</span>${o.stale?`<span class="fx-st">${staleA(o.stale)}</span>`:''}</div>`).join('')}</div>`;
    h+=A.n?`<p class="fx-al">${esc(A.day)} 새 환율 알림 ${A.n}건</p>${A.list.map(t=>`<p class="fx-ai">${esc(t)}</p>`).join('')}`
      :`<p class="fx-al">${esc(A.day)} 새 환율 알림 없음 · ${esc(A.last)}</p>`; }
  return h+`</div></section>`;
}
function tdEvHtml(ev){   // ③ 다가오는 일정
  return `<section class="dc" aria-label="다가오는 일정">${dcHd(3,'다가오는 일정','본사 실적 · 해외 세일','mk:cal')}<div class="dc-evs">`
    +(ev.length?ev.map(e=>`<button type="button" class="dc-ev" data-go="${esc(e.go)}"><span class="d">${esc(e.d)}</span><span class="ev-tt"><span class="t">${esc(e.title)}</span><span class="s">${esc(e.sub)}</span></span><span class="kind${e.kind==='세일'?' sale':''}">${e.kind}</span></button>`).join('')
      :`<p class="dc-s" style="padding-bottom:8px">90일 안 본사 실적·150일 안 해외 세일 없음</p>`)+`</div></section>`;
}
function tdNewsHtml(N){   // ④ 오늘 중요 뉴스(기사는 원문 새 창, 카드 머리는 시장 › 뉴스 전체)
  if(N.empty) return `<section class="dc" aria-label="중요 뉴스">${dcHd(4,'중요 뉴스','','news:all')}<div class="dc-nws"><p class="dc-s" style="padding-bottom:8px">${esc(N.empty)}</p></div></section>`;
  let h=`<section class="dc" aria-label="${esc(N.head)}">${dcHd(4,N.head,N.sub,'news:all')}<div class="dc-nws">`;
  h+=N.items.map(i=>`<a class="dc-news" href="${esc(safeUrl(i.link))}" target="_blank" rel="noopener"><span class="t">${esc(i.t)}</span><span class="s">${esc(i.meta)}</span></a>`).join('');
  if(N.none) h+=`<p class="dc-s" style="padding-bottom:8px">보관 기간 안 ★3 뉴스 없음</p>`;
  if(N.more) h+=`<button type="button" class="dc-xmore" data-go="news:all">외 ★3 ${N.more}건 — 뉴스에서 보기</button>`;
  return h+`</div></section>`;
}
/* v32.12 종합 '국내 의류 소매판매' 그래프 — 카드 폭에 맞춰 1배로 그림(글자 13px · 위아래 빈 공간 없음), 범례는 그래프 밖
   v33 A안: 시장 › 국내 칩 첫 카드 — 폭은 국내 칩 영역(#mk-kr) 기준, 칩이 처음 보일 때 그림(hcDraw) */
let HC_W=0;
function homeChartHtml(){
  const kr=(KR&&KR.series&&KR.series.retail_apparel)?KR.series.retail_apparel:null; if(!kr) return '';
  const ps=Object.keys(kr.values).sort(), krLast=ps[ps.length-1], krYoy=kr.yoy?kr.yoy[krLast]:null, krTrend=krTrendOf(kr);
  const yNow=krLast.slice(0,4), yPrev=String(+yNow-1);
  const cur=[],prev=[]; for(let m=1;m<=12;m++){const mm=String(m).padStart(2,'0'); cur.push(kr.values[yNow+mm]??null); prev.push(kr.values[yPrev+mm]??null);}
  const all=[...cur,...prev].filter(v=>v!=null); const mn=Math.min(...all), mx=Math.max(...all), rg=(mx-mn)||1;
  const hb=document.getElementById('mk-kr'), cw=hb?hb.clientWidth:0;
  const W=HC_W=Math.max(280,Math.round((cw||370)-30)), H=144, L=10, R=10, T=8, B=24;   // 카드 안쪽 폭 = 그리는 폭(1배) → 글자 크기 그대로
  const xs=i=>L+i*(W-L-R)/11, ys=v=>T+(H-T-B)-(v-mn)/rg*(H-T-B);
  const line=(arr,color,w)=>{const pts=arr.map((v,i)=>v==null?null:`${xs(i).toFixed(1)},${ys(v).toFixed(1)}`).filter(Boolean).join(' ');return `<polyline fill="none" stroke="${color}" stroke-width="${w}" stroke-linejoin="round" points="${pts}"/>`;};
  const lastIdx=cur.map((v,i)=>v!=null?i:-1).filter(i=>i>=0).pop();
  return `<div class="card span2" id="hcCard"><h3>국내 의류 소매판매 — 올해 vs 작년 (월별 지수)</h3>
    <div class="hc-leg"><span><i style="background:var(--accent)"></i>${yNow} 올해</span><span><i style="background:var(--chart-prev)"></i>${yPrev} 작년</span></div>
    <svg class="hc-svg" viewBox="0 0 ${W} ${H}" role="img" aria-label="국내 의류 소매판매지수 ${yNow}년 vs ${yPrev}년">
      ${line(prev,'var(--chart-prev)',2)}${line(cur,'var(--accent)',2.5)}
      ${lastIdx!=null?`<circle cx="${xs(lastIdx).toFixed(1)}" cy="${ys(cur[lastIdx]).toFixed(1)}" r="4" fill="var(--accent)"/>`:''}
      ${[0,3,6,9,11].map(i=>`<text x="${xs(i).toFixed(1)}" y="${H-6}" text-anchor="${i===0?'start':(i===11?'end':'middle')}" font-size="13" fill="var(--sub)">${i+1}월</text>`).join('')}
    </svg>
    <div class="note">${fmtPrd(krLast)} ${kr.values[krLast].toFixed(1)} (작년 ${(kr.values[yPrev+krLast.slice(4,6)]??'―')}, ${fmt(krYoy,1,true)})${krTrend?' · '+krTrend:''}</div></div>`;
}
function krTrendOf(kr){
  const ps=Object.keys(kr.values).sort(), y3=ps.slice(-3).map(p=>kr.yoy?kr.yoy[p]:null);
  if(!y3.every(v=>v!=null)) return '';
  return (y3[0]>y3[1]&&y3[1]>y3[2])?'3개월 둔화':(y3[0]<y3[1]&&y3[1]<y3[2])?'3개월 가속':'';
}
function hcDraw(){   // v33 국내 칩이 보일 때만 그림(숨은 칩은 폭 0) — 처음 한 번, 그 뒤엔 폭이 20px 넘게 바뀌었을 때만
  const box=document.getElementById('hcBox'), hb=document.getElementById('mk-kr');
  if(!box||!hb||!hb.clientWidth) return;
  if(!box.dataset.drawn||Math.abs(hb.clientWidth-30-HC_W)>20){ box.innerHTML=homeChartHtml(); box.dataset.drawn='1'; }
}
window.addEventListener('resize',()=>{ safe(hcDraw,'의류 소매 그래프','mk-kr'); });   // 화면 폭이 바뀌면(회전 등) 그래프만 다시 그림(국내 칩이 숨어 있으면 다음에 보일 때)
/* v32.12 순위 줄 — 윗줄 법인명, 아랫줄 브랜드 · 그룹 · 기준(분기 '26.06 / 연간 FY25) + 이전 값·반영 대기 표시 */
function rkRow(r,valHtml){
  const n=nmSplit(r.name), sub=[NM_KO[n.brand]||n.brand,r.group,r.basis].filter(Boolean).map(esc).join(' · ');
  return `<button type="button" class="rk" onclick="goDetail('${r.key}')"><span class="rk-n">${r.logo}<span class="rk-t"><span class="rk-m">${esc(n.main)}</span><span class="rk-s">${sub}${staleTag(r.stale)}${failTag(r.key)}${pendTag(r.pend)}</span></span></span>${valHtml}</button>`;
}
const calDot=dn=>`<i class="cal-dot${dn<=7?' on':''}" aria-hidden="true"></i>`;   // v33 실적 7일 안 = 파란 점(옛 빨간·흰 원 이모지)
function warnTog(b){   // 재고 경고 '전체 보기(N곳)' ↔ '접기'
  const m=document.getElementById('warnMore'); if(!m) return; m.hidden=!m.hidden; const o=!m.hidden;
  b.setAttribute('aria-expanded',o?'true':'false'); b.innerHTML=`<span>${o?'접기':`전체 보기(${b.dataset.n}곳)`}</span>${ic(o?'up':'down',16)}`;
}
/* v33 A안: 옛 종합(buildHome)을 나눔 — 오늘(지연 띠 + 오늘 볼 것) · 시장 › 실적·재고(KPI·순위·재고 경고·실적 발표) ·
   시장 › 소싱 지도 · 시장 › 국내(의류 소매 그래프, hcDraw). 계산은 옛 buildHome 그대로 */
function buildToday(){   // v33 S2: 오늘을 열 때마다 다시 그림(지연 판정·D-day는 열람 시점) — 머리 · 지연 띠 · 결정 카드
  paint('tdHead',todayHeadHtml,'오늘 머리');
  safe(statusWarn,'수집 지연 띠','statusWarn');
  paint('todayCard',()=>todayHtml(todayModel()),'오늘 볼 것');
}
function buildSig(){
  const rows=rows_all();
  const today=kstMid();   // v33 한국 날짜 기준(오늘 ③과 같은 D-day)
  // 성장(최근 분기 매출 전년 대비; 분기 없으면 연간) — v32.12 기준 표시: 분기 '26.06 / 연간 FY25(오래된 결산도 순위에 두고 연도만 표시)
  const basisOf=r=>r.q_yoy!=null?{g:r.q_yoy,basis:`분기 ${ym(r.q_end)||''}`.trim(),bs:ym(r.q_end)||'분기'}
                                :{g:r.rev_yoy,basis:`연간 ${fyLbl(r.fy_end)}`.trim(),bs:fyLbl(r.fy_end)||'연간'};
  const growthAll=rows.filter(r=>!WHOLE_CO[r.key]).map(r=>({...r,...basisOf(r)})).filter(r=>r.g!=null);   // 전사 수치(삼성물산) 제외
  const acq=growthAll.filter(r=>acqOn(r.key));   // 인수 효과 기간(딕스) — 순위에서 빼고 각주
  // ±100% 초과는 기저·인수 효과 가능성이 커서 순위에서 제외(각주로 표기, 값은 기업 탭에 그대로)
  const outlier=growthAll.filter(r=>!acqOn(r.key)&&Math.abs(r.g)>100);
  const growth=growthAll.filter(r=>!acqOn(r.key)&&Math.abs(r.g)<=100);
  const up=[...growth].sort((a,b)=>b.g-a.g).slice(0,4);
  const dn=[...growth].sort((a,b)=>a.g-b.g).slice(0,4);
  // 재고 경고: 재고 증가율이 매출 증가율보다 10p 이상 높고 재고 +10% 이상 — 전사 수치·인수 효과 기간은 제외(각주)
  // v32.14 재고·매출을 같은 기간끼리 비교(분기 자료가 있으면 같은 분기, 없으면 연간 결산) — 비교 기간을 줄에 표시
  const warnAll=rows.filter(r=>r.inv_yoy!=null&&r.inv_rev!=null&&r.inv_yoy>=10&&r.inv_yoy-r.inv_rev>=10).map(r=>({...r,basis:r.inv_lbl}));
  const warnAcq=warnAll.filter(r=>!WHOLE_CO[r.key]&&acqOn(r.key));
  const warn=warnAll.filter(r=>!WHOLE_CO[r.key]&&!acqOn(r.key)).sort((a,b)=>(b.inv_yoy-b.inv_rev)-(a.inv_yoy-a.inv_rev));
  // 실적 일정
  const ev=rows.filter(r=>r.earn).map(r=>({...r,d:new Date(r.earn+'T00:00:00')})).map(r=>({...r,dn:Math.round((r.d-today)/86400000)}))
    .filter(r=>r.dn>=0&&r.dn<=90).sort((a,b)=>a.dn-b.dn);
  // 국내 의류 소매
  const kr=(KR&&KR.series&&KR.series.retail_apparel)?KR.series.retail_apparel:null;
  let krLast=null, krYoy=null, krTrend='';
  if(kr){ const ps=Object.keys(kr.values).sort(); krLast=ps[ps.length-1]; krYoy=kr.yoy?kr.yoy[krLast]:null; krTrend=krTrendOf(kr); }

  // v32.12 KPI 설명은 휴대폰에서 2줄까지 — 고정 문구는 짧게, 회사 이름은 브랜드(괄호 속)로
  // v33 KPI 4칸은 시장 › 실적·재고 맨 위: 성장 1위 → 기업 상세 · 재고 경고 → 아래 재고 경고 카드 · 실적 → 캘린더 · 의류 소매 → 국내
  const kp=[
    up[0]?{l:'성장 1위',v:fmt(up[0].g,1,true),s:`${nmBrand(up[0].name)} · ${up[0].bs}`,act:`goDetail('${up[0].key}')`}:{l:'성장 1위',v:'―',s:'',act:"sw('co')"},
    {l:'재고 경고',v:`<span class="${warn.length?'neg':''}">${warn.length}곳</span>`,s:'재고 증가 > 매출 증가',act:"focusCard('warnCard')"},
    ev[0]?{l:'실적 발표',v:`D-${ev[0].dn}`,s:`${nmBrand(ev[0].name)} ${ev[0].d.getMonth()+1}/${ev[0].d.getDate()}`,act:"sw('cal')"}:{l:'실적 발표',v:'―',s:'90일 내 없음',act:"sw('cal')"},
    kr?{l:'의류 소매',v:fmt(krYoy,1,true),s:`${+krLast.slice(4,6)}월 · ${krTrend||'전년 동월 대비'}`,act:"sw('kr')"}:{l:'의류 소매',v:'―',s:'미수집',act:"sw('kr')"},
  ];
  document.getElementById('kpis').innerHTML=kp.map(k=>`<button type="button" class="kpi" onclick="${k.act}"><span class="l">${k.l}</span><span class="v">${k.v}</span><span class="s">${esc(k.s)}</span></button>`).join('');

  let h='';
  const ex=[outlier.length?`±100% 초과(기저·인수 효과 가능) ${outlier.map(r=>esc(r.name)+' '+fmt(r.g,0,true)).join(' · ')}`:'',
    ...acq.map(r=>{ const c=acqCore(r.key); return `${esc(r.name)} ${fmt(r.g,0,true)}(인수 효과${c!=null?', 본체 '+fmt(c,1,true):''})`; })].filter(Boolean);
  h+=`<div class="card"><h3>성장 상위 · 매출 전년 대비 <button type="button" class="go" onclick="sw('co')">기업 ›</button></h3>${up.map(r=>rkRow(r,`<b>${fmt(r.g,1,true)}</b>`)).join('')||'<div class="na">―</div>'}${ex.length?`<div class="note">순위 제외: ${ex.join(' · ')}</div>`:''}</div>`;
  h+=`<div class="card"><h3>성장 하위 · 매출 전년 대비</h3>${dn.map(r=>rkRow(r,`<b>${fmt(r.g,1,true)}</b>`)).join('')||'<div class="na">―</div>'}</div>`;
  const wex=[...Object.entries(WHOLE_CO).filter(([k])=>rows.some(r=>r.key===k)).map(([,v])=>esc(v)),
    ...warnAcq.map(r=>`${esc(r.name)}는 인수 효과 기간(~${mdTxt(acqOn(r.key).until)})이라 제외`)];
  h+=`<div class="card" id="warnCard"><h3>재고 경고 · 재고 증가율이 매출 증가율보다 높은 곳 <span class="na" style="font-weight:400">기업을 누르면 상세</span></h3>${(()=>{ const row=r=>rkRow(r,`<span class="rk-v2"><span>재고 <b>${fmtInv(r.inv_yoy)}</b></span><small>매출 ${fmt(r.inv_rev,1,true)}${r.dio!=null?` · ${Math.round(r.dio)}일`:''}</small></span>`);
    return (warn.slice(0,8).map(row).join('')||'<div class="na">해당 없음</div>')
      +(warn.length>8?`<div id="warnMore" hidden>${warn.slice(8).map(row).join('')}</div><button type="button" class="wm-tog" data-n="${warn.length}" aria-expanded="false" aria-controls="warnMore" onclick="warnTog(this)"><span>전체 보기(${warn.length}곳)</span>${ic('down',16)}</button>`:''); })()}
    <div class="note">기준: 재고가 1년 전보다 10% 이상 늘고, 같은 기간 매출 증가율보다 10%p 이상 빠른 곳 · 같은 기간끼리 비교(분기 자료가 있으면 최근 분기 vs 1년 전 같은 분기, 없으면 연간 결산) · N일 = 재고일수(연간)${wex.length?'<br>'+wex.join(' · '):''}</div></div>`;
  h+=`<div class="card"><h3>다가오는 실적 발표 <button type="button" class="go" onclick="sw('cal')">캘린더 ›</button></h3>${ev.slice(0,5).map(r=>rkRow({...r,basis:''},`<span>${calDot(r.dn)}D-${r.dn} · ${r.d.getMonth()+1}/${r.d.getDate()}</span>`)).join('')||'<div class="na">90일 내 일정 없음</div>'}</div>`;
  document.getElementById('sigBody').innerHTML=h;
}
function buildMap(){   // 시장 › 소싱 지도(하단 패널 #sheet은 공용)
  document.getElementById('mapBody').innerHTML=sourcingCard()||'<div class="card"><div class="na">소싱 지도 자료 없음 — 본사 지역 분해·재고 자료가 수집되면 표시</div></div>';
}

/* ── 기업 (A안: 검색·칩·압축 표·행 펼침) ── */
let coFilter='전체', coQuery='';
function buildCoChips(){
  const rows=rows_all();
  const chips=[['전체',rows.length],...CO_GROUPS.map(g=>[g,rows.filter(r=>r.group===g).length]).filter(x=>x[1]>0),
    ['온라인 플랫폼',rows.filter(r=>KR_PLATFORMS.includes(r.key)).length]].filter(x=>x[0]==='전체'||x[1]>0);
  document.getElementById('coChips').innerHTML=chips.map(([g,n])=>`<button type="button" class="chip${coFilter===g?' on':''}" data-g="${esc(g)}" aria-pressed="${coFilter===g}">${esc(g)} ${n}</button>`).join('');
  document.querySelectorAll('#coChips .chip').forEach(c=>c.onclick=()=>{const f=document.activeElement===c; coFilter=c.dataset.g;buildCoChips();buildCo(); refocus(f,`#coChips .chip[data-g="${CSS.escape(coFilter)}"]`);});
}
function buildCo(){
  // 온라인 플랫폼 칩: 공통 표 대신 플랫폼 카드(원화 환산·상태 표기 포함, v32.5)
  const plat=coFilter==='온라인 플랫폼';
  document.getElementById('coPlat').innerHTML=plat?platformCardHtml():'';
  document.getElementById('coTblCard').style.display=plat?'none':'';
  if(plat) return;
  const rows=rows_all().filter(r=>(coFilter==='전체'||r.group===coFilter)&&(!coQuery||r.name.toLowerCase().includes(coQuery)||r.key.toLowerCase().includes(coQuery)));
  let h=`<tr><th>기업</th><th>매출(원)</th><th>전년 대비</th><th>총이익률</th><th>재고 증감</th></tr>`;
  rows.forEach(r=>{
    const gmCell=(r.gm!=null)?mnum(r.gm)+'%':(r.opm!=null?mnum(r.opm)+'%<span class="na"> 영업</span>':'<span class="na">―</span>');
    const gmMini=r.gm!=null?`매출총이익률 <b>${mnum(r.gm)}%</b>`:(r.opm!=null?`영업이익률 <b>${mnum(r.opm)}%</b>`:'매출총이익률 <b>―</b>');   // v33 휴대폰은 표에서 뺀 열을 펼친 줄에
    const nm=nmSplit(r.name), nsub=[nm.brand?esc(NM_KO[nm.brand]||nm.brand):'',staleTag(r.stale),failTag(r.key),pendTag(r.pend)].filter(Boolean).join(' ');   // v32.12 이름 2줄(법인명 / 브랜드·표시)
    h+=`<tr class="co" data-k="${r.key}" tabindex="0" aria-expanded="false"><td>${r.logo}${esc(nm.main)}${nsub?`<span class="nm-sub">${nsub}</span>`:''}</td><td>${revKrwCell(r.rev,r.cur,1)}</td><td>${fmt(r.rev_yoy,1,true)}</td><td>${gmCell}</td><td>${fmtInv(r.inv_yoy)}</td></tr>`;   // v33 비교 기간 꼬리표는 펼친 줄에만(행 높이·폭)
    let mini='';
    if(r.listed){
      const x=r.item, s=segOf(r.key);
      const reg=(s&&s.extract.regions||[]).filter(z=>z.revenue!=null&&!/total|전체|합계|consolidated/i.test(z.name||'')); const tot=reg.reduce((a,b)=>a+b.revenue,0);
      const top=reg.length?reg.slice().sort((a,b)=>b.revenue-a.revenue).slice(0,2).map(z=>`${z.name} ${tot?(z.revenue/tot*100).toFixed(0):'―'}%`).join(' · '):'―';
      const ch=(s&&s.extract.channels||[]).filter(z=>z.revenue!=null); const ctot=ch.reduce((a,b)=>a+b.revenue,0);
      const chs=ch.length?ch.map(z=>`${z.name} ${ctot?(z.revenue/ctot*100).toFixed(0):'―'}%`).join(' · '):'―';
      const fy=x.fy.length?x.fy[x.fy.length-1]:{};
      const kd=((KRD&&KRD.entities)||[]).find(e=>e.link===r.key);
      const kdTxt=kd?(()=>{const ys=(kd.years||[]).filter(y=>y.rev!=null);const l=ys[ys.length-1],p=ys[ys.length-2];return l?`${moneyShort(l.rev,'KRW')} ${p?fmt(l.rev/p.rev*100-100,1,true):''}`:'미확인';})():null;
      const evd=r.earn?Math.round((new Date(r.earn+'T00:00:00')-kstMid())/86400000):null;   // v33 한국 날짜 기준
      mini=`<div class="mini"><div>최근 분기 매출 ${fmt(r.q_yoy,1,true)} <span class="na">${x.q_end?ym(x.q_end):''}</span>${r.pend?`<br><span class="na">${esc(r.pend.src)} 공시 ${ym(r.pend.end)} 분기 발표됨 · 야후 미반영</span>`:''}</div><div>영업이익률 <b>${fy.op_pct!=null?mnum(fy.op_pct)+'%':'―'}</b></div>
      <div>재고 증감 <b>${fmtInv(r.inv_yoy)}</b> <span class="na">${esc(r.inv_lbl||'')}${r.inv_rev!=null?' · 같은 기간 매출 '+fmt(r.inv_rev,1,true):''}</span></div><div>${gmMini}</div>
      <div>지역: ${esc(top)}</div><div>채널: ${esc(chs)}</div>
      <div>${kd?logoImg('krd:'+kd.id,false,kd.name)+esc(kd.name)+' ':''}${kd?`<b>${kdTxt}</b>`:'<span class="na">국내 법인 미연결</span>'}</div><div>실적 발표 ${evd!=null&&evd>=0?`<b>D-${evd}</b>`:'<span class="na">―</span>'}</div></div>`;
    } else {
      mini=`<div class="mini"><div>구분: ${esc(r.route==='none'?'DART 공시 미발견':'DART '+(r.route==='api'?'사업보고서':'감사보고서')+'(연간 · 별도'+(r.std?' · '+(STD_SH[r.std]||r.std):'')+')')}</div><div>기준: ${r.fy_end?ym(r.fy_end)+' 결산':'―'}</div>
      <div>재고일수 <b>${r.dio!=null?Math.round(r.dio)+'일':'―'}</b></div><div>재고 증감 <b>${fmtInv(r.inv_yoy)}</b> <span class="na">${esc(r.inv_lbl||'')}</span></div><div>${gmMini}</div><div></div>${r.note?`<div style="grid-column:1/-1" class="na">${esc(r.note)}</div>`:''}</div>`;
    }
    h+=`<tr class="cx" data-for="${r.key}" style="display:none"><td colspan="5">${mini}<button type="button" class="note co-more" onclick="goDetail('${r.key}')">전체 상세 ›</button></td></tr>`;
  });
  if(rows.length===0) h+=`<tr><td colspan="5" class="na">검색 결과 없음</td></tr>`;
  document.getElementById('coTbl').innerHTML=h;
  document.querySelectorAll('#coTbl tr.co').forEach(tr=>tr.onclick=()=>{const x=tr.nextElementSibling; if(x&&x.classList.contains('cx')){ x.style.display=x.style.display==='none'?'':'none'; tr.setAttribute('aria-expanded',x.style.display==='none'?'false':'true'); }});
}
function showCoList(){ document.getElementById('coDetail').style.display='none'; document.getElementById('coList').style.display=''; }
const MORE_NAME={peer:'유통사 비교',fb:'패션 브랜드',ey:'패션 브랜드',fx:'환율',logi:'물류',cb:'해외직구',status:'수집 상태'};   // v33 'check'(브랜드 점검표)는 브랜드 탭으로
// v33 A안: 기업 상세는 시장 › 기업 안 한 화면 — 어디서 열어도 같은 화면, '‹ 뒤로'·휴대폰 뒤로 = 들어온 곳(go·goBack, 아래 '이동 경로')
function goDetail(t){ go({tab:'market',chip:'co',id:String(t)}); }
function pairBars(list, curLabel, prevLabel, cur){
  const items=list.filter(r=>r.revenue!=null);
  if(!items.length) return null;
  const rows=items.map(r=>{
    let prev=r.prev_revenue, derived=false;
    if(prev==null && r.yoy_pct!=null && r.yoy_pct>-100){
      prev=r.revenue/(1+r.yoy_pct/100); derived=true;
    }
    return {name:r.name, cur:r.revenue, prev, derived, yoy:r.yoy_pct, cn:r.cn_yoy_pct};
  });
  const totalCur=rows.reduce((a,b)=>a+b.cur,0);
  const totalPrev=rows.reduce((a,b)=>a+(b.prev||0),0);
  const mx=Math.max(...rows.map(r=>Math.max(r.cur, r.prev||0)));
  let h='';
  rows.forEach(r=>{
    const shCur=totalCur?(r.cur/totalCur*100).toFixed(0):null;
    const shPrev=(r.prev&&totalPrev)?(r.prev/totalPrev*100).toFixed(0):null;
    const wC=Math.max(r.cur/mx*100,6);
    const yoy=r.yoy!=null?' '+fmt(r.yoy,1,true):'';
    h+=`<div class="pair">
    <div class="pname" title="${esc(r.name)}">${esc(r.name)}${shCur?` · 비중 ${shCur}%`:''}${shPrev?` <span class="na">(전년 ${shPrev}%)</span>`:''}${r.derived?'<span class="tag2">역산</span>':''}</div>
    <div class="prow"><div class="yr">${curLabel}</div>
      <div class="pw"><div class="pb now" style="width:${wC}%"></div>
      <div class="pv">${segMoney(r.cur,cur)}${yoy}</div></div></div>`;
    if(r.prev!=null){
      const wP=Math.max(r.prev/mx*100,6);
      h+=`<div class="prow"><div class="yr">${prevLabel}</div>
      <div class="pw"><div class="pb prev" style="width:${wP}%"></div>
      <div class="pv">${segMoney(r.prev,cur)}</div></div></div>`;
    }
    if(r.cn!=null) h+=`<div class="cnline">환율 제외 ${fmt(r.cn,1,true)}${r.yoy!=null?` <span class="na">(보고 통화 ${pp(r.yoy)})</span>`:''}</div>`;
    h+=`</div>`;
  });
  return h;
}

function compareCard(gx, e){
  /* gx: 글로벌 DATA item, e: KRD entity */
  const fy=gx.fy.length?gx.fy[gx.fy.length-1]:{};
  const ys=(e.years||[]).filter(y=>y.rev!=null); const l=ys[ys.length-1], p=ys[ys.length-2];
  if(!l) return '';
  const g={yoy:fy.rev_yoy, opm:fy.op_pct, inv:gx.inv_yoy, dio:dioOf(gx.inventory,fy.rev,fy.gp,null)};
  const k={yoy:(p&&p.rev)?(l.rev/p.rev-1)*100:null, opm:(l.op!=null&&l.rev)?l.op/l.rev*100:null,
           inv:(p&&l.inv&&p.inv)?(l.inv/p.inv-1)*100:null, dio:dioOf(l.inv,l.rev,null,l.cogs)};
  const cell=(v,pct=true)=>v==null?'<span class="na">―</span>':(pct?fmt(v,1,true):Math.round(v)+'일');
  const diff=(a,b)=>{ if(a==null||b==null) return ''; const d=+(b-a).toFixed(1); return `<span class="na"> (${d>0?'+':d<0?'−':''}${Math.abs(d).toFixed(1)}%p)</span>`; };   // v33 0.0%p는 부호 없음
  return `<div class="card"><h3>글로벌 본사 vs 국내 법인</h3>
    <div class="tblwrap"><table class="nowrap"><tr><th></th><th>${esc(gx.name)}</th><th>${esc(e.name)}</th></tr>
    <tr><td>매출 전년 대비</td><td>${cell(g.yoy)}</td><td>${cell(k.yoy)}${diff(g.yoy,k.yoy)}</td></tr>
    <tr><td>영업이익률</td><td>${g.opm!=null?mnum(g.opm)+'%':'<span class="na">―</span>'}</td><td>${k.opm!=null?mnum(k.opm)+'%':'<span class="na">―</span>'}${diff(g.opm,k.opm)}</td></tr>
    <tr><td>재고 증감</td><td>${fmtInv(g.inv)}</td><td>${fmtInv(k.inv)}${diff(g.inv,k.inv)}</td></tr>
    <tr><td>재고일수</td><td>${cell(g.dio,false)}</td><td>${cell(k.dio,false)}</td></tr></table></div>
    <div class="note">글로벌 FY ${fy.end?ym(fy.end):'―'} 연결 · 국내 법인 FY ${ym(l.end)} 별도 · 괄호 = 국내−글로벌(%p)</div></div>`;   // v33.9 짧게
}
/* v32.9 기준 표기(dart_fetch v3.4): 회계기준·보고서 종류·연결 요약 */
const STD_SH={'K-IFRS':'K-IFRS','일반기업회계기준':'K-GAAP','중소기업회계기준':'중소기업회계기준'};
const srcKind=e=>e.route==='api'?'사업보고서':(e.route==='doc'?'감사보고서':'공시 미발견');
function stdTxt(e){   // 연도별 기준이 바뀌었으면 '일반기업회계기준 → FY24부터 K-IFRS'
  const ys=(e.years||[]).filter(y=>y.rev!=null&&y.std);
  if(!ys.length) return (e.years||[]).some(y=>'std' in y)?'회계기준 미확인':'';   // 필드 자체가 없으면(dart v3.4 실행 전) 표시 안 함
  const a=ys[0].std, b=ys[ys.length-1].std;
  return a===b?b:`${a} → ${ys.find(y=>y.std===b).fy}부터 ${b}`;
}
const ymd=d=>d&&d.length===8?`${d.slice(0,4)}.${d.slice(4,6)}.${d.slice(6)}`:(d||'');
function cfsHtml(e){   // 별도 기준 화면 아래 연결 요약(사업보고서 경로) 또는 연결감사보고서 안내
  const cy=(e.cfs&&e.cfs.years)||[];
  if(cy.length){
    let h=`<div class="ndate" style="margin-top:12px">연결 기준 요약 <span class="na" style="font-weight:400">종속회사 포함 · 사업보고서 연결 재무제표 · 원화</span></div>
      <div class="tblwrap"><table class="nowrap"><tr><th>결산</th><th>매출</th><th>영업이익</th><th>순이익</th><th>별도 대비 매출</th></tr>`;
    cy.forEach(c=>{ const sy=(e.years||[]).find(y=>y.end===c.end), r=(sy&&sy.rev&&c.rev)?c.rev/sy.rev:null;
      h+=`<tr><td>FY${c.end.slice(2,4)}</td><td>${c.rev!=null?moneyShort(c.rev,'KRW'):'―'}</td><td>${c.op!=null?moneyShort(c.op,'KRW'):'―'}</td><td>${c.ni!=null?moneyShort(c.ni,'KRW'):'―'}</td><td>${r!=null?r.toFixed(2)+'배':'―'}</td></tr>`; });
    return h+`</table></div><div class="note">비교 화면(유통사·패션·아이웨어 비교, 기업 목록)은 다른 회사와 기준을 맞추려고 별도 수치를 씀 · 출처 ${esc(e.cfs.source||'')}</div>`;
  }
  if(e.cfs_report) return `<div class="note" style="margin-top:8px">연결감사보고서도 공시됨(${esc(e.cfs_report.name||'')} · ${esc(ymd(e.cfs_report.date))}) — 이 화면은 별도 기준, 연결 수치는 수집하지 않음 · <a href="https://dart.fss.or.kr/dsaf001/main.do?rcpNo=${encodeURIComponent(e.cfs_report.rcept)}" target="_blank" rel="noopener" style="color:var(--accent)">DART 원문 ›</a></div>`;
  return '';
}
function krdCard(e, linked){
  const title=linked?`국내 법인 실적 — ${esc(e.name)}`:`법인 실적`;
  let h=`<div class="card"><h3>${title} <span class="tag">DART ${srcKind(e)}</span></h3>`;
  const en=noteClean(e.note); if(en) h+=`<div class="note" style="margin:0 0 8px">${esc(en)}</div>`;
  const ys=e.years||[];
  const filled=ys.filter(y=>y.rev!=null);
  if(!filled.length){
    const why=(e.route==='none')?'DART 공시 미발견':'DART 수집 대기';
    h+=`<div class="na">미확인 — ${why}${KRD.updated_at?' · 마지막 체크 '+KRD.updated_at:''}</div></div>`;
    return h;
  }
  const fym=ys.length&&ys[ys.length-1].end?(+ys[ys.length-1].end.slice(5,7))+'월 결산':'';
  h+=`<div class="tblwrap"><table class="nowrap"><tr><th>결산</th><th>매출</th><th>전년 대비</th><th>영업률</th><th>순이익</th><th>재고</th><th>재고 증감</th></tr>`;
  ys.forEach((y,i)=>{
    const p=i>0?ys[i-1]:null;
    const yoy=(y.rev!=null&&p&&p.rev)?(y.rev/p.rev-1)*100:null;
    const opm=(y.op!=null&&y.rev)?y.op/y.rev*100:null;
    const iy=(y.inv&&p&&p.inv)?(y.inv/p.inv-1)*100:null;
    h+=`<tr><td title="${ym(y.end)||''}">${y.fy}</td>
      <td>${y.rev!=null?moneyShort(y.rev,'KRW'):'―'}</td><td>${fmt(yoy,1,true)}</td>
      <td>${opm!=null?mnum(opm)+'%':'―'}</td>
      <td>${y.ni!=null?moneyShort(y.ni,'KRW'):'―'}</td>
      <td>${y.inv!=null?moneyShort(y.inv,'KRW'):'―'}</td><td>${fmtInv(iy)}</td></tr>`;
  });
  h+=`</table></div>`;
  // v32.12 출처: 같은 보고서(접수번호)는 한 번만, DART 원문 링크로 — 'FY24·FY25 감사보고서 2026.04.10 원문 ›'
  const docs=[];
  ys.filter(y=>y.source).forEach(y=>{
    const m=String(y.source).match(/rcept=(\d{14})/), kind=/사업보고서/.test(y.source)?'사업보고서':'감사보고서';
    const k=m?m[1]:y.source, d=docs.find(o=>o.k===k);
    if(d) d.fy.push(y.fy); else docs.push({k,rc:m?m[1]:null,kind,fy:[y.fy],raw:y.source});
  });
  if(docs.length) h+=`<div class="src">출처: ${docs.map(o=>o.rc
    ?`${esc(o.fy.join('·'))} <a href="https://dart.fss.or.kr/dsaf001/main.do?rcpNo=${o.rc}" target="_blank" rel="noopener" style="color:var(--accent);white-space:nowrap">DART ${o.kind} ${ymd(o.rc.slice(0,8))} 원문 ›</a>`
    :`${esc(o.fy.join('·'))}: ${esc(String(o.raw).replace(/\(prior\)/g,'(전기)').replace(/\(current\)/g,'(당기)'))}`).join(' · ')}</div>`;
  h+=cfsHtml(e);
  h+=`<div class="note">${fym?fym+' · ':''}별도 · ${stdTxt(e)?esc(stdTxt(e))+' · ':''}원화 · 연간</div></div>`;   // v33.9 짧게
  return h;
}
function renderKrdDetail(id){
  const e=((KRD&&KRD.entities)||[]).find(z=>z.id===id);
  if(!e){ document.getElementById('detBody').innerHTML='<div class="na">미확인</div>'; return; }
  let h=`<div class="det-head">${logoImg('krd:'+e.id,true,e.name)}${esc(e.name)} <span class="tk">한국</span> <span class="tag">${esc(e.type)}</span></div>`;
  h+=krdCard(e,false);
  h+=fiDetailCard(e);
  if(e.link){
    const g=DATA.items.find(i=>i.ticker===e.link);
    if(g) h+=compareCard(g,e)+`<button type="button" class="bd-hq co-hq" data-go="co:${esc(e.link)}">${logoImg(e.link,false,g.name)}<span class="tt"><span class="s">글로벌 본사</span><span class="t">${esc(g.name)} 기업 상세</span></span>${ic('right',20,'s2 chev')}</button>`;   // 누르는 곳 44px 이상
  }
  h+=naverDetailCard('krd:'+e.id);
  h+=newsCard('krd:'+e.id);
  document.getElementById('detBody').innerHTML=h;
}
/* v32.15 본사 발언(대표 지시 2026-10-10) — 실적 문서에서 재고·할인·유통 통제 문장을 원문 그대로(extract_segments v11·ir_fetch v1.3,
   원문에 글자 그대로 있는 문장만 저장). 새 형식으로 추출된 뒤에만 보이고, 해당 문장이 없으면 '없음' 한 줄 */
const MGMT_TOPIC={inventory:'재고',discount:'할인·판촉',channel:'유통·도매'};
const MGMT_SIG={more:'<span class="mn-s mn-more">할인 물량↑</span>',less:'<span class="mn-s mn-less">할인·공급↓</span>'};   // v32.17 병행수입 매입 관점 신호
function mgmtCardHtml(s,tag){
  const ex=s&&s.extract; if(!ex||!Array.isArray(ex.mgmt_notes)) return '';
  const per=perKo((ex.period||'').split(/;| ended/)[0]);
  const rows=ex.mgmt_notes.map(n=>`<div class="mn-row"><span class="mn-t mn-${esc(n.topic)}">${MGMT_TOPIC[n.topic]||esc(n.topic)}</span><div class="mn-b">${esc(n.ko||'')}${MGMT_SIG[n.sig]||''}
    <details><summary>원문</summary><q>${esc(n.quote)}</q></details></div></div>`).join('');
  return `<div class="card"><h3>본사 발언 — ${esc(per||'최근 실적')} <span class="tag">${esc(tag)}</span></h3>${rows||'<div class="na">이번 실적 자료에는 재고·할인·유통 관련 발언 없음</div>'}
    ${why('실적 문서에서 재고 처분·할인·유통 통제 관련 문장을 원문 그대로 뽑음(원문에 있는 문장만 표시) · 요약은 참고용 · 할인 물량↑/할인·공급↓ = 병행수입 매입 관점 신호(Claude 분류)')}</div>`;   // v33.9 접음
}
function renderDetail(t){
  if(String(t).startsWith('krd:')){ renderKrdDetail(t.slice(4)); return; }
  const x=DATA.items.find(i=>i.ticker===t);
  const cur=finCurOf(x);
  let h=`<div class="det-head">${logoImg(x.ticker,true,x.name)}${esc(x.name)} <span class="tk">${esc([flagOf(x.ticker),x.ticker].filter(Boolean).join(' · '))}</span> <span class="tag">${esc(x.group||'')}</span>${staleTag(x.stale_since)}${failTag(x.ticker)}</div>`;
  if(x.note) h+=`<div class="note" style="margin:-6px 0 12px">${esc(x.note)}</div>`;
  if(x.stale_since) h+=`<div class="note" style="margin:-6px 0 12px">${ic('alert',16)} 오늘 수집 실패 — 재무·주가는 ${esc(x.stale_since)} 수집분(이전 값)</div>`;
  else if(failTag(x.ticker)) h+=`<div class="note" style="margin:-6px 0 12px">${ic('alert',16)} 오늘 수집 실패 — 이전 값도 없어 비어 있음(다음 수집 때 채워짐)</div>`;
  const pd=pendOf(x);   // v32.12 공시 분기가 야후보다 새로우면 안내(값은 그대로)
  if(pd) h+=`<div class="note" style="margin:-6px 0 12px">${pendTag(pd)} ${esc(pd.src)} 공시에 ${esc(pd.end)} 끝난 분기 실적이 있지만 야후에는 아직 ${esc(x.q_end||'')} 분기까지 — 분기 매출 전년 대비는 이전 분기 값</div>`;
  const pxCur=x.currency||'', curDiff=pxCur&&finCur(pxCur)!==cur;
  if(!x.fin_source) h+=`<div class="src" style="margin:-4px 0 10px">재무: Yahoo Finance 연간(연결) · 재무 통화 ${esc(cur||'―')}${pxCur==='GBp'?' · 주가 GBp(펜스, 1/100 파운드)':(curDiff?` · 주가 ${esc(pxCur)}(상장 거래소 통화 — 재무 통화와 다름)`:'')}</div>`;
  if(x.fin_source) h+=`<div class="src" style="margin:-4px 0 10px">재무: ${esc(x.fin_source)} · ${x.yahoo_cfs_diff?`주가·실적일: Yahoo · 분기 매출 전년 대비는 야후 연결 기준(종속회사 포함)이라 순위에서 뺌(야후 ${fmt(x.q_yoy_yahoo,1,true)})`:'주가·분기 매출 전년 대비·실적일: Yahoo'}</div>`;
  if(x.group==='글로벌 브랜드') h+=koreaCard(x);
  h+=`<div class="card"><h3>매출 3개년 — 연간 (${cur}) · 증감은 직전 결산연도 대비</h3>`;
  if(x.fy.length){
    const mx=Math.max(...x.fy.map(y=>y.rev||0));
    x.fy.forEach(y=>{
      const w=y.rev?Math.max(y.rev/mx*100,8):0;
      h+=`<div class="bar-row"><div class="lb" title="${ym(y.end)}결산">${ym(y.end)}결산</div>
      <div class="bar-wrap"><div class="bar" style="width:${w}%"></div>
      <div class="bar-val">${moneyShort(y.rev,cur)} ${y.rev_yoy!=null?fmt(y.rev_yoy,1,true):''}</div></div></div>`;
    });
  } else h+=`<div class="na">미확인(소스 조회 실패)</div>`;
  if(cur!=='KRW' && x.fy.length){   // v32.9 외화 실적은 모두 원화 환산 참고값
    const ly=x.fy[x.fy.length-1], k=krwOf(ly.rev,cur), f=(DATA.fx||{})[cur];
    if(k!=null) h+=`<div class="note" style="margin-top:6px">원화 환산 ≈ ${moneyShort(k,'KRW')} (${ym(ly.end)}결산 · 최근 환율 ${fxMul(cur)} ${esc(cur)} = ${wonR(f.rate*fxMul(cur))}원 기준, 참고용)</div>`;
  }
  h+=`</div>`;
  h+=`<div class="card"><h3>수익성 추이 — 연간</h3><table><tr><th>결산월</th><th>매출총이익률</th><th>영업이익률</th></tr>`;
  x.fy.forEach(y=>{
    h+=`<tr><td>${ym(y.end)}</td>
    <td>${y.gm_pct!=null?mnum(y.gm_pct)+'%':'―'}</td>
    <td>${y.op_pct!=null?mnum(y.op_pct)+'%':'―'}</td></tr>`;
  });
  h+=`</table></div>`;
  h+=`<div class="card"><h3>재고</h3>${x.q_inv_yoy!=null&&!x.yahoo_cfs_diff?`
  <div class="kv"><span class="k">최근 분기 <span class="na">(1년 전 같은 분기와 비교)</span></span><span>${ym(x.q_inv_date)} vs ${ym(x.q_inv_prev_date)}</span></div>
  <div class="kv"><span class="k">분기 재고자산</span><span>${money(x.q_inv,cur)}</span></div>
  <div class="kv"><span class="k">재고 증감(같은 분기)</span><span>${fmtInv(x.q_inv_yoy)}</span></div>
  <div class="kv"><span class="k">매출 증감(같은 분기)</span><span>${x.q_inv_rev_yoy!=null?fmt(x.q_inv_rev_yoy,1,true):'<span class="na">야후 분기 매출 없음</span>'}</span></div>
  <div class="note" style="margin:4px 0 8px">아래는 연간 결산 기준</div>`:''}
  <div class="kv"><span class="k">기준 시점</span><span>${x.inv_date||'―'}${x.inv_prev_date?' (전년비교: '+x.inv_prev_date+')':''}</span></div>
  <div class="kv"><span class="k">재고자산</span><span>${money(x.inventory,cur)}</span></div>
  <div class="kv"><span class="k">재고 증감(전년 대비)</span><span>${fmtInv(x.inv_yoy)}</span></div>
  <div class="kv"><span class="k">재고/매출 비율</span><span>${x.inv_sales_pct!=null?x.inv_sales_pct.toFixed(1)+'%':'―'}</span></div>
    <div class="kv"><span class="k">재고일수 <span class="na">(재고÷연간 매출원가×365)</span></span><span>${(()=>{const fy=x.fy.length?x.fy[x.fy.length-1]:{};const d=dioOf(x.inventory,fy.rev,fy.gp,null);return d!=null?Math.round(d)+'일':'―';})()}</span></div></div>`;

  /* 연결된 국내 법인 (Phase 6) */
  ((KRD&&KRD.entities)||[]).filter(e=>e.link===t).forEach(e=>{ h+=compareCard(x,e); h+=krdCard(e,true); });

  /* 지표 추이 (히스토리 축적) */
  h+=`<div class="card"><h3>지표 추이 <span class="tag2">축적 데이터</span></h3>`;
  const hs=(HIST&&HIST.tickers&&HIST.tickers[t])?HIST.tickers[t]:[];
  if(hs.length<3){
    h+=`<div class="na">축적 중 — 현재 ${hs.length}점(3점부터 추이)</div>`;   // v33.9 짧게
  } else {
    // v32.12 변화 없는 지표는 그래프 대신 한 줄, 재고 YoY는 늘면 짙은 주황·줄면 파랑(매출·이익률과 반대)
    const metrics=[["inv_yoy","재고 전년 대비","%",1,1],["gm_pct","매출총이익률","%"],["latest_q_yoy","분기 매출 전년 대비","%",0,1],["rev_yoy","연간 매출 전년 대비","%",0,1]];   // 5번째 = 성장률(부호 항상)
    const flat=[]; let drawn=0;
    metrics.forEach(([k,label,unit,upBad,sg])=>{
      const nv=v=>sg?pp(v):mnum(v)+unit;   // v33 D9: 성장률은 +·− 부호(pp), GM은 수준값
      const pts=hs.filter(p=>p[k]!=null);
      if(pts.length<2) return;
      const vals=pts.map(p=>p[k]);
      const first=pts[0], last=pts[pts.length-1];
      const delta=last[k]-first[k];
      if(Math.abs(delta)<0.05){ flat.push(`${label} ${nv(last[k])}`); return; }
      drawn++;
      const good=upBad?delta<0:delta>0;
      h+=`<div class="krhead trend" style="margin-top:8px"><span class="krname">${label}</span>
        <span class="krval">${nv(last[k])}
        <span class="kryoy ${good?'pos':'neg'}">${delta>=0?'▲':'▼'}${Math.abs(delta).toFixed(1)}p</span></span></div>
        <div class="krmeta">${first.date} → ${last.date} · ${pts.length}점</div>
        ${spark(vals,260,26,upBad)}`;
    });
    if(!drawn) h+=`<div class="na">${flat.length?`첫 기록(${mdTxt(hs[0].date)}) 이후 변화 없음 — 새 결산이 반영되면 바뀝니다`:'추이를 그릴 값 없음'}</div>`;
    if(flat.length) h+=`<div class="krmeta" style="margin-top:${drawn?8:4}px">${drawn?'변화 없음: ':''}${flat.join(' · ')}</div>`;
    h+=`<div class="note">첫 기록 대비 변화(▲▼ p) · 값은 야후 파이낸스 스냅샷 그대로${x.yahoo_cfs_diff?' · <b class="neg">야후 연결 기준(종속회사 포함)이라 위 DART 별도 수치와 다름</b>':''}</div>`;
  }
  h+=`</div>`;

  const s=segOf(t);
  const segCur=curCode((s&&s.extract&&s.extract.currency)||cur);   // 공시 추출 통화(없으면 재무 통화)
  let segEntry=(SEGS.items||{})[t];
  if(!segEntry && isKR(t)) segEntry={error:"공시 추출 미대상 — 한국 상장(DART), 향후 확장"};
  const segTag=(segEntry&&/^IR/.test(segEntry.source||''))?'IR 추출':'공시 추출';
  const segPer=(s&&s.extract&&/누적|^FY|^\d+M |^H[12]\b|half|six months|nine months/i.test(s.extract.period||''))?'최근 공시 기간(누적)':'최근 분기';   // v33.8 제냐 H1(반기)
  h+=`<div class="card"><h3>지역 분해 — ${segPer}, 당기 vs 전년 <span class="tag">${segTag}</span></h3>`;
  if(s&&s.extract.regions&&s.extract.regions.length){
    const regsAll=s.extract.regions.filter(r=>r.revenue!=null);
    const totalOnly=regsAll.length>0&&regsAll.every(r=>/total|전체|합계|consolidated/i.test(r.name||""));
    let bars;
    if(totalOnly){
      const tt=regsAll[0];
      const yoy=tt.yoy_pct!=null?' '+fmt(tt.yoy_pct,1,true):'';
      bars=`<div class="na">지역별 매출액 미공시 — 이 회사는 지역 분해 금액을 공시하지 않습니다(성장률만 공시하는 경우 하단 주석 참조)</div>
      <div class="kv"><span class="k">분기 총매출</span><span>${segMoney(tt.revenue,segCur)}${yoy}</span></div>`;
    } else {
      bars=pairBars(s.extract.regions,"당기","전년",segCur);
    }
    h+=bars||`<div class="na">미확인(공시에 수치 미기재)</div>`;
    const pctOnly=s.extract.regions.filter(r=>r.revenue==null&&(r.yoy_pct!=null||r.cn_yoy_pct!=null)&&!/total|전체|합계|consolidated/i.test(r.name||''));
    if(pctOnly.length) h+=`<div class="note">금액 없이 증감률만 공시: ${pctOnly.map(r=>{
      const v=r.cn_yoy_pct!=null?r.cn_yoy_pct:r.yoy_pct, lab=r.cn_yoy_pct!=null?'환율 제외 ':'';
      return `${esc(r.name)} ${lab}${fmt(v,1,true)}`;}).join(' · ')}</div>`;
    let noteTxt="기준: "+(s.extract.period||"―");
    if(s.extract.prev_period) noteTxt+=" · 전년: "+s.extract.prev_period;
    const nc=noteClean(s.extract.notes); if(nc) noteTxt+=" · "+nc;
    const anyCn=[...(s.extract.regions||[]),...(s.extract.channels||[])].some(r=>r.cn_yoy_pct!=null);
    h+=`<div class="note">${esc(noteTxt)}</div>`+why(`진한 바=당기 / 연한 바=전년 · [역산]=공시에 전년 수치 미기재로 전년 대비 증감률에서 계산${anyCn?'<br>환율 제외 = 현지 통화 기준 증감(회사 공시값) — 보고 통화 증감과 차이가 크면 환율 영향이 큰 것':''}`);   // v33.9 기준 줄은 그대로, 범례는 접음
    if(s.source) h+=`<div class="src">출처: ${esc(s.source)}</div>`;
  } else {
    h+=`<div class="na">미확인${segEntry&&segEntry.error?'('+esc(segEntry.error)+')':'(공시에 지역 분해 미기재)'}</div>`;
  }
  h+=`</div>`;
  h+=`<div class="card"><h3>채널 분해 (DTC/도매) — ${segPer} <span class="tag">${segTag}</span></h3>`;
  if(s&&s.extract.channels&&s.extract.channels.length){
    const bars=pairBars(s.extract.channels,"당기","전년",segCur);
    h+=bars||`<div class="na">미확인(공시에 수치 미기재)</div>`;
  } else {
    h+=`<div class="na">미확인${segEntry&&segEntry.error?'('+esc(segEntry.error)+')':'(공시에 채널 분해 미기재)'}</div>`;
  }
  h+=`</div>`;
  h+=mgmtCardHtml(s,segTag);   // v32.15 본사 발언

  if(t==='DKS'&&s&&s.extract.sub_segments&&s.extract.sub_segments.length){
    const qtr=isQtrPeriod(s.extract.period);   // v32.12 분기 실적 자료일 때만 '딕스(본체)' — 프로포마 합산표 등은 공시 이름 그대로
    h+=`<div class="card"><h3>부문 분해: 딕스 / 풋락커 <span class="tag">공시 추출</span></h3>
    <div class="tblwrap"><table><tr><th>부문</th><th>매출</th><th>전년</th><th>전년 대비</th><th>부문이익</th><th>재고</th></tr>`;   // v33 휴대폰 폭보다 넓으면 표만 가로 스크롤(390px에서 26px 넘침)
    s.extract.sub_segments.forEach(ss=>{
      h+=`<tr><td>${ss.name==="DICK'S"?(qtr?'딕스(본체)':esc(ss.name)):(qtr?'풋락커(부문)':esc(ss.name))}</td>
      <td>${segMoney(ss.revenue,segCur)}</td>
      <td>${segMoney(ss.prev_revenue,segCur)}</td>
      <td>${fmt(ss.yoy_pct!=null?ss.yoy_pct:(ss.revenue!=null&&ss.prev_revenue?(ss.revenue/ss.prev_revenue-1)*100:null),1,true)}</td>
      <td>${segMoney(ss.segment_profit,segCur)}</td>
      <td>${segMoney(ss.inventory,segCur)}</td></tr>`;
    });
    h+=`</table></div>`;
    if(s.extract.period) h+=`<div class="note">기준: ${esc(s.extract.period)}${qtr?'':' — 분기 실적 자료가 아니어서 본체·부문으로 나눠 보지 않음'}</div>`;
    const fl=s.extract.sub_segments.find(z=>z.name==='Foot Locker');
    if(fl&&fl.proforma_comp_pct!=null){
      h+=`<div class="note">풋락커 프로포마 기존점 매출: ${pp(fl.proforma_comp_pct)}
      · 풋락커는 FY26 4분기까지 공식 comp 집계 미포함(프로포마 기준)</div>`;
    }
    h+=`</div>`;
  }

  h+=`<div class="card"><h3>(부지표) 주가</h3>
  <div class="kv"><span class="k">현재가</span><span>${priceTxt(x)}</span></div>
  <div class="kv"><span class="k">52주 고점 대비</span><span>${fmtS(x.off_high_pct,1)}</span></div></div>`;   // v33 주가만 색 없이 부호(한국 증권 앱은 빨강 = 상승)
  h+=naverDetailCard(t);
  h+=newsCard(t);
  document.getElementById('detBody').innerHTML=h;
}

/* ── 캘린더 (A안: 2개월 달력 + 90일 목록) ── */
let calSel=null;
/* ── 해외 세일 시즌(v32.8) — 규칙으로 계산하는 날짜(확정)와 해마다 발표되는 행사(예상) ── */
const nthDow=(y,m,dow,n)=>{const d=new Date(y,m,1); return new Date(y,m,1+(dow-d.getDay()+7)%7+7*(n-1));};   // m: 0=1월, dow: 0=일
const lastDow=(y,m,dow)=>{const d=new Date(y,m+1,0); return new Date(y,m,d.getDate()-(d.getDay()-dow+7)%7);};
const addD=(d,n)=>new Date(d.getFullYear(),d.getMonth(),d.getDate()+n);
function saleEvents(y){
  const bf=addD(nthDow(y,10,4,4),1);   // 블랙프라이데이 = 미국 추수감사절(11월 넷째 목요일) 다음 날
  return [
    {s:new Date(y,0,1),e:new Date(y,0,3),nm:'일본 신년 세일(하츠우리)',sh:'일본 신년',cc:'JP',k:'확정',note:'백화점·편집숍 신년 할인 — 겨울 재고 정리'},
    {s:nthDow(y,0,3,2),e:addD(nthDow(y,0,3,2),27),nm:'프랑스 겨울 세일(솔드)',sh:'프랑스 겨울',cc:'FR',k:'확정',note:'법정 세일 4주(1월 둘째 수요일 시작) — 유럽 FW 재고 매입 시점'},
    {s:nthDow(y,0,6,1),e:addD(nthDow(y,0,6,1),41),nm:'이탈리아 겨울 세일(살디)',sh:'이탈리아 겨울',cc:'IT',k:'예상',note:'주(州)마다 시작일이 달라 보통 1월 첫 토요일 전후'},
    {s:new Date(y,5,1),e:new Date(y,5,18),nm:'중국 618 쇼핑 축제',sh:'618',cc:'CN',k:'확정',note:'징둥·티몰 상반기 최대 할인(6/18 마감)'},
    {s:lastDow(y,5,3),e:addD(lastDow(y,5,3),27),nm:'프랑스 여름 세일(솔드)',sh:'프랑스 여름',cc:'FR',k:'확정',note:'법정 세일 4주(6월 마지막 수요일 시작) — 유럽 SS 재고 매입 시점'},
    {s:nthDow(y,6,6,1),e:addD(nthDow(y,6,6,1),41),nm:'이탈리아 여름 세일(살디)',sh:'이탈리아 여름',cc:'IT',k:'예상',note:'7월 첫 토요일 전후 시작(주마다 다름)'},
    {s:new Date(y,6,1),e:new Date(y,6,15),nm:'일본 여름 세일',sh:'일본 여름',cc:'JP',k:'예상',note:'백화점·쇼핑몰 7월 초 시작'},
    {s:new Date(y,6,8),e:new Date(y,6,11),nm:'아마존 프라임데이',sh:'프라임데이',cc:'US',k:'예상',note:'매년 7월 중순 — 정확한 날짜는 아마존 발표 후 확정'},
    {s:new Date(y,10,1),e:new Date(y,10,11),nm:'중국 광군제(11.11)',sh:'광군제',cc:'CN',k:'확정',note:'알리·티몰 연중 최대 할인, 11/11 당일이 정점'},
    {s:new Date(y,10,1),e:new Date(y,10,30),nm:'코리아세일페스타',sh:'코세페',cc:'KR',k:'예상',note:'국내 유통 할인 행사(11월, 날짜는 매년 발표) — 국내 판매가 경쟁이 세지는 시기'},
    {s:bf,e:addD(bf,3),nm:'블랙프라이데이~사이버먼데이',sh:'블프',cc:'US',k:'확정',note:'미국 온라인 리테일러 연중 최대 할인 — 해외 배송·통관 지연 감안'},
    {s:new Date(y,11,26),e:new Date(y+1,0,5),nm:'영국 박싱데이 세일',sh:'박싱데이',cc:'GB',k:'확정',note:'12/26부터 연초까지 — 영국·유럽 리테일러 시즌 마감 할인'},
  ];
}
const saleAll=today=>[-1,0,1].flatMap(k=>saleEvents(today.getFullYear()+k));
const md2=d=>`${d.getMonth()+1}/${d.getDate()}`;
function buildCal(){
  const today=kstMid();   // v33 한국 날짜 기준(기기 시간대 무관 — 오늘 ③과 같은 날)
  const SALES=saleAll(today), dayKey=ymdL;
  const saleOn=dt=>SALES.filter(e=>dt>=e.s&&dt<=e.e), saleStart=key=>SALES.filter(e=>dayKey(e.s)===key);
  const evs=rows_all().filter(r=>r.earn).map(r=>{const d=new Date(r.earn+'T00:00:00');return {...r,d,dn:Math.round((d-today)/86400000)};}).filter(r=>r.dn>=0&&r.dn<=90).sort((a,b)=>a.dn-b.dn);
  const byDay={}; evs.forEach(r=>{(byDay[r.earn]=byDay[r.earn]||[]).push(r);});
  const months=[0,1].map(k=>new Date(today.getFullYear(),today.getMonth()+k,1));
  let h='';
  months.forEach(m0=>{
    const y=m0.getFullYear(), m=m0.getMonth(); const first=new Date(y,m,1).getDay(); const days=new Date(y,m+1,0).getDate();
    let cells=['일','월','화','수','목','금','토'].map(w=>`<div class="wd">${w}</div>`).join('');
    for(let i=0;i<first;i++) cells+=`<div class="cd"></div>`;
    for(let d=1;d<=days;d++){
      const key=`${y}-${String(m+1).padStart(2,'0')}-${String(d).padStart(2,'0')}`;
      const list=byDay[key]||[]; const isT=key===dayKey(today);   // v33 버그: toISOString()은 한국 자정을 UTC 전날로 바꿔 하루 전 칸이 '오늘'이었음
      const on=saleOn(new Date(y,m,d)), st=saleStart(key), click=list.length||on.length;
      // 칸(13px): 세일 시작은 짧은 이름(굵게 파랑), 실적은 1곳이면 브랜드 이름 한 줄·2곳 이상이면 'N곳' — 전체 이름은 날짜를 누르면 아래 줄·목록에
      const lab=`${m+1}월 ${d}일${isT?' 오늘':''}${list.length?` 실적 ${list.length}곳`:''}${on.length?` 세일 ${on.length}건`:''}`;
      cells+=`<div class="cd${list.length?' has':''}${on.length?' sale':''}${isT?' today':''}${calSel===key?' sel':''}"${click?` data-day="${key}" role="button" tabindex="0" aria-label="${lab}"`:''}><div class="dn">${d}</div>${st.slice(0,1).map(e=>`<div class="ev sl">${esc(e.sh)}</div>`).join('')}${list.length?`<div class="ev">${list.length>1?list.length+'곳':esc(nmBrand(list[0].name))}</div>`:''}</div>`;
    }
    h+=`<div class="cal"><h3>${y}년 ${m+1}월</h3><div class="cgrid">${cells}</div>${calSel&&calSel.startsWith(`${y}-${String(m+1).padStart(2,'0')}`)?`<div class="calday">${calSel.slice(5).replace('-','/')} · ${[(byDay[calSel]||[]).map(r=>r.logo+esc(r.name)).join(', '),saleOn(new Date(+calSel.slice(0,4),+calSel.slice(5,7)-1,+calSel.slice(8,10))).map(e=>'세일 '+esc(e.nm)).join(', ')].filter(Boolean).join(' · ')}</div>`:''}</div>`;
  });
  document.getElementById('calGrid').innerHTML=h;
  document.querySelectorAll('.cd[data-day]').forEach(c=>c.onclick=()=>{const f=document.activeElement===c, k=c.dataset.day; calSel=(calSel===k)?null:k;buildCal(); refocus(f,`.cd[data-day="${k}"]`);});
  // v33 A안: 90일 이내 실적 발표 줄을 누르면 기업 상세(옛 종합 '다가오는 실적 발표'와 같게)
  document.getElementById('calList').innerHTML=evs.length?evs.map(r=>`<button type="button" class="cl" data-go="co:${esc(r.key)}"><span>${calDot(r.dn)}${r.logo}${esc(r.name)}</span><span class="nw">${r.d.getMonth()+1}/${r.d.getDate()} <span class="na">D-${r.dn}</span></span></button>`).join(''):'<div class="na">90일 이내 확인된 일정 없음(미확인 포함)</div>';
  const lim=addD(today,150), up=SALES.filter(e=>e.e>=today&&e.s<=lim).sort((a,b)=>a.s-b.s);
  document.getElementById('saleList').innerHTML=up.length?up.map(e=>{const live=e.s<=today, dn=Math.round(((live?e.e:e.s)-today)/86400000);
    return `<div class="sl-row"><div class="t1"><span>${esc(e.nm)}<span class="sl-k">${e.k}</span></span><span>${md2(e.s)}${+e.e!==+e.s?'~'+md2(e.e):''} <span class="${live?'sl-live':'na'}">${live?'진행 중 · '+(dn>0?dn+'일 남음':'오늘 끝'):'D-'+dn}</span></span></div><div class="t2">${esc(e.note)}</div></div>`;}).join('')
    +'<div class="note" style="margin-top:6px">확정 = 법정·고정 규칙으로 계산한 날짜 · 예상 = 해마다 주최 측이 발표(지난해 패턴 기준) · 해외 직구 배송·통관 기간(보통 1~3주)을 감안해 미리 결제</div>'
    :'<div class="na">150일 이내 세일 없음</div>';
}

/* ── 뉴스 (v11: 그룹 필터 + NEW 배지 + 날짜별) ── */
const NEWS_FILTERS = [
  {id:"all",   label:"전체"},
  {id:"sep1",  label:"브랜드 ›", sep:true},
  {id:"b:sports",  label:"스포츠·아웃도어"},
  {id:"b:fashion", label:"패션"},
  {id:"b:luxury",  label:"명품"},
  {id:"b:retail",  label:"유통·그외"},
  {id:"sep2",  label:"산업 ›", sep:true},
  {id:"i:sports",  label:"스포츠 트렌드"},
  {id:"i:fashion", label:"패션·명품 시장"},
  {id:"i:retail",  label:"멀티브랜드 유통"},
  {id:"i:customs", label:"통관·상표권"},
  {id:"i:logistics", label:"물류·운임"},   // v33.4 news_monitor v2.14
  {id:"sep3",  label:"국내 비교 ›", sep:true},
  {id:"b:kr_peer", label:"유통사"},
  {id:"b:kr_fb",   label:"패션 브랜드"},
];
let newsFilter="all";
function newsMatch(it){
  if(newsFilter==="all") return true;
  const [scope,grp]=newsFilter.split(":");
  if(scope==="b") return it.scope==="brand" && it.group===grp;
  if(scope==="i") return it.scope==="industry" && it.key===grp;
  if(scope==="k") return it.scope==="brand" && it.key===grp;   // 검색 관심도 카드에서 브랜드 하나로 거른 경우
  return true;
}
function buildNewsChips(){
  const el=document.getElementById('newsChips');
  el.innerHTML=NEWS_FILTERS.map(f=>f.sep
    ? `<span class="chip sep">${f.label}</span>`
    : `<button type="button" class="chip${newsFilter===f.id?' on':''}" data-f="${f.id}" aria-pressed="${newsFilter===f.id}">${f.label}</button>`).join('');
  el.querySelectorAll('.chip[data-f]').forEach(c=>{
    c.onclick=()=>{ const f=document.activeElement===c; setNewsFilter(c.dataset.f); refocus(f,`#newsChips .chip[data-f="${c.dataset.f}"]`); };
  });
}
function setNewsFilter(f){   // v33 S2: 고른 필터를 지금 기록(nf)에도 저장 — 새로고침·앞으로 가기에서 풀었던 'k:' 필터가 다시 걸리지 않게(기록 수는 그대로)
  newsFilter=f; NS_SHOW=NS_PAGE; buildNewsChips(); safe(buildNews,'뉴스','mk-news');
  const s=history.state; if(s&&s.tab==='market'&&s.chip==='news') hRep({...s,nf:f,ns:NS_SHOW});
}
// v32.11 기본 보기(칩 '전체'): 오늘 전체 + 최근 7일 ★3 — ★ 기준은 10/13 모델 비교 뒤 조정
const NEWS_MIN_IMP=3, NEWS_DAYS=7;
let NEWS_MORE={}, NEWS_BUILT=false;
// v33.3 올해가 아닌 날짜엔 연도 — '2025.12.30(화)'(올해는 '10/9(금)' 그대로). 올해(한국)는 1분에 한 번만 다시 셈
let NEWS_YR=0, NEWS_YT=0;
const newsYear=()=>{ const n=Date.now(); if(!NEWS_YR||n-NEWS_YT>60000){ NEWS_YT=n; NEWS_YR=+kstToday().slice(0,4); } return NEWS_YR; };
const newsDateLbl=d=>{ const t=new Date(d+'T00:00:00'); if(isNaN(t)) return d; const w=`(${'일월화수목금토'[t.getDay()]})`;
  return t.getFullYear()===newsYear()?`${t.getMonth()+1}/${t.getDate()}${w}`:`${t.getFullYear()}.${t.getMonth()+1}.${t.getDate()}${w}`; };
// v32.12 기사 날짜 한국식 '10/9(금)' — pubDate(영문 GMT)를 한국 날짜로, 못 읽으면 원문 앞부분
let KST_DAY=null;   // v33.1 형식기는 처음 쓸 때 한 번만 만듦(기사마다 새로 만들면 검색 결과·더 보기가 느림 — 결과 글자는 같음)
const pubKr=p=>{ const t=new Date(p); if(isNaN(t)) return String(p).slice(0,16); if(!KST_DAY) KST_DAY=new Intl.DateTimeFormat('sv-SE',{timeZone:'Asia/Seoul'}); return newsDateLbl(KST_DAY.format(t)); };
const newsDay=it=>/^\d{4}-\d{2}-\d{2}$/.test(it.orig_date||'')?newsDateLbl(it.orig_date):it.pubDate?pubKr(it.pubDate):(it.first_seen?newsDateLbl(it.first_seen):'');   // 기사 줄 날짜 = 원문 날짜(v33.3, news_monitor가 원문 페이지에서 확인) → 구글 게재일 → 수집일 — 모든 화면 같게
function newsItemHtml(it,more){   // more = '더 보기'로 새로 보인 기사 표시(초점 옮길 곳)
  const stars='★'.repeat(Math.max(1,Math.min(3,it.importance||1)));
  const tag=it.scope==="brand"?it.label:(it.label||it.key), day=newsDay(it);
  return `<div class="nitem"${more?` data-more="${more}"`:''}>
      <div class="nsum"><span class="stars">${stars}</span> <a href="${esc(safeUrl(it.link))}" target="_blank" rel="noopener">${esc(it.summary||it.title)}</a></div>
      <div class="nmeta"><span class="ntag">${esc(tag)}</span>${esc(it.source||'')}${day?' · '+esc(day):''}</div>
    </div>`;
}
function newsAll(b){ const f=document.activeElement===b; setNewsFilter('all'); refocus(f,'#newsChips .chip[data-f="all"]'); }   // v33 키보드 초점 = 칩 '전체'
const newsKeyName=k=>(((NEWS&&NEWS.items)||[]).find(i=>i.key===k&&i.label)||{}).label||(nvAll().find(b=>b.news===k)||{}).name||k;   // 'k:' 필터 이름(회사·브랜드)
/* v33.1 지난 뉴스 검색 — 최근 기사(NEWS.items) + 1년 보관(news_archive.json, news_monitor v2.12). 보관 파일은 검색창을 처음 누를 때 한 번 받고
   찾을 목록은 800건씩 나눠 만듦(1년치 약 1만 건에서도 입력이 멈추지 않게). 같은 제목은 검색할 때 최신 1건(별점은 그중 가장 높은 것) */
const NS_PAGE=30, NS_CHUNK=800;
let NEWS_Q='', NS_SHOW=NS_PAGE, NS_SHOWN=-1, NS_ST='', NS_RROWS=null, NS_AROWS=null, NS_IDX=null, NS_MEMO=null, NS_T=0, NS_COMP=false, NS_RESTORE=null;
const NQ_MEM={};   // 휴대폰 '뒤로'로 떠날 때 아직 반영 안 된 입력(0.2초 안) — 앞으로 가기로 그 기록에 오면 이것
const nsQ=v=>String(v||'').normalize('NFC').replace(/\s+/g,' ').trim().slice(0,60).replace(/[\ud800-\udbff]$/,'');   // 60자에서 잘린 이모지 반쪽은 뺌
const nsFold=s=>String(s==null?'':s).normalize('NFC').toLowerCase().replace(/[À-ɏ]/g,c=>c.normalize('NFD')[0]);   // 대소문자·악센트(é→e) 무시 — 글자 수 그대로(강조 위치)
const nsTk=t=>String(t||'').slice(0,300).replace(/\s+-\s+[^-]{1,40}$/,'').toLowerCase().replace(/[^0-9a-z가-힣]/g,'').slice(0,40);   // 같은 기사 제목 키 = news_monitor title_key
const nsS=v=>typeof v==='string'?v:(typeof v==='number'&&isFinite(v)?String(v):'');   // 기사 칸은 글자·숫자만 — 이상한 기사 하나가 검색 전체를 깨지 않게
const nsYmd=d=>{ const m=/^(\d{4})-(\d{2})-(\d{2})/.exec(d||''); return m?`${m[1]}.${+m[2]}.${+m[3]}`:''; };
const nsEnc=s=>{ try{ return encodeURIComponent(s); }catch(e){ return encodeURIComponent(String(s).replace(/[\ud800-\udfff]/g,'')); } };   // 짝 없는 대리 문자면 빼고
function nsRow(it){   // 찾을 목록 한 줄 = 칸을 고른 기사 사본 + 수집일·별점 + 찾을 글자(요약·제목·브랜드·매체·키) + 제목 키
  if(!it||typeof it!=='object') return null;
  const x={}; ['id','scope','key','label','group','summary','title','link','source','pubDate','first_seen','orig_date'].forEach(k=>{ x[k]=nsS(it[k]); });   // v33.3 원문 날짜
  if(!x.id) return null;
  x.importance=Math.max(1,Math.min(3,Math.round(+nsS(it.importance))||1));
  return {it:x, d:x.first_seen, m:x.importance, h:nsFold([x.summary,x.title,x.label,x.source,x.key].join('\n')), tk:nsTk(x.title)};
}
function nsLoad(){   // 보관 파일 받기(한 번) → 찾을 목록을 나눠 만듦. 실패하면 '다시 시도'·검색창 다시 누르기로 다시
  if(NS_ST==='loading'||NS_ST==='ok') return;
  NS_ST='loading';
  fetch('news_archive.json?v='+nsEnc((NEWS&&NEWS.generated_at)||''))
    .then(r=>{ if(!r.ok) throw new Error('HTTP '+r.status); return r.json(); })
    .then(d=>new Promise(done=>{ const L=(d&&Array.isArray(d.items))?d.items:[], out=[]; let i=0;
      const step=()=>{ const e=Math.min(L.length,i+NS_CHUNK); for(;i<e;i++){ const r=nsRow(L[i]); if(r) out.push(r); } if(i<L.length) setTimeout(step,0); else done(out); };
      step(); }))
    .then(rows=>new Promise(done=>{ NS_AROWS=rows; NS_IDX=null; setTimeout(()=>{ nsIndex(); NS_ST='ok'; done(); },0); }))   // 합친 목록도 따로 한 번(첫 검색 때 멈추지 않게)
    .catch(e=>{ console.warn('뉴스 보관 파일을 못 받음:',e); NS_ST='fail'; NS_AROWS=null; NS_IDX=null; })
    .then(()=>{ NS_MEMO=null; if(NEWS_Q) nsRefresh(); else NS_RESTORE=null; });
}
function nsIndex(){   // 찾을 목록 — 최근 기사 먼저, 같은 id는 1건(별점은 높은 것), 최신순(수집일·별점)
  if(NS_IDX) return NS_IDX;
  if(!NS_RROWS) NS_RROWS=((NEWS&&NEWS.items)||[]).map(nsRow).filter(Boolean);
  const by=new Map(), out=[];
  NS_RROWS.concat(NS_AROWS||[]).forEach(r=>{ const p=by.get(r.it.id); if(p){ if(r.m>p.m) p.m=r.m; return; } by.set(r.it.id,r); out.push(r); });
  out.sort((a,b)=>a.d<b.d?1:a.d>b.d?-1:b.m-a.m);   // localeCompare 대신 문자열 비교(빠름)
  return NS_IDX=out;
}
function nsRows(q){   // 검색어·칩에 맞는 기사 — 같은 제목(다른 날짜·브랜드로 다시 잡힌 같은 기사)은 최신 1건, 별점은 그중 가장 높은 것. 마지막 결과 기억
  const idx=nsIndex(), key=q+'\u0001'+newsFilter;
  if(NS_MEMO&&NS_MEMO.key===key&&NS_MEMO.idx===idx) return NS_MEMO;
  const terms=[...new Set(nsFold(q).split(' ').filter(Boolean))], seen=new Map(), rows=[];
  idx.forEach(r=>{ if(!newsMatch(r.it)||!terms.every(t=>r.h.includes(t))) return;
    const k=r.tk?seen.get(r.tk):null; if(k){ if(r.m>k.mx) k.mx=r.m; return; }
    const o={r,mx:r.m}; if(r.tk) seen.set(r.tk,o); rows.push(o); });
  return NS_MEMO={key,idx,terms,rows};
}
function nsMark(s,terms){   // 찾은 낱말 <mark> — 원문 조각마다 이스케이프. 대소문자 바꾸기로 글자 수가 달라지면 강조 없이
  s=String(s==null?'':s); const f=nsFold(s); if(f.length!==s.length) return esc(s);
  const R=[]; terms.forEach(t=>{ for(let i=f.indexOf(t);i>=0;i=f.indexOf(t,i+t.length)) R.push([i,i+t.length]); });
  if(!R.length) return esc(s);
  R.sort((a,b)=>a[0]-b[0]); const M=[R[0].slice()];
  R.slice(1).forEach(r=>{ const l=M[M.length-1]; if(r[0]<=l[1]) l[1]=Math.max(l[1],r[1]); else M.push(r.slice()); });
  let h='', p=0; M.forEach(([a,b])=>{ h+=esc(s.slice(p,a))+'<mark>'+esc(s.slice(a,b))+'</mark>'; p=b; });
  return h+esc(s.slice(p));
}
function nsItemHtml(o,terms,more){   // o = {r: 찾을 목록 줄, mx: 같은 제목 중 가장 높은 별점}
  const it=o.r.it, main=it.summary||it.title, fm=nsFold(main), ft=it.summary?nsFold(it.title):'', day=newsDay(it);
  const showT=!!ft&&terms.some(t=>!fm.includes(t)&&ft.includes(t));   // 요약에 없는 낱말을 원문 제목에서 찾았으면 제목도
  const tag=it.scope==='brand'?it.label:(it.label||it.key);
  return `<div class="nitem"${more?' data-more="ns"':''}>
      <div class="nsum"><span class="stars">${'★'.repeat(o.mx)}</span> <a href="${esc(safeUrl(it.link))}" target="_blank" rel="noopener">${nsMark(main,terms)}</a></div>`
    +(showT?`<div class="ntitle">${nsMark(it.title,terms)}</div>`:'')
    +`<div class="nmeta"><span class="ntag">${nsMark(tag,terms)}</span>${nsMark(it.source,terms)}${day?' · '+esc(day):''}</div>
    </div>`;
}
function newsSearch(el){   // 검색 결과 = 머리 줄(건수·기간·칩) + 월별 기사 + 더 보기 + Google 뉴스
  const {terms,rows}=nsRows(NEWS_Q), n=rows.length, idx=nsIndex();
  const okD=d=>/^\d{4}-\d{2}-\d{2}$/.test(d)&&!isNaN(Date.parse(d));   // 깨진 수집일(0000-00-00 등)은 기간 시작일로 안 씀
  let o=idx.length-1; while(o>=0&&!okD(idx[o].d)) o--;
  const A=(NEWS&&NEWS.status&&NEWS.status.archive)||{}, since=nsYmd(NS_ST==='ok'&&o>=0?idx[o].d:A.since);
  const f=newsFilter, fl=f==='all'?'':(f.startsWith('k:')?newsKeyName(f.slice(2)):((NEWS_FILTERS.find(x=>x.id===f)||{}).label||f));
  const rng=NS_ST==='ok'?(since?`${since} 이후`:'지난 1년'):(NS_ST==='fail'?'최근 기사만 — 지난 기사를 못 불러옴':'최근 기사만 — 지난 1년 기사 불러오는 중…');
  let h=`<div class="note ns-st"><span>‘${esc(NEWS_Q)}’ ${n?n+'건':'없음'} · ${rng}${fl?` · ${esc(fl)}만`:''}</span>`
    +(fl?`<button type="button" class="chip" onclick="newsAll(this)">전체에서 찾기</button>`:'')
    +(NS_ST==='fail'?`<button type="button" class="chip" onclick="nsRetry(this)">다시 시도</button>`:'')+`</div>`;
  if(!n) h+=`<div class="na">${NS_ST==='ok'||NS_ST==='fail'?'맞는 기사가 없습니다 — 낱말을 줄이거나 다른 말(영문 브랜드명 등)로 찾아 보세요':'지난 기사를 불러오는 중입니다'}</div>`;
  let cur='';
  rows.slice(0,NS_SHOW).forEach((x,i)=>{
    const m=okD(x.r.d)&&/^(\d{4})-(\d{2})/.exec(x.r.d), g=m?`${m[1]}년 ${+m[2]}월`:'날짜 미상';
    if(g!==cur){ cur=g; h+=`<div class="ndate">${g}</div>`; }
    h+=nsItemHtml(x,terms,NS_SHOW>NS_PAGE&&i>=NS_SHOW-NS_PAGE);
  });
  if(n>NS_SHOW) h+=`<button type="button" class="nmore" onclick="nsMore(this)">${Math.min(NS_PAGE,n-NS_SHOW)}건 더 보기 (남은 ${n-NS_SHOW}건) ${ic('down',16)}</button>`;
  h+=`<a class="nmore" href="${esc('https://news.google.com/search?q='+nsEnc(NEWS_Q)+'&hl=ko&gl=KR&ceid=KR%3Ako')}" target="_blank" rel="noopener">Google 뉴스에서 ‘${esc(NEWS_Q)}’ 더 찾기 ${ic('right',16)}</a>`;
  el.innerHTML=h; NS_SHOWN=n;
  setText('newsSrchLive',NS_ST==='loading'&&!n?'':`검색 결과 ${n}건`);
}
function nsMem(q){   // 지금 기록에 검색어·펼친 수 저장 — 뒤로·새로고침에도 그대로(기록 수는 그대로)
  const s=history.state; if(s&&s.tab==='market'&&s.chip==='news') hRep({...s,nq:q,ns:NS_SHOW});
  if(ROUTE.k) delete NQ_MEM[ROUTE.k];
}
function nsSet(v,composing){   // 검색어 바뀜 → 다시 그림 + 기록에 저장
  const q=nsQ(v); if(q===NEWS_Q) return;
  if(q) nsLoad();
  // 한글 조합 중(받침이 다음 글자로 옮겨 가기 전, 예: '아딛')에 0건이면 지금 화면 그대로 — '없음'이 글자마다 깜빡이지 않게. 조합이 끝나면 다시 찾음
  if(composing&&q&&!nsRows(q).rows.length&&(!NEWS_Q||NS_SHOWN>0)) return;
  NEWS_Q=q; NS_SHOW=NS_PAGE;
  safe(buildNews,'뉴스','mk-news');
  nsMem(q);
}
function nsFlush(){ if(!NS_T) return; clearTimeout(NS_T); NS_T=0; const i=document.getElementById('newsSearch'); if(i) nsSet(i.value,false); }   // 0.2초 안 입력을 지금 반영(화면을 떠나기 전)
function nsRefresh(){   // 보관 기사가 온 뒤 다시 그림 — 결과 안 키보드 초점은 같은 기사로, 뒤로 와서 기다리던 스크롤 자리로
  const box=document.getElementById('newsBody'), a=document.activeElement, inBox=!!(a&&box&&a!==box&&box.contains(a));
  const href=inBox&&a.getAttribute('href'), tx=inBox&&(a.textContent||'').trim();
  safe(buildNews,'뉴스','mk-news');
  if(inBox){ const n=(href&&[...box.querySelectorAll('a[href]')].find(x=>x.getAttribute('href')===href))||[...box.querySelectorAll('button,a[href]')].find(x=>(x.textContent||'').trim()===tx)||document.getElementById('newsSearch');
    if(n) try{ n.focus({preventScroll:true}); }catch(e){} }
  const R=NS_RESTORE; NS_RESTORE=null;
  if(R&&R.k===ROUTE.k) requestAnimationFrame(()=>scrollBox().scrollTo(0,R.y));
}
function nsMore(b){ const f=document.activeElement===b; NS_SHOW+=NS_PAGE; safe(buildNews,'뉴스','mk-news'); nsMem(NEWS_Q); refocus(f,'#newsBody [data-more="ns"] a'); }   // 펼친 뒤 키보드 초점 = 새로 보인 첫 기사
function nsRetry(b){ const f=document.activeElement===b; NS_ST=''; nsLoad(); safe(buildNews,'뉴스','mk-news'); refocus(f&&KB_LAST,'#newsSearch'); }   // 휴대폰에서 누르면 자판이 뜨지 않게(키보드로 누를 때만 검색창으로)
function newsMore(k,b){ const f=document.activeElement===b; NEWS_MORE[k]=1; buildNews(); refocus(f,`#newsBody [data-more="${k}"] a`); }   // v33 펼친 뒤 키보드 초점 = 새로 보인 첫 기사
function buildNews(){
  NEWS_BUILT=true;
  const el=document.getElementById('newsBody');
  if(NEWS_Q) return newsSearch(el);   // v33.1 검색 중이면 검색 결과
  NS_SHOWN=-1; setText('newsSrchLive','');
  if(!NEWS||!NEWS.items){
    el.innerHTML='<div class="na">뉴스 데이터 없음 — 뉴스 워크플로우(update-news) 첫 실행 전이거나 수집 실패(미확인)</div>';
    return;
  }
  const today=NEWS.today||'';
  const items=NEWS.items.filter(newsMatch);
  let kb='';
  if(newsFilter.startsWith('k:')){
    const nm=newsKeyName(newsFilter.slice(2));
    kb=`<div class="nv-sum" style="display:flex;align-items:center;gap:8px">${esc(nm)} 뉴스만 보는 중<button type="button" class="chip" style="margin-left:auto" onclick="newsAll(this)">전체 보기</button></div>`;
  }
  if(!items.length){ el.innerHTML=kb+'<div class="na">해당 구분의 보관 기간 내 뉴스 없음</div>'; return; }
  const compact=newsFilter==='all', t0=new Date((today||'')+'T00:00:00');
  const age=d=>{ const t=new Date(d+'T00:00:00'); return (isNaN(t)||isNaN(t0))?0:Math.round((t0-t)/86400000); };
  const groups=[]; items.forEach(it=>{ const g=groups[groups.length-1]; if(g&&g.d===it.first_seen) g.items.push(it); else groups.push({d:it.first_seen,items:[it]}); });
  let body='', shown=0, old=[];
  groups.forEach(g=>{
    if(compact&&g.d!==today&&age(g.d)>NEWS_DAYS){ old.push(g); return; }
    const all=!compact||g.d===today||NEWS_MORE[g.d];
    const vis=all?g.items:g.items.filter(it=>(it.importance||1)>=NEWS_MIN_IMP), hid=g.items.length-vis.length;
    shown+=vis.length;
    const mk=compact&&g.d!==today&&NEWS_MORE[g.d];
    body+=`<div class="ndate">${newsDateLbl(g.d)}${g.d===kstToday()?' · 오늘':''}</div>`+vis.map(it=>newsItemHtml(it,mk&&(it.importance||1)<NEWS_MIN_IMP?g.d:'')).join('')
      +(hid?`<button type="button" class="nmore" onclick="newsMore('${g.d}',this)">★1~2 ${hid}건 더 보기 ${ic('down',16)}</button>`:'');
  });
  if(old.length){
    const n=old.reduce((a,g)=>a+g.items.length,0);
    if(NEWS_MORE.old){ shown+=n; old.forEach(g=>{ body+=`<div class="ndate">${newsDateLbl(g.d)}</div>`+g.items.map(it=>newsItemHtml(it,'old')).join(''); }); }
    else body+=`<button type="button" class="nmore" style="margin-top:8px" onclick="newsMore('old',this)">${old[0].d?newsDateLbl(old[0].d)+' 이전':'이전'} 기사 ${n}건 보기 (${NEWS_DAYS+1}일 넘은 기사) ${ic('down',16)}</button>`;
  }
  el.innerHTML=kb+`<div class="note" style="margin:0 0 6px">수집: ${NEWS.generated_at||'―'} · ${compact&&shown<items.length?`전체 ${items.length}건 중 ${shown}건 — ${today&&today!==kstToday()?newsDateLbl(today)+' 수집':'오늘'} 전체 + 최근 ${NEWS_DAYS}일 ★3`:items.length+'건'}</div>`+body;
}

/* ── 국내 수요 (KOSIS) ── */
function spark(vals,w,h,upBad,neutral){   // upBad: 오르면 나쁜 지표(재고) — 색 반대(v32.12) · neutral: 좋고 나쁨이 없는 지표(소비자물가) — 회색(v33)
  if(!vals||vals.length<2) return '';
  const mn=Math.min(...vals), mx=Math.max(...vals), rg=(mx-mn)||1;
  const pts=vals.map((v,i)=>`${(i/(vals.length-1)*w).toFixed(1)},${(h-(v-mn)/rg*h).toFixed(1)}`).join(' ');
  const up=vals[vals.length-1]>=vals[0], col=(neutral||vals[vals.length-1]===vals[0])?'var(--sub)':((upBad?!up:up)?'var(--pos)':'var(--neg)');
  return `<svg width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" preserveAspectRatio="none" style="display:block;margin-top:6px">
    <polyline points="${pts}" fill="none" stroke="${col}" stroke-width="1.6"/></svg>`;
}
function fmtPrd(p){ return p.slice(0,4)+'.'+p.slice(4,6); }
/* ── v30 국내 수요: 판매 vs 검색 교차 그래프 · 네이버 검색 관심도 ── */
let NV_SORT='yoy', NV_ALL=false, NV_GRP='global', XC_OFF={};
const NV_TOP=10;
const nvAll=()=>(NAVER&&NAVER.brands)||[];
const nvGrpOf=b=>b.group||'global';                      // v31.1: 'global'(수입·해외) / 'kr'(국내 패션) / v32.7 'eye'(글로벌 아이웨어)
const NV_EYE_KR=new Set(['krd:iicombined','krd:blueelephant']);   // 아이웨어 화면에 함께 보이는 국내 아이웨어
const NV_GRPS=[['global','수입·해외'],['kr','국내 패션'],['eye','아이웨어']];
const nvIn=(b,g)=>nvGrpOf(b)===g||(g==='eye'&&NV_EYE_KR.has(b.link));
const nvBrands=(g=NV_GRP)=>nvAll().filter(b=>nvIn(b,g));
function nvMed(g=NV_GRP){
  const ys=nvBrands(g).map(b=>b.yoy).filter(v=>v!=null).sort((a,b)=>a-b), n=ys.length;
  return n?(n%2?ys[(n-1)/2]:(ys[n/2-1]+ys[n/2])/2):null;
}
const nvRel=(y,med)=>(y==null||med==null)?'mid':(y-med>=5?'up':(y-med<=-5?'down':'mid'));
const nvWk=d=>d?(+d.slice(5,7))+'/'+(+d.slice(8,10)):'';
const nvSc=v=>v==null?'―':(v>=10?v.toFixed(0):v.toFixed(1));
/* 최근 52주(실선) vs 그 전 52주(점선), 같은 축 */
function nvSpark(s,w,h,fluid){
  if(!s||s.length<8) return '';
  const n=Math.min(52,Math.floor(s.length/2)), cur=s.slice(-n), prev=s.slice(-2*n,-n), all=cur.concat(prev);
  const mx=Math.max(...all), mn=Math.min(...all), rg=(mx-mn)||1;
  const pt=a=>a.map((v,i)=>`${(i/(n-1)*w).toFixed(1)},${(h-2-(v-mn)/rg*(h-4)).toFixed(1)}`).join(' ');
  const ns=fluid?' vector-effect="non-scaling-stroke"':'';
  return `<svg ${fluid?`style="display:block;width:100%;height:${h}px" preserveAspectRatio="none"`:`width="${w}" height="${h}" style="display:block;overflow:visible"`} viewBox="0 0 ${w} ${h}" aria-hidden="true">
    ${prev.length===n?`<polyline points="${pt(prev)}" fill="none" stroke="var(--sub)" stroke-width="1" stroke-dasharray="2 2" opacity=".7"${ns}/>`:''}
    <polyline points="${pt(cur)}" fill="none" stroke="var(--accent)" stroke-width="1.6"${ns}/>
    ${fluid?'':`<circle cx="${w}" cy="${(h-2-(cur[n-1]-mn)/rg*(h-4)).toFixed(1)}" r="2" fill="var(--accent)"/>`}</svg>`;
}
function nvRowHtml(b,med){
  // v33 S2: 수입·해외 브랜드 줄 → 브랜드 상세(판정과 이어짐, 결정 D5 — 이름은 data 속성). 국내 패션·아이웨어는 그대로 기업 상세·뉴스
  if(b.group==='global'&&brKnown(b.name)) return nvRowInner(b,med,` data-brand="${esc(b.name)}" role="button" tabindex="0"`);   // v33 Enter·Space는 전역 키 처리
  const act=b.link?`goDetail('${b.link}')`:(b.news?`nvNews('${b.news}')`:'');
  return nvRowInner(b,med,act?` role="button" tabindex="0" onclick="${act}"`:' style="cursor:default"');
}
function nvRowInner(b,med,attrs){
  return `<div class="nv-row${b.low?' low':''}"${attrs}>
    <div class="nv-nm"><span>${esc(b.name)}</span>${b.low?'<em class="nv-low">검색량 적음</em>':''}${staleTag(b.stale_since)}</div>
    <span class="nv-pill ${nvRel(b.yoy,med)}">전년 ${b.yoy!=null?pp(b.yoy):'―'}</span>
    <div class="nv-bar"><span class="tr"><i style="width:${b.scale!=null?Math.max(2,Math.min(100,b.scale)):0}%"></i></span><b>${nvSc(b.scale)}</b></div>
    <div style="justify-self:end">${nvSpark(b.s,84,24)}</div>
    <div class="nv-sub">최근 4주 vs 직전 12주 ${b.trend!=null?pp(b.trend):'―'} (계절 영향 포함)</div></div>`;
}
function naverCardHtml(){
  const grps=NV_GRPS.filter(([g])=>g==='global'||nvBrands(g).length);
  if(!grps.some(([g])=>g===NV_GRP)) NV_GRP='global';
  const bs=nvBrands();
  if(!bs.length) return `<div class="card" id="nvCard"><h3>브랜드 검색 관심도 — 네이버</h3><div class="na">네이버 검색 관심도 수집 전 — 다음 갱신 후 표시</div></div>`;
  const med=nvMed(), key=b=>NV_SORT==='yoy'?(b.yoy??-1e9):(b.scale??-1);
  const rows=[...bs].sort((a,b)=>(a.low?1:0)-(b.low?1:0)||key(b)-key(a)), shown=NV_ALL?rows:rows.slice(0,NV_TOP);   // v32.8 검색량 적은 브랜드는 맨 아래
  const ups=bs.filter(b=>!b.low&&nvRel(b.yoy,med)==='up').sort((a,b)=>b.yoy-a.yoy).slice(0,4);
  const downs=bs.filter(b=>!b.low&&nvRel(b.yoy,med)==='down').sort((a,b)=>a.yoy-b.yoy).slice(0,3);
  let h=`<div class="card" id="nvCard"><h3>브랜드 검색 관심도 — 네이버</h3>
    ${grps.length>1?`<div class="seg2" style="margin-bottom:8px;grid-template-columns:repeat(${grps.length},minmax(0,1fr))">${grps.map(([g,l])=>`<button type="button" class="${NV_GRP===g?'on':''}" aria-pressed="${NV_GRP===g}" onclick="nvGrp('${g}')">${l} ${nvBrands(g).length}</button>`).join('')}</div>`:''}
    <div class="note" style="margin:0 0 8px">주간 검색 지수 · 나이키 최근 4주 = 100 · ${nvWk(NAVER.end)} 주까지 · ${bs.length}개 브랜드${NV_GRP==='kr'?' · 중앙값은 국내 패션 브랜드끼리':NV_GRP==='eye'?' · 글로벌 아이웨어 + 국내 젠틀몬스터·블루엘리펀트, 중앙값은 이들끼리 · 명품은 선글라스·안경 검색어만':''}</div>
    <div class="seg2" style="margin-bottom:10px"><button type="button" class="${NV_SORT==='yoy'?'on':''}" aria-pressed="${NV_SORT==='yoy'}" onclick="nvSort('yoy')">전년 대비순</button><button type="button" class="${NV_SORT==='size'?'on':''}" aria-pressed="${NV_SORT==='size'}" onclick="nvSort('size')">규모순</button></div>
    <div class="nv-sum"><b>전년 대비 중앙값 ${med!=null?pp(med):'―'}</b> <span class="na">(${bs.filter(b=>b.yoy!=null).length}개 브랜드 전체${NV_GRP==='global'?' — 브랜드 점검표 중앙값은 검색량 충분한 브랜드만':''})</span> — 대부분이 같이 움직이면 네이버 검색 전반의 변화라, 중앙값보다 나은지로 봅니다.${ups.length?`<br><b style="color:var(--up)">▲ 상대 증가</b> ${ups.map(b=>`${esc(b.name)} ${pp(b.yoy)}`).join(' · ')}`:''}${downs.length?`<br><b style="color:var(--down)">▼ 상대 감소</b> ${downs.map(b=>`${esc(b.name)} ${pp(b.yoy)}`).join(' · ')}`:''}</div>`;
  shown.forEach(b=>{ h+=nvRowHtml(b,med); });
  if(rows.length>NV_TOP) h+=`<button type="button" class="nv-more" aria-expanded="${NV_ALL}" onclick="nvToggle()">${NV_ALL?`상위 ${NV_TOP}개만 보기 ${ic('up',16)}`:`전체 ${rows.length}개 보기 ${ic('down',16)}`}</button>`;
  h+=`<div class="src-legend" style="margin-top:8px"><span><i style="background:var(--accent-fill)"></i>중앙값보다 5%p 이상 좋음</span><span><i style="background:var(--warn-bg)"></i>5%p 이상 나쁨</span><span><i style="background:var(--sub);opacity:.55"></i>막대 = 규모</span><span>그래프: 최근 1년 실선 · 그 전 1년 점선</span></div>
    <div class="note" style="margin-top:6px">전년 대비 = 최근 4주 vs 1년 전 같은 4주(지수 비율 = 실제 검색 횟수 비율). 규모 1 미만은 검색량이 적어 '검색량 적음' 표시·맨 아래. 누르면 브랜드 상세(수입·해외)·기업 상세 또는 그 브랜드 뉴스로 이동. 출처: ${esc(NAVER.source||'네이버 데이터랩')}</div></div>`;
  return h;
}
function nvRefresh(){ const c=document.getElementById('nvCard'); if(c) c.outerHTML=naverCardHtml(); }
function nvSort(s){ NV_SORT=s; nvRefresh(); }
function nvToggle(){ NV_ALL=!NV_ALL; nvRefresh(); }
function nvGrp(g){ NV_GRP=g; NV_ALL=false; nvRefresh(); }
function nvNews(k){ goNews('k:'+k); }   // v33 시장 › 뉴스, 그 브랜드 뉴스만(처음 열 때 한 번만 그림)
function naverDetailCard(t){
  const bs=nvAll().filter(b=>b.link===t); if(!bs.length) return '';
  let h=`<div class="card"><h3>네이버 검색 관심도 <button type="button" class="go" onclick="NV_GRP='${nvGrpOf(bs[0])}';NV_ALL=false;nvRefresh();sw('kr')">국내 ›</button></h3>`;
  bs.forEach(b=>{
    const g=nvGrpOf(b), med=nvMed(g), grpN=nvBrands(g).length;
    h+=`<div class="nv-det"><div class="krhead"><span class="krname">${esc(b.name)}</span><span class="nv-pill ${nvRel(b.yoy,med)}" style="margin-left:auto">전년 ${b.yoy!=null?pp(b.yoy):'―'}</span></div>
      <div class="krmeta">규모 ${nvSc(b.scale)} (나이키 최근 4주 = 100) · ${g==='kr'?'국내 패션 ':g==='eye'?'아이웨어 ':''}${grpN}개 브랜드 중앙값 ${med!=null?pp(med):'―'} · 최근 4주 vs 직전 12주 ${b.trend!=null?pp(b.trend):'―'}</div>
      ${nvSpark(b.s,300,44,true)}${b.group==='global'&&brKnown(b.name)?`<button type="button" class="br-link" data-brand="${esc(b.name)}">${esc(b.name)} ${brJudged(b.name)?'매입 판정 보기':'브랜드 상세 보기'} ›</button>`:''}</div>`;   // v33 수입·해외 브랜드 → 브랜드 상세(판정)
  });
  return h+`<div class="note" style="margin-top:6px">주간 검색 지수 · 최근 1년 실선 · 그 전 1년 점선 · ${nvWk(NAVER.end)} 주까지${bs.some(b=>b.low)?' · 검색량이 적어 변동이 큼':''}</div></div>`;
}
/* 판매 vs 검색: 모두 전년 같은 달 대비(%) — 축 하나 */
function crossData(){
  const ser=[];
  if(NAVER&&NAVER.monthly){ const mo=NAVER.monthly, m={}; mo.months.forEach((p,i)=>{ if(mo.yoy[i]!=null) m[p]=mo.yoy[i]; });
    ser.push({id:'nv',label:'네이버 브랜드 검색량',col:'var(--s-naver)',m,bold:true}); }
  [['online_shoes','온라인 신발 거래액','var(--s-shoe)'],['online_apparel','온라인 의복 거래액','var(--s-apparel)']].forEach(([k,label,col])=>{
    const s=KR&&KR.series&&KR.series[k]; if(!s||!s.yoy) return; const m={};
    Object.entries(s.yoy).forEach(([p,v])=>{ if(v!=null) m[p.slice(0,4)+'-'+p.slice(4,6)]=v; });
    ser.push({id:k,label,col,m}); });
  const months=[...new Set(ser.flatMap(s=>Object.keys(s.m)))].sort().slice(-24);
  return {ser,months};
}
const XC={W:340,H:204,L:50,R:10,T:12,B:30};   // v33 축 글자 15단위(360px 폭에서도 13px 이상) — 왼쪽 여백 50
function crossChartHtml(){
  const {ser,months}=crossData();
  if(!ser.length||months.length<3) return '';
  const {W,H,L,R,T,B}=XC, iw=W-L-R, ih=H-T-B, vis=ser.filter(s=>!XC_OFF[s.id]);
  const vals=vis.flatMap(s=>months.map(m=>s.m[m]).filter(v=>v!=null));
  let lo=Math.min(0,...vals), hi=Math.max(0,...vals);
  const step=[5,10,20,25,50,100,200].find(s=>(hi-lo)/s<=6)||500;
  lo=Math.floor(lo/step)*step; hi=Math.ceil(hi/step)*step; if(hi===lo) hi=lo+step;
  const x=i=>L+(months.length>1?i/(months.length-1):.5)*iw, y=v=>T+(hi-v)/(hi-lo)*ih;
  let g='';
  for(let v=lo; v<=hi+1e-9; v+=step) g+=`<line x1="${L}" x2="${W-R}" y1="${y(v).toFixed(1)}" y2="${y(v).toFixed(1)}" stroke="var(--line)" stroke-width="${v===0?1.4:.6}"/><text x="${L-6}" y="${(y(v)+5).toFixed(1)}" text-anchor="end" font-size="15" fill="var(--sub)">${v>0?'+':v<0?'−':''}${Math.abs(v)}%</text>`;
  months.forEach((m,i)=>{ const last=months.length-1; if((i%6===0&&last-i>=5)||i===last) g+=`<text x="${x(i).toFixed(1)}" y="${H-8}" text-anchor="${i===months.length-1?'end':(i===0?'start':'middle')}" font-size="15" fill="var(--sub)">${m.slice(2,4)}.${m.slice(5,7)}</text>`; });   // 6개월 간격 · 마지막 라벨과 5칸 이상(겹침 없게)
  let ln='';
  vis.forEach(s=>{
    let d='', pen=false, li=-1;
    months.forEach((m,i)=>{ const v=s.m[m]; if(v==null){ pen=false; return; } d+=(pen?'L':'M')+x(i).toFixed(1)+','+y(v).toFixed(1); pen=true; li=i; });
    ln+=`<path d="${d}" fill="none" stroke="${s.col}" stroke-width="${s.bold?2.6:1.7}" stroke-linejoin="round" stroke-linecap="round"/>`;
    if(li>=0) ln+=`<circle cx="${x(li).toFixed(1)}" cy="${y(s.m[months[li]]).toFixed(1)}" r="3.2" fill="${s.col}"/>`;
  });
  const lastOf=s=>{ for(let i=months.length-1;i>=0;i--){ const v=s.m[months[i]]; if(v!=null) return {m:months[i],v}; } return null; };
  const summ=ser.map(s=>{ const l=lastOf(s); return l?`${esc(s.label)} <b>${pp(l.v)}</b> <span class="na">(${+l.m.slice(5,7)}월)</span>`:''; }).filter(Boolean).join(' · ');
  const legend=ser.map(s=>`<button type="button" class="xc-leg${XC_OFF[s.id]?' off':''}" aria-pressed="${!XC_OFF[s.id]}" onclick="xcToggle('${s.id}')"><i style="background:${s.col}"></i>${esc(s.label)}</button>`).join('');
  return `<div class="card" id="xcCard"><h3>국내 수요 한눈에 — 판매 vs 검색</h3>
    <div class="note" style="margin:0 0 4px">모두 전년 같은 달 대비(%) · 같은 축 · 최근 ${months.length}개월 · 그래프를 누르면 그 달 값</div>
    <div class="xc-legend">${legend}</div>
    <div class="xc-wrap"><svg class="xc-svg" id="xcSvg" viewBox="0 0 ${W} ${H}" role="img" aria-label="온라인 신발·의복 거래액과 네이버 브랜드 검색량의 전년 대비 증감">${g}${ln}<line id="xcGuide" x1="0" x2="0" y1="${T}" y2="${T+ih}" stroke="var(--sub)" stroke-width=".8" stroke-dasharray="3 3" visibility="hidden"/><rect id="xcHit" x="${L}" y="${T}" width="${iw}" height="${ih}" fill="transparent"/></svg><div class="xc-tip" id="xcTip" hidden></div></div>
    <div class="note" style="margin-top:6px;line-height:1.6">최근: ${summ}</div>
    <div class="note" style="margin-top:4px">KOSIS 온라인쇼핑 거래액은 1~2개월 늦게 나오고 네이버는 지난달까지 나옵니다. 검색선이 판매선보다 먼저 움직이면 선행 신호로 볼 수 있습니다. 네이버 선은 아래 수입·해외 브랜드 검색어의 검색량 합계(2026-10-19에 추가한 8개는 추이가 끊기지 않게 뺌)라 큰 브랜드 비중이 크며, 시장 전체가 아닌 방향 참고용입니다.</div></div>`;
}
function xcToggle(id){
  const {ser}=crossData();
  if(!XC_OFF[id]&&ser.filter(s=>!XC_OFF[s.id]).length<=1) return;   // 마지막 한 선은 끄지 않음
  XC_OFF[id]=!XC_OFF[id];
  const c=document.getElementById('xcCard'); if(c){ c.outerHTML=crossChartHtml(); xcBind(); }
}
function xcBind(){
  const svg=document.getElementById('xcSvg'); if(!svg) return;
  const hit=document.getElementById('xcHit'), tip=document.getElementById('xcTip'), gd=document.getElementById('xcGuide');
  const {ser,months}=crossData(), vis=ser.filter(s=>!XC_OFF[s.id]), {W,L,R}=XC, iw=W-L-R;
  const show=cx=>{
    const r=svg.getBoundingClientRect();
    let i=Math.round(((cx-r.left)/r.width*W-L)/iw*(months.length-1)); i=Math.max(0,Math.min(months.length-1,i));
    const xx=L+(months.length>1?i/(months.length-1):.5)*iw, m=months[i];
    gd.setAttribute('x1',xx); gd.setAttribute('x2',xx); gd.setAttribute('visibility','visible');
    tip.innerHTML=`<b>${m.slice(0,4)}년 ${+m.slice(5,7)}월</b><br>`+vis.map(s=>`<span style="color:${s.col}">●</span> ${esc(s.label)} ${s.m[m]!=null?`<b>${pp(s.m[m])}</b>`:'<span class="na">미발표</span>'}`).join('<br>');
    tip.hidden=false;
    const tw=tip.offsetWidth, px=xx/W*r.width;
    tip.style.left=Math.max(0,Math.min(r.width-tw,px-tw/2))+'px';
  };
  hit.addEventListener('pointermove',e=>show(e.clientX));
  hit.addEventListener('pointerdown',e=>show(e.clientX));
  hit.addEventListener('pointerleave',e=>{ if(e.pointerType==='mouse'){ tip.hidden=true; gd.setAttribute('visibility','hidden'); } });
}
/* ── 국내 온라인 플랫폼 (v30.2) ── */
const KR_PLATFORMS=['CPNG','krd:musinsa','krd:kream','krd:trenbe','krd:balaan','krd:mustit','krd:trexi'];
const KR_PLATFORM_STATUS={'krd:balaan':'2026.2 회생 폐지 · 청산 절차'};   // 수치 없는 이유(대표 확인 2026.10)
function platformCardHtml(){
  const all=rows_all();
  const rows=KR_PLATFORMS.map(k=>all.find(r=>r.key===k)).filter(Boolean).map(r=>{
    const fy=r.listed&&r.item.fy.length?r.item.fy[r.item.fy.length-1]:null;
    return {...r, krw:krwOf(r.rev,r.cur), op:(r.opm!=null?r.opm:(fy?fy.op_pct:null)), end:(r.fy_end||(fy?fy.end:null))};
  }).sort((a,b)=>(b.krw==null?-1:b.krw)-(a.krw==null?-1:a.krw));
  if(!rows.length) return '';
  let h=`<div class="card"><h3>국내 온라인 플랫폼 <span class="tag">연간</span></h3>
    <div class="tblwrap"><table class="nowrap"><tr><th>기업</th><th>매출</th><th>전년 대비</th><th>영업<wbr>이익률</th><th>재고 증감</th></tr>`;   // 360폭은 머리글 두 줄(아래 #coPlat 규칙)
  rows.forEach(r=>{
    const self=r.key==='krd:trexi';
    h+=`<tr class="co" tabindex="0" style="cursor:pointer${self?';background:var(--barbg)':''}" onclick="goDetail('${r.key}')">
      <td>${r.logo}${self?'<b>'+esc(r.name)+'</b>':esc(r.name)}<span class="na" style="display:block">${KR_PLATFORM_STATUS[r.key]?'<span class="neg">'+esc(KR_PLATFORM_STATUS[r.key])+'</span>':(r.end?ym(r.end)+' 결산':'미확인')}${r.listed?' · 상장':''}</span></td>
      <td>${r.rev!=null?revKrwCell(r.rev,r.cur):'<span class="na">―</span>'}</td><td>${fmt(r.rev_yoy,1,true)}</td>
      <td>${r.op!=null?fmt(r.op,1,true):'<span class="na">―</span>'}</td><td>${fmtInv(r.listed?r.item.inv_yoy:r.inv_yoy)}</td></tr>`;
  });
  const usd=(DATA.fx||{}).USD, ents=(KRD&&KRD.entities)||[];
  const kr=rows.filter(r=>!r.listed&&r.rev!=null).map(r=>({r,e:ents.find(z=>'krd:'+z.id===r.key)})).filter(o=>o.e);
  const api=kr.filter(o=>o.e.route==='api').map(o=>{const c=(o.e.cfs&&o.e.cfs.years)||[]; return `${esc(o.r.name)} = 사업보고서 별도${c.length&&c[c.length-1].rev!=null?'(연결 매출 '+moneyShort(c[c.length-1].rev,'KRW')+' — 상세 참조)':''}`;});
  const doc=kr.filter(o=>o.e.route==='doc').map(o=>esc(o.r.name.replace(/\(.*\)/,'')));
  h+=`</table></div><div class="note" style="margin-top:6px">매출 큰 순 · 쿠팡 = 미국 상장 연결(US GAAP) 달러 실적을 최근 환율${usd&&usd.rate?'(1달러 = '+Math.round(usd.rate).toLocaleString()+'원)':''}로 환산한 근사치 ·
    ${api.join(' · ')}${api.length?' · ':''}${doc.length?doc.join('·')+' = 감사보고서 별도 연간 · ':''}플랫폼 매출은 거래액과 다름(크림 등은 수수료 매출) · 행을 누르면 상세</div></div>`;
  return h;
}
/* ── 비교 카드 (v30.4 수입 브랜드 유통사 → v31.1 공통화) — 수치는 공시 그대로, 자사(트렉시)는 위치·강조로만 앞세움 ── */
const PEER_SELF='krd:trexi';
const PEER_KEYS=[PEER_SELF,'krd:daelim_corp','krd:rexmond','krd:bazig','krd:creed','krd:hana_int','krd:t1global','krd:bbluein','krd:starintl'];
const FB_KEYS=['krd:aubrandz','krd:piecepeace','krd:sjgroup','krd:matinkim','krd:layer','krd:highlight','krd:hagohouse',
  'krd:bcave','krd:fivespace','krd:koza','krd:andar','krd:sisun','krd:lowclassic'];
const EY_KEYS=['krd:iicombined','krd:blueelephant','krd:luxottica_kr','krd:kering_ey_kr','krd:seeone','krd:davich'];
const CMP={
  peer:{id:'peerCard',name:'수입 브랜드 유통사 비교',keys:PEER_KEYS,self:PEER_SELF,selfName:'트렉시',tag:'연간 · 감사보고서',
        who:'비교 유통사',src:'DART 감사보고서(별도) 연간 수치 그대로'},
  fb:{id:'fbCard',name:'국내 패션 브랜드 비교',keys:FB_KEYS,self:null,tag:'연간 · 사업·감사보고서',
      who:'패션 브랜드사',src:'DART 별도 재무제표 연간 수치 그대로(상장 3곳 사업보고서 · 외감 10곳 감사보고서) · 하고하우스는 브랜드 육성·투자 회사'},
  ey:{id:'eyCard',name:'아이웨어 비교',keys:EY_KEYS,self:null,tag:'연간 · 감사보고서',
      who:'아이웨어 기업',src:'DART 감사보고서(별도) 연간 수치 그대로 · 국내 브랜드(젠틀몬스터·블루엘리펀트) vs 글로벌 국내법인(룩소티카코리아 = 에실로룩소티카, 케어링아이웨어코리아 = 케링) vs 명품 아이웨어 수입 유통(시원아이웨어) vs 안경 체인(다비치) · 아이아이컴바인드는 탬버린즈·누데이크 포함'},
};
const CMP_GROWTH={peer:'yoy',fb:'yoy',ey:'yoy'};
// [키, 이름, 높을수록 좋음, 표시]
const PEER_METRICS=[
  ['rev','매출',true,v=>moneyShort(v,'KRW')],
  ['yoy','전년 대비',true,v=>pp(v)],
  ['cagr','연평균(2년)',true,v=>pp(v)],
  ['opm','영업이익률',true,v=>mnum(v)+'%'],
  ['gm','매출총이익률',true,v=>mnum(v)+'%'],
  ['dio','재고일수',false,v=>Math.round(v)+'일'],
];
const pgMedian=arr=>{const a=arr.filter(v=>v!=null).sort((x,y)=>x-y); if(!a.length) return null; const m=Math.floor(a.length/2); return a.length%2?a[m]:(a[m-1]+a[m])/2;};
function cmpData(c){
  const ents=(KRD&&KRD.entities)||[];
  return c.keys.map(k=>{
    const e=ents.find(x=>'krd:'+x.id===k); if(!e) return null;
    const ys=(e.years||[]).filter(y=>y.rev!=null&&y.end).sort((a,b)=>a.end<b.end?-1:1);
    const l=ys[ys.length-1], p=ys[ys.length-2], f=ys[0], n=ys.length;
    return {key:k, name:e.name, self:k===c.self, end:l?l.end:null, l, p, f,
      rev:l?l.rev:null,
      yoy:(l&&p&&p.rev>0)?(l.rev/p.rev-1)*100:null,
      cagr:(n>=3&&f.rev>0&&l.rev>0)?(Math.pow(l.rev/f.rev,1/(n-1))-1)*100:null,
      opm:(l&&l.op!=null&&l.rev)?l.op/l.rev*100:null,
      gm:(l&&l.cogs!=null&&l.rev)?(l.rev-l.cogs)/l.rev*100:null,
      dio:l?dioOf(l.inv,l.rev,null,l.cogs):null};
  }).filter(Boolean);
}
function peerRank(rows,k,hi){
  const v=rows.filter(r=>r[k]!=null).sort((a,b)=>hi?b[k]-a[k]:a[k]-b[k]);
  return {of:r=>{const i=v.indexOf(r); return i<0?null:i+1;}, n:v.length};
}
function cmpCardHtml(cid){
  const c=CMP[cid], rows=cmpData(c); if(rows.length<2) return '';
  const me=c.self?rows.find(r=>r.self):null, peers=rows.filter(r=>!r.self);
  const med={}, rk={};
  PEER_METRICS.forEach(([k,,hi])=>{ med[k]=pgMedian(peers.map(r=>r[k])); rk[k]=peerRank(rows,k,hi); });
  // 강조 기준: 비교군 중앙값(자사 제외)보다 나은 지표만 — 순위 중간을 '강점'으로 부풀리지 않음
  const hiOf=Object.fromEntries(PEER_METRICS.map(([k,,hi])=>[k,hi]));
  const topHalf=(k,r)=>r[k]!=null&&med[k]!=null&&(hiOf[k]?r[k]>med[k]:r[k]<med[k]);
  let h=`<div class="card" id="${c.id}">`;   // 제목은 더보기 화면 머리글(v32.5)
  if(me){
    const items=PEER_METRICS.map(([k,nm])=>({k,nm,x:rk[k].of(me),n:rk[k].n})).filter(i=>i.x!=null);
    const strong=items.filter(i=>topHalf(i.k,me)).sort((a,b)=>a.x-b.x), rest=items.filter(i=>!topHalf(i.k,me));
    h+=`<div class="nv-sum"><b>${esc(c.selfName)}</b> · ${rows.length}곳 비교<br>${strong.length?strong.map(i=>`<span class="pg-badge">${esc(i.nm)} ${i.x}위</span>`).join(''):''}${rest.length?`<span class="na"> ${rest.map(i=>`${esc(i.nm)} ${i.x}위`).join(' · ')}</span>`:''}</div>`;
  } else {
    h+=`<div class="note" style="margin:0 0 8px">${rows.length}곳 · 매출 큰 순 · 회색 줄 = 중앙값</div>`;
  }
  const order=[me,...peers.slice().sort((a,b)=>(b.rev??-1)-(a.rev??-1))].filter(Boolean);
  h+=`<div class="tblwrap"><table class="nowrap"><tr><th>기업</th>${PEER_METRICS.map(([,nm])=>`<th>${nm}</th>`).join('')}</tr>`;
  order.forEach(r=>{
    h+=`<tr tabindex="0" style="cursor:pointer${r.self?';background:var(--barbg)':''}" onclick="goDetail('${r.key}')"><td>${logoImg(r.key,false,r.name)}${r.self?'<b>'+esc(nmSplit(r.name).main)+'</b>':esc(nmSplit(r.name).main)}<span class="pg-rk">${nmSplit(r.name).brand?esc(nmSplit(r.name).brand)+' · ':''}${r.end?ym(r.end)+' 결산':'미확인'}</span></td>`;
    PEER_METRICS.forEach(([k,,,f])=>{
      const v=r[k];
      if(v==null){ h+=`<td><span class="na">―</span></td>`; return; }
      if(!r.self){ h+=`<td>${f(v)}</td>`; return; }
      const x=rk[k].of(r);
      h+=`<td><b>${f(v)}</b>${topHalf(k,r)?`<br><span class="pg-badge" style="margin-top:2px;white-space:nowrap">${x}위</span>`:`<span class="pg-rk">${x}위/${rk[k].n}</span>`}</td>`;
    });
    h+=`</tr>`;
  });
  h+=`<tr><td class="na">${me?'비교군 중앙값':'중앙값'}<span class="pg-rk">${me?esc(c.selfName)+' 제외 ':''}${peers.length}곳</span></td>${PEER_METRICS.map(([k,,,f])=>`<td class="na">${med[k]!=null?f(med[k]):'―'}</td>`).join('')}</tr></table></div>`;
  // 성장성 비교
  const g=CMP_GROWTH[cid], tid=c.id+'Tip';
  h+=`<div class="ndate" style="margin-top:14px">성장성 비교</div>
    <div class="seg2" style="margin:6px 0 10px"><button type="button" class="${g==='yoy'?'on':''}" aria-pressed="${g==='yoy'}" onclick="cmpGrowth('${cid}','yoy')">전년 대비</button><button type="button" class="${g==='cagr'?'on':''}" aria-pressed="${g==='cagr'}" onclick="cmpGrowth('${cid}','cagr')">연평균(2년)</button></div>`;
  const bars=rows.filter(r=>r[g]!=null).sort((a,b)=>b[g]-a[g]);
  if(bars.length){
    const mv=med[g], lo=Math.min(0,mv??0,...bars.map(r=>r[g])), hi=Math.max(0,mv??0,...bars.map(r=>r[g])), sp=(hi-lo)||1, X=t=>(t-lo)/sp*100;
    h+=`<div class="pg-bars">`;
    bars.forEach(r=>{
      const a=X(Math.min(0,r[g])), b=X(Math.max(0,r[g]));
      const from=g==='yoy'?r.p:r.f;
      const tip=`${r.name}: ${ym(from.end)} ${moneyShort(from.rev,'KRW')} → ${ym(r.l.end)} ${moneyShort(r.l.rev,'KRW')} (${g==='yoy'?'전년 대비':'연평균'} ${pp(r[g])})`;
      h+=`<div class="pg-row${r.self?' me':''}" role="button" tabindex="0" title="${esc(tip)}" data-tip="${esc(tip)}" data-k="${r.key}" onmouseenter="peerTip(this,'${tid}')" onclick="peerTip(this,'${tid}')"><span class="pg-nm">${esc(nmBrand(r.name))}</span>
        <span class="pg-tr"><i class="pg-zero" style="left:${X(0)}%"></i>${mv!=null?`<i class="pg-med" style="left:${X(mv)}%"></i>`:''}<i class="pg-bar${r[g]<0?' neg':''}" style="left:${a}%;width:${Math.max(b-a,0.8)}%"></i></span><b class="pg-v">${pp(r[g])}</b></div>`;
    });
    h+=`</div><div class="pg-tip" id="${tid}">막대를 누르면 매출 변화가 보입니다</div>`;
  } else h+=`<div class="na">비교할 수치 없음</div>`;
  h+=`<div class="src-legend" style="margin-top:8px">${me?`<span><i style="background:var(--accent)"></i>${esc(c.selfName)}</span>`:''}<span><i style="background:var(--sub);opacity:.4"></i>${c.who}</span><span><i style="border-left:1.5px dashed var(--sub);width:0;height:11px;border-radius:0"></i>${me?`비교군 중앙값(${esc(c.selfName)} 제외)`:'중앙값'}</span></div>
    <div class="note" style="margin-top:6px">${c.src}${me?' · 파란 배지 = 비교군 중앙값보다 나은 지표':''} · 순위는 수치가 있는 기업끼리 · 재고일수는 낮을수록 위 · 연평균은 3개년 자료가 있는 기업만 · 행을 누르면 기업 상세</div></div>`;
  return h;
}
// ── 유통사 재무 지표(v32) — 그룹 탭 5개 · 지표 칩 · 3개년 표 · 최근 연도 순위 (dart_fetch v3.0 재무상태표·현금흐름표) ──
const FI_G=[['pl','손익·성장'],['prof','수익성'],['wc','운전자본'],['cash','현금'],['stab','안정성']];
const fiEok=v=>{const a=Math.abs(v); const t=a>=1e12?(a/1e12).toFixed(2)+'조원':(a>=1e10?Math.round(a/1e8).toLocaleString():(a/1e8).toFixed(1))+'억원'; return (v<0?'−':'')+t;};
const fiPct=(v,d=1)=>(v<0?'−':'')+Math.abs(v).toFixed(d)+'%';
const fiDay=v=>mnum(v,0)+'일';
// f(y): 재무상태표·현금흐름 — 없으면 null, 검증 실패면 '확인 필요'
const fiF=y=>!y||!y.fin?null:(y.fin.chk?'확인 필요':y.fin);
const fiNd=f=>f.borrow==null||f.cash==null?null:f.borrow+(f.lease||0)-f.cash-(f.stfin||0);
const fiDa=(y,f)=>y.op==null||f.da==null?null:y.op+f.da;
const fiNd2=f=>f.debt==null||f.cash==null?null:f.debt-f.cash-(f.stfin||0);   // v32.9 리스·RCPS 제외 순차입금
// 지표: v=값(문자열이면 표시만·순위 제외), c=순위·중앙값 비교값(없으면 v), s=보조줄, ref=참고(순위 없음), nr=마이너스가 좋음
const FI_M={
  rev:{g:'pl',nm:'매출',hi:1,fmt:fiEok,v:y=>y.rev,f:'매출액',dir:'클수록 규모 큼',why:'브랜드 본사 협상력·물류 단가를 좌우하는 기본 체급'},
  yoy:{g:'pl',nm:'매출 성장률',hi:1,fmt:v=>pp(v),v:(y,p)=>p&&p.rev>0?(y.rev/p.rev-1)*100:null,f:'올해 매출 ÷ 전년 매출 − 1',dir:'높을수록 좋음',why:'브랜드 확보·채널 확장이 실제 매출로 이어지는지'},
  gm:{g:'prof',nm:'매출총이익률',hi:1,fmt:v=>fiPct(v),v:y=>y.cogs!=null?(y.rev-y.cogs)/y.rev*100:null,f:'(매출 − 매출원가) ÷ 매출',dir:'높을수록 좋음',why:'매입가·환율·할인 판매의 결과. 병행·수입 유통의 가격 경쟁력'},
  opm:{g:'prof',nm:'영업이익률',hi:1,fmt:v=>fiPct(v),v:y=>y.op!=null?y.op/y.rev*100:null,f:'영업이익 ÷ 매출',dir:'높을수록 좋음',why:'판관비(인건비·물류·수수료)까지 뺀 본업 수익력'},
  roe:{g:'prof',u:['equity'],nm:'ROE',hi:1,bs:1,fmt:v=>fiPct(v),v:(y,p)=>{const f=fiF(y); if(f==null||typeof f==='string') return f;
        const pf=fiF(p), e0=pf&&typeof pf!=='string'&&pf.equity!=null&&!(pf.bad||[]).includes('equity')?pf.equity:f.equity_begin;
        if(f.equity==null||e0==null||y.ni==null) return null; const a=(f.equity+e0)/2; return a>0?y.ni/a*100:'자본잠식';},
       f:'순이익 ÷ 평균 자기자본(기초·기말)',dir:'높을수록 좋음',why:'주주 돈(순자산)으로 얼마를 벌었나. 차입 효과까지 포함'},
  dio:{g:'wc',nm:'재고일수',hi:0,fmt:fiDay,v:y=>y.inv!=null&&y.cogs?y.inv/y.cogs*365:null,f:'기말 재고 ÷ 매출원가 × 365',dir:'짧을수록 좋음',why:'재고가 현금으로 바뀌는 데 걸리는 날. 시즌 지난 재고 위험'},
  dso:{g:'wc',u:['ar'],nm:'매출채권일수',hi:0,bs:1,fmt:fiDay,v:y=>{const f=fiF(y); if(f==null||typeof f==='string') return f; return f.ar!=null?f.ar/y.rev*365:null;},
       f:'기말 매출채권 ÷ 매출 × 365',dir:'짧을수록 좋음',why:'오픈마켓·백화점 정산이 들어오는 데 걸리는 날'},
  dpo:{g:'wc',u:['ap'],nm:'매입채무일수',hi:1,bs:1,fmt:fiDay,v:y=>{const f=fiF(y); if(f==null||typeof f==='string') return f; return f.ap!=null&&y.cogs?f.ap/y.cogs*365:null;},
       f:'기말 매입채무 ÷ 매출원가 × 365',dir:'길수록 현금에 유리',why:'공급처 결제를 미룰 수 있는 날. 선결제가 많은 수입 유통은 짧게 나옴'},
  ccc:{g:'wc',u:['ar','ap'],nm:'현금전환주기',hi:0,nr:1,bs:1,fmt:fiDay,v:y=>{const f=fiF(y); if(f==null||typeof f==='string') return f;
        return f.ar!=null&&f.ap!=null&&y.inv!=null&&y.cogs?y.inv/y.cogs*365+f.ar/y.rev*365-f.ap/y.cogs*365:null;},
       f:'재고일수 + 매출채권일수 − 매입채무일수',dir:'짧을수록 좋음',why:'물건값을 낸 뒤 판매 대금이 들어올 때까지 묶이는 날. 운전자금 필요량'},
  ocf:{g:'cash',u:['ocf'],nm:'영업현금흐름(OCF)',hi:1,bs:1,fmt:fiEok,v:y=>{const f=fiF(y); if(f==null||typeof f==='string') return f; return f.ocf;},
       c:y=>y.fin.ocf/y.rev*100,cn:'매출 대비 %',f:'현금흐름표 \'영업활동으로 인한 현금흐름\'',dir:'플러스·클수록 좋음',why:'장부상 이익이 아니라 실제로 들어온 현금. 재고·채권이 늘면 이익이 나도 마이너스'},
  fcf:{g:'cash',u:['ocf','capex'],nm:'잉여현금흐름(FCF)',hi:1,bs:1,fmt:fiEok,v:y=>{const f=fiF(y); if(f==null||typeof f==='string') return f; return f.ocf!=null&&f.capex!=null?f.ocf-f.capex:null;},
       c:y=>(y.fin.ocf-y.fin.capex)/y.rev*100,cn:'매출 대비 %',f:'OCF − 유형·무형자산 취득(CAPEX)',dir:'플러스·클수록 좋음',why:'설비·시스템 투자 후 남는 현금. 빚 상환·새 브랜드 선매입 여력'},
  conv:{g:'cash',u:['ocf'],nm:'이익의 현금화',hi:1,bs:1,clip:300,fmt:v=>fiPct(v,0),v:y=>{const f=fiF(y); if(f==null||typeof f==='string') return f; if(f.ocf==null||y.op==null) return null; return y.op>0?f.ocf/y.op*100:'영업적자';},
       f:'OCF ÷ 영업이익',dir:'100% 이상이 좋음',why:'영업이익이 현금으로 들어왔나. 계속 100% 아래면 재고·채권에 이익이 묶임. 재고가 크게 늘거나 준 해엔 수백 %로 흔들려 3년 흐름으로 봄'},
  nd:{g:'stab',u:['borrow','lease','cash','stfin','equity'],nm:'순부채',hi:0,nr:1,bs:1,fmt:fiEok,v:y=>{const f=fiF(y); if(f==null||typeof f==='string') return f; return fiNd(f);},
      c:y=>y.fin.equity>0?fiNd(y.fin)/y.fin.equity*100:null,cn:'순자산 대비 %',f:'차입금·사채 + RCPS 부채 + 리스부채 − 현금·단기금융상품',dir:'낮을수록 좋음 · 마이너스 = 순현금',why:'재고 선매입을 빚으로 하는 정도. 금리 오르면 바로 이익을 깎음'},
  // v32.9 회계기준이 섞인 비교군용 — K-IFRS(리스부채·RCPS 부채)와 일반기업회계기준(운용리스 부채 없음·RCPS 대개 자본)을 같은 잣대로. alt=순부채와 겹쳐 요약 점수(중앙값보다 나은 지표 수)에선 뺌
  nd2:{g:'stab',u:['borrow','cash','stfin','equity'],nm:'순차입금(리스·RCPS 제외)',hi:0,nr:1,bs:1,alt:1,fmt:fiEok,v:y=>{const f=fiF(y); if(f==null||typeof f==='string') return f; return fiNd2(f);},
       c:y=>{const f=y.fin, eq=(f.equity||0)+(f.rcps||0), n=fiNd2(f); return n!=null&&eq>0?n/eq*100:null;},cn:'순자산(RCPS 포함) 대비 %',
       f:'차입금·사채 − 현금·단기금융상품 (리스부채·RCPS 부채 제외, RCPS는 자본으로 봄)',dir:'낮을수록 좋음 · 마이너스 = 순현금',
       why:'회계기준이 다른 회사를 같은 잣대로 비교 — K-IFRS는 리스부채·RCPS를 부채로 잡아 순부채가 커 보임'},
  ndx:{g:'stab',u:['borrow','lease','cash','stfin','da'],nm:'순부채/EBITDA',hi:0,nr:1,bs:1,fmt:v=>v<0?'순현금':v.toFixed(1)+'배',v:y=>{const f=fiF(y); if(f==null||typeof f==='string') return f;
        const n=fiNd(f), e=fiDa(y,f); if(n==null||e==null) return null; return e>0?n/e:'EBITDA 적자';},
       f:'순부채 ÷ (영업이익 + 감가상각비)',dir:'낮을수록 좋음 · 3배 넘으면 주의',why:'번 돈으로 빚을 몇 년에 갚나. 은행 여신 심사에서 보는 기준'},
  dr:{g:'stab',u:['liab','equity'],nm:'부채비율',hi:0,bs:1,fmt:v=>fiPct(v,0),v:y=>{const f=fiF(y); if(f==null||typeof f==='string') return f; if(f.liab==null||f.equity==null) return null; return f.equity>0?f.liab/f.equity*100:'자본잠식';},
      f:'부채총계 ÷ 자본총계',dir:'낮을수록 좋음 · 200% 넘으면 주의',why:'매입채무까지 포함한 전체 빚 부담'},
  cash:{g:'stab',u:['cash','stfin'],nm:'현금',ref:1,bs:1,fmt:fiEok,v:y=>{const f=fiF(y); if(f==null||typeof f==='string') return f; return f.cash!=null?f.cash+(f.stfin||0):null;},
        c:y=>(y.fin.cash+(y.fin.stfin||0))/y.rev*100,cn:'매출 대비 %',f:'현금및현금성자산 + 단기금융상품',dir:'참고',why:'당장 쓸 수 있는 돈. 회사 규모 차이가 커서 순위 없이 참고'},
  eq:{g:'stab',u:['equity'],nm:'순자산',ref:1,bs:1,fmt:fiEok,v:y=>{const f=fiF(y); if(f==null||typeof f==='string') return f; return f.equity;},
      f:'자본총계(자산 − 부채)',dir:'참고',why:'쌓아 온 자기 돈. 회사 규모 차이가 커서 순위 없이 참고'},
};
const FI_K=Object.keys(FI_M);
const FI_ST={peer:{g:'pl',k:'rev'},fb:{g:'pl',k:'rev'},ey:{g:'pl',k:'rev'}};   // v32.8 비교 카드별 선택 그룹·지표
function fiRows(cid='peer'){
  const c=CMP[cid], ents=(KRD&&KRD.entities)||[];
  return c.keys.map(k=>{ const e=ents.find(x=>'krd:'+x.id===k); if(!e) return null;
    const by={}; (e.years||[]).filter(y=>y.rev!=null&&y.end).forEach(y=>{by[+y.end.slice(0,4)]=y;});
    return {key:k,name:e.name,self:k===c.self,by,std:e.acct_std||null};
  }).filter(Boolean);
}
function fiVal(r,k,fy){ // {v,c,s} 또는 {t:'사유'}
  const y=r.by[fy]; if(!y) return {t:'―'};
  const m=FI_M[k];
  if(y.fin&&y.fin.bad&&m.u&&m.u.some(f=>y.fin.bad.includes(f))) return {t:'확인 필요'};   // 보고서 간 값이 다른 항목을 쓰는 지표
  const v=m.v(y,r.by[fy-1]||null);
  if(v==null||(typeof v==='number'&&!isFinite(v))) return {t:'―'};
  if(typeof v==='string') return {t:v};
  const c=m.c?m.c(y):v;
  return {v,c:(c==null||!isFinite(c))?null:c};
}
const fiMed=a=>{a=a.filter(x=>x!=null).sort((x,y)=>x-y); if(!a.length) return null; const i=a.length>>1; return a.length%2?a[i]:(a[i-1]+a[i])/2;};
function fiStat(rows,k,fy){ // 중앙값(자사 제외)·순위·중앙값보다 나은지
  const m=FI_M[k], vs=rows.map(r=>({r,x:fiVal(r,k,fy)})).filter(o=>o.x.v!=null&&o.x.c!=null);
  const pe=vs.filter(o=>!o.r.self), md=fiMed(pe.map(o=>o.x.c)), mdv=fiMed(rows.filter(r=>!r.self).map(r=>fiVal(r,k,fy).v));
  const sorted=vs.slice().sort((a,b)=>m.hi?b.x.c-a.x.c:a.x.c-b.x.c);
  const me=rows.find(r=>r.self), mx=me?fiVal(me,k,fy):{t:'―'}, i=sorted.findIndex(o=>o.r.self);
  const better=!m.ref&&mx.v!=null&&mx.c!=null&&md!=null&&(m.hi?mx.c>md:mx.c<md);
  return {md,mdv,rank:i>=0?i+1:null,n:sorted.length,np:pe.length,better,me:mx};
}
function fiPick(g,k,cid='peer'){ FI_ST[cid]={g,k:k||FI_K.find(x=>FI_M[x].g===g)}; const el=document.getElementById(CMP[cid].id); if(el) el.outerHTML=finCardHtml(cid); }
const fiHas=cid=>fiRows(cid).some(r=>Object.values(r.by).some(y=>y.fin));   // 재무상태표·현금흐름이 한 곳이라도 있으면 재무 지표 카드
function fiScore(){   // 더보기 메뉴 줄: 자사가 최근 연도 비교군 중앙값보다 나은 지표 수
  const rows=fiRows(), me=rows.find(r=>r.self); if(!me) return null;
  const L=Math.max(...rows.flatMap(r=>Object.keys(r.by).map(Number)));
  if(!isFinite(L)) return null;   // v33 연도 자료가 없으면 'FYnfinity'가 되지 않게 없음으로
  const st=FI_K.filter(k=>!FI_M[k].ref&&!FI_M[k].alt).map(k=>fiStat(rows,k,L)), has=st.filter(t=>t.me.v!=null&&t.md!=null);
  return {L, nb:has.filter(t=>t.better).length, na:has.length, n:rows.length};
}
function finCardHtml(cid='peer'){
  const c=CMP[cid], rows=fiRows(cid); if(rows.length<2) return '';
  const FI_GRP=FI_ST[cid].g, FI_MET=FI_ST[cid].k;
  const fys=[...new Set(rows.flatMap(r=>Object.keys(r.by).map(Number)))].sort().slice(-3), L=fys[fys.length-1];
  const me=rows.find(r=>r.self), m=FI_M[FI_MET], cls=v=>v<0?(m.nr?'pos':'neg'):'';
  let h=`<div class="card" id="${c.id}">`;   // 제목은 더보기 화면 머리글(v32.4)
  if(L==null) return h+'<div class="na">재무 자료 수집 전 — DART 감사보고서 수집 후 표시</div></div>';   // v33 연도 자료가 없으면('FYdefined'·'FYN'이 되지 않게)
  // 자사 요약: 최근 연도 중앙값보다 나은 지표 수 · 그룹별
  const cmpK=FI_K.filter(k=>!FI_M[k].ref&&!FI_M[k].alt), st=Object.fromEntries(cmpK.map(k=>[k,fiStat(rows,k,L)]));
  if(me){
    const has=k=>st[k].me.v!=null&&st[k].md!=null;
    const nHas=cmpK.filter(has).length;   // v33 자사 그 해 자료가 없으면 '0/0' 대신 '자료 없음'
    h+=`<div class="nv-sum"><div class="fi-top"><b>${esc(c.selfName)}</b><span class="na">FY${String(L).slice(2)} · ${rows.length}곳 비교</span>${nHas?`<span style="margin-left:auto">중앙값보다 나은 지표 <b class="fi-big">${cmpK.filter(k=>st[k].better).length}</b><span class="na">/${nHas}</span></span>`:`<span class="na" style="margin-left:auto">${esc(c.selfName)} FY${String(L).slice(2)} 자료 없음</span>`}</div><div class="fi-gsum">`;
    FI_G.forEach(([g,gn])=>{ const ks=cmpK.filter(k=>FI_M[k].g===g);
      h+=`<button type="button" class="${g===FI_GRP?'on':''}" aria-pressed="${g===FI_GRP}" onclick="fiPick('${g}','','${cid}')"><span class="l">${gn.replace('·','·<wbr>')}</span><span class="v">${ks.filter(has).length?ks.filter(k=>st[k].better).length+'/'+ks.filter(has).length:'―'}</span><span class="fi-dots">${ks.map(k=>`<i class="${!has(k)?'x':st[k].better?'b':''}" title="${esc(FI_M[k].nm)}"></i>`).join('')}</span></button>`; });
    h+=`</div></div>`;
  }
  h+=`<div class="fi-seg" role="group" aria-label="지표 묶음">${FI_G.map(([g,gn])=>`<button type="button" aria-pressed="${g===FI_GRP}" class="${g===FI_GRP?'on':''}" onclick="fiPick('${g}','','${cid}')">${gn}</button>`).join('')}</div>`;
  h+=`<div class="chips fi-chips">${FI_K.filter(k=>FI_M[k].g===FI_GRP).map(k=>`<button type="button" class="chip${k===FI_MET?' on':''}" aria-pressed="${k===FI_MET}" onclick="fiPick('${FI_GRP}','${k}','${cid}')">${esc(FI_M[k].nm)}</button>`).join('')}</div>`;
  // 선택 지표 요약 3칸
  const s=st[FI_MET]||fiStat(rows,FI_MET,L), s0=fiStat(rows,FI_MET,L-1), mv=s.me, m0=me?fiVal(me,FI_MET,L-1):{t:'―'};
  h+=`<div class="fi-mhead"><b>${esc(m.nm)}</b><span class="na">${esc(m.dir)}</span></div>`;
  // v32.9 회계기준이 섞인 비교군 — 리스·RCPS 처리 차이가 큰 지표에서 안내
  const nI=rows.filter(r=>r.std==='K-IFRS').length, nG=rows.filter(r=>r.std==='일반기업회계기준').length, nS=rows.filter(r=>r.std==='중소기업회계기준').length, nU=rows.filter(r=>!r.std).length;
  if(nI&&(nG||nS||nU)&&['nd','ndx','dr','ocf','fcf','conv','roe'].includes(FI_MET))
    h+=`<div class="fi-warn">${ic('warn',14)} 회계기준 혼재 — K-IFRS ${nI}곳 · K-GAAP ${nG}곳${nS?` · 중소기업회계기준 ${nS}곳`:''}${nU?` · 미확인 ${nU}곳`:''}. K-IFRS는 리스부채·RCPS를 부채로 잡고 임차료가 감가상각비·이자로 나뉘어, 이 지표가 회사마다 다른 잣대로 계산됨<br><button type="button" class="chip" onclick="fiPick('stab','nd2','${cid}');refocus(true,'#${c.id} .fi-chips .chip.on')">순차입금(리스·RCPS 제외)로 비교 ›</button></div>`;
  if(me){
    const tr=(mv.c!=null&&m0.c!=null&&!m.ref)?(mv.c===m0.c?'변화 없음':((m.hi?mv.c>m0.c:mv.c<m0.c)?'<span class="pos">개선</span>':'<span class="neg">악화</span>')):'<span class="na">―</span>';
    h+=`<div class="fi-mbox"><div><span class="l">${esc(c.selfName)} FY${String(L).slice(2)}</span><span class="v ${mv.v!=null?cls(mv.v):'na'}">${mv.v!=null?m.fmt(mv.v):esc(mv.t)}</span><span class="s">${m.ref?'참고 지표':s.rank?`${s.rank}위/${s.n}`:'순위 없음'}${s.better?' · <b style="color:var(--accent)">중앙값↑</b>':''}</span></div>
      <div><span class="l">비교군 중앙값</span><span class="v">${s.mdv!=null?m.fmt(s.mdv):'―'}</span><span class="s">${esc(c.selfName)} 제외 ${s.np}곳</span></div>
      <div><span class="l">전년 대비</span><span class="v">${tr}</span><span class="s">FY${String(L-1).slice(2)} ${m0.v!=null?m.fmt(m0.v):esc(m0.t)}</span></div></div>`;
  }
  // 3개년 표 — 자사 맨 위, 나머지 최근 매출 큰 순
  const order=[me,...rows.filter(r=>!r.self).sort((a,b)=>((b.by[L]||{}).rev??-1)-((a.by[L]||{}).rev??-1))].filter(Boolean);
  const cp=v=>fiPct(v,FI_MET==='nd'?0:1);
  h+=`<div class="tblwrap"><table class="fi-tbl"><tr><th>기업</th>${fys.map(f=>`<th>FY${String(f).slice(2)}</th>`).join('')}</tr>`;
  order.forEach(r=>{
    const nm=nmSplit(r.name), sub=(nm.brand?`<span>${esc(nm.brand)}</span>`:'')+(r.std?`<span class="std-b ${r.std==='K-IFRS'?'ifrs':'gaap'}">${esc(STD_SH[r.std]||r.std)}</span>`:'');   // v32.12 법인명 / 브랜드·회계기준
    h+=`<tr class="${r.self?'me':''}" tabindex="0" style="cursor:pointer" onclick="goDetail('${r.key}')"><td title="${esc(r.name)}">${logoImg(r.key,false,r.name)}<span class="fi-nm">${esc(nm.main)}</span>${sub?`<span class="fi-nsub">${sub}</span>`:''}</td>`;
    fys.forEach(f=>{ const x=fiVal(r,FI_MET,f);
      if(x.v==null){ h+=`<td class="na">${esc(x.t)}</td>`; return; }
      let ex='';
      if(r.self&&!m.ref){ const t=fiStat(rows,FI_MET,f); if(t.rank) ex=t.better?`<span class="fi-b"><span class="pg-badge">${t.rank}위</span></span>`:`<span class="pg-rk">${t.rank}위/${t.n}</span>`; }
      h+=`<td><span class="${cls(x.v)}">${m.fmt(x.v)}</span>${m.c&&x.c!=null?`<span class="fi-sub">${cp(x.c)}</span>`:''}${ex}</td>`; });
    h+=`</tr>`;
  });
  h+=`<tr class="fi-med"><td>중앙값<span class="pg-rk">${me?esc(c.selfName)+' 제외':''}</span></td>${fys.map(f=>{const t=fiStat(rows,FI_MET,f); return `<td>${t.mdv!=null?m.fmt(t.mdv):'―'}${m.c&&t.md!=null?`<span class="fi-sub">${cp(t.md)}</span>`:''}</td>`;}).join('')}</tr></table></div>`;
  if(m.cn) h+=`<div class="note" style="margin-top:4px">작은 글씨 = ${esc(m.cn)}${m.ref?'':' · 순위·배지는 이 비율 기준(회사 규모 차이 보정)'}</div>`;
  // 최근 연도 순위 막대
  const bars=rows.map(r=>({r,x:fiVal(r,FI_MET,L)})).filter(o=>o.x.v!=null&&o.x.c!=null).sort((a,b)=>m.hi||m.ref?b.x.c-a.x.c:a.x.c-b.x.c);
  const bf=m.c?cp:m.fmt, md=m.ref?null:s.md;
  if(bars.length){
    const CL=m.clip?(t=>Math.max(-m.clip,Math.min(m.clip,t))):(t=>t);
    const all=bars.map(o=>CL(o.x.c)).concat(md!=null?[CL(md)]:[]), lo=Math.min(0,...all), hi=Math.max(0,...all), sp=(hi-lo)||1, X=t=>(CL(t)-lo)/sp*100;
    h+=`<div class="ndate">FY${String(L).slice(2)} ${m.ref?'비교(참고)':'순위'}${m.cn?' · '+esc(m.cn):''}${m.hi||m.ref?'':' · 낮을수록 위'}</div><div class="pg-bars">`;
    bars.forEach(o=>{ const v=o.x.c, a=X(Math.min(0,v)), b=X(Math.max(0,v));
      h+=`<div class="pg-row${o.r.self?' me':''}" role="button" tabindex="0" onclick="goDetail('${o.r.key}')"><span class="pg-nm" title="${esc(o.r.name)}">${esc(nmBrand(o.r.name))}</span><span class="pg-tr"><i class="pg-zero" style="left:${X(0)}%"></i>${md!=null?`<i class="pg-med" style="left:${X(md)}%"></i>`:''}<i class="pg-bar${v<0?' neg':''}" style="left:${a}%;width:${Math.max(b-a,0.8)}%"></i></span><b class="pg-v">${bf(v)}</b></div>`; });
    h+=`</div>`;
    if(m.clip&&bars.some(o=>Math.abs(o.x.c)>m.clip)) h+=`<div class="note" style="margin-top:4px">막대는 ±${m.clip}%에서 자름(숫자는 실제 값)</div>`;
    const no=rows.filter(r=>fiVal(r,FI_MET,L).v==null);
    if(no.length) h+=`<div class="note" style="margin-top:4px">제외: ${no.map(r=>esc(r.name)+'('+esc(fiVal(r,FI_MET,L).t)+')').join(' · ')}</div>`;
    h+=`<div class="src-legend" style="margin-top:8px">${me?`<span><i style="background:var(--accent)"></i>${esc(c.selfName)}</span>`:''}<span><i style="background:var(--sub);opacity:.4"></i>${c.who}</span>${md!=null?`<span><i style="border-left:1.5px dashed var(--sub);width:0;height:11px;border-radius:0"></i>중앙값${me?'('+esc(c.selfName)+' 제외)':''}</span>`:''}</div>`;
  } else h+=`<div class="na" style="margin-top:8px">비교할 수치 없음</div>`;
  h+=`<div class="fi-def"><dl><dt>식</dt><dd>${esc(m.f)}</dd><dt>좋은 방향</dt><dd>${esc(m.dir)}</dd><dt>왜 보나</dt><dd>${esc(m.why)}</dd></dl></div>`;
  h+=`<div class="note" style="margin-top:8px">${c.src}${m.bs?' · 재무상태표·현금흐름표':''}${me?' · 파란 배지 = 비교군 중앙값보다 나음':''}${cid==='fb'&&m.bs?' · 상장 3곳은 사업보고서 재무제표(감가상각비가 따로 없으면 EBITDA 지표 ―)':''} · 순위는 수치가 있는 기업끼리 · '확인 필요' = 자산≠부채+자본, 두 감사보고서의 같은 연도 값이 다름, 또는 부채 항목 합이 부채총계와 다름 · 행을 누르면 기업 상세</div></div>`;
  return h;
}
// 기업 상세: 유통사 재무 지표 3개년(재무상태표·현금흐름이 있는 법인만)
function fiDetailCard(e){
  if(!(e.years||[]).some(y=>y.fin)) return '';
  const r={key:'krd:'+e.id,name:e.name,by:{}}; (e.years||[]).filter(y=>y.rev!=null&&y.end).forEach(y=>{r.by[+y.end.slice(0,4)]=y;});
  const fys=Object.keys(r.by).map(Number).sort().slice(-3);
  let h=`<div class="card"><h3>재무 지표 3개년 — DART 별도${e.acct_std?' · '+esc(STD_SH[e.acct_std]||e.acct_std):''}</h3><div class="tblwrap"><table class="fi-tbl"><tr><th>지표</th>${fys.map(f=>`<th>FY${String(f).slice(2)}</th>`).join('')}</tr>`;
  FI_G.forEach(([g,gn])=>{
    h+=`<tr class="fi-gh"><td colspan="${fys.length+1}">${gn}</td></tr>`;
    FI_K.filter(k=>FI_M[k].g===g).forEach(k=>{ const m=FI_M[k];
      const ns=nmSplit(m.nm);   // v32.12 '순차입금(리스·RCPS 제외)' → 2줄(조건이 잘려 안 보이던 문제)
      h+=`<tr><td>${esc(ns.main)}${ns.brand?`<span class="fi-nsub" style="margin-left:0">${esc(ns.brand)}</span>`:''}</td>${fys.map(f=>{const x=fiVal(r,k,f); return x.v==null?`<td class="na">${esc(x.t)}</td>`:`<td class="${x.v<0?(m.nr?'pos':'neg'):''}">${m.fmt(x.v)}</td>`;}).join('')}</tr>`; });
  });
  const FI_NM={assets:'자산',liab:'부채',equity:'자본',cash:'현금',stfin:'단기금융상품',ar:'매출채권',ap:'매입채무',borrow:'차입금',lease:'리스부채',inv:'재고',ocf:'OCF',capex:'CAPEX',da:'감가상각비'};
  const chk=(e.years||[]).filter(y=>y.fin&&(y.fin.chk||(y.fin.bad||[]).length));
  h+=`</table></div>${chk.length?`<div class="note">확인 필요: ${chk.map(y=>`FY${y.end.slice(2,4)} ${esc([y.fin.chk,(y.fin.bad||[]).length?'값 확인('+y.fin.bad.map(k=>FI_NM[k]||k).join('·')+')':''].filter(Boolean).join(' · '))}`).join(' / ')}</div>`:''}<div class="note">식·좋은 방향은 더보기 › 유통사 비교·패션 브랜드에서 지표를 누르면 보입니다</div></div>`;
  return h;
}
function cmpGrowth(cid,m){ CMP_GROWTH[cid]=m; const el=document.getElementById(CMP[cid].id); if(el) el.outerHTML=cmpCardHtml(cid); }
function peerTip(el,tid){
  const t=document.getElementById(tid||'peerCardTip'); if(!t) return;
  t.innerHTML=`${esc(el.dataset.tip||'')} <button type="button" class="go" onclick="goDetail('${el.dataset.k}')">상세 ›</button>`;
}
function buildKR(){
  const el=document.getElementById('krBody');
  const top=crossChartHtml()+naverCardHtml();   // 플랫폼은 기업 탭 칩, 패션·아이웨어 비교는 더보기(v32.5)
  if(!KR||!KR.series||!Object.keys(KR.series).length){
    el.innerHTML=top+'<div class="na">국내 지표 없음 — 수집 워크플로우(update-kosis) 첫 실행 전이거나 조회 실패(미확인)</div>';
    xcBind();
    return;
  }
  let h=top+`<div class="ndate">KOSIS 국내 지표 (월간)</div><div class="note" style="margin:0 0 8px">갱신: ${KR.generated_at||'―'}</div>`;
  const groups=[
    ["소매판매액지수",["retail_apparel","retail_shoesbag","retail_total"]],
    ["업태별 판매액지수",["store_fashion","store_internet","store_dept"]],
    ["온라인쇼핑 거래액",["online_apparel","online_shoes","online_bag","online_fashionacc","online_sports"]],
    ["소비자물가",["cpi_apparel"]],
  ];
  groups.forEach(([title,keys])=>{
    const avail=keys.filter(k=>KR.series[k]);
    if(!avail.length) return;
    h+=`<div class="ndate">${title}</div>`;
    avail.forEach(k=>{
      const s=KR.series[k];
      const prds=Object.keys(s.values).sort();
      const last=prds[prds.length-1];
      const v=s.values[last], y=s.yoy?s.yoy[last]:null;
      const vals=prds.slice(-25).map(p=>s.values[p]);
      const isIdx=/지수|100/.test(s.unit||'');
      // 금액 단위: 원자료가 백만원 → 1,000,000백만원 = 1조 / 100백만원 = 1억
      const disp=isIdx?v.toFixed(1)
        :(v>=1000000?(v/1000000).toFixed(2)+'조원':(v/100).toLocaleString(undefined,{maximumFractionDigits:0})+'억원');
      h+=`<div class="krcard" data-k="${k}" role="button" tabindex="0" aria-expanded="false">
        <div class="krhead"><span class="krname">${esc(s.label)}</span>
          <span class="krval">${disp}
            <span class="kryoy">${fmt(y,1,true)}</span>
          </span></div>
        <div class="krmeta">${fmtPrd(last)} 기준 · ${esc(s.unit||'')} · ${s.table}${staleTag(s.stale_since)}</div>
        ${spark(vals,260,34,false,k==='cpi_apparel')}
        <div class="krtbl" id="krt-${k}"><table><tr><th>월</th><th>값</th><th>전년 대비</th></tr>
        ${prds.slice(-13).reverse().map(p=>{
          const yy=s.yoy?s.yoy[p]:null;
          const pv=s.values[p];
          const pdisp=isIdx?pv.toFixed(1)
            :(pv>=1000000?(pv/1000000).toFixed(2)+'조원':(pv/100).toLocaleString(undefined,{maximumFractionDigits:0})+'억원');
          return `<tr><td>${fmtPrd(p)}</td><td>${pdisp}</td>
          <td>${fmt(yy,1,true)}</td></tr>`;
        }).join('')}</table></div>
      </div>`;
    });
  });
  el.innerHTML=h;
  xcBind();
  el.querySelectorAll('.krcard').forEach(c=>{
    c.onclick=()=>{ const o=document.getElementById('krt-'+c.dataset.k).classList.toggle('open'); c.setAttribute('aria-expanded',o?'true':'false'); };
  });
}

/* ── 더보기 (v31): 메뉴 · 환율 · 해외직구 · 수집 상태 ── */
let MORE_VIEW=null, CB_CAT='fashion';
const FX_ALERT=['JPY','EUR','USD'];
const FX_LBL={JPY:'엔(100엔)',EUR:'유로',USD:'달러',GBP:'파운드',BRL:'브라질 헤알',CHF:'스위스 프랑',CNY:'위안',HKD:'홍콩 달러',SAR:'사우디 리얄'};
const FX_SH={JPY:'엔',EUR:'유로',USD:'달러'};
const fxMul=c=>c==='JPY'?100:1;
const wonR=v=>Math.round(v).toLocaleString('ko-KR');
const pctU=v=>pp(v);   // v33 0.0%는 부호 없음(D9)
const fxC=v=>{ const r=+v.toFixed(1); return r<0?'pos':r>0?'neg':''; };   // 환율: 쌈(내림) 파랑 · 비쌈 짙은 주황 · 0.0%는 색 없음
const fxLine=l=>l===0?'1년 평균':`${l>0?'+':'−'}${Math.abs(l)}% 선`;
const mdTxt=d=>d?`${+d.slice(5,7)}/${+d.slice(8,10)}`:'';
function fxAlertsAll(){
  const FXD=DATA.fx||{}, out=[];
  FX_ALERT.forEach(c=>((FXD[c]||{}).alerts||[]).forEach(a=>out.push({...a,c})));
  return out.sort((a,b)=>b.date.localeCompare(a.date));
}
const fxAlertTxt=a=>`${FX_SH[a.c]} ${wonR(a.rate*fxMul(a.c))}원 · ${fxLine(a.line)} ${a.dir==='dn'?'아래로':'위로'} (${pctU(a.dev)})`;
function fxSpark(f,c){
  const H=f.hist||[]; if(H.length<2) return '';
  const W=300,Ht=52,P=4,m=fxMul(c), vs=H.map(x=>x[1]*m), avg=f.avg1y*m, dn=f.next_dn*m, up=f.next_up*m;
  const all=[...vs,avg,dn,up], lo=Math.min(...all)*0.997, hi=Math.max(...all)*1.003;
  const x=i=>P+(W-2*P)*i/(vs.length-1), y=v=>P+(Ht-2*P)*(1-(v-lo)/(hi-lo));
  const d=vs.map((v,i)=>(i?'L':'M')+x(i).toFixed(1)+' '+y(v).toFixed(1)).join(' ');
  const ln=(v,a)=>`<line x1="${P}" x2="${W-P}" y1="${y(v).toFixed(1)}" y2="${y(v).toFixed(1)}" ${a} vector-effect="non-scaling-stroke"/>`;
  const at={}; H.forEach((h,i)=>{at[h[0]]=i;});
  const dots=(f.alerts||[]).filter(a=>at[a.date]!=null).map(a=>`<circle cx="${x(at[a.date]).toFixed(1)}" cy="${y(vs[at[a.date]]).toFixed(1)}" r="2.6" fill="${a.dir==='dn'?'var(--pos)':'var(--neg)'}"/>`).join('');
  return `<svg class="fxsv" viewBox="0 0 ${W} ${Ht}" preserveAspectRatio="none" role="img" aria-label="${esc(FX_LBL[c]||c)} 1년 추이">
    <path d="${d} L${x(vs.length-1).toFixed(1)} ${Ht-P} L${x(0)} ${Ht-P} Z" fill="var(--barbg)" stroke="none"/>
    ${ln(avg,'stroke="var(--sub)" stroke-width="1" stroke-dasharray="4 3"')}${ln(dn,'stroke="var(--pos)" stroke-width="1.2"')}${ln(up,'stroke="var(--neg)" stroke-width="1.2"')}
    <path d="${d}" fill="none" stroke="var(--sub)" stroke-width="1.4" vector-effect="non-scaling-stroke"/>${dots}
    <circle cx="${x(vs.length-1).toFixed(1)}" cy="${y(vs[vs.length-1]).toFixed(1)}" r="3.4" fill="var(--tx)"/></svg>`;
}
function fxGauge(f){
  const devs=(f.hist||[]).map(h=>(h[1]/f.avg1y-1)*100); if(!devs.length) return '';
  const lo=Math.min(-3,Math.floor(Math.min(...devs,f.dev_pct))-1), hi=Math.max(3,Math.ceil(Math.max(...devs,f.dev_pct))+1);
  const p=v=>((v-lo)/(hi-lo)*100).toFixed(2)+'%', s=f.seen30||[f.dev_pct,f.dev_pct];
  let h=`<div class="fg-trk"></div><div class="fg-seen" style="left:${p(s[0])};width:calc(${p(s[1])} - ${p(s[0])})"></div>`;
  for(let k=lo;k<=hi;k++) h+=`<div class="fg-tk${k===0?' z':''}" style="left:${p(k)}"></div>`;
  const labs=new Set([lo,0,hi]), gap=(hi-lo)*.2; [-10,-5,5,10].forEach(k=>{ if(k>lo+gap&&k<hi-gap) labs.add(k); });   // 13px 라벨이 끝 라벨과 겹치지 않게 양 끝 20% 안은 뺌
  labs.forEach(k=>{ h+=`<div class="fg-lb${k===lo?' l0':k===hi?' l1':''}" style="left:${p(k)}">${k===0?'평균':(k>0?'+':'−')+Math.abs(k)+'%'}</div>`; });   // v33 처음·끝 라벨은 안쪽 정렬
  return `<div class="fgauge" aria-label="1년 평균 대비 ${pctU(f.dev_pct)}">${h}<div class="fg-me" style="left:${p(f.dev_pct)}"></div></div>`;
}
function fxCard(c,f){
  const m=fxMul(c);
  if(f.avg1y==null) return `<div class="fxc"><div class="fxtop"><b>${esc(FX_LBL[c]||c)}</b>${staleTag(f.stale_since)}</div><div class="fxv num">${wonR(f.rate*m)}원</div><div class="note">1년 평균 계산 자료 부족 — 1% 칸 알림 없음</div></div>`;
  const al=f.alerts||[], last=al[al.length-1], now=last&&last.date===f.asof?last:null, ndn=al.filter(a=>a.dir==='dn').length;
  const pill=now?`<span class="fpill ${now.dir}">새 알림 · ${fxLine(now.line)} ${now.dir==='dn'?'아래로':'위로'}</span>`
                :`<span class="fpill wait">다음 ↓${wonR(f.next_dn*m)} · ↑${wonR(f.next_up*m)}</span>`;
  return `<div class="fxc ${now?now.dir:''}"><div class="fxtop"><b>${esc(FX_LBL[c]||c)}</b>${staleTag(f.stale_since)}${pill}</div>
    <div class="fxv num">${wonR(f.rate*m)}원${f.chg_pct!=null?`<small>1년 전 ${wonR(f.yago*m)}원 · <span class="${fxC(f.chg_pct)}">${pctU(f.chg_pct)}</span></small>`:''}</div>
    <div class="fxmeta"><div><span>1년 평균 대비</span><b class="num ${fxC(f.dev_pct)}">${pctU(f.dev_pct)}</b></div>
      <div><span>다음 내림 알림</span><b class="num pos">${wonR(f.next_dn*m)}원↓</b></div>
      <div><span>다음 오름 알림</span><b class="num neg">${wonR(f.next_up*m)}원↑</b></div></div>
    ${fxGauge(f)}${fxSpark(f,c)}
    <div class="fxcnt">1년 평균 ${wonR(f.avg1y*m)}원 · 지난 1년 알림 ${al.length}번 (내림 ${ndn} · 오름 ${al.length-ndn}) · ${esc(f.asof||'')} 기준</div></div>`;
}
function moreHead(t,sub){   // v33 S2: 더보기 하위 화면 머리 = '‹ 바로 전 화면'(주소로 바로 열었으면 더보기) + 제목, 그 아래 부제 한 줄
  const lb=backLbl(ROUTE,'더보기');
  return `<div class="phead dethead"><button type="button" class="hd-back mback" onclick="moreOpen(null)" aria-label="${esc(jo(lb,'으로','로',1))} 돌아가기">${ic('left',24,'s2')}<span class="hd-bl">${esc(lb)}</span></button><h1>${esc(t)}</h1><span aria-hidden="true"></span></div>${sub?`<p class="hd-sub2">${sub}</p>`:''}`;
}
function moreFxHtml(){
  const FXD=DATA.fx||{}, al=fxAlertsAll();
  let h=moreHead('환율','현지 통화 1단위의 원화 값 (엔은 100엔) · 갱신 <span class="nw">'+esc(DATA.generated_at||'')+'</span>');
  h+=`<div class="card"><h3>최근 알림 <span class="na" style="font-weight:400">1년 평균 대비 1% 선을 새로 넘은 날</span></h3>`
    +(al.length?`<div class="frec">${al.slice(0,6).map(a=>`<div><span class="d">${mdTxt(a.date)}</span><i class="${a.dir}"></i><span>${esc(fxAlertTxt(a))}</span></div>`).join('')}</div>`:'<div class="na">지난 1년 알림 없음</div>')+`</div>`;
  const cards=FX_ALERT.filter(c=>FXD[c]).map(c=>fxCard(c,FXD[c])).join('');
  h+=cards?`<div class="fxgrid">${cards}</div>`:'<div class="card"><div class="na">환율 수집 전 — 다음 갱신 후 표시</div></div>';
  h+=`<div class="fleg"><span><i></i>1년 추이</span><span><i class="avg"></i>1년 평균</span><span><i class="ldn"></i>다음 내림 선</span><span><i class="lup"></i>다음 오름 선</span><span><i class="dn"></i>내림 알림</span><span><i class="up"></i>오름 알림</span><span>칸 막대: 눈금 1% · 굵은 눈금 = 1년 평균 · 네모 표시 = 지금 · 파란 구간 = 최근 30일</span></div>`;
  const rest=Object.keys(FXD).filter(c=>FX_ALERT.indexOf(c)<0);
  // v33.2 파운드는 1년 평균 대비도(fetch_data v4.14, 브랜드 점검표 환율 점수 기준) — 1% 칸 알림은 없음
  if(rest.length) h+=`<div class="card"><h3>알림 없이 표시만</h3>${rest.map(c=>{ const f=FXD[c];
    const dv=f.dev_pct!=null?` <span class="${fxC(f.dev_pct)}">${pctU(f.dev_pct)}</span> <span class="na">1년 평균 대비</span>`:'';   // 파운드: 점검표 점수 기준(1년 평균)을 먼저
    return `<div class="fplain"><span>${esc(FX_LBL[c]||f.name||c)}${staleTag(f.stale_since)}</span><span class="num">${wonR(f.rate*fxMul(c))}원${dv}${f.chg_pct!=null?`${dv?'<br>':' '}<span class="${fxC(f.chg_pct)}">${pctU(f.chg_pct)}</span> <span class="na">1년 전 대비${f.via?' · '+esc(f.via):''}</span>`:''}</span></div>`; }).join('')}</div>`;
  h+=`<div class="card"><h3>알림을 이렇게 참고</h3><div class="fuse">
    <div><b class="pos">▼ 내릴 때</b><ul><li>외화 값이 싸짐 → 매입 부담 줄어듦</li><li>해외 매입 결제 시점 앞당김 검토</li><li>선매입·추가 발주 검토</li></ul></div>
    <div><b class="neg">▲ 오를 때</b><ul><li>외화 값이 비싸짐 → 매입 부담 커짐</li><li>선물환으로 환율 미리 확정 검토</li><li>결제 시점 조정 · 수출 비중 확대 검토</li></ul></div></div>
    <div class="note">판단 참고용 지표입니다. 실제 거래는 은행 고시 환율·수수료를 함께 확인하세요.</div></div>`;
  h+=`<div class="card"><h3>알림 규칙</h3><ol class="frules">
    <li>기준은 1년 평균(최근 365일 이동평균), 1% 단위 선(−1%, −2% … / +1%, +2% …).</li>
    <li>새 선을 넘어 내려가거나 올라간 날 알림 1번 — 매일 12:23 일일 점검이 휴대폰으로 보냄.</li>
    <li>최근 30영업일 안에 이미 닿은 선은 다시 알리지 않음(선 근처 반복 방지).</li>
    <li>'다음 알림' 가격은 지금의 1년 평균 기준이라 평균이 움직이면 조금씩 바뀝니다.</li></ol></div>`;
  return h;
}
/* 해외직구: KOSIS 백만원 단위 */
const cbMoney=v=>v==null?'―':(v>=1000000?(v/1000000).toFixed(2)+'조':Math.round(v/100).toLocaleString('ko-KR')+'억');
const cbPrd=p=>p?`${p.slice(0,4)}년 ${+p.slice(4)}분기`:'';
const cbPrdS=p=>p?`${p.slice(2,4)}년 ${+p.slice(4)}분기`:'';
const cbPrev=p=>`${+p.slice(0,4)-1}${p.slice(4)}`;
const cbVal=(k,p)=>{ const s=((KR&&KR.cross_border&&KR.cross_border.series)||{})[k]; return s&&s.values?(s.values[p]??null):null; };
const cbYoy=(c,pv)=>(c!=null&&pv)?(c/pv-1)*100:null;
const CB_CTY=[['cn','중국'],['us','미국'],['eu','유럽'],['jp','일본']];
function cbBarsHtml(){
  const CB=KR.cross_border, L=CB.last, P=cbPrev(L), g=CB_CAT;
  const rows=CB_CTY.map(([k,nm])=>({k,nm,v:cbVal(k+'|'+g,L),pv:cbVal(k+'|'+g,P)})).filter(r=>r.v!=null);
  const tot=cbVal('total|'+g,L), totP=cbVal('total|'+g,P);
  if(tot!=null&&rows.length){ const sm=rows.reduce((a,r)=>a+r.v,0), sp=rows.every(r=>r.pv!=null)?rows.reduce((a,r)=>a+r.pv,0):null;
    if(tot-sm>0) rows.push({k:'etc',nm:'기타',v:tot-sm,pv:(totP!=null&&sp!=null&&totP-sp>0)?totP-sp:null}); }
  rows.sort((a,b)=>(a.k==='etc')-(b.k==='etc')||b.v-a.v);
  const catNm=((CB.names||{})['total|'+g]||'').split(' / ')[1]||(g==='fashion'?'의류·패션':'스포츠·레저');
  let h=`<h3>나라별 · ${cbPrd(L)}</h3><div class="chips" style="margin-bottom:8px">${[['fashion','의류·패션'],['sports','스포츠·레저']].map(([k,l])=>`<button type="button" class="chip${CB_CAT===k?' on':''}" aria-pressed="${CB_CAT===k}" onclick="CB_CAT='${k}';document.getElementById('cbCard').innerHTML=cbBarsHtml()">${l}</button>`).join('')}</div>`;
  if(!rows.length) return h+'<div class="na">자료 없음</div>';
  const mx=Math.max(...rows.map(r=>r.v));
  h+=rows.map(r=>{ const y=cbYoy(r.v,r.pv); return `<div class="cb-row"><span class="lb">${r.nm}</span><div class="bar-wrap"><div class="bar${r.k==='eu'||r.k==='jp'?'':' cb-oth'}" style="width:${(r.v/mx*100).toFixed(1)}%"></div><span class="bar-val num">${cbMoney(r.v)}</span></div><span class="yy">${y!=null?fmt(y,1,true):'<span class="na">―</span>'}</span></div>`; }).join('');
  return h+`<div class="note">통계청 상품군 '${esc(catNm)}' · 합계 ${cbMoney(tot)}원 · 파란 막대 = 유럽·일본(병행수입 주요 소싱 지역) · 오른쪽 = 전년 같은 분기 대비</div>`;
}
function cbTrendHtml(){
  const S=KR.cross_border.series, out=[];
  [['us','미국'],['cn','중국'],['eu','유럽'],['jp','일본']].forEach(([k,nm])=>{
    const s=S[k+'|fashion']; if(!s||!s.values) return;
    const ps=Object.keys(s.values).sort().slice(-8); if(ps.length<2) return;
    const v=ps.map(p=>s.values[p]), y=s.yoy?s.yoy[ps[ps.length-1]]:null;
    const W=200,H=36,P=3,lo=Math.min(...v)*0.95,hi=Math.max(...v)*1.03, n=v.length-1;
    const x=i=>P+(W-2*P)*i/n, yy=a=>P+(H-2*P)*(1-(a-lo)/(hi-lo));
    const d=v.map((a,i)=>(i?'L':'M')+x(i).toFixed(1)+' '+yy(a).toFixed(1)).join(' ');
    out.push(`<div class="cb-tr"><div class="h"><b>${nm}</b><span class="num">${cbMoney(v[n])} ${y!=null?fmt(y,1,true):''}</span></div>
      <svg viewBox="0 0 ${W} ${H}" preserveAspectRatio="none" role="img" aria-label="${nm} 최근 8분기"><path d="${d} L${x(n).toFixed(1)} ${H-P} L${x(0)} ${H-P} Z" fill="var(--barbg)" stroke="none"/>
      <path d="${d}" fill="none" stroke="var(--accent)" stroke-width="1.5" vector-effect="non-scaling-stroke"/><circle cx="${x(n).toFixed(1)}" cy="${yy(v[n]).toFixed(1)}" r="3" fill="var(--accent)"/></svg>
      <div class="ax"><span>${cbPrdS(ps[0])}</span><span>${cbPrdS(ps[n])}</span></div></div>`);
  });
  return out.length?`<div class="card"><h3>최근 8분기 · 의류·패션 직구</h3><div class="cb-trend">${out.join('')}</div></div>`:'';
}
function moreCbHtml(){
  const CB=KR&&KR.cross_border;
  let h=moreHead('해외직구','통계청 온라인쇼핑동향 · 해외직접구매액 · 분기');
  if(!CB||!CB.series) return h+'<div class="card"><div class="na">해외직구 자료 수집 전 — update-kosis 실행 후 표시</div></div>';
  const L=CB.last, P=cbPrev(L);
  const tt=cbVal('total|total',L), tf=cbVal('total|fashion',L);
  const ej=['eu','jp'].map(k=>cbVal(k+'|fashion',L)), ejp=['eu','jp'].map(k=>cbVal(k+'|fashion',P));
  const ejS=ej.every(v=>v!=null)?ej[0]+ej[1]:null, ejP=ejp.every(v=>v!=null)?ejp[0]+ejp[1]:null;
  const kp=(l,v,y,sh)=>`<div class="kpi"><div class="l">${l}</div><div class="v num">${cbMoney(v)}</div><div class="s">${y!=null?fmt(y,1,true):'<span class="na">―</span>'}${sh?' · '+sh:''}</div></div>`;
  h+=`<div class="note" style="margin:0 0 6px">${cbPrd(L)} · 전년 같은 분기 대비${staleTag(CB.stale_since)}</div>`;
  h+=`<div class="kpis cbk">${kp('직구 전체',tt,cbYoy(tt,cbVal('total|total',P)))}${kp('의류·패션',tf,cbYoy(tf,cbVal('total|fashion',P)),(tt&&tf!=null)?'전체의 '+Math.round(tf/tt*100)+'%':'')}${kp('유럽+일본 패션',ejS,cbYoy(ejS,ejP),(tf&&ejS!=null)?'패션의 '+Math.round(ejS/tf*100)+'%':'')}</div>`;
  h+=`<div class="card" id="cbCard">${cbBarsHtml()}</div>`;
  h+=cbTrendHtml();
  h+=`<div class="cb-read"><b>읽는 법</b> — 유럽·일본 패션 직구가 늘면 그 브랜드의 국내 수요는 있다는 뜻이고, 정식 유통보다 싸게 사려는 고객이 직구로 빠진다는 신호이기도 합니다. 병행수입 가격이 직구 가격(관부가세·배송비 포함)보다 경쟁력이 있는지 점검할 때 씁니다.</div>`;
  h+=`<div class="note">출처: KOSIS ${esc(CB.table||'')} ${esc(CB.table_name||'')} · 단위 ${esc(CB.unit||'')}(화면은 억·조원) · 분기가 끝나고 약 2달 뒤 발표 · 갱신 ${esc(KR.generated_at||'')}<br>유럽 = 유럽연합+영국+기타 유럽 합계(통계청 지역 분류)</div>`;
  return h;
}
/* ── v33.4 물류(대표 지시 2026-10-16 '만들어줘') — docs/logistics.json(logistics_fetch v1): 한국향 운임(관세청 · 월) · 부산발 운임(KCCI · 주) ·
   바닷길(IMF PortWatch 해협·항만 · 주) · 전 세계 정시율(Sea-Intelligence · 월). '전쟁 전' = 2026-02-28 미국·이스라엘의 이란 공격 직전
   (관세청·정시율 = 2026년 2월, KCCI = 2월 마지막 발표, 해협·항만 = 1/1~2/27 하루 평균). 색: 트렉시에 좋은 쪽 파랑 · 나쁜 쪽 짙은 주황.
   v33.5 세 묶음: 수입(적출 거점 → 부산 · 항공 → 인천) · 수출(부산 → 해외) · 공통 위험 신호 ── */
const LG_WAR=(LOGI&&LOGI.war_start)||'2026-02-28', LG_PRE_M=LG_WAR.slice(0,7);   // 전쟁이 2/28(달 마지막 날) 시작이라 2월 자료 = 전쟁 전
let LG_KCS='kcs_sea_import';
const lgMon=m=>m?`${m.slice(2,4)}.${m.slice(5,7)}`:'';   // '2026-08' → '26.08'
const lgMd=d=>d?`${+d.slice(5,7)}/${+d.slice(8,10)}`:'';
const lgYm=d=>d?`${d.slice(2,4)}.${d.slice(5,7)}`:'';   // 그래프 왼쪽 끝 = 연.월('25.10')
const lgYmW=d=>d?lgYm(new Date(Date.parse(d+'T00:00:00Z')+3*86400000).toISOString().slice(0,10)):'';   // 주(월요일 시작) → 그 주 가운데 날의 연.월(2024-12-30 주 = '25.01')
const lgRatio=(a,b)=>(a!=null&&b)?a/b:null;
const lgC=(r,upGood)=>{ if(r==null||upGood==null) return ''; const v=+((r-1)*100).toFixed(1); return v===0?'':((v>0)===upGood?'pos':'neg'); };   // upGood = null → 색 없음
// 비율 → '+12.3%'(두 배 미만) · '×4.5'(두 배 이상) · '−83%'
const lgChg=(r,upGood)=>r==null||!isFinite(r)?'<span class="na">―</span>':`<span class="${lgC(r,upGood)}">${r>=2?'×'+r.toFixed(1):pp((r-1)*100)}</span>`;
const lgN=(v,d=0)=>v==null?'―':Number(v).toLocaleString('ko-KR',{maximumFractionDigits:d,minimumFractionDigits:d});
const lgU=(v,u,d=0,pre='')=>v==null?'―':pre+lgN(v,d)+u;   // 값이 있을 때만 단위·기호('$―'·'―척' 안 나오게)
function lgSpark(pts,o={}){   // pts=[[날짜·달, 값]] → 작은 선 그래프(전쟁 시작 세로 점선 · 마지막 점). o.accent = 파랑 선
  // v33.6 빈 값(null — 이상값으로 뺀 달 등)은 건너뛰되 x는 원래 자리(뒤 점이 앞으로 당겨지지 않게) · 마지막 값이 비면 끝 점 없음
  const P=pts.map((p,i)=>[p[0],p[1],i]).filter(p=>p[1]!=null); if(P.length<2) return '';
  const W=200,H=o.h||36,pd=3, vs=P.map(p=>p[1]), lo=Math.min(...vs,o.min??Infinity), hi=Math.max(...vs), rg=(hi-lo)||1, n=pts.length-1, e=P[P.length-1];
  const x=i=>pd+(W-2*pd)*i/n, y=v=>pd+(H-2*pd)*(1-(v-lo)/rg);
  const d=P.map((p,j)=>(j?'L':'M')+x(p[2]).toFixed(1)+' '+y(p[1]).toFixed(1)).join(' ');
  const wi=pts.findIndex(p=>p[0].length===7?p[0]>LG_WAR.slice(0,7):p[0]>=LG_WAR);   // 전쟁 시작 이후 첫 자리(달 자료는 3월부터, 주 자료는 2/28 이후 첫 주)
  const war=wi>0&&P[0][2]<wi&&e[2]>=wi?`<line x1="${x(wi-0.5).toFixed(1)}" x2="${x(wi-0.5).toFixed(1)}" y1="0" y2="${H}" stroke="var(--sub)" stroke-width="1" stroke-dasharray="3 3" vector-effect="non-scaling-stroke"/>`:'';
  const col=o.accent?'var(--accent)':'var(--tx)';
  // 끝 점 — 화면 픽셀 기준 둥근 점(넓은 화면에서 타원이 되지 않게) · overflow: 좁은 그래프에서 오른쪽 끝 점이 잘리지 않게
  return `<svg viewBox="0 0 ${W} ${H}" preserveAspectRatio="none" overflow="visible" role="img" aria-label="${esc(o.label||'추이')}"><path d="${d} L${x(e[2]).toFixed(1)} ${H-pd} L${x(P[0][2]).toFixed(1)} ${H-pd} Z" fill="var(--barbg)" stroke="none"/>${war}
    <path d="${d}" fill="none" stroke="${col}" stroke-width="1.5" vector-effect="non-scaling-stroke"/>${e[2]===n?`<path d="M${x(n).toFixed(1)} ${y(e[1]).toFixed(1)}h0" stroke="${col}" stroke-width="6" stroke-linecap="round" vector-effect="non-scaling-stroke"/>`:''}</svg>`;
}
/* 관세청 한국향 운임: 출발지 순서 = 트렉시 소싱(유럽·미국·일본) 먼저 */
const LG_KCS_LBL={'유럽연합':'유럽(EU)','미국서부':'미국 서부','미국동부':'미국 동부','미국':'미국','일본':'일본','중국':'중국','베트남':'베트남'};
const LG_KCS_ORD=['유럽연합','미국서부','미국동부','미국','일본','중국','베트남'];
function lgKcs(key){   // → {cols, rows, L(최근 달), P(전달), W(전쟁 전 달), Y(1년 전 달), B(블록)} 또는 null
  const B=LOGI&&LOGI[key]; if(!B||!B.rows||B.rows.length<2) return null;
  const R=B.rows, L=R[R.length-1], by=Object.fromEntries(R.map(r=>[r[0],r]));
  const ya=`${+L[0].slice(0,4)-1}${L[0].slice(4)}`;
  return {B,cols:B.cols,R,L,P:R[R.length-2],W:by[LG_PRE_M]||null,Y:by[ya]||null};
}
function lgKcsCard(key){   // key 없음 = 수입(바닷길·항공 칩, LG_KCS) · 'kcs_sea_export' = 수출(v33.5 한국발 운임)
  const ex=key==='kcs_sea_export', k=ex?key:LG_KCS, air=k==='kcs_air_import', K=lgKcs(k), unit=air?'원/kg':'천원/40ft';
  let h=ex?`<h3>한국발 운임 <span class="na" style="font-weight:400">관세청 · 수출신고 운임 · 월</span>${staleTag(K&&K.B.stale_since)}</h3>`
    :`<h3>한국향 운임 <span class="na" style="font-weight:400">관세청 · 수입신고 운임 · 월</span>${staleTag(K&&K.B.stale_since)}</h3>
    <div class="chips" style="margin-bottom:8px">${[['kcs_sea_import','바닷길 · 40ft 1개'],['kcs_air_import','항공 · kg당']].map(([c,l])=>`<button type="button" class="chip${LG_KCS===c?' on':''}" aria-pressed="${LG_KCS===c}" onclick="LG_KCS='${c}';document.getElementById('lgKcs').innerHTML=lgKcsCard()">${l}</button>`).join('')}</div>`;
  if(!K) return h+'<div class="na">자료 수집 전 — 다음 갱신 후 표시</div>';
  const idx=c=>K.cols.indexOf(c), cols=LG_KCS_ORD.filter(c=>idx(c)>=0);
  h+=`<div class="tblwrap"><table class="lg-tbl"><tr><th>${ex?'도착지':'출발지'}</th><th>${lgMon(K.L[0])}<br><span class="na">${unit}</span></th><th>전월</th><th>전쟁 전<br><span class="na">${lgMon(LG_PRE_M)}</span></th><th>1년 전</th></tr>`;
  cols.forEach(c=>{ const i=idx(c)+1, v=K.L[i];
    h+=`<tr${!ex&&(c==='유럽연합'||c==='미국서부'||c==='미국'||c==='일본')?' class="lg-me"':''}><td>${esc(LG_KCS_LBL[c]||c)}</td><td class="num">${lgN(v)}</td><td>${lgChg(lgRatio(v,K.P[i]),false)}</td><td>${lgChg(lgRatio(v,K.W&&K.W[i]),false)}</td><td>${lgChg(lgRatio(v,K.Y&&K.Y[i]),false)}</td></tr>`; });
  h+=`</table></div>`;
  // 추이(최근 24달): 수입 = 유럽·미국(서부)·일본(트렉시 소싱) · 수출 = 미국 서부·유럽·중국
  const pick=(ex?['미국서부','유럽연합','중국']:['유럽연합',air?'미국':'미국서부','일본']).filter(c=>idx(c)>=0), R24=K.R.slice(-24);
  h+=`<div class="cb-trend lg-tr k3">${pick.map((c,j)=>{ const i=idx(c)+1, pts=R24.map(r=>[r[0],r[i]]);
    return `<div class="cb-tr"><div class="h"><b>${esc(LG_KCS_LBL[c]||c)}</b><span class="num">${lgN(K.L[i])}</span></div>${lgSpark(pts,{accent:j===0,label:(LG_KCS_LBL[c]||c)+' 최근 24달'})}<div class="ax"><span>${lgMon(R24[0][0])}</span><span>${lgMon(K.L[0])}</span></div></div>`; }).join('')}</div>`;
  const tail=`매월 중순(15~19일쯤) 전달 자료(다음 등록 ${esc(K.B.next||'―')}) · 지난 값은 다음 해 2월까지 고쳐질 수 있음`;
  return h+(ex?why(`수출신고에 적힌 실제 운임 평균(40ft 컨테이너 1개 · 한국 항만 → 도착지) · ${tail} · 중동은 파일에 없음(부산 → 중동은 위 KCCI) · 점선 = 전쟁 시작`)   // v33.9 접음
    :why(`${air?'FOB 조건 수입신고의 kg당 운송비용 평균 — 인천공항 도착 항공 수입(특송·우편 제외)':'FOB 조건 수입신고의 실제 운임(할증료·수수료 포함) 평균 — 바닷길 수입(부산 등 전국 항만) · 단독 화주 40ft 컨테이너 1개(FCL, 소량 혼재 LCL 제외)'} · ${tail} · 홍콩·중동·싱가포르·말레이시아는 파일에 없음 · 점선 = 전쟁 시작`));
}
/* KCCI 부산발(수출) — 중동·유럽 항로 운임 흐름 */
const LG_KCCI=[['KMEI','부산 → 중동'],['KNEI','부산 → 북유럽'],['KMDI','부산 → 지중해'],['KUWI','부산 → 미주 서안'],['KUEI','부산 → 미주 동안'],['KCCI','종합 지수']];
function lgKcci(){   // → {cols, rows, L, P, W(전쟁 전 마지막 주)} 또는 null
  const B=LOGI&&LOGI.kcci; if(!B||!B.rows||B.rows.length<2) return null;
  const R=B.rows, W=[...R].reverse().find(r=>r[0]<LG_WAR)||null;
  return {B,cols:B.cols,R,L:R[R.length-1],P:R[R.length-2],W};
}
function lgKcciCard(){
  const K=lgKcci();
  let h=`<div class="card"><h3>부산발 운임 <span class="na" style="font-weight:400">KCCI · 40ft당 달러 · 매주 월</span>${staleTag(K&&K.B.stale_since)}</h3>`;
  if(!K) return h+'<div class="na">자료 수집 전 — 다음 갱신 후 표시</div></div>';
  const R52=K.R.slice(-52);
  h+=`<div class="cb-trend lg-tr">${LG_KCCI.map(([c,nm],k)=>{ const i=K.cols.indexOf(c)+1; if(i<1) return '';
    const v=K.L[i], rp=lgRatio(v,K.P[i]), rw=lgRatio(v,K.W&&K.W[i]);
    return `<div class="cb-tr"><div class="h"><b>${esc(nm)}</b><span class="num">${lgU(v,'',0,c==='KCCI'?'':'$')}</span></div>
      <div class="lg-sub">전주 ${lgChg(rp,false)} · 전쟁 전 ${lgChg(rw,false)}</div>${lgSpark(R52.map(r=>[r[0],r[i]]),{accent:k===0,label:nm+' 최근 52주'})}
      <div class="ax"><span>${lgYmW(R52[0][0])}</span><span>${lgMd(K.L[0])}</span></div></div>`; }).join('')}</div>`;
  return h+why(`한국해양진흥공사 KCCI(부산에서 나가는 수출 운임, 한국향 아님) — 중동 항로 할증·선복 변화와 선사 운임 흐름을 보는 용도 · ${lgMd(K.L[0])} 발표 · 전쟁 전 = ${K.W?lgMd(K.W[0]):'―'} 발표 · 그래프 = 최근 52주, 점선 = 전쟁 시작`)+`</div>`;   // v33.9 접음
}
/* 바닷길 — IMF PortWatch 해협 통과·항만 입항(하루 평균 척수) */
// 늘면 좋은 쪽(true) · 줄면 좋은 쪽(false) · 색 없음(null): 희망봉이 줄면 수에즈로 돌아온 것 · 우회 항만(코르파칸·푸자이라)은 늘어도 줄어도 색 없음
const LG_GOOD={chokepoint6:true,chokepoint4:true,chokepoint1:true,chokepoint7:false,'Busan':true,'Jebel Ali':true,'Khor Fakkan':null,'Fujairah':null};
const lgBaseChg=(v,b,good)=>(b==null||b<0.5)?'':lgChg(lgRatio(v,b),good);   // 전쟁 전이 거의 0척이면 % 생략
function lgWk(it){   // 마지막 '거의 다 찬' 주(4일 이상) — 없으면 마지막 주
  const W=(it&&it.weeks)||[]; for(let i=W.length-1;i>=0;i--) if((W[i][3]||0)>=4) return W[i]; return W[W.length-1]||null;
}
function lgItem(blk,id){ const B=LOGI&&LOGI[blk]; return B&&B.items?B.items.find(x=>x.id===id)||null:null; }
function lgMiss(B){   // 이번 수집에서 값이 아예 없는 항목 이름(status.failed의 '항만 입항(푸자이라)' 꼴) — 카드에 '값 없음'으로
  const lb=B&&B.label, f=((LOGI&&LOGI.status)||{}).failed||[]; if(!lb) return [];
  return f.filter(x=>typeof x==='string'&&x.startsWith(lb+'(')&&x.endsWith(')')).flatMap(x=>x.slice(lb.length+1,-1).split('·')).filter(Boolean);
}
function lgSuezShare(){   // 컨테이너선: 수에즈 ÷ (수에즈 + 희망봉) — 최근 주 · 전쟁 전 · 1년 전
  const s=lgItem('choke','chokepoint1'), c=lgItem('choke','chokepoint7'); if(!s||!c) return null;
  const sh=(a,b)=>(a!=null&&b!=null&&a+b>0)?a/(a+b)*100:null, ws=lgWk(s), wc=c.weeks.find(w=>ws&&w[0]===ws[0]);
  const ya=ws?new Date(Date.parse(ws[0]+'T00:00:00Z')-364*86400000).toISOString().slice(0,10):null;
  const ys=s.weeks.find(w=>w[0]===ya), yc=c.weeks.find(w=>w[0]===ya);
  return {wk:ws&&ws[0], now:sh(ws&&ws[2],wc&&wc[2]), pre:sh(s.base&&s.base[1],c.base&&c.base[1]), ya:sh(ys&&ys[2],yc&&yc[2])};
}
function lgChokeCard(){
  const B=LOGI&&LOGI.choke;
  let h=`<div class="card"><h3>바닷길 · 해협 통과 <span class="na" style="font-weight:400">IMF PortWatch · 컨테이너선 하루 평균 · 주</span>${staleTag(B&&B.stale_since)}</h3>`;
  if(!B||!B.items||!B.items.length) return h+'<div class="na">자료 수집 전 — 다음 갱신 후 표시</div></div>';
  const sw=lgSuezShare();
  if(sw&&sw.now!=null) h+=`<div class="lg-share"><div><span>수에즈 쪽 비율(전 세계)</span><b class="num">${sw.now.toFixed(0)}%</b><span class="na">컨테이너선 · ${lgMd(sw.wk)} 주</span></div>
    <div class="lg-shx">전쟁 전 ${sw.pre!=null?sw.pre.toFixed(0)+'%':'―'} · 1년 전 ${sw.ya!=null?sw.ya.toFixed(0)+'%':'―'}<br>유럽↔아시아 배가 희망봉으로 돌면 수에즈보다 약 1~2주 더 걸립니다 — 이 비율이 오르면 운송기간이 줄어드는 신호</div></div>`;
  h+=`<div class="cb-trend lg-tr">${B.items.map((it,k)=>{ const w=lgWk(it), b=it.base||[], W=it.weeks||[];
    return `<div class="cb-tr"><div class="h"><b>${esc(it.name)}</b><span class="num">${lgU(w&&w[2],'척',1)}</span></div>
      <div class="lg-sub">전쟁 전 ${lgU(b[1],'척',1)} ${lgBaseChg(w&&w[2],b[1],LG_GOOD[it.id])} · 전체 ${lgU(w&&w[1],'척')}${staleTag(it.stale_since)}</div>
      ${lgSpark(W.filter(x=>!w||x[0]<=w[0]).map(x=>[x[0],x[2]]),{accent:k===0,min:0,label:it.name+' 컨테이너선 주별'})}<div class="ax"><span>${W.length?lgYmW(W[0][0]):''}</span><span>${w?lgMd(w[0])+' 주':''}</span></div></div>`; }).join('')}</div>`;
  const ms=lgMiss(B); if(ms.length) h+=`<div class="ref"><span class="stl" style="margin-left:0" title="이번 수집 실패 — 이전 값 없음">값 없음</span> ${esc(ms.join(', '))}</div>`;
  return h+why('배 위치 신호(AIS) 기준 하루 통과 척수의 주별 평균 — 신호를 끈 배는 빠져 호르무즈는 실제보다 적게 잡힘 · 약 1주 늦게 매주 갱신 · 전쟁 전 = 1/1~2/27 평균 · 희망봉이 줄면 수에즈로 돌아온 것(파랑) · 그래프 = 2025년부터, 점선 = 전쟁 시작')+`</div>`;   // v33.9 접음
}
function lgPortCard(){   // v33.5 '중동 항만' — 걸프 안 제벨알리(막힌 쪽) ↔ 해협 밖 우회 코르파칸·푸자이라. 부산은 수입의 적출 거점 카드 위
  const B=LOGI&&LOGI.ports, its=((B&&B.items)||[]).filter(it=>it.id!=='Busan'), ms=lgMiss(B).filter(nm=>nm!=='부산');
  let h=`<div class="card"><h3>중동 항만 · 걸프 안 ↔ 우회 <span class="na" style="font-weight:400">IMF PortWatch · 하루 평균 · 주</span>${staleTag(B&&B.stale_since)}</h3>`;
  if(!its.length&&!ms.length) return h+'<div class="na">자료 수집 전 — 다음 갱신 후 표시</div></div>';
  h+=its.map(it=>{ const w=lgWk(it), b=it.base||[];
    const gulf=it.id==='Jebel Ali';   // 걸프 안(호르무즈 안쪽) — 나머지는 해협 밖 우회 항만
    return `<div class="fplain"><span>${esc(gulf?'제벨알리(두바이)':it.name)}${staleTag(it.stale_since)}<br><span class="na">${gulf?'걸프 안':'해협 밖 우회'}${w?' · '+lgMd(w[0])+' 주':''}</span></span><span class="num">컨테이너선 ${lgU(w&&w[2],'척',1)} · 전체 ${lgU(w&&w[1],'척',1)}<br><span class="na">전쟁 전 ${lgU(b[1],'척',1)}</span> ${lgBaseChg(w&&w[2],b[1],LG_GOOD[it.id])}</span></div>`; }).join('');
  h+=ms.map(nm=>`<div class="fplain"><span>${esc(nm)}</span><span class="na"><span class="stl" style="margin-left:0" title="이번 수집 실패 — 이전 값 없음">값 없음</span></span></div>`).join('');
  return h+why('제벨알리(두바이)는 걸프 안쪽 — 호르무즈가 막히자 화물이 해협 밖 코르파칸·푸자이라(아랍에미리트 동해안)로 돌아 트럭으로 들어갑니다(대기 1~2주 보도)')+`</div>`;   // v33.9 접음
}
/* v33.5 적출 거점 → 부산(logistics_fetch v1.1 hubs — 대표가 정한 홍콩·로테르담·두바이·벨기에 → 세계 1~5위 → 지역 대표).
   n = 이름(logistics_fetch HUBS와 같게 — 값 없음 줄 찾기 · '·' 쓰지 않음) · c = 나라·항만 설명 · r = 한국까지 길목(eu 수에즈·홍해 또는 희망봉 · me 호르무즈 ·
   asia·sea·us 전쟁 길목 없음) · k = 관세청 운임 지역 [바닷길, 항공]. 순서 = 화면 순서 */
const LG_HUB={'Hong Kong':{n:'홍콩',c:'홍콩 특별행정구',r:'asia'},'Rotterdam':{n:'로테르담',c:'네덜란드',r:'eu',k:['유럽연합','유럽연합']},
  'Jebel Ali':{n:'두바이',c:'아랍에미리트 · 제벨알리항',r:'me'},'Antwerp':{n:'앤트워프',c:'벨기에',r:'eu',k:['유럽연합','유럽연합']},
  'Shanghai':{n:'상하이',c:'중국 · 양산항 포함',r:'asia',k:['중국','중국']},'Singapore':{n:'싱가포르',c:'동남아 환적 거점',r:'sea'},
  'Ningbo':{n:'닝보',c:'중국',r:'asia',k:['중국','중국']},'Shenzhen':{n:'선전',c:'중국 · 옌톈·서커우',r:'asia',k:['중국','중국']},
  'Qingdao':{n:'칭다오',c:'중국',r:'asia',k:['중국','중국']},'Los Angeles-Long Beach':{n:'LA/롱비치',c:'미국 서부',r:'us',k:['미국서부','미국']},
  'Port Klang':{n:'포트클랑',c:'말레이시아',r:'sea'},'Hamburg':{n:'함부르크',c:'독일',r:'eu',k:['유럽연합','유럽연합']}};
const lgChgI=(r,upGood)=>{ if(r==null||!isFinite(r)) return '<span class="na">―</span>';   // 정수 %(좁은 줄) — 두 배 넘으면 '×2.4'
  if(r>=2) return `<span class="${upGood==null?'':upGood?'pos':'neg'}">×${r.toFixed(1)}</span>`;
  const v=Math.round((r-1)*100); return `<span class="${v===0||upGood==null?'':(v>0)===upGood?'pos':'neg'}">${v>0?'+':v<0?'−':''}${Math.abs(v)}%</span>`; };
const lgHubChg=(v,b)=>(v==null||b==null||b<0.5)?'<span class="na">―</span>':lgChgI(lgRatio(v,b),true);   // 입항이 늘면 파랑(전 값이 거의 0척이면 생략)
function lgYa(it,w){   // 1년 전 같은 주(52주 전 월요일)
  if(!it||!w) return null; const ya=new Date(Date.parse(w[0]+'T00:00:00Z')-364*86400000).toISOString().slice(0,10);
  return (it.weeks||[]).find(x=>x[0]===ya)||null;
}
function lgRoute(r){   // 한국까지 길목 → [줄에 짧게, 펼친 설명]
  if(r==='eu'){ const sw=lgSuezShare(), ok=sw&&sw.now!=null;
    return [ok?`수에즈 쪽 ${sw.now.toFixed(0)}%(전 세계)`:'수에즈·희망봉',
      `수에즈 운하·홍해로 오거나 아프리카 남단 희망봉으로 돌아옵니다 — 전 세계 컨테이너선 수에즈 쪽 비율 ${ok?sw.now.toFixed(0)+'%':'―'}(전쟁 전 ${sw&&sw.pre!=null?sw.pre.toFixed(0)+'%':'―'} · 수에즈 ÷ (수에즈+희망봉) 통과 척수). 유럽→한국 항로만의 값은 아님(실제 노선은 선사·포워더 확인). 희망봉으로 돌면 약 1~2주 더 걸립니다`]; }
  if(r==='me'){ const hz=lgItem('choke','chokepoint6'), w=lgWk(hz), b=(hz&&hz.base)||[];
    return [w&&w[2]!=null?`호르무즈 ${lgN(w[2],1)}척`:'호르무즈',
      `걸프 안쪽 항만이라 호르무즈 해협을 지나야 나옵니다 — 호르무즈 컨테이너선 하루 ${lgU(w&&w[2],'척',1)}(전쟁 전 ${lgU(b[1],'척',1)}). 해협 밖 코르파칸·푸자이라로 돌리는 길은 아래 '중동 항만'`]; }
  if(r==='us'||r==='sea'||r==='asia') return ['',   // v33.9 목록 줄에는 안 씀(8번 반복) — 길목 있는 거점만 표시
    (r==='us'?'태평양을 바로 건너옵니다':r==='sea'?'남중국해를 따라 올라옵니다':'동아시아 가까운 바다')+' — 전쟁으로 막힌 길목을 지나지 않습니다'];
  return [null,null];   // 화면에 없는 거점(수집 목록만 늘어남) — 길목을 말하지 않음
}
function lgHubFreight(m){   // 관세청 한국향 운임(그 지역 · 최근 달) — 홍콩·중동·싱가포르·말레이시아는 파일에 없음. 바닷길·항공 지역이 다를 수 있어(미국 서부 · 미국) 따로 표시
  if(!m.k) return m.r==='me'?'관세청 파일에 중동은 없습니다(보도자료에만) — 부산 → 중동 수출 운임은 아래 수출의 KCCI 중동'
    :m.r==='sea'?'관세청 파일에 싱가포르·말레이시아는 없습니다(동남아는 베트남만)':m.r==='asia'?'관세청 파일에 홍콩은 없습니다':null;
  const f=(key,c,air)=>{ const K=lgKcs(key); if(!K) return null; const i=K.cols.indexOf(c)+1; if(i<1) return null;
    return `${esc(LG_KCS_LBL[c]||c)}발 ${air?'항공':'바닷길'} ${lgU(K.L[i],air?'원/kg':'천원/40ft')}(${lgMon(K.L[0])} · 전쟁 전 ${lgChg(lgRatio(K.L[i],K.W&&K.W[i]),false)})`; };
  const a=[f('kcs_sea_import',m.k[0],false),f('kcs_air_import',m.k[1],true)].filter(Boolean);
  return a.length?a.join(' · '):'관세청 자료 수집 전';
}
function lgHubRow(it){
  const m=LG_HUB[it.id]||{c:'',r:''}, w=lgWk(it), b=it.base||[], y=lgYa(it,w), W=it.weeks||[], rt=lgRoute(m.r), fr=lgHubFreight(m);
  return `<details class="lh"><summary><span class="lh-a"><span class="t">${esc(it.name)}</span><span class="s">${esc([m.c,rt[0]].filter(Boolean).join(' · '))}${staleTag(it.stale_since)}</span></span>
    <span class="lh-b"><b class="num">${lgU(w&&w[2],'척',1)}</b><span class="s">전쟁 전 ${lgHubChg(w&&w[2],b[1])}</span><span class="s">1년 전 ${lgHubChg(w&&w[2],y&&y[2])}</span></span>${ic('down',16,'s2 lh-ic')}</summary>
    <div class="lh-in">${lgSpark(W.filter(x=>!w||x[0]<=w[0]).map(x=>[x[0],x[2]]),{min:0,label:it.name+' 컨테이너선 주별 입항'})}
      <div class="ax"><span>${W.length?lgYmW(W[0][0]):''}</span><span>${w?lgMd(w[0])+' 주':''}</span></div>
      <p>이 항만 입항(모든 행선지) · ${w?lgMd(w[0])+' 주 ':''}하루 평균 — 컨테이너선 ${lgU(w&&w[2],'척',1)} · 모든 배 ${lgU(w&&w[1],'척',1)} · 전쟁 전 컨테이너선 ${lgU(b[1],'척',1)}${y?` · 1년 전 같은 주 ${lgU(y[2],'척',1)}`:''}</p>
      ${rt[1]?`<p><b>한국까지 길목</b> ${esc(rt[1])}</p>`:''}${fr?`<p><b>한국향 운임</b> ${fr}</p>`:''}</div></details>`;
}
function lgHubCard(){
  const B=LOGI&&LOGI.hubs, P=LOGI&&LOGI.ports;
  let h=`<div class="card" id="lgHubs"><h3>적출 거점 → 부산 <span class="na" style="font-weight:400">IMF PortWatch · 그 항만 컨테이너선 하루 입항(한국행만 아님) · 주</span>${staleTag(B&&B.stale_since)}</h3>`;
  const bu=lgItem('ports','Busan'), bw=lgWk(bu), bb=(bu&&bu.base)||[], by=lgYa(bu,bw);   // 도착항 부산
  if(bu) h+=`<div class="lg-share lg-bu"><div><span>부산 입항</span><b class="num">${lgU(bw&&bw[2],'척',1)}</b><span class="na">컨테이너선 하루${bw?' · '+lgMd(bw[0])+' 주':''}</span></div>
    <div class="lh-b"><span class="s">전쟁 전 ${lgU(bb[1],'척',1)} ${lgHubChg(bw&&bw[2],bb[1])}</span><span class="s">1년 전 ${lgU(by&&by[2],'척',1)} ${lgHubChg(bw&&bw[2],by&&by[2])}</span>${staleTag(bu.stale_since||(P&&P.stale_since))}</div>
    <div class="lg-bux">${why('부산항 컨테이너선 입항 전체(수출 선적·환적 배 포함 — 수입 화물만 센 값 아님) · 바닷길 수입 컨테이너가 가장 많이 들어오는 항만 · 항공 화물은 인천공항')}</div></div>`;   // v33.9 접음
  else if(lgMiss(P).includes('부산')) h+=`<div class="ref"><span class="stl" style="margin-left:0" title="이번 수집 실패 — 이전 값 없음">값 없음</span> 부산 입항</div>`;
  if(!B||!B.items||!B.items.length) return h+'<div class="na">적출 거점 자료 수집 전 — 다음 갱신 후 표시</div></div>';
  // 정한 순서대로 — 값이 아예 없는 거점(이번 수집 실패 · 이전 값 없음)도 제자리에 '값 없음' 줄
  const ms=lgMiss(B), hid=Object.fromEntries(B.items.map(it=>[it.id,it])), ids=Object.keys(LG_HUB);
  const missRow=m=>`<div class="lh"><div class="lh-ms"><span class="lh-a"><span class="t">${esc(m.n)}</span><span class="s">${esc(m.c)}</span></span><span class="stl" title="이번 수집 실패 — 이전 값 없음">값 없음</span></div></div>`;
  h+=`<div class="lh-list">${ids.map(id=>hid[id]?lgHubRow(hid[id]):ms.includes(LG_HUB[id].n)?missRow(LG_HUB[id]):'').join('')}${B.items.filter(it=>!LG_HUB[it.id]).map(lgHubRow).join('')}</div>`;
  const msx=ms.filter(nm=>!ids.some(id=>LG_HUB[id].n===nm));
  if(msx.length) h+=`<div class="ref"><span class="stl" style="margin-left:0" title="이번 수집 실패 — 이전 값 없음">값 없음</span> ${esc(msx.join(', '))}</div>`;
  return h+why(`순서 = 대표 지정 홍콩·로테르담·두바이·벨기에 → 세계 물동량 1~5위 상하이·싱가포르·닝보·선전·칭다오 → 지역 대표 LA/롱비치(미국 서부)·포트클랑(말레이시아)·함부르크(독일) · 배 위치 신호(AIS)로 센 입항 척수의 주별 하루 평균(4일 이상 찬 마지막 주) — 항만이 막히거나 배가 빠졌는지 보는 용도(물동량·대기 시간은 아님) · 약 1주 늦게 매주 갱신 · 전쟁 전 = 1/1~2/27 평균(춘절이 끼어 있어 중국·홍콩 항만은 조금 낮게 잡힘) · 연휴·태풍 주간은 1년 전 같은 주와 비교 · 상하이 = 상하이+양산, 선전 = 옌톈+서커우 · 줄을 누르면 추이·길목·관세청 운임(그래프 점선 = 전쟁 시작)`)+`</div>`;   // v33.9 접음
}
/* v33.6 나라별 물동량(logistics_fetch v1.2 — 관세청 국가별 입항·출항 물동량, 공공데이터포털 오픈 API · 월) · 부산항 입항 컨테이너선
   (해양수산부 선박입출항 PORT-MIS · 매일) — 대표 지시 2026-10-17 '적출국별 부산향 · 에어는 인천 · 수입 수출 정보·추이 모두'.
   나라 묶음(groups — VOL_GROUPS)·이상값(odd)·이상값을 뺀 합계(total_clean)는 logistics_fetch가 정해 저장하고 화면은 그대로 씀.
   색: 나라별 물동량은 늘고 줄어도 좋고 나쁨이 아니라 색 없음 · 입항 척수는 늘면 파랑(적출 거점 카드와 같게) · 체류시간은 늘면 주황 */
let LG_VOL={vol_in:'sea',vol_out:'sea'};
const LG_VOL_NM={'아랍에미리트 연합':'아랍에미리트','러시아 연방':'러시아','체코공화국':'체코','남아프리카공화국':'남아공','사우디아라비아':'사우디','네덜란드 열도':'네덜란드령 카리브','룩셈부르그':'룩셈부르크'};
const lgVolNm=c=>LG_VOL_NM[c]||c;
const lgSum=a=>a.reduce((s,v)=>s+(v||0),0);
const lgLast=a=>Array.isArray(a)&&a.length?a[a.length-1]:null;   // 보조 값(바닷길 톤 · 항공 B/L)은 마지막 달만 실음(build_dashboard가 줄임)
const lgYaM=m=>`${+m.slice(0,4)-1}${m.slice(4)}`;   // '2026-09' → '2025-09'
const LG_ODD=`<span class="stl" style="margin-left:4px" title="앞 12달 가운데값의 20배 넘음 — 출처 입력 오류로 보여 합계·그래프·비교에서 뺌(관세청이 고치면 사라짐)">출처 값 확인 필요</span>`;
function lgVolRow(it,M,met,unit,dir,ODD,tL,O2){   // ODD = 이상값 '나라|달' 모음 · tL = 이상값을 뺀 마지막 달 전체(몫의 분모) · O2 = 마지막 달 보조 값(톤·B/L)이 이상값인 나라
  const raw=it[met]||[], mo=M.months, L=mo.length-1, isO=m=>ODD.has(it.c+'|'+m), s=raw.map((v,i)=>isO(mo[i])?null:v), v=raw[L], odd=isO(mo[L]);
  const yi=mo.indexOf(lgYaM(mo[L])), y=yi>=0?s[yi]:null, sh=!odd&&tL&&v!=null?v/tL*100:null, s12=lgSum(s.slice(-12)), nOdd=mo.filter(isO).length;
  const p12=s.length>=24&&!mo.slice(-24).some(isO)?lgSum(s.slice(-24,-12)):null;   // 이상값 달이 끼면 12달 비교는 안 함(달 수가 달라짐)
  const o2=lgLast(met==='teu'?it.ton:it.bl), oth=o2==null?'':(met==='teu'?` · ${lgN(o2)}톤`:` · B/L ${lgN(o2)}건`)+(O2.has(it.c)?LG_ODD:'');
  return `<details class="lh"><summary><span class="lh-a"><span class="t">${esc(lgVolNm(it.c))}</span><span class="s">${sh!=null&&sh>=1?`${esc(dir)} 전체의 ${Math.round(sh)}%`:''}</span></span>
    <span class="lh-b"><b class="num">${lgN(v)}<small>${unit}</small></b><span class="s">${odd?LG_ODD:`전년 같은 달 ${lgChgI(lgRatio(v,y),null)}`}</span></span>${ic('down',16,'s2 lh-ic')}</summary>
    <div class="lh-in">${lgSpark(mo.map((m,i)=>[m,s[i]]),{min:0,label:lgVolNm(it.c)+' 최근 '+mo.length+'달'})}
      <div class="ax"><span>${lgMon(mo[0])}</span><span>${lgMon(mo[L])}</span></div>
      <p>${lgMon(mo[L])} ${lgN(v)}${unit}${oth} · 전년 같은 달 ${lgU(y,unit)} · 최근 12달 ${lgN(s12)}${unit}${p12?`(그 전 12달 대비 ${lgChgI(lgRatio(s12,p12),null)})`:''}${nOdd?` · 이상값 ${nOdd}달은 그래프·합계에서 뺌`:''}</p></div></details>`;
}
function lgVolCard(key){   // key = 'vol_in'(수입 묶음 · 나라 → 부산항·인천공항) · 'vol_out'(수출 묶음 · 부산항·인천공항 → 나라) — 칩: 바닷길(부산항 TEU) · 항공(인천공항 톤)
  const out=key==='vol_out', mode=LG_VOL[key]||'sea', B=LOGI&&LOGI[key], M=B&&B[mode], air=mode==='air';
  const met=air?'ton':'teu', unit=air?'톤':'TEU', pt=air?'인천공항':'부산항', dir=`${pt} ${out?'출발':'도착'}`;
  let h=`<h3>${out?`나라별 ← ${pt} 출발 물동량`:`나라별 → ${pt} 도착 물동량`} <span class="na" style="font-weight:400">관세청 · ${out?'출항':'입항'} 적재화물목록 · 월</span>${staleTag(B&&B.stale_since)}</h3>
    <div class="chips" style="margin-bottom:8px">${[['sea','바닷길 · 부산항'],['air','항공 · 인천공항']].map(([c,l])=>`<button type="button" class="chip${mode===c?' on':''}" aria-pressed="${mode===c}" onclick="LG_VOL['${key}']='${c}';document.getElementById('lgVol_${key}').innerHTML=lgVolCard('${key}')">${l}</button>`).join('')}</div>`;
  if(!M||!M.months||M.months.length<2||!M.items||!M.total) return h+'<div class="na">자료 수집 전 — 다음 갱신 후 표시</div>';
  const mo=M.months, L=mo.length-1, I=M.items, yi=mo.indexOf(lgYaM(mo[L]));
  const ODD=new Set((M.odd||[]).filter(o=>Array.isArray(o)&&o[2]===met).map(o=>o[0]+'|'+o[1]));   // logistics_fetch vol_odd — 출처 입력 오류로 보이는 나라·달
  const tc=(M.total_clean&&M.total_clean[met])||M.total[met]||[], tL=tc[L], oL=I.filter(x=>ODD.has(x.c+'|'+mo[L])).map(x=>lgVolNm(x.c));
  const oN=[...ODD].filter(k=>k.endsWith('|'+mo[L])).length-oL.length;   // 목록 밖 나라의 이상값(전체에서만 뺌)
  // 전년 같은 달 대비 — 두 달 중 한 달이라도 이상값인 나라는 두 달 모두에서 뺀 합(logistics_fetch yoy · 같은 나라끼리). 이번 달 이상값은 아래 'OO 값 뺌' 줄이
  // 설명하고, 전년 달에만 이상값인 나라는 'OO 빼고 비교' 줄로(전체 숫자에는 들어 있음)
  const curO=[...ODD].filter(k=>k.endsWith('|'+mo[L])).map(k=>k.slice(0,k.lastIndexOf('|')));
  const Y=M.yoy&&Array.isArray(M.yoy[met])?M.yoy[met]:null, yOnly=Y&&Array.isArray(Y[2])?Y[2].filter(c=>!curO.includes(c)).map(lgVolNm):[];
  const yTxt=Y?lgChgI(lgRatio(Y[0],Y[1]),null):'<span class="na">―</span>', nm2=a=>a.length>2?`${a.slice(0,2).join('·')} 등 ${a.length}곳`:a.join('·');
  const m2=met==='teu'?'ton':'bl', O2=new Set((M.odd||[]).filter(o=>Array.isArray(o)&&o[2]===m2&&o[1]===mo[L]).map(o=>o[0]));   // 보조 값(바닷길 톤 · 항공 B/L) 이상값
  h+=`<div class="lg-share"><div><span>${esc(dir)} 전체 · ${lgMon(mo[L])}</span><b class="num">${lgN(tL)}<small>${unit}</small></b><span class="na">전년 같은 달 ${yTxt}</span>${yOnly.length?`<span class="na">${esc(nm2(yOnly))} 빼고 비교</span>`:''}${oL.length||oN>0?`<span class="na">${esc([...oL,oN>0?`그 밖 ${oN}곳`:''].filter(Boolean).join('·'))} 값 뺌${LG_ODD}</span>`:''}</div>
    <div class="lg-shx">${air?'항공 화물 무게(톤)':'컨테이너 물량(TEU · 빈 컨테이너 제외)'} · ${air?'인천공항':'신항+북항+감천항'}<br><span class="na">나라를 누르면 최근 ${mo.length}달 추이</span></div></div>`;
  const row=it=>lgVolRow(it,M,met,unit,dir,ODD,tL,O2), by=Object.fromEntries(I.map(x=>[x.c,x]));
  const G=(Array.isArray(M.groups)&&M.groups.length?M.groups:[['거점',I.map(x=>x.c)]]).map(([g,cs])=>[g,(Array.isArray(cs)?cs:[]).map(c=>by[c]).filter(Boolean)]);
  const inG=new Set(G.flatMap(g=>g[1].map(x=>x.c))), z=it=>!lgSum((it[met]||[]).slice(-12));   // 최근 12달 기록 없는 지정 나라(예: 항공 출발 벨기에 — 이웃 허브 나라로 잡힘)는 목록 밖 한 줄
  const zs=G.flatMap(g=>g[1].filter(z)), g1=G[0][1].filter(x=>!z(x)), gs=G.slice(1).map(([g,xs])=>[g,xs.filter(x=>!z(x))]).filter(g=>g[1].length), g3=I.filter(x=>!inG.has(x.c));
  const GL={'원산지·생산국':out?'브랜드 원산지·생산국으로 가는 화물':'브랜드 원산지·생산국'};
  h+=`<div class="lh-list">${g1.map(row).join('')}</div>`;
  if(gs.length||g3.length) h+=`<details class="lg-more"><summary><span>나라 더 보기</span><span class="na">${[...gs.map(([g,xs])=>`${g} ${xs.length}곳`),g3.length?`그 밖에 많은 나라 ${g3.length}곳`:''].filter(Boolean).join(' · ')}</span>${ic('down',16,'s2 lh-ic')}</summary>
    ${gs.map(([g,xs])=>`<div class="lg-grp">${esc(GL[g]||g)}</div><div class="lh-list">${xs.map(row).join('')}</div>`).join('')}${g3.length?`<div class="lg-grp">그 밖에 ${esc(dir)} 많은 나라(최근 12달)</div><div class="lh-list">${g3.map(row).join('')}</div>`:''}</details>`;
  if(zs.length) h+=`<div class="ref">최근 12달 기록 없음: ${esc(zs.map(x=>lgVolNm(x.c)).join(', '))}</div>`;
  const blTop=air?I.filter(x=>lgLast(x.bl)!=null&&!O2.has(x.c)).sort((a,b)=>lgLast(b.bl)-lgLast(a.bl)).slice(0,2).map(x=>lgVolNm(x.c)):[];
  const cov=air?'항공은 인천공항만(김해공항 등은 빠짐)':`바닷길은 부산항만(신항+북항+감천항 · 북항 = 관세청 항구 이름 '부산항') — 인천·평택·광양항 등은 빠짐${out?'':'(중국·베트남 화물은 인천항으로도 많이 들어옴)'}`;
  const unitNote=air?`항공 B/L 건수엔 ${out?'전자상거래 수출(역직구)':'해외직구'} 특송 소포가 섞임${blTop.length?`(${lgMon(mo[L])} 건수 많은 곳: ${esc(blTop.join('·'))})`:''}`:'TEU = 20ft 컨테이너 1개 기준(40ft = 2)';
  return h+(M.others?`<div class="na">목록 밖 ${M.others}개 나라는 전체에만</div>`:'')+why(`관세청 ${out?'출항':'입항'} 적재화물목록 기준 ${out?'목적지(화물목록상 내리는 항구·공항 — 허브 나라로 잡힐 수 있음: 항공 룩셈부르크·카타르, 바닷길 슬로베니아(코페르항 → 중부 유럽) 등)':'선적지(B/L상 실은 곳)'} 나라별 — ${out?'수출':'수입'} 화물만(환적 제외) · ${cov} · 매월 15일께 전달 자료(지난 달도 정정·취하로 조금씩 바뀜) · ${unitNote} · 물량이 늘고 주는 건 좋고 나쁨이 아니라 색 없음 · '출처 값 확인 필요' = 앞 12달 가운데값의 20배 넘는 값(입력 오류로 보여 전체·그래프·비교에서 뺌 — 관세청이 고치면 사라짐) · 점선 = 전쟁 시작`);   // v33.9 접음 · '목록 밖 n개 나라'는 위에 따로(접지 않음)
}
/* 부산항 입항 컨테이너선 — 직전 출항지 나라(부산 오기 바로 전 항구) 묶음 */
const LG_PM_GRP=[['중국',['CN']],['일본',['JP']],['대만·홍콩',['TW','HK','MO']],['동남아',['VN','TH','MY','SG','ID','PH','KH','MM','BN','TL']],
  ['러시아',['RU']],['북미',['US','CA','MX']],['국내 항만',['KR']]];
const lgDay=(iso,k)=>new Date(Date.parse(iso+'T00:00:00Z')+k*86400000).toISOString().slice(0,10);
function lgPmCard(){
  const B=LOGI&&LOGI.busan_calls, D=((B&&B.days)||[]).filter(r=>Array.isArray(r)&&r.length>=5&&typeof r[0]==='string');
  const last=D.length?D[D.length-1][0]:null, stop=!!(B&&/^\d{4}-\d{2}-\d{2}$/.test(B.fetched||'')&&!B.stale_since&&last&&last<lgDay(B.fetched,-3));   // 수집은 됐는데 날이 안 늘어남(logistics_fetch가 막지만 화면에서도)
  let h=`<div class="card" id="lgPm"><h3>부산항 입항 컨테이너선 <span class="na" style="font-weight:400">해양수산부 입항 신고 · ${stop||(B&&B.stale_since)?'':'어제까지 · '}매일</span>${stop?`<span class="stl" title="수집은 됐지만 새 날이 없음 — 응답 형식 확인">자료 멈춤(${lgMd(last)}까지)</span>`:staleTag(B&&B.stale_since)}</h3>`;
  if(D.length<5) return h+'<div class="na">자료 수집 전 — 다음 갱신 후 표시</div></div>';
  const by=Object.fromEntries(D.map(r=>[r[0],r]));
  const win=(end,n)=>{ const a=[]; for(let i=0;i<n;i++){ const r=by[lgDay(end,-i)]; if(r) a.push(r); } return a; };   // end부터 n일 거슬러(빈 날 빼고)
  const avg=a=>a.length?lgSum(a.map(r=>r[1]))/a.length:null, stay=a=>{ const n=lgSum(a.map(r=>r[4])); return n?lgSum(a.map(r=>r[3]))/n:null; };
  const w0=win(last,7), w4=win(lgDay(last,-7),28), wy=win(lgDay(last,-364),7);
  const a0=avg(w0), a4=w4.length>=14?avg(w4):null, ay=wy.length>=5?avg(wy):null;
  const sEnd=lgDay(last,-4), s0=stay(win(sEnd,7)), s4w=win(lgDay(sEnd,-7),28), s4=s4w.length>=14?stay(s4w):null;   // 체류는 출항 신고가 다 들어온 4일 전까지
  h+=`<div class="lg-share"><div><span>최근 7일 · ${lgMd(lgDay(last,-6))}~${lgMd(last)}</span><b class="num">${lgN(a0)}<small>척/일</small></b><span class="na">컨테이너선 하루 평균</span></div>
    <div class="lg-shx">지난 4주 ${lgU(a4,'척')} ${a4!=null?lgChgI(lgRatio(a0,a4),true):''} · 1년 전 같은 7일 ${ay!=null?lgU(ay,'척')+' '+lgChgI(lgRatio(a0,ay),true):'<span class="na">모으는 중</span>'}<br>
    체류(입항→출항) 평균 ${lgU(s0,'시간')}${s4!=null?` · 지난 4주 ${lgU(s4,'시간')} ${lgChgI(lgRatio(s0,s4),false)}`:''} <span class="na">(${lgMd(lgDay(sEnd,-6))}~${lgMd(sEnd)} 입항)</span></div></div>`;
  const cc={}; w0.forEach(r=>Object.entries(r[2]||{}).forEach(([c,k])=>{ cc[c]=(cc[c]||0)+(+k||0); }));
  const known=new Set(LG_PM_GRP.flatMap(g=>g[1])), grp=LG_PM_GRP.map(([nm,cs])=>[nm,lgSum(cs.map(c=>cc[c]))]);
  grp.push(['그 밖',lgSum(Object.entries(cc).filter(([c])=>!known.has(c)).map(([,k])=>k))]);   // 유럽·중동·인도·남미 등
  const mx=Math.max(1,...grp.map(g=>g[1]));
  h+=`<div class="lg-grp">직전 출항지 나라 · 최근 7일 합(${lgN(lgSum(grp.map(g=>g[1])))}척)</div><div class="lg-hb">${grp.filter(g=>g[1]>0).map(([nm,k])=>
    `<div><span class="t">${esc(nm)}</span><span class="bw"><span class="b" style="width:${(k/mx*100).toFixed(1)}%"></span></span><span class="num">${lgN(k)}척</span></div>`).join('')}</div>`;
  const wk={}; D.forEach(r=>{ const m=lgDay(r[0],-((new Date(Date.parse(r[0]+'T00:00:00Z')).getUTCDay()+6)%7)); (wk[m]=wk[m]||[]).push(r[1]); });
  let m0=Object.keys(wk).sort().pop(); if(m0&&wk[m0].length<5) m0=lgDay(m0,-7);   // 이번 주가 덜 찼으면 한 주 앞부터
  const W=[]; for(let m=m0;m&&wk[m]&&wk[m].length>=5;m=lgDay(m,-7)) W.unshift([m,lgSum(wk[m])/wk[m].length]);   // 월요일 시작 주(5일 이상 찬 주) — 가장 최근 주부터 빈틈없이 이어진 데까지(지난 자료를 채우는 중엔 1년 전 비교용 날이 떨어져 있음)
  if(W.length>=2) h+=`<div class="lg-pmtr">${lgSpark(W,{min:0,accent:true,label:'부산 컨테이너선 주별 하루 평균'})}<div class="ax"><span>${lgYmW(W[0][0])}</span><span>${lgMd(W[W.length-1][0])} 주</span></div></div>`;
  const warIn=W.length>=2&&W[0][0]<LG_WAR&&W[W.length-1][0]>=LG_WAR;   // lgSpark가 전쟁 시작 점선을 그릴 때만 설명
  return h+(B&&B.missing?`<div class="na">지난 자료 채우는 중(빈 날 ${lgN(B.missing)}일)</div>`:'')+why(`해양수산부 PORT-MIS 입항 신고(공공데이터포털) — 부산항 전체(북항·신항·감천 등)에 들어온 컨테이너선 · 수출 선적·환적 배 포함(수입 화물만 센 값 아님) · 위 적출 거점 카드의 '부산 입항'(IMF PortWatch · 배 위치 신호 · 주 단위)과 세는 방식이 달라 값이 다름 — 두 값은 서로 견주지 말고 각 카드의 추이로 봄 · 직전 출항지 = 부산에 오기 바로 전 항구의 나라(유럽·미주 배도 중국·일본을 들르면 그 나라로 잡힘 · 그 밖 = 유럽·중동·인도·남미 등) · 체류 = 입항→출항 시각(${lgN((B&&B.stay_cap)||96)}시간 넘으면 그 값) · 매일 최근 7일을 다시 받음 · 그래프 = 주별 하루 평균${warIn?', 점선 = 전쟁 시작':''}`)+`</div>`;   // v33.9 접음 · '지난 자료 채우는 중'은 위에 따로(접지 않음)
}
/* 전 세계 정시율 — Sea-Intelligence GLP(월) */
function lgGlp(){ const B=LOGI&&LOGI.glp; if(!B||!B.months||!B.months.length) return null;
  const M=B.months, by=Object.fromEntries(M.map(m=>[m[0],m])); return {B,M,L:M[M.length-1],W:by[LG_PRE_M]||null}; }
function lgGlpCard(){
  const G=lgGlp();
  let h=`<div class="card"><h3>전 세계 정시율 <span class="na" style="font-weight:400">Sea-Intelligence · 월</span>${staleTag(G&&G.B.stale_since)}</h3>`;
  if(!G) return h+'<div class="na">자료 수집 전 — 다음 갱신 후 표시</div></div>';
  const M=G.M.slice(-13);
  h+=`<div class="lg-share"><div><span>${lgMon(G.L[0])} 정시 도착</span><b class="num">${lgN(G.L[1],1)}%</b><span class="na">늦은 배 평균 ${G.L[2]!=null?lgN(G.L[2],2)+'일':'―'} 지연</span></div>
    <div class="lg-shx">전쟁 전(${lgMon(LG_PRE_M)}) <span class="nw">${G.W?lgN(G.W[1],1)+'%':'―'}</span> · <span class="nw">늦은 배 ${G.W&&G.W[2]!=null?lgN(G.W[2],2)+'일':'―'}</span><br>정시율이 내리고 지연이 늘면 도착일이 들쭉날쭉해집니다 — 재고·판매 일정에 여유를 둡니다</div></div>`;
  const fl=Math.max(0,Math.min(30,Math.floor(Math.min(...M.map(m=>m[1]))/10)*10-10));   // 막대 바닥 = 가장 낮은 값보다 조금 아래(차이가 보이게) — 숫자는 막대 위에
  h+=`<div class="lg-bars" role="img" aria-label="최근 ${M.length}달 정시율 ${M.map(m=>`${m[0].slice(0,4)}년 ${+m[0].slice(5,7)}월 ${m[1]}%`).join(', ')}">${M.map(m=>`<div><span class="v num">${Math.round(m[1])}</span><span class="bw"><span class="b${m[0]===G.L[0]?' on':''}" style="height:${Math.max(4,Math.min(100,(m[1]-fl)/(100-fl)*100)).toFixed(1)}%"></span></span><span class="m">${+m[0].slice(5,7)}</span></div>`).join('')}</div>`;
  return h+why(`막대 아래 = 달(${lgMon(M[0][0])}~${lgMon(G.L[0])}) · 전 세계 컨테이너선이 일정대로(하루 안) 도착한 비율 · 매월 말 전달 자료를 보도자료에서 읽음 · 항로별 값은 유료 보고서라 없음`)+`</div>`;   // v33.9 접음
}
function lgNewsCard(){
  const L=((NEWS&&NEWS.items)||[]).filter(it=>it.scope==='industry'&&it.key==='logistics').sort((a,b)=>(b.first_seen||'').localeCompare(a.first_seen||'')||(b.importance||0)-(a.importance||0));
  const list=newsDedupe(L,5);
  let h=`<div class="card"><h3>물류·운임 뉴스 <button type="button" class="go" onclick="goNews('i:logistics')">뉴스 ›</button></h3>`;
  if(!list.length) return h+'<div class="na">보관 기간 내 선별 뉴스 없음 — 매일 03:17 수집</div></div>';
  list.forEach(it=>{ h+=`<div class="nitem"><div class="nsum"><span class="stars">${'★'.repeat(Math.max(1,Math.min(3,it.importance||1)))}</span> <a href="${esc(safeUrl(it.link))}" target="_blank" rel="noopener">${esc(it.summary||it.title)}</a></div>
    <div class="nmeta">${[it.source,newsDay(it)].filter(Boolean).map(esc).join(' · ')}</div></div>`; });
  return h+`</div>`;
}
function lgKpis(){   // 맨 위 6칸(v33.5 순서) — 수입 유럽→한국(바닷길·인천 항공) · 길목(호르무즈·수에즈 쪽 비율) · 정시율 · 수출 부산→중동
  const S=lgKcs('kcs_sea_import'), A=lgKcs('kcs_air_import'), K=lgKcci(), G=lgGlp(), hz=lgItem('choke','chokepoint6'), sw=lgSuezShare();
  const kv=(K2,c)=>{ if(!K2) return null; const i=K2.cols.indexOf(c)+1; return i<1?null:{v:K2.L[i],w:K2.W?K2.W[i]:null,m:K2.L[0]}; };
  const se=kv(S,'유럽연합'), ae=kv(A,'유럽연합'), me=K?(()=>{ const i=K.cols.indexOf('KMEI')+1; return i<1?null:{v:K.L[i],w:K.W&&K.W[i],d:K.L[0]}; })():null;
  const hw=lgWk(hz), kp=(l,v,s)=>`<div class="kpi"><div class="l">${l}</div><div class="v num">${v}</div><div class="s">${s}</div></div>`;
  return `<div class="kpis lgk">
    ${kp('유럽→한국 바닷길',lgU(se&&se.v,'<small>천원</small>'),se?`40ft · ${lgMon(se.m)} · 전쟁 전 ${lgChg(lgRatio(se.v,se.w),false)}`:'수집 전')}
    ${kp('유럽→인천 항공',lgU(ae&&ae.v,'<small>원</small>'),ae?`kg당 · ${lgMon(ae.m)} · 전쟁 전 ${lgChg(lgRatio(ae.v,ae.w),false)}`:'수집 전')}
    ${kp('호르무즈 컨테이너선',lgU(hw&&hw[2],'<small>척</small>',1),hw?`하루 · 전쟁 전 ${lgU(hz.base&&hz.base[1],'척',1)}`:'수집 전')}
    ${kp('수에즈 쪽 비율',sw&&sw.now!=null?sw.now.toFixed(0)+'%':'―',sw&&sw.pre!=null?`전 세계 컨테이너선 · 전쟁 전 ${sw.pre.toFixed(0)}%`:'수집 전')}
    ${kp('전 세계 정시율',G?lgN(G.L[1],1)+'%':'―',G?`${lgMon(G.L[0])} · 전쟁 전 ${G.W?lgN(G.W[1],1)+'%':'―'}`:'수집 전')}
    ${kp('부산→중동 수출',lgU(me&&me.v,'',0,'$'),me?`40ft · ${lgMd(me.d)} · 전쟁 전 ${lgChg(lgRatio(me.v,me.w),false)}`:'수집 전')}
  </div>`;
}
function lgJump(id){   // v33.5 맨 위 칩 → 그 묶음 제목으로(고정 머리 밑에 숨지 않게 scroll-padding 먼저)
  const e=document.getElementById(id); if(!e) return;
  cancelAnimationFrame(SCROLL_RAF); SCROLL_RAF=0; phSync(); e.scrollIntoView({behavior:smoothB(),block:'start'});
}
function moreLogiHtml(){
  let h=moreHead('물류','갱신 <span class="nw">'+esc((LOGI&&LOGI.generated_at)||'―')+'</span>');   // v33.9 머리 줄은 갱신 시각만
  if(!LOGI) return h+'<div class="card"><div class="na">물류 자료 수집 전 — update-dashboard 실행 후 표시</div></div>';
  const sf=(nm,fn)=>{ try{ return fn(); }catch(e){ console.error('[물류 · '+nm+'] 그리기 실패:',e); return `<div class="card"><div class="na">${esc(nm)} — 그리기 실패</div></div>`; } };
  const sec=(id,t,sub)=>`<h2 class="lg-h2" id="${id}">${t}<span>${sub}</span></h2>`;
  h+=sf('요약',lgKpis);
  h+=`<div class="chips lg-jump">${[['lgImp','수입'],['lgExp','수출'],['lgRisk','공통 위험 신호']].map(([id,t])=>`<button type="button" class="chip" onclick="lgJump('${id}')">${t}${ic('down',16)}</button>`).join('')}</div>`;
  h+=why(`① 수입: 적출 거점 입항이 줄면 그 항만이 막혔거나 배(노선)가 빠졌다는 신호일 수 있습니다 — 연휴(춘절·국경절·추석)·태풍 주간에도 줄어드니 1년 전 같은 주와 함께 봅니다. 운송기간은 한국까지 지나는 길목(유럽 = 수에즈·희망봉, 두바이 = 호르무즈)이 정합니다. 그 나라에서 부산항(바닷길)·인천공항(항공)으로 들어온 물량은 나라별 도착 물동량(관세청 · 월 — 인천·평택·광양항 등은 빠짐), 어제까지 부산항에 들어온 배는 부산항 입항 컨테이너선(해수부 · 매일 — 수출 선적·환적 배 포함). 원가는 한국향 운임(관세청 수입신고 운임 — 바닷길은 부산 등 전국 항만, 항공은 인천공항 도착). ② 수출: 부산발 운임(KCCI)·한국발 운임(관세청 수출신고)·나라별 출발 물동량(부산항·인천공항). ③ 공통 위험 신호: 해협 통과·중동 항만·정시율이 나빠지면 도착일이 늦어지고 들쭉날쭉해집니다.`,'이 화면 읽는 법');   // v33.9 접음
  h+=sec('lgImp','수입','적출 거점 → 부산 · 항공 → 인천')+sf('적출 거점',lgHubCard)+sf('나라별 도착 물동량',()=>`<div class="card" id="lgVol_vol_in">${lgVolCard('vol_in')}</div>`)
    +sf('부산항 입항 선박',lgPmCard)+sf('한국향 운임',()=>`<div class="card" id="lgKcs">${lgKcsCard()}</div>`);
  h+=sec('lgExp','수출','부산 → 해외 · 항공 인천 → 해외')+sf('부산발 운임',lgKcciCard)+sf('한국발 운임',()=>`<div class="card">${lgKcsCard('kcs_sea_export')}</div>`)
    +sf('나라별 출발 물동량',()=>`<div class="card" id="lgVol_vol_out">${lgVolCard('vol_out')}</div>`);
  h+=sec('lgRisk','공통 위험 신호','바닷길 · 정시율 · 뉴스')+sf('해협 통과',lgChokeCard)+sf('중동 항만',lgPortCard)+sf('정시율',lgGlpCard)+sf('물류 뉴스',lgNewsCard);
  const st=LOGI.status||{}, bad=(st.kept||[]).concat(st.failed||[]);
  // v33.10 공공데이터포털 연결 차단(logistics_fetch v1.3) — 실패 줄 끝에 사유(수집 상태 _conn_note와 같은 규칙)
  const dc=(LOGI.dgk_conn&&typeof LOGI.dgk_conn==='object'&&!Array.isArray(LOGI.dgk_conn))?LOGI.dgk_conn:{};
  const dtr=Array.isArray(dc.tries)?dc.tries.filter(t=>t&&typeof t==='object'&&!Array.isArray(t)):[], dn=dtr.length, dall=dn>0&&dtr.every(t=>t.blocked);
  const dIn=[dall?(dn>1?'GitHub 서버 '+dn+'대 모두 막힘':'GitHub 서버에서 막힘'):(dn?'GitHub 서버 '+dn+'대에서 시도':''),typeof dc.since==='string'&&dc.since?esc(dc.since)+'부터':''].filter(Boolean).join(' · ');
  const dcTxt=(Array.isArray(dc.keys)&&dc.keys.length)?` — 공공데이터포털 연결 ${dall?'안 됨':'오류'}${dIn?'('+dIn+')':''}`:'';
  if(bad.length) h+=`<div class="note"><span class="stl" style="margin-left:0">이번 수집 일부 실패</span> ${esc(bad.join(', '))}${dcTxt}</div>`;   // v33.9 실패 표시는 접지 않음
  h+=`<div class="note">출처: 관세청 · 해양수산부 · 한국해양진흥공사 KCCI · IMF PortWatch · Sea-Intelligence</div>`;   // v33.9 출처 한 줄은 보이게
  h+=why('관세청 수출입 운송비용(공공데이터포털 · 공공누리 1유형) · 관세청 국가별 입항·출항 물동량 · 해양수산부 선박입출항(공공데이터포털 오픈 API · 이용허락 제한 없음) · 한국해양진흥공사 KCCI · IMF PortWatch(UN Global Platform AIS) · Sea-Intelligence GLP 보도자료 · 매일 update-dashboard에서 받음','출처 자세히');
  return h;
}
/* ── 검색 관심도 vs 실적(v32.8) — 국내 패션·아이웨어: 같은 해 네이버 검색 증감 vs 매출 증감, 올해 검색 추이 ── */
const SV_LINK_EXTRA={'krd:luxottica_kr':'EL.PA'};   // 룩소티카코리아 = 에실로룩소티카 브랜드(레이밴·오클리·프라다) 합
function svData(){
  const BM=NAVER&&NAVER.brand_monthly; if(!BM||!BM.series||!BM.months||!BM.months.length) return null;
  const ents=(KRD&&KRD.entities)||[], mo=BM.months, last=mo[mo.length-1], cy=+last.slice(0,4), cm=+last.slice(5,7);
  const ysum=(v,y,upto=12)=>{let t=0,n=0; mo.forEach((p,i)=>{ if(+p.slice(0,4)===y&&+p.slice(5,7)<=upto){ t+=v[i]; n++; } }); return n===upto?t:null;};
  const pct=(a,b)=>a!=null&&b?(a/b-1)*100:null;
  const rows=[];
  FB_KEYS.concat(EY_KEYS).forEach(k=>{
    const e=ents.find(x=>'krd:'+x.id===k); if(!e) return;
    const lk=SV_LINK_EXTRA[k]||k, bs=nvAll().filter(b=>b.link===lk&&BM.series[b.name]);
    if(!bs.length) return;
    const v=mo.map((_,i)=>bs.reduce((t,b)=>t+(BM.series[b.name][i]||0),0));
    const ys=(e.years||[]).filter(y=>y.rev!=null&&y.end).sort((a,b)=>a.end<b.end?-1:1), l=ys[ys.length-1], p=ys[ys.length-2];
    const fy=l?+l.end.slice(0,4):null;   // 국내 패션·아이웨어는 모두 12월 결산 → 결산 연도 = 검색 비교 연도
    let w4=null; const ws=bs.map(b=>b.s).filter(Boolean);
    if(ws.length&&ws[0].length>=56){ const n=ws[0].length, sw=i=>ws.reduce((t,s)=>t+(s[i]||0),0); let a=0,b=0; for(let i=n-4;i<n;i++){ a+=sw(i); b+=sw(i-52); } w4=pct(a,b); }
    rows.push({key:k,name:e.name,brands:bs.map(b=>b.name),fy,
      rev:l&&p&&p.rev>0?(l.rev/p.rev-1)*100:null, srch:fy?pct(ysum(v,fy),ysum(v,fy-1)):null,
      ytd:pct(ysum(v,cy,cm),ysum(v,cy-1,cm)), w4});
  });
  return {rows,cy,cm};
}
function svCardHtml(){
  const d=svData(); if(!d||!d.rows.length) return '';
  const {rows,cy,cm}=d, both=rows.filter(r=>r.rev!=null&&r.srch!=null), same=both.filter(r=>(r.rev>=0)===(r.srch>=0));
  const fys=[...new Set(both.map(r=>r.fy))].sort(), fyT=fys.length?fys.map(f=>'FY'+String(f).slice(2)).join('·'):'―';
  const cell=(v,w)=>v==null?'<span class="na">―</span>':`${fmt(v,1,true)}${w&&v<=-15?'<br><span class="mbadge late" style="white-space:nowrap">관심 둔화</span>':w&&v>=15?'<br><span class="pg-badge" style="white-space:nowrap">관심 증가</span>':''}`;
  const order=rows.slice().sort((a,b)=>(b.ytd??-1e9)-(a.ytd??-1e9));
  const down=order.filter(r=>r.ytd!=null&&r.ytd<=-15).map(r=>r.name.replace(/\(.*\)/,'')), up=order.filter(r=>r.ytd!=null&&r.ytd>=15).map(r=>r.name.replace(/\(.*\)/,''));
  let h=`<div class="ndate" style="margin-top:16px">검색 관심도 vs 실적 <span class="na" style="font-weight:400">${rows.length}곳 · 네이버 월간 검색 · DART 연간 매출</span></div><div class="card" id="svCard">`;
  h+=`<div class="nv-sum">${both.length?`<b>${fyT} 매출과 같은 해 검색이 같은 방향</b> ${same.length}/${both.length}곳 — 많을수록 검색 흐름이 그 회사 매출을 잘 따라간다는 뜻이라, 올해 검색 변화를 다음 실적의 미리보기로 쓸 수 있습니다.`:'매출·검색을 함께 비교할 수 있는 회사가 아직 없습니다.'}
    ${down.length?`<br><b style="color:var(--down)">▼ 올해 검색 15% 넘게 감소</b> ${down.map(esc).join(' · ')}`:''}${up.length?`<br><b style="color:var(--up)">▲ 15% 넘게 증가</b> ${up.map(esc).join(' · ')}`:''}</div>`;
  h+=`<div class="tblwrap"><table class="nowrap sv-tbl"><tr><th>기업</th><th>매출<br><span class="na">결산 연도</span></th><th>검색<br><span class="na">같은 해</span></th><th>검색<br><span class="na">${cy} 1~${cm}월</span></th><th>검색<br><span class="na">최근 4주</span></th></tr>`;
  order.forEach(r=>{
    const bn=r.brands.length>2?r.brands.slice(0,2).join('·')+` 외 ${r.brands.length-2}`:r.brands.join('·');
    h+=`<tr tabindex="0" style="cursor:pointer" onclick="goDetail('${r.key}')"><td>${esc(r.name.replace(/\(.*\)/,''))}<span class="pg-rk">${esc(bn)}${r.fy?' · FY'+String(r.fy).slice(2):''}</span></td><td>${cell(r.rev)}</td><td>${cell(r.srch)}</td><td>${cell(r.ytd,1)}</td><td>${cell(r.w4)}</td></tr>`;
  });
  h+=`</table></div><div class="note" style="margin-top:6px">검색 = 네이버 검색량(브랜드 검색어 합 · 수입 법인은 취급 브랜드 합: 룩소티카코리아 = 레이밴·오클리·프라다, 케어링아이웨어코리아 = 구찌·생로랑·까르띠에·린드버그, 시원아이웨어 = 디올). 매출 = DART 별도 재무제표 전년 대비. 같은 해 검색 = 결산 연도 1~12월 합 vs 전년. 올해 = 1월부터 지난달까지 vs 전년 같은 기간. 검색은 온라인 관심의 흐름일 뿐 매출과 1:1이 아니고, 아이아이컴바인드 매출에는 탬버린즈·누데이크가 들어 있습니다. 하고하우스·시선인터내셔널·다비치는 브랜드 검색어가 없어 제외. 행을 누르면 기업 상세</div></div>`;
  return h;
}
function moreMenuHtml(){   // v33 S2: 머리 '더보기' + 메뉴 줄 5개(선 아이콘) + '화면 테마'(id="themeBtn") · 오른쪽 = 지금 상태
  // 오른쪽 값은 줄마다 따로 — 하나가 깨져도 그 칸만 '―'
  const sv=(nm,fn,dflt)=>{ try{ return fn(); }catch(e){ console.error('[더보기 · '+nm+' 줄] 계산 실패:',e); return dflt==null?'―':dflt; } };
  const row=(v,icn,t,d,r)=>`<button type="button" class="mi" data-go="more:${v}"><span class="mic">${ic(icn,22)}</span><span class="mtt"><span class="mt">${t}</span><span class="md">${d}</span></span><span class="mr">${r}</span></button>`;
  return `<div class="phead"><h1>더보기</h1></div><nav class="mmenu" aria-label="더보기 화면">
    ${row('peer','store','유통사 비교','수입 브랜드 유통사 재무 지표 · 3개년',sv('유통사 비교',()=>{ const fs=fiScore(); return fs&&fs.na?`<b>${esc(CMP.peer.selfName)} FY${String(fs.L).slice(2)}</b><br>중앙값보다 나음 ${fs.nb}/${fs.na}`:fs?'자료 없음':'수집 전'; }))}
    ${row('fb','shirt','패션 브랜드','국내 패션 브랜드 비교 · 아이웨어 비교 · 검색 vs 실적',sv('패션 브랜드',()=>{ const a=cmpData(CMP.fb), b=cmpData(CMP.ey), L=a.concat(b).map(x=>x.end).filter(Boolean).sort().pop();
      return a.length||b.length?`패션 <b>${a.length}</b> · 아이웨어 <b>${b.length}</b>${L?'<br>FY'+L.slice(2,4):''}`:'수집 전'; }))}
    ${row('fx','fx','환율','엔·유로·달러 1% 칸 알림 · 1년 추이',sv('환율',()=>{ const la=fxAlertsAll()[0]; return la?`<b>${mdTxt(la.date)} 알림</b><br>${FX_SH[la.c]} ${fxLine(la.line)} ${la.dir==='dn'?'↓':'↑'}`:'알림 없음'; }))}
    ${row('logi','ship','물류','수입(적출 거점·나라별 → 부산 · 항공 → 인천) · 수출 · 위험 신호',sv('물류',()=>{ const K=lgKcs('kcs_sea_import'); if(!K) return LOGI?'자료 확인':'수집 전'; const i=K.cols.indexOf('유럽연합')+1, v=i>0?K.L[i]:null;
      return v!=null?`<b>유럽발 ${lgN(v)}천원</b><br>40ft · ${lgMon(K.L[0])}`:'자료 확인'; }))}
    ${row('cb','globe','해외직구','나라별·상품군별 직구 금액 (분기)',sv('해외직구',()=>{ const CB=KR&&KR.cross_border; return CB&&CB.last?`<b>${cbPrdS(CB.last)}</b><br>최근 자료`:'수집 전'; }))}
    ${row('status','pulse','수집 상태','자료별 마지막 갱신 · 지연 여부'+sv('Claude 사용액',claudeMonthTxt,''),sv('수집 상태',()=>{ const st=statusRows(), late=st.filter(r=>r.late).length, part=st.reduce((a,r)=>a+(r.failed||0),0);
      return late?`<span class="wn">지연 ${late}</span>`:(part?`<span class="wn">일부 실패 ${part}곳</span>`:'<b class="ok">정상</b>'); }))}
    ${themeRowHtml()}
  </nav><p class="mnote">새 지표는 하단 탭(4개)을 늘리지 않고 시장 칩이나 여기에 추가합니다.</p>`;
}
// '화면 테마' 줄(자료와 무관) — 메뉴가 통째로 실패해도 buildMore가 남김
const themeRowHtml=()=>`<button type="button" class="mi" id="themeBtn" aria-pressed="${theme==='dark'}" onclick="toggleTheme()"><span class="mic">${ic(theme==='dark'?'moon':'sun',22)}</span><span class="mtt"><span class="mt">화면 테마</span><span class="md">밝게 · 어둡게 바꾸기</span></span><span class="mr"><b>${theme==='dark'?'어둡게':'밝게'}</b></span></button>`;
function moreFashionHtml(){   // 패션 브랜드: 국내 패션 브랜드 비교 + 아이웨어 비교(v32.6)
  const sec=cid=>{const c=CMP[cid], n=cmpData(c).length; return n?`<div class="ndate" style="margin-top:16px">${esc(c.name)} <span class="na" style="font-weight:400">${n}곳 · ${esc(c.tag)}</span></div>`+(fiHas(cid)?finCardHtml(cid):cmpCardHtml(cid)):'';};
  return moreHead('패션 브랜드','국내 패션 브랜드 비교 · 아이웨어 비교 · 검색 vs 실적 · DART 연간')+sec('fb')+sec('ey')+svCardHtml();
}
/* ── 브랜드 점검표(v32.17, 대표 지시 2026-10-10) — 국내 수요 + 매입 조건(본사 재고·본사 발언·환율)으로 브랜드별 판정.
   대상: 네이버 검색 감시 브랜드(global) 중 본사가 상장사로 연결된 곳. 본사 자료가 없는 브랜드는 아래 표에 검색·환율만 ── */
const CHK_CUR=__CHK_CUR__;   // 원산지(본사) 통화 — 파이썬 CHK_CUR(이 파일 아래, 판정 기록과 같은 표)에서 넣음
const CHK_RULE=__CHK_RULE__;   // v33.2 판정 규칙 판 — 기록(history.json verdicts)의 rule이 같을 때만 '어제와 달라진 판정'을 비교
const CHK_SIG=__CHK_SIG__;   // v33.2 비교 기준(감시 브랜드·본사 연결·원산지 통화표, 파이썬 chk_sig) — 같은 기록끼리만 비교(화면에는 같은 것만 들어옴)
const CHK_CUR_NOTE={'가니':'덴마크 크로네(유로 고정)','에코(ECCO)':'덴마크 크로네(유로 고정)','노르다':'캐나다 — 미국 달러로 대신',
  '아크테릭스':'캐나다 — 미국 달러로 대신','룰루레몬':'캐나다 — 미국 달러로 대신',   // v33.7
  '톰브라운':'뉴욕 브랜드 — 달러(본사 제냐 재무는 유로)'};   // v33.8
const CHK_SALE={EUR:['FR','IT'],GBP:['GB'],USD:['US'],JPY:['JP']};   // 통화 지역의 해외 세일(캘린더와 같은 일정, saleEvents의 나라 코드 cc)
const CHK_LV={2:{t:'지금 검토'},1:{t:'관망'},0:{t:'주의'}};   // v33 배지 모양은 VB·vbadge(아래)
const sgn=v=>(v>0?'+':(v<0?'−':''))+Math.abs(v);
let CHK_CACHE=null;
function chkMedian(){   // 감시 브랜드(global, 검색량 충분) 전년 대비의 중앙값 — 시장 전체 흐름을 빼고 브랜드 힘만 보려고
  const v=((NAVER&&NAVER.brands)||[]).filter(b=>b.group==='global'&&b.yoy!=null&&!b.low).map(b=>b.yoy).sort((a,b)=>a-b), n=v.length;
  return n?(n%2?v[(n-1)/2]:(v[n/2-1]+v[n/2])/2):null;
}
// v33 S2: chk*는 화면(브랜드 탭·상세·오늘)에 쓰는 원래 숫자도 돌려줌 — 점수·판정 규칙(±10%p·±5%p·±5/±10%)은 그대로
function chkDemand(b,med){
  if(b.yoy==null) return {pt:0,na:1,yoy:null,med,low:!!b.low,trend:b.trend,txt:'검색 자료 없음'};
  if(med==null) return {pt:0,yoy:b.yoy,med,low:!!b.low,trend:b.trend,stale:b.stale_since,txt:`전년 대비 ${pp(b.yoy)}`};
  const rel=b.yoy-med, pt=b.low?0:(rel>=10?1:(rel<=-10?-1:0));
  return {pt, rel, yoy:b.yoy, med, low:!!b.low, trend:b.trend, stale:b.stale_since, txt:`전년 대비 ${pp(b.yoy)} · 감시 브랜드 중앙값(${pp(med)})보다 ${ppp(rel)}`
    +(b.trend!=null?` · 최근 4주 vs 직전 12주 ${pp(b.trend)}`:'')+(b.low?' · 검색량 적어 점수 제외':'')};
}
function chkInv(x){
  const ip=invPick(x);
  if(ip.inv==null||ip.rev==null) return {pt:0,na:1,txt:'같은 기간 재고·매출 자료 없음'};
  const P=ip.inv-ip.rev, pt=P>=5?1:(P<=-5?-1:0);
  return {pt, P, inv:ip.inv, rev:ip.rev, lbl:ip.lbl, q:ip.q, end:ip.end, stale:x.stale_since, pend:pendOf(x), txt:`재고 ${pp(ip.inv)} vs 매출 ${pp(ip.rev)} (${ip.lbl}) → 재고 압력 ${ppp(P)} · ${pt>0?'처분 물량 기대':(pt<0?'재고 빠듯':'보통')}`};
}
function chkNotes(t){
  const s=segOf(t), ex=s&&s.extract;
  if(!ex||!Array.isArray(ex.mgmt_notes)) return {pt:0,na:1,none:1,list:[],m:0,l:0,z:0,u:0,txt:'발언 자료 없음 — 이 회사 실적 자료에서 뽑은 발언이 없음(표 형식 자료·야후 수치만)'};
  const L=ex.mgmt_notes, m=L.filter(n=>n.sig==='more').length, l=L.filter(n=>n.sig==='less').length,
    z=L.filter(n=>n.sig==='neutral').length, u=L.length-m-l-z, per=perKo((ex.period||'').split(/;| ended/)[0]);   // u = 아직 신호 분류 전(다음 추출 때 판정)
  return {pt:m>l?1:(l>m?-1:0), na:(L.length&&u===L.length)?1:0, list:L, m, l, z, u, per, tag:/^IR/.test(s.source||'')?'IR 추출':'공시 추출', txt:(per?per+' · ':'')+(L.length?`할인 물량↑ ${m}건 · 할인·공급↓ ${l}건`
    +(z?` · 중립 ${z}건`:'')+(u?` · 신호 분류 전 ${u}건(다음 추출 때 판정)`:''):'재고·할인·유통 관련 발언 없음')};
}
function chkFx(cur){
  const f=(DATA.fx||{})[cur]; if(!f) return {pt:0,na:1,txt:`${cur} 환율 자료 없음`};
  const dev=f.dev_pct!=null, v=dev?f.dev_pct:f.chg_pct;
  if(v==null) return {pt:0,na:1,name:f.name,txt:`${f.name} 변동 자료 없음`};
  const pt=v<=-10?2:(v<=-5?1:(v>=10?-2:(v>=5?-1:0)));
  return {pt, v, basis:dev?'avg':'yago', name:f.name, rate:f.rate, mul:fxMul(cur), chg:f.chg_pct, dev:f.dev_pct, asof:f.asof, stale:f.stale_since, txt:`${f.name} ${dev?'1년 평균 대비':'1년 전 대비'} ${pp(v)} · ${pt>0?'매입 부담 줄어듦':(pt<0?'매입 부담 커짐':'비슷')}`};
}
function chkSaleEv(cur){   // v33 S2: 통화 지역의 다음 해외 세일 사건 {e, dn, live} — 브랜드 상세 '다음 일정'(캘린더 탭과 같은 일정)
  const today=kstMid(); const cc=CHK_SALE[cur]||[];
  const e=saleAll(today).filter(e=>cc.indexOf(e.cc)>=0&&e.e>=today).sort((a,b)=>a.s-b.s)[0];
  return e?{e, dn:Math.round((e.s-today)/86400000), live:e.s<=today}:null;
}
// 최근 14일 ★2 이상 브랜드 뉴스(참고) — 제목·요약에 그 브랜드 이름(키워드)이 있는 것만(호카·어그처럼 뉴스 묶음을 같이 쓰는 경우), 최대 n건
function chkNewsList(b,n){
  const key=b&&b.news; if(!key||!NEWS||!NEWS.items) return [];
  const kw=((b.keywords&&b.keywords.length)?b.keywords:[b.name]).map(k=>String(k).toLowerCase()).filter(Boolean);
  // v33.8 한글 검색어는 띄어쓰기를 빼고도 맞춤('톰 브라운'·'스톤 아일랜드'·'랄프 로렌' 기사) — 영문은 그대로(낱말이 붙어 엉뚱하게 맞지 않게)
  const nsp=s=>s.replace(/\s+/g,''), hit=t=>{ const T=t.toLowerCase(), N=nsp(T); return kw.some(k=>T.indexOf(k)>=0||(/[가-힣]/.test(k)&&N.indexOf(nsp(k))>=0)); };
  return newsDedupe(NEWS.items.filter(it=>it.scope==='brand'&&it.key===key&&(it.importance||1)>=2
      &&hit((it.title||'')+' '+(it.summary||'')))
    .sort((a,b)=>(b.first_seen||'').localeCompare(a.first_seen||'')||(b.importance||0)-(a.importance||0)),n||3);
}
function chkModel(){
  if(CHK_CACHE) return CHK_CACHE;
  const med=chkMedian(), main=[], rest=[];
  ((NAVER&&NAVER.brands)||[]).filter(b=>b.group==='global').forEach(b=>{
    const cur=own(CHK_CUR,b.name)?CHK_CUR[b.name]:null, link=b.link?String(b.link):'';
    const x=link&&!link.startsWith('krd:')?DATA.items.find(i=>i.ticker===link):null;
    // v33 S2: 옛 점검표 카드용 sale·news는 뺌(다음 세일·뉴스는 상세에서 chkSaleEv·chkNewsList) — 세일·뉴스 자료가 깨져도 판정 목록은 그려짐
    const r={b, x, cur, link, dem:chkDemand(b,med), fx:cur?chkFx(cur):{pt:0,na:1,txt:'원산지 통화 미지정'}};
    if(!x){ rest.push(r); return; }
    r.inv=chkInv(x); r.notes=chkNotes(x.ticker);
    if(r.inv.na&&r.notes.na){ rest.push(r); return; }   // 본사 재고·발언 근거가 둘 다 없으면 판정하지 않음(환율만으로 판정되지 않게)
    r.buy=r.inv.pt+r.notes.pt+r.fx.pt;
    r.lv=(r.dem.pt>=0&&r.buy>=2)?2:(((r.dem.pt<0&&r.buy<=1)||r.buy<=-1)?0:1);
    main.push(r);
  });
  const relOf=r=>r.dem.rel!=null?r.dem.rel:-999;
  main.sort((a,b)=>(b.lv-a.lv)||((b.buy+b.dem.pt)-(a.buy+a.dem.pt))||(relOf(b)-relOf(a)));
  rest.sort((a,b)=>relOf(b)-relOf(a));
  return (CHK_CACHE={main, rest, med});
}
/* ── v33.2 판정 기록 — history_append가 자료 날짜마다 저장(history.json verdicts: {date, rule, b:{브랜드:[판정, 수요, 재고, 발언, 환율]}},
   판정은 파이썬 chk_verdicts = 위 chkModel과 같은 규칙). 지금 판정을 보는 자료 날짜 바로 전 기록과 비교해 '어제와 달라진 판정'.
   규칙 판(CHK_RULE)이 다른 기록은 비교하지 않음 · 오늘 기록이 화면 판정과 다른 브랜드(계산 어긋남)는 비교에서 빼고 콘솔에 남김 ── */
const CHK_PT=['수요','재고','발언','환율'];
const NB='\u00a0';   // 줄바꿈 안 되는 칸 — '지금 검토'·'환율 0 → +1'이 두 줄로 갈라지지 않게
const lvT=v=>v==null?`판정${NB}안${NB}함`:CHK_LV[v].t.replace(/ /g,NB);
const ptT=v=>v==null?'―':sg0(v);
let CHK_HIST=null;
function chkHist(){
  if(CHK_HIST) return CHK_HIST;
  const dd=String(DATA.generated_at||'').slice(0,10), H=(HIST&&Array.isArray(HIST.verdicts))?HIST.verdicts:[];
  // 비교할 수 있는 기록만 — 규칙 판·비교 기준(sig: 감시 브랜드·본사 연결·통화표)이 같고 모양이 맞는 것(파이썬이 같은 것만 넣지만 한 번 더)
  const V=H.filter(r=>r&&r.rule===CHK_RULE&&r.sig===CHK_SIG&&typeof r.date==='string'&&/^\d{4}-\d{2}-\d{2}$/.test(r.date)&&r.b&&typeof r.b==='object'&&!Array.isArray(r.b))
    .sort((a,c)=>a.date<c.date?-1:(a.date>c.date?1:0));
  const prev=V.filter(r=>r.date<dd).pop()||null, cur=V.filter(r=>r.date===dd).pop()||null, M=chkModel();
  // 기록의 판정 — [판정 0·1·2, 점수 4개(정수·null)]면 판정 값, 기록에 없으면 null(판정 안 함), 모양이 틀리면 undefined(비교하지 않음) — 파이썬 chk_entry_ok와 같은 기준
  const lvOf=(rec,n)=>{ if(!rec||!own(rec.b,n)) return null; const v=rec.b[n];
    return (Array.isArray(v)&&v.length>=5&&Number.isInteger(v[0])&&own(CHK_LV,v[0])&&v.slice(1,5).every(p=>p===null||Number.isInteger(p)))?v[0]:undefined; };
  const by=Object.create(null), list=[], skip=[];
  if(prev){
    const now=new Set(M.main.map(r=>r.b.name)), shown=new Set(M.main.concat(M.rest).map(r=>r.b.name));   // shown = 지금 점검표에 있는 브랜드
    M.main.forEach(r=>{ const n=r.b.name;
      if(cur&&lvOf(cur,n)!==r.lv){ skip.push(n); return; }
      const pl=lvOf(prev,n); if(pl===undefined){ skip.push(n); return; } if(pl===r.lv) return;
      const p=prev.b[n], np=[r.dem,r.inv,r.notes,r.fx].map(o=>(!o||o.na)?null:o.pt);
      const why=pl!=null?CHK_PT.map((k,j)=>{ const a=p[j+1]; return a!==np[j]?[k,ptT(a),'→',ptT(np[j])].join(NB):''; }).filter(Boolean):[];
      list.push(by[n]={name:n, from:pl, to:r.lv, why}); });
    Object.keys(prev.b).forEach(n=>{ if(now.has(n)||!shown.has(n)) return; const pl=lvOf(prev,n); if(pl===null) return;   // null = 그때도 판정 안 함
      if(pl===undefined||(cur&&lvOf(cur,n)!==null)){ skip.push(n); return; }   // 모양 틀림 · 오늘 기록은 판정했는데 화면은 판정 안 함
      list.push(by[n]={name:n, from:pl, to:null, why:[]}); });
  }
  // 오늘 기록만 판정한 브랜드(화면은 판정 안 함) — 어제 기록에 없어도 계산 어긋남이라 알림
  if(cur) Object.keys(cur.b).forEach(n=>{ if(!M.main.some(r=>r.b.name===n)&&skip.indexOf(n)<0&&lvOf(cur,n)!==null) skip.push(n); });
  if(skip.length) console.error('[판정 기록] 화면 판정과 기록이 다르거나 기록 모양이 틀림 — 비교에서 뺌:',skip.join(', '));
  const gap=prev?Math.round((new Date(dd+'T00:00:00')-new Date(prev.date+'T00:00:00'))/86400000):0;
  return (CHK_HIST={prev, V, by, list, skip, dd, gap});
}
// 날짜 이름은 볼 때마다 — 자료가 오늘(한국 날짜) 것이고 바로 전 기록이 하루 전이면 '오늘'·'어제', 아니면 날짜(자정이 지나면 바뀜)
function chkLbl(C){
  const cl=C.dd===kstToday()?'오늘':mdTxt(C.dd), pl=C.prev?((cl==='오늘'&&C.gap===1)?'어제':mdTxt(C.prev.date)):'';
  return {cl, pl, vs:pl==='어제'?'어제와':`${pl} 기록과`};   // vs: '어제와' · '10/12 기록과'(날짜 끝소리 조사 피함)
}
const chkChgTxt=c=>`${c.name} ${lvT(c.from)} → ${lvT(c.to)}${c.why.length?`(${c.why.join(', ')})`:''}`;
// 판정이 바뀐 브랜드 꼬리표 — '어제 관망'(바뀌기 전 판정), 새로 판정된 브랜드는 '새로 판정'
function chgTag(n){
  let C; try{ C=chkHist(); }catch(e){ console.error('[판정 기록] 비교 실패:',e); return ''; }
  const c=C.by[n]; if(!c) return '';
  const Lb=chkLbl(C);
  return `<span class="tg chg" title="${esc(`${Lb.pl} ${lvT(c.from)} → ${Lb.cl} ${lvT(c.to)}`)}">${esc(c.from==null?'새로 판정':`${Lb.pl} ${lvT(c.from)}`)}</span>`;
}
function chkSince(n,lv){   // 같은 판정이 이어진 첫 기록 날짜 — {d, first: 판정 기록을 시작한 날부터 내내, cut: 비교할 수 있는 기록 처음부터 내내(그 전은 기준이 다르거나 화면에 없음)}
  const C=chkHist(), V=C.V.filter(r=>r.date<=C.dd); let d=null;
  for(let j=V.length-1;j>=0;j--){ const v=V[j].b[n]; if(Array.isArray(v)&&v[0]===lv) d=V[j].date; else break; }
  if(!d) return null;
  const all=d===V[0].date, st=HIST&&HIST.verdicts_start;
  return {d, first:all&&(!st||st===d), cut:all&&!!st&&st<d};
}
/* ── v33 A안 S2: 판정 이유 · 점수 칸 · 상세 모델 — Claude·무작위 없이 chkModel 값만(판정 규칙은 위 그대로 · 주간 메일과 같은 규칙) ── */
const JONG_D={0:21,1:8,3:16,6:1,7:8,8:8};   // 숫자 끝을 읽는 소리의 받침(영·일·삼·육·칠·팔)
const jo=(s,a,b,ro)=>{ s=String(s); const ch=s[s.length-1]||'', c=ch.charCodeAt(0);
  const j=(c>=0xAC00&&c<=0xD7A3)?(c-0xAC00)%28:(/\d/.test(ch)?(JONG_D[ch]||0):0);
  return s+((j&&!(ro&&j===8))?a:b); };   // 조사 — 받침 있으면 a, 없으면 b(ro=1이면 ㄹ 받침도 '로')
const sg0=v=>v?sgn(v):'0';
const p1=v=>Math.abs(v).toFixed(1);
/* 판정 이유 {head 상세 제목, short 목록·오늘 한 줄(최대 2구절), say 상세 한 문장} — 구절 순서 재고 → 발언 → 환율. 계절 영향이 섞인 trend는 쓰지 않음 */
function chkWhy(r){
  const d=r.dem, i=r.inv||{pt:0,na:1}, n=r.notes||{pt:0,na:1}, x=r.fx||{pt:0,na:1};
  const cur=x.name||r.cur||'', base=x.basis==='avg'?'1년 평균':'1년 전';
  const fxS=x.na?'':`${cur} ${p1(x.v)}% ${x.v<0?'쌈':'비쌈'}`;                              // '유로 11.1% 쌈'
  const fxClause=x.na?'':`${jo(cur,'이','가')} ${base}보다 ${p1(x.v)}% ${x.v<0?'싸':'비싸'}`;     // '유로가 1년 평균보다 11.1% 싸'
  // 성분별 문구 — nm 이름 · ps/ns 짧은 구절(유리/불리) · pn 이점 명사 · pc/nc 문장 조각[중간(~고), 끝(~서/~해), 양보(~지만)]
  const C={
    inv:{nm:'본사 재고', ps:'본사 재고 증가로 처분 물량 기대', ns:'본사 재고 빠듯', pn:'처분 물량 기대',
         pc:i.na?[]:[`본사 재고가 매출보다 ${p1(i.P)}%p 빨리 늘었고`,`본사 재고가 매출보다 ${p1(i.P)}%p 빨리 늘어`,`본사 재고가 매출보다 ${p1(i.P)}%p 빨리 늘었지만`],
         nc:['본사 재고가 빠듯하고','본사 재고가 빠듯해']},
    notes:{nm:'본사 발언', ps:'본사 할인 물량 확대 발언', ns:'본사 할인·공급 축소 발언', pn:'할인 물량 확대 발언',
         pc:['본사가 할인 물량 확대를 언급했고','본사가 할인 물량 확대를 언급해','본사가 할인 물량 확대를 언급했지만'],
         nc:['본사가 할인·공급 축소를 언급했고','본사가 할인·공급 축소를 언급해']},
    fx:{nm:'환율', ps:fxS, ns:fxS, pn:`${cur} 이점`, pc:[fxClause+'고',fxClause+'서',fxClause+'지만'], nc:[fxClause+'고',fxClause+'서']}
  };
  const P={inv:i.pt, notes:n.pt, fx:x.pt}, K=['inv','notes','fx'], O={inv:i,notes:n,fx:x};
  const pos=K.filter(k=>P[k]>0), neg=K.filter(k=>P[k]<0), neu=K.filter(k=>P[k]===0&&!O[k].na);
  const chain=(ks,f)=>ks.map((k,j)=>C[k][f][j<ks.length-1?0:1]).join(', ');   // 'A하고, B해서'
  const list=ks=>ks.map((k,j)=>j<ks.length-1?jo(C[k].nm,'과','와'):jo(C[k].nm,'은','는')).join(' ');   // '본사 재고와 본사 발언은'
  const dS=d.yoy!=null?`국내 검색 ${pctU(d.yoy)}로 약함`:'국내 검색 약함';
  const buyS=`매입 조건 ${sg0(r.buy)}${pos.length&&r.buy>0?`(${pos.map(k=>C[k].nm).join('·')})`:''}`;
  let head, short, say;
  if(r.lv===2){
    if(i.pt+n.pt<=0){   // 옛 점검표 '환율 영향이 대부분'과 같은 조건(환율 +2, 재고+발언 0)
      head='환율 영향이 대부분'; short=[head, fxS];
      // '보통'은 점수 0인 성분만 — 검색 +1·재고/발언 상쇄는 따로(타일·근거 카드와 같은 말)
      const zs=[d.na||d.pt?null:'국내 검색', i.na||i.pt?null:'본사 재고', n.na||n.pt?null:'본사 발언'].filter(Boolean);
      const zl=zs.map((t,j)=>j<zs.length-1?jo(t,'과','와'):jo(t,'은','는')).join(' '), dh=d.pt>0?`국내 검색은 감시 브랜드 중앙값보다 ${p1(d.rel)}%p 높고`:'';
      const cl=[dh?[dh,dh]:null, zs.length?[zl+' 보통이고',zl+' 보통인데']:null,   // [중간, 끝]
        i.pt&&n.pt?[`본사 재고와 본사 발언은 ${sgn(i.pt)}·${sgn(n.pt)}로 서로 상쇄되고`,`본사 재고와 본사 발언은 ${sgn(i.pt)}·${sgn(n.pt)}로 서로 상쇄되지만`]:null].filter(Boolean);
      say=`${cl.map((c,j)=>c[j<cl.length-1?0:1]+', ').join('')}${fxClause}서 매입 조건이 ${jo(sgn(r.buy),'이','가')} 됐습니다.`;
    } else {
      head=C[pos[0]].ps; short=pos.slice(0,2).map(k=>C[k].ps);
      say=`${chain(pos,'pc')} 매입 조건이 ${jo(sgn(r.buy),'이','가')} 됐습니다.`;
    }
  } else if(r.lv===0){
    if(d.pt<0){
      head='국내 수요 약함'; short=[dS, neg.length?C[neg[0]].ns:buyS];
      say=`네이버 검색이 감시 브랜드 중앙값보다 ${p1(d.rel)}%p 낮고, `+(r.buy>0?`매입 조건은 ${sgn(r.buy)}에 그쳐`:`매입 조건도 ${jo(sg0(r.buy),'이라','라')}`)+' 주의로 봅니다.';
    } else {
      head='매입 조건 불리'; short=neg.slice(0,2).map(k=>C[k].ns);
      say=`${pos.length?C[pos[0]].pn+'에도 ':''}${chain(neg,'nc')} 매입 조건이 ${jo(sgn(r.buy),'이','가')} 됐습니다(주의 기준 −1 이하).`;
    }
  } else if(d.pt<0){   // 관망: 매입 조건은 좋지만 수요가 약함
    head='매입 조건은 좋지만 수요 약함'; short=[dS, `매입 조건 ${sgn(r.buy)}`];
    say=`매입 조건은 ${jo(sgn(r.buy),'으로','로',1)} 지금 검토 기준(+2)을 넘지만, 국내 검색이 중앙값보다 ${p1(d.rel)}%p 낮아 관망으로 봅니다.`;
  } else {             // 관망: 수요는 괜찮고 매입 조건 0~+1
    const off=pos.length&&neg.length;
    const s2=off?`${neg.length>1?jo(neg.map(k=>C[k].nm).join('·'),'이','가')+' 불리해':C[neg[0]].nc[1]} ${jo(C[pos[0]].pn,'과','와')} 상쇄`:pos.length?`${pos.map(k=>C[k].nm).join('·')}만 유리`:'특이 신호 없음';
    if(d.pt>0){
      head='수요는 강하지만 매입 조건 부족'; short=[`국내 검색 중앙값보다 +${p1(d.rel)}%p`, s2];
      say=`국내 검색은 감시 브랜드 중앙값보다 ${p1(d.rel)}%p 높지만 매입 조건이 ${jo(sg0(r.buy),'이라','라')} 지금 검토 기준(+2)에 못 미칩니다.`;
    } else if(off){
      head='유리·불리 신호가 상쇄'; short=[s2];
      say=`${s2}되고, 매입 조건이 ${jo(sg0(r.buy),'이라','라')} 지금 검토 기준(+2)에 못 미칩니다.`;
    } else if(pos.length){
      head=s2; short=[s2, C[pos[0]].ps];
      say=`${C[pos[0]].pc[2]} ${neu.length?list(neu)+' 보통이라':'다른 본사 자료가 없어'} 매입 조건이 ${sgn(r.buy)}에 그칩니다(지금 검토는 +2부터).`;
    } else {
      head='특이 신호 없음'; short=[head, '매입 조건 0'];
      const ok=[d.na?'':'국내 검색', i.na?'':'본사 재고', n.na?'':'본사 발언', x.na?'':'환율'].filter(Boolean);   // 자료 있는 성분만
      say=`${jo(ok.join('·'),'이','가')}${ok.length>1?' 모두':''} 보통 범위라 관망으로 봅니다.`;
    }
  }
  return {head, short:short.filter(Boolean).join(' · '), say};
}
/* 브랜드 행 점수 4칸(수요·재고·발언·환율) — tone p 유리 · n 불리 · z 보통 · na 자료 없음 */
function chkCells(r){
  return [['수요',r.dem],['재고',r.inv],['발언',r.notes],['환율',r.fx]].map(([k,o])=>({k, v:(!o||o.na)?'―':(o.pt?sgn(o.pt):'0'),
    tone:(!o||o.na)?'na':(o.pt>0?'p':(o.pt<0?'n':'z'))}));
}
const chkHq=r=>r.x?nmSplit(r.x.name).main:'';   // '데커스(HOKA)' → '데커스'
const chkCurKo=r=>CHK_CUR_NOTE[r.b.name]||((DATA.fx||{})[r.cur]||{}).name||r.cur||'통화 미지정';
function chkFind(n){ const M=chkModel(); return M.main.concat(M.rest).find(r=>r.b.name===n)||null; }
const krdOf=l=>String(l||'').startsWith('krd:')?(((KRD&&KRD.entities)||[]).find(e=>'krd:'+e.id===l)||null):null;   // 'krd:' 연결은 법인이 수집돼 있을 때만
/* 브랜드 상세 모델 — 판정 안 함(rest)도 같은 틀: 근거 2장(국내 수요·원산지 통화) */
function chkDetail(r){
  const judged=r.lv!=null;
  if(!judged) r={...r, inv:r.inv||{pt:0,na:1,txt:''}, notes:r.notes||{pt:0,na:1,none:1,list:[],m:0,l:0,z:0,u:0}};
  const d=r.dem, i=r.inv, n=r.notes, x=r.fx, hq=chkHq(r), ke=krdOf(r.link), gd=String(DATA.generated_at||'').slice(0,10);
  const base=x.basis==='avg'?'1년 평균':'1년 전', fxNm=r.cur==='JPY'?'엔(100엔)':(x.name||r.cur||''), curKo=(r.cur||CHK_CUR_NOTE[r.b.name])?chkCurKo(r):'';   // curKo '' = CHK_CUR에 없음(미지정)
  const w=judged?chkWhy(r):{head:'판정 안 함 — 검색·환율만 참고',
    say:((r.x?`본사 ${hq}의 재고·발언 자료가 없어`:(ke?'국내 법인만 연결돼 본사 재고·발언 자료가 없어':'본사가 비상장이거나 연결된 상장사가 없어'))+' 판정하지 않습니다.'
      +(d.low&&d.yoy!=null?` 국내 검색(전년 대비 ${pctU(d.yoy)})은 검색량이 적어 중앙값과 비교하지 않고`   // 검색량 적음 = 점수 제외(타일과 같게)
        :d.rel!=null?(p1(d.rel)==='0.0'?' 국내 검색은 감시 브랜드 중앙값과 같고':` 국내 검색은 감시 브랜드 중앙값보다 ${p1(d.rel)}%p ${d.rel>=0?'높':'낮'}고`):'')
      +(x.na?'':`${d.rel!=null?',':''} ${jo(x.name,'은','는')} ${base}보다 ${p1(x.v)}% ${x.v<0?'쌉':'비쌉'}니다.`)).replace(/고$/,'습니다.')};
  const sib=nvAll().filter(b=>b.group==='global'&&r.x&&b.link===r.x.ticker).map(b=>b.name);
  const word=(o,a,b)=>o.na?'자료 없음':(o.pt>0?a:(o.pt<0?b:'보통'));
  const tone=o=>o.na?'':(o.pt>0?'p':(o.pt<0?'n':''));
  const today=kstMid();
  const s8=(r.b.s||[]).slice(-8), wk=((NAVER&&NAVER.weeks)||[]).slice(-8);
  const sparkOk=s8.length===8&&wk.length===8&&s8.every(v=>typeof v==='number'&&isFinite(v));
  const oldInv=!i.na&&i.q===false&&!!i.end&&(today-new Date(i.end+'T00:00:00'))/86400000>270;   // 연간 결산 재고가 9개월 넘음 — 표시만, 점수 그대로(결정 D14)
  const unc=n.list.length&&n.u===n.list.length;
  const ev=[
    {id:'dem', label:'국내 수요', score:d.na?'':sg0(d.pt), tone:tone(d), word:d.low?'보통(검색량 적음)':word(d,'강함','약함'),
      value:d.yoy!=null?`네이버 검색 전년 대비 ${pctU(d.yoy)}`:'네이버 검색 자료 없음', tags:staleA(r.b.stale_since),
      explain:d.yoy==null?'이 브랜드의 네이버 검색 자료가 없어 점수에 넣지 않았습니다.'
        :d.low?'검색량이 적어(나이키 대비 규모 1 미만) 변동이 커서 점수에 넣지 않습니다.'
        :d.rel==null?'비교할 중앙값이 없어 0으로 둡니다.'
        :(p1(d.rel)==='0.0'?`감시 브랜드 중앙값(${pctU(d.med)})과 같아 보통으로 봅니다.`
          :`감시 브랜드 중앙값(${pctU(d.med)})보다 ${p1(d.rel)}%p ${d.rel>=0?'높':'낮'}${d.pt===0?'지만 ±10%p 안이라 보통으로 봅니다.':(d.pt>0?'아 +1입니다.':'아 −1입니다.')}`)
          +(d.trend!=null?` 최근 4주는 직전 12주보다 ${pctU(d.trend)}(계절 영향 포함).`:''),
      spark:sparkOk?{vals:s8, wk}:null},
    {id:'inv', label:'본사 재고', score:i.na?'':sg0(i.pt), tone:tone(i), word:word(i,'유리','불리'),
      value:i.na?'같은 기간 재고·매출 자료 없음':`재고 압력 ${ppp(i.P)}`,
      tags:(i.na?'':staleA(i.stale)+pendA(i.pend))+(oldInv?tagA(`결산 ${ym(i.end)} · 오래된 자료`,'연간 결산 재고가 9개월 넘게 지남 — 점수는 그대로'):''),
      explain:i.na?'본사 재고와 같은 기간 매출이 없어 점수에 넣지 않았습니다.'
        :`재고 ${pctU(i.inv)} vs 매출 ${pctU(i.rev)}(${i.lbl}). `+(Math.abs(i.P)<1?'재고 증가율과 매출 증가율이 거의 같습니다. ':'')
          +(i.pt===0?'차이가 5%p 이상이어야 신호로 봅니다.':i.pt>0?'재고가 매출보다 5%p 넘게 빨리 늘어 할인·처분 물량이 나올 수 있습니다.':'재고가 매출보다 5%p 넘게 덜 늘어 처분 물량이 적을 수 있습니다.')
          +(sib.length>1?` 본사 전체 기준(${sib.join('·')} = ${hq}).`:'')
          +(i.pend?` 본사가 ${mdTxt(i.pend.end)} 끝난 분기 실적을 냈지만 야후 미반영 — 이전 분기 값입니다.`:'')},
    {id:'notes', label:'본사 발언', score:n.na?'':sg0(n.pt), tone:tone(n), word:unc?'분류 전':word(n,'유리','불리'),
      value:n.none?'발언 자료 없음':!n.list.length?'재고·할인·유통 관련 발언 없음'
        :(unc?`발언 ${n.list.length}건 · 신호 분류 전`:`할인 물량↑ ${n.m}건 · 할인·공급↓ ${n.l}건${n.z?` · 중립 ${n.z}건`:''}${n.u?` · 분류 전 ${n.u}건`:''}`),
      explain:n.none?`${hq||r.b.name} 본사 실적 자료에서 재고 처분·할인 관련 발언을 뽑지 못해(표 형식 자료·야후 수치만) 점수에 넣지 않았습니다.`
        :!n.list.length?`${n.per||'최근 실적'} 자료에 재고·할인·유통 관련 발언이 없어 0입니다.`
        :unc?'발언은 뽑혔지만 신호(할인 물량↑/할인·공급↓) 분류 전이라 점수에 넣지 않았습니다. 매주 공시 추출 때 분류됩니다.'
        :`할인 물량을 늘린다는 발언 ${n.m}건, 할인·공급을 줄인다는 발언 ${n.l}건이라 ${sg0(n.pt)}입니다.${n.per?` (${n.per}${n.tag?' · '+n.tag:''})`:''}`,
      list:(n.list||[]).map(q=>({sig:q.sig||null, topic:q.topic, ko:q.ko, quote:q.quote}))},
    {id:'fx', label:`원산지 통화 · ${x.name||curKo||'미지정'}`, score:x.na?'':sg0(x.pt), tone:tone(x), word:word(x,'유리','불리'),
      value:(x.na||x.rate==null)?'환율 자료 없음':`${fxNm} ${wonR(x.rate*x.mul)}원 · ${base}보다 ${p1(x.v)}% ${x.v<0?'쌈':'비쌈'}`, tags:x.na?'':staleA(x.stale),
      explain:x.na?'원산지 통화 환율이 없어 점수에 넣지 않았습니다.'
        :(x.basis==='avg'&&x.chg!=null?`1년 전보다${(x.chg<0)===(x.v<0)?'도':'는'} ${p1(x.chg)}% ${x.chg<0?'쌉':'비쌉'}니다. `:x.basis==='yago'?'1년 평균을 계산하지 않는 통화라 1년 전 대비로 봅니다. ':'')
          +(x.pt===0?'±5% 안이라 0입니다.':`${Math.abs(x.v)>=10?'10':'5'}% 이상 ${x.v<0?'싸서':'비싸서'} ${sgn(x.pt)}`+((judged&&r.lv===2&&i.pt+n.pt<=0)?` — 매입 조건 ${jo(sgn(r.buy),'이','가')} 모두 환율에서 나왔습니다.`:'입니다.'))
          +(CHK_CUR_NOTE[r.b.name]?` (${CHK_CUR_NOTE[r.b.name]})`:'')}
  ];
  const nx=[];
  if(r.x&&r.x.earn_date){ const dd=new Date(r.x.earn_date+'T00:00:00'), dn=Math.round((dd-today)/86400000);
    if(dn>=0) nx.push({dn, d:dn===0?'오늘':'D-'+dn, title:`${hq} 실적 발표`, sub:`${md2(dd)} · 발표 후 재고 점수 다시 계산`, kind:'실적', go:'co:'+r.x.ticker}); }
  if(!nx.length&&r.x) nx.push({dn:9999, d:'―', title:`${hq} 실적 발표일 미확인`, sub:'야후에 다음 발표일 없음 — 본사 공시로 확인', kind:'실적', go:'co:'+r.x.ticker});
  const se=chkSaleEv(r.cur), curNm=((DATA.fx||{})[r.cur]||{}).name||r.cur||'';
  if(se){ const e=se.e, yy=e.s.getFullYear()!==today.getFullYear();
    nx.push({dn:se.dn, d:se.live?'진행 중':'D-'+se.dn, title:e.nm, kind:'세일', go:'mk:cal:saleList',
      sub:se.live?`${md2(e.s)}~${md2(e.e)} · ${curNm} 지역 세일`:`${yy?ymdL(e.s):md2(e.s)}${e.k==='예상'?' 예상':''} · ${curNm} 지역 다음 세일`}); }
  nx.sort((a,c)=>a.dn-c.dn);
  const sameKey=r.b.news?nvAll().filter(b=>b.group==='global'&&b.news===r.b.news).map(b=>b.name):[];
  // v33.2 판정 기록 한 줄 — 바뀌었으면 '어제(10/13) 관망 → 오늘 지금 검토 · 환율 0 → +1', 그대로면 같은 판정이 이어진 첫 날
  let hist='';
  try{ const C=chkHist(), c=C.by[r.b.name], Lb=chkLbl(C);
    if(c) hist=`${Lb.pl==='어제'?`어제(${mdTxt(C.prev.date)})`:mdTxt(C.prev.date)} ${lvT(c.from)} → ${Lb.cl} ${lvT(c.to)}${c.why.length?` · ${c.why.join(', ')}`:''}`;
    else if(judged&&C.prev&&C.skip.indexOf(r.b.name)<0){ const sn=chkSince(r.b.name,r.lv);
      if(sn) hist=sn.first?`판정 기록을 시작한 ${mdTxt(sn.d)}부터 계속 ${lvT(r.lv)}`:sn.cut?`적어도 ${mdTxt(sn.d)}부터 계속 ${lvT(r.lv)}`:`${mdTxt(sn.d)}부터 계속 ${lvT(r.lv)}`; }
  }catch(e){ console.error('[브랜드 상세 · 판정 기록] 비교 실패:',e); }
  return {name:r.b.name, lv:judged?r.lv:null, verdict:judged?CHK_LV[r.lv].t:'판정 안 함', hist,
    meta:`${r.x?`본사 ${hq}`:(ke?`국내 법인 ${nmSplit(ke.name).main}`:'본사 연결 없음')} · 원산지 통화 ${curKo||'미지정'}${gd?` · ${mdTxt(gd)} ${judged?'판정':'기준'}`:''}`,
    head:w.head, say:w.say,
    tiles:{dem:{v:d.na?'―':sg0(d.pt), cap:d.na?'검색 자료 없음':d.low?'검색량 적어 점수 제외':d.pt>0?'강함 · 중앙값보다 10%p 이상 높음':d.pt<0?'약함 · 중앙값보다 10%p 이상 낮음':'보통 · 약하지 않음'},
           buy:!judged?{v:'―', cap:'본사 자료 없음 — 판정 안 함', ring:''}
             :{v:sg0(r.buy), cap:r.lv===2?'지금 검토 기준 +2 충족':r.buy<=-1?'주의 기준(−1 이하)':d.pt<0?(r.buy>=2?'+2 넘지만 국내 수요 약함':'수요 약함 + 매입 +1 이하 = 주의'):`지금 검토까지 +${2-r.buy}`,
               ring:r.buy>=2?'acc':(r.buy<=-1?'warn':'')}},
    ev:judged?ev:[ev[0],ev[3]], next:nx,
    news:chkNewsList(r.b,3).map(it=>({t:it.summary||it.title||'', link:it.link||'', meta:[newsDay(it), it.source, '★'.repeat(Math.max(1,Math.min(3,it.importance||1)))].filter(Boolean).join(' · ')})),
    newsAll:(r.b.news&&((NEWS&&NEWS.items)||[]).some(i=>i.scope==='brand'&&i.key===r.b.news))?{key:r.b.news, label:(sameKey.length?sameKey:[r.b.name]).join('·')}:null,   // 보관 뉴스 0건이면 단추 없음
    hqLink:r.x?{go:'co:'+r.x.ticker, title:`본사 ${hq} 기업 상세`, sub:'재무 · 지역·부문 매출'}:(ke?{go:'co:'+r.link, title:'국내 법인 상세', sub:'DART 연간 실적'}:null)};
}
/* 판정 배지 3종(+ 판정 안 함) — 지금 검토 = 파랑 채움 + 체크 원 · 관망 = 흰 바탕 회색 테두리 + 일시정지 원 · 주의 = 주황 + 삼각형 */
const VB={2:['go','go','지금 검토'],1:['wait','wait','관망'],0:['warn','warn','주의']};
const vbadge=(lv,big)=>(lv==null||!VB[lv])?`<span class="vb none${big?' lg':''}">${ic('info',big?17:15)}판정 안 함</span>`:`<span class="vb ${VB[lv][0]}${big?' lg':''}">${ic(VB[lv][1],big?17:15)}${VB[lv][2]}</span>`;
/* 최근 8주 네이버 검색 지수 — 회색 선 + 마지막 주 파란 점(값이 다 같으면 가운데 수평선) */
function spark8(vals,wk){
  const W=328,H=56,PX=6,PT=8,PB=8, n=vals.length, lo=Math.min(...vals), hi=Math.max(...vals);
  const pts=vals.map((v,i)=>[PX+i*(W-2*PX)/Math.max(1,n-1), hi===lo?(PT+(H-PT-PB)/2):(PT+(hi-v)/(hi-lo)*(H-PT-PB))]), L=pts[n-1];
  const lbl=`최근 8주 네이버 검색 지수, ${nvWk(wk[0])} 주 ${vals[0].toFixed(1)}에서 ${nvWk(wk[n-1])} 주 ${vals[n-1].toFixed(1)}`;
  return `<svg class="bd-spark" viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(lbl)}"><polyline class="sl" points="${pts.map(p=>p[0].toFixed(1)+','+p[1].toFixed(1)).join(' ')}"/><circle class="sd" cx="${L[0].toFixed(1)}" cy="${L[1].toFixed(1)}" r="5"/></svg>`;
}

/* ── v33 A안 S2: 브랜드 탭(A2) — 머리(제목·판정 기준 (i)·판정 필터 4칸) + 압축 행 + 판정 안 함 접기. 필터·(i)·접기는 기록 없이 메모리만 ── */
let BR_FILTER='all', BR_INFO=false, BR_REST=false;
const BR_F=[['all','전체',null],['go','지금 검토',2],['wait','관망',1],['warn','주의',0]];
const BR_NOTE={all:'점수: + 매입에 유리, − 불리, 0 보통, ― 자료 없음', go:'지금 검토 = 국내 수요가 약하지 않고 매입 조건 +2 이상',
  wait:'관망 = 지금 검토에도 주의에도 해당하지 않음', warn:'주의 = 국내 수요가 약하고 매입 조건 +1 이하, 또는 매입 조건 −1 이하'};
const chkMedN=()=>((NAVER&&NAVER.brands)||[]).filter(b=>b.group==='global'&&b.yoy!=null&&!b.low).length;   // chkMedian과 같은 거름(검색량 충분)
let BR_DAY=null;   // v33.2 브랜드 목록을 그린 한국 날짜
function buildBrand(){
  BR_DAY=kstToday();
  const M=chkModel(), cnt=lv=>M.main.filter(r=>r.lv===lv).length, gd=String(DATA.generated_at||'').slice(0,10);
  paint('brHead',()=>`<div class="hd-row"><div class="hd-tt"><h1>브랜드 점검표</h1><span class="hd-sub">본사 자료가 있는 ${M.main.length}곳${gd?` · ${mdTxt(gd)} 기준`:''}</span></div>
    <button type="button" class="icbtn" id="brInfoBtn" aria-label="판정 기준 보기" aria-expanded="${BR_INFO}" aria-controls="brInfo" onclick="brInfo()">${ic('info',22)}</button></div>
    <div class="seg4" role="group" aria-label="판정으로 거르기">${BR_F.map(([f,l,lv])=>`<button type="button" data-filter="${f}" aria-pressed="${BR_FILTER===f}" onclick="brFilter('${f}')">${l} <span class="tn">${lv==null?M.main.length:cnt(lv)}</span></button>`).join('')}</div>`,'브랜드 점검표 머리');
  paint('brandBody',brandBodyHtml,'브랜드 점검표');
}
function brSetFilter(f){   // 필터 바꾸기 — 목록만 다시 그림(머리의 단추는 그대로 두고 눌림 표시만). 스크롤은 부르는 쪽에서
  BR_FILTER=f;
  document.querySelectorAll('#brHead [data-filter]').forEach(b=>b.setAttribute('aria-pressed',b.dataset.filter===f?'true':'false'));
  paint('brandBody',brandBodyHtml,'브랜드 점검표');
}
function brFilter(f){ if(!own(BR_NOTE,f)) return; brSetFilter(f); scrollBox().scrollTo(0,0); }   // 판정 필터 단추 — 목록 맨 위로
function brInfo(){   // (i) 판정 기준 — 펼침만 바꿈(다시 그리지 않음). 목록을 내린 채 열면 패널이 머리 위(화면 밖)에 펼쳐지므로 머리 바로 아래로 올림
  BR_INFO=!BR_INFO; const p=document.getElementById('brInfo'), b=document.getElementById('brInfoBtn'), hd=document.getElementById('brHead');
  if(p) p.hidden=!BR_INFO; if(b) b.setAttribute('aria-expanded',BR_INFO?'true':'false');
  if(BR_INFO&&p&&hd){ const d=p.getBoundingClientRect().top-hd.getBoundingClientRect().bottom-(parseFloat(getComputedStyle(hd).marginBottom)||0); if(d<0) scrollBox().scrollBy(0,d); }
}
function brandBodyHtml(){
  const M=chkModel();
  const lvOf={go:2,wait:1,warn:0}, rows=M.main.filter(r=>BR_FILTER==='all'||r.lv===lvOf[BR_FILTER]), medT=M.med!=null?pctU(M.med):'―', medN=chkMedN();
  // 판정 기준 패널은 자료가 없어도 그림 — 머리의 (i) 단추가 늘 펼칠 것이 있게
  let h=`<section id="brInfo" class="br-info" aria-label="판정 기준"${BR_INFO?'':' hidden'}><p class="bi-t">판정 = 국내 수요 + 매입 조건</p>
    <p><b>국내 수요</b> 네이버 검색 전년 대비가 감시 브랜드 중앙값(${M.med!=null?`${medT}, 검색량 충분한 ${medN}곳 기준`:'자료 수집 전'})보다 10%p 이상 높으면 +1, 낮으면 −1(검색량이 적은 브랜드는 0)</p>
    <p><b>매입 조건</b> 본사 재고 + 본사 발언 + 환율. 재고 증가율이 같은 기간 매출 증가율보다 5%p 이상 높으면 +1(처분 물량 기대), 5%p 이상 낮으면 −1. 할인 물량을 늘린다는 발언이 많으면 +1, 할인·공급을 줄인다는 발언이 많으면 −1. 원산지 통화가 1년 평균(없으면 1년 전)보다 5% 이상 싸면 +1, 10% 이상 싸면 +2, 비싸면 같은 폭으로 −1·−2</p>
    <p><b>판정</b> 수요가 약하지 않고 매입 조건 +2 이상이면 지금 검토. 수요가 약하고 매입 조건 +1 이하이거나, 매입 조건이 −1 이하면 주의. 나머지는 관망</p>
    <p class="bi-s">본사 재고는 브랜드가 아니라 본사 전체 기준 · 본사 발언 신호는 매주 공시 추출 때 Claude가 분류 · 본사 재고·발언 자료가 둘 다 없으면 판정하지 않음 · 다음 세일·뉴스는 참고</p></section>`;
  if(!M.main.length&&!M.rest.length) return h+`<p class="br-empty">네이버 검색 자료 수집 전 — 다음 갱신 후 표시</p>`;
  h+=`<p class="br-fnote">${BR_NOTE[BR_FILTER]}</p>`;
  if(!M.main.length) h+=`<p class="br-empty">판정할 브랜드 없음 — 본사 재고·발언 자료 수집 전${BR_FILTER==='all'&&M.rest.length?` · 아래 판정 안 함 ${M.rest.length}곳은 검색·환율만`:''}</p>`;
  else h+=rows.length?`<section class="br-list" aria-label="판정 목록">${rows.map(brRowHtml).join('')}</section>`:`<p class="br-empty">이 판정에 해당하는 브랜드가 없습니다</p>`;
  if(BR_FILTER==='all'&&M.rest.length) h+=brRestHtml(M);
  // 맺음: 점검표 중앙값(검색량 충분한 N곳)과 시장 › 국내 네이버 카드 중앙값(전체)이 다른 이유를 밝힘 · 같은 본사를 쓰는 브랜드 묶음은 자동
  const grp={}; nvAll().filter(b=>b.group==='global').forEach(b=>{ const r=M.main.find(o=>o.b===b); if(r&&r.x) (grp[r.x.ticker]=grp[r.x.ticker]||{hq:chkHq(r),bs:[]}).bs.push(b.name); });
  const same=Object.values(grp).filter(g=>g.bs.length>1).map(g=>`${g.bs.join('·')} = ${g.hq}`);
  h+=`<p class="br-foot">검색은 네이버 전년 대비, 감시 브랜드 중앙값 ${medT}(검색량 충분한 ${medN}곳). 본사 재고는 본사 전체 기준${same.length?`(${esc(same.join(', '))})`:''}.</p>`;
  h+=`<button type="button" class="br-link" data-go="mk:map">지역별로 보기 › 소싱 지도</button>`;
  return h;
}
function brRowHtml(r){   // 압축 행: 이름·본사·통화·배지 / 한 줄 이유 / 점수 4칸 — 누르면 브랜드 상세(이름은 data 속성: 따옴표 안전)
  return `<button type="button" class="br-row" data-brand="${esc(r.b.name)}"><span class="br-m">
    <span class="br-l1"><span class="br-nm"><span class="br-name">${esc(r.b.name)}</span><span class="br-hq">본사 ${esc(chkHq(r))} · ${esc(chkCurKo(r))}</span>${chgTag(r.b.name)}${staleA(r.x&&r.x.stale_since)}${pendA(r.inv&&r.inv.pend)}</span>${vbadge(r.lv)}</span>
    <span class="br-why">${nb(esc(chkWhy(r).short))}</span>
    <span class="br-cells">${chkCells(r).map(c=>`<span class="br-c">${c.k}<b class="sc-${c.tone}">${c.v}</b></span>`).join('')}</span></span>${ic('right',20,'s2 chev')}</button>`;
}
function brRestHtml(M){   // 판정 안 함(본사 재고·발언 자료 없음) — 접힘, 검색 강한 순(rest 정렬 그대로)
  const k=M.rest.filter(r=>r.dem.pt>0).length, byCur={};
  M.rest.forEach(r=>{ if(r.cur) (byCur[r.cur]=byCur[r.cur]||[]).push(r); });
  const curs=Object.keys(byCur).sort((a,c)=>byCur[c].length-byCur[a].length);
  const curTxt=curs.map((c,j)=>{ const f=chkFx(c), nm=c==='JPY'?'엔':(f.name||c);
    return `${nm}${j?'':' 원산지'} ${byCur[c].length}곳 — ${f.na?'환율 자료 없음':`${f.basis==='avg'?'1년 평균':'1년 전'}보다 ${p1(f.v)}% ${f.v<0?'쌈':'비쌈'}`}`; }).join(' · ');
  const rows=M.rest.map(r=>{ const d=r.dem, sub=(CHK_CUR_NOTE[r.b.name]||(r.cur?`${chkCurKo(r)} 원산지`:'원산지 통화 미지정'))+(r.b.low?' · 검색량 적음':'');
    return `<button type="button" class="br-rest-row" data-brand="${esc(r.b.name)}"><span class="tt"><span class="t">${esc(r.b.name)}${chgTag(r.b.name)}</span><span class="s">${esc(sub)}</span></span>`
      +`<span class="y">검색 <b class="${d.pt>0?'sc-p':d.pt<0?'sc-n':'sc-tx'}">${r.b.yoy!=null?pctU(r.b.yoy):'―'}</b></span></button>`; }).join('');
  return `<details id="brRest" class="br-rest"${BR_REST?' open':''} ontoggle="BR_REST=this.open"><summary><span class="tt"><span class="t">판정 안 함 ${M.rest.length}곳</span>`
    +`<span class="s">본사 자료가 없어 검색·환율만 참고${k?` · 검색 강함 ${k}곳`:''}</span></span>${ic('down',20,'s2')}</summary>`
    +`<div class="br-rest-in">${rows}${curTxt?`<p class="br-rest-cur">${esc(curTxt)}</p>`:''}</div></details>`;
}
/* ── v33 A안 S2: 브랜드 상세(A3) — 판정·한 문장 이유·타일 2칸 → 판단 근거 4장(판정 안 함 2장) → 다음 일정 → 최근 뉴스 → 본사 기업 상세 ── */
function brDetailHtml(d){
  const T=d.tiles, judged=d.lv!=null;
  const ptB=e=>`<span class="bd-pt${e.tone?' '+e.tone:''}">${e.score!==''?`<b>${esc(e.score)}</b>`:''}${esc(e.word)}</span>`;
  const SIGT={more:'할인 물량↑',less:'할인·공급↓',neutral:'중립'};
  let h=`<div class="bd"><section class="bd-top" aria-label="판정"><div class="bd-vr">${vbadge(d.lv,true)}<span class="bd-meta">${esc(d.meta)}</span></div>${d.hist?`<p class="bd-chg">${esc(d.hist)}</p>`:''}
    <h2 class="bd-head">${esc(d.head)}</h2><p class="bd-say">${esc(d.say)}</p>
    <div class="bd-tiles"><div class="bd-tile"><span class="tl">국내 수요</span><span class="tv">${esc(T.dem.v)}</span><span class="tc">${nb(esc(T.dem.cap))}</span></div>
    <div class="bd-tile${T.buy.ring?' '+T.buy.ring:''}"><span class="tl">매입 조건</span><span class="tv">${esc(T.buy.v)}</span><span class="tc">${nb(esc(T.buy.cap))}</span></div></div></section>`;
  h+=`<section class="bd-sec" aria-labelledby="bdEvH"><h2 id="bdEvH">${judged?'판단 근거 4가지':'참고 근거 2가지'}</h2><div class="bd-evs">`;
  d.ev.forEach(e=>{
    h+=`<div class="bd-ev" data-ev="${e.id}"><div class="bd-ev-hd"><span class="bd-ev-l">${esc(e.label)}</span>${ptB(e)}</div><p class="bd-ev-v">${nb(esc(e.value))}${e.tags||''}</p><p class="bd-ev-x">${esc(e.explain)}</p>`;
    if(e.spark){ const S=e.spark; h+=`<div class="bd-sp"><span class="cap">최근 8주 검색 지수</span>${spark8(S.vals,S.wk)}<div class="ends"><span>첫 주(${nvWk(S.wk[0])}) ${S.vals[0].toFixed(1)}</span><b>마지막 주(${nvWk(S.wk[7])}) ${S.vals[7].toFixed(1)}</b></div></div>`; }
    if(e.list&&e.list.length) h+=`<div class="bdq">${e.list.map(q=>`<div class="bdq-row"><span class="bdq-t">${esc(MGMT_TOPIC[q.topic]||q.topic||'기타')}</span><div class="bdq-b">${esc(q.ko||'')}<span class="bdq-s${q.sig==='more'||q.sig==='less'?' '+q.sig:''}">${SIGT[q.sig]||'분류 전'}</span>${q.quote?`<details><summary>원문</summary><q>${esc(q.quote)}</q></details>`:''}</div></div>`).join('')}</div>`;
    h+=`</div>`;
  });
  h+=`</div></section><section class="bd-sec" aria-labelledby="bdNxH"><h2 id="bdNxH">다음 일정</h2>`;
  h+=d.next.length?`<div class="bd-next">${d.next.map(n=>{ const inner=`<span class="d">${esc(n.d)}</span><span class="ev-tt"><span class="t">${esc(n.title)}</span><span class="s">${esc(n.sub)}</span></span><span class="kind${n.kind==='세일'?' sale':''}">${n.kind}</span>`;
      return n.go?`<button type="button" class="bd-nx" data-go="${esc(n.go)}">${inner}</button>`:`<div class="bd-nx">${inner}</div>`; }).join('')}</div>`
    :`<p class="bd-none">본사 실적·통화 지역 세일 일정 없음</p>`;
  h+=`</section><section class="bd-sec" aria-labelledby="bdNwH"><h2 id="bdNwH">최근 뉴스</h2><div class="bd-nws">`;
  h+=d.news.length?d.news.map(n=>`<a class="bd-news" href="${esc(safeUrl(n.link))}" target="_blank" rel="noopener"><span class="t">${esc(n.t)}</span><span class="s">${esc(n.meta)}</span></a>`).join('')
    :`<p class="bd-none">최근 14일 중요(★2 이상) 뉴스 없음</p>`;
  if(d.newsAll) h+=`<button type="button" class="bd-link" data-go="news:k:${esc(d.newsAll.key)}"><span class="tt"><span class="t">${esc(d.newsAll.label)} 뉴스 모두 보기</span><span class="s">시장 › 뉴스</span></span>${ic('right',20,'s2 chev')}</button>`;
  h+=`</div></section>`;
  if(d.hqLink) h+=`<button type="button" class="bd-hq" data-go="${esc(d.hqLink.go)}"><span class="tt"><span class="t">${esc(d.hqLink.title)}</span><span class="s">${esc(d.hqLink.sub)}</span></span>${ic('right',20,'s2 chev')}</button>`;
  return h+`</div>`;
}
function renderBrandDetail(name){   // #/brand/<이름> — 판정 9곳·판정 안 함 21곳 모두 같은 틀
  const r=chkFind(name);
  paint('brDetBody',()=>r?brDetailHtml(chkDetail(r)):`<p class="br-empty">점검표에 없는 브랜드</p>`,'브랜드 상세');
}
function buildMore(){   // 메뉴 · 하위 화면(유통사 비교·패션 브랜드·환율·물류·해외직구·수집 상태). 그리다 실패하면 머리 + 안내만(옛 화면이 남지 않게)
  const el=document.getElementById('moreBody'); if(!el) return;
  const head=()=>moreHead(MORE_NAME[MORE_VIEW]||'더보기','');
  paint('moreBody',()=>MORE_VIEW==='peer'?moreHead('유통사 비교','수입 브랜드 유통사 재무 지표 · 연간 · DART 감사보고서(별도) · '+fiRows().length+'곳')+finCardHtml()
    : (MORE_VIEW==='fb'||MORE_VIEW==='ey')?moreFashionHtml()
    : MORE_VIEW==='fx'?moreFxHtml()
    : MORE_VIEW==='logi'?moreLogiHtml()
    : MORE_VIEW==='cb'?moreCbHtml()
    : MORE_VIEW==='status'?moreHead('수집 상태','열람 시점 기준 지연 판정 · 화면 갱신 <span class="nw">'+esc(DATA.generated_at||'―')+'</span> · 출처 Yahoo·SEC·DART·KOSIS')+statusCard()+claudeCard()
    : moreMenuHtml(),'더보기',MORE_VIEW?head:()=>`<div class="phead"><h1>더보기</h1></div><nav class="mmenu" aria-label="더보기 화면">${themeRowHtml()}</nav>`);
}
function moreOpen(v){ if(v==null) goBack({tab:'more'}); else goMore(v); }   // v33 메뉴 줄 · '‹ 뒤로'(바로 전 화면, 없으면 메뉴)
function goMore(v){ go(v==='check'?{tab:'brand'}:{tab:'more',view:v}); }   // v33 기록 1개(sw+moreOpen 따로 부르지 않음). 옛 'check' = 브랜드 탭, 'ey' = 'fb'

/* ── v33 A안: 이동 경로 — 화면 상태 {tab, chip?, view?, id?} 하나를 go()로 그림 ──
   주소: 오늘 = 해시 없음 · #/brand · #/brand/<브랜드> · #/market/<칩> · #/market/co/<티커> · #/more · #/more/<화면>
   기록: 화면 이동(탭·상세·더보기 화면·다른 탭으로 건너뛰기) = pushState · 시장 칩 전환·같은 주소 = replaceState ·
   필터·정렬·펼치기 = 기록 없음. 떠나기 직전 지금 기록에 스크롤·열린 패널 저장 → 뒤로(popstate) 오면 그대로 복원.
   depth = 앱 안에서 쌓은 기록 수 — '‹ 뒤로'는 depth>0이면 history.back(), 주소로 바로 열었으면(0) 부모 화면으로 바꿔 끼움 */
const TABS=['today','brand','market','more'];
const MK_CHIPS=[['news','뉴스'],['cal','캘린더'],['sig','실적·재고'],['co','기업'],['kr','국내'],['map','소싱 지도']];
const MK_NAME=Object.fromEntries(MK_CHIPS);
const own=(o,k)=>k!=null&&Object.prototype.hasOwnProperty.call(o,k);   // 이름표는 자기 키만 — 주소의 'constructor'·'toString'·'__proto__'를 칩·화면으로 받지 않게
const MORE_VIEWS=['peer','fb','fx','logi','cb','status'];   // 'ey'는 'fb' 별칭, 'check'(옛 점검표)는 브랜드 탭
let ROUTE={tab:'today',depth:0}, MK_CHIP='news', MORE_SHOWN, DET_SHOWN=null, BR_SHOWN=null;
// v33 기록마다 열쇠(k) — 휴대폰 뒤로로 떠난 화면은 그 기록을 고칠 수 없어(popstate 뒤) 스크롤을 메모리에 둠 → 앞으로 가기로 오면 그 자리
let KEY_N=0; const newKey=()=>Date.now().toString(36)+Math.random().toString(36).slice(2,6)+(++KEY_N), SCROLL_MEM={};
const scrollBox=()=>document.getElementById('content');
const setText=(id,t)=>{ const el=document.getElementById(id); if(el) el.textContent=t; };
function hPush(st,url){ try{ history.pushState(st,'',url==null?location.href:url); return true; }catch(e){ return false; } }   // 파일로 열기 등 기록을 못 쓰는 곳에서도 화면은 그대로 바뀜
function hRep(st,url){ try{ history.replaceState(st,'',url==null?location.href:url); return true; }catch(e){ return false; } }
// renderDetail은 모르는 티커에서 오류 → 부모로. 국내 법인(krd:)은 네이버 줄이 가리키는 곳이면 자료가 아직 없어도 상세('미확인')를 엶(옛 동작 — 예: 다음 DART 수집 전 스케쳐스코리아)
const coKnown=t=>String(t).startsWith('krd:')?(((KRD&&KRD.entities)||[]).some(e=>'krd:'+e.id===t)||nvAll().some(b=>b.link===t)):DATA.items.some(i=>i.ticker===t);
function brKnown(n){ try{ const M=chkModel(); return M.main.concat(M.rest).some(r=>r.b.name===n); }catch(e){ return false; } }
function brJudged(n){ try{ return chkModel().main.some(r=>r.b.name===n); }catch(e){ return false; } }   // 판정 대상(판정 안 함 제외)
const nfKnown=f=>f==='all'||/^k:./.test(f)||NEWS_FILTERS.some(x=>!x.sep&&x.id===f);
function normRoute(r){   // 모르는 탭·칩·기업·브랜드·화면은 오류 없이 부모로
  r=r||{};
  const o={tab:TABS.includes(r.tab)?r.tab:'today'}, id=(r.id==null||r.id==='')?null:String(r.id);
  if(r.tab&&o.tab!==r.tab) console.warn('모르는 화면 → 오늘:',r.tab);
  if(o.tab==='market'){
    o.chip=own(MK_NAME,r.chip)?r.chip:(id&&!r.chip?'co':MK_CHIP);
    if(r.chip&&!own(MK_NAME,r.chip)) console.warn('모르는 시장 칩:',r.chip);
    if(o.chip==='co'&&id){ if(coKnown(id)) o.id=id; else console.warn('모르는 기업 → 기업 목록:',id); }
    if(o.chip==='news'&&r.nf!=null&&nfKnown(r.nf)) o.nf=r.nf;
    if(o.chip==='news'&&typeof r.nq==='string') o.nq=nsQ(r.nq);   // v33.1 검색어 · 펼친 검색 결과 수
    if(o.chip==='news'&&Number.isInteger(r.ns)&&r.ns>0) o.ns=Math.min(r.ns,3000);
  } else if(o.tab==='brand'){
    if(id){ if(brKnown(id)) o.id=id; else console.warn('모르는 브랜드 → 점검표:',id); }
  } else if(o.tab==='more'){
    const v=r.view==='ey'?'fb':r.view;
    if(v==='check') return {tab:'brand'};
    if(MORE_VIEWS.includes(v)) o.view=v; else if(v) console.warn('모르는 더보기 화면 → 메뉴:',v);
  }
  return o;
}
// 기록에 저장한 스크롤·패널(+패널 안 스크롤)·뒤로 라벨·바로 아래 기록의 화면(fromKey)은 그대로
const withMeta=(o,st)=>({...o,depth:st.depth||0,from:st.from,fromKey:st.fromKey,scroll:st.scroll,sheet:st.sheet,sheetY:st.sheetY,k:st.k});
function routeOfHash(h){
  const s=String(h||'').replace(/^#/,'');
  if(!s.startsWith('/')) return normRoute({tab:'today'});
  const p=s.slice(1).split('/').map(x=>{ try{ return decodeURIComponent(x); }catch(e){ return x; } });
  if(p[0]==='market') return normRoute({tab:'market',chip:p[1]||MK_CHIP,id:p[1]==='co'?p[2]:null});
  if(p[0]==='brand') return normRoute({tab:'brand',id:p[1]});
  if(p[0]==='more') return normRoute({tab:'more',view:p[1]});
  return normRoute({tab:p[0]||'today'});
}
function hashOf(r){   // 이름·티커는 encodeURIComponent — '#/' 접두어라 요소 id와 겹치지 않음
  const e=encodeURIComponent;
  if(r.tab==='brand') return '#/brand'+(r.id?'/'+e(r.id):'');
  if(r.tab==='market') return '#/market/'+r.chip+(r.chip==='co'&&r.id?'/'+e(r.id):'');
  if(r.tab==='more') return '#/more'+(r.view?'/'+r.view:'');
  return location.href.split('#')[0];   // 오늘 = 해시 없음
}
function coName(t){   // 뒤로 라벨·상세 머리 제목용 — 괄호 앞 이름만(본문 머리엔 전체 이름)
  t=String(t);
  if(t.startsWith('krd:')){ const e=((KRD&&KRD.entities)||[]).find(z=>'krd:'+z.id===t); return e?nmSplit(e.name).main:t; }
  const x=DATA.items.find(i=>i.ticker===t); return x?nmSplit(x.name).main:t;
}
function labelOf(r){   // '‹ 뒤로'에 붙는 화면 이름
  if(!r) return '';
  if(r.tab==='brand') return r.id||'점검표';
  if(r.tab==='market') return r.id?coName(r.id):(r.chip==='co'?'기업 목록':(own(MK_NAME,r.chip)?MK_NAME[r.chip]:'시장'));
  if(r.tab==='more') return own(MORE_NAME,r.view)?MORE_NAME[r.view]:'더보기';
  return '오늘';
}
const backLbl=(st,parent)=>(st&&st.depth>0&&st.from)?st.from:parent;   // 바로 전 화면 이름, 앱 안 전 화면이 없으면 부모
const scrKey=r=>[r.tab,r.tab==='market'?r.chip:'',r.view||'',r.id||''].join('|');   // 같은 화면인지(스크롤·패널 제외)
function go(r,opt){   // 화면 이동 하나 = 기록(push/replace) + 그리기
  opt=opt||{};
  nsFlush();   // v33.1 0.2초 안 검색 입력을 떠나는 기록에 먼저 반영
  if(BACK_REQ&&Date.now()-BACK_REQ<1500){ goAfterBack(r,opt); return; }   // v33 S2: 뒤로가 아직 도착 전이면 도착 뒤 이어서(누른 이동이 사라지지 않게)
  const st=normRoute(r), cur=history.state||{}, same=scrKey(st)===scrKey(ROUTE);
  const sheet=SRC_SHEET||LAST_SHEET||null, shY=SRC_SHEET?sheetScrollY():(LAST_SHEET?LAST_SHEET_Y:0); LAST_SHEET=null;
  if(opt.replace||(same&&!SRC_SHEET)){   // 시장 칩 전환·같은 주소 다시 들어오기 = 바꿔 끼움
    st.depth=cur.depth||0; st.from=cur.from; st.fromKey=cur.fromKey; st.k=cur.k||newKey();
    hRep(st,hashOf(st));
  } else {
    const lk=cur.k||ROUTE.k;   // 패널이 열려 있으면 패널 기록 키 — 뒤로 오면 패널 안 누른 줄로
    if(lk){ SCROLL_MEM[lk]=scrollBox().scrollTop; focusRemember(lk); }
    // 떠나기 직전 지금 기록에 스크롤·열린 패널(+패널 안 스크롤)·뉴스 필터 저장 — 뒤로 오면 그대로 복원
    hRep({...ROUTE,...cur,scroll:scrollBox().scrollTop,sheet,sheetY:sheet?shY:0,...(ROUTE.tab==='market'&&ROUTE.chip==='news'?{nf:newsFilter,nq:NEWS_Q,ns:NS_SHOW}:{})});
    st.depth=(cur.depth||0)+1; st.from=labelOf(ROUTE); st.fromKey=scrKey(ROUTE); st.k=newKey();   // fromKey = 바로 아래 기록의 화면(칩으로 그 화면에 갈 때 뒤로 처리)
    hPush(st,hashOf(st));
  }
  render(st,false);
}
/* history.back()은 popstate가 올 때까지(보통 수십 ms) 기록이 그대로 — 그사이 '‹ 뒤로'를 한 번 더 누르면 두 화면 뒤로 감.
   우리가 부른 뒤로가 아직 도착하지 않았으면 이번 누름은 무시(popstate가 안 오면 1.5초 뒤 풀림). want = 도착해야 할 화면(칩으로 뒤로 간 경우) */
let BACK_REQ=0, BACK_WANT=null, GO_NEXT=null;
function goAfterBack(r,opt){ GO_NEXT=[r,opt]; setTimeout(()=>{ if(GO_NEXT&&!(BACK_REQ&&Date.now()-BACK_REQ<1500)){ const [a,o]=GO_NEXT; GO_NEXT=null; go(a,o); } },1600); }   // popstate가 끝내 안 오면 1.6초 뒤 실행
function histBack(want){
  if(BACK_REQ&&Date.now()-BACK_REQ<1500) return true;
  BACK_REQ=Date.now(); BACK_WANT=want||null;
  try{ history.back(); return true; }catch(e){ BACK_REQ=0; BACK_WANT=null; return false; }
}
function goBack(parent){   // 화면 '‹ 뒤로' = 휴대폰 뒤로. 주소로 바로 열어 앱 안 전 화면이 없으면(depth 0) 부모 화면으로 바꿔 끼움
  const s=history.state;
  if(s&&s.depth>0&&histBack()) return;
  go(parent,{replace:true});
}
function render(st,restore,init){   // st = 기록에 든 화면 상태 · restore = 뒤로·앞으로 왔을 때(스크롤·패널 복원) · init = navInit
  if(WF_DEFER) wfSwap(1);   // v33 글꼴을 미뤄 뒀으면 화면을 바꾸는 지금(새 화면을 Plex로 그림 — 밀림 없음)
  ROUTE=st;
  closeSheetRaw();
  const root=st.tab==='market'?!st.id:(st.tab==='today'||(!st.id&&!st.view));   // 탭 첫 화면이면 aria-current=page, 그 아래 화면이면 true
  document.querySelectorAll('nav.tabs .tab').forEach(b=>{ const on=b.dataset.p===st.tab; b.classList.toggle('on',on);   // 하단 탭 강조 = 화면의 집(기업 상세 → 시장)
    if(on) b.setAttribute('aria-current',root?'page':'true'); else b.removeAttribute('aria-current'); });
  document.querySelectorAll('.pane').forEach(x=>x.classList.toggle('on',x.id==='p-'+st.tab));
  if(st.tab==='today') safe(buildToday,'오늘','p-today');   // v33 S2: 오늘은 열 때마다 다시 그림(지연 판정·D-day는 열람 시점, 몇 ms)
  else if(st.tab==='brand') renderBrand(st);
  else if(st.tab==='market') renderMarket(st);
  else if(st.tab==='more') renderMore(st);
  const mem=restore&&st.k?SCROLL_MEM[st.k]:null;   // 메모리(떠날 때 스크롤)가 기록에 든 값보다 새것
  scrollSet(restore?(mem!=null?mem:(st.scroll||0)):0,init&&!restore);
  NS_RESTORE=(restore&&st.tab==='market'&&st.chip==='news'&&NEWS_Q&&NS_ST==='loading')?{k:st.k,y:mem!=null?mem:(st.scroll||0)}:null;   // v33.1 보관 기사가 오면 이 자리로 다시(그전엔 결과가 짧아 스크롤이 잘림)
  if(restore&&st.sheet){ openSheet(st.sheet,true); sheetScrollTo(st.sheetY); }   // 패널에서 기업을 열었다 돌아오면 같은 패널을 같은 자리로 다시
  phSoon();
  try{ document.title=st.tab==='today'?'스포츠 산업 모니터':labelOf(st)+' · 스포츠 산업 모니터'; }catch(e){}
  if(!init) focusAfter(st,restore);
}
/* v33 키보드: 화면을 바꾼 뒤 초점이 사라졌으면 — 뒤로 = 떠날 때 누른 줄, 앞으로 = 새 화면 제목. 마지막 입력이 키보드일 때만(KB_LAST) · 입력 칸 제외 */
let KB_LAST=false, FOCUS_MEM={}, SHEET_FOCUS=null;
document.addEventListener('pointerdown',()=>{ KB_LAST=false; },true);
document.addEventListener('keydown',e=>{ if(!e.isComposing&&!/^(Shift|Control|Alt|Meta)$/.test(e.key)) KB_LAST=true; },true);
const focusLost=()=>{ const a=document.activeElement; return !a||a===document.body||a===document.documentElement||!a.isConnected||!a.getClientRects().length||!!(a.closest&&a.closest('[inert]')); };
function focusDesc(el){   // 다시 찾을 단서 — data-go·data-brand·data-k·onclick·글자·같은 모양 순번
  if(!el||el===document.body||!el.closest||!el.closest('#content,#sheet')||el.matches('input,textarea,select')) return null;
  const key=x=>x.tagName.toLowerCase()+[...x.classList].filter(c=>!/^(on|off|open|sel|flash)$/.test(c)).map(c=>'.'+CSS.escape(c)).join('');
  const box=el.closest('#sheet')?document.getElementById('sheet'):el.closest('.pane'); if(!box) return null;
  const sig=key(el), same=[...box.querySelectorAll(sig)];
  return {sheet:!!el.closest('#sheet'), id:el.id||'', go:el.getAttribute('data-go')||'', brand:el.getAttribute('data-brand')||'', k:el.getAttribute('data-k')||'',
    oc:el.getAttribute('onclick')||'', tx:(el.textContent||'').trim().slice(0,60), sig, i:same.indexOf(el)};
}
function focusRemember(k){ const a=document.activeElement, d=focusDesc(a)||(focusLost()&&SHEET_FOCUS)||null; SHEET_FOCUS=null; if(d) FOCUS_MEM[k]=d; else delete FOCUS_MEM[k]; }
function focusFind(d){
  if(!d) return null;
  const box=d.sheet?document.getElementById('sheet'):document.querySelector('.pane.on'); if(!box) return null;
  const vis=x=>x&&x.getClientRects().length&&!x.closest('[inert]')?x:null, q=a=>vis(box.querySelector(a));
  const att=(n,v)=>{ if(!v) return null; const L=[...box.querySelectorAll(`[${n}="${CSS.escape(v)}"]`)].filter(x=>vis(x));   // 같은 목적지 단추가 여럿이면 누른 단추 글자로
    return L.length===1?L[0]:(L.find(x=>(x.textContent||'').trim().slice(0,60)===d.tx)||null); };
  let el=(d.id&&vis(document.getElementById(d.id))&&box.contains(document.getElementById(d.id))?document.getElementById(d.id):null)||att('data-go',d.go)||att('data-brand',d.brand)||att('data-k',d.k)||att('onclick',d.oc);
  if(!el){ const same=[...box.querySelectorAll(d.sig)].filter(x=>vis(x)); el=same.find(x=>(x.textContent||'').trim().slice(0,60)===d.tx)||same[Math.min(Math.max(d.i,0),same.length-1)]||null; }
  return el;
}
function focusHead(st){   // 새 화면 제목(tabindex -1) — 시장 칩 화면은 고른 칩, 패널이 열려 있으면 패널 닫기 단추
  if(SRC_SHEET) return document.querySelector('#sheet .sh-x');
  if(st.tab==='market'&&!st.id) return document.querySelector('#mkChips .mk-chip.on');
  const h=st.tab==='market'?document.getElementById('coTitle'):(st.tab==='brand'&&st.id)?document.getElementById('brTitle'):document.querySelector('.pane.on .phead h1');
  if(h&&!h.hasAttribute('tabindex')) h.setAttribute('tabindex','-1');
  return h;
}
function focusAfter(st,restore){
  if(!KB_LAST||!focusLost()) return;
  const el=(restore&&focusFind(FOCUS_MEM[st.k]))||focusHead(st);
  if(el&&el.getClientRects().length) try{ el.focus({preventScroll:true}); }catch(e){}
}
/* v33 S2: 화면을 바꾼 뒤 스크롤 — 부드러운 스크롤(focusCard·탭 다시 누름)이 도는 중에 화면이 바뀌면 남은 한 걸음이 복원 위치를 밀어냄(예: 300 → 335).
   다음 프레임에 한 번 더 맞춤. focusCard는 새로 부드럽게 스크롤하기 전에 이 예약을 취소. lazy(처음 열 때, 이미 0) = 스크립트 안 레이아웃 강제 없이 다음 프레임 확인만 */
let SCROLL_RAF=0;
function scrollSet(y,lazy){
  const b=scrollBox(); if(!lazy) b.scrollTo(0,y); cancelAnimationFrame(SCROLL_RAF);
  SCROLL_RAF=requestAnimationFrame(()=>{ SCROLL_RAF=0; if(Math.abs(b.scrollTop-y)>1) b.scrollTo(0,y); });
}
/* v33 S2: #content scroll-padding-top = 보이는 고정 머리(.phead) 높이 + 8px — 키보드 초점·scrollIntoView가 머리 밑에 숨지 않게.
   화면을 바꾼 다음 프레임·머리 크기가 바뀔 때 잼. 시장 탭은 고정 칩 줄(44px)도 */
let PH_RAF=0;
function phSync(){
  if(PH_RAF){ cancelAnimationFrame(PH_RAF); PH_RAF=0; } const c=scrollBox(); if(!c) return; let h=0;
  document.querySelectorAll('.pane.on .phead,.pane.on .mk-chips').forEach(e=>{ h=Math.max(h,e.offsetHeight); });
  const v=h?(h+8)+'px':''; if(c.style.scrollPaddingTop!==v) c.style.scrollPaddingTop=v;
}
function phSoon(){ if(!PH_RAF) PH_RAF=requestAnimationFrame(phSync); }
try{ const ro=new ResizeObserver(phSoon); ['tdHead','brHead'].forEach(id=>{ const e=document.getElementById(id); if(e) ro.observe(e); }); }catch(e){}
window.addEventListener('resize',phSoon);
function renderBrand(st){
  if(BR_DAY&&BR_DAY!==kstToday()){ BR_SHOWN=null; safe(buildBrand,'브랜드 점검표','brandBody'); }   // v33.2 자정이 지나면 목록·상세를 다시(꼬리표 '어제'·'오늘' → 날짜)
  const d=!!st.id, bl=document.getElementById('brandList'), bd=document.getElementById('brandDetail');
  if(bl) bl.style.display=d?'none':''; if(bd) bd.style.display=d?'':'none';
  if(!d) return;
  if(BR_SHOWN!==st.id){ BR_SHOWN=st.id; setText('brTitle',st.id); renderBrandDetail(st.id); }   // 목록(필터·펼침·스크롤)은 그대로 두고 상세만 그림
  backLabel('brBack','brBackLbl',backLbl(st,'점검표'));
}
function backLabel(btn,span,lb){   // v33 S2: 상세 머리 '‹ 바로 전 화면' 글자 + 화면 읽기 이름('…로 돌아가기')
  setText(span,lb); const b=document.getElementById(btn); if(b) b.setAttribute('aria-label',jo(lb,'으로','로',1)+' 돌아가기');
}
function renderMarket(st){
  MK_CHIP=st.chip;
  { const pm=document.getElementById('p-market'); if(pm) pm.classList.toggle('det',st.chip==='co'&&!!st.id); }   // v33 S2: 기업 상세 = 칩 줄 대신 상세 머리
  document.querySelectorAll('#mkChips .mk-chip').forEach(b=>{ const on=b.dataset.c===st.chip; b.classList.toggle('on',on); b.setAttribute('aria-pressed',on?'true':'false'); });
  document.querySelectorAll('#p-market .mk').forEach(x=>x.classList.toggle('on',x.id==='mk-'+st.chip));
  if(st.chip==='news'){   // 뉴스는 칩이 처음 보일 때 한 번만 그림(v32.11) — 필터가 바뀌어 온 경우만 다시
    // 'k:'(회사·브랜드 하나) 필터는 그 기록(nf)에만 — nf 없이 들어오면(칩·하단 탭·sw) 기본 보기로(map_nav 7.8). 칩에서 고른 필터는 그대로
    const nf=st.nf!=null?st.nf:(String(newsFilter).startsWith('k:')?'all':newsFilter);
    // v33.1 검색어: '뒤로'로 떠날 때 못 넣은 입력(NQ_MEM) > 기록(nq — 뒤로·앞으로·새로고침, goNews는 '') > 없으면(칩·하단 탭) 그대로
    const nq=own(NQ_MEM,st.k)?NQ_MEM[st.k]:(st.nq!=null?st.nq:NEWS_Q), qc=nq!==NEWS_Q;
    if(st.k) delete NQ_MEM[st.k];
    if(qc){ NEWS_Q=nq; NS_SHOW=(st.nq===nq&&st.ns>0)?st.ns:NS_PAGE; const i=document.getElementById('newsSearch'); if(i) i.value=nq; if(nq) nsLoad(); }
    if(nf!==newsFilter){ newsFilter=nf; if(!qc) NS_SHOW=NS_PAGE; safe(buildNewsChips,'뉴스 칩','mk-news'); safe(buildNews,'뉴스','mk-news'); }
    else if(!NEWS_BUILT||qc) safe(buildNews,'뉴스','mk-news');
    { const s=history.state; if(s&&s.tab==='market'&&s.chip==='news'&&(s.nf!==newsFilter||s.nq!==NEWS_Q||s.ns!==NS_SHOW)) hRep({...s,nf:newsFilter,nq:NEWS_Q,ns:NS_SHOW}); }   // 보이는 필터·검색어를 이 기록에(칩 전환 뒤 새로고침에도 그대로)
  } else if(st.chip==='kr') safe(hcDraw,'의류 소매 그래프','mk-kr');   // 숨은 칩에서 그리면 폭 0 → 보일 때 그림
  else if(st.chip==='co'){
    if(!st.id){ showCoList(); return; }
    document.getElementById('coList').style.display='none'; document.getElementById('coDetail').style.display='';
    if(DET_SHOWN!==st.id){ DET_SHOWN=st.id; setText('coTitle',coName(st.id)); safe(()=>{ document.getElementById('detBody').innerHTML=''; renderDetail(st.id); },'기업 상세','detBody'); }
    backLabel('coBack','coBackLbl',backLbl(st,'기업 목록'));
  }
}
function renderMore(st){
  const v=st.view||null;
  if(MORE_SHOWN!==v){ MORE_SHOWN=v; MORE_VIEW=v; safe(buildMore,'더보기','moreBody'); }
  const lb=backLbl(st,'더보기');
  document.querySelectorAll('#moreBody .mback').forEach(b=>{ const t=b.querySelector('.hd-bl'); if(t) t.textContent=lb; b.setAttribute('aria-label',jo(lb,'으로','로',1)+' 돌아가기'); });
}
function onHistory(){   // 뒤로·앞으로(popstate)·주소창에서 해시를 바꾼 경우(hashchange)
  const want=(BACK_REQ&&Date.now()-BACK_REQ<1500)?BACK_WANT:null; BACK_REQ=0; BACK_WANT=null;   // 우리가 부른 뒤로가 도착 — 다시 누를 수 있음
  if(ROUTE.k){ SCROLL_MEM[ROUTE.k]=scrollBox().scrollTop; focusRemember(ROUTE.k); }   // 떠나는 화면의 스크롤·초점(앞으로 가기로 돌아올 때)
  if(NS_T){ clearTimeout(NS_T); NS_T=0; const i=document.getElementById('newsSearch'); if(i&&ROUTE.k) NQ_MEM[ROUTE.k]=nsQ(i.value); }   // v33.1 0.2초 안에 '뒤로' — 못 넣은 검색 입력은 떠나는 기록 몫(앞으로 오면 그대로)
  let st=history.state;
  if(!st||!st.tab){ st={...routeOfHash(location.hash),depth:(ROUTE.depth||0)+1,from:labelOf(ROUTE),fromKey:scrKey(ROUTE),k:newKey()}; hRep(st,hashOf(st)); }   // 주소창에서 바꾼 해시 — 모르는 값은 부모로, 주소도 정리
  else st=withMeta(normRoute(st),st);   // 기록에 든 기업·브랜드가 데이터에서 빠졌으면 부모로
  if(scrKey(st)===scrKey(ROUTE)){   // 같은 화면(패널 기록) — 패널만 열고 닫음
    ROUTE=st;
    if(st.sheet){ if(SRC_SHEET!==st.sheet){ openSheet(st.sheet,true); sheetScrollTo(st.sheetY); } }
    else if(SRC_SHEET){ const f=SHEET_FROM; SHEET_FROM=null; closeSheetRaw(); if(KB_LAST&&f&&f.isConnected&&f.getClientRects().length) try{ f.focus({preventScroll:true}); }catch(e){} }   // 뒤로로 닫아도 연 단추로 초점
    else if(st.scroll!=null) scrollBox().scrollTo(0,st.scroll);   // 같은 화면 기록이 이어진 드문 경우라도 그 기록의 스크롤로
  } else render(st,true);
  if(want&&scrKey(ROUTE)!==scrKey(want)) go(want,{replace:ROUTE.tab==='market'});   // 칩으로 뒤로 갔는데 다른 화면에 닿으면(앞으로 가기 뒤 등) 그 칩으로
  if(GO_NEXT){ const [a,o]=GO_NEXT; GO_NEXT=null; go(a,o); }   // v33 S2: 뒤로 도착 전에 누른 이동
}
window.addEventListener('popstate',onHistory);
window.addEventListener('hashchange',()=>{ if(scrKey(routeOfHash(location.hash))!==scrKey(ROUTE)) onHistory(); });
function sheetPush(kind){   // 하단 패널 = 기록 1개(휴대폰 뒤로로 닫힘). 이미 패널 기록이면 바꿔 끼움
  const s=history.state||{};
  if(s.sheet){ hRep({...s,sheet:kind,sheetY:0}); return; }
  hRep({...ROUTE,...s,scroll:scrollBox().scrollTop,sheet:null,sheetY:0});
  hPush({...ROUTE,...s,scroll:scrollBox().scrollTop,sheet:kind,sheetY:0,depth:(s.depth||0)+1,fromKey:scrKey(ROUTE),k:newKey()});
}
// 옛 함수 이름 호환 — 화면 안 인라인 onclick이 그대로 동작
const LEGACY_P={home:{tab:'today'},today:{tab:'today'},brand:{tab:'brand'},co:{tab:'market',chip:'co'},cal:{tab:'market',chip:'cal'},news:{tab:'market',chip:'news'},kr:{tab:'market',chip:'kr'},more:{tab:'more'}};
function sw(p){   // 'home'→오늘 · 'co'·'cal'·'news'·'kr'→시장 칩 · 'more' · 새 이름(today·brand·market)
  if(p==='market'){ go({tab:'market',chip:MK_CHIP}); return; }
  if(!own(LEGACY_P,p)) console.warn('sw: 모르는 화면 '+p+' → 오늘');
  go(own(LEGACY_P,p)?LEGACY_P[p]:{tab:'today'});
}
function goNews(f){ go({tab:'market',chip:'news',nf:f,nq:''}); }   // 시장 › 뉴스 + 필터('all' · 'k:<뉴스 키>' · 칩 id) — 검색어는 지움(v33.1)
function openBrand(n){ go({tab:'brand',id:n}); }   // 브랜드 상세(S2에서 점검표 줄·오늘 카드가 씀)
const CARD_HOME={warnCard:['market','sig'],srcCard:['market','map'],hcCard:['market','kr'],saleList:['market','cal'],calList:['market','cal'],statusCard:['more','status'],claudeCard:['more','status']};   // 카드 → 그 카드가 있는 화면
function focusCard(id){   // 그 화면으로 간 뒤(칩 그리기 끝난 다음) 카드로 스크롤 + 강조
  const h=own(CARD_HOME,id)?CARD_HOME[id]:null;
  if(!h){ console.warn('focusCard: 카드 위치를 모름 — '+id); return; }
  const r=normRoute(h[0]==='market'?{tab:'market',chip:h[1]}:{tab:'more',view:h[1]});
  if(scrKey(r)!==scrKey(ROUTE)) go(r);
  const el=document.getElementById(id);
  if(!el){ console.warn('focusCard: 카드가 그려지지 않음 — '+id); return; }
  const box=el.closest('.card')||el;
  cancelAnimationFrame(SCROLL_RAF); SCROLL_RAF=0;   // 방금 화면을 바꾼 render의 '한 번 더 맞춤'이 이 스크롤을 끊지 않게
  phSync();   // 방금 바꾼 화면의 머리 높이로 scroll-padding 먼저(다음 프레임 예약을 기다리면 전 화면 값으로 스크롤)
  box.scrollIntoView({behavior:smoothB(),block:'start'});
  box.classList.add('flash'); setTimeout(()=>box.classList.remove('flash'),1600);
}
function calDay(d){   // 오늘 ③ 여러 곳 실적 → 캘린더 그 날 골라 두고 그 달 카드로(달력 밖이면 90일 목록)
  calSel=d; safe(buildCal,'캘린더','mk-cal');
  const c=document.querySelector(`#calGrid .cd[data-day="${CSS.escape(d)}"]`);
  if(!c){ calSel=null; safe(buildCal,'캘린더','mk-cal'); return focusCard('calList'); }
  const r=normRoute({tab:'market',chip:'cal'}); if(scrKey(r)!==scrKey(ROUTE)) go(r);
  cancelAnimationFrame(SCROLL_RAF); SCROLL_RAF=0; phSync();
  (c.closest('.cal')||c).scrollIntoView({behavior:smoothB(),block:'start'});
}
function tabTap(t){   // 하단 탭 = 그 탭의 첫 화면(시장은 마지막으로 본 칩, 기업 칩이면 목록). 이미 첫 화면이면 맨 위로만
  const r=normRoute(t==='market'?{tab:'market',chip:MK_CHIP}:{tab:t});
  if(scrKey(r)===scrKey(ROUTE)){ scrollBox().scrollTo({top:0,behavior:smoothB()}); return; }
  go(r);
}
function mkChip(c){   // 시장 칩 전환 = 기록 바꿔 끼움. 이미 그 칩 첫 화면이면 맨 위로만
  const r=normRoute({tab:'market',chip:c}), k=scrKey(r), s=history.state||{};
  if(k===scrKey(ROUTE)){ scrollBox().scrollTo({top:0,behavior:smoothB()}); return; }
  // 바로 아래 기록이 그 칩 화면이면(상세·KPI·네이버 줄로 건너온 경우) 뒤로 — 바꿔 끼우면 같은 화면 기록 두 개가 이어져 휴대폰 뒤로 한 번이 헛돎. 스크롤도 그 자리로
  if(s.depth>0&&s.fromKey===k&&!SRC_SHEET&&histBack(r)) return;
  go(r,{replace:ROUTE.tab==='market'});
}
function navInit(){   // 처음 열 때 주소 해석(모르는 값은 부모로) → 기록 바꿔 끼움(주소로 열면 depth 0, 새로고침이면 그 기록 그대로) → 그리기
  try{ history.scrollRestoration='manual'; }catch(e){}   // 스크롤 상자가 window가 아니라 #content — 직접 복원
  let st={...routeOfHash(location.hash),depth:0};
  // 새로고침(기록에 같은 화면이 이미 있음): 앱 안 깊이·뒤로 라벨·뉴스 필터·열린 패널은 그대로 — 패널 기록을 패널 없는 depth 0으로 바꾸면
  // 바로 아래 기록과 같은 화면이 되어 휴대폰 뒤로 한 번이 헛돎. 주소로 처음 열면(기록 없음) depth 0
  const hs=history.state, hr=hs&&hs.tab?normRoute(hs):null;
  if(hr&&scrKey(hr)===scrKey(st)) st=withMeta(hr,hs);
  if(!st.k) st.k=newKey();
  hRep(st,hashOf(st));
  render(st,false,true);
  if(st.sheet){ openSheet(st.sheet,true); if(!SRC_SHEET) hRep({...st,sheet:null}); }
}
/* v33 부팅 보호 — 한 영역이 실패해도 나머지는 그리고, 그 자리에 한 줄 남김(같은 영역이 다시 실패해도 줄이 쌓이지 않음) */
const bootErr=name=>`<div class="note boot-err" data-n="${esc(name)}">${ic('alert',16)} 이 영역을 그리지 못했습니다(콘솔 참고) — ${esc(name)}</div>`;
function safe(fn,name,box){
  try{ return fn(); }catch(e){
    console.error('['+name+'] 그리기 실패:',e);
    const el=box&&document.getElementById(box); if(!el) return;
    [...el.querySelectorAll('.boot-err')].forEach(n=>{ if(n.dataset.n===name) n.remove(); });
    el.insertAdjacentHTML('afterbegin',bootErr(name));
  }
}
/* v33 S2: 칸 하나를 통째로 다시 그림 — 실패하면 옛 내용 대신 안내 한 줄(keep = 그래도 남길 머리, 예: 더보기 하위 화면의 뒤로 단추) */
const PANE_OF={tdHead:'p-today',todayCard:'p-today',brHead:'p-brand',brandBody:'p-brand',brDetBody:'p-brand',moreBody:'p-more'};
function paint(id,fn,name,keep){
  const el=document.getElementById(id);
  if(!el){ safe(()=>{ throw new Error('#'+id+' 칸 없음'); },name,PANE_OF[id]); return false; }   // 칸이 빠졌으면 그 탭에 안내 한 줄(나머지 화면은 그대로)
  try{ el.innerHTML=fn(); return true; }
  catch(e){ console.error('['+name+'] 그리기 실패:',e); let k=''; try{ k=keep?keep():''; }catch(_){}
    el.innerHTML=k+bootErr(name); return false; }
}
/* v33 S2: 새 화면 단추의 목적지(data-go) — 'today' · 'brand' · 'brand-all'(필터 '전체'로) · 'brand:<이름>' · 'co:<티커>' · 'more' · 'more:<화면>' · 'news:<필터>' · 'mk:<칩>' · 'mk:<칩>:<카드 id>' · 'mk:cal:day:<YYYY-MM-DD>' */
function goKey(k){
  k=String(k||'');
  if(k==='today'||k==='brand'||k==='more') return go({tab:k});
  if(k==='brand-all'){ if(BR_FILTER!=='all') brSetFilter('all'); return go({tab:'brand'}); }   // 오늘 '점검표 전체 보기' — 전에 고른 필터를 '전체'로(스크롤은 go가 맨 위로)
  if(k.startsWith('brand:')) return openBrand(k.slice(6));
  if(k.startsWith('co:')) return goDetail(k.slice(3));
  if(k.startsWith('more:')) return goMore(k.slice(5));
  if(k.startsWith('news:')) return goNews(k.slice(5));
  if(k.startsWith('mk:')){ const [c,f,v]=k.slice(3).split(':'); if(c==='cal'&&f==='day'&&/^\d{4}-\d{2}-\d{2}$/.test(v||'')) return calDay(v); if(f&&own(CARD_HOME,f)) return focusCard(f); return go({tab:'market',chip:c}); }
  console.warn('goKey: 모르는 목적지 '+k);
}
document.querySelectorAll('nav.tabs .tab').forEach(b=>{ b.onclick=()=>tabTap(b.dataset.p); });
document.querySelectorAll('#mkChips .mk-chip').forEach(b=>{ b.onclick=()=>mkChip(b.dataset.c); });
{ const b=document.getElementById('coBack'); if(b) b.onclick=()=>goBack({tab:'market',chip:'co'}); }
{ const b=document.getElementById('brBack'); if(b) b.onclick=()=>goBack({tab:'brand'}); }
{ const b=document.getElementById('coSearch'); if(b) b.addEventListener('input',e=>{coQuery=e.target.value.trim().toLowerCase();buildCo();}); }
{ const b=document.getElementById('newsSearch'); if(b){   // v33.1 지난 뉴스 검색 — 누르면 보관 파일을 미리 받기 시작, 입력은 0.2초 모아서(한글 조합 중인지 함께)
  b.addEventListener('focus',nsLoad);
  b.addEventListener('input',e=>{ NS_COMP=!!e.isComposing; clearTimeout(NS_T); NS_T=setTimeout(()=>{ NS_T=0; nsSet(b.value,NS_COMP); },200); });
  b.addEventListener('compositionend',()=>{ NS_COMP=false; clearTimeout(NS_T); NS_T=setTimeout(()=>{ NS_T=0; nsSet(b.value,false); },200); });
  b.addEventListener('keydown',e=>{ if(e.key==='Enter'&&!e.isComposing){ clearTimeout(NS_T); NS_T=0; nsSet(b.value,false); if(matchMedia('(pointer:coarse)').matches) b.blur(); } });   // 휴대폰 '검색' = 자판 닫고 결과
} }
['wheel','touchstart','keydown'].forEach(ev=>document.addEventListener(ev,()=>{ NS_RESTORE=null; },{capture:true,passive:true}));   // 직접 움직이면 보관 기사 도착 뒤 스크롤 맞추기 안 함
['newsChips','coChips'].forEach(id=>{ const el=document.getElementById(id); if(el) el.addEventListener('focusin',e=>{ const t=e.target; if(!t||!t.closest||!t.closest('.chip')) return;   // Tab으로 간 칩을 상자 안으로
  const r=t.getBoundingClientRect(), b=el.getBoundingClientRect(); if(r.left<b.left+4) el.scrollLeft-=b.left+8-r.left; else if(r.right>b.right-4) el.scrollLeft+=r.right-b.right+8; }); });
document.addEventListener('click',e=>{   // v33 키보드: 누른 단추가 카드째 다시 그려져 사라지면 새로 그린 같은 단추로 초점(body로 떨어지지 않게)
  const a=document.activeElement;
  if(!a||a===document.body||!a.matches||!a.matches('button,a[href],[role="button"],[tabindex]')||!a.contains(e.target)) return;
  const host=a.parentElement&&a.parentElement.closest('[id]'); if(!host) return;
  const hid=host.id, id=a.id, oc=a.getAttribute('onclick'), tx=(a.textContent||'').trim();
  const key=el=>el.tagName.toLowerCase()+[...el.classList].filter(c=>!/^(on|off|open|sel)$/.test(c)).map(c=>'.'+CSS.escape(c)).join('');
  const sel=key(a.parentElement)+'>'+key(a), idx=[...host.querySelectorAll(sel)].indexOf(a);   // 같은 줄(부모 모양)의 같은 모양 단추끼리 — 묶음 요약 단추와 묶음 탭처럼 onclick이 같은 다른 단추로 가지 않게
  setTimeout(()=>{
    if(a.isConnected) return;
    const f=document.activeElement; if(f&&f!==document.body&&f!==document.documentElement) return;   // 다른 곳으로 초점을 옮긴 경우(패널 닫기 등)는 그대로
    const h=document.getElementById(hid); if(!h||!h.getClientRects().length) return;
    const c=[...h.querySelectorAll(sel)];
    const n=(id&&document.getElementById(id))||(oc&&c.find(x=>x.getAttribute('onclick')===oc))||c.find(x=>(x.textContent||'').trim()===tx)||c[Math.min(Math.max(idx,0),c.length-1)];
    if(n&&n.getClientRects().length) try{ n.focus({preventScroll:true}); }catch(err){}
  },0);
},true);
document.addEventListener('click',e=>{
  const br=e.target.closest('[data-brand]');   // v33 S2: 브랜드 행·판정 안 함 행·국내 네이버 수입·해외 줄 → 브랜드 상세(이름은 data 속성 — 따옴표 안전)
  if(br){ e.preventDefault(); openBrand(br.dataset.brand); return; }
  const g=e.target.closest('[data-go]');   // v33 S2: 새 화면 단추(오늘 카드·브랜드 탭·브랜드 상세·더보기 메뉴) → goKey
  if(g){ e.preventDefault(); goKey(g.dataset.go); return; }
});

// v33 S2: 옛 머리의 갱신 문구(#gen)는 오늘 머리 단추·맺음 줄로, 출처(Yahoo·SEC·DART·KOSIS)는 더보기 › 수집 상태 부제로. 오늘은 화면을 열 때 그림(render)
safe(buildSig,'실적·재고','mk-sig'); safe(buildMap,'소싱 지도','mk-map');
safe(buildCoChips,'기업 칩','mk-co'); safe(buildCo,'기업 표','mk-co'); safe(buildCal,'캘린더','mk-cal');
safe(buildNewsChips,'뉴스 칩','mk-news'); safe(buildKR,'국내','mk-kr'); safe(buildBrand,'브랜드 점검표','brandBody'); safe(buildMore,'더보기','moreBody');
safe(navInit,'이동 경로','content');   // 뉴스·의류 소매 그래프는 그 칩이 처음 보일 때(v32.11·v33)
WF_GO=true; requestAnimationFrame(()=>setTimeout(webFont,0));   // v33 첫 화면을 그린 다음 글꼴(webFont)
</script>
</body>
</html>
"""


# ── v33.2 브랜드 점검표 판정 — 파이썬 쌍둥이(history_append가 매일 history.json verdicts에 기록, weekly_digest가 요약) ──
# 화면 JS chkMedian·chkDemand·chkInv(invPick)·chkNotes(segOf)·chkFx·chkModel과 같은 규칙. 규칙(점수 기준·판정식·대상)을 바꾸면
# 양쪽을 함께 고치고 CHK_RULE을 올림 — 기록의 rule이 다르면 화면·주간 메일이 판정 변화를 비교하지 않음(규칙이 바뀐 날 '변화'가 잘못 뜨지 않게)
CHK_RULE = 1
CHK_CUR = {   # 원산지(본사) 통화 — 네이버 감시 브랜드(global)를 추가하면 함께 넣음(화면 JS CHK_CUR로 그대로 들어감)
    "나이키": "USD", "뉴발란스": "USD", "우포스": "USD", "아디다스": "EUR", "호카": "USD", "드래곤디퓨전": "EUR", "메종키츠네": "EUR",
    "푸마": "EUR", "킨(KEEN)": "USD", "가니": "EUR", "언더아머": "USD", "헌터": "GBP", "닥터마틴": "GBP", "크록스": "USD", "핏플랍": "GBP",
    "락포트": "USD", "피레넥스": "EUR", "클락스": "GBP", "브룩스": "USD", "파라부트": "EUR", "와일드동키": "EUR", "휴먼메이드": "JPY",
    "CEP": "EUR", "노르다": "USD", "비비안웨스트우드": "GBP", "에코(ECCO)": "EUR", "단톤": "EUR", "어그": "USD", "샤카웨어": "USD",
    "스케쳐스": "USD",
    # v33.7 추가 8개(naver_trend v1.8 ADD_BRANDS)
    "아식스": "JPY", "오니츠카타이거": "JPY", "미즈노": "JPY", "살로몬": "EUR", "아크테릭스": "USD", "룰루레몬": "USD", "온러닝": "CHF",
    "써코니": "USD",
    # v33.8 2순위 새 종목 5개(naver_trend v1.9) — 톰브라운은 뉴욕 브랜드라 달러(본사 제냐 재무는 유로, CHK_CUR_NOTE)
    "몽클레르": "EUR", "스톤아일랜드": "EUR", "톰브라운": "USD", "버버리": "GBP", "폴로 랄프로렌": "USD",
}
CHK_LV = {2: "지금 검토", 1: "관망", 0: "주의"}
VERDICT_EMBED = 60   # 화면에 넣는 판정 기록 수(history.json에는 history_append가 최대 400일)


def chk_sig(naver):
    """판정 비교 기준(sig) — 감시 브랜드(global)의 이름·본사 연결과 원산지 통화표(CHK_CUR). 브랜드 추가·삭제·연결 변경이나 CHK_CUR 수정이
    있으면 값이 바뀌어 그 전 기록과 비교하지 않음(감시 브랜드 중앙값·판정 대상이 바뀌어 생긴 변화를 '어제와 달라진 판정'으로 보이지 않게).
    입력 측정 방식(재고 비교 기간·환율 기준·검색 전년 대비·발언 신호)이나 판정 규칙을 바꾸면 CHK_RULE을 올림"""
    bs = sorted((str(b.get("name")), str(b.get("link") or "")) for b in ((naver or {}).get("brands") or [])
                if isinstance(b, dict) and b.get("group") == "global")
    raw = json.dumps([bs, sorted(CHK_CUR.items())], ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:10]


def chk_entry_ok(x):
    """판정 기록의 한 브랜드 값이 올바른지 — [판정 0·1·2, 수요, 재고, 발언, 환율](점수는 정수 또는 None). 화면 chkHist lvOf와 같은 기준 —
    틀린 값은 판정 변화 비교에서 뺌(화면은 '판정 기록 비교 제외')"""
    return (isinstance(x, list) and len(x) >= 5 and type(x[0]) is int and x[0] in CHK_LV
            and all(v is None or type(v) is int for v in x[1:5]))


def chk_records(hist):
    """history.json verdicts에서 모양이 맞는 기록만(날짜 YYYY-MM-DD 문자열 · rule 정수 · b dict) — 날짜순"""
    vs = (hist or {}).get("verdicts") if isinstance(hist, dict) else None
    return sorted((r for r in (vs if isinstance(vs, list) else []) if isinstance(r, dict) and isinstance(r.get("date"), str)
                   and re.fullmatch(r"\d{4}-\d{2}-\d{2}", r["date"]) and type(r.get("rule")) is int and isinstance(r.get("b"), dict)),
                  key=lambda r: r["date"])


def _chk_median(brands):
    """감시 브랜드(global, 검색량 충분) 전년 대비의 중앙값 — JS chkMedian"""
    v = sorted(b["yoy"] for b in brands if b.get("group") == "global" and b.get("yoy") is not None and not b.get("low"))
    n = len(v)
    if not n:
        return None
    return v[(n - 1) // 2] if n % 2 else (v[n // 2 - 1] + v[n // 2]) / 2


def _chk_dem(b, med):
    """국내 수요 점수(None = 검색 자료 없음) — JS chkDemand"""
    if b.get("yoy") is None:
        return None
    if med is None:
        return 0
    rel = b["yoy"] - med
    return 0 if b.get("low") else (1 if rel >= 10 else (-1 if rel <= -10 else 0))


def _chk_inv(x):
    """본사 재고 점수(None = 같은 기간 재고·매출 없음) — JS chkInv·invPick(분기 재고가 있으면 같은 분기끼리, 없으면 연간 결산)"""
    fy = ((x.get("fy") or [{}])[-1]) or {}
    if x.get("q_inv_yoy") is not None and x.get("q_inv_rev_yoy") is not None and not x.get("yahoo_cfs_diff"):
        iv, rv = x["q_inv_yoy"], x["q_inv_rev_yoy"]
    else:
        iv, rv = x.get("inv_yoy"), fy.get("rev_yoy")
    if iv is None or rv is None:
        return None
    p = iv - rv
    return 1 if p >= 5 else (-1 if p <= -5 else 0)


def _js_true(v):
    """JS 참·거짓 — 빈 dict·list도 참(파이썬과 다름)"""
    if v is None or v is False or v == "":
        return False
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        return v == v and v != 0
    return True


def _chk_notes(t, segs, segs_ir):
    """본사 발언 점수(None = 발언 자료 없음·모두 신호 분류 전) — JS chkNotes·segOf(IR 추출이 있으면 IR, 없으면 공시)"""
    e = None
    for src in (segs_ir, segs):
        c = ((src or {}).get("items") or {}).get(t)
        if isinstance(c, dict) and _js_true(c.get("extract")):
            e = c
            break
    ex = e["extract"] if e else None
    if not isinstance(ex, dict) or not isinstance(ex.get("mgmt_notes"), list):
        return None
    sig = [n.get("sig") if isinstance(n, dict) else None for n in ex["mgmt_notes"]]
    m, l, z = sig.count("more"), sig.count("less"), sig.count("neutral")
    if sig and len(sig) - m - l - z == len(sig):
        return None
    return 1 if m > l else (-1 if l > m else 0)


def _chk_fx(f):
    """원산지 통화 점수(None = 환율 자료 없음) — JS chkFx(1년 평균 대비, 없으면 1년 전 대비)"""
    if not f:
        return None
    v = f.get("dev_pct") if f.get("dev_pct") is not None else f.get("chg_pct")
    if v is None:
        return None
    return 2 if v <= -10 else (1 if v <= -5 else (-2 if v >= 10 else (-1 if v >= 5 else 0)))


def chk_verdicts(data, naver, segs, segs_ir):
    """브랜드 점검표 판정 — 화면 chkModel과 같은 대상·규칙. data는 merge_kr_listed를 거친 것(화면과 같은 재고·매출).
    반환 {브랜드: [판정, 수요, 재고, 발언, 환율]} — 판정 2 지금 검토 · 1 관망 · 0 주의, 점수는 화면 점수 칸 그대로(None = 자료 없음).
    본사가 상장사로 연결되지 않았거나 본사 재고·발언 자료가 둘 다 없는 브랜드(판정 안 함)는 넣지 않음"""
    brands = [b for b in ((naver or {}).get("brands") or []) if isinstance(b, dict) and b.get("group") == "global"]
    med = _chk_median(brands)
    items = (data or {}).get("items") or []
    fxd = (data or {}).get("fx") or {}
    out = {}
    for b in brands:
        link = str(b.get("link") or "")
        x = next((i for i in items if i.get("ticker") == link), None) if link and not link.startswith("krd:") else None
        if x is None:
            continue
        inv, notes = _chk_inv(x), _chk_notes(x.get("ticker"), segs, segs_ir)
        if inv is None and notes is None:
            continue
        cur = CHK_CUR.get(b.get("name"))
        dem, fx = _chk_dem(b, med), (_chk_fx(fxd.get(cur)) if cur else None)
        buy = (inv or 0) + (notes or 0) + (fx or 0)
        dp = dem or 0
        lv = 2 if (dp >= 0 and buy >= 2) else (0 if ((dp < 0 and buy <= 1) or buy <= -1) else 1)
        out[b["name"]] = [lv, dem, inv, notes, fx]
    return out


def merge_kr_listed(data):
    """국내 상장사 재무를 DART 전체재무제표(연결 우선, 종목별 fs)로 교체 (야후는 주가·분기YoY·실적일 유지)"""
    if not os.path.exists("docs/kr_listed_fin.json"):
        return 0
    try:
        with open("docs/kr_listed_fin.json", encoding="utf-8") as f:
            krf = json.load(f)
    except Exception:
        return 0
    n = 0
    for item in data.get("items", []):
        e = (krf.get("items") or {}).get(item.get("ticker"))
        if not e or not e.get("years"):
            continue
        ys = e["years"]
        # v32.9 야후(연결) 연간 매출이 DART 값과 20% 넘게 다르면 기준이 다른 것(예: LS네트웍스 지정 별도 vs 야후 LS증권 포함 연결)
        # → 야후 분기 매출 전년 대비는 순위·목록에서 빼고 상세에만 '야후 연결' 표기와 함께 보임
        # 가장 최근 공통 연도만 비교 — 옛 연도는 DART 재작성(중단영업 등) 값이라 야후와 다를 수 있음(신세계인터내셔날 FY23)
        dmap = {(y.get("end") or "")[:4]: y.get("rev") for y in ys}
        diff = [(y["end"], abs(y["rev"] / dmap[(y.get("end") or "")[:4]] - 1)) for y in (item.get("fy") or [])
                if y.get("rev") and y.get("end") and dmap.get(y["end"][:4])]
        if diff and max(diff)[1] > 0.2:
            item["yahoo_cfs_diff"] = True
            item["q_yoy_yahoo"] = item.get("latest_q_yoy")
            item["latest_q_yoy"] = None
        fy = []
        for i, y in enumerate(ys):
            rev, cogs, op = y.get("rev"), y.get("cogs"), y.get("op")
            prev = ys[i - 1].get("rev") if i > 0 else None
            fy.append({
                "end": y.get("end"), "rev": rev,
                "gp": (rev - cogs) if (rev is not None and cogs is not None) else None,
                "op": op,
                "rev_yoy": ((rev / prev - 1) * 100) if (rev and prev) else None,
                "gm_pct": ((rev - cogs) / rev * 100) if (rev and cogs is not None) else None,
                "op_pct": (op / rev * 100) if (rev and op is not None) else None,
            })
        item["fy"] = fy[-3:]
        last, prev = ys[-1], (ys[-2] if len(ys) > 1 else None)
        item["inventory"] = last.get("inv")
        item["inv_date"] = last.get("end")
        item["inv_prev_date"] = prev.get("end") if prev else None
        item["inv_yoy"] = ((last["inv"] / prev["inv"] - 1) * 100) if (prev and last.get("inv") and prev.get("inv")) else None
        item["inv_sales_pct"] = (last["inv"] / last["rev"] * 100) if (last.get("inv") and last.get("rev")) else None
        item["currency"] = "KRW"
        item["fin_fs"] = e.get("fs") or ("별도" if "(별도)" in (e.get("source") or "") else "연결")
        item["acct_std"] = e.get("std")
        # v32.9 '연결' 고정 문구 대신 실제 기준(source의 연결/별도) + 회계기준 + 예외 사유
        item["fin_source"] = " · ".join(x for x in ["DART " + (e.get("source") or "").strip(), e.get("std"), e.get("fs_note")] if x)
        n += 1
    return n


# 수집 상태: (파일, 표시명, 워크플로우, 주기 표기, 지연 판정 일수)
STATUS_SOURCES = [
    ("data.json", "재무·주가", "update-dashboard", "매일 04:17", 2),
    ("news.json", "뉴스", "update-news", "매일 03:17", 2),
    ("segments.json", "미국 공시 지역·채널", "extract-segments", "매주 월", 9),
    ("segments_ir.json", "유럽·일본 IR", "update-ir", "매주 일", 9),
    ("kr_domestic.json", "국내 법인·상장 재무", "update-dart", "매월 15일", 40),
    ("kosis.json", "국내 소매 지표", "update-kosis", "매월 5일", 40),
    ("naver_trend.json", "네이버 검색 관심도", "update-dashboard", "매일 04:17", 2),
    ("logistics.json", "물류 운임·바닷길", "update-dashboard", "매일 04:17", 2),   # v33.4 logistics_fetch v1
]


def _ts_iso(v):
    """'2026-10-01 11:22 KST' / '2026-09-30' → ISO(+09:00), 실패 시 None"""
    m = re.match(r"(\d{4}-\d{2}-\d{2})(?:[ T](\d{2}):(\d{2}))?", str(v or ""))
    if not m:
        return None
    return f"{m.group(1)}T{m.group(2) or '00'}:{m.group(3) or '00'}:00+09:00"


def _conn_note(c, name):
    """v33.10 일부 GitHub 서버에서만 막히는 연결(logistics_fetch v1.3 dgk_conn · kosis_fetch v5.2 conn) — 이번 실행에서 못 받았을 때만 한 줄.
    모든 차례가 연결 시험에서 막혔으면 '연결 안 됨(GitHub 서버 n대 모두 막힘)', 아니면 '연결 오류(GitHub 서버 n대에서 시도)'(5xx·시간 초과 등)"""
    if not isinstance(c, dict) or not isinstance(c.get("keys"), list) or not c["keys"]:
        return []
    tr = c.get("tries")
    tr = [t for t in tr if isinstance(t, dict)] if isinstance(tr, list) else []
    nt = len(tr)
    blocked = bool(tr) and all(t.get("blocked") for t in tr)
    how = ((f"GitHub 서버 {nt}대 모두 막힘" if nt > 1 else "GitHub 서버에서 막힘") if blocked else
           (f"GitHub 서버 {nt}대에서 시도" if nt else ""))
    since = c.get("since") if isinstance(c.get("since"), str) else ""
    inner = " · ".join(x for x in (how, f"{since}부터" if since else "") if x)
    return [f"{name} 연결 {'안 됨' if blocked else '오류'}" + (f"({inner})" if inner else "")]


def _partial(fn, d):
    """v32.12 부분 실패 요약 — (못 받은 곳 수(이전 값 + 값 없음), 화면에 보일 짧은 설명 목록). 필드가 없으면 (0, [])
    수는 각 수집 스크립트가 남긴 실패 목록으로 셈: data.json fetch_status(fetch_data v4.12) · naver_trend.json status(v1.7) ·
    kosis.json failed(v5.1) · segments(_ir).json failed(extract_segments — kept_reason은 설명만) · kr_domestic.json failed(dart_fetch v3.4)"""
    n, notes = 0, []
    if fn == "data.json":
        fs = d.get("fetch_status") or {}
        kept, bad = fs.get("kept") or [], fs.get("failed") or []
        fxk, fxf = fs.get("fx_kept") or [], fs.get("fx_failed") or []
        n = len(kept) + len(bad) + len(fxk) + len(fxf)
        if kept:
            notes.append(f"종목 {len(kept)}곳 이전 값")
        if bad:
            notes.append(f"종목 {len(bad)}곳 값 없음")
        if fxk:
            notes.append("환율 이전 값 " + "·".join(fxk))
        if fxf:
            notes.append("환율 없음 " + "·".join(fxf))
    elif fn == "naver_trend.json":
        st = d.get("status") or {}
        kb = st.get("kept_brands") or [b.get("name") for b in d.get("brands") or [] if b.get("stale_since")]
        fb, bmk, bmf = st.get("failed_brands") or [], st.get("brand_monthly_kept") or [], st.get("brand_monthly_failed") or []
        m_bad = bool(st) and d.get("monthly") is None          # 월간 합계를 못 받았고 이전 값도 없음
        n = len(set(kb) | set(fb) | set(bmk) | set(bmf)) + (1 if st.get("monthly_kept") or m_bad else 0)   # 브랜드는 한 번만 셈
        if kb:
            notes.append(f"브랜드 {len(kb)}개 이전 값")
        if fb:
            notes.append(f"브랜드 {len(fb)}개 값 없음")
        if st.get("monthly_kept"):
            notes.append("월간 합계 이전 값")
        if m_bad:
            notes.append("월간 합계 값 없음")
        if bmk:
            notes.append(f"브랜드 월간 {len(bmk)}개 이전 값")
        if bmf:
            notes.append(f"브랜드 월간 {len(bmf)}개 값 없음")
    elif fn == "kosis.json":
        ser = d.get("series") or {}
        kept = [k for k, v in ser.items() if isinstance(v, dict) and v.get("stale_since")]
        if (d.get("cross_border") or {}).get("stale_since"):
            kept.append("cross_border")
        bad = [k for k in d.get("failed") or [] if k not in kept]
        n = len(set(d.get("failed") or []) | set(kept))      # failed = 이전 값 + 값 없음(kosis_fetch v5.1)
        if kept:
            notes.append(f"지표 {len(kept)}개 이전 값" + (" (해외직구 포함)" if "cross_border" in kept else ""))
        if bad:
            notes.append(f"지표 {len(bad)}개 값 없음" + (" (해외직구 포함)" if "cross_border" in bad else ""))
        notes += _conn_note(d.get("conn"), "통계청")   # v33.10 kosis_fetch v5.2
    elif fn in ("segments.json", "segments_ir.json"):
        # 수 = 이번 실행에서 실패한 종목(failed). kept_reason은 설명만 — 새 공시에 분해가 없어 이전 실적을 지킨 경우·
        # 지난 실패 사유가 이월된 경우는 실패로 세지 않음
        items = d.get("items") or {}
        failed = list(dict.fromkeys(d.get("failed") or []))
        n = len(failed)
        kr = {t: v for t, v in items.items() if isinstance(v, dict) and v.get("kept_reason")}
        bad = [t for t in failed if t not in kr]
        # 사유 3종(extract_segments v10): 실패해 이전 값(kept_failed) · 더 새 공시를 실적 자료 아님으로 건너뜀(안내) · 새 공시에 분해 없어 이전 실적 유지
        k_fail = [t for t, v in kr.items() if v.get("kept_failed")]
        rs = {t: str(v.get("kept_reason")) for t, v in kr.items() if t not in k_fail}
        k_note = [t for t, r in rs.items() if re.search(r"건너뜀|투자자의 날|프로포마", r)]
        k_unread = [t for t, r in rs.items() if t not in k_note and "못 읽음" in r]
        k_keep = [t for t in rs if t not in k_note and t not in k_unread]
        if k_fail:
            notes.append("실패·이전 추출 유지 " + "·".join(k_fail))
        if k_note:
            notes.append("최신 공시 건너뜀(투자자의 날·프로포마 등) " + "·".join(k_note))
        if k_unread:
            notes.append("최신 공시 못 읽음·이전 추출 유지 " + "·".join(k_unread))
        if k_keep:
            notes.append("새 공시에 분해 없음·이전 추출 유지 " + "·".join(k_keep))
        if bad:
            notes.append(f"종목 {len(bad)}곳 값 없음")
    elif fn == "news.json":
        st = d.get("status") or {}      # news_monitor v2.9 — 선별 실패는 1곳으로 셈, 검색어 일부 실패는 설명만
        if st.get("curate") == "failed":
            n = 1
            notes.append(f"Claude 선별 실패(신규 {st.get('new', 0)}건은 다음 실행에서)")
        if st.get("failed_queries"):
            notes.append(f"검색어 {st['failed_queries']}/{st.get('queries', '?')}개 실패")
        ar = st.get("archive")      # v33.1 news_monitor v2.12 지난 뉴스 1년 보관(검색창)
        if isinstance(ar, dict) and ar.get("ok") is False:
            n += 1
            notes.append("검색용 1년 보관 파일 저장 실패")
        elif isinstance(ar, dict) and isinstance(ar.get("n"), int) and ar["n"] > 0:
            part = ar.get("partial") is True     # git 기록 일부로 만듦(news_monitor가 실패 표시 — 점검 알림과 맞춤)
            n += 1 if part else 0
            notes.append(f"검색용 보관 {ar['n']:,}건" + (f"({ar['since']}부터)" if isinstance(ar.get("since"), str) and ar["since"] else "")
                         + (" — 일부만 복구(다음 실행에서 다시)" if part else ""))
        dc = st.get("date_check")   # v33.3 news_monitor v2.13 옛 기사 거르기(구글이 새 날짜로 다시 낸 지난 기사)
        if isinstance(dc, dict):
            num = lambda k: dc[k] if isinstance(dc.get(k), int) and not isinstance(dc.get(k), bool) and dc[k] > 0 else 0
            if dc.get("broken") is True:   # news_monitor가 실패 표시 — 점검 알림과 맞춤
                n += 1
                notes.append("구글 링크를 못 풀어 원문 날짜·글 번호 확인 안 됨(옛 기사는 Claude 확인으로만)")
            elif dc.get("error") is True:
                n += 1
                notes.append("옛 기사 확인 오류(이번 실행은 거르지 않음)")
            if dc.get("blocked") is True:
                notes.append("구글이 원문 확인을 막음(다음 실행에서)")
            if num("stale") or num("memory"):
                notes.append(f"옛 기사 이번 {num('stale')}건 제외" + (f" · 기억 {num('memory')}건" if num("memory") else ""))
            if num("left_ai") or num("left_page"):
                notes.append(f"옛 기사 점검 남음 {num('left_ai') + num('left_page')}건(다음 실행에서)")
    elif fn == "logistics.json":
        st = d.get("status") or {}      # v33.4 logistics_fetch v1 — kept = 이전 값(해협·항만은 '해협 통과(호르무즈 해협)'처럼 일부 항목), failed = 값 없음
        kept = [x for x in st.get("kept") or [] if isinstance(x, str)]
        bad = [x for x in st.get("failed") or [] if isinstance(x, str)]
        n = len(kept) + len(bad)
        if kept:
            notes.append("이전 값 " + ", ".join(kept))
        if bad:
            notes.append("값 없음 " + ", ".join(bad))
        notes += _conn_note(d.get("dgk_conn"), "공공데이터포털")   # v33.10 logistics_fetch v1.3
    else:
        n = len(d.get("failed") or [])   # v32.9 dart_fetch v3.4: 일부 법인 실패(이전 값 유지)
    return n, notes


# v32.16 Claude 사용액: (파일, 표시명, 주기) — 각 수집 스크립트가 월별 claude_usage를 저장
CLAUDE_SOURCES = [
    ("news.json", "뉴스 선별", "매일"),
    ("segments.json", "미국 공시 추출", "매주 월"),
    ("segments_ir.json", "유럽·일본 IR 추출", "매주 일"),
    ("kr_domestic.json", "국내 감사보고서 추출", "매월 15일"),
]
KST_TZ = datetime.timezone(datetime.timedelta(hours=9))


def collect_claude(now=None):
    """v32.16 작업별 이번 달·지난달 Claude 사용액 — 기록이 하나도 없으면 None.
    since = 기록을 이번 달 중간에 시작한 작업(이전 달 기록 없음)의 시작일 — 그 전 사용은 빠져 있다는 표시"""
    now = now or datetime.datetime.now(KST_TZ)
    month = now.strftime("%Y-%m")
    prev = (now.replace(day=1) - datetime.timedelta(days=1)).strftime("%Y-%m")
    rows, any_rec = [], False
    for fn, label, cad in CLAUDE_SOURCES:
        cu = {}
        try:
            with open(os.path.join("docs", fn), encoding="utf-8") as f:
                cu = json.load(f).get("claude_usage") or {}
        except Exception:
            pass
        cu = {k: v for k, v in cu.items() if isinstance(v, dict)} if isinstance(cu, dict) else {}
        any_rec = any_rec or bool(cu)
        cur, pm = cu.get(month) or {}, cu.get(prev) or {}
        since = cur.get("since") if cur and not any(k < month for k in cu) else None
        psince = pm.get("since") if pm and not any(k < prev for k in cu) else None   # 지난달도 기록 시작 달이면 그 전은 빠짐
        rows.append({"label": label, "cad": cad, "rec": bool(cu), "usd": cur.get("usd"), "calls": cur.get("calls"),
                     "prev": pm.get("usd"), "since": since if isinstance(since, str) and since[8:10] > "01" else None,
                     "prev_since": psince if isinstance(psince, str) and psince[8:10] > "01" else None})
    return {"month": month, "prev": prev, "rows": rows} if any_rec else None


def collect_status():
    out = []
    for fn, label, wf, cad, limit in STATUS_SOURCES:
        ts, date_only, failed, notes = None, False, 0, []
        p = os.path.join("docs", fn)
        if os.path.exists(p):
            try:
                with open(p, encoding="utf-8") as f:
                    d = json.load(f)
                raw = str(d.get("generated_at") or d.get("updated_at") or "")
                ts = _ts_iso(raw)
                date_only = not re.search(r"\d{2}:\d{2}", raw)
                failed, notes = _partial(fn, d)
            except Exception as e:
                print(f"[WARN] 수집 상태 {fn} 읽기 실패: {str(e)[:100]}")
        out.append({"file": fn, "label": label, "wf": wf, "cadence": cad, "limit": limit,
                    "ts": ts, "date_only": date_only, "failed": failed, "notes": notes})
    return {"sources": out, "claude": collect_claude()}


def main():
    with open("docs/data.json", encoding="utf-8") as f:
        data = json.load(f)
    merged = merge_kr_listed(data)
    print(f"국내 상장사 DART 재무 병합: {merged}개")
    segs = {"items": {}}
    if os.path.exists("docs/segments.json"):
        try:
            with open("docs/segments.json", encoding="utf-8") as f:
                segs = json.load(f)
        except Exception:
            pass
    wmap = None
    if os.path.exists("docs/worldmap.json"):
        try:
            with open("docs/worldmap.json", encoding="utf-8") as f:
                wmap = json.load(f)
        except Exception:
            pass
    segs_ir = None
    if os.path.exists("docs/segments_ir.json"):
        try:
            with open("docs/segments_ir.json", encoding="utf-8") as f:
                segs_ir = json.load(f)
        except Exception:
            pass
    krd = None
    if os.path.exists("docs/kr_domestic.json"):
        try:
            with open("docs/kr_domestic.json", encoding="utf-8") as f:
                krd = {k: v for k, v in json.load(f).items() if not k.startswith("_")}   # 추출 캐시 제외
        except Exception:
            pass
    hist = None
    if os.path.exists("docs/history.json"):
        try:
            with open("docs/history.json", encoding="utf-8") as f:
                hist = json.load(f)
        except Exception:
            pass
    kr = None
    if os.path.exists("docs/kosis.json"):
        try:
            with open("docs/kosis.json", encoding="utf-8") as f:
                kr = json.load(f)
        except Exception:
            pass
    naver = None
    if os.path.exists("docs/naver_trend.json"):
        try:
            with open("docs/naver_trend.json", encoding="utf-8") as f:
                naver = json.load(f)
        except Exception as e:
            print(f"[WARN] naver_trend.json 읽기 실패: {str(e)[:100]}")
    logi = None   # v33.4 물류(logistics_fetch v1)
    if os.path.exists("docs/logistics.json"):
        try:
            with open("docs/logistics.json", encoding="utf-8") as f:
                logi = json.load(f)
            if isinstance(logi.get("glp"), dict):
                logi["glp"].pop("skip", None)   # 정시율 기사 건너뜀 기억 — 화면에 안 씀
                logi["glp"].pop("fmt_skip", None)
            for vk in ("vol_in", "vol_out"):   # v33.6 나라별 물동량 — 화면은 앞 지표(바닷길 TEU · 항공 톤) 시계열 + 보조 지표(톤 · B/L) 마지막 달만 씀
                for md in ("sea", "air"):
                    m = (logi.get(vk) or {}).get(md) if isinstance(logi.get(vk), dict) else None
                    if not isinstance(m, dict) or not isinstance(m.get("metrics"), list) or not m["metrics"]:
                        continue
                    lead = m["metrics"][0]
                    for tk in ("total", "total_clean", "yoy"):
                        if isinstance(m.get(tk), dict):
                            m[tk] = {lead: m[tk].get(lead)}
                    for it in m.get("items") or []:
                        for k in m["metrics"][1:]:
                            if isinstance(it, dict) and isinstance(it.get(k), list):
                                it[k] = it[k][-1:]
            bc = logi.get("busan_calls")   # v33.6 부산항 입항 — 직전 출항지·체류는 최근 40일만 씀(그 앞은 하루 척수만)
            if isinstance(bc, dict) and isinstance(bc.get("days"), list) and bc["days"] and isinstance(bc["days"][-1], list):
                try:
                    cut = (datetime.date.fromisoformat(str(bc["days"][-1][0])) - datetime.timedelta(days=40)).isoformat()
                    bc["days"] = [[r[0], r[1], {}, 0, 0] if isinstance(r, list) and len(r) >= 5 and str(r[0]) < cut else r for r in bc["days"]]
                except ValueError:
                    pass
        except Exception as e:
            print(f"[WARN] logistics.json 읽기 실패: {str(e)[:100]}")
            logi = None
    news = None
    if os.path.exists("docs/news.json"):
        try:
            with open("docs/news.json", encoding="utf-8") as f:
                news = json.load(f)
            for k in ("seen_ids", "seen_titles", "seen_since", "model_compare", "stale_titles", "boards"):   # v32.11 화면에 안 쓰는 항목(약 100KB) — 원본 news.json은 그대로 · v33.3 옛 기사 제목 기억·게시판 글 번호
                news.pop(k, None)
        except Exception:
            pass
    # v33.2 판정 기록은 지금과 비교할 수 있는 것(규칙 판 CHK_RULE · 비교 기준 sig가 같음)의 최근 VERDICT_EMBED개만 화면에 넣음
    # (화면은 바로 전 기록·같은 판정이 이어진 날짜만 씀). verdicts_start = 모든 기록의 첫 날짜('판정 기록을 시작한 날' vs '적어도 그날부터')
    sig = chk_sig(naver)
    if isinstance(hist, dict) and "verdicts" in hist:
        rs = chk_records(hist)
        cv = [r for r in rs if r["rule"] == CHK_RULE and r.get("sig") == sig]
        hist = {**hist, "verdicts": cv[-VERDICT_EMBED:], "verdicts_start": rs[0]["date"] if rs else None}
    def js(v):   # v33 내장 데이터 — 뉴스 요약 등에 '</script'·'<!--'가 들어와도 화면 스크립트가 끊기지 않게(JSON 안에서는 같은 글자: \/ = /, \u0021 = !)
        return json.dumps(v, ensure_ascii=False).replace("</", "<\\/").replace("<!--", "<\\u0021--")
    html = (TEMPLATE
            .replace("__DATA__", js(data))
            .replace("__SEGS__", js(segs))
            .replace("__NEWS__", js(news))
            .replace("__KR__", js(kr))
            .replace("__NAVER__", js(naver))
            .replace("__HIST__", js(hist))
            .replace("__KRD__", js(krd))
            .replace("__SEGS_IR__", js(segs_ir))
            .replace("__STATUS__", js(collect_status()))
            .replace("__WMAP__", js(wmap))
            .replace("__LOGI__", js(logi))
            .replace("__CHK_CUR__", js(CHK_CUR))
            .replace("__CHK_RULE__", str(CHK_RULE))
            .replace("__CHK_SIG__", json.dumps(sig)))
    with open("docs/index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("saved docs/index.html")


if __name__ == "__main__":
    main()

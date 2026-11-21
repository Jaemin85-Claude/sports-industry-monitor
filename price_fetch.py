# -*- coding: utf-8 -*-
"""
sports-industry-monitor — Phase 11: 해외 정가 (나라별 브랜드 대표 상품 소비자가)
v1.25: (대표 지시 2026-11-21 '해외정가 금일 추가 수집' — 브랜드당 20개 2차) 상품 78개 추가(147 → 225 · 값 621 → 921): 아크테릭스 +9 · 써코니 +9 · 킨 +10 · 우포스 +10 ·
    헌터 +10 · 푸마 +7 · 닥터마틴 +4 · 나이키 +3(모두 20개 · 써코니 18) + 판정 브랜드 첫 해외 정가 톰브라운 12(본사 쇼피파이 몰 나라별 폴더 6개 나라 · 상품 .json) ·
    버버리 4(kr·us·uk.burberry.com JSON-LD sku = p 번호) — 나라별 몰 사이트맵·공개 기획전·쇼피파이 공개 .json으로 한국과 같은 글로벌 품번 → GitHub 서버에서 정가 읽기 확인(11/21) ·
    블프 검사: 한국 정가 ÷ (현지 정가 × 11/20 환율)이 그 브랜드 기존 상품 나라별 가운데값의 1.25배를 넘는 나라는 뺌(할인가가 정가로 읽힌 것 — 아크테릭스 영국·독일 노반 LD 4 ·
    써코니 엔돌핀 싱글렛·쇼트 슬리브 · 푸마 T7 트랙 자켓 영국 등) · 써코니 가이드 19 한국 주소를 품절 색상(373)에서 같은 품번 다른 색(372)으로 · 드래곤디퓨전은 코오롱몰 8개 모델이
    모두 들어가 더 없음 · 살로몬 해외(www.salomon.com)는 11/20부터 첫 요청에서 403(PerimeterX — robots.txt는 열림)이라 늘리지 않음 · Firecrawl 안 씀
v1.24:(대표 지시 2026-11-20 '브랜드당 MSRP 20개' · 결정 '검색만'(Firecrawl은 후보 주소 찾기만 · 정가는 우리 봇) · '블프 전 1차 + 이후 주 1회 차례')
    1차 29개 상품(값 약 140개): 나이키 +7(17) · 온러닝 +10(20) · 닥터마틴 +6(16) · 푸마 +2(13) — 나라별 몰 사이트맵(robots.txt에 적힌 것)·나이키 product_feed로
    한국과 같은 글로벌 품번 → GitHub 서버에서 정가 읽기 확인(11/20) · 닥터마틴 미국 몰은 블프 할인가가 정가로 읽혀(한국 정가 ÷ 미국 값이 지금 상품의 1.4배) 처치만 넣고
    나머지 미국 값은 블프 뒤에 · 아크테릭스·써코니·살로몬은 다음 차례(검색 결과에 품번이 드물고 살로몬 해외는 한 실행 8건)
v1.23: (대표 결정 2026-11-19 '추천대로' — 개편 A1 · build_dashboard v33.34) 상품마다 분류 cat(신발 shoe · 부츠 boot · 샌들류 sandal · 반팔·민소매 top ·
    옷 wear · 가방 bag)을 PRODUCTS에 넣고 prices.json 상품에 함께 저장(받지 않는 날도 지금 PRODUCTS 것으로) — 화면 착지가 분류별 무게·관세(가방 8%)로 계산 ·
    분류가 없거나 모르는 이름이면 불러오기에서 멈춤(새 상품은 cat 필수) · cfg_hash는 cat을 빼고 셈(분류만 바꾼 날 전체를 다시 받지 않음)
v1.22: (11/17 update-dashboard — 언더아머 한국·영국·독일 27건 '가격 데이터 없음') 원인 = 세 몰이 11/17부터 상품 페이지 대신 봇 확인 화면('Client Challenge' · HTTP 200 · 3KB ·
    11/17 GitHub 서버 확인 — 우회하지 않음) → ① PAUSED에 넣음(why '한국/영국/독일 공식몰이 자동 접속을 막음' · 화면 '접속 막음 · 11/11 값' · 21일 알림 안 냄 · 주 1회 SKU 차례에서 다시 열렸는지 확인 —
    v1.20 푸마 일본과 같은 처리 · 미국·멕시코·두바이 몰은 그대로) ② HTTP 200 봇 확인 화면 알아보기(_challenge — HTML 30KB 밑 + 'Client Challenge'·'Just a moment...' 같은 제목이나
    /_fs-ch-·challenges.cloudflare.com·captcha-delivery·px-captcha 표식) → 403처럼 그 실행에서 그 사이트에 더 요청 안 함 · 까닭 '봇 확인 화면(접속 차단 — 우회하지 않음)'(전에는 'JSON-LD 없음')
v1.21: (SKU 9차 · 정기 차례 11/17 · 대표 상시 지시 2026-10-26) 상품이 적은 브랜드부터 — 푸마 디비에이트 나이트로 엘리트 트레일 여성(310468 · 한국·미국·독일·멕시코)·
    포에버런 나이트로 2(310109 · 한국·미국·독일·두바이)·킹 인도어(401683 · 한국·미국·멕시코·두바이) · 헌터 리파인드 슬림핏 숏(WFS2200RMA · 한국·영국·일본)·플레이 비건 시어링
    인슐레이티드 톨(WFT2235RMA)·인트레피드 톨 스노 부츠(WFT2108WWU · 각 한국·영국) · 써코니 엔돌핀 아주라(S21070 · 한국·미국·영국·독일)·엔돌핀 트레이너(S20996 · 한국·영국·독일)
    → 상품 122개 · 값 505개(+26 · 11/17 GitHub 서버에서 모두 정가 읽기 확인) · 멈춘 사이트 그대로: 브룩스 한국(443 연결 거부 — 80은 brookssports.co.kr로 넘김)·푸마 일본(robots.txt까지
    Cloudflare 봇 확인 화면 403) · 푸마 팔레르모 프리미엄·이지 라이더 빈티지·시부이 캣·팔레르모 레더는 한국 페이지 404라 뺌 · 써코니 엑소더스 울트라 4는 한국 몰 가격 없음(품절) ·
    헌터 코오롱몰 상품 번호는 목록 화면에서 품번 바로 앞 /Product/K… (상품 이름 끝 품번으로 정가 읽기에서 다시 확인)
v1.20: (대표 지시 2026-11-11 '추천 순서대로' — 블프 전 해외 정가 빈칸 줄이기) ① 푸마 일본(jp.puma.com)이 11/10부터 robots.txt까지 Cloudflare 봇 확인 화면(HTTP 403 ·
    11/11 GitHub 서버 확인 — 우회하지 않음) → PAUSED에 넣음(why '일본 공식몰이 자동 접속을 막음' · 화면 '접속 막음 · 11/03 값' · 21일 알림 안 냄 · 요청 안 함 —
    주 1회 SKU 차례에서 우리 봇으로 다시 열렸는지 확인하고 열리면 뺌) ② 온러닝: 옛 클라우드몬스터(61.98434 — 한국)·남성 클라우드노바 2(3ME30210108 — 한국·일본)가 11/10부터 그 나라 몰에서
    빠져 상품 주소가 목록(/shop)으로 넘어감('JSON-LD 없음'으로 보였음) → 클라우드몬스터 1(3MF30740553 · 한국·미국·영국·독일 — 일본 몰에 없음) · 클라우드몬스터 1
    워터프루프(3MG10701043 · 5개 나라 · id on-cloudmonster1wp) — 11/11 나라별 상품 사이트맵(https://www.on.com/{loc}/products.xml)·정가 읽기 확인 · 상품 114개 · 값 479개 ·
    온러닝 상품 주소가 목록으로 넘어가면 까닭을 바로 적음('상품 페이지가 목록(/ko-kr/shop)으로 넘어감 — 그 나라 몰에서 빠짐') · 다른 모델 페이지로 넘어가도 실패(같은 모델 다른 색상은 예전처럼 —
    11/11 브랜치 실행: 클라우드틸트 한국·로저 일본이 다른 색상으로 넘어감 · 정가는 모델마다 같음)
v1.19: (대표 확인 2026-11-10 '브룩스 한국 공식몰은 리뉴얼 중 — 접속은 되는데 조회되는 정보가 없음' · 결정 '리뉴얼 표시 + 알림 끔') 수집을 잠시 멈추는
    사이트 PAUSED {사이트: {since, why}} — 그 사이트 값은 요청하지 않고(robots.txt도 안 받음) 이전 값을 그대로 두며 값에 표시 paused = 까닭
    (화면 '리뉴얼 중 · 11/3 값' — build_dashboard v33.32) · 받은 값·못 받은 값 셈('절반 넘게'·브랜드 통째)과 21일 알림에서 뺌 · 이전 값도 없으면
    값 없음 기록(failed)도 지움(알림 안 냄) · 로그 '건너뜀 — 한국 공식몰 리뉴얼 중(수집 멈춤 · 11-03부터) · 이전 값(11-03 받은 값)'('실패'·[WARN] 없음) ·
    표시는 실행마다 지금 PAUSED로 다시 매김(받지 않는 날도) — PAUSED에서 빼면 그 값은 다음 실행에서 바로 다시 받고(주 1회를 기다리지 않음 · 다시 받기) 알림도 예전대로 ·
    지금 brooksrunning.co.kr(11/03부터 GitHub 서버에서 443 연결 거부 — 리뉴얼). 리뉴얼이 끝나면 주 1회 SKU 차례에서 새 주소·상품 번호로 다시 연결하고 PAUSED에서 뺌
v1.18: (SKU 8차 · 정기 차례 11/10 · 대표 상시 지시 2026-10-26) 상품이 적은 브랜드부터 — 푸마 T7 올웨이즈 온 숏 트랙 자켓(여성 629796 · 6개 나라) ·
    언더아머 언디나이어블 5.0 더플백 라지(1369224)·UA 레인 6(3027341 · 각 6개 나라) · 나이키 코트 비전 로우 넥스트 네이처(DH2987-101 · 7개 나라)
    → 상품 114개 · 값 481개(+25 · 써코니 영국·독일 −2 · 11/10 GitHub 서버에서 25개 모두 정가 읽기 확인) · 써코니 엔돌핀 스피드 5: 영국·독일 몰에서 빠짐(10/30부터 HTTP 404 —
    유럽은 엔돌핀 스피드 6 S101825로 바뀌었고 한국 몰엔 아직 6이 없음) → 영국·독일 뺌, 한국 화이트/검 페이지가 전 사이즈 품절로 가격 칸이 비어
    화이트/크림슨(220 · 219,000원)으로 · 브룩스 한국(brooksrunning.co.kr)은 11/03부터 GitHub 서버에서 열리지 않음(443 연결 거부 · 80은
    brookssports.co.kr 빈 페이지로 넘김 — 몰 쪽 문제로 보임, 공식 링크 페이지는 그대로 이 주소) — 코드는 그대로(이전 값 유지)
v1.17: (대표 지시 2026-11-03 '두바이 추가해주세요') 나라에 두바이(AE · UAE 공식몰 · 디르함 AED · 부가세 5% 포함) — 같은 품번을 GitHub 서버에서 확인한
    4개 브랜드 나이키 6 · 푸마 6 · 언더아머 7 · 온러닝 9(값 +28 → 상품 110개 · 값 458개 · 11/03 브랜치 시험).
    ① 나이키 상품 정보(product_feed)에는 두바이가 없음(AE 정가 100000 자리표시 · 다른 품번은 결과 없음) → 나이키 상품에 나라별 페이지 주소 urls(AE = nike.ae
       공식몰 · GMG 운영)를 두고 그 나라만 페이지로 읽음 — 묶음·다시 받기·값 없음 기록·할인 가드·크게 바뀜은 그 나라를 페이지 값처럼(_feed · ccs)
    ② nike.ae·underarmour.ae(SFCC SFRA)는 취소선 정가가 글자 대신 content 칸이고 추천 상품 칸에도 취소선 정가가 있음 → SFRA_LIST(sfra_list): 이 상품
       품번 표시(data-variation-group-id = NK·UA + 품번)를 확인하고, 이 상품 가격 칸(b-pdp__priceline 등 — 추천 상품 칸 product-tile은 뺌)의 취소선 정가 중
       곁 판매가가 JSON-LD 판매가와 같은 것 · 이 상품 GTM 상세(판매가 price · 정가 item_original_price)와 맞아야 함 · 할인 중인데 취소선 정가를 못 읽으면
       실패(할인가를 정가로 쓰지 않음) · 회원 전용 상품은 실패
    ③ on.ae(쇼피파이)는 할인 표시(compare_at_price) 없이 일부 색상 값만 내림 → SHOP_MODEL: 같은 모델(품번 앞 7자리) 다른 색상보다 낮으면 처음 값으로는
       쓰지 않음(이전 값이 있으면 할인 가드가 정가를 지킴) · 상품 .json은 변형 250개까지만(클라우드 6·클라우드서퍼 2가 250개 — 비교는 응답에 온 색상끼리,
       이 색상이 잘려 빠지면 '대응표 확인' 대신 '변형 250개에서 잘림')
    ④ 써코니·브룩스 두바이 몰(SVD)은 robots.txt까지 우리 봇에 405 차단 페이지(우회 안 함) · 아크테릭스·살로몬·닥터마틴·헌터·킨·드래곤디퓨전·우포스는
       UAE 공식 온라인몰 없음 · 나이키 블레이저·코르테즈·조던 1 로우 두바이는 사이트맵에 없는 재고 정리 페이지(할인가만 · 품절)라 뺌 ·
       푸마 디비에이트 나이트로 엘리트 트레일(JSON-LD 없음)·온 클라우드몬스터(옛 모델 재고 정리 — 모든 색상 같은 낮은 값)는 뺌
v1.16: (SKU 늘리기 7차 11/03 — 주 1회 정기 차례 · 대표 상시 지시 2026-10-26) 나이키 에어맥스 플러스·킬샷 2 레더(6개 나라) · 브룩스 글리세린 23·
    고스트 맥스 4·캐스캐디아 20(남성 · 한국·일본) · 우포스 OOcloog+·OOmy Stride·OOahh Sport(한국·미국) — 상품 110개 · 값 430개(+24).
    브룩스 한국 robots.txt 사이트맵은 카페24 데모 사이트(ecudemo…)라 첫 화면·목록 상품 번호 → 상품 페이지 prd_model 품번 · 일본 트레일 모델 품번은
    BMM…(캐스캐디아 20 BMM4893 · 로드는 BRM…) · 우포스 OOahh Sport 블랙은 미국 몰에 FootJoy 콜라보뿐이라 두 몰에 다 있는 택티컬 그린 ·
    드래곤디퓨전 새 모델(유벤투스백 W2BAS26023)은 글로벌 몰 사이트맵에 없어 이번엔 없음
v1.15: (SKU 늘리기 6차 10/29 — 대표 '네 1번부터 진행해주세요') 아크테릭스 노반 LD 4 GTX·사일렌 2·크래그·컨실 트렉 부츠·노반 재킷(남성 · 5개 나라 같은 품번)
    — 상품 102개 · 값 406개(+25). 한국 몰은 목록 화면이 스크립트로 그려져 상품 번호가 페이지에 없음 → 공개 기획전 페이지(arcteryx.co.kr/lp)의
    상품 이미지 주소 products/{상품 번호}/S26_X0000{모델}에서 상품 번호를 찾아 상품 페이지 Model(KR) 품번으로 확인(몰 내부 API는 쓰지 않음) ·
    일본 몰 신발 페이지는 JSON-LD가 없어 상품 .json(변형 품번 X0000…) · 코펙 2 로우 GTX는 영국·독일 몰 404·일본 몰에 없어 뺌 · 노반 LD 4는 다음 차례
v1.14: (SKU 늘리기 5차 10/28 — 대표 '네 바로 진행해주세요', 쇼피파이 몰이 아닌 브랜드부터) 온러닝 클라우드몬스터 3·클라우드러너 3·클라우드 X 5·
    클라우드 6 워터프루프(검정 · 5개 나라 같은 품번) — 상품 97개 · 값 381개(+20). 온러닝 상품은 https://www.on.com/sitemap.xml(robots.txt에는 없음 · ko-kr 상품 사이트맵)에서 찾음.
    아크테릭스는 한국 몰 목록 화면이 스크립트로 그려져(상품 번호가 페이지에 없음) 이번에 못 찾음 — 다음 차례에 다른 방법
v1.13: (SKU 늘리기 4차 10/28 — 대표 '네 진행해주세요', v1.12 묶음 동시 받기로 시간 여유) 브룩스 아드레날린 GTS 25·하이페리온 3(한국·일본) ·
    킨 하우저 III 슬라이드·유니크 트레커·A86(5개 나라)·재스퍼 자이오닉 워터프루프(한국·미국·일본 — 영국·독일 몰에 없음) — 상품 93개 · 값 361개(+22).
    카페24 몰 소비자가 칸(CAFE24_LIST · 브룩스 한국): 할인 중이면 JSON-LD에 판매가만이라, 이 상품 판매가 칸 바로 뒤 소비자가(price_custom)를 정가로
    (판매가 칸이 이 상품 JSON-LD 판매가와 같고 소비자가가 한 가지일 때만 · 판매가보다 높고 5배 안) — 10/28 블랙프라이데이 GTS 25 판매가 132,300 · 소비자가 189,000.
    브룩스 고스트 맥스 3(607)은 10/27·10/28 모두 한국 몰 pageNotFound라 후보에서 뺌 · 온러닝은 robots.txt에 사이트맵이 없어 다음 차례에 다른 방법으로
v1.12: (대표 승인 10/28 '1번(수집 방식 변경)부터' — 전체 받기 615초 = 13분 한도의 79%라 SKU를 더 늘리면 한도에 걸림) 묶음 동시 받기.
    지금까지는 모든 요청이 한 줄로 1.5초씩 띄워져(339건 × 1.5초 ≈ 500초) 사이트와 상관없이 오래 걸림 → 브랜드·사이트가 이어진 상품끼리 한 묶음
    (코오롱몰 = 드래곤디퓨전+헌터 · LANE_JOIN 킨+우포스 = LF 수입사 몰)으로 나눠 묶음 6개까지 동시에 받음.
    묶음 안은 지금과 같은 순서·간격(1.5초 · 살로몬 해외 8초·한 실행 8건) · 같은 사이트는 묶음과 상관없이 한 번에 한 요청·1.5초 넘게 ·
    여러 회사가 함께 쓰는 쇼핑몰 플랫폼(쇼피파이 — .json 상품·PACE_EXTRA, 카페24, 고도몰)은 묶음을 넘어서도 지금처럼 한 줄로 1.5초(PACE — 그 몰의
    robots.txt·다른 이름 사이트로 넘겨진 요청도) — 한 사이트·플랫폼이 받는 요청 빠르기는 그대로(SFCC형 몰은 브랜드마다 따로 운영이라 사이트별 간격만).
    430(쇼피파이가 우리 서버를 거절)도 차단으로 봄 — 그 실행에서 쇼피파이 몰 모두 더 요청 안 함. 결과는 값마다 모아 PRODUCTS 순서로 합침(파일·알림 규칙 그대로 —
    받은 날·다시 받기·한도 미룸·21일 알림). 묶음이 13분 + 60초 안에 안 끝나면 멈추고 남은 값은 시간 초과처럼 이전 값(내일 다시) · 묶음 안에서
    예상 못 한 오류가 나면 저장하지 않고 멈춤(예전과 같음). update.yml 수동 실행 입력 price_lanes(PRICE_LANES) — 비우면 6, 1이면 예전처럼 차례대로.
    로그 '해외 정가 묶음 …' 줄에 묶음별 걸린 시간(가장 긴 묶음 = 전체 받기 시간의 기준).
    브랜치 시험(10/28 · GitHub 서버 실제 수집): 141초(10/27 615초) · 받음 331/332(10/27과 같음 — 써코니 한국 1건 연결 끊김 · 살로몬 해외 7건 한도 미룸) ·
    차단(403·429·430) 0건 · 가장 긴 묶음 킨+우포스 131초·드래곤디퓨전+헌터 125초(쇼피파이 몰 줄이 기준 — 쇼피파이 값 하나 늘 때 약 1.5초).
v1.11: (SKU 늘리기 3차 10/27 — 대표 '계속 진행하시지요', 상품이 적은 브랜드부터) 닥터마틴 아드리안·8065 메리제인·싱클레어·1461 모노(한국·미국·영국) ·
    푸마 스피드캣 GO 여성(한국·미국·일본·멕시코)·디비에이트 나이트로 엘리트 트레일(한국·미국·독일) — 상품 87개 · 값 339개(+19). 브룩스 아드레날린 GTS 25는 이번에도,
    고스트 맥스 3·하이페리온 3은 처음 시험에서 한국 몰 페이지가 pageNotFound(사이트맵에는 있음 · 기존 고스트 18은 정상 · 10/27 실행 3번)라 뺌 · 푸마 팔레르모 프리미엄은 한국 404
v1.10: (SKU 늘리기 2차 10/27 — 대표 상시 지시 '브랜드 별 주요 SKU는 계속 늘려주세요', 값이 적은 브랜드부터) 드래곤디퓨전 난터켓 빅 백·청키 펠리니 포셰트
    (한국·미국) · 헌터 오리지널 톨 글로스(한국·미국·영국·일본)·숏 글로스(한국·미국·영국) — 상품 81개 · 값 320개(+11). 써코니 엔돌핀 프로 5 미국은
    색상 없는 주소가 10/23부터 JSON-LD 없는 페이지라 색상(품번) 지정 주소로. 브룩스 아드레날린 GTS 25는 한국 몰 상품 페이지가 시험 중 없어져(pageNotFound) 다음 차례에
v1.9: (v1.8 검토 반영 10/26) ① 다시 받기에서는 한도 사이트 값 가운데 이번 주기에 아직 다시 받아 보지 않은 값(미룬 값·새 값·전체 받기 날 못 받은 값 —
    값마다 마지막으로 받으러 간 날 host_try로 가름)을 먼저, 다시 받기에서 이미 못 받은 값은 남은 한도로만 — 계속 실패하는 값이 한도를 다 써서
    다른 값이 영영 안 받히지 않게 ② 한 주기(7일+1) 넘게 미뤄진 값은 이전 값 표시·21일 알림에, 이전 값도 없는 값은 '값 없음'으로 ③ 이번 주기에
    잘 끝난 실행이 있으면 그 뒤 다시 받기는 조용히(미룬 값 때문에 다시 받기 날이 늘어도 매일 빨간 X 없음) ④ 값마다 다시 받기는 한 번 —
    다시 받기에서도 못 받은 값만 남으면 다음 날 다시 받지 않고 다음 주에(미룬 값 로그도 '다음 주에')
v1.8: (대표 지시 2026-10-26 '살로몬 차단 문제 점검') 살로몬 해외(www.salomon.com)는 요청 간격(8초)과 상관없이 한 실행 10번째 요청에서 403 —
    10/22·10/23·10/26 전체 받기마다 같은 6건이 막히고 다음 날 다시 받기(6건)는 다 받힘 → 한 실행 요청 한도 HOST_CAP(살로몬 해외 8건)까지만 받고
    나머지는 다음 실행으로 미룸(Defer — 이전 값 그대로 · 실패·'이전 값' 표시 아님 · tried로 다음 날 그 값만) — 차단을 일으키지 않게
v1.7: (대표 상시 지시 2026-10-26 '브랜드 별 주요 SKU는 계속 늘려주세요' — 1차) 언더아머 아이콘 플리스 후디(1373880)·히트기어 모크 민소매(1361521)
    — 5개 나라 같은 품번 · GitHub 서버에서 정가 읽기 확인(10/26)
v1.6: (대표 지시 2026-10-26 '언더아머 멕시코는 다른 상품으로') 언더아머 히트기어 컴프레션 반팔(1361518)·긴팔(1361524)이 멕시코 몰에서 빠져(HTTP 410 ·
    사이트맵에 없음) 5개 나라 몰에 같은 품번이 있는 히트기어 컴프레션 모크 반팔(1372586)·허슬 6.0 백팩(1384672)으로 바꿈(GitHub 서버 시험 10/26 — 5개 나라 정가 읽힘)
v1.5: (대표 지시 2026-10-26 '추천 순서대로' 5번 — 블프 전) 할인가·정가 변동 기록. ① 할인가 sp = 그 상품 색상·사이즈 중 지금 가장 싼 값
    (나이키 currentPrice · 쇼피파이 변형 가격 · JSON-LD 판매가 · 고도몰 판매가 — 이미 읽던 값을 버리지 않고 저장 · 정가보다 0.5% 넘게 낮을 때만,
    할인 가드로 정가를 지킨 날은 이번에 보인 값도 할인가 후보) · 확인한 날 sp_date ② 할인 기록 sh = [날짜, 할인가 또는 null(할인 끝)] —
    할인 시작·끝·할인가가 바뀐 날만, 최근 20개 ③ 정가 변동 기록 ph = [날짜, 이전 정가, 새 정가] — 정가가 0.5% 넘게 바뀐 날만(크게 바뀜·할인
    가드는 반영된 날), 최근 12개 · 통화가 바뀌면 기록을 새로. 화면(build_dashboard v33.23)·주간 메일(weekly_digest v1.14 '■ 해외 정가 변동')이 씀
    · 할인은 화면에 보이는 정가 p 기준(크게 바뀌어 보류 중인 날은 할인 판단 안 함 — 보류 전에 '할인 아님'을 본 것은 off_seen으로 이어 감) ·
    언제 시작했는지 모르는 할인(v1.5 전부터 할인 중 · 새 상품·나라)은
    첫 기록에 'base'([날짜, 할인가, "base"]) — 주간 메일이 '할인 시작'으로 세지 않음
v1.4: (대표 지시 2026-10-22 '스포츠 브랜드는 모두 추가하고 싶습니다' — 봇 차단은 우회하지 않고 되는 곳만) 아크테릭스 6 · 킨(KEEN) 6 · 우포스 7 추가
    (상품 56 → 75개 · 값 227 → 299개 · 나라별 같은 품번을 GitHub 서버에서 확인 — 브랜치 시험 10/23 72/72).
    ① 아크테릭스 한국(아머스포츠코리아 공식몰): 시즌 상품 페이지마다 한국 품번(Model(KR) — PRODUCTS cc_code KR, 시즌이 바뀌면 주소와 함께 바꿈) ·
       JSON-LD는 판매가뿐이라 화면 데이터의 정가 retail_price — 같은 { } 묶음에 이 상품 품번이 있고 판매가(sell·last)가 JSON-LD 가격과 같을 때만, 판매가의 5배 안.
       미국·영국·독일(arcteryx.com)·일본(쇼피파이 페이지)은 JSON-LD 품번(X0000…) · 맨티스 26 일본은 옛 모델이라 뺌.
    ② 킨·우포스 한국(수입사 LF 공식몰 — 고도몰, JSON-LD 없음): 상품 정보 칸 품번(ARTICLE · Article No.)이 이 상품 품번과 같을 때만
       주문 칸 숨은 값 정가(set_goods_fixedPrice)·판매가(set_goods_price) 중 높은 값(godo_price · 같은 칸 값이 여러 가지면 실패).
       우포스 콜라보 상품은 같은 Article No.라 상품 번호(goodsNo)로 고름 · 우포스는 영국·독일·일본·멕시코에 공식 온라인몰이 없어 한국·미국만.
    ③ 쇼피파이 변형 품번이 바코드인 몰(킨 미국·독일·일본)은 상품 태그에 품번이 있으면 그 상품(헌터처럼 상품 주소에 품번이 없음).
    ④ 한 실행 최대 11 → 13분(update.yml 해외 정가 단계 13 → 15분 · 작업 32 → 34분).
    ⑤ 넣지 못한 브랜드(접속 시험·조사 10/21~23): 아디다스·뉴발란스·아식스·오니츠카타이거·룰루레몬·오클리(봇 차단 403/429) ·
       크록스·스케쳐스(한국 몰 차단) · 호카(한국 공식 온라인몰 없음) · 미즈노(한국 공식몰에 현재 모델 없음) · 노르다·CEP(한국 공식몰 없음) ·
       안다르(한국몰 상품 페이지에 자체 품번이 없어 일본 공식몰 상품과 같은지 확인 불가).
v1.3: (대표 지시 2026-10-22 '브랜드별 대표 인기 상품으로 골라서 추가 — 최소 5개 이상씩') 상품 13 → 56개(브랜드마다 5~7개 · 값 227개 —
    나라별로 같은 품번을 GitHub 서버에서 확인한 것만 · 그 나라 몰에 없거나 품번·사양이 다르거나 할인가가 정가로 보이면 그 나라는 뺌, 이유는 상품 줄 주석).
    ① SFCC형 몰(푸마 한국 등)이 가격인하 중이면 JSON-LD에 판매가만 있어, 이 상품 가격 칸의 취소선 정가(strike-through list)를 정가로 —
    취소선 곁 판매가 칸 값이 이 상품 판매가와 같을 때만(추천 상품 칸 섞임 방지 · 검토 반영) · 판매가보다 높고 5배 안(푸마 한국 팔레르모 10/22 119,000 → 35,700원 · 70% 할인)
    ② 한 실행 최대 6 → 11분(값 1개 약 2초 · update.yml 해외 정가 단계 8 → 13분 · 작업 25 → 32분) ③ 온러닝·살로몬 나라별 주소 도우미 _on·_sal.
    ④ 브랜치 시험(10/22 · 216/223 · 385초): 살로몬 해외가 9번째 요청 뒤 403(우회 안 함) → 같은 사이트 요청 간격 HOST_GAP(살로몬 해외 8초) ·
    몇 값만 못 받은 날(사이트가 중간에 막음·연결 끊김 — 써코니 한국 1건)도 다음 날 그 값만 한 번 더(알림 없이) · 같은 사이트가 연달아 2번
    응답 없으면(연결 오류·시간 초과) 그 실행에서 건너뜀(한 사이트가 11분을 다 쓰지 않게) · 푸마 인헤일 → 디비에이트 나이트로 엘리트 4
    (인헤일은 미국 몰이 전 색상 할인가 73.99달러뿐 — 할인가가 정가로 보이면 그 나라는 뺀다는 기준 · 다른 나라 몰에는 없음).
v1.2: (대표 지시 2026-10-22 '추가 가능 5곳 넣어주세요') 드래곤디퓨전·헌터·언더아머·써코니·브룩스 대표 상품 추가(접속 시험 10/22 —
    나라별 같은 상품 주소·가격 칸을 GitHub 서버에서 확인). ① 상품 페이지에 JSON-LD가 없고 schema.org 마이크로데이터(itemprop)만 있는
    SFCC형 몰(써코니 해외) — 이 상품 품번(data-stock-number)이 있을 때만, 판매가(itemprop price · 가능하면 priceincents)와
    '원래 가격'(price-standard — 판매가가 이 상품 가격과 같을 때만)을 읽음 · 독일식 소수점(190,00)도 ② 쇼피파이 변형 품번이 바코드인 몰
    (헌터 미국·영국)은 상품 주소(handle)에 품번이 있으면 그 상품 ③ 그 나라 수입사 품번이 따로 있으면 cc_code(브룩스 일본 BRM4933)
    ④ 이름으로 찾는 상품 중 code_in_page면 페이지에 품번이 있어야 함(써코니·브룩스 한국 — 품번이 JSON-LD 밖 상품 정보 칸에만 있음).
    브랜치 시험(10/22): 56/56 받음 — 써코니 독일은 할인 중(€160 → €128)인데 '128,00 &#8364;'의 HTML 기호 숫자가 섞여 원래 가격을 못 읽음 → 기호를 먼저 풂.
    검토 반영: 쇼피파이 .json도 변형의 통화(price_currency)가 그 나라 통화가 아니면 실패(멕시코 서버면 페소가 달러로 저장될 수 있음 —
    해외 쇼피파이 몰이 생겨서) · cc_code를 바꾸면 그 나라 이전 값은 쓰지 않음(prices.json items에 cc_code 저장) ·
    마이크로데이터 priceincents는 다음 가격 칸으로 넘어가 읽지 않음.
v1.1: (2026-10-22 main 첫 수집에서 푸마 멕시코가 전 색상 30% 세일이라 할인가 1,539.3페소가 정가로 저장됨 — JSON-LD에 정가 표기 없음)
    SFCC형 몰 화면 데이터의 "c_listPrice"(정가)·"c_salePrice"(판매가)를 정가 명세로 읽음 — 판매가가 이 상품 JSON-LD 가격과 같을 때만
    (추천 상품 섞임 방지 · 정가는 판매가의 1~3배일 때만). 푸마 멕시코 확인(2026-10-22 브랜치 진단: c_listPrice 2199 · c_salePrice 1539.3).
v1: (대표 지시 2026-10-21 '국가별 브랜드 대표상품 소비자가격 — 미주·유럽·중남미 vs 한국 RRP' · 수기 없음 · 할인 전 풀프라이스 ·
    환율로 한국이 몇 % 싸거나 비싼지 · 브랜드 상세 하단 · 나이키 포함) 브랜드 공식몰의 같은 상품(글로벌 품번)을 나라별로 받아
    docs/prices.json에 저장 — 원화 환산·차이(%)는 화면(build_dashboard)이 그날 환율(data.json fx)로 계산.
    ① 나이키 = 나이키 상품 정보(api.nike.com product_feed, styleColor로 찾음)의 정가 fullPrice — 할인 중이어도 정가가 따로 있음
    ② 그 밖의 공식몰 = 상품 페이지의 구조화 데이터(schema.org JSON-LD): 정가 명세(ListPrice·StrikethroughPrice)가 있으면 그 값,
       없으면 그 상품 색상·사이즈별 가격 중 가장 높은 값(일부 색상만 할인일 때 정가) · 살로몬 해외는 기본가(basePrice)
    ③ 한국 쇼피파이형 몰(살로몬·닥터마틴) = 상품 .json의 compare_at_price(정가)·price 중 높은 값, 변형(사이즈)의 품번이 글로벌 품번과 같아야 함
    찾는 상품 = 글로벌 품번이 품번·주소에 있는 JSON-LD 상품 우선(없을 때만 이름의 모델명 — 관련·추천 상품 칸은 빼고, 이름이 다른
    상품이 여럿이면 실패) — 추천·관련 상품 가격이 섞이지 않게. 넘겨짐(3xx)은 직접 따라가며 매번 robots.txt·막힘을 먼저 확인.
    할인 가드: 이번 값이 저장된 정가보다 낮으면(모든 색상이 할인 중일 때) 120일 동안은 저장된 정가를 지킴(obs에 이번 값) — 그 뒤에도 낮으면 새 정가.
    나이키 fullPrice는 정가 자체라 가드 없이 바로 반영. 정가가 1.5배 넘게 오르면(나이키는 내려도) 바로 바꾸지 않고 다음 확인 때
    비슷하면(10% 안) 반영(cand).
    주 1회(7일) — 매일 update-dashboard 안에서 돌되 7일이 안 지났고 상품 목록이 같으면 건너뜀(update.yml 수동 실행 입력 price_force=1 → PRICE_FORCE=1이면 바로).
    절반 넘게 실패했거나, 한 브랜드 값을 하나도 못 받았거나, 시간 초과로 다 못 받은 날은 '받은 날'(fetched)을 옮기지 않고 다음 날
    그때 못 받은 값만 다시 받음(tried · 다시 받기도 못 받으면 실패 표시 · 다음 주 받을 날이면 전체를 다시). 전체 받기는 잘 끝났는데
    몇 값만 못 받은 날도 다음 날 그 값만 한 번 더(v1.3 · 또 못 받아도 알림 없이 다음 주에 — 21일 기준은 그대로).
    상품의 품번을 바꾸면 그 상품의 이전 값·값 없음 기록은 쓰지 않음(id가 같아도 다른 상품).
    봇 차단은 우회하지 않음: 우리 봇 이름(UA)을 밝히고 robots.txt(RFC 9309 — 우리 이름 그룹 우선·* 와일드카드·가장 긴 규칙)를 먼저 확인,
    robots.txt가 서버 오류·연결 안 됨이면 그 사이트는 이번 실행 건너뜀(예외: robots.txt를 두지 않는 API 주소는 같은 회사 대표 사이트의
    robots.txt를 따름 — ROBOTS_ALT), 403/429를 받으면 그 사이트에 더 요청하지 않음, 주소당 1번만 요청
    (접속 시험 2026-10-21: 아디다스·뉴발란스·아식스·크록스 한국·에코·몽클레르·룰루레몬·랄프로렌·어그·스케쳐스 한국은 403/429라 넣지 않음).
    못 받으면 이전 값(stale_since = 마지막으로 받은 날) · 전에 받던 값이 '팔지 않음'으로 바뀌어도 실패로 셈 · 이전 값도 없으면 failed(값 없음, 처음 실패한 날).
    한 실행에서 절반 넘게 실패하거나, 한 값이 21일 넘게 이전 값·값 없음이면 실패 표시(soft_fail.txt).
    나라를 늘리면 MK + build_dashboard PR_ORD·PR_CC·PR_SYM·LAND(lvat · 운임 출발지가 있으면 fcol — 없으면 '운임 없음')·_partial ccn +
    weekly_digest CC_KO·CUR_SYM + (새 통화면) fetch_data FX·build_dashboard FX_LBL를 함께 고친다.
    (v1.17 나이키 상품 정보에 없는 나라는 MK 첫 칸을 None으로 두고 나이키 상품 urls에 그 나라 페이지 주소)
"""
import collections, contextlib, datetime, hashlib, json, os, re, sys, threading, time, traceback, urllib.parse
from html import unescape
import requests

SCRIPT = "price_fetch"
OUT = "docs/prices.json"
KST = datetime.timezone(datetime.timedelta(hours=9))
BOT = "sports-industry-monitor"   # robots.txt에서 우리를 가리키는 이름(UA 안의 이름과 같게)
UA = f"Mozilla/5.0 (compatible; {BOT} price bot; +https://github.com/Jaemin85-Claude/sports-industry-monitor)"
HDR = {"User-Agent": UA, "Accept": "text/html,application/json;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.8,ko;q=0.6"}
DAYS = 7            # 주 1회
SALE_GUARD = 120    # 일 — 이 기간 안에 정가보다 낮게 보이면 할인으로 보고 정가를 지킴
STALE_ALERT = 21    # 일 — 이 일수 넘게 이전 값이면 실패 표시
TIME_LIMIT = 13 * 60   # 초 — 한 실행 최대(넘으면 남은 것은 이전 값) · v1.3 상품 56개·값 227개(1개 약 2초)라 6 → 11분 · v1.4 값 299개라 13분
                       # v1.12 묶음 동시 받기로 전체 받기 약 2~3분 — 13분은 여유로 둠
GAP = 1.5           # 초 — 요청 사이 쉬는 시간(v1.12 묶음 안 · 같은 사이트 · 같은 플랫폼(PACE) 각각)
LANES = 6           # v1.12 동시에 받는 묶음 수(update.yml 수동 실행 입력 price_lanes → PRICE_LANES · 1이면 예전처럼 차례대로)
LANE_GRACE = 60     # 초 — 묶음이 TIME_LIMIT + 이만큼 안에 안 끝나면 멈추고 남은 값은 이전 값(단계 15분 제한 전에 저장)
LANE_JOIN = [("킨(KEEN)", "우포스")]   # v1.12 사이트는 다르지만 같은 회사·수입사 몰 — 한 묶음(차례대로) · 킨·우포스 한국 = LF 공식몰(고도몰)
PACE_EXTRA = {"arcteryx.jp": "shopify", "dragondiffusion.com": "shopify",   # v1.12 여러 회사가 함께 쓰는 플랫폼 — 묶음을 넘어 한 줄로 GAP
              "saucony.co.kr": "cafe24", "brooksrunning.co.kr": "cafe24",   # (쇼피파이 .json 상품 주소의 사이트는 저절로 shopify)
              "www.keenfootwear.kr": "godo", "www.oofos.co.kr": "godo"}     # SFCC형 몰(푸마·언더아머·써코니 해외)은 브랜드마다 따로 운영(자체 CDN)이라 넣지 않음 — 사이트별 간격만
HOST_GAP = {"www.salomon.com": 8}   # 초 — 같은 사이트 요청 사이 최소 간격(v1.3 · 10/22 브랜치 시험에서 살로몬 해외가 9번째 요청 뒤 403 — 천천히 요청)
HOST_CAP = {"www.salomon.com": 8}   # v1.8 한 실행에서 그 사이트에 보낼 상품 페이지 요청 수 — 살로몬 해외는 간격과 상관없이 10번째 요청에서 403(10/22·10/23·10/26 실행 4번 모두)
                                    # → 8건까지만 받고 나머지는 다음 실행(다음 날 다시 받기)으로 미룸 — 차단을 일으키지 않게(우회 아님 · 실패로 세지 않음)
JUMP = 1.5          # 배 — 정가가 이만큼 넘게 바뀌면 다음 확인 때 같아야 반영
PAUSED = {"brooksrunning.co.kr": {"since": "2026-11-03", "why": "한국 공식몰 리뉴얼 중"},   # v1.19 수집을 잠시 멈춘 사이트(대표 확인 2026-11-10) —
          "jp.puma.com": {"since": "2026-11-10", "why": "일본 공식몰이 자동 접속을 막음"},   # v1.20 11/10부터 robots.txt까지 Cloudflare 봇 확인 화면(HTTP 403 · 11/11 GitHub 서버 확인) — 우회하지 않음
          # v1.22 언더아머 한국·영국·독일 몰이 11/17부터 상품 페이지 대신 봇 확인 화면('Client Challenge' · HTTP 200 · 3KB — 11/17 GitHub 서버 확인) — 우회하지 않음 · 미국·멕시코·두바이 몰은 그대로
          "www.underarmour.co.kr": {"since": "2026-11-17", "why": "한국 공식몰이 자동 접속을 막음"},
          "www.underarmour.co.uk": {"since": "2026-11-17", "why": "영국 공식몰이 자동 접속을 막음"},
          "www.underarmour.de": {"since": "2026-11-17", "why": "독일 공식몰이 자동 접속을 막음"}}
                                    # 요청 안 함 · 이전 값 그대로 + 표시 paused · 셈·21일 알림에서 뺌 · 다시 열리면 주소·상품 번호를 고치고 여기서 뺌
CAFE24_LIST = {"brooksrunning.co.kr"}   # v1.13 소비자가 칸(price_custom)을 할인 전 정가로 읽는 카페24 몰 — 그 칸이 실제 정가인지 확인한 몰만(10/28 브룩스 한국:
                                         # 글리세린 맥스 2 소비자가 249,000 = 세일 전 받은 정가 · 아드레날린 GTS 25 189,000 · 블랙프라이데이 판매가 132,300)
SFRA_LIST = {"www.nike.ae": "NK", "www.underarmour.ae": "UA"}   # v1.17 두바이 SFCC(SFRA) 몰 → 이 상품 품번 표시(data-variation-group-id) 앞 글자 — sfra_list로 정가 확인
SHOP_MODEL = {"on.ae": 7}   # v1.17 할인 표시 없이 일부 색상 값만 내리는 쇼피파이 몰 → 같은 모델로 볼 품번 앞 글자 수(온러닝 3MG1005… = 모델·성별)
                            # 상품 .json은 변형 250개까지만 — 11/03 cloud-6·cloudsurfer-2가 250개에서 잘림(cloudmonster-3 243개) → 같은 모델 비교는 응답에 온 색상끼리만
SH_MAX, PH_MAX = 20, 12   # v1.5 할인 기록·정가 변동 기록 최대 개수(오래된 것부터 버림)


def note_sale(o, now, td, seen_off=False):
    """v1.5 할인가(sp)·할인 기록(sh) — now = 지금 가장 싼 값(없으면 None). 화면에 보이는 정가 o['p']보다 0.5% 넘게 낮으면 할인 중.
    할인 시작·끝·할인가가 바뀐 날만 sh에 남김. seen_off = 이 값이 할인 아닌 상태로 보인 적이 있음(이전 실행 sale False) —
    없으면(v1.5 전 자료가 이미 할인 중 · 새 상품·나라 · 품번·통화가 바뀜) 첫 기록에 'base'를 붙여 주간 메일이 '할인 시작'으로 세지 않음"""
    base = o.get("p")
    sh = [x for x in (o.get("sh") or []) if isinstance(x, list) and len(x) >= 2]
    last = sh[-1][1] if sh else None
    if now and base and now < base * 0.995:
        o["sale"], o["sp"], o["sp_date"] = True, round(now, 2), td
        if not sh and not seen_off:
            sh.append([td, o["sp"], "base"])     # 언제 시작했는지 모르는 할인 — 기록의 출발점
        elif last is None or abs(last - o["sp"]) > max(0.01, last * 0.005):
            sh.append([td, o["sp"]])
    else:
        o["sale"] = False
        o.pop("sp", None); o.pop("sp_date", None)
        if last is not None and now:
            sh.append([td, None])       # 할인 끝(지금 가격을 읽었을 때만 — 못 읽은 날은 끝으로 적지 않음)
    if sh:
        o["sh"] = sh[-SH_MAX:]
    else:
        o.pop("sh", None)

# 나라 → (나이키 상품 정보 marketplace·language, 통화) — 나이키 상품 정보에 없는 나라는 None(나이키 상품 urls의 페이지로 읽음)
MK = {"KR": ("KR", "ko", "KRW"), "US": ("US", "en", "USD"), "GB": ("GB", "en-GB", "GBP"), "DE": ("DE", "de", "EUR"),
      "JP": ("JP", "ja", "JPY"), "MX": ("MX", "es-419", "MXN"),
      "AE": (None, None, "AED")}   # v1.17 두바이(UAE 공식몰) — product_feed AE는 정가 100000 자리표시·다른 품번 결과 없음(11/03 시험)이라 nike.ae 페이지
NIKE_FEED = ("https://api.nike.com/product_feed/threads/v3/?filter=marketplace({m})&filter=language({l})"
             "&filter=channelId(d9a5bc42-4b9c-4976-858a-f159cf99c647)&filter=productInfo.merchProduct.styleColor({s})")

# 대표 상품 — brand는 브랜드 점검표(네이버 감시 브랜드) 이름과 같게. urls 없는 나라는 그 브랜드 공식몰에서 받지 못하는 곳(시험 2026-10-21)
DM = "https://www.drmartens.com"
def _on(slug, ae=None):   # 온러닝 — 나라별 몰 주소(상품 주소 꼴이 같음) · v1.17 ae = 두바이 몰(on.ae — Seddiqi 운영 쇼피파이)의 모델 상품 .json(handle) — 변형 품번 '3MG10051043 M 7'
    u = {cc: f"https://www.on.com/{loc}/products/{slug}" for cc, loc in (("KR", "ko-kr"), ("US", "en-us"), ("GB", "en-gb"), ("DE", "de-de"), ("JP", "ja-jp"))}
    if ae:   # 모델 .json은 변형 250개까지만(11/03 cloud-6·cloudsurfer-2 = 250 — 이 색상이 잘려 빠지면 '변형 250개에서 잘림' · SHOP_MODEL 주석)
        u["AE"] = f"https://on.ae/products/{ae}.json"
    return u


def _sal(kr, slug):   # 살로몬 — 한국 쇼피파이 상품(.json, 색상 품번) + 해외 모델 페이지(미국·영국·독일, 모델 기본가)
    return {"KR": f"https://salomon.co.kr/products/{kr}.json", **{cc: f"https://www.salomon.com/{loc}/product/{slug}" for cc, loc in (("US", "en-us"), ("GB", "en-gb"), ("DE", "de-de"))}}


def _arc(kr, slug, jp=None, g="mens/"):   # 아크테릭스 — 한국 시즌 상품 페이지(시즌마다 번호·한국 품번이 바뀜) + 미국·영국·독일(같은 주소 꼴) + 일본 쇼피파이 페이지
    u = {"KR": f"https://arcteryx.co.kr/products/view/{kr}", **{cc: f"https://arcteryx.com/{loc}/en/shop/{g}{slug}" for cc, loc in (("US", "us"), ("GB", "gb"), ("DE", "de"))}}
    if jp:
        u["JP"] = f"https://arcteryx.jp/products/{jp}"
    return u


def _keen(kr, h, jp=True, gb=None, de=True):   # 킨 — 한국 LF 공식몰(고도몰 상품 번호) + 미국·영국·독일·일본 쇼피파이 상품 .json(같은 상품 주소 꼴)
    u = {"KR": f"https://www.keenfootwear.kr/goods/goods_view.php?goodsNo={kr}", "US": f"https://www.keenfootwear.com/products/{h}.json",
         "GB": f"https://www.keenfootwear.co.uk/products/{gb or h}.json"}
    if de:
        u["DE"] = f"https://www.keenfootwear.de/en/products/{h}.json"
    if jp:
        u["JP"] = f"https://www.keenfootwear.jp/products/{jp if isinstance(jp, str) else h}.json"
    return u


def _oofos(kr, h):   # 우포스 — 한국 LF 공식몰(고도몰) + 미국 쇼피파이 .json(영국·독일·일본·멕시코는 공식 온라인몰 없음 — 소매점 판매)
    return {"KR": f"https://www.oofos.co.kr/goods/goods_view.php?goodsNo={kr}", "US": f"https://www.oofos.com/products/{h}.json"}


PRODUCTS = [
    # v1.17 나이키 두바이(AE)는 상품 정보(product_feed)에 없어 nike.ae 공식몰(GMG 운영 · SFCC) 페이지 — urls의 나라만 페이지로 읽음(sfra_list)
    {"id": "nike-af1", "cat": "shoe", "brand": "나이키", "name": "에어포스 1 '07", "code": "CW2288-111", "src": "nike", "cc": ["KR", "US", "GB", "DE", "JP", "MX"],
     "urls": {"AE": "https://www.nike.ae/en/air-force-1-07-mens-shoes/NKCW2288-111.html"}},
    {"id": "nike-dunk", "cat": "shoe", "brand": "나이키", "name": "덩크 로우 레트로", "code": "DD1391-100", "src": "nike", "cc": ["KR", "US", "GB", "DE", "JP", "MX"],
     "urls": {"AE": "https://www.nike.ae/en/dunk-low-retro-mens-shoe/NKDD1391-100.html"}},
    {"id": "nike-am90", "cat": "shoe", "brand": "나이키", "name": "에어맥스 90", "code": "CN8490-100", "src": "nike", "cc": ["KR", "US", "GB", "DE", "JP", "MX"],
     "urls": {"AE": "https://www.nike.ae/en/air-max-90-mens-shoe/NKCN8490-100.html"}},   # 브라질은 나이키 직영이 아님(시험 2026-10-21 · 결과 없음)
    # v1.17 블레이저 미드 '77·코르테즈·조던 1 로우 두바이(nike.ae)는 사이트맵에 없는 재고 정리 페이지(품절 · 할인가만 남음)라 뺌 — 곧 없어져 이전 값·21일 알림이 될 것
    {"id": "nike-blazer77", "cat": "shoe", "brand": "나이키", "name": "블레이저 미드 '77 빈티지", "code": "BQ6806-100", "src": "nike", "cc": ["KR", "US", "GB", "DE", "JP", "MX"]},
    {"id": "nike-cortez", "cat": "shoe", "brand": "나이키", "name": "코르테즈", "code": "DM4044-108", "src": "nike", "cc": ["KR", "US", "GB", "DE", "JP", "MX"]},
    {"id": "nike-aj1low", "cat": "shoe", "brand": "나이키", "name": "에어 조던 1 로우", "code": "553558-161", "src": "nike", "cc": ["KR", "US", "GB", "DE", "JP", "MX"]},
    {"id": "nike-vomero5", "cat": "shoe", "brand": "나이키", "name": "줌 보메로 5", "code": "BV1358-003", "src": "nike", "cc": ["KR", "US", "GB", "DE", "JP", "MX"],
     "urls": {"AE": "https://www.nike.ae/en/zoom-vomero-5-mens-shoes/NKBV1358-003.html"}},
    # v1.16 SKU 7차 — 6개 나라 product_feed 모두 같은 styleColor(11/03 · 정가 fullPrice — 킬샷 한국만 판매가 107,100) · v1.17 두바이 = nike.ae 사이트맵 상품 페이지
    {"id": "nike-airmaxplus", "cat": "shoe", "brand": "나이키", "name": "에어맥스 플러스", "code": "604133-139", "src": "nike", "cc": ["KR", "US", "GB", "DE", "JP", "MX"],
     "urls": {"AE": "https://www.nike.ae/en/air-max-plus-mens-shoes/NK604133-139.html"}},   # White/Black/Cool Grey/White
    {"id": "nike-killshot2", "cat": "shoe", "brand": "나이키", "name": "킬샷 2 레더", "code": "432997-107", "src": "nike", "cc": ["KR", "US", "GB", "DE", "JP", "MX"],
     "urls": {"AE": "https://www.nike.ae/en/killshot-2-leather-mens-shoes/NK432997-107.html"}},   # Sail/Gum Yellow/Midnight Navy
    {"id": "nike-courtvisionlo", "cat": "shoe", "brand": "나이키", "name": "코트 비전 로우 넥스트 네이처", "code": "DH2987-101", "src": "nike", "cc": ["KR", "US", "GB", "DE", "JP", "MX"],
     "urls": {"AE": "https://www.nike.ae/en/court-vision-low-next-nature-mens-shoes/NKDH2987-101.html"}},   # v1.18 White/Black-White · 11/10 한국·일본 할인 중(정가 fullPrice)
    # v1.24 해외 정가 브랜드당 20개 1차(대표 결정 2026-11-20 '검색만' · '블프 전 1차') — product_feed styleColor로 나라별 정가 fullPrice 읽기 확인(11/20 GitHub 서버) ·
    # 두바이 = nike.ae 사이트맵에 같은 품번 상품 페이지가 있는 것만(블레이저 로우 77·V2K 런은 없음 · 베나시는 페이지에 가격 데이터(JSON-LD) 없음)
    {"id": "nike-calm", "cat": "sandal", "brand": "나이키", "name": "캄 슬라이드", "code": "FD4116-001", "src": "nike", "cc": ["KR", "US", "GB", "DE", "JP", "MX"],
     "urls": {"AE": "https://www.nike.ae/en/calm-mens-slides/NKFD4116-001.html"}},   # Black/Black
    {"id": "nike-victorione", "cat": "sandal", "brand": "나이키", "name": "빅토리 원 슬라이드", "code": "CN9675-002", "src": "nike", "cc": ["KR", "US", "GB", "DE", "JP", "MX"],
     "urls": {"AE": "https://www.nike.ae/en/victori-one-mens-slides/NKCN9675-002.html"}},   # Black/White-Black
    {"id": "nike-blazerlo77", "cat": "shoe", "brand": "나이키", "name": "블레이저 로우 77 빈티지", "code": "DA6364-101", "src": "nike", "cc": ["KR", "US", "GB", "DE", "JP", "MX"]},   # 11/20 멕시코 빼고 할인 중(정가 fullPrice)
    {"id": "nike-v2krun", "cat": "shoe", "brand": "나이키", "name": "V2K 런", "code": "FD0736-100", "src": "nike", "cc": ["KR", "US", "GB", "DE", "JP", "MX"]},
    {"id": "nike-airmax97", "cat": "shoe", "brand": "나이키", "name": "에어맥스 97", "code": "921826-101", "src": "nike", "cc": ["KR", "US", "GB", "DE", "JP", "MX"],
     "urls": {"AE": "https://www.nike.ae/en/air-max-97-mens-shoes/NK921826-101.html"}},
    {"id": "nike-airmaxsc", "cat": "shoe", "brand": "나이키", "name": "에어맥스 SC", "code": "CW4555-002", "src": "nike", "cc": ["KR", "GB", "DE", "JP", "MX"],
     "urls": {"AE": "https://www.nike.ae/en/air-max-sc-mens-shoes/NKCW4555-002.html"}},   # 미국 나이키에서 팔지 않음(11/20)
    {"id": "nike-benassi", "cat": "sandal", "brand": "나이키", "name": "베나시 JDI 슬라이드", "code": "343880-090", "src": "nike", "cc": ["KR", "US", "JP", "MX"]},   # 영국·독일 나이키에서 팔지 않음 · 두바이 페이지는 가격 데이터 없음(11/20)
    # v1.25 SKU 2차(11/21) — 6개 나라 product_feed 같은 styleColor 정가 fullPrice 읽기 확인(GitHub 서버) · 두바이 = nike.ae 사이트맵 상품 페이지(헤리티지 백팩은 가격 데이터(JSON-LD) 없음) ·
    # 블프 검사(참고 — fullPrice는 정가 자체) 한국 정가 ÷ (현지 정가 × 11/20 환율)이 기존 17개 나라별 가운데값(미국 0.90 · 영국 0.75 · 독일 0.82 · 일본 1.06 · 멕시코 0.76 · 두바이 0.63)의 0.87~1.13배 ·
    # 예비 에어 허라취(DD1068-102 · 6개 나라 OK · 두바이 사이트맵에 없음)는 브랜드당 20개라 다음 차례에 · 에어맥스 엑시(CD4165-100)는 한국 나이키에서 팔지 않음
    {"id": "nike-p6000", "cat": "shoe", "brand": "나이키", "name": "P-6000", "code": "CN0149-001", "src": "nike", "cc": ["KR", "US", "GB", "DE", "JP"],
     "urls": {"AE": "https://www.nike.ae/en/p-6000-shoe/NKCN0149-001.html"}},   # 멕시코 나이키에서 팔지 않음(11/21)
    {"id": "nike-af1mid", "cat": "shoe", "brand": "나이키", "name": "에어포스 1 미드 '07", "code": "CW2289-111", "src": "nike", "cc": ["KR", "US", "GB", "DE", "JP", "MX"],
     "urls": {"AE": "https://www.nike.ae/en/air-force-1-mid-07-mens-shoe/NKCW2289-111.html"}},   # 에어포스 1 '07(로우 CW2288-111)과 다른 모델·가격
    {"id": "nike-heritagebp", "cat": "bag", "brand": "나이키", "name": "헤리티지 백팩(25L)", "code": "DC4244-010", "src": "nike", "cc": ["KR", "US", "GB", "DE", "JP", "MX"]},   # 11/21 한국·미국·영국·독일 할인 중(정가 fullPrice) · 두바이 페이지는 가격 데이터 없음
    # v1.17 푸마 두바이 = ae.puma.com(PUMA UAE 직영 · SFCC) — JSON-LD 품번 398846_xx · 할인 중이면 화면 데이터 c_listPrice(지금 page_price 그대로)
    {"id": "puma-speedcat", "cat": "shoe", "brand": "푸마", "name": "스피드캣 OG", "code": "398846", "src": "page", "hint": "speedcat", "urls": {
        "KR": "https://kr.puma.com/kr/ko/pd/%EC%8A%A4%ED%94%BC%EB%93%9C%EC%BA%A3-og-%3Cbr%3Espeedcat-og/398846.html",
        "US": "https://us.puma.com/us/en/pd/speedcat-og-sneakers/398846",
        "GB": "https://uk.puma.com/uk/en/pd/speedcat-og-sneakers-unisex/398846",
        "DE": "https://eu.puma.com/de/de/pd/speedcat-og-sneakers/398846",
        "JP": "https://jp.puma.com/jp/ja/pd/%E3%83%A6%E3%83%8B%E3%82%BB%E3%83%83%E3%82%AF%E3%82%B9-%E3%82%B9%E3%83%94%E3%83%BC%E3%83%89%E3%82%AD%E3%83%A3%E3%83%83%E3%83%88-og-%E3%82%B9%E3%83%8B%E3%83%BC%E3%82%AB%E3%83%BC/398846",
        "MX": "https://mx.puma.com/mx/es/pd/tenis-speedcat-og/398846.html",
        "AE": "https://ae.puma.com/ae/en/pd/speedcat-og-sneakers-unisex/398846.html"}},
    {"id": "puma-palermo", "cat": "shoe", "brand": "푸마", "name": "팔레르모", "code": "396463", "src": "page", "hint": "palermo", "urls": {
        "KR": "https://kr.puma.com/kr/ko/pd/%ED%8C%94%EB%A0%88%EB%A5%B4%EB%AA%A8-%3Cbr%3Epalermo/396463.html",
        "US": "https://us.puma.com/us/en/pd/palermo-sneakers/396463",
        "GB": "https://uk.puma.com/uk/en/pd/palermo-sneakers-unisex/396463",
        "DE": "https://eu.puma.com/de/de/pd/palermo-sneakers-unisex/396463",
        "JP": "https://jp.puma.com/jp/ja/pd/%E3%83%A6%E3%83%8B%E3%82%BB%E3%83%83%E3%82%AF%E3%82%B9-%E3%83%91%E3%83%AC%E3%83%AB%E3%83%A2-%E3%82%B9%E3%83%8B%E3%83%BC%E3%82%AB%E3%83%BC/396463",
        "AE": "https://ae.puma.com/ae/en/pd/palermo-sneakers-unisex/396463.html"}},   # 멕시코 몰에는 팔레르모(396463) 없음(시험 10/22)
    {"id": "puma-mostro", "cat": "shoe", "brand": "푸마", "name": "모스트로 OG", "code": "397330", "src": "page", "hint": "mostro", "urls": {
        "KR": "https://kr.puma.com/kr/ko/pd/%EB%AA%A8%EC%8A%A4%ED%8A%B8%EB%A1%9C-og-%3Cbr%3Emostro-og/397330.html",
        "US": "https://us.puma.com/us/en/pd/mostro-og-mens-sneakers/397330",
        "GB": "https://uk.puma.com/uk/en/pd/mostro-og-sneakers-unisex/397330",
        "DE": "https://eu.puma.com/de/de/pd/mostro-og-sneakers-unisex/397330",
        "JP": "https://jp.puma.com/jp/ja/pd/%E3%83%A6%E3%83%8B%E3%82%BB%E3%83%83%E3%82%AF%E3%82%B9-%E3%83%A2%E3%82%B9%E3%83%88%E3%83%AD-og-%E3%82%B9%E3%83%8B%E3%83%BC%E3%82%AB%E3%83%BC/397330",
        "MX": "https://mx.puma.com/mx/es/pd/tenis-mostro-og/397330.html",
        "AE": "https://ae.puma.com/ae/en/pd/mostro-og-sneakers-unisex/397330.html"}},
    {"id": "puma-suede", "cat": "shoe", "brand": "푸마", "name": "스웨이드 클래식", "code": "399781", "src": "page", "hint": "suede", "urls": {
        "KR": "https://kr.puma.com/kr/ko/pd/%EC%8A%A4%EC%9B%A8%EC%9D%B4%EB%93%9C-%ED%81%B4%EB%9E%98%EC%8B%9D%3Cbr%3Esuede-classic/399781.html",
        "US": "https://us.puma.com/us/en/pd/suede-classic-sneakers/399781",
        "GB": "https://uk.puma.com/uk/en/pd/suede-classic-sneakers-unisex/399781",
        "DE": "https://eu.puma.com/de/de/pd/suede-classic-sneakers-unisex/399781",
        "JP": "https://jp.puma.com/jp/ja/pd/%E3%83%A6%E3%83%8B%E3%82%BB%E3%83%83%E3%82%AF%E3%82%B9-%E3%82%B9%E3%82%A6%E3%82%A7%E3%83%BC%E3%83%89-%E3%82%AF%E3%83%A9%E3%82%B7%E3%83%83%E3%82%AF-%E3%82%B9%E3%83%8B%E3%83%BC%E3%82%AB%E3%83%BC/399781",
        "MX": "https://mx.puma.com/mx/es/pd/tenis-suede-classic/399781.html",
        "AE": "https://ae.puma.com/ae/en/pd/suede-classic-sneakers-unisex/399781.html"}},
    {"id": "puma-dne4", "cat": "shoe", "brand": "푸마", "name": "디비에이트 나이트로 엘리트 4(남성)", "code": "312127", "src": "page", "hint": "deviate nitro elite 4", "urls": {
        "KR": "https://kr.puma.com/kr/ko/pd/%EB%94%94%EB%B9%84%EC%97%90%EC%9D%B4%ED%8A%B8-%EB%82%98%EC%9D%B4%ED%8A%B8%EB%A1%9C-%EC%97%98%EB%A6%AC%ED%8A%B8-4-%3Cbr%3Edeviate-nitro-elite-4/312127.html",
        "US": "https://us.puma.com/us/en/pd/deviate-nitro-elite-4-mens-road-running-shoes/312127",
        "GB": "https://uk.puma.com/uk/en/pd/deviate-nitro%E2%84%A2-elite-4-running-shoes-men/312127",
        "DE": "https://eu.puma.com/de/de/pd/deviate-nitro-elite-4-laufschuhe-herren/312127",
        "JP": "https://jp.puma.com/jp/ja/pd/%E3%83%A1%E3%83%B3%E3%82%BA-%E3%83%87%E3%82%A3%E3%83%B4%E3%82%A3%E3%82%A8%E3%82%A4%E3%83%88-%E3%83%8B%E3%83%88%E3%83%AD-%E3%82%A8%E3%83%AA%E3%83%BC%E3%83%88-4-%E3%83%A9%E3%83%B3%E3%83%8B%E3%83%B3%E3%82%B0%E3%82%B7%E3%83%A5%E3%83%BC%E3%82%BA/312127",
        "MX": "https://mx.puma.com/mx/es/pd/tenis-de-running-deviate-nitrotm-elite-4-para-hombre/312127.html",
        "AE": "https://ae.puma.com/ae/en/pd/deviate-nitrotm-elite-4-running-shoes-men/312127.html"}},   # 인헤일(401560) 대신 — 미국 몰은 전 색상 할인가(73.99달러)뿐이라 뺌(검토 반영 10/22)
    {"id": "puma-speedcatgo", "cat": "shoe", "brand": "푸마", "name": "스피드캣 GO(여성)", "code": "403589", "src": "page", "hint": "speedcat go", "urls": {
        "KR": "https://kr.puma.com/kr/ko/pd/%EC%8A%A4%ED%94%BC%EB%93%9C%EC%BA%A3-go-%EC%9A%B0%EB%A8%BC%EC%8A%A4-%3Cbr%3Espeedcat-go-wns/403589.html",
        "US": "https://us.puma.com/us/en/pd/speedcat-go-womens-sneakers/403589",
        "JP": "https://jp.puma.com/jp/ja/pd/%E3%82%A6%E3%82%A3%E3%83%A1%E3%83%B3%E3%82%BA-%E3%82%B9%E3%83%94%E3%83%BC%E3%83%89%E3%82%AD%E3%83%A3%E3%83%83%E3%83%88-go-%E3%82%B9%E3%83%8B%E3%83%BC%E3%82%AB%E3%83%BC/403589",
        "MX": "https://mx.puma.com/mx/es/pd/tenis-speedcat-go-para-mujer/403589.html",
        "AE": "https://ae.puma.com/ae/en/pd/speedcat-go-shoes-women/403589.html"}},   # 독일 몰은 할인가(45.95유로)만 보여 정가로 읽혀 뺌(스피드캣 OG 독일 정가 109.95유로) · 영국 몰 사이트맵에 없음(10/27)
    {"id": "puma-dnetrail", "cat": "shoe", "brand": "푸마", "name": "디비에이트 나이트로 엘리트 트레일(남성)", "code": "310034", "src": "page", "hint": "deviate nitro elite trail", "urls": {
        "KR": "https://kr.puma.com/kr/ko/pd/%EB%94%94%EB%B9%84%EC%97%90%EC%9D%B4%ED%8A%B8-%EB%82%98%EC%9D%B4%ED%8A%B8%EB%A1%9C-%EC%97%98%EB%A6%AC%ED%8A%B8-%ED%8A%B8%EB%A0%88%EC%9D%BC-%3Cbr%3Edeviate-nitro-elite-trail/310034.html",
        "US": "https://us.puma.com/us/en/pd/deviate-nitro-elite-mens-trail-running-shoes/310034",
        "DE": "https://eu.puma.com/de/de/pd/deviate-nitro-elite-trailrunning-laufschuhe-herren/310034"}},   # 영국·일본 몰은 상품 가격 데이터(JSON-LD) 없음 · 멕시코 몰 사이트맵에 없음(10/27) · 두바이 몰도 JSON-LD 없음·사이트맵에 없음(11/03)
    {"id": "puma-t7track", "cat": "wear", "brand": "푸마", "name": "T7 올웨이즈 온 숏 트랙 자켓(여성)", "code": "629796", "src": "page", "hint": "t7", "urls": {
        "KR": "https://kr.puma.com/kr/ko/pd/t7-always-on-%EC%88%8F-%EA%B8%B0%EC%9E%A5-%ED%8A%B8%EB%9E%99-%EC%9E%90%EC%BC%93-%3Cbr%3Et7-always-on-short-track-jacket/629796.html",
        "US": "https://us.puma.com/us/en/pd/t7-womens-short-track-jacket/629796",
        "GB": "https://uk.puma.com/uk/en/pd/t7-always-on-short-track-jacket-women/629796",
        "DE": "https://eu.puma.com/de/de/pd/t7-always-on-kurze-trainingsjacke-damen/629796",
        "MX": "https://mx.puma.com/mx/es/pd/chamarra-t7-always-on-para-mujer/629796.html",
        "AE": "https://ae.puma.com/ae/en/pd/t7-always-on-jacket-women/629796.html"}},   # v1.18 일본 몰 사이트맵에 없음 · 11/10 한국·미국·영국·독일 할인 중(정가는 이 상품 취소선 정가)
    # v1.21 SKU 9차(정기 차례 11/17) — 한국 사이트맵 666개 중 해외 몰에 같은 품번이 있는 것(11/17 GitHub 서버 정가 읽기 확인 · 일본 몰은 접속 막음이라 뺌)
    {"id": "puma-dnetrailw", "cat": "shoe", "brand": "푸마", "name": "디비에이트 나이트로 엘리트 트레일(여성)", "code": "310468", "src": "page", "hint": "deviate nitro elite trail", "urls": {
        "KR": "https://kr.puma.com/kr/ko/pd/%EB%94%94%EB%B9%84%EC%97%90%EC%9D%B4%ED%8A%B8-%EB%82%98%EC%9D%B4%ED%8A%B8%EB%A1%9C-%EC%97%98%EB%A6%AC%ED%8A%B8-%ED%8A%B8%EB%A0%88%EC%9D%BC-%EC%9A%B0%EB%A8%BC%EC%8A%A4-%3Cbr%3Edeviate-nitro-elite-trail-wn/310468.html",
        "US": "https://us.puma.com/us/en/pd/deviate-nitro-elite-womens-trail-running-shoes/310468",
        "DE": "https://eu.puma.com/de/de/pd/deviate-nitro-elite-trailrunning-laufschuhe-damen/310468",
        "MX": "https://mx.puma.com/mx/es/pd/deviate-nitrotm-elite-trail-running-shoes-women/310468.html"}},   # 영국 몰은 상품 가격 데이터(JSON-LD) 없음 · 두바이 몰에 없음(11/17)
    {"id": "puma-foreverrun2", "cat": "shoe", "brand": "푸마", "name": "포에버런 나이트로 2(남성)", "code": "310109", "src": "page", "hint": "foreverrun nitro 2", "urls": {
        "KR": "https://kr.puma.com/kr/ko/pd/%ED%8F%AC%EC%97%90%EB%B2%84%EB%9F%B0-%EB%82%98%EC%9D%B4%ED%8A%B8%EB%A1%9C-2-%3Cbr%3Eforeverrun-nitro-2/310109.html",
        "US": "https://us.puma.com/us/en/pd/foreverrun-nitro-2-mens-road-running-shoes/310109",
        "DE": "https://eu.puma.com/de/de/pd/foreverrun-nitro-2-laufschuhe-herren/310109",
        "AE": "https://ae.puma.com/ae/en/pd/foreverrun-nitrotm-2-running-shoes-men/310109.html"}},   # 영국·멕시코 몰에 없음(11/17 사이트맵) · 11/17 한국·미국·독일·두바이 할인 중(정가는 취소선 정가)
    {"id": "puma-kingindoor", "cat": "shoe", "brand": "푸마", "name": "킹 인도어", "code": "401683", "src": "page", "hint": "king indoor", "urls": {
        "KR": "https://kr.puma.com/kr/ko/pd/%ED%82%B9-%EC%9D%B8%EB%8F%84%EC%96%B4-%3Cbr%3Eking-indoor/401683.html",
        "US": "https://us.puma.com/us/en/pd/king-indoor-sneakers/401683",
        "MX": "https://mx.puma.com/mx/es/pd/tenis-king-indoor/401683.html",
        "AE": "https://ae.puma.com/ae/en/pd/king-indoor-sneakers-unisex/401683.html"}},   # 영국·독일 몰에 없음(11/17 사이트맵)
    # v1.24 1차(11/20) — 한국 사이트맵 666개 중 해외 3개 나라 이상에 같은 품번이 있는 새 성인 상품은 이 둘뿐(나머지는 아동·한국 페이지 404 상품) ·
    # 포에버런 나이트로 3은 한국 사이트맵에 아직 없지만 한국 몰 상품 페이지가 열려 정가 읽기 확인(Firecrawl 검색으로 주소 찾음)
    {"id": "puma-foreverrun2w", "cat": "shoe", "brand": "푸마", "name": "포에버런 나이트로 2(여성)", "code": "310471", "src": "page", "hint": "foreverrun nitro 2", "urls": {
        "KR": "https://kr.puma.com/kr/ko/pd/%ED%8F%AC%EC%97%90%EB%B2%84%EB%9F%B0-%EB%82%98%EC%9D%B4%ED%8A%B8%EB%A1%9C-2-%EC%9A%B0%EB%A8%BC%EC%8A%A4-%3Cbr%3Eforeverrun-nitro-2-wn/310471.html",
        "US": "https://us.puma.com/us/en/pd/foreverrun-nitro-2-womens-road-running-shoes/310471",
        "DE": "https://eu.puma.com/de/de/pd/foreverrun-nitro-2-laufschuhe-damen/310471",
        "AE": "https://ae.puma.com/ae/en/pd/foreverrun-nitrotm-2-running-shoes-women/310471.html"}},   # 영국·멕시코 몰에 없음 · 11/20 네 나라 모두 할인 중(정가는 취소선 정가)
    {"id": "puma-foreverrun3", "cat": "shoe", "brand": "푸마", "name": "포에버런 나이트로 3(남성)", "code": "312942", "src": "page", "hint": "foreverrun nitro 3", "urls": {
        "KR": "https://kr.puma.com/kr/ko/pd/%ED%8F%AC%EC%97%90%EB%B2%84%EB%9F%B0-%EB%82%98%EC%9D%B4%ED%8A%B8%EB%A1%9C-3-%3Cbr%3Eforeverrun-nitro-3/312942.html",
        "US": "https://us.puma.com/us/en/pd/foreverrun-nitro-3-mens-road-running-shoes/312942",
        "GB": "https://uk.puma.com/uk/en/pd/foreverrun-nitro%E2%84%A2-3-running-shoes-men/312942",
        "DE": "https://eu.puma.com/de/de/pd/foreverrun-nitro-3-laufschuhe-herren/312942",
        "MX": "https://mx.puma.com/mx/es/pd/tenis-de-running-foreverrun-nitrotm-3-para-hombre/312942.html",
        "AE": "https://ae.puma.com/ae/en/pd/foreverrun-nitrotm-3-running-shoes-men/312942.html"}},
    # v1.25 SKU 2차(11/21) — 한국 몰 /pd/x/{품번}.html이 넘겨 준 정식 주소(한국 사이트맵에 아직 없는 새 품번) ∩ 미국·영국·독일·멕시코·두바이 몰 같은 품번(사이트맵) —
    #   11/21 GitHub 서버 정가 읽기 확인 · 일본 몰은 접속 막음이라 뺌 · 블프 검사 = 한국 정가 ÷ (현지 정가 × 11/20 환율)이 기존 푸마 13개 나라별 가운데값
    #   (미국 0.99 · 영국 0.91 · 독일 0.91 · 멕시코 0.97 · 두바이 0.76)의 1.25배 안인 나라만
    {"id": "puma-dn4", "cat": "shoe", "brand": "푸마", "name": "디비에이트 나이트로 4(남성)", "code": "312123", "src": "page", "hint": "deviate nitro 4", "urls": {
        "KR": "https://kr.puma.com/kr/ko/pd/%EB%94%94%EB%B9%84%EC%97%90%EC%9D%B4%ED%8A%B8-%EB%82%98%EC%9D%B4%ED%8A%B8%EB%A1%9C-4-%3Cbr%3Edeviate-nitro-4/312123.html",
        "US": "https://us.puma.com/us/en/pd/deviate-nitro-4-mens-road-running-shoes/312123",
        "GB": "https://uk.puma.com/uk/en/pd/deviate-nitro%E2%84%A2-4-running-shoes-men/312123",
        "DE": "https://eu.puma.com/de/de/pd/deviate-nitro-4-laufschuhe-herren/312123",
        "MX": "https://mx.puma.com/mx/es/pd/tenis-de-running-deviate-nitrotm-4-para-hombre/312123.html",
        "AE": "https://ae.puma.com/ae/en/pd/deviate-nitrotm-4-running-shoes-men/312123.html"}},   # 11/21 한국·영국·독일·멕시코 할인 중(정가는 이 상품 취소선 정가)
    {"id": "puma-magmax2", "cat": "shoe", "brand": "푸마", "name": "매그맥스 나이트로 2(남성)", "code": "312125", "src": "page", "hint": "magmax nitro 2", "urls": {
        "KR": "https://kr.puma.com/kr/ko/pd/%EB%A7%A4%EA%B7%B8%EB%A7%A5%EC%8A%A4-%EB%82%98%EC%9D%B4%ED%8A%B8%EB%A1%9C-2-%3Cbr%3Emagmax-nitro-2/312125.html",
        "US": "https://us.puma.com/us/en/pd/magmax-nitro-2-mens-road-running-shoes/312125",
        "DE": "https://eu.puma.com/de/de/pd/magmax-nitro-2-laufschuhe-herren/312125",
        "MX": "https://mx.puma.com/mx/es/pd/tenis-de-running-magmax-nitrotm-2-para-hombre/312125.html",
        "AE": "https://ae.puma.com/ae/en/pd/magmax-nitrotm-2-running-shoes-men/312125.html"}},   # 영국 몰은 시험 때 응답 없음(읽기 시간 초과 · 11/21) — 다음 차례에
    {"id": "puma-hstreet", "cat": "shoe", "brand": "푸마", "name": "H-스트리트 OG", "code": "403692", "src": "page", "hint": "h-street", "urls": {
        "KR": "https://kr.puma.com/kr/ko/pd/h-street-og/403692.html",
        "US": "https://us.puma.com/us/en/pd/h-street-og-sneakers/403692",
        "DE": "https://eu.puma.com/de/de/pd/h-street-og-sneakers-unisex/403692",
        "MX": "https://mx.puma.com/mx/es/pd/tenis-h-street-og-unisex/403692.html",
        "AE": "https://ae.puma.com/ae/en/pd/h-street-og-sneakers-unisex/403692.html"}},   # 영국 몰은 할인가(38파운드)만 보여 정가로 읽혀 뺌(한국 정가 ÷ 영국 값 1.94 — 가운데값의 2.1배 · 11/21)
    {"id": "puma-speedcatballet", "cat": "shoe", "brand": "푸마", "name": "스피드캣 발레 스웨이드(여성)", "code": "401287", "src": "page", "hint": "speedcat ballet", "urls": {
        "KR": "https://kr.puma.com/kr/ko/pd/%EC%8A%A4%ED%94%BC%EB%93%9C%EC%BA%A3-%EB%B0%9C%EB%A0%9B-sd-%EC%9A%B0%EB%A8%BC%EC%8A%A4-%3Cbr%3Espeedcat-ballet-sd-wns/401287.html",
        "US": "https://us.puma.com/us/en/pd/speedcat-ballet-suede-womens-sneakers/401287",
        "GB": "https://uk.puma.com/uk/en/pd/speedcat-suede-ballet-shoes-women/401287",
        "MX": "https://mx.puma.com/mx/es/pd/balerinas-speedcat-gamuza-para-mujer/401287.html",
        "AE": "https://ae.puma.com/ae/en/pd/speedcat-ballet-suede-sneakers-women/401287.html"}},   # 독일 63.95유로는 할인가로 보여 뺌(비율 1.27 — 가운데값의 1.4배 · 영국 70파운드는 0.97) · 11/21 한국 −67% 할인 중
    {"id": "puma-t7jacket", "cat": "wear", "brand": "푸마", "name": "T7 트랙 자켓(남성)", "code": "629587", "src": "page", "hint": "t7", "urls": {
        "KR": "https://kr.puma.com/kr/ko/pd/t7-%EC%98%AC%EC%9B%A8%EC%9D%B4%EC%A6%88-%EC%98%A8-%ED%8A%B8%EB%9E%99-%EC%9E%90%EC%BC%93-%3Cbr%3Et7-always-on-track-jacket-dk/629587.html",
        "US": "https://us.puma.com/us/en/pd/t7-mens-track-jacket/629587",
        "DE": "https://eu.puma.com/de/de/pd/t7-always-on-trainingsjacke-herren/629587",
        "MX": "https://mx.puma.com/mx/es/pd/chamarra-t7-always-on-para-hombre/629587.html",
        "AE": "https://ae.puma.com/ae/en/pd/t7-always-on-track-jacket-men/629587.html"}},   # 영국(55파운드)은 뺌 — 한국 정가 비율이 푸마 가운데값의 1.25배 바로 밑이고 이 상품 나라 간 비교(영국÷독일 0.73)에서 영국만 낮음(블프 할인가 의심) · 11/21 다섯 나라 할인 중(정가는 취소선 정가)
    {"id": "puma-velocity5", "cat": "shoe", "brand": "푸마", "name": "벨로시티 나이트로 5(남성)", "code": "312944", "src": "page", "hint": "velocity nitro 5", "urls": {
        "KR": "https://kr.puma.com/kr/ko/pd/%EB%B2%A8%EB%A1%9C%EC%8B%9C%ED%8B%B0-%EB%82%98%EC%9D%B4%ED%8A%B8%EB%A1%9C-5-%3Cbr%3Evelocity-nitro-5/312944.html",
        "US": "https://us.puma.com/us/en/pd/velocity-nitro-5-running-shoes-men-mens-road-running-shoes/312944",
        "GB": "https://uk.puma.com/uk/en/pd/velocity-nitro%E2%84%A2-5-running-shoes-men/312944",
        "DE": "https://eu.puma.com/de/de/pd/velocity-nitro-5-laufschuhe-herren/312944",
        "MX": "https://mx.puma.com/mx/es/pd/tenis-de-running-velocity-nitrotm-5-para-hombre/312944.html",
        "AE": "https://ae.puma.com/ae/en/pd/velocity-nitrotm-5-running-shoes-men/312944.html"}},   # 11/21 한국·멕시코만 할인 중
    {"id": "puma-velocityteew", "cat": "top", "brand": "푸마", "name": "런 벨로시티 티셔츠(여성)", "code": "526578", "src": "page", "hint": "velocity", "urls": {
        "KR": "https://kr.puma.com/kr/ko/pd/%EC%97%AC%EC%84%B1-%EB%9F%B0-%EB%B2%A8%EB%A1%9C%EC%8B%9C%ED%8B%B0-%ED%8B%B0%EC%85%94%EC%B8%A0(poly)-%3Cbr%3Ew-run-velocity-tee-(poly)/526578.html",
        "GB": "https://uk.puma.com/uk/en/pd/velocity-running-tee-women/526578",
        "MX": "https://mx.puma.com/mx/es/pd/playera-de-running-velocity-para-mujer/526578.html",
        "AE": "https://ae.puma.com/ae/en/pd/velocity-running-tee-women/526578.html"}},   # 미국 몰 사이트맵에 없음 · 독일 21.95유로는 할인가로 보여 뺌(비율 1.22 — 가운데값의 1.34배 · 11/21 1단계·2차 모두)
    # 뺌(11/21): 스웨이드 XL(395205)·리드캣 2.0 슬라이드(384139)·T7 스트레이트 트랙 팬츠 여성(629797) — 한국 페이지 404 ·
    #   디비에이트 나이트로 엘리트 4 여성(312128)·포에버런 나이트로 3 여성(312943)·디비에이트 나이트로 4 여성(312124) — 남성 모델(puma-dne4·puma-foreverrun3·puma-dn4)과 여섯 나라 정가가 모두 같아 뺌 ·
    #   매그맥스 나이트로 여성(310089) — 새 모델 매그맥스 나이트로 2가 나와 미국 −30%·두바이 −50% 재고 정리 중이라 뺌
    # v1.20 옛 클라우드몬스터(61.98434 올 화이트)는 11/10부터 한국 몰에서 빠짐(상품 주소가 목록 /shop으로 넘어감 · 일본은 재고 정리 할인 중) → 같은 모델 새 품번 '클라우드몬스터 1'(3MF3074) 블랙 —
    # 한국 몰에 있는 색상은 이것뿐 · 일본 몰에는 남성 클라우드몬스터 1이 없어 뺌 · 두바이(on.ae)는 이 색상 없음(11/11 나라별 상품 사이트맵·정가 읽기 확인)
    {"id": "on-cloudmonster", "cat": "shoe", "brand": "온러닝", "name": "클라우드몬스터 1", "code": "3MF30740553", "src": "page", "hint": "cloudmonster", "urls": {
        cc: u for cc, u in _on("cloudmonster-1-m-3mf3074/mens/black-shoes-3MF30740553").items() if cc != "JP"}},
    # v1.17 온러닝 두바이 = on.ae(Seddiqi 운영 쇼피파이 · 변형 품번 = 글로벌 품번 + 사이즈) — 모델 상품 .json에서 이 색상 품번 변형만(SHOP_MODEL)
    {"id": "on-cloud6", "cat": "shoe", "brand": "온러닝", "name": "클라우드 6", "code": "3MF10071200", "src": "page", "hint": "cloud 6", "urls": _on("cloud-6-m-3mf1007/mens/white-white-shoes-3MF10071200", "cloud-6")},
    {"id": "on-cloudsurfer2", "cat": "shoe", "brand": "온러닝", "name": "클라우드서퍼 2", "code": "3MF10121043", "src": "page", "hint": "cloudsurfer", "urls": _on("cloudsurfer-2-3mf1012/mens/black-black-shoes-3MF10121043", "cloudsurfer-2")},
    {"id": "on-cloudtilt", "cat": "shoe", "brand": "온러닝", "name": "클라우드틸트", "code": "3ME10101430", "src": "page", "hint": "cloudtilt", "urls": _on("cloudtilt-m-3me1010/mens/black-ivory-shoes-3ME10101430", "cloudtilt")},
    {"id": "on-roger", "cat": "shoe", "brand": "온러닝", "name": "더 로저 어드밴티지", "code": "3MF30641200", "src": "page", "hint": "roger", "urls": _on("the-roger-advantage-m-3mf3064/mens/white-white-shoes-3MF30641200", "the-roger-advantage")},
    # v1.20 남성 클라우드노바 2(3ME3021)는 11/10부터 한국·일본 몰에서 모델째 빠짐 → 5개 나라 몰에 같은 품번이 있는 클라우드몬스터 1 워터프루프 블랙(11/11 정가 읽기 확인 ·
    # 두바이 on.ae에는 이 모델 없음 — HTTP 404)
    {"id": "on-cloudmonster1wp", "cat": "shoe", "brand": "온러닝", "name": "클라우드몬스터 1 워터프루프", "code": "3MG10701043", "src": "page", "hint": "cloudmonster", "urls": _on("cloudmonster-1-wp-m-3mg1070/mens/black-black-shoes-3MG10701043")},
    # v1.14 SKU 5차 — 한국 몰 사이트맵(https://www.on.com/sitemap.xml → ko-kr 상품 · robots.txt에는 적혀 있지 않음)의 남성 신발 중 주요 모델 검정 · 5개 나라 같은 품번(10/28 GitHub 서버 확인)
    {"id": "on-cloudmonster3", "cat": "shoe", "brand": "온러닝", "name": "클라우드몬스터 3", "code": "3MG10051043", "src": "page", "hint": "cloudmonster 3", "urls": _on("cloudmonster-3-m-3mg1005/mens/black-black-shoes-3MG10051043", "cloudmonster-3")},
    {"id": "on-cloudrunner3", "cat": "shoe", "brand": "온러닝", "name": "클라우드러너 3", "code": "3MG10071043", "src": "page", "hint": "cloudrunner 3", "urls": _on("cloudrunner-3-m-3mg1007/mens/black-black-shoes-3MG10071043", "cloudrunner-3")},
    {"id": "on-cloudx5", "cat": "shoe", "brand": "온러닝", "name": "클라우드 X 5", "code": "3MG30081043", "src": "page", "hint": "cloud x 5", "urls": _on("cloud-x-5-m-3mg3008/mens/black-black-shoes-3MG30081043", "cloud-x-5")},
    {"id": "on-cloud6wp", "cat": "shoe", "brand": "온러닝", "name": "클라우드 6 워터프루프", "code": "3MF10061043", "src": "page", "hint": "cloud 6", "urls": _on("cloud-6-wp-3mf1006/mens/black-black-shoes-3MF10061043", "cloud-6-waterproof")},
    # v1.24 1차(11/20) — 나라별 상품 사이트맵({loc}/products.xml) 5개 나라 같은 품번 신발 중 주요 모델 · 정가 읽기 확인(GitHub 서버) · 두바이(on.ae)는 다음 차례에
    {"id": "on-cloud6coast", "cat": "shoe", "brand": "온러닝", "name": "클라우드 6 코스트", "code": "3MF10030080", "src": "page", "hint": "cloud 6 coast", "urls": _on("cloud-6-coast-3mf1003/mens/black-rock-shoes-3MF10030080")},
    {"id": "on-cloudzone", "cat": "shoe", "brand": "온러닝", "name": "클라우드존", "code": "3MF10080106", "src": "page", "hint": "cloudzone", "urls": _on("cloudzone-3mf1008/mens/black-eclipse-shoes-3MF10080106")},
    {"id": "on-cloudrocklowwp", "cat": "shoe", "brand": "온러닝", "name": "클라우드록 로우 워터프루프", "code": "3MF10251043", "src": "page", "hint": "cloudrock", "urls": _on("cloudrock-low-wp-3mf1025/mens/black-black-shoes-3MF10251043")},
    {"id": "on-cloudultra3", "cat": "shoe", "brand": "온러닝", "name": "클라우드울트라 3", "code": "3MF30231043", "src": "page", "hint": "cloudultra", "urls": _on("cloudultra-3-m-3mf3023/mens/black-black-shoes-3MF30231043")},
    {"id": "on-cloudboommax", "cat": "shoe", "brand": "온러닝", "name": "클라우드붐 맥스", "code": "3MF30310462", "src": "page", "hint": "cloudboom", "urls": _on("cloudboom-max-m-3mf3031/mens/white-black-shoes-3MF30310462")},
    {"id": "on-cloudsurfernext", "cat": "shoe", "brand": "온러닝", "name": "클라우드서퍼 넥스트", "code": "3ME30021200", "src": "page", "hint": "cloudsurfer", "urls": _on("cloudsurfer-next-3me3002/mens/white-white-shoes-3ME30021200")},
    {"id": "on-cloudsurfermax", "cat": "shoe", "brand": "온러닝", "name": "클라우드서퍼 맥스", "code": "3MF30431200", "src": "page", "hint": "cloudsurfer max", "urls": _on("cloudsurfer-max-m-3mf3043/mens/white-white-shoes-3MF30431200")},
    {"id": "on-cloud6w", "cat": "shoe", "brand": "온러닝", "name": "클라우드 6(여성)", "code": "3WF10061043", "src": "page", "hint": "cloud 6", "urls": _on("cloud-6-3wf1006/womens/black-black-shoes-3WF10061043")},
    {"id": "on-cloudmonster3w", "cat": "shoe", "brand": "온러닝", "name": "클라우드몬스터 3(여성)", "code": "3WG10031043", "src": "page", "hint": "cloudmonster 3", "urls": _on("cloudmonster-3-w-3wg1003/womens/black-black-shoes-3WG10031043")},
    {"id": "on-cloudrunner3w", "cat": "shoe", "brand": "온러닝", "name": "클라우드러너 3(여성)", "code": "3WG10051043", "src": "page", "hint": "cloudrunner 3", "urls": _on("cloudrunner-3-w-3wg1005/womens/black-black-shoes-3WG10051043")},
    {"id": "salomon-xt6", "cat": "shoe", "brand": "살로몬", "name": "XT-6 고어텍스", "code": "L47450600", "alt": ["LG9333"], "src": "page", "hint": "xt-6", "urls": {
        "KR": "https://salomon.co.kr/products/l47450600.json",
        "US": "https://www.salomon.com/en-us/product/xt-6-gore-tex-lg9333",
        "GB": "https://www.salomon.com/en-gb/product/xt-6-gore-tex-lg9333",
        "DE": "https://www.salomon.com/de-de/product/xt-6-gore-tex-lg9333"}},
    {"id": "salomon-xt6base", "cat": "shoe", "brand": "살로몬", "name": "XT-6", "code": "L41086600", "alt": ["LG4239"], "src": "page", "hint": "xt-6", "urls": _sal("l41086600", "xt-6-lg4239")},
    {"id": "salomon-xt4og", "cat": "shoe", "brand": "살로몬", "name": "XT-4 OG", "code": "L47132900", "alt": ["LI3335"], "src": "page", "hint": "xt-4", "urls": _sal("l47132900", "xt-4-og-li3335")},
    {"id": "salomon-xt6expanse", "cat": "shoe", "brand": "살로몬", "name": "XT-6 익스팬스", "code": "L41741300", "alt": ["LG9334"], "src": "page", "hint": "xt-6", "urls": _sal("l41741300", "xt-6-expanse-lg9334")},
    {"id": "salomon-xt4oggtx", "cat": "shoe", "brand": "살로몬", "name": "XT-4 OG 고어텍스", "code": "L49210800", "alt": ["LI8806"], "src": "page", "hint": "xt-4", "urls": _sal("l49210800", "xt-4-og-gore-tex-li8806")},
    {"id": "drm-1461", "cat": "shoe", "brand": "닥터마틴", "name": "1461 스무스", "code": "11838002", "src": "page", "hint": "1461", "urls": {
        "KR": "https://www.drmartens.co.kr/products/boots-1461-black-smooth.json",
        "US": f"{DM}/us/en/1461-smooth-leather-oxford-shoes-black/p/11838002",
        "GB": f"{DM}/uk/en_gb/1461-smooth-leather-oxford-shoes-black/p/11838002"}},
    {"id": "drm-jadon", "cat": "boot", "brand": "닥터마틴", "name": "제이든", "code": "15265001", "src": "page", "hint": "jadon", "urls": {
        "KR": "https://www.drmartens.co.kr/products/boots-jadon-black-15265001.json",
        "US": f"{DM}/us/en/jadon-smooth-leather-platform-boots-black/p/15265001",
        "GB": f"{DM}/uk/en_gb/jadon-smooth-leather-platform-boots-black/p/15265001"}},
    # 닥터마틴 1460 블랙은 한국 몰 품번(10072004)이 해외(11822006)와 달라 넣지 않음(같은 상품인지 확인 안 됨) — 체리레드(11822600)는 같아서 넣음(v1.3)
    # v1.2 — 접속 시험 2026-10-22: 해외 몰 주소는 GitHub 서버에서 확인(나라별 같은 품번)
    {"id": "drm-1460cr", "cat": "boot", "brand": "닥터마틴", "name": "1460 스무스 체리레드", "code": "11822600", "src": "page", "hint": "1460", "urls": {
        "KR": "https://www.drmartens.co.kr/products/boots-1460-cherry-red-11822600.json",
        "US": f"{DM}/us/en/1460-smooth-leather-lace-up-boots-cherry-red/p/11822600",
        "GB": f"{DM}/uk/en_gb/1460-smooth-leather-lace-up-boots-cherry-red/p/11822600"}},
    {"id": "drm-2976", "cat": "boot", "brand": "닥터마틴", "name": "2976 첼시", "code": "22227001", "src": "page", "hint": "2976", "urls": {
        "KR": "https://www.drmartens.co.kr/products/boots-2976ys-black-smooth.json",
        "US": f"{DM}/us/en/2976-smooth-leather-chelsea-boots-black/p/22227001",
        "GB": f"{DM}/uk/en_gb/2976-smooth-leather-chelsea-boots-black/p/22227001"}},
    {"id": "drm-1460bex", "cat": "boot", "brand": "닥터마틴", "name": "1460 벡스", "code": "25345001", "src": "page", "hint": "bex", "urls": {
        "KR": "https://www.drmartens.co.kr/products/boots-1460-bex-black-smooth.json",
        "US": f"{DM}/us/en/1460-bex-smooth-leather-lace-up-boots-black/p/25345001",
        "GB": f"{DM}/uk/en_gb/1460-bex-smooth-leather-lace-up-boots-black/p/25345001"}},
    {"id": "drm-1460mono", "cat": "boot", "brand": "닥터마틴", "name": "1460 모노", "code": "14353001", "src": "page", "hint": "mono", "urls": {
        "KR": "https://www.drmartens.co.kr/products/1460-mofalse.json",
        "US": f"{DM}/us/en/1460-mono-smooth-leather-lace-up-boots-black/p/14353001",
        "GB": f"{DM}/uk/en_gb/1460-mono-smooth-leather-lace-up-boots-black/p/14353001"}},
    {"id": "drm-adrian", "cat": "shoe", "brand": "닥터마틴", "name": "아드리안 태슬 로퍼", "code": "14573001", "src": "page", "hint": "adrian", "urls": {
        "KR": "https://www.drmartens.co.kr/products/adeurian.json",
        "US": f"{DM}/us/en/adrian-smooth-leather-tassel-loafers-black/p/14573001",
        "GB": f"{DM}/uk/en_gb/adrian-smooth-leather-tassel-loafers-black/p/14573001"}},
    {"id": "drm-8065", "cat": "shoe", "brand": "닥터마틴", "name": "8065 메리제인", "code": "12916001", "src": "page", "hint": "8065", "urls": {
        "KR": "https://www.drmartens.co.kr/products/shoes-8065-maryjane-black-smooth-12916001.json",
        "US": f"{DM}/us/en/8065-smooth-leather-mary-jane-shoes-black/p/12916001",
        "GB": f"{DM}/uk/en_gb/8065-smooth-leather-mary-jane-shoes-black/p/12916001"}},
    {"id": "drm-sinclair", "cat": "boot", "brand": "닥터마틴", "name": "싱클레어", "code": "22564001", "src": "page", "hint": "sinclair", "urls": {
        "KR": "https://www.drmartens.co.kr/products/singkeulreeo.json",
        "US": f"{DM}/us/en/sinclair-womens-leather-platform-boots-black-milled-nappa/p/22564001",
        "GB": f"{DM}/uk/en_gb/sinclair-soft-leather-platform-boots-black/p/22564001"}},
    {"id": "drm-1461mono", "cat": "shoe", "brand": "닥터마틴", "name": "1461 모노", "code": "14345001", "src": "page", "hint": "1461", "urls": {
        "KR": "https://www.drmartens.co.kr/products/shoes-1461-mono-black-14345001.json",
        "US": f"{DM}/us/en/1461-mono-smooth-leather-oxford-shoes-black/p/14345001",
        "GB": f"{DM}/uk/en_gb/1461-mono-smooth-leather-oxford-shoes-black/p/14345001"}},
    # v1.24 1차(11/20) — 한국 쇼피파이 /products.json 품번 앞 8자리 ∩ 미국·영국 사이트맵 /p/품번 289개 중 주요 모델 · 정가 읽기 확인(GitHub 서버) ·
    # 11/20 미국 몰은 블프 할인 중이라 많은 상품이 할인가로 읽힘(한국 정가 ÷ 미국 값이 지금 상품들 1,360~1,550 → 이 상품들 1,950~2,180) — 첫 값이 정가로 저장되지 않게
    # 처치 말고는 미국을 블프 뒤에 넣음 · 영국 값도 할인으로 보이는 8053·2976 벡스·오드릭·그리폰은 뺌
    {"id": "drm-2976quad", "cat": "boot", "brand": "닥터마틴", "name": "2976 쿼드", "code": "24687001", "src": "page", "hint": "2976", "urls": {
        "KR": "https://www.drmartens.co.kr/products/boots-2976-quad-black-polished-smooth.json",
        "GB": f"{DM}/uk/en_gb/2976-quad-smooth-leather-platform-chelsea-boots-black/p/24687001"}},
    {"id": "drm-1461bex", "cat": "shoe", "brand": "닥터마틴", "name": "1461 벡스", "code": "21084001", "src": "page", "hint": "1461", "urls": {
        "KR": "https://www.drmartens.co.kr/products/shoes-1461-bex-black-smooth.json",
        "GB": f"{DM}/uk/en_gb/1461-bex-smooth-leather-oxford-shoes-black/p/21084001"}},
    {"id": "drm-1461quad", "cat": "shoe", "brand": "닥터마틴", "name": "1461 쿼드 레트로", "code": "25567001", "src": "page", "hint": "1461", "urls": {
        "KR": "https://www.drmartens.co.kr/products/shoes-1461-quad-retro-25567001.json",
        "GB": f"{DM}/uk/en_gb/1461-quad-smooth-leather-platform-shoes-black/p/25567001"}},
    {"id": "drm-polley", "cat": "shoe", "brand": "닥터마틴", "name": "폴리 메리제인", "code": "14852001", "src": "page", "hint": "polley", "urls": {
        "KR": "https://www.drmartens.co.kr/products/14852001.json",
        "GB": f"{DM}/uk/en_gb/polley-smooth-leather-mary-jane-shoes-black/p/14852001"}},
    {"id": "drm-1490", "cat": "boot", "brand": "닥터마틴", "name": "1490 버지니아", "code": "22524001", "src": "page", "hint": "1490", "urls": {
        "KR": "https://www.drmartens.co.kr/products/core-1490-black-virgina.json",
        "GB": f"{DM}/uk/en_gb/1490-virginia-leather-high-boots-black/p/22524001"}},
    {"id": "drm-church", "cat": "boot", "brand": "닥터마틴", "name": "처치 몽키 부츠", "code": "16054001", "src": "page", "hint": "church", "urls": {
        "KR": "https://www.drmartens.co.kr/products/boots-church-black-16054001.json",
        "US": f"{DM}/us/en/church-vintage-monkey-boots-black/p/16054001",
        "GB": f"{DM}/uk/en_gb/church-vintage-smooth-leather-monkey-boots-black/p/16054001"}},
    # v1.25 SKU 2차(11/21) — 한국 쇼피파이 /products.json 품번 ∩ 영국 사이트맵 /p/품번 · 정가 읽기 확인(GitHub 서버) · 한국·영국만(기존 묶음 방침) ·
    # 영국 값은 한국 정가 ÷ (영국 값 × 환율) 0.90~0.91로 기존 16개 가운데값 0.904와 같아 할인가 아님 · 미국은 블프 할인가로 읽혀 블프 뒤(블레어 $60 = 1.99 · 리더 $84 = 1.60 — 기존 가운데값 1.12) ·
    # 빈티지(메이드 인 잉글랜드)는 일반 1460·1461·2976과 다른 줄·다른 가격(349,000·299,000 vs 279,000·229,000) · 1461 체리레드·앰버서더·크레이지 호스, 1460 파스칼 모노·크레이지 호스·버지니아,
    # 2976 모노·앰버서더는 기존 상품과 같은 모델 같은 가격이라 뺌 · 리더(27104001)·제이든 III(26378001)는 정가 읽기 OK였으나 브랜드당 20개라 다음 차례에(독일 칸도 브랜드 전체로 다음에)
    {"id": "drm-vintage1460", "cat": "boot", "brand": "닥터마틴", "name": "빈티지 1460(메이드 인 잉글랜드)", "code": "12308001", "src": "page", "hint": "1460", "urls": {
        "KR": "https://www.drmartens.co.kr/products/bintiji-1460.json",
        "GB": f"{DM}/uk/en_gb/vintage-1460-quilon-leather-ankle-boots-black/p/12308001"}},
    {"id": "drm-vintage1461", "cat": "shoe", "brand": "닥터마틴", "name": "빈티지 1461(메이드 인 잉글랜드)", "code": "12877001", "src": "page", "hint": "1461", "urls": {
        "KR": "https://www.drmartens.co.kr/products/bintiji-1461.json",
        "GB": f"{DM}/uk/en_gb/vintage-1461-quilon-leather-oxford-shoes-black/p/12877001"}},
    {"id": "drm-blaire", "cat": "sandal", "brand": "닥터마틴", "name": "블레어 샌들", "code": "31520001", "src": "page", "hint": "blaire", "urls": {
        "KR": "https://www.drmartens.co.kr/products/31520001-blaire.json",
        "GB": f"{DM}/uk/en_gb/blaire-athena-leather-strap-sandals-black/p/31520001"}},
    {"id": "drm-vintage2976", "cat": "boot", "brand": "닥터마틴", "name": "빈티지 2976 첼시(메이드 인 잉글랜드)", "code": "25747001", "src": "page", "hint": "2976", "urls": {
        "KR": "https://www.drmartens.co.kr/products/boots-2976-black-quillon-25747001.json",
        "GB": f"{DM}/uk/en_gb/2976-vintage-made-in-england-chelsea-boots-black/p/25747001"}},
    {"id": "dd-santacroce", "cat": "bag", "brand": "드래곤디퓨전", "name": "산타크로체 빅 백", "code": "8892", "alt": ["W2BAS26025DBR"], "src": "page", "hint": "santa croce", "urls": {
        "KR": "https://www.kolonmall.com/Brands/DRAGON_DIFFUSION/Product/W2BAS26025DBR",   # 코오롱몰(공식 수입) 자체 품번
        "US": "https://dragondiffusion.com/products/santa-croce-big-dark-brown-woven-leather-bag-handmade"}},   # 글로벌 몰 1곳 — 접속한 나라 통화(미국 서버 → 달러), 달러가 아니면 실패
    {"id": "dd-santamaria", "cat": "bag", "brand": "드래곤디퓨전", "name": "산타마리아 백", "code": "8700", "alt": ["W2BAS26026BKX"], "src": "page", "hint": "santa maria", "urls": {
        "KR": "https://www.kolonmall.com/Brands/DRAGON_DIFFUSION/Product/W2BAS26026BKX",
        "US": "https://dragondiffusion.com/products/santa-maria-black-woven-leather-bag"}},
    {"id": "dd-triplejump", "cat": "bag", "brand": "드래곤디퓨전", "name": "트리플 점프 스몰 백", "code": "8811", "alt": ["W2BAS26029BKX"], "src": "page", "hint": "triple jump", "urls": {
        "KR": "https://www.kolonmall.com/Brands/DRAGON_DIFFUSION/Product/W2BAS26029BKX",
        "US": "https://dragondiffusion.com/products/triple-jump-small-black-woven-leather-bag-handmade"}},
    {"id": "dd-rosanna", "cat": "bag", "brand": "드래곤디퓨전", "name": "로잔나 백", "code": "8943", "alt": ["W2BAS26024BKX"], "src": "page", "hint": "rosanna", "urls": {
        "KR": "https://www.kolonmall.com/Brands/DRAGON_DIFFUSION/Product/W2BAS26024BKX",
        "US": "https://dragondiffusion.com/products/rosanna-black-woven-leather-bag-handmade"}},
    {"id": "dd-ars", "cat": "bag", "brand": "드래곤디퓨전", "name": "아르스 토트백", "code": "8848", "alt": ["W2BAS26027DBR"], "src": "page", "hint": "ars", "urls": {
        "KR": "https://www.kolonmall.com/Brands/DRAGON_DIFFUSION/Product/W2BAS26027DBR",
        "US": "https://dragondiffusion.com/products/ars-tote-dark-brown-woven-leather-bag"}},
    {"id": "dd-nantucket", "cat": "bag", "brand": "드래곤디퓨전", "name": "난터켓 빅 백", "code": "8822", "alt": ["W2BAS26030DBR"], "src": "page", "hint": "nantucket", "urls": {
        "KR": "https://www.kolonmall.com/Brands/DRAGON_DIFFUSION/Product/W2BAS26030DBR",
        "US": "https://dragondiffusion.com/products/nantucket-big-dark-brown-woven-leather-bag-handmade"}},
    {"id": "dd-chunkyfellini", "cat": "bag", "brand": "드래곤디퓨전", "name": "청키 펠리니 포셰트", "code": "8036", "alt": ["W2BAS26028DBR"], "src": "page", "hint": "chunky fellini", "urls": {
        "KR": "https://www.kolonmall.com/Brands/DRAGON_DIFFUSION/Product/W2BAS26028DBR",
        "US": "https://dragondiffusion.com/products/chunky-fellini-pochette-dark-brown-woven-leather-pochette-handmade"}},
    {"id": "hunter-origtall", "cat": "boot", "brand": "헌터", "name": "오리지널 톨(여성·무광)", "code": "WFT1000RMA", "src": "page", "hint": "wft1000rmablk", "urls": {
        "KR": "https://www.kolonmall.com/Brands/HUNTER/Product/K1760508652696038BK01",   # 코오롱몰 — 품번은 상품 이름 끝(WFT1000RMABLK)에만
        "US": "https://hunterboots.com/products/womens-original-tall-rain-boots-in-black-wft1000rma-hbl01.json",
        "GB": "https://hunterboots.co.uk/products/womens-original-tall-wellington-boots-wft1000rma-blk.json",
        "JP": "https://hunterboots.co.jp/products/wft1000rma-blk.json"}},
    {"id": "hunter-origshort", "cat": "boot", "brand": "헌터", "name": "오리지널 숏(여성·무광)", "code": "WFS1000RMA", "src": "page", "hint": "wfs1000rmablk", "urls": {
        "KR": "https://www.kolonmall.com/Brands/HUNTER/Product/K1760507742896066BK01",
        "US": "https://hunterboots.com/products/womens-original-short-rain-boots-in-black-wfs1000rma-hbl01.json",
        "GB": "https://hunterboots.co.uk/products/womens-original-short-boot-wfs1000rma-blk.json",
        "JP": "https://hunterboots.co.jp/products/wfs1000rma-blk.json"}},
    {"id": "hunter-playtall", "cat": "boot", "brand": "헌터", "name": "플레이 톨(여성)", "code": "WFT2007RMA", "src": "page", "hint": "wft2007rmablk", "urls": {
        "KR": "https://www.kolonmall.com/Brands/HUNTER/Product/K1760508641433091BK01",
        "US": "https://hunterboots.com/products/womens-play-tall-rain-boots-in-black-wft2007rma-hbl01.json",
        "GB": "https://hunterboots.co.uk/products/womens-play-tall-wellington-boots-wft2007rma-blk.json",
        "JP": "https://hunterboots.co.jp/products/wft2007rma-blk.json"}},
    {"id": "hunter-chelsea", "cat": "boot", "brand": "헌터", "name": "오리지널 첼시(여성)", "code": "WFS2078RMA", "src": "page", "hint": "wfs2078rmablk", "urls": {
        "KR": "https://www.kolonmall.com/Brands/HUNTER/Product/K1760510634046010NO01",
        "US": "https://hunterboots.com/products/womens-original-chelsea-boots-in-black-wfs2078rma-hbl01.json",
        "GB": "https://hunterboots.co.uk/products/womens-original-chelsea-boots-wfs2078rma-blk.json"}},   # 일본 몰에서 같은 품번(WFS2078RMA)을 못 찾음(시험 10/22)
    {"id": "hunter-playshort", "cat": "boot", "brand": "헌터", "name": "플레이 숏(여성)", "code": "WFS2020RMA", "src": "page", "hint": "wfs2020rmablk", "urls": {
        "KR": "https://www.kolonmall.com/Brands/HUNTER/Product/K1760066476268098BK01",
        "US": "https://hunterboots.com/products/womens-play-short-rain-boots-in-black-wfs2020rma-hbl01.json",
        "GB": "https://hunterboots.co.uk/products/womens-play-short-wellington-boots-wfs2020rma-blk.json"}},   # 일본 몰에는 없음(404, 10/22)
    {"id": "hunter-glosstall", "cat": "boot", "brand": "헌터", "name": "오리지널 톨 글로스(여성)", "code": "WFT1000RGL", "src": "page", "hint": "wft1000rglblk", "urls": {
        "KR": "https://www.kolonmall.com/Brands/HUNTER/Product/K1760508619617098BK01",
        "US": "https://hunterboots.com/products/womens-original-tall-gloss-rain-boots-in-black-wft1000rgl-hbl01.json",
        "GB": "https://hunterboots.co.uk/products/womens-original-tall-gloss-wellington-boots-wft1000rgl-blk.json",
        "JP": "https://hunterboots.co.jp/products/wft1000rgl-blk.json"}},
    {"id": "hunter-glossshort", "cat": "boot", "brand": "헌터", "name": "오리지널 숏 글로스(여성)", "code": "WFS1000RGL", "src": "page", "hint": "wfs1000rglblk", "urls": {
        "KR": "https://www.kolonmall.com/Brands/HUNTER/Product/K1760507733522065BK01",
        "US": "https://hunterboots.com/products/womens-original-short-gloss-rain-boots-in-black-wfs1000rgl-hbl01.json",
        "GB": "https://hunterboots.co.uk/products/womens-original-short-gloss-wellington-boots-wfs1000rgl-blk.json"}},   # 일본 몰 사이트맵에 없음(10/27)
    # v1.21 SKU 9차 — 코오롱몰 헌터 목록 화면의 품번(상품 이름 끝) ∩ 영국·일본 쇼피파이(11/17 정가 읽기 확인 · 미국 몰에 없음)
    {"id": "hunter-refinedshort", "cat": "boot", "brand": "헌터", "name": "리파인드 슬림핏 숏(여성)", "code": "WFS2200RMA", "src": "page", "hint": "wfs2200rmablk", "urls": {
        "KR": "https://www.kolonmall.com/Brands/HUNTER/Product/K1760507760063021BK01",
        "GB": "https://hunterboots.co.uk/products/womens-refined-slim-fit-short-wellington-boots-wfs2200rma-blk.json",
        "JP": "https://hunterboots.co.jp/products/wfs2200rma-blk.json"}},
    {"id": "hunter-veganshearling", "cat": "boot", "brand": "헌터", "name": "플레이 비건 시어링 인슐레이티드 톨(여성)", "code": "WFT2235RMA", "src": "page", "hint": "wft2235rmablk", "urls": {
        "KR": "https://www.kolonmall.com/Brands/HUNTER/Product/K1760084797358063BK01",
        "GB": "https://hunterboots.co.uk/products/womens-play-vegan-shearling-insulated-tall-wellington-boots-wft2235rma-blk.json"}},   # 일본 몰 사이트맵에 없음(11/17)
    {"id": "hunter-intrepidtall", "cat": "boot", "brand": "헌터", "name": "인트레피드 톨 스노 부츠(여성)", "code": "WFT2108WWU", "src": "page", "hint": "wft2108wwublk", "urls": {
        "KR": "https://www.kolonmall.com/Brands/HUNTER/Product/K1760508591697023BK01",
        "GB": "https://hunterboots.co.uk/products/womens-intrepid-tall-snow-boot-wft2108wwu-blk.json"}},   # 일본 몰 사이트맵에 없음(11/17)
    # v1.25 SKU 2차 — 코오롱몰 목록 화면 품번(상품 이름 끝) ∩ 일본 쇼피파이(11/21 정가 읽기 확인 · 미국·영국 몰은 새 시즌 상품을 새 품번 HF…·HA…로 바꿔 같은 품번 없음 · 영국은 MFS9135WWU만)
    # 블프 검사(한국 정가 ÷ (현지 정가 × 11/20 환율)): 일본 0.87~1.14(기존 헌터 가운데값 0.93의 0.94~1.23배) · 영국 0.93(가운데값 0.95) — 모두 1.25배 안
    {"id": "hunter-wandershort", "cat": "boot", "brand": "헌터", "name": "인트레피드 원더러 숏 스노 부츠", "code": "UFS7119WWU", "src": "page", "hint": "ufs7119wwublk", "urls": {
        "KR": "https://www.kolonmall.com/Brands/HUNTER/Product/K1792133875939070BK01",
        "JP": "https://hunterboots.co.jp/products/ufs7119wwu-blk.json"}},
    {"id": "hunter-wandertall", "cat": "boot", "brand": "헌터", "name": "인트레피드 원더러 톨 스노 부츠", "code": "UFT7120WWU", "src": "page", "hint": "uft7120wwublk", "urls": {
        "KR": "https://www.kolonmall.com/Brands/HUNTER/Product/K1792133666918092BK01",
        "JP": "https://hunterboots.co.jp/products/uft7120wwu-blk.json"}},
    {"id": "hunter-refinedtall", "cat": "boot", "brand": "헌터", "name": "리파인드 슬림핏 톨(여성)", "code": "WFT2200RMA", "src": "page", "hint": "wft2200rmablk", "urls": {
        "KR": "https://www.kolonmall.com/Brands/HUNTER/Product/K1760508601844067BK01",
        "JP": "https://hunterboots.co.jp/products/wft2200rma-blk.json"}},
    {"id": "hunter-neochelsea", "cat": "boot", "brand": "헌터", "name": "오리지널 네오프렌 첼시(여성)", "code": "WFS2403NRE", "src": "page", "hint": "wfs2403nreblk", "urls": {
        "KR": "https://www.kolonmall.com/Brands/HUNTER/Product/K1785476517288037BK01",
        "JP": "https://hunterboots.co.jp/products/wfs2403nre-blk.json"}},
    {"id": "hunter-mplaychelsea", "cat": "boot", "brand": "헌터", "name": "플레이 네오프렌 첼시(남성)", "code": "MFS9022RMA", "src": "page", "hint": "mfs9022rmablk", "urls": {
        "KR": "https://www.kolonmall.com/Brands/HUNTER/Product/K1760508683714035NO01",   # 상품 번호 끝은 NO01이지만 상품 이름 끝 품번은 MFS9022RMABLK(블랙)
        "JP": "https://hunterboots.co.jp/products/mfs9022rma-blk.json"}},
    {"id": "hunter-mintrepidshort", "cat": "boot", "brand": "헌터", "name": "인트레피드 인슐레이티드 숏 스노 부츠(남성)", "code": "MFS9135WWU", "src": "page", "hint": "mfs9135wwublk", "urls": {
        "KR": "https://www.kolonmall.com/Brands/HUNTER/Product/K1760084986999013BK01",
        "GB": "https://hunterboots.co.uk/products/mens-intrepid-insulated-short-snow-boots-mfs9135wwu-blk.json"}},   # 영국은 11/21 할인 중(96파운드) — 정가는 compare_at 160(비율 0.93) · 일본 몰에 없음
    {"id": "hunter-gripexplorer", "cat": "boot", "brand": "헌터", "name": "그립 익스플로러 레이스업 부츠", "code": "UFS7123LNR", "src": "page", "hint": "ufs7123lnrblk", "urls": {
        "KR": "https://www.kolonmall.com/Brands/HUNTER/Product/K1789969305240016BK01",
        "JP": "https://hunterboots.co.jp/products/ufs7123lnr-blk.json"}},
    {"id": "hunter-explorerchelsea", "cat": "boot", "brand": "헌터", "name": "리파인드 익스플로러 로퍼 첼시 부츠", "code": "UFS7125LEA", "src": "page", "hint": "ufs7125leablk", "urls": {
        "KR": "https://www.kolonmall.com/Brands/HUNTER/Product/K1774579934235020BK01",
        "JP": "https://hunterboots.co.jp/products/ufs7125lea-blk.json"}},
    {"id": "hunter-griptall", "cat": "boot", "brand": "헌터", "name": "그립 톨 스노 부츠", "code": "UFT7101NYL", "src": "page", "hint": "uft7101nylblk", "urls": {
        "KR": "https://www.kolonmall.com/Brands/HUNTER/Product/K1760084821690065BK01",
        "JP": "https://hunterboots.co.jp/products/uft7101nyl-blk.json"}},
    {"id": "hunter-travel2suede", "cat": "shoe", "brand": "헌터", "name": "트래블 2.0 방수 스웨이드 스니커즈", "code": "UFF7146REN", "src": "page", "hint": "uff7146renblk", "urls": {
        "KR": "https://www.kolonmall.com/Brands/HUNTER/Product/K1784599846737092BK01",
        "JP": "https://hunterboots.co.jp/products/uff7146ren-blk.json"}},
    # 예비 4개(트래블 2.0 레이스 UFF7147REN·원더러 부클 숏 WFS2226WAD(일본 −50% 할인 중 · compare_at 정가)·원더러 프로텍트 UFF7139REN·트래블 플로우 UFF7159LEA)도
    # 한국·일본 정가 읽기 OK(11/21)였으나 브랜드당 20개 상한이라 뺌 — 위 상품이 몰에서 빠지면 대신 넣을 후보(남성 오리지널 숏·톨·첼시·플레이 숏은 코오롱몰 K 번호를 찾으면 4개 나라 · 바꿀 때 우선)
    # v1.17 언더아머 두바이 = underarmour.ae(공식 중동 유통사 Athlocity · SFCC) — 색상 페이지 UA품번-색상(정가는 색상과 같음 · 11/03 확인) · sfra_list
    {"id": "ua-tech2", "cat": "top", "brand": "언더아머", "name": "UA 테크 2.0 반팔", "code": "1326413", "src": "page", "hint": "ua tech", "urls": {
        "KR": "https://www.underarmour.co.kr/ko-kr/p/%EC%83%81%EC%9D%98/ua_tech_2.0/1326413.html",
        "US": "https://www.underarmour.com/en-us/p/ua_tech_2.0_mens_short_sleeve/1326413.html",
        "GB": "https://www.underarmour.co.uk/en-gb/p/ua-tech-2.0-mens-short-sleeve/1326413.html",
        "DE": "https://www.underarmour.de/de-de/p/ua-tech-2.0/1326413.html",
        "MX": "https://www.underarmour.com.mx/es-mx/p/tops/ua_tech_2.0/1326413.html",
        "AE": "https://www.underarmour.ae/en/ua-tech-2.0/UA1326413-001.html"}},   # 일본은 수입사(DOME) 품번·사양이 달라 뺌
    {"id": "ua-hg-mock", "cat": "top", "brand": "언더아머", "name": "히트기어 컴프레션 모크 반팔", "code": "1372586", "src": "page", "hint": "heatgear", "urls": {
        "KR": "https://www.underarmour.co.kr/ko-kr/p/%EC%83%81%EC%9D%98/heatgear_%EC%BB%B4%ED%94%84%EB%A0%88%EC%85%98/1372586.html",
        "US": "https://www.underarmour.com/en-us/p/heatgear_compression_mens_mock_short_sleeve/1372586.html",
        "GB": "https://www.underarmour.co.uk/en-gb/p/heatgear-compression-mens-mock-short-sleeve/1372586.html",
        "DE": "https://www.underarmour.de/de-de/p/heatgear-compression/1372586.html",
        "MX": "https://www.underarmour.com.mx/es-mx/p/house_of_baselayer/heatgear_compression/1372586.html",
        "AE": "https://www.underarmour.ae/en/mens-heatgearreg-compression-mock-short-sleeve/UA1372586-001.html"}},   # v1.6 히트기어 컴프레션 반팔 1361518·긴팔 1361524 대신(멕시코 몰에서 빠짐 — HTTP 410 · 10/26 사이트맵에 없음)
    {"id": "ua-hustle6", "cat": "bag", "brand": "언더아머", "name": "허슬 6.0 백팩", "code": "1384672", "src": "page", "hint": "hustle", "urls": {
        "KR": "https://www.underarmour.co.kr/ko-kr/p/%EC%95%A1%EC%84%B8%EC%84%9C%EB%A6%AC/ua_%ED%97%88%EC%8A%AC_6.0/1384672.html",
        "US": "https://www.underarmour.com/en-us/p/ua_hustle_6.0_backpack/1384672.html",
        "GB": "https://www.underarmour.co.uk/en-gb/p/ua-hustle-6.0-backpack/1384672.html",
        "DE": "https://www.underarmour.de/de-de/p/ua-hustle-6.0/1384672.html",
        "MX": "https://www.underarmour.com.mx/es-mx/p/mochilas_y_bolsos/ua_hustle_6.0/1384672.html",
        "AE": "https://www.underarmour.ae/en/ua-hustle-6.0/UA1384672-002.html"}},   # 5개 나라 같은 품번(GitHub 서버 시험 10/26 — 차지드 어서트 11은 한국·멕시코 robots.txt가 막음) · 두바이 -001(검정)은 품절·사이트맵에 없어 -002(JSON-LD 품번이 바코드라 이름 + 품번 표시로 확인)
    {"id": "ua-tech-hz", "cat": "wear", "brand": "언더아머", "name": "UA 테크 ½ 집", "code": "1328495", "src": "page", "hint": "ua tech", "urls": {
        "KR": "https://www.underarmour.co.kr/ko-kr/p/%EC%83%81%EC%9D%98/ua_tech/1328495.html",
        "US": "https://www.underarmour.com/en-us/p/ua_tech_mens_1-2_zip_long_sleeve/1328495.html",
        "GB": "https://www.underarmour.co.uk/en-gb/p/ua-tech-mens-1-2-zip-long-sleeve/1328495.html",
        "DE": "https://www.underarmour.de/de-de/p/ua-tech/1328495.html",
        "AE": "https://www.underarmour.ae/en/ua-tech/UA1328495-001.html"}},   # 멕시코 몰은 정가 없이 할인가(539.4페소)만 보여 뺌(시험 10/22)
    {"id": "ua-leftchest", "cat": "top", "brand": "언더아머", "name": "레프트 체스트 로고 반팔", "code": "1326799", "src": "page", "hint": "left chest", "urls": {
        "KR": "https://www.underarmour.co.kr/ko-kr/p/%EC%83%81%EC%9D%98/ua_%EB%A0%88%ED%94%84%ED%8A%B8_%EC%B2%B4%EC%8A%A4%ED%8A%B8_%EB%A1%9C%EA%B3%A0/1326799.html",
        "US": "https://www.underarmour.com/en-us/p/ua_left_chest_logo_mens_short_sleeve/1326799.html",
        "GB": "https://www.underarmour.co.uk/en-gb/p/ua-left-chest-logo-mens-short-sleeve/1326799.html",
        "DE": "https://www.underarmour.de/de-de/p/ua-left-chest-logo/1326799.html",
        "MX": "https://www.underarmour.com.mx/es-mx/p/tops/ua_left_chest_logo/1326799.html",
        "AE": "https://www.underarmour.ae/en/mens-ua-sportstyle-left-chest-short-sleeve-shirt/UA1326799-001.html"}},   # 두바이 -001·-100 정가 같음(11/03)
    {"id": "ua-icon-hoodie", "cat": "wear", "brand": "언더아머", "name": "아이콘 플리스 후디", "code": "1373880", "src": "page", "hint": "icon fleece", "urls": {
        "KR": "https://www.underarmour.co.kr/ko-kr/p/%EC%83%81%EC%9D%98/ua_%EC%95%84%EC%9D%B4%EC%BD%98_%ED%94%8C%EB%A6%AC%EC%8A%A4/1373880.html",
        "US": "https://www.underarmour.com/en-us/p/ua_icon_fleece_mens_hoodie/1373880.html",
        "GB": "https://www.underarmour.co.uk/en-gb/p/ua-icon-fleece-mens-hoodie/1373880.html",
        "DE": "https://www.underarmour.de/de-de/p/ua-icon-fleece/1373880.html",
        "MX": "https://www.underarmour.com.mx/es-mx/p/tops/sudadera_con_capucha_ua_icon_fleece_para_hombre/1373880.html",
        "AE": "https://www.underarmour.ae/en/mens-ua-essential-fleece-hoodie/UA1373880-012.html"}},   # v1.7 SKU 늘리기 — 5개 나라 같은 품번(GitHub 서버 시험 10/26) · 두바이는 -001 없음 → -012(주소 이름만 essential · 품번·상품 이름 UA Icon Fleece 같음)
    {"id": "ua-hg-sleeveless", "cat": "top", "brand": "언더아머", "name": "히트기어 모크 민소매", "code": "1361521", "src": "page", "hint": "heatgear", "urls": {
        "KR": "https://www.underarmour.co.kr/ko-kr/p/%EC%83%81%EC%9D%98/heatgear_%EB%AA%A8%ED%81%AC/1361521.html",
        "US": "https://www.underarmour.com/en-us/p/heatgear_mock_mens_sleeveless/1361521.html",
        "GB": "https://www.underarmour.co.uk/en-gb/p/heatgear-mock-mens-sleeveless/1361521.html",
        "DE": "https://www.underarmour.de/de-de/p/heatgear-mock/1361521.html",
        "MX": "https://www.underarmour.com.mx/es-mx/p/house_of_baselayer/playera_de_cuello_alto_sin_mangas_heatgear_para_hombre/1361521.html",
        "AE": "https://www.underarmour.ae/en/heatgearreg-mock/UA1361521-001.html"}},
    {"id": "ua-undeniable-l", "cat": "bag", "brand": "언더아머", "name": "언디나이어블 5.0 더플백 라지", "code": "1369224", "src": "page", "hint": "undeniable", "urls": {
        "KR": "https://www.underarmour.co.kr/ko-kr/p/%EA%B0%80%EB%B0%A9/ua_%EC%96%B8%EB%94%94%EB%82%98%EC%9D%B4%EC%96%B4%EB%B8%94_5.0_%EB%9D%BC%EC%A7%80/1369224.html",
        "US": "https://www.underarmour.com/en-us/p/ua_undeniable_5.0_large_duffle_bag/1369224.html",
        "GB": "https://www.underarmour.co.uk/en-gb/p/ua-undeniable-5.0-large-duffle-bag/1369224.html",
        "DE": "https://www.underarmour.de/de-de/p/ua-undeniable-5.0-large/1369224.html",
        "MX": "https://www.underarmour.com.mx/es-mx/p/mochilas_y_bolsos/ua_undeniable_5.0_grande/1369224.html",
        "AE": "https://www.underarmour.ae/en/ua-undeniable-5.0-large-duffle-bag/UA1369224-001.html"}},   # v1.18 일본은 수입사 품번·사양이 달라 뺌(다른 언더아머와 같음) · 11/10 두바이 할인 중
    {"id": "ua-reign6", "cat": "shoe", "brand": "언더아머", "name": "UA 레인 6 트레이닝화(남성)", "code": "3027341", "src": "page", "hint": "reign", "urls": {
        "KR": "https://www.underarmour.co.kr/ko-kr/p/%EC%8B%A0%EB%B0%9C/ua_%EB%A0%88%EC%9D%B8_6/3027341.html",
        "US": "https://www.underarmour.com/en-us/p/ua_reign_6_mens_training_shoes/3027341.html",
        "GB": "https://www.underarmour.co.uk/en-gb/p/ua-reign-6-mens-training-shoes/3027341.html",
        "DE": "https://www.underarmour.de/de-de/p/ua-reign-6/3027341.html",
        "MX": "https://www.underarmour.com.mx/es-mx/p/entrenamiento/tenis_de_entrenamiento_ua_tribase_reign_6_para_hombre/3027341.html",
        "AE": "https://www.underarmour.ae/en/ua-reign-6/UA3027341-001.html"}},   # v1.18 · 11/10 영국·독일·두바이 할인 중
    {"id": "saucony-ride19", "cat": "shoe", "brand": "써코니", "name": "라이드 19(남성)", "code": "S21055", "src": "page", "hint": "라이드 19", "code_in_page": True, "urls": {
        "KR": "https://saucony.co.kr/product/%EB%82%A8%EC%84%B1-%EB%9D%BC%EC%9D%B4%EB%93%9C-19-whitecrimson/210/",   # 품번은 상품 정보 칸 '모델 S21055-172'
        "US": "https://www.saucony.com/en/ride-19/60823M.html",
        "GB": "https://www.saucony.com/UK/en_GB/ride-19/60823M.html",
        "DE": "https://www.saucony.com/DE/de_DE/ride-19/60823M.html"}},   # 해마다 새 모델(라이드 20 등)이 나오면 품번·주소를 바꿈
    {"id": "saucony-endspeed5", "cat": "shoe", "brand": "써코니", "name": "엔돌핀 스피드 5(남성)", "code": "S21007", "src": "page", "hint": "엔돌핀 스피드 5", "code_in_page": True, "urls": {
        "KR": "https://saucony.co.kr/product/%EB%82%A8%EC%84%B1-%EC%97%94%EB%8F%8C%ED%95%80-%EC%8A%A4%ED%94%BC%EB%93%9C-5-whitecrimson/220/",   # v1.18 화이트/검(164)은 전 사이즈 품절로 JSON-LD 가격 없음
        "US": "https://www.saucony.com/en/endorphin-speed-5/60307M.html"}},   # v1.18 영국·독일 몰은 10/30부터 404(유럽은 엔돌핀 스피드 6 S101825 — 한국 몰에 6이 들어오면 품번·주소를 6으로)
    {"id": "saucony-endpro5", "cat": "shoe", "brand": "써코니", "name": "엔돌핀 프로 5(남성)", "code": "S21064", "src": "page", "hint": "엔돌핀 프로 5", "code_in_page": True, "urls": {
        "KR": "https://saucony.co.kr/product/%EB%82%A8%EC%84%B1-%EC%97%94%EB%8F%8C%ED%95%80-%ED%94%84%EB%A1%9C-5-whiteblack/302/",
        "US": "https://www.saucony.com/en/endorphin-pro-5/60803M.html?dwvar_60803M_color=S21064-100",   # 색상 없는 주소는 10/23부터 JSON-LD 없는 페이지
        "GB": "https://www.saucony.com/UK/en_GB/endorphin-pro-5/60803M.html",
        "DE": "https://www.saucony.com/DE/de_DE/endorphin-pro-5/60803M.html"}},
    {"id": "saucony-triumph24", "cat": "shoe", "brand": "써코니", "name": "트라이엄프 24(남성)", "code": "S100997", "src": "page", "hint": "트라이엄프 24", "code_in_page": True, "urls": {
        "KR": "https://saucony.co.kr/product/%EB%82%A8%EC%84%B1-%ED%8A%B8%EB%9D%BC%EC%9D%B4%EC%97%84%ED%94%84-24-triple-black/418/",
        "US": "https://www.saucony.com/en/triumph-24/61229M.html",
        "GB": "https://www.saucony.com/UK/en_GB/triumph-24/61229M.html",
        "DE": "https://www.saucony.com/DE/de_DE/triumph-24/61229M.html"}},
    {"id": "saucony-guide19", "cat": "shoe", "brand": "써코니", "name": "가이드 19(남성)", "code": "S21058", "src": "page", "hint": "가이드 19", "code_in_page": True, "urls": {
        "KR": "https://saucony.co.kr/product/%EB%82%A8%EC%84%B1-%EA%B0%80%EC%9D%B4%EB%93%9C-19-fossilcarbon/372/",   # v1.25 triple-black(373)은 전 사이즈 품절로 가격 없음 → fossilcarbon(같은 품번 S21058 · 11/21 179,000원)
        "US": "https://www.saucony.com/en/guide-19/60838M.html",
        "GB": "https://www.saucony.com/UK/en_GB/guide-19/60838M.html",
        "DE": "https://www.saucony.com/DE/de_DE/guide-19/60838M.html"}},
    {"id": "saucony-hurricane26", "cat": "shoe", "brand": "써코니", "name": "허리케인 26(남성)", "code": "S101098", "src": "page", "hint": "허리케인 26", "code_in_page": True, "urls": {
        "KR": "https://saucony.co.kr/product/%EB%82%A8%EC%84%B1-%ED%97%88%EB%A6%AC%EC%BC%80%EC%9D%B8-26-triple-black/535/",
        "US": "https://www.saucony.com/en/hurricane-26/61249M.html",
        "GB": "https://www.saucony.com/UK/en_GB/hurricane-26/61249M.html",
        "DE": "https://www.saucony.com/DE/de_DE/hurricane-26/61249M.html"}},
    {"id": "saucony-kinvara16", "cat": "shoe", "brand": "써코니", "name": "킨바라 16(남성)", "code": "S21020", "src": "page", "hint": "킨바라 16", "code_in_page": True, "urls": {
        "KR": "https://saucony.co.kr/product/%EB%82%A8%EC%84%B1-%ED%82%A8%EB%B0%94%EB%9D%BC-16-blackwhite/153/",
        "US": "https://www.saucony.com/en/kinvara-16/60309M.html"}},   # 영국·독일 몰 같은 주소는 다른 색상 품번(S101468)만 있어 뺌(시험 10/22)
    # v1.21 SKU 9차 — 한국 몰 상품 화면의 품번(상품 설명 그림 이름 SAUCONY29S…-색상) ∩ 미국·영국·독일 몰 같은 품번(data-stock-number · 11/17 정가 읽기 확인)
    {"id": "saucony-azura", "cat": "shoe", "brand": "써코니", "name": "엔돌핀 아주라(남성)", "code": "S21070", "src": "page", "hint": "엔돌핀 아주라", "code_in_page": True, "urls": {
        "KR": "https://saucony.co.kr/product/%EB%82%A8%EC%84%B1-%EC%97%94%EB%8F%8C%ED%95%80-%EC%95%84%EC%A3%BC%EB%9D%BC-whitecrimson/314/",
        "US": "https://www.saucony.com/en/endorphin-azura/60807M.html?dwvar_60807M_color=S21070-172",
        "GB": "https://www.saucony.com/UK/en_GB/endorphin-azura/60807M.html",
        "DE": "https://www.saucony.com/DE/de_DE/endorphin-azura/60807M.html"}},
    {"id": "saucony-endtrainer", "cat": "shoe", "brand": "써코니", "name": "엔돌핀 트레이너(남성)", "code": "S20996", "src": "page", "hint": "엔돌핀 트레이너", "code_in_page": True, "urls": {
        "KR": "https://saucony.co.kr/product/%EB%82%A8%EC%84%B1-%EC%97%94%EB%8F%8C%ED%95%80-%ED%8A%B8%EB%A0%88%EC%9D%B4%EB%84%88-whitenavy/214/",
        "GB": "https://www.saucony.com/UK/en_GB/endorphin-trainer/59961M.html",
        "DE": "https://www.saucony.com/DE/de_DE/endorphin-trainer/59961M.html"}},   # 미국 몰 같은 주소 HTTP 404(11/17) · 엑소더스 울트라 4는 한국 몰 가격 없음(품절)이라 뺌
    # SKU 2차(11/21) — 한국 몰 상품 정보 칸 '모델' 품번 ∩ 미국·영국·독일 몰 같은 품번(data-stock-number · 11/21 GitHub 서버 정가 읽기 확인) · 여성 모델·옷 포함
    {"id": "saucony-azuraw", "cat": "shoe", "brand": "써코니", "name": "엔돌핀 아주라(여성)", "code": "S11070", "src": "page", "hint": "엔돌핀 아주라", "code_in_page": True, "urls": {
        "KR": "https://saucony.co.kr/product/%EC%97%AC%EC%84%B1-%EC%97%94%EB%8F%8C%ED%95%80-%EC%95%84%EC%A3%BC%EB%9D%BC-ivorywhite/307/",
        "US": "https://www.saucony.com/en/endorphin-azura/60808W.html",
        "GB": "https://www.saucony.com/UK/en_GB/endorphin-azura/60808W.html",
        "DE": "https://www.saucony.com/DE/de_DE/endorphin-azura/60808W.html"}},   # 11/21 영국·독일 할인 중(£140 → £112 · €160 → €128 — 정가는 원래 가격 칸)
    {"id": "saucony-endpro5w", "cat": "shoe", "brand": "써코니", "name": "엔돌핀 프로 5(여성)", "code": "S11064", "src": "page", "hint": "엔돌핀 프로 5", "code_in_page": True, "urls": {
        "KR": "https://saucony.co.kr/product/%EC%97%AC%EC%84%B1-%EC%97%94%EB%8F%8C%ED%95%80-%ED%94%84%EB%A1%9C-5-whiteblack/298/",
        "US": "https://www.saucony.com/en/endorphin-pro-5/60804W.html?dwvar_60804W_color=S11064-101"}},   # 색상 없는 주소는 미국·영국·독일 모두 JSON-LD 없는 페이지(11/21) — 미국만 색상 지정 주소로 확인, 영국·독일은 다음 차례에
    {"id": "saucony-omnist23", "cat": "shoe", "brand": "써코니", "name": "옴니 ST 23(남성)", "code": "S21072", "src": "page", "hint": "옴니 st 23", "code_in_page": True, "urls": {
        "KR": "https://saucony.co.kr/product/%EB%82%A8%EC%84%B1-%EC%98%B4%EB%8B%88-st-23-triple-black/289/",
        "US": "https://www.saucony.com/en/omni-st-23/60844M.html",
        "GB": "https://www.saucony.com/UK/en_GB/omni-st-23/60844M.html",
        "DE": "https://www.saucony.com/DE/de_DE/omni-st-23/60844M.html"}},
    {"id": "saucony-trainer80", "cat": "shoe", "brand": "써코니", "name": "트레이너 80(공용)", "code": "S70884", "src": "page", "hint": "트레이너 80", "code_in_page": True, "urls": {
        "KR": "https://saucony.co.kr/product/%EA%B3%B5%EC%9A%A9-%ED%8A%B8%EB%A0%88%EC%9D%B4%EB%84%88-80-blackwhite/222/",
        "GB": "https://www.saucony.com/UK/en_GB/trainer-80/59999U.html",
        "DE": "https://www.saucony.com/DE/de_DE/trainer-80/59999U.html"}},   # 미국 몰 같은 주소는 JSON-LD 없는 페이지(11/21)라 뺌 · 11/21 영국·독일 할인 중(£85 → £68 · €100 → €80)
    {"id": "saucony-peregrine16", "cat": "shoe", "brand": "써코니", "name": "페레그린 16 와이드(남성)", "code": "S21067", "src": "page", "hint": "페레그린 16", "code_in_page": True, "urls": {
        "KR": "https://saucony.co.kr/product/%EB%82%A8%EC%84%B1-%ED%8E%98%EB%A0%88%EA%B7%B8%EB%A6%B0-16-%EC%99%80%EC%9D%B4%EB%93%9C-carbonblack/211/",
        "US": "https://www.saucony.com/en/peregrine-16-wide/60849M.html"}},   # 한국 몰은 와이드(S21067) — 보통 폭 주소(60848M)는 미국 JSON-LD 없음·영국·독일 페이지에 S21067 없음(11/21)이라 미국 와이드 몰만
    {"id": "saucony-recoveryhoody", "cat": "wear", "brand": "써코니", "name": "리커버리 후디(공용)", "code": "SAU800047", "src": "page", "hint": "리커버리 후디", "code_in_page": True, "urls": {
        "KR": "https://saucony.co.kr/product/%EA%B3%B5%EC%9A%A9-%EB%A6%AC%EC%BB%A4%EB%B2%84%EB%A6%AC-%ED%9B%84%EB%94%94-light-grey-heather/275/",
        "US": "https://www.saucony.com/en/recovery-hoody/58009U.html"}},
    {"id": "saucony-hurricanejkt", "cat": "wear", "brand": "써코니", "name": "허리케인 워터프루프 재킷(남성)", "code": "SAM800360", "src": "page", "hint": "허리케인 워터프루프 재킷", "code_in_page": True, "urls": {
        "KR": "https://saucony.co.kr/product/%EB%82%A8%EC%84%B1-%ED%97%88%EB%A6%AC%EC%BC%80%EC%9D%B8-%EC%9B%8C%ED%84%B0%ED%94%84%EB%A3%A8%ED%94%84-%EC%9E%AC%ED%82%B7-white-black/278/",
        "US": "https://www.saucony.com/en/hurricane-waterproof-jacket/58003M.html"}},
    {"id": "saucony-stopwatchls", "cat": "wear", "brand": "써코니", "name": "스톱워치 롱 슬리브(남성)", "code": "SAM800379", "src": "page", "hint": "스톱워치 롱 슬리브", "code_in_page": True, "urls": {
        "KR": "https://saucony.co.kr/product/%EB%82%A8%EC%84%B1-%EC%8A%A4%ED%86%B1%EC%9B%8C%EC%B9%98-%EB%A1%B1-%EC%8A%AC%EB%A6%AC%EB%B8%8C-ivory-heather/271/",
        "US": "https://www.saucony.com/en/stopwatch-long-sleeve/58947M.html",
        "GB": "https://www.saucony.com/UK/en_GB/stopwatch-long-sleeve/58947M.html",
        "DE": "https://www.saucony.com/DE/de_DE/stopwatch-long-sleeve/58947M.html"}},   # 긴팔이라 분류 wear(top = 반팔·민소매) · 11/21 미국 할인 중($48 → $35.95)
    {"id": "saucony-outpace5", "cat": "wear", "brand": "써코니", "name": "아웃페이스 5인치 쇼츠(남성)", "code": "SAM800410", "src": "page", "hint": "아웃페이스 5인치", "code_in_page": True, "urls": {
        "KR": "https://saucony.co.kr/product/%EB%82%A8%EC%84%B1-%EC%95%84%EC%9B%83%ED%8E%98%EC%9D%B4%EC%8A%A4-5%EC%9D%B8%EC%B9%98-%EC%87%BC%EC%B8%A0-black/250/",
        "US": "https://www.saucony.com/en/outpace-5-inch-short/60026M.html",
        "GB": "https://www.saucony.com/UK/en_GB/outpace-5-inch-short/60026M.html",
        "DE": "https://www.saucony.com/DE/de_DE/outpace-5-inch-short/60026M.html"}},
    # 뺌(11/21): 엔돌핀 스피드 5 여성(S11007) — 한국 몰 연결 끊김(한 번 · 1단계에선 219,000원 읽힘 · 미국·영국·독일 정가 읽기 OK) → 다음 차례에
    # 뺌: 라이드 19 여성·킨바라 16 여성·프로그리드 가이드 7·프로그리드 트라이엄프 4 — 미국·영국·독일 몰 모두 JSON-LD 없는 페이지(색상 지정 주소로 다음 차례에) · 가이드 19 여성 — 한국 /512/·/510/ 페이지에 품번 S11058 없음
    # 뺌: 엔돌핀 엘리트 2(S30994) — 정가 읽기는 OK(한국 339,000 · $290 · £280 · €300)이나 새 모델 엘리트 3(한국 369,000원 · S100981)이 나와 해외 3곳 모두 약 50% 재고 정리 중 → 엘리트 3로 다음 차례에
    # 뺌(11/21 검증): 엔돌핀 싱글렛(SAM800382)·엔돌핀 쇼트 슬리브(SAM800394) — 영국·독일 값의 한국 정가 비율이 써코니 가운데값의 1.6~1.8배(블프 할인가가 정가로 읽힌 것으로 봄) · 빼면 한국만 남아 상품째 뺌
    {"id": "brooks-ghost18", "cat": "shoe", "brand": "브룩스", "name": "고스트 18(남성)", "code": "1104931D", "cc_code": {"JP": "BRM4933"}, "src": "page", "hint": "고스트 18", "code_in_page": True, "urls": {
        "KR": "https://brooksrunning.co.kr/product/%EB%82%A8%EC%84%B1-%EA%B3%A0%EC%8A%A4%ED%8A%B8-18-%EB%B8%94%EB%9E%99-medium/852/",   # 품번은 prd_model 칸(1104931D020)
        "JP": "https://brooksrunning.co.jp/products/brm4933-b-b.json"}},   # 일본 수입사 품번 BRM4933 = 고스트 18 남성 보통 폭 · 미국·유럽 몰은 403(넣지 않음)
    {"id": "brooks-ghost18w", "cat": "shoe", "brand": "브룩스", "name": "고스트 18(여성)", "code": "1204821B", "cc_code": {"JP": "BRW4822"}, "src": "page", "hint": "고스트 18", "code_in_page": True, "urls": {
        "KR": "https://brooksrunning.co.kr/product/%EC%97%AC%EC%84%B1-%EA%B3%A0%EC%8A%A4%ED%8A%B8-18-%ED%99%94%EC%9D%B4%ED%8A%B8-medium/864/",
        "JP": "https://brooksrunning.co.jp/products/brw4822-blk.json"}},
    {"id": "brooks-glycgts23", "cat": "shoe", "brand": "브룩스", "name": "글리세린 GTS 23(남성)", "code": "1105031D", "cc_code": {"JP": "BRM5033"}, "src": "page", "hint": "글리세린 gts 23", "code_in_page": True, "urls": {
        "KR": "https://brooksrunning.co.kr/product/%EB%82%A8%EC%84%B1-%EA%B8%80%EB%A6%AC%EC%84%B8%EB%A6%B0-gts-23%ED%8E%84-medium/799/",
        "JP": "https://brooksrunning.co.jp/products/brm5033-blk-w.json"}},
    {"id": "brooks-glycmax2", "cat": "shoe", "brand": "브룩스", "name": "글리세린 맥스 2(남성)", "code": "1104791D", "cc_code": {"JP": "BRM4793"}, "src": "page", "hint": "글리세린 맥스 2", "code_in_page": True, "urls": {
        "KR": "https://brooksrunning.co.kr/product/%EB%82%A8%EC%84%B1-%EA%B8%80%EB%A6%AC%EC%84%B8%EB%A6%B0-%EB%A7%A5%EC%8A%A4-2%ED%8C%AC%ED%85%80-medium/697/",
        "JP": "https://brooksrunning.co.jp/products/brm4793-b-b.json"}},
    {"id": "brooks-ghostamp", "cat": "shoe", "brand": "브룩스", "name": "고스트 AMP(남성)", "code": "1104971D", "cc_code": {"JP": "BRM4973"}, "src": "page", "hint": "고스트 amp", "code_in_page": True, "urls": {
        "KR": "https://brooksrunning.co.kr/product/%EB%82%A8%EC%84%B1-%EA%B3%A0%EC%8A%A4%ED%8A%B8-amp%ED%94%84%EB%9D%BC%EC%9D%B4%EB%A8%B8medium/947/",
        "JP": "https://brooksrunning.co.jp/products/brm4973-blu.json"}},
    # v1.13 SKU 4차 — 한국 몰이 블랙프라이데이 할인 중(10/28)이라 JSON-LD에는 판매가만 → 소비자가 칸(price_custom, CAFE24_LIST)으로 정가 · 일본은 한국과 같은 색이 없어 다른 색(같은 품번 · 색과 상관없이 같은 값)
    {"id": "brooks-gts25", "cat": "shoe", "brand": "브룩스", "name": "아드레날린 GTS 25(남성)", "code": "1104541D", "cc_code": {"JP": "BRM4543"}, "src": "page", "hint": "아드레날린gts 25", "code_in_page": True, "urls": {
        "KR": "https://brooksrunning.co.kr/product/%EB%82%A8%EC%84%B1-%EC%95%84%EB%93%9C%EB%A0%88%EB%82%A0%EB%A6%B0gts-25%EB%B8%94%EB%9E%99medium/664/",
        "JP": "https://brooksrunning.co.jp/products/brm4543-dgry.json"}},
    {"id": "brooks-hyperion3", "cat": "shoe", "brand": "브룩스", "name": "하이페리온 3(남성)", "code": "1104651D", "cc_code": {"JP": "BRM4653"}, "src": "page", "hint": "하이페리온 3", "code_in_page": True, "urls": {
        "KR": "https://brooksrunning.co.kr/product/%EB%82%A8%EC%84%B1-%ED%95%98%EC%9D%B4%ED%8E%98%EB%A6%AC%EC%98%A8-3%EC%98%A4%EC%9D%B4%EC%8A%A4%ED%84%B0-medium/583/",
        "JP": "https://brooksrunning.co.jp/products/brm4653-gry.json"}},
    # v1.16 SKU 7차 — 한국 robots.txt 사이트맵은 카페24 데모 사이트(ecudemo…)라 첫 화면·목록에서 상품 번호 → 상품 페이지 prd_model 품번 · 일본 products.json 정가(compare_at 없음)
    {"id": "brooks-glycerin23", "cat": "shoe", "brand": "브룩스", "name": "글리세린 23(남성)", "code": "1104761D", "cc_code": {"JP": "BRM4763"}, "src": "page", "hint": "글리세린 23", "code_in_page": True, "urls": {
        "KR": "https://brooksrunning.co.kr/product/%EB%82%A8%EC%84%B1-%EA%B8%80%EB%A6%AC%EC%84%B8%EB%A6%B0-23%EB%B8%94%EB%9E%99-medium/784/",   # prd_model 1104761D020 · 블프 판매가 139,300 → 소비자가 칸 199,000(11/03)
        "JP": "https://brooksrunning.co.jp/products/brm4763-blk.json"}},
    {"id": "brooks-ghostmax4", "cat": "shoe", "brand": "브룩스", "name": "고스트 맥스 4(남성)", "code": "1104961D", "cc_code": {"JP": "BRM4963"}, "src": "page", "hint": "고스트 맥스 4", "code_in_page": True, "urls": {
        "KR": "https://brooksrunning.co.kr/product/%EB%82%A8%EC%84%B1-%EA%B3%A0%EC%8A%A4%ED%8A%B8-%EB%A7%A5%EC%8A%A4-4%EA%B7%B8%EB%A0%88%EC%9D%B4-medium/962/",   # 남성 보통 폭 검정이 없어 그레이(1104961D015 · 같은 품번 · 색과 상관없이 같은 값)
        "JP": "https://brooksrunning.co.jp/products/brm4963-blk.json"}},
    {"id": "brooks-cascadia20", "cat": "shoe", "brand": "브룩스", "name": "캐스캐디아 20(남성)", "code": "1104891D", "cc_code": {"JP": "BMM4893"}, "src": "page", "hint": "캐스캐디아 20", "code_in_page": True, "urls": {
        "KR": "https://brooksrunning.co.kr/product/%EB%82%A8%EC%84%B1-%EC%BA%90%EC%8A%A4%EC%BA%90%EB%94%94%EC%95%84-20%EB%B8%94%EB%9E%99-medium/973/",   # prd_model 1104891D027
        "JP": "https://brooksrunning.co.jp/products/bmm4893-gry.json"}},   # 일본 트레일 모델 품번은 BMM…(로드 BRM…) · 일본은 검정이 없어 그레이
    # v1.4 아크테릭스 — 한국은 시즌 상품 페이지마다 한국 품번(cc_code KR, 페이지 Model(KR))이 따로 · JSON-LD 판매가 + 화면 데이터 정가(retail_price)
    {"id": "arc-atomhoody", "cat": "wear", "brand": "아크테릭스", "name": "아톰 후디(남성)", "code": "X000009556", "cc_code": {"KR": "AJQSM09556"}, "src": "page", "hint": "atom hoody",
     "urls": _arc("686241", "atom-hoody-9556", "atom-hoody-m")},
    {"id": "arc-atomjacket", "cat": "wear", "brand": "아크테릭스", "name": "아톰 재킷(남성)", "code": "X000009561", "cc_code": {"KR": "AJPFM09561"}, "src": "page", "hint": "atom jacket",
     "urls": _arc("685690", "atom-jacket-9561", "atom-jacket-m")},   # 한국은 2025 가을·겨울 페이지(2026 페이지 없음 · 10/23)
    {"id": "arc-gammapant", "cat": "wear", "brand": "아크테릭스", "name": "감마 팬츠(남성)", "code": "X000010481", "cc_code": {"KR": "APQSM10481"}, "src": "page", "hint": "gamma pant",
     "urls": _arc("686323", "gamma-pant-0481", "gamma-pant-m")},
    {"id": "arc-squamish", "cat": "wear", "brand": "아크테릭스", "name": "스쿼미시 후디(남성)", "code": "X000010276", "cc_code": {"KR": "AJQSM10276"}, "src": "page", "hint": "squamish hoody",
     "urls": _arc("686259", "squamish-hoody-0276", "squamish-hoody-m")},
    {"id": "arc-cerium", "cat": "wear", "brand": "아크테릭스", "name": "세륨 후디(남성)", "code": "X000010521", "cc_code": {"KR": "AJQFM10521"}, "src": "page", "hint": "cerium hoody",
     "urls": _arc("686764", "cerium-hoody-0521", "cerium-hoody-m")},
    {"id": "arc-mantis26", "cat": "bag", "brand": "아크테릭스", "name": "맨티스 26 백팩", "code": "X000010643", "cc_code": {"KR": "ABQSU10643"}, "src": "page", "hint": "mantis 26",
     "urls": _arc("686432", "mantis-26-backpack-0643", g="")},   # 일본 몰 mantis-26-backpack은 옛 모델(X000009825)이라 뺌 · 맨티스 2 웨이스트 팩은 한국 페이지에 가격 데이터가 없어 넣지 않음(10/23)
    # v1.15 SKU 6차 — 한국 상품 번호는 공개 기획전 페이지(/lp)의 상품 이미지 주소 products/{상품 번호}/S26_X0000{모델}에서 찾아 상품 페이지 품번으로 확인 ·
    #   일본 몰 신발 페이지는 JSON-LD가 없어 상품 .json(변형 품번 X0000…)
    {"id": "arc-norvanld4gtx", "cat": "shoe", "brand": "아크테릭스", "name": "노반 LD 4 GTX(남성)", "code": "X000010397", "cc_code": {"KR": "AFQFM10397"}, "src": "page", "hint": "norvan ld 4 gtx",
     "urls": _arc("686729", "norvan-ld-4-gtx-shoe-0397", "norvan-ld-4-gtx-m.json")},
    {"id": "arc-sylan2", "cat": "shoe", "brand": "아크테릭스", "name": "사일렌 2(남성)", "code": "X000010155", "cc_code": {"KR": "AFQSM10155"}, "src": "page", "hint": "sylan 2",
     "urls": _arc("686215", "sylan-2-shoe-0155", "sylan-2-m.json")},
    {"id": "arc-kragg", "cat": "shoe", "brand": "아크테릭스", "name": "크래그(남성)", "code": "X000010078", "cc_code": {"KR": "AFQFM10078"}, "src": "page", "hint": "kragg",
     "urls": _arc("686681", "kragg-shoe-0078", "kragg-m.json")},
    {"id": "arc-konsealtrek", "cat": "boot", "brand": "아크테릭스", "name": "컨실 트렉 부츠(남성)", "code": "X000010504", "cc_code": {"KR": "AFQFM10504"}, "src": "page", "hint": "konseal trek boot",
     "urls": _arc("686731", "konseal-trek-boot-0504", "konseal-trek-m.json")},
    {"id": "arc-norvanjacket", "cat": "wear", "brand": "아크테릭스", "name": "노반 재킷(남성)", "code": "X000009571", "cc_code": {"KR": "AJQFM09571"}, "src": "page", "hint": "norvan jacket",
     "urls": _arc("686750", "norvan-jacket-9571", "norvan-jacket-m")},   # 노반 LD 4(GTX 아님)는 다음 차례 · 코펙 2 로우 GTX는 영국·독일 몰 404·일본 몰에 없어 뺌(10/29)
    # 20개 2차(11/21) — 한국 상품 번호·품번은 1단계에서 상품 페이지로 확인 · 블프 검사 = 한국 정가 ÷ (현지 정가 × 11/20 환율)이 기존 11개 나라별 가운데값
    #   (미국 1.29 · 영국 1.08 · 독일 1.18 · 일본 1.20)의 1.25배 안인 나라만 · 여성 신발은 같은 남성 모델과 모든 나라 정가가 같은지도 확인
    {"id": "arc-norvanld4", "cat": "shoe", "brand": "아크테릭스", "name": "노반 LD 4(남성)", "code": "X000010398", "cc_code": {"KR": "AFQFM10398"}, "src": "page", "hint": "norvan ld 4",
     "urls": {cc: u for cc, u in _arc("686685", "norvan-ld-4-shoe-0398", "norvan-ld-4-m.json").items() if cc not in ("GB", "DE")}},   # 영국 £90·독일 €102는 블프 40% 할인가가 정가로 읽힘(비율 1.85·1.94) — 블프 뒤 차례에
    {"id": "arc-norvan7vest", "cat": "bag", "brand": "아크테릭스", "name": "노반 7 베스트(남성)", "code": "X000006747", "cc_code": {"KR": "ABQFM06747"}, "src": "page", "hint": "norvan 7 vest",
     "urls": _arc("686986", "norvan-7-vest-6747", "norvan-7-vest-m.json")},   # 여성(6803)은 남성과 같은 값의 같은 모델이라 뺌
    {"id": "arc-kopecgtx", "cat": "shoe", "brand": "아크테릭스", "name": "코펙 GTX(남성)", "code": "X000010023", "cc_code": {"KR": "AFQFM10023"}, "src": "page", "hint": "kopec gtx",
     "urls": {cc: u for cc, u in _arc("686680", "kopec-gtx-shoe-0023", "kopec-gtx-m.json").items() if cc != "US"}},   # 미국 몰 사이트맵에 0023 없음 · 여성(0028)은 남성과 같은 값이라 뺌
    {"id": "arc-kraggw", "cat": "shoe", "brand": "아크테릭스", "name": "크래그(여성)", "code": "X000010081", "cc_code": {"KR": "AFQSW10081"}, "src": "page", "hint": "kragg",
     "urls": _arc("686228", "kragg-shoe-0081", "kragg-w.json", g="womens/")},
    {"id": "arc-sylan2w", "cat": "shoe", "brand": "아크테릭스", "name": "사일렌 2(여성)", "code": "X000010153", "cc_code": {"KR": "AFQSW10153"}, "src": "page", "hint": "sylan 2",
     "urls": _arc("686229", "sylan-2-shoe-0153", g="womens/")},   # 일본 몰 sylan-2-w는 404라 뺌(남성 주소 꼴에서 짐작한 주소)
    {"id": "arc-konsealtrekw", "cat": "boot", "brand": "아크테릭스", "name": "컨실 트렉 부츠(여성)", "code": "X000010502", "cc_code": {"KR": "AFQFW10502"}, "src": "page", "hint": "konseal trek boot",
     "urls": _arc("686738", "konseal-trek-boot-0502", "konseal-trek-w.json", g="womens/")},
    {"id": "arc-norvancrewlsw", "cat": "wear", "brand": "아크테릭스", "name": "노반 크루 셔츠 LS(여성)", "code": "X000010748", "cc_code": {"KR": "ATQFW10748"}, "src": "page", "hint": "norvan crew",
     "urls": _arc("687008", "norvan-crew-shirt-ls-0748", "norvan-crew-ls-w.json", g="womens/")},
    {"id": "arc-downwordls", "cat": "wear", "brand": "아크테릭스", "name": "노반 다운워드 로고 셔츠 LS(남성)", "code": "X000010730", "cc_code": {"KR": "ATQFM10730"}, "src": "page", "hint": "norvan downword logo",
     "urls": _arc("686883", "norvan-downword-logo-shirt-ls-0730", "norvan-downword-logo-ls-m.json")},   # 영국·독일은 지금 30% 할인 중(£63·€70) — 정가 £90·€100으로 읽힘(비율 정상)
    {"id": "arc-norvanshort3w", "cat": "wear", "brand": "아크테릭스", "name": "노반 쇼츠 3인치(여성)", "code": "X000010613", "cc_code": {"KR": "APQSW10613"}, "src": "page", "hint": "norvan short 3",
     "urls": _arc("686342", "norvan-short-3-0613", g="womens/")},   # 일본 몰에 없음
    # 뺌: 노반 LD 4 GTX 여성(0399)·노반 LD 4 여성(0400)은 남성(기존 0397·이번 0398)과 모든 나라 정가가 같고 영국·독일은 블프로 빠져 3개 나라뿐 — 20개 한도 안에서 다른 상품을 먼저 ·
    #   버텍스 알파인 GTX는 해외 사이트맵에 없음 · 코펙 2 로우 GTX 여성은 영국·독일 404 · Walk Gently는 협업 한정 컬렉션
    # v1.4 킨 — 품번 = 색상까지 정해진 7자리 · 한국 고도몰은 상품 정보 칸 ARTICLE, 미국·독일·일본 쇼피파이는 변형 품번이 바코드라 상품 태그, 영국은 변형 품번(1022258-10)
    {"id": "keen-newporth2", "cat": "sandal", "brand": "킨(KEEN)", "name": "뉴포트 H2(남성 · 트리플 블랙)", "code": "1022258", "src": "page", "hint": "newport h2",
     "urls": _keen("1000000673", "mens-newport-h2-triple-black")},
    {"id": "keen-newporth2b", "cat": "sandal", "brand": "킨(KEEN)", "name": "뉴포트 H2(남성 · 블랙)", "code": "1001907", "src": "page", "hint": "newport h2",
     "urls": _keen("1000000679", "mens-newport-h2-black")},
    {"id": "keen-uneek", "cat": "sandal", "brand": "킨(KEEN)", "name": "유니크(남성 · 블랙)", "code": "1014097", "src": "page", "hint": "uneek",
     "urls": _keen("1000000653", "mens-uneek-monochrome-black-black", gb="mens-uneek-black-black")},
    {"id": "keen-jasper3", "cat": "shoe", "brand": "킨(KEEN)", "name": "재스퍼 III(남성 · 블랙)", "code": "1032681", "src": "page", "hint": "jasper iii",
     "urls": _keen("1000000996", "mens-jasper-iii-black-black")},
    {"id": "keen-targhee4", "cat": "shoe", "brand": "킨(KEEN)", "name": "타기 IV 워터프루프(남성 · 트리플 블랙)", "code": "1029827", "src": "page", "hint": "targhee iv",
     "urls": _keen("1000000580", "mens-targhee-iv-waterproof-triple-black")},
    {"id": "keen-jasper", "cat": "shoe", "brand": "킨(KEEN)", "name": "재스퍼(남성 · 블랙)", "code": "1026592", "src": "page", "hint": "jasper",
     "urls": _keen("1000000804", "mens-jasper-hairy-black-black", jp=False)},   # 일본 몰에 없음(10/23)
    # v1.13 SKU 4차 — 한국 LF 몰 상품 번호 ↔ 상품 정보 칸 품번(Article No.)을 미국 쇼피파이 상품 태그 품번과 대조(10/28) · 재스퍼 자이오닉 블랙은 한국 품번이 달라(1029584) 뺌
    {"id": "keen-howser3", "cat": "sandal", "brand": "킨(KEEN)", "name": "하우저 III 슬라이드(남성 · 블랙)", "code": "1032618", "src": "page", "hint": "howser",
     "urls": _keen("1000001043", "mens-howser-iii-slide-black-quilted")},
    {"id": "keen-uneektrek", "cat": "shoe", "brand": "킨(KEEN)", "name": "유니크 트레커(남성 · 블랙)", "code": "1032783", "src": "page", "hint": "uneek trekker",
     "urls": _keen("1000000868", "mens-uneek-trekker-black-keen-maple")},
    {"id": "keen-a86", "cat": "shoe", "brand": "킨(KEEN)", "name": "A86(남성 · 트리플 블랙)", "code": "1032844", "src": "page", "hint": "a86",
     "urls": _keen("1000001054", "mens-a86-triple-black")},
    {"id": "keen-jzwp", "cat": "shoe", "brand": "킨(KEEN)", "name": "재스퍼 자이오닉 워터프루프(남성 · 블랙)", "code": "1032795", "src": "page", "hint": "jasper zionic", "urls": {
        "KR": "https://www.keenfootwear.kr/goods/goods_view.php?goodsNo=1000000945",
        "US": "https://www.keenfootwear.com/products/mens-jasper-zionic-waterproof-black-black.json",
        "JP": "https://www.keenfootwear.jp/products/mens-jasper-zionic-waterproof-black-black.json"}},   # 영국·독일 몰에 없음(404, 10/28)
    # SKU 2차(11/21) 킨 — 한국 LF 몰 상품 번호 ↔ 상품 정보 칸 품번(Article No.)을 해외 쇼피파이 상품 태그 품번과 대조 · 블프 검사 = 한국 정가 ÷ (현지 정가 × 환율)이 기존 킨 나라별 가운데값의 1.25배 넘으면 그 나라 뺌
    {"id": "keen-uneekwk", "cat": "sandal", "brand": "킨(KEEN)", "name": "유니크 WK(남성 · 블랙)", "code": "1030271", "src": "page", "hint": "uneek wk",
     "urls": _keen("1000000638", "mens-uneek-wk-black-black", gb="mens-uneek-wk-sneaker-black-black")},   # 영국 몰은 상품 주소가 다름(…-sneaker-…)
    {"id": "keen-wander", "cat": "shoe", "brand": "킨(KEEN)", "name": "원더(남성 · 블랙)", "code": "1033146", "src": "page", "hint": "wander", "urls": {
        "KR": "https://www.keenfootwear.kr/goods/goods_view.php?goodsNo=1000000860",
        "GB": "https://www.keenfootwear.co.uk/products/mens-wander-black-magnet.json",
        "DE": "https://www.keenfootwear.de/en/products/mens-wander-black-magnet.json",
        "JP": "https://www.keenfootwear.jp/products/mens-wander-black-magnet.json"}},   # 미국 140달러는 비율 1.279(가운데값 1.005의 1.27배 · 할인 표시 없음) — 블프 할인가로 보여 뺌, 블프 뒤 차례에(11/21)
    {"id": "keen-roamwp", "cat": "shoe", "brand": "킨(KEEN)", "name": "롬 워터프루프(남성 · 블랙)", "code": "1032758", "src": "page", "hint": "roam waterproof",
     "urls": _keen("1000000890", "mens-roam-waterproof-black-black")},
    {"id": "keen-seek", "cat": "shoe", "brand": "킨(KEEN)", "name": "시크(남성 · 사파리/블랙)", "code": "1032315", "src": "page", "hint": "seek",
     "urls": _keen("1000000588", "mens-seek-safari-black")},
    {"id": "keen-jzionic", "cat": "shoe", "brand": "킨(KEEN)", "name": "재스퍼 자이오닉(남성 · 마그넷/스틸 그레이)", "code": "1032646", "src": "page", "hint": "jasper zionic",
     "urls": _keen("1000000952", "mens-jasper-zionic-magnet-steel-grey")},   # 워터프루프(keen-jzwp)와 다른 모델 · 블랙(1029584)은 한국 품번이 달라 이 색으로
    {"id": "keen-jnylonwp", "cat": "shoe", "brand": "킨(KEEN)", "name": "재스퍼 나일론 워터프루프(남성 · 블랙)", "code": "1032707", "src": "page", "hint": "jasper nylon waterproof",
     "urls": _keen("1000000986", "mens-jasper-nylon-waterproof-black-black")},
    {"id": "keen-howser2", "cat": "sandal", "brand": "킨(KEEN)", "name": "하우저 II(남성 · 트리플 블랙)", "code": "1023997", "src": "page", "hint": "howser ii",
     "urls": _keen("1000001045", "mens-howser-ii-triple-black")},
    {"id": "keen-targhee4ox", "cat": "shoe", "brand": "킨(KEEN)", "name": "타기 IV 옥스포드(남성 · 블랙)", "code": "1031647", "src": "page", "hint": "targhee iv oxford",
     "urls": _keen("1000000585", "mens-targhee-iv-oxford-black")},   # 한국 몰 할인 중(판매가 159,200) — 정가 칸 199,000으로 읽힘(11/21)
    {"id": "keen-uneeklea", "cat": "sandal", "brand": "킨(KEEN)", "name": "유니크 레더(남녀공용 · 블랙)", "code": "1032097", "src": "page", "hint": "uneek leather", "urls": {
        "KR": "https://www.keenfootwear.kr/goods/goods_view.php?goodsNo=1000000073",
        "US": "https://www.keenfootwear.com/products/all-gender-uneek-lea-perseid-black.json",
        "JP": "https://www.keenfootwear.jp/products/all-gender-uneek-lea-perseid-black.json"}},   # 영국 몰에 없음 · 독일 125유로는 비율 1.307(가운데값 1.019의 1.28배 · 할인 표시 없음) — 블프 할인가로 보여 뺌(11/21)
    {"id": "keen-jmerko", "cat": "shoe", "brand": "킨(KEEN)", "name": "재스퍼 멀코(남성 · 블랙)", "code": "1032554", "src": "page", "hint": "jasper merko", "urls": {
        "KR": "https://www.keenfootwear.kr/goods/goods_view.php?goodsNo=1000000991",
        "US": "https://www.keenfootwear.com/products/mens-jasper-merko-black-black.json",
        "DE": "https://www.keenfootwear.de/en/products/mens-jasper-merko-black-black.json",
        "JP": "https://www.keenfootwear.jp/products/mens-jasper-merko-black-black.json"}},   # 영국 몰에 없음(11/21)
    # 예비 재스퍼 록스 SP(1032958)·KS86(1032651)·샨티(1026263)·타기 IV 슬립온(1031164)도 정가 읽기 OK였으나 브랜드당 20개라 넣지 않음 · ASPIRE·TTS ZIP은 미국 몰에만 있어 뺌(11/21)
    # v1.4 우포스 — 품번 = 모델 4자리 + 색상(한국 Article No. '1100 Black' · 미국 변형 품번 앞머리 '1100BLK…') · 한국 콜라보 상품(같은 Article No.)은 다른 상품 번호
    {"id": "oofos-ooriginal", "cat": "sandal", "brand": "우포스", "name": "OOriginal 샌들(블랙)", "code": "1000", "cc_code": {"KR": "1000 Black", "US": "1000BLK"}, "src": "page", "hint": "ooriginal",
     "urls": _oofos("1000000050", "mens-original-sandal-black")},
    {"id": "oofos-ooahh", "cat": "sandal", "brand": "우포스", "name": "OOahh 슬라이드(블랙)", "code": "1100", "cc_code": {"KR": "1100 Black", "US": "1100BLK"}, "src": "page", "hint": "ooahh",
     "urls": _oofos("1000000084", "mens-sandal-ooahh-slide-black")},
    {"id": "oofos-oocloog", "cat": "sandal", "brand": "우포스", "name": "OOcloog 클로그(블랙)", "code": "1200", "cc_code": {"KR": "1200 Black", "US": "1200BLK"}, "src": "page", "hint": "oocloog",
     "urls": _oofos("1000000159", "mens-oocloog-clog-black")},
    {"id": "oofos-ooriginalplus", "cat": "sandal", "brand": "우포스", "name": "OOriginal+ 샌들(블랙)", "code": "2000", "cc_code": {"KR": "2000 Black", "US": "2000BLACK"}, "src": "page", "hint": "ooriginal",
     "urls": _oofos("1000000062", "mens-ooriginal-plus-sandal-black")},
    {"id": "oofos-ooahhplus", "cat": "sandal", "brand": "우포스", "name": "OOahh+ 슬라이드(블랙)", "code": "2200", "cc_code": {"KR": "2200 Black", "US": "2200BLACK"}, "src": "page", "hint": "ooahh",
     "urls": _oofos("1000000058", "mens-ooahh-plus-slide-sandal-black")},
    {"id": "oofos-ooriginalsport", "cat": "sandal", "brand": "우포스", "name": "OOriginal Sport 샌들(그라파이트)", "code": "1001", "cc_code": {"KR": "1001 Graphite", "US": "1001GRPH"}, "src": "page", "hint": "ooriginal sport",
     "urls": _oofos("1000000087", "mens-sandal-ooriginal-sport-graphite")},
    {"id": "oofos-sportflex", "cat": "sandal", "brand": "우포스", "name": "OOahh Sport Flex 슬라이드(매트 블랙)", "code": "1550", "cc_code": {"KR": "1550 Black Matte", "US": "1550MATBLK"}, "src": "page", "hint": "sport flex",
     "urls": _oofos("1000000031", "mens-ooahh-sport-flex-black-matte")},
    # v1.16 SKU 7차 — 한국 상품 번호 ↔ Article No. 확인(11/03): 1000000140 = 2400 Chalk · 17·15 = 5087 White Black·White(다른 색이라 안 씀)
    {"id": "oofos-oocloogplus", "cat": "sandal", "brand": "우포스", "name": "OOcloog+ 클로그(블랙)", "code": "2400", "cc_code": {"KR": "2400 Black", "US": "2400BLACK"}, "src": "page", "hint": "oocloog",
     "urls": _oofos("1000000055", "mens-oocloog-plus-clog-black")},
    {"id": "oofos-oomystride", "cat": "shoe", "brand": "우포스", "name": "OOmy Stride 운동화(블랙)", "code": "5087", "cc_code": {"KR": "5087 Black", "US": "5087BLACK"}, "src": "page", "hint": "oomy stride",
     "urls": _oofos("1000000018", "mens-oomy-stride-black")},
    {"id": "oofos-ooahhsport", "cat": "sandal", "brand": "우포스", "name": "OOahh Sport 슬라이드(택티컬 그린)", "code": "1500", "cc_code": {"KR": "1500 Tactical Green", "US": "1500TACGRN"}, "src": "page", "hint": "ooahh sport",
     "urls": _oofos("1000000063", "mens-ooahh-sport-slide-sandal-tactical-green")},   # 블랙은 한국 1500 Black Matrix(64) ↔ 미국 FootJoy 콜라보뿐이라 두 몰 모두 있는 택티컬 그린
    # 20개 2차(11/21) — 한국 LF 몰 Article No.(cc_code KR) ∩ 미국 쇼피파이 변형 품번 앞머리(cc_code US) · 11/21 GitHub 서버 정가 읽기 확인(11개 모두 OK) ·
    #   블프 검사 = 한국 정가 ÷ (미국 정가 × 11/20 환율 1,334.79원)이 기존 10개 가운데값 0.972의 1.25배(1.215) 안 — 새 10개 0.85~1.12 · 미국 할인 중(−20%)인 상품은 정가 = compare_at_price
    {"id": "oofos-ooyea", "cat": "sandal", "brand": "우포스", "name": "OOyea 슬라이드(블랙)", "code": "1700", "cc_code": {"KR": "1700 Black", "US": "1700BLACK"}, "src": "page", "hint": "ooyea",
     "urls": _oofos("1000000054", "womens-ooyea-slide-sandal-black")},
    {"id": "oofos-oocoozie", "cat": "sandal", "brand": "우포스", "name": "OOcoozie Thermo 뮬(남성 · 블랙)", "code": "5286", "cc_code": {"KR": "5286 Black", "US": "5286BLACK"}, "src": "page", "hint": "oocoozie",
     "urls": _oofos("1000000148", "mens-oocoozie-thermo-mule-black")},   # 11/21 미국 할인 중($119.95 → $95.96)
    {"id": "oofos-roamthermo", "cat": "shoe", "brand": "우포스", "name": "Roam Thermo 방한화(남성 · 블랙)", "code": "5388", "cc_code": {"KR": "5388 Black", "US": "5388BLACK"}, "src": "page", "hint": "roam thermo",
     "urls": _oofos("1000000145", "mens-roam-thermo-black")},   # 미국 상품 분류 Shoe · 11/21 미국 할인 중($139.95 → $111.96)
    {"id": "oofos-roamthermow", "cat": "shoe", "brand": "우포스", "name": "Roam Thermo 방한화(여성 · 블랙)", "code": "5378", "cc_code": {"KR": "5378 Black", "US": "5378BLACK"}, "src": "page", "hint": "roam thermo",
     "urls": _oofos("1000000149", "womens-roam-thermo-black")},   # 여성은 모델 번호가 다름(남성 5388) · 11/21 미국 할인 중($139.95 → $111.96)
    {"id": "oofos-posh", "cat": "sandal", "brand": "우포스", "name": "OOmega Posh 뮬(여성 · 블랙)", "code": "5374", "cc_code": {"KR": "5374 Black", "US": "5374BLACK"}, "src": "page", "hint": "posh",
     "urls": _oofos("1000000153", "womens-oomega-posh-mule-black")},   # 11/21 미국 할인 중($139.95 → $111.96)
    {"id": "oofos-sherpa", "cat": "sandal", "brand": "우포스", "name": "OOcoozie Sherpa 뮬(여성 · 블랙)", "code": "5277", "cc_code": {"KR": "5277 Black", "US": "5277BLACK"}, "src": "page", "hint": "sherpa",
     "urls": _oofos("1000000151", "womens-oocoozie-sherpa-mule-black")},
    {"id": "oofos-oocloogluxe", "cat": "sandal", "brand": "우포스", "name": "OOcloog Luxe 스택 클로그(포토벨로)", "code": "1201", "cc_code": {"KR": "1201 Stacked Portobello", "US": "1201NOMPOR"}, "src": "page", "hint": "oocloog",
     "urls": _oofos("1000000075", "mens-oocloog-stacked-clog-portobello")},   # 한국 남녀공용 · 미국 Stacked Clog(남성·여성 주소 같은 품번 1201NOMPORM) · 11/21 미국 할인 중($84.95 → $67.96)
    {"id": "oofos-oolala", "cat": "sandal", "brand": "우포스", "name": "OOlala 샌들(블랙)", "code": "1400", "cc_code": {"KR": "1400 Black", "US": "1400BLK"}, "src": "page", "hint": "oolala",
     "urls": _oofos("1000000073", "womens-sandal-oolala-black")},   # 한국 몰에 같은 Article No. 상품이 둘(073·037 — 같은 이름·정가) — 상품 번호로 고름
    {"id": "oofos-oomegaoolala", "cat": "sandal", "brand": "우포스", "name": "OOmega OOlala 샌들(블랙)", "code": "1410", "cc_code": {"KR": "1410 Black", "US": "1410BLACK"}, "src": "page", "hint": "oomega",
     "urls": _oofos("1000000067", "womens-oomega-oolala-sandal-black")},   # 한국 몰에 같은 Article No. 상품이 둘(067·035) — 상품 번호로 고름 · 11/21 미국 할인 중($89.95 → $71.96)
    {"id": "oofos-oomystridew", "cat": "shoe", "brand": "우포스", "name": "OOmy Stride 운동화(여성 · 블랙)", "code": "5077", "cc_code": {"KR": "5077 Black", "US": "5077BLACK"}, "src": "page", "hint": "oomy stride",
     "urls": _oofos("1000000027", "womens-oomy-stride-black")},   # 여성은 모델 번호가 다름(남성 5087) · 11/21 미국 할인 중($119.95 → $95.96)
    # 뺌(11/21): OOcoozie Thermo 뮬 여성(5276 Black · 한국 1000000154 · 정가 읽기 OK 159,000원 · $119.95) — 남성(5286)과 같은 모델·같은 정가라 하나만(브랜드 20개 한도)
    # 톰브라운(SKU 2차 11/21 · 판정 브랜드 첫 해외 정가): 본사 쇼피파이 몰 하나(www.thombrowne.com) · 나라별 하위 폴더 — 한국 /ko-kr(원화) · 미국 맨 위(달러) · 영국 /en-gb ·
    # 독일 = /en-eu(EU 공통 유로 가격 — 독일 전용 몰 없음) · 일본 /ja-jp · 두바이 /en-ae · 멕시코 없음 · 같은 상품은 나라별 handle이 같고 handle 끝에 품번 · robots.txt Allow: / (상품 .json 막지 않음)
    {"id": "tb-cardigan-m", "cat": "wear", "brand": "톰브라운", "name": "메리노 4-바 밀라노 스티치 카디건(남성·네이비)", "code": "MKC160A-00014-415", "src": "page", "hint": "mkc160a", "urls": {
        "KR": "https://www.thombrowne.com/ko-kr/products/merino-wool-4-bar-milano-stitch-cardigan-mkc160a-00014-415.json",
        "US": "https://www.thombrowne.com/products/merino-wool-4-bar-milano-stitch-cardigan-mkc160a-00014-415.json",
        "GB": "https://www.thombrowne.com/en-gb/products/merino-wool-4-bar-milano-stitch-cardigan-mkc160a-00014-415.json",
        "DE": "https://www.thombrowne.com/en-eu/products/merino-wool-4-bar-milano-stitch-cardigan-mkc160a-00014-415.json",
        "JP": "https://www.thombrowne.com/ja-jp/products/merino-wool-4-bar-milano-stitch-cardigan-mkc160a-00014-415.json",
        "AE": "https://www.thombrowne.com/en-ae/products/merino-wool-4-bar-milano-stitch-cardigan-mkc160a-00014-415.json"}},
    {"id": "tb-cardigan-w", "cat": "wear", "brand": "톰브라운", "name": "울 4-바 브이넥 카디건(여성·네이비)", "code": "FKC207A-00014-415", "src": "page", "hint": "fkc207a", "urls": {
        "KR": "https://www.thombrowne.com/ko-kr/products/wool-4-bar-v-neck-cardigan-fkc207a-00014-415.json",
        "US": "https://www.thombrowne.com/products/wool-4-bar-v-neck-cardigan-fkc207a-00014-415.json",
        "GB": "https://www.thombrowne.com/en-gb/products/wool-4-bar-v-neck-cardigan-fkc207a-00014-415.json",
        "DE": "https://www.thombrowne.com/en-eu/products/wool-4-bar-v-neck-cardigan-fkc207a-00014-415.json",
        "JP": "https://www.thombrowne.com/ja-jp/products/wool-4-bar-v-neck-cardigan-fkc207a-00014-415.json",
        "AE": "https://www.thombrowne.com/en-ae/products/wool-4-bar-v-neck-cardigan-fkc207a-00014-415.json"}},
    {"id": "tb-pullover-w", "cat": "wear", "brand": "톰브라운", "name": "밀라노 스티치 메리노 4-바 풀오버(여성·네이비)", "code": "FKA239A-00014-415", "src": "page", "hint": "fka239a", "urls": {
        "KR": "https://www.thombrowne.com/ko-kr/products/milano-stitch-merino-wool-4-bar-pullover-fka239a-00014-415.json",
        "US": "https://www.thombrowne.com/products/milano-stitch-merino-wool-4-bar-pullover-fka239a-00014-415.json",
        "GB": "https://www.thombrowne.com/en-gb/products/milano-stitch-merino-wool-4-bar-pullover-fka239a-00014-415.json",
        "DE": "https://www.thombrowne.com/en-eu/products/milano-stitch-merino-wool-4-bar-pullover-fka239a-00014-415.json",
        "JP": "https://www.thombrowne.com/ja-jp/products/milano-stitch-merino-wool-4-bar-pullover-fka239a-00014-415.json",
        "AE": "https://www.thombrowne.com/en-ae/products/milano-stitch-merino-wool-4-bar-pullover-fka239a-00014-415.json"}},
    {"id": "tb-vcardigan-m", "cat": "wear", "brand": "톰브라운", "name": "메리노 4-바 클래식 브이넥 카디건(남성·네이비)", "code": "MKC002A-Y1014-415", "src": "page", "hint": "mkc002a", "urls": {
        "KR": "https://www.thombrowne.com/ko-kr/products/merino-wool-4-bar-classic-v-neck-cardigan-mkc002a-y1014-415.json",
        "US": "https://www.thombrowne.com/products/merino-wool-4-bar-classic-v-neck-cardigan-mkc002a-y1014-415.json",
        "GB": "https://www.thombrowne.com/en-gb/products/merino-wool-4-bar-classic-v-neck-cardigan-mkc002a-y1014-415.json",
        "DE": "https://www.thombrowne.com/en-eu/products/merino-wool-4-bar-classic-v-neck-cardigan-mkc002a-y1014-415.json",
        "JP": "https://www.thombrowne.com/ja-jp/products/merino-wool-4-bar-classic-v-neck-cardigan-mkc002a-y1014-415.json",
        "AE": "https://www.thombrowne.com/en-ae/products/merino-wool-4-bar-classic-v-neck-cardigan-mkc002a-y1014-415.json"}},
    {"id": "tb-pullover-m", "cat": "wear", "brand": "톰브라운", "name": "파인 메리노 4-바 풀오버(남성·네이비)", "code": "MKA002A-Y1014-415", "src": "page", "hint": "mka002a", "urls": {
        "KR": "https://www.thombrowne.com/ko-kr/products/fine-merino-wool-4-bar-pullover-mka002a-y1014-415.json",
        "US": "https://www.thombrowne.com/products/fine-merino-wool-4-bar-pullover-mka002a-y1014-415.json",
        "GB": "https://www.thombrowne.com/en-gb/products/fine-merino-wool-4-bar-pullover-mka002a-y1014-415.json",
        "DE": "https://www.thombrowne.com/en-eu/products/fine-merino-wool-4-bar-pullover-mka002a-y1014-415.json",
        "JP": "https://www.thombrowne.com/ja-jp/products/fine-merino-wool-4-bar-pullover-mka002a-y1014-415.json",
        "AE": "https://www.thombrowne.com/en-ae/products/fine-merino-wool-4-bar-pullover-mka002a-y1014-415.json"}},
    {"id": "tb-woolpullover-m", "cat": "wear", "brand": "톰브라운", "name": "울 4-바 풀오버(남성·네이비)", "code": "MKA189A-00014-415", "src": "page", "hint": "mka189a", "urls": {
        "KR": "https://www.thombrowne.com/ko-kr/products/wool-4-bar-pullover-mka189a-00014-415.json",
        "US": "https://www.thombrowne.com/products/wool-4-bar-pullover-mka189a-00014-415.json",
        "GB": "https://www.thombrowne.com/en-gb/products/wool-4-bar-pullover-mka189a-00014-415.json",
        "DE": "https://www.thombrowne.com/en-eu/products/wool-4-bar-pullover-mka189a-00014-415.json",
        "JP": "https://www.thombrowne.com/ja-jp/products/wool-4-bar-pullover-mka189a-00014-415.json",
        "AE": "https://www.thombrowne.com/en-ae/products/wool-4-bar-pullover-mka189a-00014-415.json"}},
    {"id": "tb-sweatpants-m", "cat": "wear", "brand": "톰브라운", "name": "와플 4-바 스웨트팬츠(남성·그레이)", "code": "MJQ082A-06452-035", "src": "page", "hint": "mjq082a", "urls": {
        "KR": "https://www.thombrowne.com/ko-kr/products/waffle-4-bar-sweatpants-mjq082a-06452-035.json",
        "US": "https://www.thombrowne.com/products/waffle-4-bar-sweatpants-mjq082a-06452-035.json",
        "GB": "https://www.thombrowne.com/en-gb/products/waffle-4-bar-sweatpants-mjq082a-06452-035.json",
        "DE": "https://www.thombrowne.com/en-eu/products/waffle-4-bar-sweatpants-mjq082a-06452-035.json",
        "JP": "https://www.thombrowne.com/ja-jp/products/waffle-4-bar-sweatpants-mjq082a-06452-035.json",
        "AE": "https://www.thombrowne.com/en-ae/products/waffle-4-bar-sweatpants-mjq082a-06452-035.json"}},
    {"id": "tb-oxford-m", "cat": "wear", "brand": "톰브라운", "name": "옥스퍼드 클래식 셔츠(남성·화이트)", "code": "MWL001A-F0313-100", "src": "page", "hint": "mwl001a", "urls": {
        "KR": "https://www.thombrowne.com/ko-kr/products/oxford-shirt-mwl001a-f0313-100.json",
        "US": "https://www.thombrowne.com/products/oxford-shirt-mwl001a-f0313-100.json",
        "GB": "https://www.thombrowne.com/en-gb/products/oxford-shirt-mwl001a-f0313-100.json",
        "DE": "https://www.thombrowne.com/en-eu/products/oxford-shirt-mwl001a-f0313-100.json",
        "JP": "https://www.thombrowne.com/ja-jp/products/oxford-shirt-mwl001a-f0313-100.json",
        "AE": "https://www.thombrowne.com/en-ae/products/oxford-shirt-mwl001a-f0313-100.json"}},
    {"id": "tb-longwing-m", "cat": "shoe", "brand": "톰브라운", "name": "페블 그레인 롱윙 브로그 러버솔(남성·블랙)", "code": "MFD002H-00198-001", "src": "page", "hint": "mfd002h", "urls": {
        "KR": "https://www.thombrowne.com/ko-kr/products/pebble-grain-leather-longwing-brogues-with-rubber-soles-mfd002h-00198-001.json",
        "US": "https://www.thombrowne.com/products/pebble-grain-leather-longwing-brogues-with-rubber-soles-mfd002h-00198-001.json",
        "GB": "https://www.thombrowne.com/en-gb/products/pebble-grain-leather-longwing-brogues-with-rubber-soles-mfd002h-00198-001.json",
        "DE": "https://www.thombrowne.com/en-eu/products/pebble-grain-leather-longwing-brogues-with-rubber-soles-mfd002h-00198-001.json",
        "JP": "https://www.thombrowne.com/ja-jp/products/pebble-grain-leather-longwing-brogues-with-rubber-soles-mfd002h-00198-001.json",
        "AE": "https://www.thombrowne.com/en-ae/products/pebble-grain-leather-longwing-brogues-with-rubber-soles-mfd002h-00198-001.json"}},
    {"id": "tb-penny-m", "cat": "shoe", "brand": "톰브라운", "name": "페블 그레인 페니 로퍼 러버솔(남성·블랙)", "code": "MFD054G-00198-001", "src": "page", "hint": "mfd054g", "urls": {
        "KR": "https://www.thombrowne.com/ko-kr/products/pebble-grain-leather-penny-loafers-with-rubber-soles-mfd054g-00198-001.json",
        "US": "https://www.thombrowne.com/products/pebble-grain-leather-penny-loafers-with-rubber-soles-mfd054g-00198-001.json",
        "GB": "https://www.thombrowne.com/en-gb/products/pebble-grain-leather-penny-loafers-with-rubber-soles-mfd054g-00198-001.json",
        "DE": "https://www.thombrowne.com/en-eu/products/pebble-grain-leather-penny-loafers-with-rubber-soles-mfd054g-00198-001.json",
        "JP": "https://www.thombrowne.com/ja-jp/products/pebble-grain-leather-penny-loafers-with-rubber-soles-mfd054g-00198-001.json",
        "AE": "https://www.thombrowne.com/en-ae/products/pebble-grain-leather-penny-loafers-with-rubber-soles-mfd054g-00198-001.json"}},
    {"id": "tb-hector-m", "cat": "bag", "brand": "톰브라운", "name": "헥터 백 페블 그레인(블랙)", "code": "MAG050A-00198-001", "src": "page", "hint": "mag050a", "urls": {
        "KR": "https://www.thombrowne.com/ko-kr/products/hector-bag-in-pebble-grain-leather-mag050a-00198-001.json",
        "US": "https://www.thombrowne.com/products/hector-bag-in-pebble-grain-leather-mag050a-00198-001.json",
        "GB": "https://www.thombrowne.com/en-gb/products/hector-bag-in-pebble-grain-leather-mag050a-00198-001.json",
        "DE": "https://www.thombrowne.com/en-eu/products/hector-bag-in-pebble-grain-leather-mag050a-00198-001.json",
        "JP": "https://www.thombrowne.com/ja-jp/products/hector-bag-in-pebble-grain-leather-mag050a-00198-001.json",
        "AE": "https://www.thombrowne.com/en-ae/products/hector-bag-in-pebble-grain-leather-mag050a-00198-001.json"}},
    {"id": "tb-mrthom-m", "cat": "bag", "brand": "톰브라운", "name": "미스터 톰 백 페블 그레인(블랙)", "code": "MAG001L-00198-001", "src": "page", "hint": "mag001l", "urls": {
        "KR": "https://www.thombrowne.com/ko-kr/products/pebble-grain-mr-thom-bag-mag001l-00198-001.json",
        "US": "https://www.thombrowne.com/products/pebble-grain-mr-thom-bag-mag001l-00198-001.json",
        "GB": "https://www.thombrowne.com/en-gb/products/pebble-grain-mr-thom-bag-mag001l-00198-001.json",
        "DE": "https://www.thombrowne.com/en-eu/products/pebble-grain-mr-thom-bag-mag001l-00198-001.json",
        "JP": "https://www.thombrowne.com/ja-jp/products/pebble-grain-mr-thom-bag-mag001l-00198-001.json",
        "AE": "https://www.thombrowne.com/en-ae/products/pebble-grain-mr-thom-bag-mag001l-00198-001.json"}},
    # 버버리(SKU 2차 11/21 · 판정 브랜드 첫 해외 정가): 나라별 공식몰 kr·us·uk.burberry.com · robots.txt가 상품 페이지 허용 · JSON-LD Product sku = 주소 끝 p 뒤 8자리(세 나라 같음) ·
    # 독일·일본·멕시코·두바이는 이번에 시험 안 함(다음 차례) · 체크 울 캐시미어 스카프(81307581)는 세 나라 모두 JSON-LD 가격 없음이라 뺌
    {"id": "bbr-kensington-mid", "cat": "wear", "brand": "버버리", "name": "미드 렝스 개버딘 켄싱턴 트렌치코트", "code": "81332441", "src": "page", "hint": "", "urls": {
        "KR": "https://kr.burberry.com/mid-length-gabardine-kensington-trench-coat-p81332441",
        "US": "https://us.burberry.com/mid-length-gabardine-kensington-trench-coat-p81332441",
        "GB": "https://uk.burberry.com/mid-length-gabardine-kensington-trench-coat-p81332441"}},
    {"id": "bbr-kensington-long", "cat": "wear", "brand": "버버리", "name": "롱 캐시미어 켄싱턴 트렌치코트", "code": "81361201", "src": "page", "hint": "", "urls": {
        "KR": "https://kr.burberry.com/long-cashmere-kensington-trench-coat-p81361201",
        "US": "https://us.burberry.com/long-cashmere-kensington-trench-coat-p81361201",
        "GB": "https://uk.burberry.com/long-cashmere-kensington-trench-coat-p81361201"}},
    {"id": "bbr-lakefield-long", "cat": "wear", "brand": "버버리", "name": "롱 개버딘 레이크필드 트렌치코트", "code": "81354831", "src": "page", "hint": "", "urls": {
        "KR": "https://kr.burberry.com/long-gabardine-lakefield-trench-coat-p81354831",
        "US": "https://us.burberry.com/long-gabardine-lakefield-trench-coat-p81354831",
        "GB": "https://uk.burberry.com/long-gabardine-lakefield-trench-coat-p81354831"}},
    {"id": "bbr-checkscarf", "cat": "wear", "brand": "버버리", "name": "체크 캐시미어 스카프", "code": "81250011", "src": "page", "hint": "", "urls": {
        "KR": "https://kr.burberry.com/check-cashmere-scarf-p81250011",
        "US": "https://us.burberry.com/check-cashmere-scarf-p81250011",
        "GB": "https://uk.burberry.com/check-cashmere-scarf-p81250011"}},
]
# v1.23 분류 cat(화면 착지 무게·관세 — build_dashboard LAND.cat과 같은 이름) — 새 상품은 반드시 넣음(빠지면 불러오기에서 멈춤 → check-files 실패)
CATS = ("shoe", "boot", "sandal", "top", "wear", "bag")   # 신발 · 부츠 · 샌들류(샌들·슬리퍼·클로그 · 킨 유니크 포함) · 반팔·민소매 · 옷(후디·집업·바지·재킷) · 가방
_badcat = [p["id"] for p in PRODUCTS if p.get("cat") not in CATS]
assert not _badcat, f"PRODUCTS 분류(cat) 없음·모름: {_badcat}"


def log(msg):
    """v1.12 묶음(스레드)이 값을 받는 중이면 그 값의 줄로 모았다가 값이 끝날 때 한꺼번에 출력(묶음끼리 줄이 섞이지 않게)"""
    c = _ctx()
    if c.buf is not None:
        c.buf.append(msg)
    else:
        _out([msg])


def _out(lines):
    if lines:
        with _PRINT:
            sys.stdout.write("".join(f"{x}\n" for x in lines)); sys.stdout.flush()


def soft_fail(msg):
    """심각한 실패 표시 — 저장은 하되 워크플로우 마지막 단계가 빨간 X로 끝내 점검 알림이 가게 함"""
    print(f"실패 표시: {msg}", flush=True)
    with open("soft_fail.txt", "a", encoding="utf-8") as f:
        f.write(f"{SCRIPT}: {msg}\n")


class Skip(Exception):
    """이 나라에서는 팔지 않음·주소 없음(실패로 세지 않음)"""


class Defer(Exception):
    """v1.8 이 사이트의 한 실행 요청 한도(HOST_CAP)를 다 씀 — 다음 실행에서 받음(실패로 세지 않음)"""


_ROB, _BLOCKED, _HLAST, _DOWN, _HCOUNT = {}, set(), {}, {}, {}   # 사이트별 — v1.12 그 사이트 자물쇠(_HLOCK) 안에서만 읽고 씀
_PACE, _GLAST, _GBLOCKED = {}, {}, set()   # v1.12 사이트 → 플랫폼 묶음(쇼피파이·카페24·고도몰) · 플랫폼별 마지막 요청 시각 · 430으로 막힌 플랫폼
_HLOCK, _GLOCK = {}, {}           # v1.12 사이트별·플랫폼별 자물쇠(한 번에 한 요청) — 자물쇠 순서는 늘 사이트 → 플랫폼
_GUARD, _PRINT = threading.Lock(), threading.Lock()
_STOP = threading.Event()         # v1.12 묶음 시간 초과 — 남은 묶음은 더 요청하지 않음
_TL = threading.local()


class _Ctx:
    """v1.12 묶음 하나의 요청 상태 — 마지막 요청 시각(묶음 안 GAP) · 세션(넘겨짐 사이 쿠키) · 값 하나의 로그 줄"""
    def __init__(self):
        self.last, self.sess, self.buf = 0.0, requests.Session(), None


_MAIN = _Ctx()   # 차례대로 받을 때(PRICE_LANES=1 — 예전처럼 모든 요청이 한 줄로 GAP)·스레드 밖


def _ctx():
    return getattr(_TL, "c", None) or _MAIN


def _lock(d, k):
    with _GUARD:
        return d.setdefault(k, threading.Lock())
# robots.txt를 두지 않는 API 주소 → 같은 회사 대표 사이트 robots.txt를 따름(그 사이트 robots.txt도 못 받으면 건너뜀)
# api.nike.com: 상품 정보 경로 밖 모든 주소(/, robots.txt, 없는 주소)에 Akamai가 '503 DNS failure' — 2026-10-21 브랜치 시험에서 확인
ROBOTS_ALT = {"api.nike.com": "https://www.nike.com"}


def _robots_rules(txt):
    """robots.txt → 우리에게 맞는 규칙 [(허용?, 정규식, 길이)] — RFC 9309: 우리 이름 그룹이 있으면 그것만, 없으면 *"""
    groups, g, rule_seen = [], None, True
    for line in txt.splitlines():
        line = line.split("#", 1)[0].strip()
        if ":" not in line: continue
        k, v = (x.strip() for x in line.split(":", 1)); k = k.lower()
        if k == "user-agent":
            if rule_seen: g = {"ua": set(), "rules": []}; groups.append(g); rule_seen = False
            g["ua"].add(v.lower())
        elif k in ("allow", "disallow") and g is not None:
            rule_seen = True
            if v:   # %2A·%24는 글자 그대로(와일드카드·끝 표시가 아님)
                lit = re.sub(r"%2[aA]", "\x00", re.sub(r"%24", "\x01", v))
                rx = re.escape(urllib.parse.unquote(lit)).replace(r"\*", ".*")
                if rx.endswith(r"\$"): rx = rx[:-2] + "$"
                rx = rx.replace("\x00", r"\*").replace("\x01", r"\$")
                g["rules"].append((k == "allow", re.compile(rx), len(v)))
    mine = [gg for gg in groups if BOT in gg["ua"]] or [gg for gg in groups if "*" in gg["ua"]]
    return [r for gg in mine for r in gg["rules"]]


def _robots_get(base):
    """규칙 목록, 또는 못 받은 이유(글) — 4xx면 규칙 없음, 429·5xx·연결 안 됨이면 이유(RFC 9309: 그 사이트 전체를 막힌 것으로)"""
    try:
        r = requests.get(base + "/robots.txt", headers=HDR, timeout=20)
        if r.status_code == 429 or r.status_code >= 500:
            return f"robots.txt HTTP {r.status_code}"
        if r.status_code != 200:
            return []
        raw = getattr(r, "content", None)
        return _robots_rules(raw.decode("utf-8", "replace") if isinstance(raw, bytes) else r.text)   # 글자 집합 표시가 없어도 UTF-8
    except requests.RequestException as e:
        return f"robots.txt 못 받음({type(e).__name__})"


def robots_ok(url):
    """(허용?, 이유) — 사이트별 robots.txt는 실행마다 1번만 받음"""
    p = urllib.parse.urlsplit(url); base = f"{p.scheme}://{p.netloc}"
    if base not in _ROB:
        _ROB[base] = _robots_get(base)
        alt = ROBOTS_ALT.get(p.netloc)
        if isinstance(_ROB[base], str) and alt:
            got = _robots_get(alt)
            if not isinstance(got, str):
                log(f"  {p.netloc}: {_ROB[base]} — robots.txt를 두지 않는 API 주소라 {urllib.parse.urlsplit(alt).netloc} robots.txt를 따름")
                _ROB[base] = got
    rules = _ROB[base]
    if isinstance(rules, str):
        return False, f"{rules} — 이 사이트 건너뜀"
    path = urllib.parse.unquote(p.path or "/") + ("?" + urllib.parse.unquote(p.query) if p.query else "")
    hit = [(n, a) for a, rx, n in rules if rx.match(path)]
    return (True, "") if not hit or max(hit)[1] else (False, "robots.txt가 막음")


_S = _MAIN.sess   # 넘겨짐 사이 쿠키를 이어 주려고(예전 allow_redirects=True와 같게) · v1.12 묶음마다 세션(_Ctx.sess)


CHALLENGE = re.compile(r"(?is)<title[^>]*>\s*(?:Client Challenge|Just a moment\.\.\.|Attention Required|Access Denied|Pardon Our Interruption)\s*</title>"
                       r"|/_fs-ch-|challenges\.cloudflare\.com|captcha-delivery\.com|px-captcha")


def _challenge(r):
    """v1.22 응답이 봇 확인 화면인지 — HTML이고 작으며(30KB 밑) 확인 화면 제목·표식이 있을 때만(큰 상품 페이지 본문의 낱말에 걸리지 않게)"""
    h = getattr(r, "headers", None) or {}
    body = getattr(r, "content", None)
    ct = (h.get("Content-Type") or "").lower()
    if (ct and "html" not in ct) or body is None or len(body) > 30000:
        return False
    return bool(CHALLENGE.search(getattr(r, "text", "") or ""))


def get(url, hops=5):
    """주소 → 응답. 넘겨짐(3xx)은 직접 따라가며 매번 막힘·robots.txt를 먼저 확인(막힌 주소는 요청하지 않음).
    v1.12 그 사이트 자물쇠 안에서 확인·기다림·요청(같은 사이트는 묶음과 상관없이 한 번에 한 요청) — 기다림 = 묶음 안 GAP과
    같은 사이트 GAP(살로몬 해외 HOST_GAP) 중 긴 것, 플랫폼(PACE)이면 플랫폼 자물쇠 안에서 플랫폼 GAP도(그 몰의 robots.txt도 ·
    플랫폼 몰이 다른 이름 사이트로 넘기면 그 사이트도 같은 플랫폼으로). 넘겨짐은 자물쇠를 풀고 따라감 · 멈춤(_STOP)은 요청 바로 전에도 확인"""
    c, moved, g0 = _ctx(), False, None
    for _ in range(hops + 1):
        p = urllib.parse.urlsplit(url); host = p.netloc
        pre = "넘겨진 주소: " if moved else ""
        g = _PACE.get(host) or g0
        with _lock(_HLOCK, host):
            if _STOP.is_set():
                raise RuntimeError(pre + "묶음을 멈춤(시간 초과·다른 묶음 오류) — 더 요청 안 함")
            if host in _BLOCKED:
                raise RuntimeError(pre + "이번 실행에서 이 사이트가 막음 — 더 요청 안 함")
            if g in _GBLOCKED:
                raise RuntimeError(pre + f"이번 실행에서 이 플랫폼({g})이 막음(430) — 더 요청 안 함")
            if _DOWN.get(host, 0) >= 2:
                raise RuntimeError(pre + "이번 실행에서 이 사이트가 연달아 응답 없음 — 더 요청 안 함")
            if g and f"{p.scheme}://{host}" not in _ROB:   # 플랫폼 몰의 robots.txt도 플랫폼 줄에 맞춰(앞 요청이 끝나고 GAP 뒤)
                with _lock(_GLOCK, g):
                    w = GAP - (time.time() - _GLAST.get(g, 0.0))
                    if w > 0: time.sleep(w)
                    _GLAST[g] = time.time()
                    robots_ok(url)
            ok, why = robots_ok(url)
            if not ok:
                raise RuntimeError(pre + why)
            if host in HOST_CAP and _HCOUNT.get(host, 0) >= HOST_CAP[host]:
                raise Defer(f"{host} 한 실행 요청 한도 {HOST_CAP[host]}건")
            w = max(GAP - (time.time() - c.last), max(GAP, HOST_GAP.get(host, 0)) - (time.time() - _HLAST.get(host, 0.0)))
            if w > 0: time.sleep(w)
            with (_lock(_GLOCK, g) if g else contextlib.nullcontext()):   # 플랫폼은 묶음을 넘어 한 줄로(앞 요청이 끝나고 GAP 뒤)
                if g:
                    w = GAP - (time.time() - _GLAST.get(g, 0.0))
                    if w > 0: time.sleep(w)
                if _STOP.is_set():   # 기다리는 사이 멈춤 — 요청하지 않음(한도 셈도 안 씀)
                    raise RuntimeError(pre + "묶음을 멈춤(시간 초과·다른 묶음 오류) — 더 요청 안 함")
                _HCOUNT[host] = _HCOUNT.get(host, 0) + 1
                c.last = _HLAST[host] = time.time()
                if g:
                    _GLAST[g] = c.last
                try:
                    r = c.sess.get(url, headers=HDR, timeout=25, allow_redirects=False)
                except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
                    _DOWN[host] = _DOWN.get(host, 0) + 1   # v1.3 같은 사이트가 연달아 2번 응답 없으면 이번 실행에서 건너뜀(한 사이트가 시간 제한을 다 쓰지 않게)
                    raise
            _DOWN.pop(host, None)
            loc = (getattr(r, "headers", None) or {}).get("Location") if 300 <= r.status_code < 400 else None
            if not loc:
                if r.status_code in (403, 429, 430):   # v1.12 430 = 쇼피파이가 우리 서버(IP)를 거절
                    _BLOCKED.add(host)   # 실제로 막은 사이트
                    if r.status_code == 430 and g:
                        _GBLOCKED.add(g)   # 플랫폼이 거절 — 그 실행에서 같은 플랫폼 몰 모두 더 요청 안 함
                    raise RuntimeError(pre + f"HTTP {r.status_code}(접속 차단 — 우회하지 않음)")
                if r.status_code >= 400:
                    raise RuntimeError(pre + f"HTTP {r.status_code}")
                if _challenge(r):   # v1.22 HTTP 200인데 봇 확인 화면(언더아머 한국·영국·독일 11/17 'Client Challenge') — 403처럼 그 실행에서 더 요청 안 함
                    _BLOCKED.add(host)
                    raise RuntimeError(pre + "봇 확인 화면(접속 차단 — 우회하지 않음)")
                return r
        try:
            loc = loc.encode("latin1").decode("utf-8")   # requests와 같게 UTF-8 주소 되살림
        except (UnicodeEncodeError, UnicodeDecodeError):
            pass
        url, moved, g0 = urllib.parse.urljoin(url, loc), True, g
    raise RuntimeError(f"넘겨짐이 {hops}번 넘음")


def _json(r):
    d = r.json()
    if not isinstance(d, dict):
        raise RuntimeError("응답 형식이 다름")
    return d


def num(v):
    try:
        x = float(str(v).replace(",", ""))
        return x if x > 0 else None
    except (TypeError, ValueError):
        return None


def _money(s):
    """화면 글자 가격 → 숫자: '$1,234.56' · '1.234,56 €' · '190,00' · '1.234 €'(독일식 천 단위) — '&#8364;'(€) 같은 HTML 기호는 먼저 풂(숫자가 섞이지 않게)"""
    t = re.sub(r"[^0-9.,]", "", unescape(str(s)))
    if re.fullmatch(r"\d{1,3}(\.\d{3})*,\d{1,2}", t):
        t = t.replace(".", "").replace(",", ".")
    elif re.fullmatch(r"\d{1,3}(\.\d{3})+", t):
        t = t.replace(".", "")
    return num(t)


def _micro(html, cur, codes):
    """schema.org 마이크로데이터(itemprop) 가격 — JSON-LD가 없는 SFCC형 몰(써코니 해외). 이 상품 품번(data-stock-number)이 있을 때만.
    판매가 = itemprop price(같이 있는 priceincents ÷ 100 우선 — 190,00 같은 독일식 표기 오해 방지), 정가 = 판매가 바로 뒤 '원래 가격'(price-standard)"""
    stock = " ".join(re.findall(r'data-stock-number="([^"]+)"', html)).lower()
    if not codes or not any(c in stock for c in codes):
        return [], [], False
    offers, end = [], 0
    for m in re.finditer(r'itemprop="priceCurrency"[^>]*>\s*([A-Z]{3})\s*<.{0,300}?itemprop="price"[^>]*>\s*([0-9][0-9.,]*)\s*<'
                         r'(?:(?:(?!itemprop="priceCurrency").){0,200}?itemprop="priceincents"[^>]*>\s*([0-9]+)\s*<)?', html, re.S):   # 다음 가격 칸의 priceincents를 가져오지 않게
        c, p, cents = m.groups()
        v = (int(cents) / 100 if cents else None) or _money(p)
        if c == cur and v:
            offers.append(v); end = m.end()
    lists = []
    for m in re.finditer(r'class="price-sales[^"]*"[^>]*>\s*([^<]*?)\s*<(?:(?!class="price-sales).){0,300}?class="price-standard[^"]*"[^>]*>\s*([^<]*?)\s*<',
                         html[:end], re.S):   # 이 상품 가격 칸(마이크로데이터) 앞만 · 바로 다음 판매가 칸 전까지 — 추천 상품 칸의 원래 가격과 짝짓지 않게
        sv, lv = _money(m.group(1)), _money(m.group(2))
        if sv and lv and sv <= lv <= sv * 3 and any(abs(sv - o) < 0.01 for o in offers):
            lists.append(lv)
    return offers, lists, True


def nike_price(code, cc):
    m, l, cur = MK[cc]
    if not m:   # v1.17 나이키 상품 정보에 없는 나라(두바이 — AE는 정가 100000 자리표시) — 나이키 상품 urls의 페이지로
        raise RuntimeError("나이키 상품 정보에 이 나라 없음 — 상품 urls에 페이지 주소 필요")
    d = _json(get(NIKE_FEED.format(m=m, l=l, s=code)))
    objs = [o for o in d.get("objects") or [] if isinstance(o, dict)]
    if not objs:
        raise Skip("이 나라 나이키에서 팔지 않음")
    for o in objs:
        for pi in o.get("productInfo") or []:
            mp, mer = pi.get("merchPrice") or {}, pi.get("merchProduct") or {}
            if mer.get("styleColor") != code:
                continue
            fp = num(mp.get("fullPrice"))
            if fp and mp.get("currency") == cur:
                return fp, {"cur_price": num(mp.get("currentPrice"))}
    raise RuntimeError("정가(fullPrice) 없음")


REL = {"isSimilarTo", "isRelatedTo", "isAccessoryOrSparePartFor", "isConsumableFor", "itemListElement"}   # 관련·추천 상품 칸


def _ld_nodes(html, skip=()):
    out = []
    for m in re.finditer(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', html, re.S | re.I):
        try:
            d = json.loads(m.group(1).strip())
        except ValueError:
            continue
        st = [d]
        while st:
            x = st.pop()
            if isinstance(x, list):
                st.extend(x)
            elif isinstance(x, dict):
                out.append(x)
                st.extend(v for k, v in x.items() if isinstance(v, (dict, list)) and k not in skip)
    return out


def _types(n):
    t = n.get("@type")
    return {str(x).lower() for x in (t if isinstance(t, list) else [t])}


def page_price(html, hint, cur, codes=()):
    """상품 페이지 → 정가. 글로벌 품번(codes)이 품번·주소에 있는 JSON-LD 상품만 보고, 그런 상품이 없을 때만 이름에 모델명(hint)이
    낱말로 있는 상품을 봄(추천·관련 상품 섞임 방지)"""
    offers, lists = [], []
    codes = [c.lower() for c in codes if c]
    nodes = [n for n in _ld_nodes(html) if _types(n) & {"product", "productgroup"}]
    word = re.compile(rf"(?<![\w-]){re.escape(hint)}(?![\w-])")
    by_code = [n for n in nodes if any(c in " ".join(str(n.get(k, "")) for k in ("sku", "productID", "productGroupID", "mpn", "url", "@id")).lower() for c in codes)]
    prods = by_code
    if not by_code:   # 품번이 없으면 이름으로 — 관련·추천 상품 칸은 빼고, 이름이 다른 상품이 여럿이면 실패(틀린 값을 저장하지 않게)
        prods = [n for n in _ld_nodes(html, REL) if _types(n) & {"product", "productgroup"} and word.search(str(n.get("name", "")).lower())]
        names = {str(n.get("name", "")).strip().lower() for n in _ld_nodes(html, REL | {"hasVariant"})
                 if _types(n) & {"product", "productgroup"} and word.search(str(n.get("name", "")).lower())}
        if len(names) > 1:
            raise RuntimeError(f"품번이 없고 이름이 비슷한 상품이 여럿({' / '.join(sorted(names))[:60]})")
    for p in prods:
        st = [p.get("offers"), p.get("hasVariant")]
        while st:
            x = st.pop()
            if isinstance(x, list): st.extend(x); continue
            if not isinstance(x, dict): continue
            if _types(x) & {"product"}: st.append(x.get("offers")); continue
            if str(x.get("priceCurrency", cur)) == cur:
                v = num(x.get("price") or x.get("highPrice") or x.get("lowPrice"))
                if v: offers.append(v)
            for ps in (x.get("priceSpecification") if isinstance(x.get("priceSpecification"), list) else [x.get("priceSpecification")]):
                if isinstance(ps, dict) and re.search(r"ListPrice|StrikethroughPrice", str(ps.get("priceType", ""))) and str(ps.get("priceCurrency", cur)) == cur:
                    v = num(ps.get("price"))
                    if v: lists.append(v)
            if x.get("offers"): st.append(x.get("offers"))
    flat = html.replace('\\"', '"')
    # SFCC형 몰(푸마 멕시코): 화면 데이터의 c_listPrice(정가)·c_salePrice(판매가) — 판매가가 이 상품 가격과 같을 때만(추천 상품 섞임 방지)
    for m in re.finditer(r'"c_listPrice":([0-9.]+),"c_salePrice":([0-9.]+)', flat):
        lp, sp = num(m.group(1)), num(m.group(2))
        if lp and sp and sp <= lp <= sp * 3 and any(abs(sp - o) < 0.01 for o in offers):
            lists.append(lp)
    # SFCC형 몰(푸마 한국 등): 가격인하 중이면 JSON-LD에는 판매가만 — 이 상품 가격 칸의 취소선 정가(strike-through list)를 정가로.
    # 이 상품 것만: 취소선 바로 곁 판매가 칸(sales — 푸마 한국은 취소선 바로 앞, SFCC 기본은 바로 뒤)의 값이 이 상품 판매가(JSON-LD)와 같을 때만
    # (추천 상품 칸의 할인 가격을 가져오지 않게) · 그런 정가가 한 가지일 때만 · 판매가보다 높고 5배 안(70% 할인까지 — 푸마 한국 팔레르모 10/22 119,000 → 35,700원)
    lps = set()
    for m in re.finditer(r'class="strike-through list"[^>]*>\s*(?:<(?!span class="value")[^>]+>\s*)*<span class="value"[^>]*>\s*([^<]+?)\s*</span>', html):
        back = html[max(0, m.start() - 600):m.start()]; k = back.rfind('class="sales')
        seg = back[k:] if k >= 0 else html[m.end():m.end() + 600]
        sm = re.search(r'class="sales[^"]*"(?:(?!strike-through).)*?<span class="value"[^>]*>\s*([^<]+?)\s*</span>', seg, re.S)
        lp, sv = _money(m.group(1)), _money(sm.group(1)) if sm else None
        if lp and sv and any(abs(sv - o) < 0.01 for o in offers) and sv <= lp <= sv * 5:
            lps.add(lp)
    if len(lps) == 1:
        lists.append(lps.pop())
    # 아크테릭스 한국: JSON-LD에는 판매가만 — 화면 데이터의 정가(retail_price). 이 상품 것만(같은 { } 묶음 안에 이 상품 품번) · 판매가(sell·last)가
    # 이 상품 JSON-LD 가격과 같을 때만 · 판매가보다 높고 5배 안
    for m in re.finditer(r'"retail_price":([0-9.]+),"sell_price":([0-9.]+),"last_price":([0-9.]+)', flat):
        back = flat[max(0, m.start() - 400):m.start()]
        if not any(c in back[back.rfind("{") + 1:].lower() for c in codes): continue
        lp, sps = num(m.group(1)), [num(m.group(2)), num(m.group(3))]
        if lp and any(sp and sp <= lp <= sp * 5 and any(abs(sp - o) < 0.01 for o in offers) for sp in sps):
            lists.append(lp)
    # 살로몬 해외: 상품 이름 바로 뒤 기본가(basePrice) — 화면 데이터가 따옴표를 \"로 감싸 둠. 품번이 맞는 것 우선, 없으면 이름(모델명)
    base_code, base_name = set(), set()
    for m in re.finditer(r'"name":"([^"]{0,80})","newModelCodes":\[([^\]]*)\],"price":\{"basePrice":([0-9.]+),"currency":"([A-Z]{3})"', flat):
        v = num(m.group(3))
        if not v or m.group(4) != cur: continue
        if any(c in m.group(2).lower() for c in codes): base_code.add(v)
        elif word.search(m.group(1).lower()): base_name.add(v)
    base = base_code or base_name
    if len(base) > 1:
        raise RuntimeError(f"여러 상품 기본가가 섞임({', '.join(f'{x:g}' for x in sorted(base))})")
    lists.extend(base)
    micro = False
    if not prods and not lists:   # JSON-LD가 없으면 마이크로데이터(써코니 해외 — 품번이 페이지 상품 칸에 있을 때만)
        mo, ml, micro = _micro(html, cur, codes)
        offers += mo; lists += ml
    if not prods and not lists and not micro:
        raise RuntimeError("상품 가격 데이터(JSON-LD) 없음")
    if not offers and not lists:
        raise RuntimeError(f"{cur} 가격 없음")
    full = max(lists) if lists else max(offers)
    if offers and max(offers) > full: full = max(offers)   # 정가 명세보다 높은 판매가는 없으므로 높은 쪽
    return full, {"cur_price": min(offers) if offers else None, "by": "품번" if by_code or base_code or micro else "이름" if prods or base_name else ""}


def cafe24_list(html, sale):
    """v1.13 카페24 몰(브룩스 한국): 할인 중이면 JSON-LD에는 판매가만 — 이 상품 판매가 칸(product_price) 바로 뒤 소비자가 칸(price_custom)을 정가로.
    판매가 칸 값이 이 상품 JSON-LD 판매가와 같을 때만(추천 상품 칸 섞임 방지) · 그런 소비자가가 한 가지일 때만 · 판매가보다 높고 5배 안"""
    lps = set()
    for m in re.finditer(r'class="product_price">\s*([\d,]+)\s*<span>원</span>\s*</p>\s*<p class="price_custom[^"]*">\s*([\d,]+)\s*원', html):
        sv, lp = num(m.group(1)), num(m.group(2))
        if sv and lp and abs(sv - sale) < 0.01 and sv < lp <= sv * 5:
            lps.add(lp)
    return lps.pop() if len(lps) == 1 else None


SFRA_BOX = re.compile(r'b-pdp__priceline|product-detail__priceline|b-microproduct__price|product-tile')   # v1.17 가격 칸 표시 — 뒤 것(추천 상품 칸)은 이 상품 아님
SFRA_STRIKE = re.compile(r'class="strike-through list"[^>]*>\s*(?:<(?!span class="value")[^>]+>\s*)*<span class="value"[^>]*?content="([0-9][0-9.,]*)"')
SFRA_SALES = re.compile(r'class="sales[^"]*"(?:(?!strike-through).)*?<span class="value"[^>]*?content="([0-9][0-9.,]*)"', re.S)


def sfra_list(html, code, pre, sale):
    """v1.17 두바이 SFCC(SFRA) 몰(nike.ae·underarmour.ae) 정가 — 취소선 정가가 글자 대신 <span class="value" content="799.00">이고 추천 상품 칸에도 취소선이 있음.
    ① 이 상품 품번: 상품 상세 칸(data-gtm-onload="pdpView" 태그)의 data-variation-group-id가 pre + 품번(나이키 NKCW2288-111 · 언더아머 UA1372586-001)
    ② 이 상품 GTM 상세(data-gtm-enhance-commerce-details · ecommerce.detail) 판매가 price = JSON-LD 판매가(sale)
    ③ 취소선 정가 = 바로 앞 가격 칸 표시가 이 상품 가격 칸(b-pdp__priceline·product-detail__priceline·b-microproduct__price — product-tile은 추천 상품)이고
       같은 칸 판매가(sales content)가 sale인 것 · 한 가지 · 판매가보다 높고 5배 안 · GTM 정가 item_original_price와 같아야 함
    ④ 취소선이 없으면 GTM 정가가 판매가와 같을 때만 판매가가 정가(할인 중인데 취소선 정가를 못 읽으면 실패 — 할인가를 정가로 쓰지 않음)"""
    if re.search(r'data-producttype-memberonly="true"', html):
        raise RuntimeError("회원 전용 상품 — 넣지 않음")
    want, dets = (pre + code).upper(), {}
    for m in re.finditer(r'data-variation-group-id="([^"]+)"', html):
        e = html.find("<", m.end())
        tag = html[html.rfind("<", 0, m.start()):e if e >= 0 else len(html)]   # 그 태그(속성 값에는 < 가 없음 — &lt;)
        gm = re.search(r'data-gtm-enhance-commerce-details="([^"]*)"', tag)
        if 'data-gtm-onload="pdpView"' not in tag or not gm:
            continue   # 상품 상세 칸이 아님
        try:
            ps = ((json.loads(unescape(gm.group(1))).get("ecommerce") or {}).get("detail") or {}).get("products") or []
        except (ValueError, AttributeError):
            continue
        if ps and isinstance(ps[0], dict):
            dets[m.group(1).upper()] = ps[0]
    if len(dets) != 1:
        raise RuntimeError(f"이 상품 상세 칸(GTM 상세) {len(dets)}개 — 페이지 모양이 바뀜(정가 확인 안 됨)")
    vg, d = dets.popitem()
    if vg != want and not vg.startswith(want + "-"):
        raise RuntimeError(f"품번 표시가 다름({vg}) — 다른 상품으로 바뀜(대응표 확인)")
    gp, go = num(d.get("price")), num(d.get("item_original_price"))
    if not sale or not gp or abs(gp - sale) > 0.01 or not go:
        raise RuntimeError(f"판매가가 서로 다름(JSON-LD {sale} · GTM {d.get('price')}/{d.get('item_original_price')})")
    lps = set()
    for m in SFRA_STRIKE.finditer(html):
        box = list(SFRA_BOX.finditer(html, max(0, m.start() - 1500), m.start()))
        if not box or box[-1].group(0) == "product-tile":
            continue   # 이 상품 가격 칸이 아님(추천 상품 칸 · 표시 없음)
        nxt = SFRA_BOX.search(html, m.end())
        sm = SFRA_SALES.search(html[box[-1].start():nxt.start() if nxt else m.end() + 1500])   # 같은 가격 칸 안 판매가(나이키는 취소선 뒤 · 언더아머는 앞)
        lp, sv = num(m.group(1)), num(sm.group(1)) if sm else None
        if lp and sv and abs(sv - sale) < 0.01 and sv < lp <= sv * 5:
            lps.add(lp)
    if len(lps) > 1:
        raise RuntimeError(f"이 상품 취소선 정가가 여러 가지({', '.join(f'{x:g}' for x in sorted(lps))})")
    if lps:
        lp = lps.pop()
        if abs(lp - go) > 0.01:
            raise RuntimeError(f"취소선 정가 {lp:g} ≠ GTM 정가 {go:g}")
        return lp
    if go > sale * 1.005:
        raise RuntimeError(f"할인가 {sale:g}만 읽힘(GTM 정가 {go:g} · 취소선 정가 칸을 못 찾음) — 할인가를 정가로 쓰지 않음")
    return sale


def shopify_price(url, code, cur):
    p = _json(get(url)).get("product") or {}
    vs = [v for v in p.get("variants") or [] if isinstance(v, dict) and code.lower() in str(v.get("sku", "")).lower()]
    tags = p.get("tags") if isinstance(p.get("tags"), list) else str(p.get("tags") or "").split(",")
    if not vs and (code.lower().replace("-", "") in str(p.get("handle", "")).lower().replace("-", "")
                   or code.lower() in {str(t).strip().lower() for t in tags}):
        vs = [v for v in p.get("variants") or [] if isinstance(v, dict)]   # 변형 품번이 바코드인 몰 — 상품 주소(handle, 헌터 미국·영국)나 상품 태그(킨 미국·독일)에 품번
    if not vs and len(p.get("variants") or []) >= 250:   # v1.17 쇼피파이 상품 .json은 변형 250개까지만 — 그 뒤 색상은 응답에 없음(대응표 문제가 아닐 수 있음)
        raise RuntimeError("이 품번 변형이 응답에 없음 — 상품 .json이 변형 250개에서 잘림(쇼피파이 한도 · 이 색상이 뒤로 밀렸을 수 있음)")
    if not vs:
        raise RuntimeError("품번이 다른 상품(대응표 확인)")
    # 쇼피파이 마켓은 접속한 나라 통화로 보여 줄 수 있음(GitHub 서버가 멕시코면 페소) — 변형의 통화 표시가 다르면 실패(이전 값 유지)
    bad = {str(v.get(k)) for v in vs for k in ("price_currency", "compare_at_price_currency") if v.get(k) and str(v.get(k)) != cur}
    if bad:
        raise RuntimeError(f"{cur} 가격 없음(통화 {', '.join(sorted(bad))} — 접속한 서버 나라 통화)")
    full = max(max(num(v.get("price")) or 0, num(v.get("compare_at_price")) or 0) for v in vs)
    if not full:
        raise RuntimeError("가격 없음")
    extra = {"cur_price": min(num(v.get("price")) or full for v in vs)}
    k = SHOP_MODEL.get(urllib.parse.urlsplit(url).netloc)
    if k and not any(num(v.get("compare_at_price")) for v in vs):   # v1.17 할인 표시 없이 일부 색상 값만 내리는 몰(on.ae) — 같은 모델 다른 색상이 더 비싸면 정가 확인 안 됨
        top = max([num(v.get("price")) or 0 for v in p.get("variants") or [] if isinstance(v, dict)
                   and str(v.get("sku", "")).upper().startswith(code.upper()[:k])] or [0])
        if top > full * 1.005:
            extra["unsure"] = f"이 색상만 값이 낮음({full:g} · 같은 모델 다른 색상 {top:g} — 할인 표시 없는 할인으로 보임) — 처음 값으로 쓰지 않음"
    return full, extra


def godo_price(html, cur, code):
    """고도몰형 한국 몰(킨·우포스 — 수입사 LF 공식몰): 상품 정보 칸 품번(ARTICLE · Article No.)이 이 상품 품번과 같을 때만, 이 상품 주문 칸의
    숨은 값 정가(set_goods_fixedPrice)·판매가(set_goods_price) 중 높은 값 — 정가를 비워 두면(0) 판매가 · 같은 칸 값이 여러 가지면 실패"""
    if cur != "KRW":
        raise RuntimeError(f"{cur} 가격 없음")
    arts = {unescape(a).strip().lower() for a in re.findall(r'(?:ARTICLE</td>|Article No\.</th>)\s*<td[^>]*>\s*([^<]+?)\s*</td>', html)}
    if code.lower() not in arts:
        raise RuntimeError(f"상품 정보 칸 품번이 다름({', '.join(sorted(arts))[:40] or '품번 칸 없음'}) — 다른 상품으로 바뀜(대응표 확인)")
    def hid(k):
        vs = {num(v) for v in re.findall(rf'name="{k}"\s+value="([0-9.,]+)"', html)}
        if len(vs) > 1:
            raise RuntimeError(f"{k} 값이 여러 가지")
        return vs.pop() if vs else None
    fp, sp = hid("set_goods_fixedPrice"), hid("set_goods_price")
    if not (fp or sp):
        raise RuntimeError("상품 가격 칸(set_goods_price) 없음")
    return max(fp or 0, sp or 0), {"cur_price": sp or fp}


def _feed(prod, cc):
    """v1.17 나이키 상품 정보(product_feed)로 받는 값 — 나이키 상품이라도 urls에 있는 나라(두바이)는 페이지로 읽음(페이지 값처럼 할인 가드·크게 바뀜)"""
    return prod["src"] == "nike" and cc not in (prod.get("urls") or {})


def paused_of(prod, cc):
    """v1.19 이 값의 사이트가 수집을 멈춘 사이트(PAUSED)면 {since, why}, 아니면 None — 나이키 상품 정보(product_feed) 값은 해당 없음"""
    u = None if _feed(prod, cc) else (prod.get("urls") or {}).get(cc)
    return PAUSED.get(urllib.parse.urlsplit(u).netloc) if u else None


def ccs(prod):
    """v1.17 상품이 받는 나라 — 나이키는 상품 정보 나라(cc) + 페이지 나라(urls), 그 밖은 urls"""
    if prod["src"] == "nike":
        return list(prod["cc"]) + [cc for cc in prod.get("urls") or {} if cc not in prod["cc"]]
    return list(prod["urls"])


def fetch_one(prod, cc):
    cur = MK[cc][2]
    code = (prod.get("cc_code") or {}).get(cc, prod["code"])   # 그 나라 수입사 품번이 따로 있으면(브룩스 일본)
    if _feed(prod, cc):
        return nike_price(prod["code"], cc), NIKE_FEED.format(m=MK[cc][0], l=MK[cc][1], s=prod["code"])
    url = prod["urls"].get(cc)
    if not url:
        raise Skip("주소 없음")
    if url.endswith(".json"):
        return shopify_price(url, code, cur), url[:-5]
    r = get(url)
    loc = urllib.parse.urlsplit(url).path.split("/")[1]
    if prod["id"].startswith("on-") and loc not in urllib.parse.urlsplit(r.url).path:   # 온: 그 나라 몰이 없으면 다른 나라로 넘김
        raise Skip(f"다른 나라 몰로 넘어감({urllib.parse.urlsplit(r.url).path.split('/')[1]})")
    if prod["id"].startswith("on-"):   # v1.20 그 나라 몰에서 빠진 색상은 목록(/shop)으로 넘어감(11/10 한국·일본) — 다른 상품 페이지로 넘어가도 이름으로 엉뚱한 값을 읽지 않게
        fp = urllib.parse.urlsplit(r.url).path
        if "/products/" not in fp:
            raise RuntimeError(f"상품 페이지가 목록({fp})으로 넘어감 — 그 나라 몰에서 빠짐(다른 색상·새 모델로 바꿈)")
        mod = lambda pth: pth.split("/products/", 1)[1].split("/", 1)[0] if "/products/" in pth else ""
        if mod(fp) != mod(urllib.parse.urlsplit(url).path):   # 같은 모델 다른 색상으로 넘어간 것은 예전처럼(온러닝 정가는 모델마다 같음 — 이름으로 찾음)
            raise RuntimeError(f"다른 모델 페이지({mod(fp)})로 넘어감 — 이 상품({mod(urllib.parse.urlsplit(url).path)})이 그 나라 몰에서 빠짐")
    if prod.get("code_in_page") and code.lower() not in r.text.lower():   # 품번이 JSON-LD 밖에만 있는 몰 — 페이지에 품번이 없으면 다른 상품
        raise RuntimeError(f"페이지에 품번({code}) 없음 — 다른 상품으로 바뀜(대응표 확인)")
    if 'name="set_goods_fixedPrice"' in r.text:   # 고도몰형 한국 몰(킨·우포스) — JSON-LD 없음, 상품 정보 칸 품번으로 확인
        return godo_price(r.text, cur, code), url
    full, extra = page_price(r.text, prod.get("hint") or code, cur, [code] + prod.get("alt", []))   # 나이키 상품은 hint 없음(품번으로만 찾음)
    host = urllib.parse.urlsplit(url).netloc
    if host in SFRA_LIST:   # v1.17 두바이 SFCC 몰 — 이 상품 품번 표시·GTM 상세로 확인한 취소선 정가(할인 중이면 JSON-LD는 판매가뿐)
        if extra.get("cur_price") is None or abs(full - extra["cur_price"]) > 0.01:
            raise RuntimeError(f"JSON-LD 가격이 여러 가지({full:g} · {extra.get('cur_price')})")
        full = sfra_list(r.text, code, SFRA_LIST[host], extra["cur_price"])
        extra["by"] = "품번"   # data-variation-group-id로 확인(JSON-LD 품번이 바코드인 언더아머 상품도)
    if host in CAFE24_LIST:   # v1.13 카페24 몰 소비자가 칸 — 할인 중이면 JSON-LD에 판매가만
        lp = cafe24_list(r.text, full)
        if lp:
            full = lp
    return (full, extra), url


def cfg_hash():   # v1.23 분류(cat)는 화면 착지 계산용이라 빼고 셈 — 분류만 바꾼 날 전체를 다시 받지 않음
    return hashlib.sha1(json.dumps([{k: v for k, v in p.items() if k != "cat"} for p in PRODUCTS], ensure_ascii=False, sort_keys=True).encode()).hexdigest()[:12]


def _hosts(p):
    """상품이 요청하는 사이트(나라마다 하나)"""
    return [urllib.parse.urlsplit(NIKE_FEED if _feed(p, cc) else p["urls"][cc]).netloc for cc in ccs(p)]   # v1.17 나이키 페이지 나라(두바이)는 그 사이트


def build_lanes(products):
    """v1.12 동시에 받을 묶음 — 브랜드·사이트(·ROBOTS_ALT·LANE_JOIN)로 이어진 상품끼리 한 묶음, 묶음 안은 PRODUCTS 순서.
    한 사이트·한 브랜드는 늘 한 묶음에만 있음(사이트별 요청 수·한도 미룸·브랜드 셈을 그 묶음만 씀).
    est = 예상 초(값 × max(GAP, HOST_GAP), 한도 사이트는 한도까지) — 긴 묶음부터 시작"""
    par = {}
    def find(x):
        par.setdefault(x, x)
        while par[x] != x:
            par[x] = par[par[x]]; x = par[x]
        return x
    def union(a, b):
        par[find(a)] = find(b)
    for p in products:
        for h in _hosts(p):
            union("b:" + p["brand"], "h:" + h)
            if h in ROBOTS_ALT:
                union("h:" + h, "h:" + urllib.parse.urlsplit(ROBOTS_ALT[h]).netloc)
    for a, b in LANE_JOIN:
        union("b:" + a, "b:" + b)
    lanes = {}
    for p in products:
        ln = lanes.setdefault(find("b:" + p["brand"]), {"prods": [], "brands": [], "hosts": collections.Counter()})
        ln["prods"].append(p); ln["hosts"].update(_hosts(p))
        if p["brand"] not in ln["brands"]:
            ln["brands"].append(p["brand"])
    for ln in lanes.values():
        ln["name"], ln["n"] = "+".join(ln["brands"]), sum(ln["hosts"].values())
        ln["est"] = sum(min(n, HOST_CAP.get(h, n)) * max(GAP, HOST_GAP.get(h, 0)) for h, n in ln["hosts"].items())
    return list(lanes.values())


def pace_map(products):
    """v1.12 사이트 → 플랫폼 묶음 — 쇼피파이 상품 .json 주소의 사이트 + PACE_EXTRA"""
    pm = {urllib.parse.urlsplit(u).netloc: "shopify" for p in products for u in (p.get("urls") or {}).values() if u.endswith(".json")}
    pm.update(PACE_EXTRA)
    return pm


def _lanes_n():
    try:
        return max(1, min(16, int(os.environ.get("PRICE_LANES") or LANES)))
    except ValueError:
        return LANES


def main():
    t0 = time.time(); now = datetime.datetime.now(KST); today = now.date(); td = today.isoformat()
    old = {}
    if os.path.exists(OUT):
        try:
            with open(OUT, encoding="utf-8") as f: old = json.load(f)
        except (OSError, ValueError) as e:
            log(f"[WARN] {OUT} 읽기 실패 — 처음부터: {e}")
    def _days(d): return (today - datetime.date.fromisoformat(d)).days
    last, tried = old.get("fetched"), old.get("tried")   # 받은 날(잘 끝난 실행) · 못 받아 다시 받을 값이 남은 날
    att = old.get("attempt") or last                      # 마지막으로 전체를 받으러 간 날(잘 됐든 안 됐든)
    cfg = cfg_hash()
    if os.environ.get("PRICE_FORCE") == "1" or old.get("cfg") != cfg or not att or _days(att) >= DAYS:
        mode = "full"
    elif tried:
        mode = "retry"   # 지난 실행에서 못 받은 값만 다시
    else:
        mode = None
    if not mode:   # v1.19 PAUSED에서 뺀 사이트(지난 실행까지 표시 paused) — 다음 전체 받기를 기다리지 않고 그 값을 바로 다시 받기로(받기 전에 21일 알림이 먼저 나지 않게)
        _bp = {p["id"]: p for p in PRODUCTS}
        unp = [f"{it.get('id')} {cc}" for it in old.get("items", []) if isinstance(it, dict) and it.get("id") in _bp
               for cc, o in (it.get("m") or {}).items() if isinstance(o, dict) and o.get("paused") and not paused_of(_bp[it["id"]], cc)]
        if unp:
            mode = "retry"
            log(f"해외 정가: 수집 멈춤을 푼 값 {len(unp)}건 — 바로 다시 받기({', '.join(unp[:5])}{' …' if len(unp) > 5 else ''})")
    codes = {p["id"]: p["code"] for p in PRODUCTS}
    # 품번이 바뀐 상품은 id가 같아도 다른 상품 — 이전 값·값 없음 기록을 쓰지 않음
    prev = {it["id"]: it for it in old.get("items", []) if isinstance(it, dict) and it.get("code") == codes.get(it.get("id"))}
    keys = {f"{p['id']} {cc}" for p in PRODUCTS for cc in ccs(p)}
    failed = {k: f for f in old.get("failed", []) if isinstance(f, dict) and (k := f"{f.get('id')} {f.get('cc')}") in keys
              and f.get("code", codes.get(f.get("id"))) == codes.get(f.get("id"))}   # 값 없음(이전 값도 없음) — 처음 실패한 날
    # v1.9 한도 사이트(HOST_CAP) 값마다 마지막으로 받으러 간 날(그 실행에서 사이트가 막혀 요청을 못 보낸 날 포함 — 그날 못 받은 것으로 셈) — 다시 받기에서 이번 주기에 아직 다시 받아 보지 않은 값을 먼저(한도로 미룬 날은 받으러 간 날이 아님)
    htry = {k: v for k, v in (old.get("host_try") or {}).items() if k in keys and isinstance(v, str)}
    ok_run, again = None, False
    if not mode:
        log(f"해외 정가: 주 1회 — 마지막 {att}, 다음 {datetime.date.fromisoformat(att) + datetime.timedelta(days=DAYS)} (건너뜀)")
        items = [it for it in old.get("items", []) if isinstance(it, dict) and it.get("id") in codes]
    else:
        if mode == "retry":
            log(f"해외 정가: 다시 받기 — {att} 받기에서 못 받은 값만")
        items, bt, cnt = [], {}, collections.Counter()   # bt = 브랜드별 [볼 값, 못 받은 값] — 한 브랜드를 통째로 못 받으면 다음 날 다시
        def _prev_o(pi, prod, cc):   # 이전 값(나라별 수입사 품번이 바뀌었으면 없음)
            pv = pi.get("m", {})
            same = (pi.get("cc_code") or {}).get(cc) == (prod.get("cc_code") or {}).get(cc)
            return dict(pv.get(cc) or {}) if same and isinstance(pv.get(cc), dict) else {}
        def _capped(prod, cc):   # 한 실행 요청 한도가 있는 사이트(HOST_CAP)면 그 주소의 사이트
            u = None if _feed(prod, cc) else prod["urls"].get(cc)
            h = urllib.parse.urlsplit(u).netloc if u else ""
            return h if h in HOST_CAP else ""
        def _done(o):   # 다시 받기 — 이번 주기에 이미 받은 값(그대로 둠)
            return mode == "retry" and bool(o) and not o.get("stale_since") and (o.get("obs_date") or "") >= (att or "")
        def _due(key):   # v1.9 이번 주기에 아직 다시 받아 보지 않음(마지막 요청이 전체 받기 날이나 그 전 — 미룬 값·새 값·전체 받기 날 못 받은 값)
            return (htry.get(key) or "") <= (att or "")
        # v1.9 다시 받기에서는 한도 사이트의 _due 값을 먼저 — 다시 받기에서도 못 받은 값이 한도를 다 써서 다른 값이 영영 안 받히지 않게
        # (검토 반영 10/26). _due 값 수를 미리 세어 두고, 그 밖의 값은 남은 한도가 그만큼 있을 때만
        due_left = {}
        if mode == "retry":
            for prod in PRODUCTS:
                pi = prev.get(prod["id"]) or {}
                for cc in ccs(prod):
                    h = _capped(prod, cc)
                    if h and _due(f"{prod['id']} {cc}") and not _done(_prev_o(pi, prod, cc)):
                        due_left[h] = due_left.get(h, 0) + 1
        def _cut(prod, cc, o, key):   # 시간 초과 — 이전 값(다음 날 다시) · 이전 값도 없으면 값 없음(처음 못 받은 날부터 21일 알림)
            if o:
                o.setdefault("stale_since", o.get("obs_date") or o.get("seen") or td); o["why"] = "시간 초과로 못 받음"
                return {"o": o, "n": {"cut": 1}}
            f = dict(failed.get(key) or {"id": prod["id"], "cc": cc, "since": td})
            f.update(code=prod["code"], brand=prod["brand"], name=prod["name"], why="시간 초과로 못 받음")
            return {"fop": ("set", f), "n": {"cut": 1}}
        def _value(prod, cc, pi, cut=False):
            """v1.12 값 하나 받기 — 묶음(스레드) 안에서 돎. 공유 기록(failed·htry·bt)은 읽기만 하고 결과로 돌려줌 —
            o = 상품 m에 넣을 값 · fop = 값 없음 기록(pop·set) · hop = 받으러 간 날(host_try) · n = 셈 · b = 브랜드 [볼 값, 못 받은 값]"""
            o = _prev_o(pi, prod, cc); key = f"{prod['id']} {cc}"   # 나라별 수입사 품번을 바꾸면 그 나라 이전 값은 다른 상품
            if _done(o):
                return {"o": o, "b": (1, 0)}   # 지난 받기에서 받은 값 — 그대로
            pz = paused_of(prod, cc)
            if pz:   # v1.19 수집을 멈춘 사이트 — 요청 없이 이전 값 그대로(셈·알림 밖 · 표시는 아래 합칠 때 매김)
                st = o.get("stale_since") or o.get("obs_date") or o.get("seen")
                log(f"  {key}: 건너뜀 — {pz['why']}(수집 멈춤 · {pz['since'][5:]}부터)" + (f" · 이전 값({str(st)[5:10]} 받은 값)" if o else " · 이전 값 없음"))
                if o:
                    o.setdefault("stale_since", st or td)
                    return {"o": o, "n": {"paused": 1}}
                return {"fop": ("pop",), "n": {"paused": 1}}   # 이전 값도 없음 — 값 없음 기록도 지움(알림 안 냄)
            host = _capped(prod, cc); due = bool(host) and _due(key)
            if host and mode == "retry":   # 한도 사이트는 한 묶음에만 있어 due_left·_HCOUNT를 그 묶음만 씀
                if due:
                    due_left[host] = max(0, due_left.get(host, 0) - 1)
                elif _HCOUNT.get(host, 0) + due_left.get(host, 0) >= HOST_CAP[host]:   # 다시 받기에서도 못 받은 값 — 아직 다시 받아 보지 않은 값에 한도를 먼저
                    log(f"  {key}: 다음에 다시 — {host} 한도는 아직 다시 받아 보지 않은 값 먼저")
                    return {"o": o, "n": {"defer": 1}}
            if cut or time.time() - t0 > TIME_LIMIT:   # 남은 것은 이전 값(다음 날 다시) · cut = 묶음이 안 끝나 요청 없이 시간 초과로
                return _cut(prod, cc, o, key)
            hop = ("set", td) if host else None   # v1.9 받으러 간 날(한도로 미루면 그대로 둠)
            try:
                (full, extra), src_url = fetch_one(prod, cc)
                if MK[cc][2] == "KRW" and full < 1000:   # 원화가 1,000원 아래면 단위가 다른 응답
                    raise RuntimeError(f"원화 값이 이상함({full:g})")
                if extra.get("unsure") and not (o.get("p") and o.get("cur") == MK[cc][2]):   # v1.17 정가 확인 안 됨(on.ae 표시 없는 할인) — 이전 값이 있으면 아래 할인 가드
                    raise RuntimeError(extra["unsure"])
            except Defer as e:   # v1.8 사이트 요청 한도 — 이전 값 그대로 두고 다음 실행에서(실패·이전 값 표시 아님)
                n = {"defer": 1, "due_defer": int(due)}
                log(f"  {key}: {'다음 실행에서' if mode == 'full' or due else '다음 주에'} 받음 — {e}")
                if o:
                    if not o.get("stale_since") and _days(o.get("obs_date") or o.get("seen") or td) > DAYS + 1:   # v1.9 한 주기 넘게 못 받음 → 이전 값 표시·21일 알림에 들어가게
                        o["stale_since"] = o.get("obs_date") or o.get("seen") or td; o["why"] = "사이트 요청 한도로 미룸"
                    return {"o": o, "n": n}
                f = dict(failed.get(key) or {"id": prod["id"], "cc": cc, "since": td})   # v1.9 이전 값도 없음(새 상품·나라) → 값 없음으로 보이게(다음 날 받으면 지움)
                f.update(code=prod["code"], brand=prod["brand"], name=prod["name"], why="사이트 요청 한도로 미룸 — 다음 실행에서")
                return {"fop": ("set", f), "n": n}
            except Skip as e:
                if not o:   # 처음부터 이 나라에서 팔지 않음 — 실패 아님
                    log(f"  {key}: 건너뜀 — {e}")
                    return {"fop": ("pop",), "hop": hop}
                e = RuntimeError(f"전에는 받았는데 이번엔 {e}")   # 조용히 사라지지 않게 실패로 셈
                log(f"  {key}: 못 받음 — {e}")
                o.setdefault("stale_since", o.get("obs_date") or o.get("seen") or td); o["why"] = str(e)[:80]
                return {"o": o, "hop": hop, "n": {"try": 1, "fail": 1}, "b": (1, 1)}
            except Exception as e:   # 이상한 응답 모양(AttributeError 등)도 이 값만 실패로
                why = f"{type(e).__name__}: {e}" if not isinstance(e, RuntimeError) else str(e)
                log(f"  {key}: 못 받음 — {why[:120]}")
                if o:
                    o.setdefault("stale_since", o.get("obs_date") or o.get("seen") or td); o["why"] = why[:80]
                    return {"o": o, "hop": hop, "n": {"try": 1, "fail": 1}, "b": (1, 1)}
                f = dict(failed.get(key) or {"id": prod["id"], "cc": cc, "since": td})
                f.update(code=prod["code"], brand=prod["brand"], name=prod["name"], why=why[:80])
                return {"fop": ("set", f), "hop": hop, "n": {"try": 1, "fail": 1}, "b": (1, 1)}
            n = {"try": 1}
            full = round(full, 2); cur = MK[cc][2]
            note, held, guard = "", False, False
            same = o.get("p") and o.get("cur") == cur
            hist = {k: o[k] for k in ("sh", "ph") if same and isinstance(o.get(k), list)}   # v1.5 기록은 통화가 같을 때만 이어 감
            seen_off = bool(same and (o.get("sh") or o.get("off_seen") or (o.get("sale") is False and not o.get("cand"))))   # 할인 아닌 상태를 본 적 있음(그 뒤 할인 = 할인 시작 · 보류 중 sale False는 판단 안 한 것 — 보류 전에 본 것은 off_seen으로 이어 감)
            feed = _feed(prod, cc)   # v1.17 나이키 상품 정보 정가(fullPrice)만 — 나이키 두바이 페이지 값은 다른 몰처럼
            big = same and (full > o["p"] * JUMP or (feed and full < o["p"] / JUMP))
            if big and not (o.get("cand") and abs(o["cand"] - full) <= o["cand"] * 0.10):   # 크게 바뀜 — 다음 확인 때 비슷하면 반영
                n["hold"] = 1; held = True
                o.update(cand=full, cand_date=td, obs=full, obs_date=td, url=src_url, sale=False)
                o.pop("stale_since", None); o.pop("why", None)
                o.pop("sp", None); o.pop("sp_date", None)   # v1.5 보류 중엔 할인 판단 안 함(어느 정가 기준인지 모름) — 할인 기록 sh는 그대로 두고 확인 뒤 이어 감
                if seen_off:
                    o["off_seen"] = True
                note = f"정가 {o['p']:,g} {cur} 유지(이번 {full:,g} — 크게 바뀜, 다음 확인 때 비슷하면 반영)"
            elif (same and not big and not feed and full < o["p"] * 0.995
                  and _days(o.get("seen") or td) < SALE_GUARD):   # 할인 가드
                o.update(obs=full, obs_date=td, sale=True, url=src_url)
                for k in ("stale_since", "why", "cand", "cand_date", "off_seen"): o.pop(k, None)
                note, guard = f"정가 {o['p']:,g} {cur} 유지(이번 {full:,g} — 할인으로 봄)", True
            else:
                old_p = o.get("p") if same else None
                o = {"p": full, "cur": cur, "seen": td, "url": src_url, "obs": full, "obs_date": td, "sale": False, **hist}
                note = f"정가 {full:,g} {cur}"
                if old_p and abs(full - old_p) > old_p * 0.005:   # v1.5 정가 변동 기록(크게 바뀐 값은 다음 확인에서 반영된 날)
                    o["ph"] = (o.get("ph") or [])[-(PH_MAX - 1):] + [[td, old_p, full]]
                    note += f" (전 {old_p:,g} → {(full / old_p - 1) * 100:+.1f}%)"
            # v1.5 할인가 — 지금 가장 싼 색상·사이즈(cur_price). 할인 가드로 정가를 지킨 날은 이번에 보인 값(full)도 할인가 후보
            if not held:
                cands = [v for v in (extra.get("cur_price"), full if guard else None) if v]
                note_sale(o, min(cands) if cands else None, td, seen_off)
            if extra.get("by") == "이름":
                n["name"] = 1; note += " · 이름으로 찾음(페이지에 품번 있음)" if prod.get("code_in_page") else " · 품번이 없어 이름으로 찾음"
            log(f"  {key}: {note}" + (f" · 할인 중 {o['sp']:,g}({(o['sp'] / o['p'] - 1) * 100:+.0f}%)" if o.get("sp") else ""))
            return {"o": o, "fop": ("pop",), "hop": hop, "n": n, "b": (1, 0)}
        # v1.12 묶음 동시 받기 — 묶음마다 값을 차례대로 받아 결과(res)에 넣고, 다 끝나면 PRODUCTS 순서로 합침(예전과 같은 파일·알림)
        res, rlock, closed, errs, took = {}, threading.Lock(), [False], [], {}
        def run_lane(ln):   # 다 받으면 True · 시간 초과로 멈추면 False
            c = _ctx()
            for prod in ln["prods"]:
                pi = prev.get(prod["id"]) or {}
                for cc in ccs(prod):
                    if _STOP.is_set():
                        return False
                    c.buf = []
                    try:
                        out = _value(prod, cc, pi)
                    finally:
                        lines, c.buf = c.buf, None
                    with rlock:
                        if closed[0]:
                            return False
                        res[f"{prod['id']} {cc}"] = out
                        _out(lines)   # 값 하나의 줄은 한꺼번에(묶음끼리 섞이지 않게)
            return True
        def worker(q):
            while True:
                with rlock:
                    if not q or closed[0] or _STOP.is_set():
                        return
                    ln = q.pop(0)
                c = _TL.c = _Ctx(); s = time.time()   # 묶음마다 새 세션·간격 시계
                try:
                    if run_lane(ln):
                        took[ln["name"]] = time.time() - s
                except Exception:   # 예상 못 한 오류 — 다른 묶음도 멈추고 저장하지 않음(예전처럼 실행 실패)
                    errs.append((ln["name"], traceback.format_exc())); _STOP.set()
                finally:
                    c.sess.close(); _TL.c = None
        lanes, k = build_lanes(PRODUCTS), _lanes_n()
        _PACE.clear(); _PACE.update(pace_map(PRODUCTS)); _STOP.clear(); cpu0 = time.process_time()
        if k <= 1:   # 예전처럼 차례대로(한 세션 · 모든 요청이 한 줄로 GAP)
            for ln in lanes:
                s = time.time(); run_lane(ln); took[ln["name"]] = time.time() - s
        else:
            q = sorted(lanes, key=lambda x: -x["est"])   # 긴 묶음부터
            ths = [threading.Thread(target=worker, args=(q,), daemon=True) for _ in range(min(k, len(lanes)))]
            for th in ths:
                th.start()
            for th in ths:   # 묶음이 걸려도 단계 제한(15분) 전에 저장하도록 TIME_LIMIT + LANE_GRACE까지만 기다림
                th.join(max(0.0, t0 + TIME_LIMIT + LANE_GRACE - time.time()))
            with rlock:
                closed[0] = True   # 이 뒤에 끝나는 값은 받지 않음
            _STOP.set()
            if errs:
                for name, tb in errs:
                    log(f"해외 정가: {name} 묶음 오류 — 저장 안 함\n{tb.rstrip()}")
                raise RuntimeError(f"해외 정가 묶음 오류({', '.join(n for n, _ in errs)})")
            stuck = [ln["name"] for ln in lanes if ln["name"] not in took]
            if stuck:
                log(f"[WARN] 해외 정가: {', '.join(stuck)} 묶음이 {TIME_LIMIT + LANE_GRACE}초 안에 안 끝남 — 남은 값은 이전 값(내일 다시)")
        for prod in PRODUCTS:   # PRODUCTS 순서로 합침
            pi = prev.get(prod["id"]) or {}
            m, b = {}, bt.setdefault(prod["brand"], [0, 0])
            for cc in ccs(prod):
                key = f"{prod['id']} {cc}"
                out = res.get(key)
                if out is None:   # 묶음이 시간 안에 안 끝나 못 받은 값 — 시간 초과와 같게(이미 받은 값·한도 미룸은 예전 차례대로)
                    out = _value(prod, cc, pi, cut=True)
                if out.get("o"):
                    m[cc] = out["o"]
                fop, hop = out.get("fop"), out.get("hop")
                if fop and fop[0] == "pop":
                    failed.pop(key, None)
                elif fop:
                    failed[key] = fop[1]
                if hop:
                    htry[key] = hop[1]
                cnt.update(out.get("n") or {})
                db, df = out.get("b") or (0, 0); b[0] += db; b[1] += df
            items.append({"id": prod["id"], "brand": prod["brand"], "name": prod["name"], "code": prod["code"], "m": m,
                          **({"cc_code": prod["cc_code"]} if prod.get("cc_code") else {})})
        n_try, n_fail, n_cut, n_hold, n_name, n_defer, n_due_defer = (cnt[x] for x in ("try", "fail", "cut", "hold", "name", "defer", "due_defer"))
        ok = n_try - n_fail
        whole = [br for br, (n, f) in bt.items() if n and f == n]
        half = bool(n_try and n_fail * 2 > n_try)
        # v1.3 전체 받기는 잘 끝났는데 몇 값만 못 받은 날(사이트가 중간에 막음·연결 끊김) → 다음 날 그 값만 한 번 더(조용한 다시 받기 —
        # 또 못 받아도 알림 없이 다음 주에 · 21일 기준은 그대로). 전체 받기가 잘 끝났으면 받은 날(fetched) = 받으러 간 날(attempt)
        quiet = mode == "retry" and bool(last) and last >= (att or "")   # v1.9 이번 주기에 잘 끝난 실행이 있으면 그 뒤 다시 받기는 조용히(미룬 값으로 다시 받기가 길어져도 매일 알림 안 냄)
        ok_run = not (half or whole or n_cut) and not quiet
        again = (not ok_run and not quiet) or (mode == "full" and (n_fail > 0 or n_defer > 0)) or n_due_defer > 0   # v1.8·v1.9 미룬 값(아직 다시 받아 보지 않은 값)은 다음 날 다시 받기로
        log(f"해외 정가: {len(PRODUCTS)}개 상품 · 받음 {ok}/{n_try} · {time.time() - t0:.0f}초"
            + (f" · 크게 바뀜 {n_hold}건 다음 확인" if n_hold else "") + (f" · 이름으로 찾음 {n_name}건" if n_name else "")
            + (f" · 시간 초과로 {n_cut}건 못 받음" if n_cut else "")
            + (f" · 사이트 요청 한도로 {n_defer}건은 {'다음 실행에서' if again else '다음 주에'}" if n_defer else ""))
        log(f"해외 정가 묶음 {len(lanes)}개 · 동시 {min(k, len(lanes))}: "   # v1.12 가장 긴 묶음 = 전체 받기 시간의 기준
            + " · ".join(f"{ln['name']} {took[ln['name']]:.0f}초({ln['n']})" if ln["name"] in took else f"{ln['name']} 안 끝남({ln['n']})"
                         for ln in sorted(lanes, key=lambda x: -took.get(x["name"], 1e9)))
            + f" · CPU {time.process_time() - cpu0:.0f}초")
        if mode == "full":
            if half:
                soft_fail(f"해외 정가 절반 넘게 못 받음({n_fail}/{n_try}) — 이전 값 유지, 내일 다시")
            elif whole:   # 첫날은 알림 없이 다음 날 다시(한 번 끊긴 것일 수 있음)
                log(f"해외 정가: {', '.join(whole)} 값을 하나도 못 받음 — 내일 다시")
            elif n_fail:
                log(f"해외 정가: {n_fail}건 못 받음 — 내일 그 값만 한 번 더")
        elif (half or whole) and not quiet:
            soft_fail(f"해외 정가 다시 받기도 못 받음({n_fail}/{n_try}" + (f" · {', '.join(whole)} 전부" if whole else "")
                      + ") — 이전 값 유지, 내일 다시")
        elif quiet and n_fail:
            log(f"해외 정가: 다시 받기에서도 {n_fail}건 못 받음 — 다음 주 받을 때 다시")
        if n_cut:
            log(f"[WARN] 해외 정가: 시간 초과({TIME_LIMIT}초)로 {n_cut}건 못 받음 — 내일 다시")
    # v1.19 수집을 멈춘 사이트(PAUSED) 표시를 지금 설정으로 다시 매김(받지 않은 날도 · PAUSED에서 빼면 표시도 지움)
    byid = {p["id"]: p for p in PRODUCTS}
    n_pause = 0
    for it in items:
        prod = byid.get(it.get("id"))
        for cc, o in (it.get("m") or {}).items():
            if not isinstance(o, dict):
                continue
            pz = paused_of(prod, cc) if prod else None
            if pz:
                o["paused"] = pz["why"]; n_pause += 1
                o.setdefault("stale_since", o.get("obs_date") or o.get("seen") or td)   # 받지 않은 날(주 1회 건너뜀)에도 화면 'm/d 값' 날짜가 비지 않게
            else:
                o.pop("paused", None)
    failed = {k: f for k, f in failed.items() if not (byid.get(f.get("id")) and paused_of(byid[f["id"]], f.get("cc")))}   # 멈춘 사이트의 값 없음 기록은 지움
    if n_pause:
        log(f"해외 정가: 수집 멈춤 {n_pause}건 — " + " · ".join(f"{h} {v['why']}({v['since'][5:]}부터)" for h, v in PAUSED.items()) + " · 이전 값 그대로(알림 안 함)")
    # 오래 멈춘 값(21일 넘게 이전 값·값 없음) 알림 — v1.19 수집을 멈춘 사이트 값은 뺌
    stale = [f"{it['brand']} {it['name']} {cc}" for it in items for cc, o in it.get("m", {}).items()
             if isinstance(o, dict) and o.get("stale_since") and not o.get("paused") and _days(o["stale_since"]) > STALE_ALERT]
    stale += [f"{f.get('brand', '')} {f.get('name', '')} {f['cc']}(값 없음)" for f in failed.values() if _days(f["since"]) > STALE_ALERT]
    if stale:
        soft_fail(f"해외 정가 {len(stale)}건이 {STALE_ALERT}일 넘게 이전 값·값 없음: " + ", ".join(stale[:6]))
    cat_of = {p["id"]: p["cat"] for p in PRODUCTS}
    for it in items:   # v1.23 분류는 받지 않는 날도 지금 PRODUCTS 것으로(화면 착지 무게·관세)
        it["cat"] = cat_of.get(it.get("id"))
    out = {"generated_at": now.strftime("%Y-%m-%d %H:%M KST"),
           "fetched": td if ok_run else last,                       # 받은 날 — 잘 끝난 실행만
           "attempt": td if mode == "full" else att,                # 전체를 받으러 간 날 — 다음 주 받을 날의 기준
           "cfg": cfg if mode else old.get("cfg"),
           "status": "ok" if not stale else "kept", "items": items, "failed": list(failed.values()), "host_try": htry,
           "note": "브랜드 공식몰 정가(할인 전) · 나이키는 상품 정보 fullPrice(두바이는 공식몰 페이지) · 미국은 판매세 별도, 그 밖은 부가세 포함(두바이 5%)"}
    if again:
        out["tried"] = td                                           # 못 받은 값이 남음 — 다음 날 그 값만 다시
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    log(f"saved {OUT} ({sum(len(it['m']) for it in items)}개 값" + (f" · 값 없음 {len(failed)}건" if failed else "") + ")")


if __name__ == "__main__":
    main()

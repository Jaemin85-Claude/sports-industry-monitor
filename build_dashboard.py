# -*- coding: utf-8 -*-
"""
sports-industry-monitor — 단일 HTML 대시보드 빌드
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

TEMPLATE = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, viewport-fit=cover">
<title>스포츠 산업 모니터</title>
<style>
:root{
  --bg:#f4f6fa;--card:#ffffff;--line:#dde3ee;--tx:#1c2433;
  --sub:#5f6b80;--pos:#0e9f4f;--neg:#d92d2d;--accent:#0043FF;
  --accent-prev:#a8bdd6;--barbg:#e8edf5;
  /* 타이포 스케일 (v18) — 이 6개만 사용 */
  --fs-2xs:10px;   /* 태그·배지·셀 아래 기준시점 */
  --fs-xs:11px;    /* 메타·안내문·출처 */
  --fs-sm:12px;    /* 표·바·칩·헤더 보조 */
  --fs-base:13px;  /* 본문·카드 내용·뉴스 */
  --fs-lg:15px;    /* 핵심 수치·셀렉트 */
  --fs-xl:17px;    /* 제목·상세 헤더 */
}
[data-theme="dark"]{
  --bg:#0f1420;--card:#1a2233;--line:#2a3550;--tx:#e8ecf4;--sub:#8b96ad;
  --pos:#3ddc84;--neg:#ff6b6b;--accent:#4d9fff;--accent-prev:#3a4a68;--barbg:#0c101a;
}
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html,body{height:100%}
body{background:var(--bg);color:var(--tx);font-family:-apple-system,'Apple SD Gothic Neo','Malgun Gothic',sans-serif;font-size:var(--fs-base);line-height:1.45;overflow:hidden}
.app{display:flex;flex-direction:column;height:100vh;height:100dvh}
.content{flex:1;overflow-y:auto;overflow-x:hidden;-webkit-overflow-scrolling:touch}
header{flex:none;padding:12px 16px;border-bottom:1px solid var(--line);display:flex;align-items:flex-start;background:var(--card)}
header h1{font-size:var(--fs-xl);font-weight:700}
header .sub{color:var(--sub);font-size:var(--fs-xs);margin-top:4px}
#themeBtn{margin-left:auto;background:var(--card);border:1px solid var(--line);color:var(--tx);
border-radius:10px;padding:8px 12px;font-size:var(--fs-lg);cursor:pointer}
.tabs{display:flex;flex:none;border-top:1px solid var(--line);background:var(--card);
padding-bottom:env(safe-area-inset-bottom,0px)}
.tab{flex:1;text-align:center;padding:7px 0 6px;color:var(--sub);font-size:var(--fs-2xs);cursor:pointer;display:flex;flex-direction:column;align-items:center;gap:2px;line-height:1.2}
.tab .ic{font-size:19px;line-height:1}
.tab.on{color:var(--accent);font-weight:600}
@media(min-width:760px){.tabs{justify-content:center}.tab{flex:0 0 120px}}
.pane{display:none;padding:12px}
.pane.on{display:block}
/* 표 */
table{width:100%;border-collapse:collapse;font-size:var(--fs-sm)}
th{color:var(--sub);font-weight:500;padding:8px 4px;text-align:right;border-bottom:1px solid var(--line);font-size:var(--fs-sm)}
th:first-child,td:first-child{text-align:left}
td{padding:9px 4px;text-align:right;border-bottom:1px solid var(--line)}
tr.grp td{color:var(--sub);font-size:var(--fs-sm);padding:14px 4px 4px;border-bottom:1px solid var(--line)}
tr.grp td b{color:var(--tx);font-size:var(--fs-sm)}
tr.grp-kr td{background:var(--barbg);border-radius:6px}
tr.subrow td{font-size:var(--fs-xs);color:var(--sub)}
tr.subrow td:first-child{padding-left:26px}
tr.mrow{cursor:pointer}
tr.mrow.open td{border-bottom:none}
tr.refrow{display:none}
tr.refrow.open{display:table-row}
tr.refrow td{font-size:var(--fs-2xs);color:var(--sub);padding:2px 4px 8px;text-align:left;border-bottom:1px solid var(--line)}
.pos{color:var(--pos)}.neg{color:var(--neg)}.na{color:var(--sub)}
.nm{font-weight:600;white-space:nowrap}
.rev-main{font-weight:600}
.ref{font-size:var(--fs-2xs);color:var(--sub);font-weight:400;margin-top:2px}
.flag{font-size:var(--fs-base);margin-right:3px}
.logo{width:18px;height:18px;border-radius:4px;vertical-align:-4px;margin-right:6px;background:#fff;border:1px solid var(--line);object-fit:contain}
.lg{display:inline-flex;align-items:center;vertical-align:middle;margin-right:6px}
.lg .logo,.lg .logo-lg{margin-right:0;vertical-align:baseline}
.lgfb{display:inline-flex;align-items:center;justify-content:center;width:18px;height:18px;border-radius:4px;background:var(--accent);color:#fff;font-size:var(--fs-2xs);font-weight:700;font-style:normal}
.lgfb-lg{width:28px;height:28px;border-radius:6px;font-size:var(--fs-base)}
.logo-lg{width:28px;height:28px;border-radius:6px;vertical-align:-8px;margin-right:8px;background:#fff;border:1px solid var(--line);object-fit:contain}
/* 카드 */
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px;margin-bottom:12px}
.card h3{font-size:var(--fs-base);color:var(--sub);margin-bottom:10px;font-weight:500}
.det-head{font-size:var(--fs-xl);font-weight:700;margin-bottom:12px}
.det-head .tk{font-size:var(--fs-sm);color:var(--sub);font-weight:400}
.tag{display:inline-block;font-size:var(--fs-2xs);color:var(--accent);border:1px solid var(--accent);
border-radius:6px;padding:1px 6px;margin-left:6px;vertical-align:1px;font-weight:400}
.tag2{display:inline-block;font-size:var(--fs-2xs);color:var(--sub);border:1px solid var(--sub);
border-radius:6px;padding:0 5px;margin-left:4px;font-weight:400}
select{width:100%;padding:12px;background:var(--card);color:var(--tx);border:1px solid var(--line);border-radius:10px;font-size:var(--fs-lg);margin-bottom:12px}
/* 바 */
.bar-row{display:flex;align-items:center;margin-bottom:8px;font-size:var(--fs-sm)}
.bar-row .lb{width:72px;color:var(--sub);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;flex-shrink:0;cursor:pointer}
.bar-row .lb.open{width:auto;max-width:60%;white-space:normal;overflow:visible;word-break:break-word;padding-right:6px}
.bar-wrap{flex:1;background:var(--barbg);border-radius:4px;height:22px;position:relative;min-width:60px}
.bar{height:100%;border-radius:4px;background:var(--accent);opacity:.85}
.bar-val{position:absolute;right:6px;top:0;line-height:22px;font-size:var(--fs-xs);color:var(--tx)}
.pair{margin-bottom:14px}
.pair .pname{font-size:var(--fs-sm);font-weight:600;margin-bottom:4px;cursor:pointer;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.pair .pname.open{white-space:normal;overflow:visible}
.prow{display:flex;align-items:center;margin-bottom:3px;font-size:var(--fs-xs)}
.prow .yr{width:38px;color:var(--sub);font-size:var(--fs-2xs);flex-shrink:0}
.prow .pw{flex:1;background:var(--barbg);border-radius:4px;height:18px;position:relative;min-width:50px}
.prow .pb{height:100%;border-radius:4px}
.pb.now{background:var(--accent);opacity:.9}
.pb.prev{background:var(--accent-prev)}
.prow .pv{position:absolute;right:6px;top:0;line-height:18px;font-size:var(--fs-2xs);color:var(--tx);white-space:nowrap}
/* 키-값 */
.kv{display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid var(--line);font-size:var(--fs-base)}
.kv:last-child{border-bottom:none}
.kv .k{color:var(--sub)}
.note{color:var(--sub);font-size:var(--fs-xs);margin-top:10px;line-height:1.6}
.src{color:var(--sub);font-size:var(--fs-2xs);margin-top:8px;word-break:break-all}
/* 캘린더 */
.cal-item{display:flex;align-items:center;padding:12px;background:var(--card);border:1px solid var(--line);border-radius:10px;margin-bottom:8px;font-size:var(--fs-base)}
.cal-item .dn{width:56px;font-weight:700}
.cal-item .dt{margin-left:auto;color:var(--sub)}
.hot{color:var(--neg)}
/* v27 한국 시장 신호 · 수집 상태 */
.ksig{padding:8px 0;border-bottom:1px solid var(--line)}
.ksig:last-of-type{border-bottom:none}
.ksig .kh{display:flex;justify-content:space-between;align-items:center;font-size:var(--fs-xs);color:var(--sub)}
.ksig .kb{display:flex;justify-content:space-between;align-items:baseline;gap:8px;margin-top:3px;font-size:var(--fs-base)}
.ksig .kb .d{min-width:0;overflow-wrap:anywhere}
.ksig .kb .v{flex:none;white-space:nowrap;font-weight:600}
.ksig .ks{font-size:var(--fs-xs);color:var(--sub);margin-top:2px}
.warnbar{background:color-mix(in srgb,var(--neg) 10%,var(--card));border:1px solid var(--neg);border-radius:10px;padding:8px 12px;font-size:var(--fs-sm);margin-bottom:10px;cursor:pointer}
#statusTbl td,#statusTbl th{white-space:nowrap;padding:7px 4px}
#statusTbl td:first-child{white-space:normal}
.st-ok{color:var(--pos);font-weight:600}.st-late{color:var(--neg);font-weight:600}
/* v28 소싱 기회 지도 */
.src-wrap{display:grid;gap:10px;grid-template-columns:minmax(0,1fr);grid-template-areas:"seg" "map" "regs" "btns"}
.src-seg{grid-area:seg}.src-mapbox{grid-area:map}.src-regs{grid-area:regs}.src-btns{grid-area:btns}
.seg2{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:6px}
.seg2 button{min-height:40px;border-radius:10px;border:1px solid var(--line);background:var(--card);color:var(--tx);font-size:var(--fs-sm);font-weight:600;cursor:pointer;font-family:inherit}
.seg2 button.on{background:var(--accent);border-color:var(--accent);color:#fff}
.src-desc{font-size:var(--fs-xs);color:var(--sub);margin-top:6px;line-height:1.5}
.src-map{position:relative}
.src-svg{width:100%;height:auto;display:block;border-radius:10px}
.mp-sea{fill:#f2f5fa}.mp-other{fill:#dde2ea;stroke:var(--card);stroke-width:.25}
.mp-reg{stroke:var(--card);stroke-width:.25}
.mp-click{cursor:pointer;transition:opacity .12s}.mp-click:hover{opacity:.78}
.mp-flow{fill:none;stroke:#E8590C;stroke-width:.7;stroke-dasharray:2 1.4}
.mp-kr{fill:#E8590C;stroke:#E8590C;stroke-width:.8}
.mp-lbl{font-size:6.5px;font-weight:700;fill:#8A3B0A;stroke:var(--card);stroke-width:1.6;paint-order:stroke}
[data-theme="dark"] .mp-sea{fill:#121a2a}[data-theme="dark"] .mp-other{fill:#2b3650}[data-theme="dark"] .mp-lbl{fill:#ffb27a}
.src-cl{position:absolute;transform:translate(-50%,-50%);display:flex;flex-direction:column;align-items:center;gap:3px;background:transparent;border:0;padding:4px;min-width:44px;min-height:44px;cursor:pointer;font-family:inherit}
.src-cl .bs{display:flex;align-items:center}
.src-bd{width:26px;height:26px;border-radius:13px;background:#fff;border:2px solid;display:inline-flex;align-items:center;justify-content:center;overflow:hidden;box-sizing:border-box;flex:none}
.src-bd+.src-bd{margin-left:-7px}
.src-bd img{width:16px;height:16px;object-fit:contain}
.src-bd i{font-style:normal;font-size:var(--fs-2xs);font-weight:800;color:#1c2433}
.src-bd.lg{width:34px;height:34px;border-radius:17px}.src-bd.lg img{width:20px;height:20px}
@media(max-width:480px){.src-cl .src-bd{width:22px;height:22px;border-radius:11px}.src-cl .src-bd img{width:14px;height:14px}.src-cl .src-bd+.src-bd{margin-left:-6px}.src-cl .src-more{min-width:20px;height:20px}.src-cl .src-pill{font-size:var(--fs-2xs)}}
.src-more{margin-left:-6px;min-width:24px;height:24px;padding:0 5px;border-radius:12px;background:#1c2433;color:#fff;font-size:var(--fs-2xs);font-weight:700;display:inline-flex;align-items:center;justify-content:center;box-sizing:border-box}
.src-pill{font-size:var(--fs-xs);font-weight:700;background:var(--card);border:1px solid var(--line);border-radius:999px;padding:1px 8px;color:var(--tx);white-space:nowrap}
.src-legend{display:flex;flex-wrap:wrap;gap:4px 10px;font-size:var(--fs-xs);color:var(--sub);margin-top:6px}
.src-legend span{display:inline-flex;align-items:center;gap:4px}
.src-legend i{width:11px;height:11px;border-radius:3px;display:inline-block;box-sizing:border-box}
.src-regs{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:6px}
.src-regs button{min-height:52px;border-radius:12px;border:1px solid var(--line);background:var(--card);color:var(--tx);cursor:pointer;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3px;font-family:inherit}
.src-regs b{font-size:var(--fs-base)}
.src-regs .rl{display:flex;flex-direction:column;align-items:center;gap:2px;min-width:0}
.src-regs .tops{display:none;font-size:var(--fs-xs);color:var(--sub);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:100%}
.lvchip{font-size:var(--fs-xs);font-weight:700;padding:1px 8px;border-radius:999px;white-space:nowrap}
.src-btns{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:6px}
.src-btns button{min-height:42px;border-radius:12px;border:1px solid var(--line);background:var(--card);color:var(--accent);font-size:var(--fs-sm);font-weight:600;cursor:pointer;font-family:inherit}
/* PC: 지도 왼쪽 · 오른쪽 열이 지도 높이를 채움(빈 공간 없음) — 기본 규칙 뒤에 둬야 적용됨 */
@media(min-width:760px){.src-wrap{grid-template-columns:minmax(0,1.2fr) minmax(0,1fr);grid-template-rows:auto 1fr auto;grid-template-areas:"map seg" "map regs" "map btns";align-items:stretch}
  .src-regs{grid-template-columns:minmax(0,1fr);grid-auto-rows:1fr}
  .src-regs button{flex-direction:row;justify-content:space-between;padding:0 14px}
  .src-regs .rl{align-items:flex-start}.src-regs .tops{display:block}}
/* 하단 패널 */
.sheet{position:fixed;top:0;right:0;bottom:0;left:0;z-index:60;display:none}
.sheet.on{display:block}
.sh-bd{position:absolute;top:0;right:0;bottom:0;left:0;width:100%;height:100%;background:rgba(10,14,22,.45);border:0;cursor:pointer}
.sh-pn{position:absolute;left:0;right:0;bottom:0;max-width:760px;margin:0 auto;max-height:80vh;overflow-y:auto;background:var(--card);border-radius:16px 16px 0 0;padding:8px 14px calc(18px + env(safe-area-inset-bottom,0px));box-sizing:border-box}
.sh-grip{width:36px;height:4px;border-radius:2px;background:var(--line);margin:2px auto 8px}
.sh-hd{display:flex;justify-content:space-between;align-items:center;gap:8px}
.sh-tt{display:flex;align-items:center;gap:8px;font-size:var(--fs-lg);font-weight:700;min-width:0}
.sh-x{width:44px;height:44px;border:0;background:transparent;color:var(--sub);font-size:var(--fs-xl);cursor:pointer}
.sh-warn{font-size:var(--fs-sm);line-height:1.5;background:#fff4ec;color:#7a3208;border-radius:8px;padding:8px 10px;margin:4px 0}
.sh-row{display:flex;gap:10px;padding:10px 0;border-bottom:1px solid var(--line);cursor:pointer}
.sh-row .bx{flex:1;min-width:0;display:flex;flex-direction:column;gap:2px}
.sh-row .t1{display:flex;justify-content:space-between;align-items:center;gap:8px;font-size:var(--fs-base);font-weight:600}
.sh-row .t2{font-size:var(--fs-base);color:var(--tx)}
.sh-row .t3{font-size:var(--fs-xs);color:var(--sub)}
.sh-sub{font-size:var(--fs-sm);font-weight:700;color:var(--tx);margin:14px 0 2px;display:flex;flex-wrap:wrap;gap:2px 6px;align-items:baseline}
.sh-sub span{font-size:var(--fs-xs);font-weight:400;color:var(--sub)}
.sh-empty{font-size:var(--fs-sm);color:var(--sub);padding:8px 0;border-bottom:1px solid var(--line)}
.sh-fx{padding:9px 0;border-bottom:1px solid var(--line)}
.sh-fx .t1{display:flex;justify-content:space-between;align-items:baseline;gap:8px;font-size:var(--fs-base)}
.sh-fx .t3{font-size:var(--fs-xs);color:var(--sub);margin-top:2px}
#srcTbl{table-layout:fixed}
#srcTbl th:first-child,#srcTbl td:first-child{width:30%;text-align:left}
#srcTbl th,#srcTbl td{text-align:center;padding:6px 3px}
#srcTbl td .cv{border-radius:8px;padding:4px 2px;font-weight:700;font-size:var(--fs-sm);line-height:1.25;box-sizing:border-box}
#srcTbl td .cv small{display:block;font-size:var(--fs-2xs);font-weight:500}
.sh-mt p{font-size:var(--fs-base);line-height:1.55;margin:2px 0 10px}.sh-mt b{font-size:var(--fs-base)}
.prow .pv{background:color-mix(in srgb,var(--card) 82%,transparent);border-radius:4px;padding:0 4px;right:3px}
.cnline{font-size:var(--fs-xs);color:var(--sub);margin:2px 0 0 38px}
/* 표 줄바꿈 금지 — 표가 넓으면 표만 가로 스크롤 */
.tblwrap{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:0 -4px}
table.nowrap th,table.nowrap td{white-space:nowrap;padding-left:3px;padding-right:3px}
table.nowrap th{font-size:var(--fs-2xs)}
#detBody .card table th,#detBody .card table td{white-space:nowrap}
#krBody .krtbl table th,#krBody .krtbl table td{white-space:nowrap}
.card.flash{outline:2px solid var(--accent);transition:outline .3s}
/* A안 — 종합 */
.kpis{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:6px;margin-bottom:10px}
.kpi{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:10px 4px;text-align:center;cursor:pointer;min-width:0;overflow:hidden}
.kpi .l{font-size:var(--fs-xs);color:var(--sub);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.kpi .v{font-size:var(--fs-lg);font-weight:700;margin:2px 0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.kpi .s{font-size:var(--fs-2xs);color:var(--sub);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
@media(min-width:480px){.kpi .v{font-size:var(--fs-xl)}}
.hgrid{display:grid;grid-template-columns:minmax(0,1fr);gap:10px}
.hgrid>.card{min-width:0}
@media(min-width:760px){.hgrid{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}.span2{grid-column:1/3}}
.card h3 .go{margin-left:auto;color:var(--accent);font-size:var(--fs-sm);cursor:pointer;font-weight:500}
.rk{display:flex;justify-content:space-between;align-items:center;gap:8px;padding:6px 0;border-bottom:1px solid var(--line);font-size:var(--fs-base);cursor:pointer;min-width:0}
.rk>span:first-child{min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.rk>span:last-child,.rk>b{flex:none;white-space:nowrap}
.rk:last-child{border-bottom:none}
.rk .g{font-size:var(--fs-2xs);color:var(--sub);margin-left:4px}
/* A안 — 기업 */
.search{width:100%;padding:9px 12px;border:1px solid var(--line);border-radius:10px;font-size:var(--fs-base);margin-bottom:8px;background:var(--card);color:var(--tx)}
#coTbl th{white-space:nowrap;font-size:var(--fs-2xs);padding:7px 3px}
#coTbl td{white-space:nowrap;padding:9px 3px}
#coTbl tr.cx td{white-space:normal;overflow-wrap:anywhere;max-width:0}
.mini div{white-space:normal;overflow-wrap:anywhere}
@media(max-width:480px){#coTbl .mini{grid-template-columns:1fr}}
tr.co{cursor:pointer}tr.co td:first-child{font-weight:600;max-width:150px;overflow:hidden;text-overflow:ellipsis}
tr.co td:first-child .lg{vertical-align:-4px}
@media(max-width:400px){tr.co td:first-child{max-width:132px}}
tr.cx td{background:var(--barbg);padding:10px 8px;text-align:left}
.mini{display:grid;grid-template-columns:1fr 1fr;gap:6px 14px;font-size:var(--fs-sm)}
.mini b{font-weight:600}
.back{color:var(--accent);font-size:var(--fs-base);cursor:pointer;margin-bottom:10px;font-weight:600}
/* A안 — 캘린더 */
.cal{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:10px}
.cal h3{font-size:var(--fs-base);color:var(--sub);font-weight:500;margin-bottom:6px}
.cgrid{display:grid;grid-template-columns:repeat(7,1fr);gap:2px}
.cgrid .wd{font-size:var(--fs-2xs);color:var(--sub);text-align:center;padding:2px 0}
.cd{min-height:46px;border-radius:6px;padding:3px 3px;font-size:var(--fs-2xs);border:1px solid transparent}
.cd .dn{color:var(--sub);text-align:right}
.cd.has{background:var(--barbg);cursor:pointer}
.cd.today{border-color:var(--accent)}
.cd .ev{font-size:var(--fs-2xs);line-height:1.25;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;color:var(--tx)}
.cd.sel{outline:2px solid var(--accent)}
.calday{font-size:var(--fs-sm);margin-top:8px;color:var(--sub)}
.cl{display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid var(--line);font-size:var(--fs-base)}
.cl:last-child{border-bottom:none}
/* 뉴스 */
.chips{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:12px}
.chip{font-size:var(--fs-sm);padding:6px 10px;border-radius:14px;border:1px solid var(--line);background:var(--card);color:var(--sub);cursor:pointer;white-space:nowrap}
.chip.on{color:#fff;background:var(--accent);border-color:var(--accent)}
.chip.sep{border:none;background:transparent;color:var(--sub);padding:6px 2px;cursor:default}
.newbadge{display:inline-block;font-size:var(--fs-2xs);font-weight:700;color:#fff;background:var(--neg);border-radius:5px;padding:1px 5px;margin-right:5px;vertical-align:1px}
.ndate{font-size:var(--fs-sm);color:var(--sub);margin:14px 0 6px;font-weight:600}
.nitem{padding:10px 0;border-bottom:1px solid var(--line)}
.nitem:last-child{border-bottom:none}
.nitem .nsum{font-size:var(--fs-base);line-height:1.5}
.nitem .nsum a{color:var(--tx);text-decoration:none}
.nitem .nmeta{font-size:var(--fs-xs);color:var(--sub);margin-top:3px}
.ntag{display:inline-block;font-size:var(--fs-2xs);color:var(--accent);border:1px solid var(--accent);border-radius:6px;padding:0 5px;margin-right:5px}
/* 국내(KOSIS)·추이 카드 */
.krcard{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 14px;margin-bottom:10px;cursor:pointer}
.krhead{display:flex;align-items:baseline;gap:8px}
.krname{font-size:var(--fs-base);font-weight:600}
.krval{margin-left:auto;font-size:var(--fs-lg);font-weight:700}
.kryoy{font-size:var(--fs-sm);font-weight:600}
.krmeta{font-size:var(--fs-xs);color:var(--sub);margin-top:2px}
.krtbl{display:none;margin-top:10px}
.krtbl.open{display:block}
.trend .krname{font-weight:500}
.trend .krval{font-size:var(--fs-base)}
/* v30 국내 수요 — 판매 vs 검색 교차 그래프 · 네이버 검색 관심도 */
:root{--s-naver:#0043FF;--s-shoe:#D9480F;--s-apparel:#6E56CF;--up:#0043FF;--down:#D9480F;--on-sig:#ffffff}
[data-theme="dark"]{--s-naver:#4d9fff;--s-shoe:#ff8a4c;--s-apparel:#a897ff;--up:#4d9fff;--down:#ff8a4c;--on-sig:#0f1420}
.xc-legend{display:flex;flex-wrap:wrap;gap:6px;margin:8px 0}
.xc-leg{display:inline-flex;align-items:center;gap:6px;border:1px solid var(--line);border-radius:999px;padding:4px 10px;font-size:var(--fs-sm);background:var(--card);color:var(--tx);cursor:pointer;font-family:inherit;min-height:32px}
.xc-leg i{width:14px;height:3px;border-radius:2px;display:inline-block}
.xc-leg.off{opacity:.4}
.xc-leg:focus-visible,.nv-row:focus-visible,.nv-more:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.xc-wrap{position:relative}
.xc-svg{width:100%;height:auto;display:block;touch-action:pan-y}
.xc-tip{position:absolute;top:2px;pointer-events:none;background:var(--card);color:var(--tx);border:1px solid var(--line);border-radius:8px;padding:6px 8px;font-size:var(--fs-xs);line-height:1.55;white-space:nowrap;font-variant-numeric:tabular-nums}
.nv-sum{background:var(--barbg);border-radius:10px;padding:10px 12px;font-size:var(--fs-sm);line-height:1.6;margin-bottom:8px}
/* 수입 브랜드 유통사 비교 (v30.4) */
.pg-badge{display:inline-block;padding:1px 6px;border-radius:999px;background:var(--accent);color:#fff;font-size:var(--fs-2xs);font-weight:700;line-height:1.5;margin:1px 2px 1px 0}
.pg-rk{display:block;font-size:var(--fs-2xs);color:var(--sub)}
.pg-bars{display:flex;flex-direction:column;gap:6px}
.pg-row{display:grid;grid-template-columns:96px minmax(0,1fr) 56px;align-items:center;gap:8px;cursor:pointer;font-size:var(--fs-sm);min-height:24px}
.pg-nm{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;color:var(--sub)}
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
.nv-row{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:3px 10px;padding:9px 0;border-top:1px solid var(--line);cursor:pointer}
.nv-row.low{opacity:.55}
.nv-nm{display:flex;align-items:center;gap:6px;min-width:0;font-weight:700;font-size:var(--fs-base)}
.nv-nm span{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.nv-low{font-style:normal;font-size:var(--fs-2xs);color:var(--sub);border:1px solid var(--line);border-radius:6px;padding:0 5px;font-weight:500;flex:none}
.nv-pill{justify-self:end;align-self:center;border-radius:999px;padding:1px 9px;font-size:var(--fs-sm);font-weight:700;font-variant-numeric:tabular-nums;white-space:nowrap}
.nv-pill.up{background:var(--up);color:var(--on-sig)}.nv-pill.down{background:var(--down);color:var(--on-sig)}.nv-pill.mid{background:var(--barbg);color:var(--tx)}
.nv-bar{display:flex;align-items:center;gap:8px;min-width:0}
.nv-bar .tr{flex:1;height:6px;background:var(--barbg);border-radius:3px;overflow:hidden}
.nv-bar .tr i{display:block;height:100%;background:var(--sub);opacity:.55}
.nv-bar b{font-size:var(--fs-sm);min-width:34px;text-align:right;font-variant-numeric:tabular-nums}
.nv-sub{grid-column:1/-1;font-size:var(--fs-xs);color:var(--sub)}
.nv-more{width:100%;margin-top:8px;min-height:40px;border-radius:10px;border:1px solid var(--line);background:var(--card);color:var(--accent);font-weight:700;font-size:var(--fs-sm);cursor:pointer;font-family:inherit}
.nv-det+.nv-det{margin-top:12px;padding-top:12px;border-top:1px solid var(--line)}
/* v31 더보기 — 메뉴 · 환율 · 해외직구 · 수집 상태 */
.mhead{display:flex;align-items:center;gap:12px;margin:2px 0 10px}
.mhead .mback{color:var(--accent);font-size:var(--fs-sm);cursor:pointer;white-space:nowrap;padding:6px 0}
.mhead b{font-size:var(--fs-xl)}
.mhead .ms{display:block;color:var(--sub);font-size:var(--fs-2xs);font-weight:400}
.mmenu{padding:2px 12px}
.mi{display:grid;grid-template-columns:30px minmax(0,1fr) auto;gap:10px;align-items:center;padding:12px 0;border-bottom:1px solid var(--line);cursor:pointer}
.mi:last-child{border-bottom:none}
.mi .mic{font-size:20px;text-align:center}
.mi .mt{font-weight:700}
.mi .md{font-size:var(--fs-xs);color:var(--sub)}
.mi .mr{font-size:var(--fs-2xs);color:var(--sub);text-align:right;white-space:nowrap}
.mi .mr b{display:block;font-size:var(--fs-xs);color:var(--tx)}
.mbadge{display:inline-block;font-size:var(--fs-2xs);font-weight:700;border-radius:999px;padding:0 7px;line-height:1.7;color:#fff;background:var(--pos)}
.mbadge.up,.mbadge.late{background:var(--neg)}
.fxgrid{display:grid;grid-template-columns:minmax(0,1fr);gap:10px;margin-bottom:10px}
@media(min-width:760px){.fxgrid{grid-template-columns:repeat(3,minmax(0,1fr))}}
.fxc{border:1px solid var(--line);border-radius:12px;padding:12px;background:var(--card);min-width:0}
.fxc.dn{border-color:var(--pos)}.fxc.up{border-color:var(--neg)}
.fxtop{display:flex;align-items:center;gap:6px;font-size:var(--fs-sm)}
.fpill{margin-left:auto;font-size:var(--fs-2xs);font-weight:700;border-radius:999px;padding:1px 8px;line-height:1.7;white-space:nowrap}
.fpill.dn{background:var(--pos);color:#fff}.fpill.up{background:var(--neg);color:#fff}
.fpill.wait{border:1px solid var(--line);color:var(--sub);font-weight:500}
.fxv{font-size:var(--fs-lg);font-weight:700;margin-top:2px}
.fxv small{font-size:var(--fs-xs);font-weight:400;color:var(--sub);margin-left:4px}
.fxmeta{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:4px;margin-top:6px;font-size:var(--fs-sm)}
.fxmeta span{display:block;color:var(--sub);font-size:var(--fs-2xs)}
.fgauge{position:relative;height:30px;margin-top:8px}
.fg-trk{position:absolute;left:0;right:0;top:9px;height:6px;background:var(--barbg);border-radius:3px}
.fg-tk{position:absolute;top:7px;width:1px;height:10px;background:var(--line)}
.fg-tk.z{background:var(--sub);top:4px;height:16px}
.fg-seen{position:absolute;top:9px;height:6px;background:var(--accent);opacity:.3;border-radius:3px}
.fg-me{position:absolute;top:4px;width:10px;height:16px;margin-left:-5px;border-radius:3px;background:var(--tx)}
.fg-lb{position:absolute;top:19px;font-size:var(--fs-2xs);color:var(--sub);transform:translateX(-50%);white-space:nowrap}
.fxsv{display:block;width:100%;height:52px;margin-top:6px}
.fxcnt{font-size:var(--fs-2xs);color:var(--sub);margin-top:4px}
.fleg{display:flex;gap:10px;flex-wrap:wrap;font-size:var(--fs-2xs);color:var(--sub);margin:0 0 10px}
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
.fuse{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}
.fuse>div{border-radius:10px;padding:8px 10px;background:var(--barbg);min-width:0}
.fuse b{display:block;font-size:var(--fs-sm);margin-bottom:2px}
.fuse ul,.frules{margin:0;padding-left:16px;font-size:var(--fs-xs);display:flex;flex-direction:column;gap:2px}
.kpis.cbk{grid-template-columns:repeat(3,minmax(0,1fr))}
.kpis.cbk .kpi{cursor:default}
.cb-row{display:grid;grid-template-columns:62px minmax(0,1fr) 56px;gap:8px;align-items:center;font-size:var(--fs-sm);margin-bottom:8px}
.cb-row .lb{color:var(--sub);white-space:nowrap}
.cb-row .yy{text-align:right;font-size:var(--fs-xs);font-variant-numeric:tabular-nums}
.bar.cb-src{background:var(--pos);opacity:.9}
.cb-trend{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}
@media(min-width:760px){.cb-trend{grid-template-columns:repeat(4,minmax(0,1fr))}}
.cb-tr{border:1px solid var(--line);border-radius:10px;padding:6px 8px;min-width:0}
.cb-tr .h{display:flex;justify-content:space-between;gap:4px;font-size:var(--fs-xs)}
.cb-tr svg{display:block;width:100%;height:36px;margin-top:2px}
.cb-tr .ax{display:flex;justify-content:space-between;font-size:var(--fs-2xs);color:var(--sub)}
.cb-read{background:var(--barbg);border-radius:10px;padding:8px 10px;font-size:var(--fs-xs);margin-bottom:10px}
</style>
</head>
<body>
<div class="app">
<header>
  <div>
    <h1>🏭 스포츠 산업 모니터</h1>
    <div class="sub" id="gen"></div>
  </div>
  <button id="themeBtn" title="테마 전환">🌙</button>
</header>
<main class="content" id="content">
<div class="pane on" id="p-home">
  <div id="statusWarn"></div>
  <div class="kpis" id="kpis"></div>
  <div class="hgrid" id="homeBody"></div>
</div>

<div class="pane" id="p-co">
  <div id="coList">
    <input class="search" id="coSearch" placeholder="기업명 검색 (예: 나이키, 아식스)">
    <div class="chips" id="coChips"></div>
    <div class="card" style="padding:4px 8px"><table id="coTbl"></table></div>
    <div class="note">행을 누르면 핵심 지표가 펼쳐지고, "전체 상세 ▸"로 3개년·지역/채널·추이를 봅니다 · "―" = 미확인(§29-D) · 국내 법인은 연간 자료</div>
  </div>
  <div id="coDetail" style="display:none">
    <div class="back" id="coBack">◂ 기업 목록</div>
    <div id="detBody"></div>
  </div>
</div>

<div class="pane" id="p-cal">
  <div class="hgrid" id="calGrid"></div>
  <div class="card" style="margin-top:10px"><h3>90일 이내 실적 발표</h3><div id="calList"></div></div>
  <div class="note">달력의 날짜를 누르면 그 날 발표 기업이 표시됩니다 · 일정 미표시 종목은 소스 미제공(미확인)</div>
</div>

<div class="pane" id="p-news">
  <div class="chips" id="newsChips"></div>
  <div id="newsBody"></div>
  <div class="note">매일 06:30 수집 · 최근 14일 보관 · <span class="newbadge">NEW</span>=오늘 신규 · ★=중요도<br>
  실제 기사 헤드라인 기반 선별(§29-D) · 관세·환율·정책 뉴스는 제외 · 헤드라인을 누르면 원문</div>
</div>

<div class="pane" id="p-kr">
  <div id="krBody"></div>
  <div class="note">출처: KOSIS(통계청) — 서비스업동향조사·온라인쇼핑동향조사·소비자물가조사 · 월 1회 갱신<br>
  지수는 2020=100 기준 · YoY는 전년 동월 대비 · 지표를 누르면 최근 13개월 수치 표</div>
</div>

<div class="pane" id="p-more">
  <div id="moreBody"></div>
</div>

</main>
<nav class="tabs">
  <div class="tab on" data-p="home"><span class="ic">🏠</span>종합</div>
  <div class="tab" data-p="co"><span class="ic">🏢</span>기업</div>
  <div class="tab" data-p="cal"><span class="ic">📅</span>캘린더</div>
  <div class="tab" data-p="news"><span class="ic">📰</span>뉴스</div>
  <div class="tab" data-p="kr"><span class="ic">🇰🇷</span>국내</div>
  <div class="tab" data-p="more"><span class="ic">☰</span>더보기</div>
</nav>
<div class="sheet" id="sheet"></div>
</div>
<script>
const DATA = __DATA__;
const SEGS = __SEGS__;
const SEGS_IR = __SEGS_IR__;
if(SEGS_IR&&SEGS_IR.items){ SEGS.items=SEGS.items||{}; Object.entries(SEGS_IR.items).forEach(([k,v])=>{ if(v&&v.extract) SEGS.items[k]=v; }); }
const NEWS = __NEWS__;
const KR = __KR__;
const NAVER = __NAVER__;   // 네이버 데이터랩 검색 관심도(docs/naver_trend.json)
const HIST = __HIST__;
const KRD = __KRD__;
const STATUS = __STATUS__;
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
  "krd:descente_kr":"descentekorea.co.kr", "krd:nb_eland":"newbalance.co.kr", "krd:abcmart_kr":"abcmart.co.kr",
  "krd:shoemarker":"shoemarker.co.kr", "krd:musinsa":"musinsa.com", "krd:k2_kr":"k2group.co.kr",
  "krd:blackyak":"blackyak.com", "krd:nepa":"nepa.co.kr", "krd:shinsung":"shinsungtongsang.com",
  "krd:kream":"kream.co.kr", "krd:trenbe":"trenbe.com", "krd:balaan":"balaan.co.kr", "krd:mustit":"mustit.co.kr",
  "krd:rexmond":"okmall.com", "krd:hana_int":"hahamall.net", "krd:bbluein":"bblue.co.kr",
  "EL.PA":"essilorluxottica.com", "SFL.MI":"safilogroup.com", "krd:iicombined":"gentlemonster.com", "krd:luxottica_kr":"luxottica.com",
  "krd:fivespace":"adererror.com", "krd:andar":"andar.co.kr", "krd:matinkim":"matinkim.com", "krd:piecepeace":"mardimercredi.com"
};
/* ── 브랜드 본사 국가 국기 ── */
const FLAGS = {
  "NKE":"🇺🇸", "ADS.DE":"🇩🇪", "ONON":"🇨🇭", "DECK":"🇺🇸", "AS":"🇫🇮",
  "LULU":"🇨🇦", "7936.T":"🇯🇵", "BIRK":"🇩🇪", "CROX":"🇺🇸", "VFC":"🇺🇸",
  "UAA":"🇺🇸", "8022.T":"🇯🇵", "7906.T":"🇯🇵", "8111.T":"🇯🇵",
  "2020.HK":"🇨🇳", "2331.HK":"🇨🇳", "PUM.DE":"🇩🇪", "WWW":"🇺🇸",
  "COLM":"🇺🇸", "DOCS.L":"🇬🇧", "EL.PA":"🇫🇷", "SFL.MI":"🇮🇹", "DKS":"🇺🇸", "JD.L":"🇬🇧", "ASO":"🇺🇸",
  "FRAS.L":"🇬🇧", "ZAL.DE":"🇩🇪", "SBFG3.SA":"🇧🇷", "4240.SR":"🇸🇦",
  "456A.T":"🇯🇵", "0933.HK":"🇭🇰", "VULC3.SA":"🇧🇷", "LUXE":"🇩🇪", "2670.T":"🇯🇵", "6110.HK":"🇨🇳",
  "TJX":"🇺🇸", "ROST":"🇺🇸", "BURL":"🇺🇸", "CPNG":"🇰🇷"
};
const GROUPS = (DATA.group_order && DATA.group_order.length) ? DATA.group_order
  : ["글로벌 브랜드","글로벌 유통","국내 브랜드","국내 패션대기업","국내 OEM","국내 유통"];
const GROUP_ICON = {"글로벌 브랜드":"🌍","글로벌 유통":"🌍","국내 브랜드":"🇰🇷","국내 패션대기업":"🇰🇷","국내 OEM":"🇰🇷","국내 유통":"🇰🇷"};
const GROUP_NOTE = {"국내 OEM":"브랜드 오더의 선행지표","삼성물산(패션부문)":""};
const isKR = t => /\.K[SQ]$/.test(t);
const NEWS_KEY = {"FRAS.L":"frasers","ZAL.DE":"zalando","SBFG3.SA":"sbf","4240.SR":"cenomi","NKE":"nike","ADS.DE":"adidas","ONON":"on","DECK":"hoka","AS":"amer","LULU":"lululemon","7936.T":"asics",
  "BIRK":"birkenstock","CROX":"crocs","VFC":"vf","UAA":"ua","8022.T":"mizuno","7906.T":"yonex","8111.T":"goldwin",
  "2020.HK":"anta","2331.HK":"lining","PUM.DE":"puma","WWW":"saucony","COLM":"columbia","DOCS.L":"drmartens","456A.T":"humanmade","0933.HK":"clarks","DKS":"dks","JD.L":"jd","ASO":"academy",
  "krd:nike_kr":"nike","krd:adidas_kr":"adidas","krd:asics_kr":"asics","krd:puma_kr":"puma","krd:descente_kr":"descente",
  "krd:nb_eland":"newbalance"};
/* 재고일수 = 재고 ÷ 매출원가 × 365 (연간 원가 기준, 재고는 최근 잔액) */
function dioOf(inv, rev, gp, cogs){
  const c = (cogs!=null) ? cogs : ((rev!=null && gp!=null) ? rev-gp : null);
  if(inv==null || !c || c<=0) return null;
  return inv / c * 365;
}
/* ── 🇰🇷 한국 시장 신호 (v27) ── */
/* 한국이 속한 지역 찾기: 지역명에 Korea 명시 > 나이키 APLA > 아시아태평양 > Rest of World > International */
const KOREA_PAT=[[/korea/i,true],[/asia pacific & latin america|\bapla\b/i,false],
  [/asia[\s\/-]*pacific|\bapac\b|\bapma\b/i,false],[/rest of world/i,false],[/international/i,false]];
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
  let h=`<div class="card"><h3>🇰🇷 한국 시장 신호</h3>`;
  // ① 국내 법인 (DART)
  const kd=((KRD&&KRD.entities)||[]).find(e=>e.link===t);
  if(kd){
    const ys=(kd.years||[]).filter(y=>y.rev!=null), l=ys[ys.length-1], p=ys[ys.length-2];
    if(l){
      const yoy=(p&&p.rev)?(l.rev/p.rev-1)*100:null, iy=(p&&l.inv&&p.inv)?(l.inv/p.inv-1)*100:null;
      const dio=dioOf(l.inv,l.rev,null,l.cogs);
      h+=ksigRow('국내 법인','DART',`${logoImg('krd:'+kd.id,false,kd.name)}${esc(kd.name)}`,
        `매출 ${fmt(yoy,1,true)} · 재고 ${fmt(iy,1,true)}`,
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
  h+=`<div class="note">본사 지역 수치는 한국 단독이 아니라 한국이 속한 지역 합계 · 환율 제외 = 현지 통화 기준(회사 공시값) · 국내 법인은 연간(별도 재무제표)</div></div>`;
  return h;
}
/* ── 🌍 소싱 기회 지도 (v28) ── */
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
const SRC_LV={2:{bg:'#0043FF',fg:'#FFFFFF',txt:'높음',ring:'#0043FF',map:'#0043FF'},
              1:{bg:'#9DB4FF',fg:'#0B1A4A',txt:'보통',ring:'#7F9BFF',map:'#9DB4FF'},
              0:{bg:'#E6EBF7',fg:'#3A4560',txt:'낮음',ring:'#B9C4DE',map:'#CBD6F5'}};
const SRC_RNAME=[[/^europe$/i,'유럽'],[/^emea$|europe, middle east/i,'유럽·중동·아프리카'],[/emerging markets/i,'신흥시장'],
  [/asia pacific & latin america/i,'아시아·남미'],[/latin america and asia/i,'남미·아시아'],[/latin america/i,'중남미'],[/^others/i,'남미·한국 등'],
  [/japan\/south korea/i,'일본·한국'],[/^japan$/i,'일본'],[/north america/i,'북미'],[/^americas$/i,'미주'],[/^united states$/i,'미국'],
  [/^domestic$/i,'미국 내수'],[/^asia[\s\/-]*pacific$|^apac$/i,'아시아·태평양']];
const srcRegName=n=>{ for(const [re,k] of SRC_RNAME) if(re.test(n||'')) return k; return n; };
const pp=v=>(v>0?'+':'')+v.toFixed(1)+'%';
let SRC_PRESET='A', SRC_SHEET=null, SRC_CACHE=null;
function srcModel(){
  if(SRC_CACHE) return SRC_CACHE;
  const g=r=>r.cn_yoy_pct!=null?r.cn_yoy_pct:r.yoy_pct;
  const out=[];
  Object.entries(SRC_CFG).forEach(([t,cfg])=>{
    const x=DATA.items.find(i=>i.ticker===t); const s=(SEGS.items||{})[t]; const ex=s&&s.extract;
    if(!x||!ex||!ex.regions||x.inv_yoy==null) return;
    const fy=x.fy.length?x.fy[x.fy.length-1]:{}; if(fy.rev_yoy==null) return;
    const regs=ex.regions.filter(r=>g(r)!=null&&!/total|합계|corporate|global brand|converse/i.test(r.name||''));
    if(!regs.length) return;
    const vs=regs.map(g).sort((a,b)=>a-b), n=vs.length, med=n%2?vs[(n-1)/2]:(vs[n/2-1]+vs[n/2])/2;
    const P=x.inv_yoy-fy.rev_yoy, cells={};
    SRC_KEYS.forEach(k=>{
      const spec=cfg[k]; const r=spec?regs.find(z=>spec[0].test(z.name||'')):null;
      if(!r){ cells[k]=null; return; }
      const v=g(r), excess=P>=5, weak=v<0||(v<10&&v<med);
      const why=[]; if(excess) why.push(`재고 압력 ${P>0?'+':''}${P.toFixed(1)}%p`); if(weak) why.push(v<0?'지역 역성장':'지역 성장 둔화');
      cells[k]={g:v, basis:r.cn_yoy_pct!=null?'환율 제외':'보고 통화', rname:srcRegName(r.name), proxy:spec[1],
        A:(excess&&weak)?2:((excess||weak)?1:0), B:(v>=15||x.inv_yoy>=15)?2:((v>=5||x.inv_yoy>=5)?1:0), why:why.join(' · ')||'해당 없음'};
    });
    out.push({t, name:x.name, inv:x.inv_yoy, rev:fy.rev_yoy, period:(ex.period||'').split(' ended')[0], cells, kr:koreaRegion(t)});
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
    const fy=x.fy&&x.fy.length?x.fy[x.fy.length-1]:null;
    return (x.inv_yoy==null||!fy||fy.rev_yoy==null)?null:{name:x.name, d:x.inv_yoy-fy.rev_yoy}; }).filter(Boolean);
  if(!rs.length) return {pt:0, txt:'현지 유통사 자료 없음'};
  const heavy=rs.filter(r=>r.d>=5);
  if(heavy.length) return {pt:1, txt:'현지 유통 재고 무거움 '+heavy.map(r=>r.name).join('·')};
  if(rs.every(r=>r.d<=-5)) return {pt:-1, txt:'현지 유통 재고 가벼움'};
  return {pt:0, txt:'현지 유통 재고 보통'};
}
function srcFxSig(k){
  const fx=(SRC_FXMAP[k]||[]).map(c=>(DATA.fx||{})[c]).filter(f=>f&&f.chg_pct!=null);
  if(!fx.length) return {pt:0, txt:'환율 자료 없음'};
  const avg=fx.reduce((a,f)=>a+f.chg_pct,0)/fx.length, lst=fx.map(f=>`${f.name} ${pp(f.chg_pct)}`).join('·');
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
  return `<svg class="src-svg" viewBox="${W.viewBox}" role="img" aria-label="유럽·북미·일본·중동·남미 소싱 기회 지도">
    <defs><pattern id="srcHatch" width="2.6" height="2.6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="2.6" stroke="#ffffff" stroke-width="0.9"/></pattern></defs>
    <rect class="mp-sea" x="${vb[0]}" y="${vb[1]}" width="${vb[2]}" height="${vb[3]}"/>
    <path class="mp-other" d="${W.other}"/>
    ${SRC_KEYS.map(k=>`<path class="mp-reg mp-click" fill="${fill(k)}" d="${W[k]}" onclick="openSheet('${k}')"><title>${SRC_NAMES[k]} — 눌러서 브랜드 목록</title></path>`).join('')}
    ${Object.keys(SRC_EST).filter(k=>W[k]).map(k=>`<path fill="url(#srcHatch)" d="${W[k]}" pointer-events="none"/>`).join('')}
    <path class="mp-kr" d="${W.korea}"/>
    ${W.flows.map(f=>`<path class="mp-flow" d="${f}"/>`).join('')}
    <circle cx="${K[0]}" cy="${K[1]}" r="2.2" fill="#E8590C" stroke="#ffffff" stroke-width="0.6"/>
    <text class="mp-lbl" x="${(K[0]+3).toFixed(1)}" y="${(K[1]-3).toFixed(1)}">한국</text>
  </svg>`;
}
function sourcingCard(){
  if(!srcModel().length) return '';
  const W=WMAP;
  let cl='';
  if(W) SRC_KEYS.forEach(k=>{
    const list=srcRanked(k), top=list.slice(0,3), lv=SRC_LV[srcSumm(k).level];
    cl+=`<button type="button" class="src-cl" style="left:${W.anchors[k][0]};top:${W.anchors[k][1]}" onclick="openSheet('${k}')" aria-label="${SRC_NAMES[k]} 브랜드 목록 열기">
      <span class="bs">${top.map(o=>srcBadge(o.b.t,o.b.name,SRC_LV[o.lvl].ring)).join('')}${list.length>3?`<span class="src-more">+${list.length-3}</span>`:''}</span>
      <span class="src-pill">${SRC_NAMES[k]} · ${lv.txt}${SRC_EST[k]?'(추정)':''}</span></button>`;
  });
  const desc=SRC_PRESET==='A'?'재고가 매출보다 빨리 늘었고 그 지역 판매가 약하면 처분 물량이 나온다고 봅니다. 현지 유통 재고와 환율도 함께 반영합니다.'
                             :'지역 성장이 빠르거나 재고가 많이 늘면 유통 물량 자체가 커진다고 봅니다. 환율도 함께 반영합니다.';
  return `<div class="card span2" id="srcCard"><h3>🌍 소싱 기회 지도 — 유럽 · 북미 · 일본 · 중동 · 남미 <span class="tag2">공시 기반</span></h3>
  <div class="src-wrap">
    <div class="src-seg"><div class="seg2">
      <button type="button" class="${SRC_PRESET==='A'?'on':''}" onclick="setSrcPreset('A')">재고 과잉형</button>
      <button type="button" class="${SRC_PRESET==='B'?'on':''}" onclick="setSrcPreset('B')">시장 확대형</button></div>
      <div class="src-desc">${desc}</div></div>
    <div class="src-mapbox"><div class="src-map">${srcMapSvg()}${cl}</div>
      <div class="src-legend"><span><i style="background:#0043FF"></i>높음</span><span><i style="background:#9DB4FF"></i>보통</span><span><i style="background:#CBD6F5"></i>낮음</span>
      <span><i style="background:#9DB4FF;border:1px dashed #3A4560"></i>빗금 = 추정</span><span><i style="background:#E8590C;border-radius:6px"></i>판매처</span></div></div>
    <div class="src-regs">${SRC_KEYS.map(k=>{const sm=srcSumm(k), lv=SRC_LV[sm.level];
      const tops=(sm.hi.length?sm.hi:srcRanked(k)).slice(0,3).map(o=>o.b.name).join(' · ');
      return `<button type="button" onclick="openSheet('${k}')"><span class="rl"><b>${SRC_NAMES[k]}</b><span class="tops">${sm.hi.length?'기회 높음: ':'상위: '}${esc(tops)}</span></span><span class="lvchip" style="background:${lv.bg};color:${lv.fg}">${lv.txt} ${sm.hi.length}개</span></button>`;}).join('')}</div>
    <div class="src-btns"><button type="button" onclick="openSheet('matrix')">브랜드 × 지역 전체 표</button><button type="button" onclick="openSheet('method')">가정과 계산 방식</button></div>
  </div></div>`;
}
function setSrcPreset(p){ SRC_PRESET=p; const c=document.getElementById('srcCard'); if(c) c.outerHTML=sourcingCard(); if(SRC_SHEET) openSheet(SRC_SHEET); }
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
    const fy=x.fy&&x.fy.length?x.fy[x.fy.length-1]:null;
    const inv=x.inv_yoy, rev=fy?fy.rev_yoy:null; any=true;
    let chip='<span class="lvchip" style="background:var(--barbg);color:var(--sub)">미확인</span>', t3='재고 또는 매출 미공시';
    if(inv!=null&&rev!=null){ const d=inv-rev, lv=d>=5?2:(d<=-5?0:1), L=SRC_LV[lv];
      chip=`<span class="lvchip" style="background:${L.bg};color:${L.fg}">재고 ${lv===2?'무거움':(lv===0?'가벼움':'보통')}</span>`;
      t3=`재고 압력 ${d>0?'+':''}${d.toFixed(1)}%p · ${fy.end?('결산 '+ym(fy.end)):''}`; }
    h+=`<div class="sh-row" onclick="closeSheet();goDetail('${t}')">${srcBadge(t,x.name,'#C9D0DD',true)}
      <div class="bx"><div class="t1"><span>${esc(x.name)} ${flagOf(t)||''}</span>${chip}</div>
      <div class="t2">재고 ${inv!=null?pp(inv):'―'} · 매출 ${rev!=null?pp(rev):'―'}</div><div class="t3">${esc(t3)}</div></div></div>`;
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
    h+=`<div class="sh-fx"><div class="t1"><span>${esc(f.name)} <span class="na">${c==='JPY'?'100엔':c}</span></span><b>${rate}원</b></div>
      <div class="t3">${ch!=null?`1년 전보다 ${ch>0?'+':''}${ch.toFixed(1)}% · `:''}${f.dev_pct!=null?`1년 평균 대비 ${f.dev_pct>0?'+':''}${f.dev_pct.toFixed(1)}% · `:''}${verdict}${c==='USD'&&k==='middleeast'?' · 디르함·리얄은 달러에 고정':''}${f.via?' · '+esc(f.via):''} · ${esc(f.asof||'')} 기준</div></div>`; });
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
  return h+`<div class="sh-fx" style="cursor:pointer" onclick="closeSheet();goMore('cb')"><div class="t1"><span>${esc(nm)}</span><b>${cbMoney(v)}원</b></div>
    <div class="t3">${y!=null?`${y>=0?'+':''}${y.toFixed(1)}% · `:''}${cbPrd(CB.last)} · 누르면 더보기 › 해외직구</div></div>`;
}
function srcNewsHtml(k){
  let h=`<div class="sh-sub">현지 유통 뉴스 <span>최근 14일 선별</span></div>`;
  const keys=SRC_NEWSKEYS[k]||[];
  const list=((NEWS&&NEWS.items)||[]).filter(it=>it.scope==='brand'&&keys.indexOf(it.key)>=0)
    .sort((a,b)=>(b.first_seen||'').localeCompare(a.first_seen||'')||(b.importance||0)-(a.importance||0));
  const list3=newsDedupe(list,3);
  if(!list3.length) return h+`<div class="sh-empty">최근 14일 선별된 뉴스 없음</div>`;
  list3.forEach(it=>{ h+=`<div class="nitem"><div class="nsum"><a href="${it.link}" target="_blank" rel="noopener">${'★'.repeat(it.importance||1)} ${esc(it.summary||it.title)}</a></div>
    <div class="nmeta">${esc(it.label||'')} · ${esc(it.source||'')} · ${esc((it.first_seen||'').slice(5).replace('-','/'))}</div></div>`; });
  return h;
}
function openSheet(kind){
  SRC_SHEET=kind; const sh=document.getElementById('sheet');
  let title='', chip='', body='';
  if(SRC_NAMES[kind]){
    const sm=srcSumm(kind), lv=SRC_LV[sm.level];
    title=`${SRC_NAMES[kind]} 브랜드`; chip=`<span class="lvchip" style="background:${lv.bg};color:${lv.fg}">기회 ${lv.txt}</span>`;
    if(kind==='middleeast') body+=`<div class="sh-warn">중동은 대부분 브랜드가 유럽·중동·아프리카 또는 신흥시장으로 묶어 공시합니다. 그 합산값을 빌려 쓴 추정치입니다.</div>`;
    if(kind==='japan') body+=`<div class="sh-warn">일본을 따로 공시하는 곳은 아식스뿐이고, 아디다스는 일본+한국 합산입니다. 나머지는 아시아·태평양 합산값을 빌려 쓴 추정치입니다.</div>`;
    body+=`<div class="note" style="margin:2px 0 8px"><b>판정 ${lv.txt} (${sm.score}점)</b> — ${sm.parts.map(p=>`${esc(p.txt)} ${p.pt>0?'+':''}${p.pt}`).join(' · ')}</div>`;
    srcRanked(kind).forEach(o=>{ const l=SRC_LV[o.lvl], c=o.c;
      const t2=SRC_PRESET==='A'?`${c.rname} ${pp(c.g)}(${c.basis}) · 재고 ${pp(o.b.inv)} vs 매출 ${pp(o.b.rev)}`:`${c.rname} ${pp(c.g)} · 재고 ${pp(o.b.inv)}`;
      const t3=(SRC_PRESET==='A'?'근거: '+c.why:'기준: '+o.b.period)+(c.proxy&&c.proxy.indexOf('차용')>=0?' · 추정(유럽·중동·아프리카 값 차용)':(c.proxy&&kind!=='europe'?' · '+c.proxy:''));
      body+=`<div class="sh-row" onclick="closeSheet();goDetail('${o.b.t}')">${srcBadge(o.b.t,o.b.name,l.ring,true)}
        <div class="bx"><div class="t1"><span>${esc(o.b.name)}</span><span class="lvchip" style="background:${l.bg};color:${l.fg}">${l.txt}</span></div>
        <div class="t2">${esc(t2)}</div><div class="t3">${esc(t3)}</div></div></div>`; });
    body+=srcRetailHtml(kind)+srcFxHtml(kind)+srcCbHtml(kind)+srcNewsHtml(kind);
  } else if(kind==='matrix'){
    title='브랜드 × 지역';
    body=`<div class="note" style="margin:2px 0 6px">칸 = 지역 성장률(환율 제외 우선) · 색 = 선택한 가정의 기회 수준 · 한국 수요 = 한국이 속한 지역 성장률</div>
    <table id="srcTbl"><tr><th>브랜드</th><th>유럽</th><th>중동</th><th>남미</th><th>한국 수요</th></tr>`;
    srcModel().forEach(b=>{
      body+=`<tr><td>${logoImg(b.t,false,b.name)}${esc(b.name)}<div class="ref">${esc(b.period)}</div></td>`;
      SRC_KEYS.forEach(k=>{ const c=b.cells[k];
        if(!c){ body+=`<td><div class="cv" style="background:var(--barbg);color:var(--sub)">―<small>자료 없음</small></div></td>`; return; }
        const l=SRC_LV[c[SRC_PRESET]], bor=c.proxy&&c.proxy.indexOf('차용')>=0;
        body+=`<td><div class="cv" style="background:${l.bg};color:${l.fg};${bor?'border:1px dashed #3A4560':''}">${pp(c.g)}<small>${bor?'추정':l.txt}</small></div></td>`; });
      const kr=b.kr, kv=kr?(kr.cn!=null?kr.cn:kr.yoy):null;
      body+=`<td>${kv!=null?fmt(kv,1,true):'―'}<div class="ref">${kr?(kr.cn!=null?'환율 제외':'보고 통화'):''}</div></td></tr>`;
    });
    body+=`</table>`;
  } else if(kind==='method'){
    title='가정과 계산 방식';
    body=`<div class="sh-mt"><b>재고 과잉형 (보완안)</b><p>브랜드 재고 증가율이 매출 증가율보다 5%p 이상 높고(재고 압력), 그 지역이 역성장하거나 +10% 미만이면서 브랜드의 지역 중 하위권이면 높음. 둘 중 하나만 맞으면 보통.</p>
      <b>시장 확대형 (원안)</b><p>지역 성장률 +15% 이상 또는 브랜드 재고 증가 +15% 이상이면 높음, +5% 이상이면 보통.</p>
      <b>지도 배지</b><p>지역마다 기회 수준이 높은 순으로 최대 3개 브랜드를 표시하고 나머지는 +숫자로 묶습니다. 테두리 색이 기회 수준이며, 브랜드를 누르면 기업 상세로 이동합니다.</p>
      <b>지역 판정 (지도 색·지역 칩)</b><p>점수 = 기회 높은 브랜드 수(최대 2점) + 현지 유통 재고(재고 과잉형만: "무거움"인 유통사가 하나라도 있으면 +1, 모두 "가벼움"이면 −1) + 환율(현지 통화 원화 값이 1년 전보다 평균 2% 이상 내리면 매입 부담이 줄어 +1, 2% 이상 오르면 −1). 3점 이상 높음, 1~2점 보통, 0점 이하 낮음. 지역 패널 맨 위에 점수 내역을 표시합니다.</p>
      <b>현지 유통사·환율·뉴스</b><p>유통사는 재고 증가율이 매출 증가율보다 5%p 이상 높으면 "무거움"(처분 물량 가능성), 5%p 이상 낮으면 "가벼움". 환율은 현지 통화 1단위의 원화 값 1년 변동입니다(북미는 달러, 일본은 엔(100엔 단위 표시), 중동은 달러 고정 통화라 달러로 대신). 뉴스는 참고 정보로만 붙입니다.</p>
      <b>데이터 한계</b><p>지역별 재고는 공시되지 않아 브랜드 전체 재고를 씁니다. 국가가 아닌 지역 단위이며, 중동은 유럽·중동·아프리카 또는 신흥시장 합산값을 빌려 쓰고 상장 유통사도 없어 뉴스로 보완합니다.</p></div>`;
  } else return;
  sh.innerHTML=`<button type="button" class="sh-bd" aria-label="닫기" onclick="closeSheet()"></button>
    <div class="sh-pn" role="dialog" aria-modal="true" aria-label="${title}"><div class="sh-grip"></div>
    <div class="sh-hd"><div class="sh-tt">${title} ${chip}</div><button type="button" class="sh-x" aria-label="닫기" onclick="closeSheet()">✕</button></div>${body}</div>`;
  sh.classList.add('on');
}
function closeSheet(){ SRC_SHEET=null; const sh=document.getElementById('sheet'); sh.classList.remove('on'); sh.innerHTML=''; }
document.addEventListener('keydown',e=>{ if(e.key==='Escape'&&SRC_SHEET) closeSheet(); });

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
  let h=`<div class="card" id="statusCard"><h3>⚙️ 자료별 마지막 갱신</h3><table id="statusTbl"><tr><th>자료</th><th>마지막 갱신</th><th>주기</th><th>상태</th></tr>`;
  rows.forEach(r=>{
    const when=r.ts?(r.ts.slice(5,7)+'/'+r.ts.slice(8,10)+(r.date_only?'':' '+r.ts.slice(11,16))):'―';   // 기록된 한국 시각 그대로
    const ageTxt=r.age==null?'':(r.age<1?'오늘':`${Math.floor(r.age)}일 전`);
    h+=`<tr><td>${esc(r.label)}<div class="ref">${esc(r.wf)}</div></td><td>${when}<div class="ref">${ageTxt}</div></td><td>${esc(r.cadence)}</td>
      <td>${r.late?'<span class="st-late">● 지연</span>':'<span class="st-ok">● 정상</span>'}</td></tr>`;
  });
  h+=`</table><div class="note">지연 = 주기보다 오래 갱신되지 않음 → GitHub Actions에서 해당 워크플로우 실행 기록 확인</div></div>`;
  return h;
}
function statusWarn(){
  const late=statusRows().filter(r=>r.late);
  document.getElementById('statusWarn').innerHTML=late.length?
    `<div class="warnbar" onclick="goMore('status')">⚠️ 수집 지연: ${late.map(r=>`${esc(r.label)} ${r.age==null?'자료 없음':Math.floor(r.age)+'일'}`).join(' · ')} — 눌러서 확인</div>`:'';
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
function newsFor(key, n=3){
  const k = NEWS_KEY[key]; if(!k || !NEWS || !NEWS.items) return [];
  return newsDedupe(NEWS.items.filter(it=>it.scope==='brand' && it.key===k)
    .sort((a,b)=>(b.first_seen||'').localeCompare(a.first_seen||'') || (b.importance||0)-(a.importance||0)), n);
}
function newsCard(key){
  const list=newsFor(key);
  let h=`<div class="card"><h3>📰 최근 뉴스 <span class="go" onclick="sw('news')">뉴스 ▸</span></h3>`;
  if(!list.length){ h+=`<div class="na">최근 14일 선별 뉴스 없음</div></div>`; return h; }
  list.forEach(it=>{
    h+=`<div class="nitem"><div class="nsum"><a href="${it.link}" target="_blank" rel="noopener">${'★'.repeat(it.importance||1)} ${esc(it.summary||it.title)}</a></div>
      <div class="nmeta">${esc(it.source||'')} · ${esc((it.first_seen||'').slice(5).replace('-','/'))}</div></div>`;
  });
  return h+`</div>`;
}
function flagOf(t){
  const f = FLAGS[t] || (isKR(t) ? "🇰🇷" : null);
  return f ? `<span class="flag">${f}</span>` : "";
}
function logoImg(t, large, name){
  const d = DOMAINS[t];
  const cls = large ? "logo-lg" : "logo";
  const init = String(name||t).replace(/[^가-힣A-Za-z0-9]/g,'').slice(0,1) || '·';
  const fb = `<i class="lgfb ${large?'lgfb-lg':''}" style="display:none">${init}</i>`;
  if(!d) return `<span class="lg">${fb.replace('display:none','')}</span>`;
  return `<span class="lg"><img class="${cls}" loading="lazy" alt="" onerror="this.style.display='none';this.nextSibling.style.display='inline-flex'"
    src="https://www.google.com/s2/favicons?domain=${d}&sz=64">${fb}</span>`;
}

/* ── 테마 ── */
const btn=document.getElementById('themeBtn');
function applyTheme(t){
  if(t==='dark'){document.documentElement.setAttribute('data-theme','dark');btn.textContent='☀️';}
  else{document.documentElement.removeAttribute('data-theme');btn.textContent='🌙';}
}
let theme='light';
try{theme=localStorage.getItem('sim-theme')||'light';}catch(e){}
applyTheme(theme);
btn.onclick=()=>{
  theme=(theme==='dark')?'light':'dark';
  applyTheme(theme);
  try{localStorage.setItem('sim-theme',theme);}catch(e){}
};

const esc=s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;')
  .replace(/>/g,'&gt;').replace(/"/g,'&quot;');
const fmt=(v,d=1,sign=false)=>{
  if(v===null||v===undefined) return '<span class="na">―</span>';
  const s=v.toFixed(d); const cls=v>=0?'pos':'neg';
  return sign?`<span class="${cls}">${v>=0?'+':''}${s}%</span>`:s;
};
/* 재무제표 통화: 야후 currency는 주가 통화라 영국 상장사는 GBp(펜스) — 재무 수치는 GBP(파운드) */
const finCur=c=>c==='GBp'?'GBP':(c||'');
const finCurOf=x=>finCur(x.fin_currency||x.currency);   // 재무제표 통화 우선(v30.1)
/* 외화 금액의 원화 근사(v30.2) — data.json fx의 최근 환율, 환율 없으면 null */
const krwOf=(v,cur)=>{ if(v==null) return null; if(cur==='KRW') return v; const f=(DATA.fx||{})[cur]; return (f&&f.rate)?v*f.rate:null; };
/* 국내 그룹의 외화 실적: "≈46.9조" + 작은 글씨로 원래 통화 */
function revKrwCell(rev,cur){
  const k=krwOf(rev,cur);
  if(cur==='KRW'||k==null) return moneyShort(rev,cur);
  return `≈${moneyShort(k,'KRW')}<span class="na" style="font-size:var(--fs-2xs);display:block">${moneyShort(rev,cur)} ${esc(cur)}</span>`;
}
const money=(v,cur)=>{
  if(v===null||v===undefined) return '―';
  if(cur==='KRW'){
    return v>=1e12?(v/1e12).toFixed(2)+'조원':(v/1e8).toLocaleString(undefined,{maximumFractionDigits:0})+'억원';
  }
  const m=v/1e6;
  return m>=1000?(m/1000).toFixed(2)+'B '+(cur||''):m.toFixed(0)+'M '+(cur||'');
};
const moneyShort=(v,cur)=>{
  if(v===null||v===undefined) return '―';
  if(cur==='KRW'){
    return v>=1e12?(v/1e12).toFixed(2)+'조':(v/1e8).toLocaleString(undefined,{maximumFractionDigits:0})+'억';
  }
  const m=v/1e6;
  return m>=1000?(m/1000).toFixed(1)+'B':m.toFixed(0)+'M';
};
const segMoney=v=>{
  if(v===null||v===undefined) return '―';
  return v>=1000?(v/1000).toFixed(2)+'B':v.toFixed(0)+'M';
};
const ym=d=>d?("'"+d.slice(2,4)+"."+d.slice(5,7)):null;
function segOf(t){
  const e=(SEGS.items||{})[t];
  return (e&&e.extract)?e:null;
}

/* ── 공통: 기업 행 데이터(상장 41 + 국내 법인) ── */
function rows_all(){
  const out=[];
  DATA.items.forEach(x=>{
    const fy=x.fy.length?x.fy[x.fy.length-1]:{};
    out.push({key:x.ticker, name:x.name, group:x.group, flag:flagOf(x.ticker), logo:logoImg(x.ticker,false,x.name), listed:true,
      rev:fy.rev, cur:finCurOf(x), rev_yoy:fy.rev_yoy, gm:fy.gm_pct, q_yoy:x.latest_q_yoy, dio:dioOf(x.inventory,fy.rev,fy.gp,null),
      inv_yoy:x.inv_yoy, earn:x.earn_date, note:x.note, item:x});
  });
  ((KRD&&KRD.entities)||[]).forEach(e=>{
    const ys=(e.years||[]).filter(y=>y.rev!=null); const last=ys[ys.length-1], prev=ys[ys.length-2];
    const yoy=(last&&prev&&prev.rev)?(last.rev/prev.rev-1)*100:null;
    const opm=(last&&last.op!=null&&last.rev)?last.op/last.rev*100:null;
    const gmk=(last&&last.cogs!=null&&last.rev)?(last.rev-last.cogs)/last.rev*100:null;
    const invy=(last&&prev&&last.inv&&prev.inv)?(last.inv/prev.inv-1)*100:null;
    const diok=last?dioOf(last.inv,last.rev,null,last.cogs):null;
    out.push({key:'krd:'+e.id, name:e.name, group:'국내 법인', flag:'🇰🇷', logo:logoImg('krd:'+e.id,false,e.name), listed:false,
      rev:last?last.rev:null, cur:'KRW', rev_yoy:yoy, gm:gmk, opm, q_yoy:null, inv_yoy:invy, earn:null, dio:diok,
      note:e.note, route:e.route, fy_end:last?last.end:null});
  });
  return out;
}
const CO_GROUPS = [...GROUPS, '국내 법인'];

/* ── 종합 (A안: 신호) ── */
function buildHome(){
  const rows=rows_all();
  const today=new Date(); today.setHours(0,0,0,0);
  // 성장(최근 분기 매출 전년 대비; 국내 법인은 연간)
  const growthAll=rows.map(r=>({...r, g:(r.q_yoy!=null?r.q_yoy:r.rev_yoy), basis:(r.q_yoy!=null?'분기':'연간')})).filter(r=>r.g!=null);
  // ±100% 초과는 기저·인수 효과 가능성이 커서 순위에서 제외(각주로 표기, §29-D: 값은 기업 탭에 그대로)
  const outlier=growthAll.filter(r=>Math.abs(r.g)>100);
  const growth=growthAll.filter(r=>Math.abs(r.g)<=100);
  const up=[...growth].sort((a,b)=>b.g-a.g).slice(0,4);
  const dn=[...growth].sort((a,b)=>a.g-b.g).slice(0,4);
  // 재고 경고: 재고 증가율이 매출 증가율보다 10p 이상 높고 재고 +10% 이상
  const warn=rows.filter(r=>r.inv_yoy!=null&&r.rev_yoy!=null&&r.inv_yoy>=10&&r.inv_yoy-r.rev_yoy>=10)
    .sort((a,b)=>(b.inv_yoy-b.rev_yoy)-(a.inv_yoy-a.rev_yoy));
  // 실적 일정
  const ev=rows.filter(r=>r.earn).map(r=>({...r,d:new Date(r.earn+'T00:00:00')})).map(r=>({...r,dn:Math.round((r.d-today)/86400000)}))
    .filter(r=>r.dn>=0&&r.dn<=90).sort((a,b)=>a.dn-b.dn);
  // 국내 의류 소매
  const kr=(KR&&KR.series&&KR.series.retail_apparel)?KR.series.retail_apparel:null;
  let krLast=null, krYoy=null, krTrend='';
  if(kr){ const ps=Object.keys(kr.values).sort(); krLast=ps[ps.length-1]; krYoy=kr.yoy?kr.yoy[krLast]:null;
    const y3=ps.slice(-3).map(p=>kr.yoy?kr.yoy[p]:null);
    if(y3.every(v=>v!=null)) krTrend = (y3[0]>y3[1]&&y3[1]>y3[2])?'3개월 둔화':(y3[0]<y3[1]&&y3[1]<y3[2])?'3개월 가속':''; }

  const kp=[
    up[0]?{l:'성장 1위',v:fmt(up[0].g,1,true),s:`${up[0].name} ${up[0].basis}`,act:`goDetail('${up[0].key}')`}:{l:'성장 1위',v:'―',s:'',act:"sw('co')"},
    {l:'재고 경고',v:`<span class="${warn.length?'neg':''}">${warn.length}곳</span>`,s:'재고↑ 매출↓ · 누르면 목록',act:"focusCard('warnCard')"},
    ev[0]?{l:'실적 발표',v:`D-${ev[0].dn}`,s:`${ev[0].name} ${ev[0].d.getMonth()+1}/${ev[0].d.getDate()}`,act:"sw('cal')"}:{l:'실적 발표',v:'―',s:'90일 내 없음',act:"sw('cal')"},
    kr?{l:'국내 의류 소매',v:fmt(krYoy,1,true),s:`${fmtPrd(krLast)} · ${krTrend||'전년 동월 대비'}`,act:"sw('kr')"}:{l:'국내 의류 소매',v:'―',s:'미수집',act:"sw('kr')"},
  ];
  document.getElementById('kpis').innerHTML=kp.map(k=>`<div class="kpi" onclick="${k.act}"><div class="l">${k.l}</div><div class="v">${k.v}</div><div class="s">${esc(k.s)}</div></div>`).join('');

  let h='';
  // 올해 vs 작년 꺾은선 (국내 의류 소매판매지수)
  if(kr){
    const ps=Object.keys(kr.values).sort(); const yNow=krLast.slice(0,4), yPrev=String(+yNow-1);
    const cur=[],prev=[]; for(let m=1;m<=12;m++){const mm=String(m).padStart(2,'0'); cur.push(kr.values[yNow+mm]??null); prev.push(kr.values[yPrev+mm]??null);}
    const all=[...cur,...prev].filter(v=>v!=null); const mn=Math.min(...all), mx=Math.max(...all), rg=(mx-mn)||1;
    const W=700,H=140,L=24,R=16,T=18,B=22; const xs=i=>L+i*(W-L-R)/11, ys=v=>T+(H-T-B)-(v-mn)/rg*(H-T-B);
    const line=(arr,color,w)=>{const pts=arr.map((v,i)=>v==null?null:`${xs(i).toFixed(1)},${ys(v).toFixed(1)}`).filter(Boolean).join(' ');return `<polyline fill="none" stroke="${color}" stroke-width="${w}" points="${pts}"/>`;};
    const lastIdx=cur.map((v,i)=>v!=null?i:-1).filter(i=>i>=0).pop();
    h+=`<div class="card span2"><h3>국내 의류 소매판매 — 올해 vs 작년 (월별 지수) <span class="go" onclick="sw('kr')">국내 ▸</span></h3>
    <svg viewBox="0 0 ${W} ${H}" width="100%" height="${H}" style="display:block">
      ${line(prev,'var(--accent-prev)',2)}${line(cur,'var(--accent)',2.5)}
      ${lastIdx!=null?`<circle cx="${xs(lastIdx)}" cy="${ys(cur[lastIdx])}" r="4" fill="var(--accent)"/>`:''}
      ${[0,3,6,9,11].map(i=>`<text x="${xs(i)-8}" y="${H-6}" style="font-size:10px;fill:var(--sub)">${i+1}월</text>`).join('')}
      <text x="${W-150}" y="12" style="font-size:10px;fill:var(--accent)">— ${yNow}</text><text x="${W-90}" y="12" style="font-size:10px;fill:var(--sub)">— ${yPrev}</text>
    </svg>
    <div class="note">${fmtPrd(krLast)} ${kr.values[krLast].toFixed(1)} (작년 ${(kr.values[yPrev+krLast.slice(4,6)]??'―')}, ${fmt(krYoy,1,true)})${krTrend?' · '+krTrend:''}</div></div>`;
  }
  h+=sourcingCard();
  const rk=(r,valHtml)=>`<div class="rk" onclick="goDetail('${r.key}')"><span>${r.logo}${esc(r.name)}<span class="g">${esc(r.group)}${r.basis?' · '+r.basis:''}</span></span>${valHtml}</div>`;
  h+=`<div class="card"><h3>성장 상위 · 매출 전년 대비 <span class="go" onclick="sw('co')">기업 ▸</span></h3>${up.map(r=>rk(r,`<b class="pos">${fmt(r.g,1,true)}</b>`)).join('')||'<div class="na">―</div>'}${outlier.length?`<div class="note">순위 제외(±100% 초과, 기저·인수 효과 가능): ${outlier.map(r=>esc(r.name)+' '+fmt(r.g,0,true)).join(' · ')}</div>`:''}</div>`;
  h+=`<div class="card"><h3>성장 하위 · 매출 전년 대비</h3>${dn.map(r=>rk(r,`<b>${fmt(r.g,1,true)}</b>`)).join('')||'<div class="na">―</div>'}</div>`;
  h+=`<div class="card" id="warnCard"><h3>재고 경고 · 재고 증가율이 매출 증가율보다 높은 곳 <span class="na" style="margin-left:auto;font-size:var(--fs-2xs)">기업을 누르면 상세</span></h3>${warn.slice(0,8).map(r=>rk(r,`<span>재고 <b class="neg">${fmt(r.inv_yoy,1,true)}</b> · 매출 ${fmt(r.rev_yoy,1,true)}${r.dio!=null?` · <span class="na">${Math.round(r.dio)}일</span>`:''}</span>`)).join('')||'<div class="na">해당 없음</div>'}</div>`;
  h+=`<div class="card"><h3>다가오는 실적 발표 <span class="go" onclick="sw('cal')">캘린더 ▸</span></h3>${ev.slice(0,5).map(r=>rk(r,`<span>${r.dn<=7?'🔴':'⚪'} D-${r.dn} · ${r.d.getMonth()+1}/${r.d.getDate()}</span>`)).join('')||'<div class="na">90일 내 일정 없음</div>'}</div>`;
  document.getElementById('homeBody').innerHTML=h;
  statusWarn();
}

/* ── 기업 (A안: 검색·칩·압축 표·행 펼침) ── */
let coFilter='전체', coQuery='';
function buildCoChips(){
  const rows=rows_all();
  const chips=[['전체',rows.length],...CO_GROUPS.map(g=>[g,rows.filter(r=>r.group===g).length]).filter(x=>x[1]>0),
    ['유통사 비교',rows.filter(r=>PEER_KEYS.includes(r.key)).length],
    ['패션 브랜드 비교',rows.filter(r=>FB_KEYS.includes(r.key)).length],
    ['아이웨어 비교',rows.filter(r=>EY_KEYS.includes(r.key)).length]].filter(x=>x[0]==='전체'||x[1]>0);
  document.getElementById('coChips').innerHTML=chips.map(([g,n])=>`<span class="chip ${coFilter===g?'on':''}" data-g="${g}">${g==='전체'?'전체':(g==='유통사 비교'?'🏷️':g==='패션 브랜드 비교'?'👕':g==='아이웨어 비교'?'🕶️':(GROUP_ICON[g]||'🇰🇷'))+' '+g} ${n}</span>`).join('');
  document.querySelectorAll('#coChips .chip').forEach(c=>c.onclick=()=>{coFilter=c.dataset.g;buildCoChips();buildCo();});
}
function buildCo(){
  const rows=rows_all().filter(r=>(coFilter==='전체'||r.group===coFilter||(coFilter==='유통사 비교'&&PEER_KEYS.includes(r.key))||(coFilter==='패션 브랜드 비교'&&FB_KEYS.includes(r.key))||(coFilter==='아이웨어 비교'&&EY_KEYS.includes(r.key)))&&(!coQuery||r.name.toLowerCase().includes(coQuery)||r.key.toLowerCase().includes(coQuery)));
  let h=`<tr><th>기업</th><th>매출</th><th>전년 대비</th><th>총이익률</th><th>재고 증감</th></tr>`;
  rows.forEach(r=>{
    const gmCell=(r.gm!=null)?r.gm.toFixed(1)+'%':(r.opm!=null?r.opm.toFixed(1)+'%<span class="na" style="font-size:var(--fs-2xs)"> 영업</span>':'<span class="na">―</span>');
    h+=`<tr class="co" data-k="${r.key}"><td>${r.logo}${esc(r.name)}</td><td>${String(r.group||'').startsWith('국내')?revKrwCell(r.rev,r.cur):moneyShort(r.rev,r.cur)}</td><td>${fmt(r.rev_yoy,1,true)}</td><td>${gmCell}</td><td>${fmt(r.inv_yoy,1,true)}</td></tr>`;
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
      const evd=r.earn?Math.round((new Date(r.earn+'T00:00:00')-new Date().setHours(0,0,0,0))/86400000):null;
      mini=`<div class="mini"><div>최근 분기 매출 ${fmt(r.q_yoy,1,true)} <span class="na">${x.q_end?ym(x.q_end):''}</span></div><div>영업이익률 <b>${fy.op_pct!=null?fy.op_pct.toFixed(1)+'%':'―'}</b></div>
      <div>지역: ${esc(top)}</div><div>채널: ${esc(chs)}</div>
      <div>${kd?logoImg('krd:'+kd.id,false,kd.name)+esc(kd.name)+' ':'🇰🇷 '}${kd?`<b>${kdTxt}</b>`:'<span class="na">국내 법인 미연결</span>'}</div><div>실적 발표 ${evd!=null&&evd>=0?`<b>D-${evd}</b>`:'<span class="na">―</span>'}</div></div>`;
    } else {
      mini=`<div class="mini"><div>구분: ${esc(r.route==='none'?'DART 공시 미발견':'DART 감사보고서(연간)')}</div><div>기준: ${r.fy_end?ym(r.fy_end)+' 결산':'―'}</div>
      <div>재고일수 <b>${r.dio!=null?Math.round(r.dio)+'일':'―'}</b></div><div>재고 증감 <b>${fmt(r.inv_yoy,1,true)}</b></div>${r.note?`<div style="grid-column:1/3" class="na">${esc(r.note)}</div>`:''}</div>`;
    }
    h+=`<tr class="cx" data-for="${r.key}" style="display:none"><td colspan="5">${mini}<div class="note" style="margin-top:6px;color:var(--accent);cursor:pointer" onclick="goDetail('${r.key}')">전체 상세 ▸</div></td></tr>`;
  });
  if(rows.length===0) h+=`<tr><td colspan="5" class="na">검색 결과 없음</td></tr>`;
  document.getElementById('coTbl').innerHTML=h;
  document.querySelectorAll('#coTbl tr.co').forEach(tr=>tr.onclick=()=>{const x=tr.nextElementSibling; if(x&&x.classList.contains('cx')) x.style.display=x.style.display==='none'?'':'none';});
}
function showCoList(){ document.getElementById('coDetail').style.display='none'; document.getElementById('coList').style.display=''; }
function goDetail(t){
  sw('co');
  document.getElementById('coList').style.display='none';
  document.getElementById('coDetail').style.display='';
  renderDetail(t);
  document.getElementById('content').scrollTo(0,0);
}
function pairBars(list, curLabel, prevLabel){
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
    const yoy=r.yoy!=null?` <span class="${r.yoy>=0?'pos':'neg'}">${r.yoy>=0?'+':''}${r.yoy.toFixed(1)}%</span>`:'';
    h+=`<div class="pair">
    <div class="pname" title="${esc(r.name)}">${esc(r.name)}${shCur?` · 비중 ${shCur}%`:''}${shPrev?` <span class="na">(전년 ${shPrev}%)</span>`:''}${r.derived?'<span class="tag2">역산</span>':''}</div>
    <div class="prow"><div class="yr">${curLabel}</div>
      <div class="pw"><div class="pb now" style="width:${wC}%"></div>
      <div class="pv">${segMoney(r.cur)}${yoy}</div></div></div>`;
    if(r.prev!=null){
      const wP=Math.max(r.prev/mx*100,6);
      h+=`<div class="prow"><div class="yr">${prevLabel}</div>
      <div class="pw"><div class="pb prev" style="width:${wP}%"></div>
      <div class="pv">${segMoney(r.prev)}</div></div></div>`;
    }
    if(r.cn!=null) h+=`<div class="cnline">환율 제외 <span class="${r.cn>=0?'pos':'neg'}">${r.cn>=0?'+':''}${r.cn.toFixed(1)}%</span>${r.yoy!=null?` <span class="na">(보고 통화 ${r.yoy>=0?'+':''}${r.yoy.toFixed(1)}%)</span>`:''}</div>`;
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
  const diff=(a,b)=>(a==null||b==null)?'':`<span class="na" style="font-size:var(--fs-2xs)"> (${(b-a)>=0?'+':''}${(b-a).toFixed(1)}p)</span>`;
  return `<div class="card"><h3>🌍 글로벌 본사 vs 🇰🇷 국내 법인</h3>
    <div class="tblwrap"><table class="nowrap"><tr><th></th><th>${esc(gx.name)}</th><th>${esc(e.name)}</th></tr>
    <tr><td>매출 전년 대비</td><td>${cell(g.yoy)}</td><td>${cell(k.yoy)}${diff(g.yoy,k.yoy)}</td></tr>
    <tr><td>영업이익률</td><td>${g.opm!=null?g.opm.toFixed(1)+'%':'<span class="na">―</span>'}</td><td>${k.opm!=null?k.opm.toFixed(1)+'%':'<span class="na">―</span>'}${diff(g.opm,k.opm)}</td></tr>
    <tr><td>재고 증감</td><td>${cell(g.inv)}</td><td>${cell(k.inv)}${diff(g.inv,k.inv)}</td></tr>
    <tr><td>재고일수</td><td>${cell(g.dio,false)}</td><td>${cell(k.dio,false)}</td></tr></table></div>
    <div class="note">글로벌 FY ${fy.end?ym(fy.end):'―'} 연결 · 국내 법인 FY ${ym(l.end)} 별도 — 회계기간·기준이 달라 방향 비교용 · 괄호는 국내−글로벌 차이(p)</div></div>`;
}
function krdCard(e, linked){
  const title=linked?`🇰🇷 국내 법인 실적 — ${esc(e.name)}`:`🇰🇷 법인 실적`;
  let h=`<div class="card"><h3>${title} <span class="tag">DART 감사보고서</span></h3>`;
  if(e.note) h+=`<div class="note" style="margin:0 0 8px">ℹ️ ${esc(e.note)}</div>`;
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
      <td>${opm!=null?opm.toFixed(1)+'%':'―'}</td>
      <td>${y.ni!=null?moneyShort(y.ni,'KRW'):'―'}</td>
      <td>${y.inv!=null?moneyShort(y.inv,'KRW'):'―'}</td><td>${fmt(iy,1,true)}</td></tr>`;
  });
  h+=`</table></div>`;
  const srcs=ys.filter(y=>y.source).map(y=>y.fy+': '+y.source);
  if(srcs.length) h+=`<div class="src">출처: ${esc(srcs.join(' · '))}</div>`;
  h+=`<div class="note">${fym?fym+' · ':''}별도(개별) 재무제표 · 원화 · 연간 — 글로벌 실적과 회계기간·기준이 다를 수 있음</div></div>`;
  return h;
}
function renderKrdDetail(id){
  const e=((KRD&&KRD.entities)||[]).find(z=>z.id===id);
  if(!e){ document.getElementById('detBody').innerHTML='<div class="na">미확인</div>'; return; }
  let h=`<div class="det-head">${logoImg('krd:'+e.id,true,e.name)}${esc(e.name)} <span class="tk">🇰🇷</span> <span class="tag">${esc(e.type)}</span></div>`;
  h+=krdCard(e,false);
  if(e.link){
    const g=DATA.items.find(i=>i.ticker===e.link);
    if(g) h+=compareCard(g,e)+`<div class="note">글로벌 본사: <a href="#" onclick="goDetail('${e.link}');return false;" style="color:var(--accent)">${logoImg(e.link,false,g.name)}${esc(g.name)} ▸</a></div>`;
  }
  h+=naverDetailCard('krd:'+e.id);
  h+=newsCard('krd:'+e.id);
  document.getElementById('detBody').innerHTML=h;
}
function renderDetail(t){
  if(String(t).startsWith('krd:')){ renderKrdDetail(t.slice(4)); return; }
  const x=DATA.items.find(i=>i.ticker===t);
  const cur=finCurOf(x);
  let h=`<div class="det-head">${logoImg(x.ticker,true,x.name)}${x.name} <span class="tk">${flagOf(x.ticker)} ${x.ticker}</span> <span class="tag">${esc(x.group||'')}</span></div>`;
  if(x.note) h+=`<div class="note" style="margin:-6px 0 12px">ℹ️ ${esc(x.note)}</div>`;
  if(x.fin_source) h+=`<div class="src" style="margin:-4px 0 10px">재무: ${esc(x.fin_source)} · 주가·분기 매출 전년 대비·실적일: Yahoo</div>`;
  if(x.group==='글로벌 브랜드') h+=koreaCard(x);
  h+=`<div class="card"><h3>📈 매출 3개년 — 연간 (${cur}) · YoY는 직전 결산연도 대비</h3>`;
  if(x.fy.length){
    const mx=Math.max(...x.fy.map(y=>y.rev||0));
    x.fy.forEach(y=>{
      const w=y.rev?Math.max(y.rev/mx*100,8):0;
      h+=`<div class="bar-row"><div class="lb" title="${ym(y.end)}결산">${ym(y.end)}결산</div>
      <div class="bar-wrap"><div class="bar" style="width:${w}%"></div>
      <div class="bar-val">${moneyShort(y.rev,cur)} ${y.rev_yoy!=null?(y.rev_yoy>=0?'+':'')+y.rev_yoy.toFixed(1)+'%':''}</div></div></div>`;
    });
  } else h+=`<div class="na">미확인(소스 조회 실패)</div>`;
  if(String(x.group||'').startsWith('국내') && cur!=='KRW' && x.fy.length){
    const ly=x.fy[x.fy.length-1], k=krwOf(ly.rev,cur), f=(DATA.fx||{})[cur];
    if(k!=null) h+=`<div class="note" style="margin-top:6px">원화 환산 ≈ ${moneyShort(k,'KRW')}원 (${ym(ly.end)}결산 · 최근 환율 1 ${esc(cur)} = ${Math.round(f.rate).toLocaleString()}원 기준, 참고용)</div>`;
  }
  h+=`</div>`;
  h+=`<div class="card"><h3>💰 수익성 추이 — 연간</h3><table><tr><th>결산월</th><th>매출총이익률</th><th>영업이익률</th></tr>`;
  x.fy.forEach(y=>{
    h+=`<tr><td>${ym(y.end)}</td>
    <td>${y.gm_pct!=null?y.gm_pct.toFixed(1)+'%':'―'}</td>
    <td>${y.op_pct!=null?y.op_pct.toFixed(1)+'%':'―'}</td></tr>`;
  });
  h+=`</table></div>`;
  h+=`<div class="card"><h3>📦 재고</h3>
  <div class="kv"><span class="k">기준 시점</span><span>${x.inv_date||'―'}${x.inv_prev_date?' (전년비교: '+x.inv_prev_date+')':''}</span></div>
  <div class="kv"><span class="k">재고자산</span><span>${money(x.inventory,cur)}</span></div>
  <div class="kv"><span class="k">재고 증감(전년 대비)</span><span>${fmt(x.inv_yoy,1,true)}</span></div>
  <div class="kv"><span class="k">재고/매출 비율</span><span>${x.inv_sales_pct!=null?x.inv_sales_pct.toFixed(1)+'%':'―'}</span></div>
    <div class="kv"><span class="k">재고일수 <span class="na">(재고÷연간 매출원가×365)</span></span><span>${(()=>{const fy=x.fy.length?x.fy[x.fy.length-1]:{};const d=dioOf(x.inventory,fy.rev,fy.gp,null);return d!=null?Math.round(d)+'일':'―';})()}</span></div></div>`;

  /* 연결된 국내 법인 (Phase 6) */
  ((KRD&&KRD.entities)||[]).filter(e=>e.link===t).forEach(e=>{ h+=compareCard(x,e); h+=krdCard(e,true); });

  /* 지표 추이 (히스토리 축적) */
  h+=`<div class="card"><h3>📉 지표 추이 <span class="tag2">축적 데이터</span></h3>`;
  const hs=(HIST&&HIST.tickers&&HIST.tickers[t])?HIST.tickers[t]:[];
  if(hs.length<3){
    h+=`<div class="na">축적 중 — 현재 ${hs.length}점 (변화가 있을 때와 주 1회 기록되며, 3점 이상부터 추이를 그립니다)</div>`;
  } else {
    const metrics=[["inv_yoy","재고 YoY","%"],["gm_pct","GM","%"],["latest_q_yoy","분기 매출 YoY","%"],["rev_yoy","FY 매출 YoY","%"]];
    metrics.forEach(([k,label,unit])=>{
      const pts=hs.filter(p=>p[k]!=null);
      if(pts.length<2) return;
      const vals=pts.map(p=>p[k]);
      const first=pts[0], last=pts[pts.length-1];
      const delta=last[k]-first[k];
      h+=`<div class="krhead trend" style="margin-top:8px"><span class="krname">${label}</span>
        <span class="krval">${last[k].toFixed(1)}${unit}
        <span class="kryoy ${delta>=0?'pos':'neg'}">${delta>=0?'▲':'▼'}${Math.abs(delta).toFixed(1)}p</span></span></div>
        <div class="krmeta">${first.date} → ${last.date} · ${pts.length}점</div>
        ${spark(vals,260,26)}`;
    });
    h+=`<div class="note">첫 기록 대비 변화(▲▼ p) · 값은 야후 파이낸스 스냅샷 그대로(§29-D)</div>`;
  }
  h+=`</div>`;

  const s=segOf(t);
  let segEntry=(SEGS.items||{})[t];
  if(!segEntry && isKR(t)) segEntry={error:"공시 추출 미대상 — 한국 상장(DART), 향후 확장"};
  const segTag=(segEntry&&/^IR/.test(segEntry.source||''))?'IR 추출':'공시 추출';
  const segPer=(s&&s.extract&&/누적|^FY|^\d+M /.test(s.extract.period||''))?'최근 공시 기간(누적)':'최근 분기';
  h+=`<div class="card"><h3>🌍 지역 분해 — ${segPer}, 당기 vs 전년 <span class="tag">${segTag}</span></h3>`;
  if(s&&s.extract.regions&&s.extract.regions.length){
    const regsAll=s.extract.regions.filter(r=>r.revenue!=null);
    const totalOnly=regsAll.length>0&&regsAll.every(r=>/total|전체|합계|consolidated/i.test(r.name||""));
    let bars;
    if(totalOnly){
      const tt=regsAll[0];
      const yoy=tt.yoy_pct!=null?` <span class="${tt.yoy_pct>=0?'pos':'neg'}">${tt.yoy_pct>=0?'+':''}${tt.yoy_pct.toFixed(1)}%</span>`:'';
      bars=`<div class="na">지역별 매출액 미공시 — 이 회사는 지역 분해 금액을 공시하지 않습니다(성장률만 공시하는 경우 하단 주석 참조)</div>
      <div class="kv"><span class="k">분기 총매출</span><span>${segMoney(tt.revenue)}${yoy}</span></div>`;
    } else {
      bars=pairBars(s.extract.regions,"당기","전년");
    }
    h+=bars||`<div class="na">미확인(공시에 수치 미기재)</div>`;
    const pctOnly=s.extract.regions.filter(r=>r.revenue==null&&(r.yoy_pct!=null||r.cn_yoy_pct!=null)&&!/total|전체|합계|consolidated/i.test(r.name||''));
    if(pctOnly.length) h+=`<div class="note">금액 없이 증감률만 공시: ${pctOnly.map(r=>{
      const v=r.cn_yoy_pct!=null?r.cn_yoy_pct:r.yoy_pct, lab=r.cn_yoy_pct!=null?'환율 제외 ':'';
      return `${esc(r.name)} <span class="${v>=0?'pos':'neg'}">${lab}${v>=0?'+':''}${v.toFixed(1)}%</span>`;}).join(' · ')}</div>`;
    let noteTxt="기준: "+(s.extract.period||"―");
    if(s.extract.prev_period) noteTxt+=" · 전년: "+s.extract.prev_period;
    if(s.extract.notes) noteTxt+=" · "+s.extract.notes;
    const anyCn=[...(s.extract.regions||[]),...(s.extract.channels||[])].some(r=>r.cn_yoy_pct!=null);
    h+=`<div class="note">${noteTxt}<br>진한 바=당기 / 연한 바=전년 · [역산]=공시에 전년 수치 미기재로 YoY에서 계산(§29-D 구분)${anyCn?'<br>환율 제외 = 현지 통화 기준 증감(회사 공시값) — 보고 통화 증감과 차이가 크면 환율 영향이 큰 것':''}</div>`;
    if(s.source) h+=`<div class="src">출처: ${s.source}</div>`;
  } else {
    h+=`<div class="na">미확인${segEntry&&segEntry.error?'('+segEntry.error+')':'(공시에 지역 분해 미기재)'}</div>`;
  }
  h+=`</div>`;
  h+=`<div class="card"><h3>🛒 채널 분해 (DTC/도매) — ${segPer} <span class="tag">${segTag}</span></h3>`;
  if(s&&s.extract.channels&&s.extract.channels.length){
    const bars=pairBars(s.extract.channels,"당기","전년");
    h+=bars||`<div class="na">미확인(공시에 수치 미기재)</div>`;
  } else {
    h+=`<div class="na">미확인${segEntry&&segEntry.error?'('+segEntry.error+')':'(공시에 채널 분해 미기재)'}</div>`;
  }
  h+=`</div>`;

  if(t==='DKS'&&s&&s.extract.sub_segments&&s.extract.sub_segments.length){
    h+=`<div class="card"><h3>🏬 부문 분해: 딕스 / 풋락커 <span class="tag">공시 추출</span></h3>
    <table><tr><th>부문</th><th>매출</th><th>전년</th><th>YoY</th><th>부문이익</th><th>재고</th></tr>`;
    s.extract.sub_segments.forEach(ss=>{
      h+=`<tr><td>${ss.name==="DICK'S"?'딕스(본체)':'풋락커(부문)'}</td>
      <td>${segMoney(ss.revenue)}</td>
      <td>${segMoney(ss.prev_revenue)}</td>
      <td>${fmt(ss.yoy_pct,1,true)}</td>
      <td>${segMoney(ss.segment_profit)}</td>
      <td>${segMoney(ss.inventory)}</td></tr>`;
    });
    h+=`</table>`;
    if(s.extract.period) h+=`<div class="note">기준: ${s.extract.period}</div>`;
    const fl=s.extract.sub_segments.find(z=>z.name==='Foot Locker');
    if(fl&&fl.proforma_comp_pct!=null){
      h+=`<div class="note">풋락커 프로포마 기존점 매출: ${fl.proforma_comp_pct>=0?'+':''}${fl.proforma_comp_pct.toFixed(1)}%
      · 풋락커는 FY26 4분기까지 공식 comp 집계 미포함(프로포마 기준)</div>`;
    }
    h+=`</div>`;
  }

  h+=`<div class="card"><h3>(부지표) 주가</h3>
  <div class="kv"><span class="k">현재가</span><span>${x.price!=null?x.price.toFixed(2)+' '+(x.currency||''):'―'}</span></div>
  <div class="kv"><span class="k">52주 고점比</span><span>${fmt(x.off_high_pct,1,true)}</span></div></div>`;
  h+=naverDetailCard(t);
  h+=newsCard(t);
  document.getElementById('detBody').innerHTML=h;
}

/* ── 캘린더 (A안: 2개월 달력 + 90일 목록) ── */
let calSel=null;
function buildCal(){
  const today=new Date(); today.setHours(0,0,0,0);
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
      const list=byDay[key]||[]; const isT=key===today.toISOString().slice(0,10);
      cells+=`<div class="cd ${list.length?'has':''} ${isT?'today':''} ${calSel===key?'sel':''}" ${list.length?`data-day="${key}"`:''}><div class="dn">${d}</div>${list.slice(0,2).map(r=>`<div class="ev">${esc(r.name)}</div>`).join('')}${list.length>2?`<div class="ev na">+${list.length-2}</div>`:''}</div>`;
    }
    h+=`<div class="cal"><h3>${y}년 ${m+1}월</h3><div class="cgrid">${cells}</div>${calSel&&calSel.startsWith(`${y}-${String(m+1).padStart(2,'0')}`)?`<div class="calday">${calSel.slice(5).replace('-','/')} · ${(byDay[calSel]||[]).map(r=>r.logo+esc(r.name)).join(', ')}</div>`:''}</div>`;
  });
  document.getElementById('calGrid').innerHTML=h;
  document.querySelectorAll('.cd[data-day]').forEach(c=>c.onclick=()=>{calSel=(calSel===c.dataset.day)?null:c.dataset.day;buildCal();});
  document.getElementById('calList').innerHTML=evs.length?evs.map(r=>`<div class="cl"><span>${r.dn<=7?'🔴':'⚪'} ${r.logo}${esc(r.name)}</span><span>${r.d.getMonth()+1}/${r.d.getDate()} <span class="na">D-${r.dn}</span></span></div>`).join(''):'<div class="na">90일 이내 확인된 일정 없음(미확인 포함)</div>';
}

/* ── 뉴스 (v11: 그룹 필터 + NEW 배지 + 날짜별) ── */
const NEWS_FILTERS = [
  {id:"all",   label:"전체"},
  {id:"sep1",  label:"브랜드 ▸", sep:true},
  {id:"b:sports",  label:"스포츠·아웃도어"},
  {id:"b:fashion", label:"패션"},
  {id:"b:luxury",  label:"명품"},
  {id:"b:retail",  label:"유통·그외"},
  {id:"sep2",  label:"산업 ▸", sep:true},
  {id:"i:sports",  label:"스포츠 트렌드"},
  {id:"i:fashion", label:"패션·명품 시장"},
  {id:"i:retail",  label:"멀티브랜드 유통"},
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
    : `<span class="chip ${newsFilter===f.id?'on':''}" data-f="${f.id}">${f.label}</span>`).join('');
  el.querySelectorAll('.chip[data-f]').forEach(c=>{
    c.onclick=()=>{ newsFilter=c.dataset.f; buildNewsChips(); buildNews(); };
  });
}
function buildNews(){
  const el=document.getElementById('newsBody');
  if(!NEWS||!NEWS.items){
    el.innerHTML='<div class="na">뉴스 데이터 없음 — 뉴스 워크플로우(update-news) 첫 실행 전이거나 수집 실패(미확인)</div>';
    return;
  }
  const today=NEWS.today||'';
  const items=NEWS.items.filter(newsMatch);
  let kb='';
  if(newsFilter.startsWith('k:')){
    const k=newsFilter.slice(2), nm=(NEWS.items.find(i=>i.key===k)||{}).label||(nvAll().find(b=>b.news===k)||{}).name||k;
    kb=`<div class="nv-sum" style="display:flex;align-items:center;gap:8px">${esc(nm)} 뉴스만 보는 중<button type="button" class="chip" style="margin-left:auto" onclick="newsFilter='all';buildNewsChips();buildNews()">전체 보기</button></div>`;
  }
  if(!items.length){ el.innerHTML=kb+'<div class="na">해당 구분의 최근 14일 뉴스 없음</div>'; return; }
  let h=kb+`<div class="note" style="margin:0 0 6px">수집: ${NEWS.generated_at||'―'} · ${items.length}건</div>`;
  let curDate=null;
  items.forEach(it=>{
    if(it.first_seen!==curDate){
      curDate=it.first_seen;
      h+=`<div class="ndate">${curDate}${curDate===today?' · 오늘':''}</div>`;
    }
    const stars='★'.repeat(Math.max(1,Math.min(3,it.importance||1)));
    const tag=it.scope==="brand"?it.label:(it.label||it.key);
    h+=`<div class="nitem">
      <div class="nsum">${it.first_seen===today?'<span class="newbadge">NEW</span>':''}<span class="pos">${stars}</span> <a href="${it.link}" target="_blank" rel="noopener">${esc(it.summary||it.title)}</a></div>
      <div class="nmeta"><span class="ntag">${esc(tag)}</span>${esc(it.source||'')}${it.pubDate?' · '+esc(String(it.pubDate).slice(0,16)):''}</div>
    </div>`;
  });
  el.innerHTML=h;
}

/* ── 국내 수요 (KOSIS) ── */
function spark(vals,w,h){
  if(!vals||vals.length<2) return '';
  const mn=Math.min(...vals), mx=Math.max(...vals), rg=(mx-mn)||1;
  const pts=vals.map((v,i)=>`${(i/(vals.length-1)*w).toFixed(1)},${(h-(v-mn)/rg*h).toFixed(1)}`).join(' ');
  const up=vals[vals.length-1]>=vals[0];
  return `<svg width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" preserveAspectRatio="none" style="display:block;margin-top:6px">
    <polyline points="${pts}" fill="none" stroke="${up?'var(--pos)':'var(--neg)'}" stroke-width="1.6"/></svg>`;
}
function fmtPrd(p){ return p.slice(0,4)+'.'+p.slice(4,6); }
/* ── v30 국내 수요: 판매 vs 검색 교차 그래프 · 네이버 검색 관심도 ── */
let NV_SORT='yoy', NV_ALL=false, NV_GRP='global', XC_OFF={};
const NV_TOP=10;
const nvAll=()=>(NAVER&&NAVER.brands)||[];
const nvGrpOf=b=>b.group||'global';                      // v31.1: 'global'(수입·해외) / 'kr'(국내 패션)
const nvBrands=(g=NV_GRP)=>nvAll().filter(b=>nvGrpOf(b)===g);
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
  const go=b.link?`goDetail('${b.link}')`:`nvNews('${b.news}')`;
  return `<div class="nv-row${b.low?' low':''}" role="button" tabindex="0" onclick="${go}" onkeydown="if(event.key==='Enter'){${go}}">
    <div class="nv-nm"><span>${esc(b.name)}</span>${b.low?'<em class="nv-low">검색량 적음</em>':''}</div>
    <span class="nv-pill ${nvRel(b.yoy,med)}">전년 ${b.yoy!=null?pp(b.yoy):'―'}</span>
    <div class="nv-bar"><span class="tr"><i style="width:${b.scale!=null?Math.max(2,Math.min(100,b.scale)):0}%"></i></span><b>${nvSc(b.scale)}</b></div>
    <div style="justify-self:end">${nvSpark(b.s,84,24)}</div>
    <div class="nv-sub">최근 4주 vs 직전 12주 ${b.trend!=null?pp(b.trend):'―'} (계절 영향 포함)</div></div>`;
}
function naverCardHtml(){
  const bs=nvBrands();
  if(!bs.length) return `<div class="card" id="nvCard"><h3>🔎 브랜드 검색 관심도 — 네이버</h3><div class="na">네이버 검색 관심도 수집 전 — 다음 갱신 후 표시</div></div>`;
  const med=nvMed(), key=b=>NV_SORT==='yoy'?(b.yoy??-1e9):(b.scale??-1);
  const rows=[...bs].sort((a,b)=>key(b)-key(a)), shown=NV_ALL?rows:rows.slice(0,NV_TOP);
  const ups=bs.filter(b=>!b.low&&nvRel(b.yoy,med)==='up').sort((a,b)=>b.yoy-a.yoy).slice(0,4);
  const downs=bs.filter(b=>!b.low&&nvRel(b.yoy,med)==='down').sort((a,b)=>a.yoy-b.yoy).slice(0,3);
  let h=`<div class="card" id="nvCard"><h3>🔎 브랜드 검색 관심도 — 네이버</h3>
    ${nvBrands('kr').length?`<div class="seg2" style="margin-bottom:8px"><button type="button" class="${NV_GRP==='global'?'on':''}" aria-pressed="${NV_GRP==='global'}" onclick="nvGrp('global')">수입·해외 브랜드 ${nvBrands('global').length}</button><button type="button" class="${NV_GRP==='kr'?'on':''}" aria-pressed="${NV_GRP==='kr'}" onclick="nvGrp('kr')">국내 패션 브랜드 ${nvBrands('kr').length}</button></div>`:''}
    <div class="note" style="margin:0 0 8px">주간 검색 지수 · 나이키 최근 4주 = 100 · ${nvWk(NAVER.end)} 주까지 · ${bs.length}개 브랜드${NV_GRP==='kr'?' · 중앙값은 국내 패션 브랜드끼리':''}</div>
    <div class="seg2" style="margin-bottom:10px"><button type="button" class="${NV_SORT==='yoy'?'on':''}" aria-pressed="${NV_SORT==='yoy'}" onclick="nvSort('yoy')">전년 대비순</button><button type="button" class="${NV_SORT==='size'?'on':''}" aria-pressed="${NV_SORT==='size'}" onclick="nvSort('size')">규모순</button></div>
    <div class="nv-sum"><b>전년 대비 중앙값 ${med!=null?pp(med):'―'}</b> — 대부분이 같이 움직이면 네이버 검색 전반의 변화라, 중앙값보다 나은지로 봅니다.${ups.length?`<br><b style="color:var(--up)">▲ 상대 증가</b> ${ups.map(b=>`${esc(b.name)} ${pp(b.yoy)}`).join(' · ')}`:''}${downs.length?`<br><b style="color:var(--down)">▼ 상대 감소</b> ${downs.map(b=>`${esc(b.name)} ${pp(b.yoy)}`).join(' · ')}`:''}</div>`;
  shown.forEach(b=>{ h+=nvRowHtml(b,med); });
  if(rows.length>NV_TOP) h+=`<button type="button" class="nv-more" onclick="nvToggle()">${NV_ALL?`상위 ${NV_TOP}개만 보기 ▴`:`전체 ${rows.length}개 보기 ▾`}</button>`;
  h+=`<div class="src-legend" style="margin-top:8px"><span><i style="background:var(--up)"></i>중앙값보다 5%p 이상 좋음</span><span><i style="background:var(--down)"></i>5%p 이상 나쁨</span><span><i style="background:var(--sub);opacity:.55"></i>막대 = 규모</span><span>그래프: 최근 1년 실선 · 그 전 1년 점선</span></div>
    <div class="note" style="margin-top:6px">전년 대비 = 최근 4주 vs 1년 전 같은 4주(지수 비율 = 실제 검색 횟수 비율). 규모 1 미만은 검색량이 적어 흐리게 표시. 누르면 기업 상세 또는 그 브랜드 뉴스로 이동. 출처: ${esc(NAVER.source||'네이버 데이터랩')}</div></div>`;
  return h;
}
function nvRefresh(){ const c=document.getElementById('nvCard'); if(c) c.outerHTML=naverCardHtml(); }
function nvSort(s){ NV_SORT=s; nvRefresh(); }
function nvToggle(){ NV_ALL=!NV_ALL; nvRefresh(); }
function nvGrp(g){ NV_GRP=g; NV_ALL=false; nvRefresh(); }
function nvNews(k){ newsFilter='k:'+k; sw('news'); buildNewsChips(); buildNews(); }
function naverDetailCard(t){
  const bs=nvAll().filter(b=>b.link===t); if(!bs.length) return '';
  let h=`<div class="card"><h3>🔎 네이버 검색 관심도 <span class="go" onclick="sw('kr')">국내 ▸</span></h3>`;
  bs.forEach(b=>{
    const med=nvMed(nvGrpOf(b)), grpN=nvBrands(nvGrpOf(b)).length;
    h+=`<div class="nv-det"><div class="krhead"><span class="krname">${esc(b.name)}</span><span class="nv-pill ${nvRel(b.yoy,med)}" style="margin-left:auto">전년 ${b.yoy!=null?pp(b.yoy):'―'}</span></div>
      <div class="krmeta">규모 ${nvSc(b.scale)} (나이키 최근 4주 = 100) · ${nvGrpOf(b)==='kr'?'국내 패션 ':''}${grpN}개 브랜드 중앙값 ${med!=null?pp(med):'―'} · 최근 4주 vs 직전 12주 ${b.trend!=null?pp(b.trend):'―'}</div>
      ${nvSpark(b.s,300,44,true)}</div>`;
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
const XC={W:340,H:196,L:36,R:10,T:12,B:28};
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
  for(let v=lo; v<=hi+1e-9; v+=step) g+=`<line x1="${L}" x2="${W-R}" y1="${y(v).toFixed(1)}" y2="${y(v).toFixed(1)}" stroke="var(--line)" stroke-width="${v===0?1.4:.6}"/><text x="${L-5}" y="${(y(v)+3).toFixed(1)}" text-anchor="end" font-size="9" fill="var(--sub)">${v>0?'+':''}${v}%</text>`;
  months.forEach((m,i)=>{ const last=months.length-1; if((i%3===0&&last-i>=2)||i===last) g+=`<text x="${x(i).toFixed(1)}" y="${H-10}" text-anchor="${i===months.length-1?'end':(i===0?'start':'middle')}" font-size="9" fill="var(--sub)">${m.slice(2,4)}.${m.slice(5,7)}</text>`; });
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
  return `<div class="card" id="xcCard"><h3>📈 국내 수요 한눈에 — 판매 vs 검색</h3>
    <div class="note" style="margin:0 0 4px">모두 전년 같은 달 대비(%) · 같은 축 · 최근 ${months.length}개월 · 그래프를 누르면 그 달 값</div>
    <div class="xc-legend">${legend}</div>
    <div class="xc-wrap"><svg class="xc-svg" id="xcSvg" viewBox="0 0 ${W} ${H}" role="img" aria-label="온라인 신발·의복 거래액과 네이버 브랜드 검색량의 전년 대비 증감">${g}${ln}<line id="xcGuide" x1="0" x2="0" y1="${T}" y2="${T+ih}" stroke="var(--sub)" stroke-width=".8" stroke-dasharray="3 3" visibility="hidden"/><rect id="xcHit" x="${L}" y="${T}" width="${iw}" height="${ih}" fill="transparent"/></svg><div class="xc-tip" id="xcTip" hidden></div></div>
    <div class="note" style="margin-top:6px;line-height:1.6">최근: ${summ}</div>
    <div class="note" style="margin-top:4px">KOSIS 온라인쇼핑 거래액은 1~2개월 늦게 나오고 네이버는 지난달까지 나옵니다. 검색선이 판매선보다 먼저 움직이면 선행 신호로 볼 수 있습니다. 네이버 선은 아래 브랜드 검색어 전체의 검색량 합계라 큰 브랜드 비중이 크며, 시장 전체가 아닌 방향 참고용입니다.</div></div>`;
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
/* ── 🛒 국내 온라인 플랫폼 (v30.2) ── */
const KR_PLATFORMS=['CPNG','krd:musinsa','krd:kream','krd:trenbe','krd:balaan','krd:mustit','krd:trexi'];
const KR_PLATFORM_STATUS={'krd:balaan':'2026.2 회생 폐지 · 청산 절차'};   // 수치 없는 이유(대표 확인 2026.10)
function platformCardHtml(){
  const all=rows_all();
  const rows=KR_PLATFORMS.map(k=>all.find(r=>r.key===k)).filter(Boolean).map(r=>{
    const fy=r.listed&&r.item.fy.length?r.item.fy[r.item.fy.length-1]:null;
    return {...r, krw:krwOf(r.rev,r.cur), op:(r.opm!=null?r.opm:(fy?fy.op_pct:null)), end:(r.fy_end||(fy?fy.end:null))};
  }).sort((a,b)=>(b.krw==null?-1:b.krw)-(a.krw==null?-1:a.krw));
  if(!rows.length) return '';
  let h=`<div class="card"><h3>🛒 국내 온라인 플랫폼 <span class="tag">연간</span></h3>
    <div class="tblwrap"><table class="nowrap"><tr><th>기업</th><th>매출</th><th>전년 대비</th><th>영업이익률</th><th>재고 증감</th></tr>`;
  rows.forEach(r=>{
    const self=r.key==='krd:trexi';
    h+=`<tr class="co" style="cursor:pointer${self?';background:var(--barbg)':''}" onclick="goDetail('${r.key}')">
      <td>${r.logo}${self?'<b>'+esc(r.name)+'</b>':esc(r.name)}<span class="na" style="font-size:var(--fs-2xs);display:block">${KR_PLATFORM_STATUS[r.key]?'<span class="neg">'+esc(KR_PLATFORM_STATUS[r.key])+'</span>':(r.end?ym(r.end)+' 결산':'미확인')}${r.listed?' · 상장':''}</span></td>
      <td>${r.rev!=null?revKrwCell(r.rev,r.cur):'<span class="na">―</span>'}</td><td>${fmt(r.rev_yoy,1,true)}</td>
      <td>${r.op!=null?fmt(r.op,1,true):'<span class="na">―</span>'}</td><td>${fmt(r.inv_yoy,1,true)}</td></tr>`;
  });
  const usd=(DATA.fx||{}).USD;
  h+=`</table></div><div class="note" style="margin-top:6px">매출 큰 순 · 쿠팡은 미국 상장 달러 실적을 최근 환율${usd&&usd.rate?'(1달러 = '+Math.round(usd.rate).toLocaleString()+'원)':''}로 환산한 근사치 ·
    나머지는 DART 감사보고서(별도) 연간 · 플랫폼 매출은 거래액과 다름(크림 등은 수수료 매출) · 행을 누르면 상세</div></div>`;
  return h;
}
/* ── 비교 카드 (v30.4 수입 브랜드 유통사 → v31.1 공통화) — 수치는 공시 그대로, 자사(트렉시)는 위치·강조로만 앞세움 ── */
const PEER_SELF='krd:trexi';
const PEER_KEYS=[PEER_SELF,'krd:daelim_corp','krd:rexmond','krd:bazig','krd:creed','krd:hana_int','krd:t1global','krd:bbluein','krd:starintl'];
const FB_KEYS=['krd:aubrandz','krd:piecepeace','krd:sjgroup','krd:matinkim','krd:layer','krd:highlight','krd:hagohouse',
  'krd:bcave','krd:fivespace','krd:koza','krd:andar','krd:sisun','krd:lowclassic'];
const EY_KEYS=['krd:iicombined','krd:blueelephant','krd:luxottica_kr','krd:davich'];
const CMP={
  peer:{id:'peerCard',icon:'🏷️',name:'수입 브랜드 유통사 비교',keys:PEER_KEYS,self:PEER_SELF,selfName:'트렉시',tag:'연간 · 감사보고서',
        who:'비교 유통사',src:'DART 감사보고서(별도) 연간 수치 그대로'},
  fb:{id:'fbCard',icon:'👕',name:'국내 패션 브랜드 비교',keys:FB_KEYS,self:null,tag:'연간 · 사업·감사보고서',
      who:'패션 브랜드사',src:'DART 별도 재무제표 연간 수치 그대로(상장 3곳 사업보고서 · 외감 10곳 감사보고서) · 하고하우스는 브랜드 육성·투자 회사'},
  ey:{id:'eyCard',icon:'🕶️',name:'아이웨어 비교',keys:EY_KEYS,self:null,tag:'연간 · 감사보고서',
      who:'아이웨어 기업',src:'DART 감사보고서(별도) 연간 수치 그대로 · 국내 브랜드(젠틀몬스터·블루엘리펀트) vs 글로벌 국내법인(룩소티카코리아 = 에실로룩소티카) vs 안경 체인(다비치) · 아이아이컴바인드는 탬버린즈·누데이크 포함'},
};
const CMP_GROWTH={peer:'yoy',fb:'yoy',ey:'yoy'};
// [키, 이름, 높을수록 좋음, 표시]
const PEER_METRICS=[
  ['rev','매출',true,v=>moneyShort(v,'KRW')],
  ['yoy','전년 대비',true,v=>pp(v)],
  ['cagr','연평균(2년)',true,v=>pp(v)],
  ['opm','영업이익률',true,v=>v.toFixed(1)+'%'],
  ['gm','매출총이익률',true,v=>v.toFixed(1)+'%'],
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
  let h=`<div class="card" id="${c.id}"><h3>${c.icon} ${c.name} <span class="tag">${c.tag}</span></h3>`;
  if(me){
    const items=PEER_METRICS.map(([k,nm])=>({k,nm,x:rk[k].of(me),n:rk[k].n})).filter(i=>i.x!=null);
    const strong=items.filter(i=>topHalf(i.k,me)).sort((a,b)=>a.x-b.x), rest=items.filter(i=>!topHalf(i.k,me));
    h+=`<div class="nv-sum"><b>${esc(c.selfName)}</b> · ${rows.length}곳 비교<br>${strong.length?strong.map(i=>`<span class="pg-badge">${esc(i.nm)} ${i.x}위</span>`).join(''):''}${rest.length?`<span class="na" style="font-size:var(--fs-xs)"> ${rest.map(i=>`${esc(i.nm)} ${i.x}위`).join(' · ')}</span>`:''}</div>`;
  } else {
    h+=`<div class="note" style="margin:0 0 8px">${rows.length}곳 · 매출 큰 순 · 회색 줄 = 중앙값</div>`;
  }
  const order=[me,...peers.slice().sort((a,b)=>(b.rev??-1)-(a.rev??-1))].filter(Boolean);
  h+=`<div class="tblwrap"><table class="nowrap"><tr><th>기업</th>${PEER_METRICS.map(([,nm])=>`<th>${nm}</th>`).join('')}</tr>`;
  order.forEach(r=>{
    h+=`<tr style="cursor:pointer${r.self?';background:var(--barbg)':''}" onclick="goDetail('${r.key}')"><td>${logoImg(r.key,false,r.name)}${r.self?'<b>'+esc(r.name)+'</b>':esc(r.name)}<span class="pg-rk">${r.end?ym(r.end)+' 결산':'미확인'}</span></td>`;
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
  h+=`<div class="ndate" style="margin-top:14px">📈 성장성 비교</div>
    <div class="seg2" style="margin:6px 0 10px"><button type="button" class="${g==='yoy'?'on':''}" aria-pressed="${g==='yoy'}" onclick="cmpGrowth('${cid}','yoy')">전년 대비</button><button type="button" class="${g==='cagr'?'on':''}" aria-pressed="${g==='cagr'}" onclick="cmpGrowth('${cid}','cagr')">연평균(2년)</button></div>`;
  const bars=rows.filter(r=>r[g]!=null).sort((a,b)=>b[g]-a[g]);
  if(bars.length){
    const mv=med[g], lo=Math.min(0,mv??0,...bars.map(r=>r[g])), hi=Math.max(0,mv??0,...bars.map(r=>r[g])), sp=(hi-lo)||1, X=t=>(t-lo)/sp*100;
    h+=`<div class="pg-bars">`;
    bars.forEach(r=>{
      const a=X(Math.min(0,r[g])), b=X(Math.max(0,r[g]));
      const from=g==='yoy'?r.p:r.f;
      const tip=`${r.name}: ${ym(from.end)} ${moneyShort(from.rev,'KRW')} → ${ym(r.l.end)} ${moneyShort(r.l.rev,'KRW')} (${g==='yoy'?'전년 대비':'연평균'} ${pp(r[g])})`;
      h+=`<div class="pg-row${r.self?' me':''}" role="button" tabindex="0" title="${esc(tip)}" data-tip="${esc(tip)}" data-k="${r.key}" onmouseenter="peerTip(this,'${tid}')" onclick="peerTip(this,'${tid}')"><span class="pg-nm">${esc(r.name)}</span>
        <span class="pg-tr"><i class="pg-zero" style="left:${X(0)}%"></i>${mv!=null?`<i class="pg-med" style="left:${X(mv)}%"></i>`:''}<i class="pg-bar${r[g]<0?' neg':''}" style="left:${a}%;width:${Math.max(b-a,0.8)}%"></i></span><b class="pg-v">${pp(r[g])}</b></div>`;
    });
    h+=`</div><div class="pg-tip" id="${tid}">막대를 누르면 매출 변화가 보입니다</div>`;
  } else h+=`<div class="na">비교할 수치 없음</div>`;
  h+=`<div class="src-legend" style="margin-top:8px">${me?`<span><i style="background:var(--accent)"></i>${esc(c.selfName)}</span>`:''}<span><i style="background:var(--sub);opacity:.4"></i>${c.who}</span><span><i style="border-left:1.5px dashed var(--sub);width:0;height:11px;border-radius:0"></i>${me?`비교군 중앙값(${esc(c.selfName)} 제외)`:'중앙값'}</span></div>
    <div class="note" style="margin-top:6px">${c.src}${me?' · 파란 배지 = 비교군 중앙값보다 나은 지표':''} · 순위는 수치가 있는 기업끼리 · 재고일수는 낮을수록 위 · 연평균은 3개년 자료가 있는 기업만 · 행을 누르면 기업 상세</div></div>`;
  return h;
}
const peerCardHtml=()=>cmpCardHtml('peer');
function cmpGrowth(cid,m){ CMP_GROWTH[cid]=m; const el=document.getElementById(CMP[cid].id); if(el) el.outerHTML=cmpCardHtml(cid); }
function peerTip(el,tid){
  const t=document.getElementById(tid||'peerCardTip'); if(!t) return;
  t.innerHTML=`${esc(el.dataset.tip||'')} <span class="go" style="color:var(--accent);cursor:pointer" onclick="goDetail('${el.dataset.k}')">상세 ▸</span>`;
}
function buildKR(){
  const el=document.getElementById('krBody');
  const top=crossChartHtml()+platformCardHtml()+peerCardHtml()+cmpCardHtml('fb')+cmpCardHtml('ey')+naverCardHtml();
  if(!KR||!KR.series||!Object.keys(KR.series).length){
    el.innerHTML=top+'<div class="na">국내 지표 없음 — 수집 워크플로우(update-kosis) 첫 실행 전이거나 조회 실패(미확인)</div>';
    xcBind();
    return;
  }
  let h=top+`<div class="ndate">🧾 KOSIS 국내 지표 (월간)</div><div class="note" style="margin:0 0 8px">갱신: ${KR.generated_at||'―'}</div>`;
  const groups=[
    ["🛍️ 소매판매액지수",["retail_apparel","retail_shoesbag","retail_total"]],
    ["🏬 업태별 판매액지수",["store_fashion","store_internet","store_dept"]],
    ["💻 온라인쇼핑 거래액",["online_apparel","online_shoes","online_bag","online_fashionacc","online_sports"]],
    ["🏷️ 소비자물가",["cpi_apparel"]],
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
      h+=`<div class="krcard" data-k="${k}">
        <div class="krhead"><span class="krname">${esc(s.label)}</span>
          <span class="krval">${disp}
            <span class="kryoy ${y==null?'na':(y>=0?'pos':'neg')}">${y==null?'―':(y>=0?'+':'')+y.toFixed(1)+'%'}</span>
          </span></div>
        <div class="krmeta">${fmtPrd(last)} 기준 · ${esc(s.unit||'')} · ${s.table}</div>
        ${spark(vals,260,34)}
        <div class="krtbl" id="krt-${k}"><table><tr><th>월</th><th>값</th><th>YoY</th></tr>
        ${prds.slice(-13).reverse().map(p=>{
          const yy=s.yoy?s.yoy[p]:null;
          const pv=s.values[p];
          const pdisp=isIdx?pv.toFixed(1)
            :(pv>=1000000?(pv/1000000).toFixed(2)+'조원':(pv/100).toLocaleString(undefined,{maximumFractionDigits:0})+'억원');
          return `<tr><td>${fmtPrd(p)}</td><td>${pdisp}</td>
          <td>${yy==null?'<span class="na">―</span>':`<span class="${yy>=0?'pos':'neg'}">${yy>=0?'+':''}${yy.toFixed(1)}%</span>`}</td></tr>`;
        }).join('')}</table></div>
      </div>`;
    });
  });
  el.innerHTML=h;
  xcBind();
  el.querySelectorAll('.krcard').forEach(c=>{
    c.onclick=()=>document.getElementById('krt-'+c.dataset.k).classList.toggle('open');
  });
}

/* ── 더보기 (v31): 메뉴 · 환율 · 해외직구 · 수집 상태 ── */
let MORE_VIEW=null, CB_CAT='fashion';
const FX_ALERT=['JPY','EUR','USD'];
const FX_LBL={JPY:'🇯🇵 엔 (100엔)',EUR:'🇪🇺 유로',USD:'🇺🇸 달러',GBP:'🇬🇧 파운드',BRL:'🇧🇷 브라질 헤알'};
const FX_SH={JPY:'엔',EUR:'유로',USD:'달러'};
const fxMul=c=>c==='JPY'?100:1;
const wonR=v=>Math.round(v).toLocaleString('ko-KR');
const pctU=v=>(v>=0?'+':'−')+Math.abs(v).toFixed(1)+'%';
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
  const labs=new Set([lo,0,hi]); [-10,-5,5,10].forEach(k=>{ if(k>lo+1&&k<hi-1) labs.add(k); });
  labs.forEach(k=>{ h+=`<div class="fg-lb" style="left:${p(k)}">${k===0?'평균':(k>0?'+':'−')+Math.abs(k)+'%'}</div>`; });
  return `<div class="fgauge" aria-label="1년 평균 대비 ${pctU(f.dev_pct)}">${h}<div class="fg-me" style="left:${p(f.dev_pct)}"></div></div>`;
}
function fxCard(c,f){
  const m=fxMul(c);
  if(f.avg1y==null) return `<div class="fxc"><div class="fxtop"><b>${esc(FX_LBL[c]||c)}</b></div><div class="fxv num">${wonR(f.rate*m)}원</div><div class="note">1년 평균 계산 자료 부족 — 1% 칸 알림 없음</div></div>`;
  const al=f.alerts||[], last=al[al.length-1], now=last&&last.date===f.asof?last:null, ndn=al.filter(a=>a.dir==='dn').length;
  const pill=now?`<span class="fpill ${now.dir}">새 알림 · ${fxLine(now.line)} ${now.dir==='dn'?'아래로':'위로'}</span>`
                :`<span class="fpill wait">다음 ↓${wonR(f.next_dn*m)} · ↑${wonR(f.next_up*m)}</span>`;
  return `<div class="fxc ${now?now.dir:''}"><div class="fxtop"><b>${esc(FX_LBL[c]||c)}</b>${pill}</div>
    <div class="fxv num">${wonR(f.rate*m)}원${f.chg_pct!=null?`<small>1년 전 ${wonR(f.yago*m)}원 · <span class="${f.chg_pct<=0?'pos':'neg'}">${pctU(f.chg_pct)}</span></small>`:''}</div>
    <div class="fxmeta"><div><span>1년 평균 대비</span><b class="num ${f.dev_pct<=0?'pos':'neg'}">${pctU(f.dev_pct)}</b></div>
      <div><span>다음 내림 알림</span><b class="num pos">${wonR(f.next_dn*m)}원↓</b></div>
      <div><span>다음 오름 알림</span><b class="num neg">${wonR(f.next_up*m)}원↑</b></div></div>
    ${fxGauge(f)}${fxSpark(f,c)}
    <div class="fxcnt">1년 평균 ${wonR(f.avg1y*m)}원 · 지난 1년 알림 ${al.length}번 (내림 ${ndn} · 오름 ${al.length-ndn}) · ${esc(f.asof||'')} 기준</div></div>`;
}
function moreHead(t,sub){ return `<div class="mhead"><span class="mback" onclick="moreOpen(null)">‹ 더보기</span><div><b>${t}</b><span class="ms">${sub}</span></div></div>`; }
function moreFxHtml(){
  const FXD=DATA.fx||{}, al=fxAlertsAll();
  let h=moreHead('💱 환율','현지 통화 1단위의 원화 값 (엔은 100엔) · 갱신 '+esc(DATA.generated_at||''));
  h+=`<div class="card"><h3>최근 알림 <span class="na" style="font-size:var(--fs-2xs)">1년 평균 대비 1% 선을 새로 넘은 날</span></h3>`
    +(al.length?`<div class="frec">${al.slice(0,6).map(a=>`<div><span class="d">${mdTxt(a.date)}</span><i class="${a.dir}"></i><span>${esc(fxAlertTxt(a))}</span></div>`).join('')}</div>`:'<div class="na">지난 1년 알림 없음</div>')+`</div>`;
  const cards=FX_ALERT.filter(c=>FXD[c]).map(c=>fxCard(c,FXD[c])).join('');
  h+=cards?`<div class="fxgrid">${cards}</div>`:'<div class="card"><div class="na">환율 수집 전 — 다음 갱신 후 표시</div></div>';
  h+=`<div class="fleg"><span><i></i>1년 추이</span><span><i class="avg"></i>1년 평균</span><span><i class="ldn"></i>다음 내림 선</span><span><i class="lup"></i>다음 오름 선</span><span><i class="dn"></i>내림 알림</span><span><i class="up"></i>오름 알림</span><span>칸 막대: 눈금 1% · 굵은 눈금 = 1년 평균 · 검은 표시 = 지금 · 파란 구간 = 최근 30일</span></div>`;
  const rest=Object.keys(FXD).filter(c=>FX_ALERT.indexOf(c)<0);
  if(rest.length) h+=`<div class="card"><h3>알림 없이 표시만</h3>${rest.map(c=>{ const f=FXD[c];
    return `<div class="fplain"><span>${esc(FX_LBL[c]||f.name||c)}</span><span class="num">${wonR(f.rate*fxMul(c))}원${f.chg_pct!=null?` <span class="${f.chg_pct<=0?'pos':'neg'}">${pctU(f.chg_pct)}</span> <span class="na">1년 전 대비${f.via?' · '+esc(f.via):''}</span>`:''}</span></div>`; }).join('')}</div>`;
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
const cbPrdS=p=>p?`${p.slice(2,4)}.${+p.slice(4)}Q`:'';
const cbPrev=p=>`${+p.slice(0,4)-1}${p.slice(4)}`;
const cbVal=(k,p)=>{ const s=((KR&&KR.cross_border&&KR.cross_border.series)||{})[k]; return s&&s.values?(s.values[p]??null):null; };
const cbYoy=(c,pv)=>(c!=null&&pv)?(c/pv-1)*100:null;
const CB_CTY=[['cn','🇨🇳 중국'],['us','🇺🇸 미국'],['eu','🇪🇺 유럽'],['jp','🇯🇵 일본']];
function cbBarsHtml(){
  const CB=KR.cross_border, L=CB.last, P=cbPrev(L), g=CB_CAT;
  const rows=CB_CTY.map(([k,nm])=>({k,nm,v:cbVal(k+'|'+g,L),pv:cbVal(k+'|'+g,P)})).filter(r=>r.v!=null);
  const tot=cbVal('total|'+g,L), totP=cbVal('total|'+g,P);
  if(tot!=null&&rows.length){ const sm=rows.reduce((a,r)=>a+r.v,0), sp=rows.every(r=>r.pv!=null)?rows.reduce((a,r)=>a+r.pv,0):null;
    if(tot-sm>0) rows.push({k:'etc',nm:'기타',v:tot-sm,pv:(totP!=null&&sp!=null&&totP-sp>0)?totP-sp:null}); }
  rows.sort((a,b)=>(a.k==='etc')-(b.k==='etc')||b.v-a.v);
  const catNm=((CB.names||{})['total|'+g]||'').split(' / ')[1]||(g==='fashion'?'의류·패션':'스포츠·레저');
  let h=`<h3>나라별 · ${cbPrd(L)}</h3><div class="chips" style="margin-bottom:8px">${[['fashion','의류·패션'],['sports','스포츠·레저']].map(([k,l])=>`<span class="chip${CB_CAT===k?' on':''}" onclick="CB_CAT='${k}';document.getElementById('cbCard').innerHTML=cbBarsHtml()">${l}</span>`).join('')}</div>`;
  if(!rows.length) return h+'<div class="na">자료 없음</div>';
  const mx=Math.max(...rows.map(r=>r.v));
  h+=rows.map(r=>{ const y=cbYoy(r.v,r.pv); return `<div class="cb-row"><span class="lb">${r.nm}</span><div class="bar-wrap"><div class="bar${r.k==='eu'||r.k==='jp'?' cb-src':''}" style="width:${(r.v/mx*100).toFixed(1)}%"></div><span class="bar-val num">${cbMoney(r.v)}</span></div><span class="yy">${y!=null?fmt(y,1,true):'<span class="na">―</span>'}</span></div>`; }).join('');
  return h+`<div class="note">통계청 상품군 '${esc(catNm)}' · 합계 ${cbMoney(tot)}원 · 초록 막대 = 유럽·일본(병행수입 주요 소싱 지역) · 오른쪽 = 전년 같은 분기 대비</div>`;
}
function cbTrendHtml(){
  const S=KR.cross_border.series, out=[];
  [['us','🇺🇸 미국'],['cn','🇨🇳 중국'],['eu','🇪🇺 유럽'],['jp','🇯🇵 일본']].forEach(([k,nm])=>{
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
  let h=moreHead('🌏 해외직구','통계청 온라인쇼핑동향 · 해외직접구매액 · 분기');
  if(!CB||!CB.series) return h+'<div class="card"><div class="na">해외직구 자료 수집 전 — update-kosis 실행 후 표시</div></div>';
  const L=CB.last, P=cbPrev(L);
  const tt=cbVal('total|total',L), tf=cbVal('total|fashion',L);
  const ej=['eu','jp'].map(k=>cbVal(k+'|fashion',L)), ejp=['eu','jp'].map(k=>cbVal(k+'|fashion',P));
  const ejS=ej.every(v=>v!=null)?ej[0]+ej[1]:null, ejP=ejp.every(v=>v!=null)?ejp[0]+ejp[1]:null;
  const kp=(l,v,y,sh)=>`<div class="kpi"><div class="l">${l}</div><div class="v num">${cbMoney(v)}</div><div class="s">${y!=null?fmt(y,1,true):'<span class="na">―</span>'}${sh?' · '+sh:''}</div></div>`;
  h+=`<div class="note" style="margin:0 0 6px">${cbPrd(L)} · 전년 같은 분기 대비</div>`;
  h+=`<div class="kpis cbk">${kp('직구 전체',tt,cbYoy(tt,cbVal('total|total',P)))}${kp('의류·패션',tf,cbYoy(tf,cbVal('total|fashion',P)),(tt&&tf!=null)?'전체의 '+Math.round(tf/tt*100)+'%':'')}${kp('유럽+일본 패션',ejS,cbYoy(ejS,ejP),(tf&&ejS!=null)?'패션의 '+Math.round(ejS/tf*100)+'%':'')}</div>`;
  h+=`<div class="card" id="cbCard">${cbBarsHtml()}</div>`;
  h+=cbTrendHtml();
  h+=`<div class="cb-read"><b>읽는 법</b> — 유럽·일본 패션 직구가 늘면 그 브랜드의 국내 수요는 있다는 뜻이고, 정식 유통보다 싸게 사려는 고객이 직구로 빠진다는 신호이기도 합니다. 병행수입 가격이 직구 가격(관부가세·배송비 포함)보다 경쟁력이 있는지 점검할 때 씁니다.</div>`;
  h+=`<div class="note">출처: KOSIS ${esc(CB.table||'')} ${esc(CB.table_name||'')} · 단위 ${esc(CB.unit||'')}(화면은 억·조원) · 분기가 끝나고 약 2달 뒤 발표 · 갱신 ${esc(KR.generated_at||'')}<br>유럽 = 유럽연합+영국+기타 유럽 합계(통계청 지역 분류)</div>`;
  return h;
}
function moreMenuHtml(){
  const la=fxAlertsAll()[0], CB=KR&&KR.cross_border, late=statusRows().filter(r=>r.late);
  const row=(v,ic,t,d,r)=>`<div class="mi" onclick="moreOpen('${v}')"><span class="mic">${ic}</span><span><span class="mt">${t}</span><br><span class="md">${d}</span></span><span class="mr">${r}</span></div>`;
  return `<div class="mhead"><b>더보기</b></div><div class="card mmenu">
    ${row('fx','💱','환율','엔·유로·달러 1% 칸 알림 · 1년 추이',la?`<span class="mbadge ${la.dir}">${mdTxt(la.date)} 알림</span><br>${FX_SH[la.c]} ${fxLine(la.line)} ${la.dir==='dn'?'↓':'↑'}`:'알림 없음')}
    ${row('cb','🌏','해외직구','나라별·상품군별 직구 금액 (분기)',CB&&CB.last?`<b>${cbPrdS(CB.last)}</b>분기 자료`:'수집 전')}
    ${row('status','⚙️','수집 상태','자료별 마지막 갱신 · 지연 여부',late.length?`<span class="mbadge late">지연 ${late.length}</span>`:'<span class="st-ok">● 정상</span>')}
  </div><div class="note">새 지표는 하단 탭을 늘리지 않고 여기에 추가합니다.</div>`;
}
function buildMore(){
  const el=document.getElementById('moreBody'); if(!el) return;
  el.innerHTML = MORE_VIEW==='fx'?moreFxHtml()
    : MORE_VIEW==='cb'?moreCbHtml()
    : MORE_VIEW==='status'?moreHead('⚙️ 수집 상태','열람 시점 기준 지연 판정')+statusCard()
    : moreMenuHtml();
}
function moreOpen(v){ MORE_VIEW=v; buildMore(); document.getElementById('content').scrollTo(0,0); }
function goMore(v){ sw('more'); moreOpen(v); }

/* ── 탭 / 토글 ── */
function focusCard(id){
  sw('home');
  const el=document.getElementById(id); if(!el) return;
  el.scrollIntoView({behavior:'smooth',block:'start'});
  el.classList.add('flash'); setTimeout(()=>el.classList.remove('flash'),1600);
}
function sw(p){
  if(SRC_SHEET) closeSheet();
  document.querySelectorAll('.tab').forEach(x=>x.classList.toggle('on',x.dataset.p===p));
  document.querySelectorAll('.pane').forEach(x=>x.classList.toggle('on',x.id==='p-'+p));
  if(p!=='co') showCoList();
  document.getElementById('content').scrollTo(0,0);
}
document.querySelectorAll('.tab').forEach(t=>{ t.onclick=()=>{ sw(t.dataset.p); showCoList(); if(t.dataset.p==='more') moreOpen(null); }; });
document.getElementById('coBack').onclick=showCoList;
document.getElementById('coSearch').addEventListener('input',e=>{coQuery=e.target.value.trim().toLowerCase();buildCo();});
document.addEventListener('click',e=>{
  const p=e.target.closest('.pname')||e.target.closest('.bar-row .lb');
  if(p){ p.classList.toggle('open'); return; }
  const r=e.target.closest('tr.mrow');
  if(r){
    r.classList.toggle('open');
    const nx=r.nextElementSibling;
    if(nx&&nx.classList.contains('refrow')) nx.classList.toggle('open');
  }
});

document.getElementById('gen').textContent='갱신: '+DATA.generated_at+' · Yahoo·SEC·DART·KOSIS';
buildHome(); buildCoChips(); buildCo(); buildCal(); buildNewsChips(); buildNews(); buildKR(); buildMore();
</script>
</body>
</html>
"""


def merge_kr_listed(data):
    """국내 상장사 재무를 DART 연결 재무제표로 교체 (야후는 주가·분기YoY·실적일 유지)"""
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
        item["fin_source"] = "DART 연결 재무제표 · " + (e.get("source") or "")
        n += 1
    return n


# 수집 상태: (파일, 표시명, 워크플로우, 주기 표기, 지연 판정 일수)
STATUS_SOURCES = [
    ("data.json", "재무·주가", "update-dashboard", "매일 07:30", 2),
    ("news.json", "뉴스", "update-news", "매일 06:30", 2),
    ("segments.json", "미국 공시 지역·채널", "extract-segments", "매주 월", 9),
    ("segments_ir.json", "유럽·일본 IR", "update-ir", "매주 일", 9),
    ("kr_domestic.json", "국내 법인·상장 재무", "update-dart", "매월 15일", 40),
    ("kosis.json", "국내 소매 지표", "update-kosis", "매월 5일", 40),
    ("naver_trend.json", "네이버 검색 관심도", "update-dashboard", "매일 07:30", 2),
]


def _ts_iso(v):
    """'2026-10-01 11:22 KST' / '2026-09-30' → ISO(+09:00), 실패 시 None"""
    m = re.match(r"(\d{4}-\d{2}-\d{2})(?:[ T](\d{2}):(\d{2}))?", str(v or ""))
    if not m:
        return None
    return f"{m.group(1)}T{m.group(2) or '00'}:{m.group(3) or '00'}:00+09:00"


def collect_status():
    out = []
    for fn, label, wf, cad, limit in STATUS_SOURCES:
        ts, date_only = None, False
        p = os.path.join("docs", fn)
        if os.path.exists(p):
            try:
                with open(p, encoding="utf-8") as f:
                    d = json.load(f)
                raw = str(d.get("generated_at") or d.get("updated_at") or "")
                ts = _ts_iso(raw)
                date_only = not re.search(r"\d{2}:\d{2}", raw)
            except Exception:
                pass
        out.append({"file": fn, "label": label, "wf": wf, "cadence": cad, "limit": limit,
                    "ts": ts, "date_only": date_only})
    return {"sources": out}


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
                krd = json.load(f)
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
    news = None
    if os.path.exists("docs/news.json"):
        try:
            with open("docs/news.json", encoding="utf-8") as f:
                news = json.load(f)
        except Exception:
            pass
    html = (TEMPLATE
            .replace("__DATA__", json.dumps(data, ensure_ascii=False))
            .replace("__SEGS__", json.dumps(segs, ensure_ascii=False))
            .replace("__NEWS__", json.dumps(news, ensure_ascii=False))
            .replace("__KR__", json.dumps(kr, ensure_ascii=False))
            .replace("__NAVER__", json.dumps(naver, ensure_ascii=False))
            .replace("__HIST__", json.dumps(hist, ensure_ascii=False))
            .replace("__KRD__", json.dumps(krd, ensure_ascii=False))
            .replace("__SEGS_IR__", json.dumps(segs_ir, ensure_ascii=False))
            .replace("__STATUS__", json.dumps(collect_status(), ensure_ascii=False))
            .replace("__WMAP__", json.dumps(wmap, ensure_ascii=False)))
    with open("docs/index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("saved docs/index.html")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
sports-industry-monitor — 단일 HTML 대시보드 빌드
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

</main>
<nav class="tabs">
  <div class="tab on" data-p="home"><span class="ic">🏠</span>종합</div>
  <div class="tab" data-p="co"><span class="ic">🏢</span>기업</div>
  <div class="tab" data-p="cal"><span class="ic">📅</span>캘린더</div>
  <div class="tab" data-p="news"><span class="ic">📰</span>뉴스</div>
  <div class="tab" data-p="kr"><span class="ic">🇰🇷</span>국내</div>
</nav>
</div>
<script>
const DATA = __DATA__;
const SEGS = __SEGS__;
const NEWS = __NEWS__;
const KR = __KR__;
const HIST = __HIST__;
const KRD = __KRD__;   // 국내 법인(비상장) — 연 1회 수동 갱신

/* ── 브랜드 로고 도메인 ── */
const DOMAINS = {
  "NKE":"nike.com", "ADS.DE":"adidas.com", "ONON":"on.com",
  "DECK":"hoka.com", "AS":"amersports.com", "LULU":"lululemon.com",
  "7936.T":"asics.com", "BIRK":"birkenstock.com", "CROX":"crocs.com",
  "VFC":"vfc.com", "UAA":"underarmour.com",
  "8022.T":"mizuno.com", "7906.T":"yonex.com", "8111.T":"goldwin.co.jp",
  "2020.HK":"anta.com", "2331.HK":"lining.com", "PUM.DE":"puma.com",
  "WWW":"wolverineworldwide.com", "COLM":"columbia.com",
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
  "krd:blackyak":"blackyak.com", "krd:nepa":"nepa.co.kr", "krd:shinsung":"shinsungtongsang.com"
};
/* ── 브랜드 본사 국가 국기 ── */
const FLAGS = {
  "NKE":"🇺🇸", "ADS.DE":"🇩🇪", "ONON":"🇨🇭", "DECK":"🇺🇸", "AS":"🇫🇮",
  "LULU":"🇨🇦", "7936.T":"🇯🇵", "BIRK":"🇩🇪", "CROX":"🇺🇸", "VFC":"🇺🇸",
  "UAA":"🇺🇸", "8022.T":"🇯🇵", "7906.T":"🇯🇵", "8111.T":"🇯🇵",
  "2020.HK":"🇨🇳", "2331.HK":"🇨🇳", "PUM.DE":"🇩🇪", "WWW":"🇺🇸",
  "COLM":"🇺🇸", "DKS":"🇺🇸", "JD.L":"🇬🇧", "ASO":"🇺🇸"
};
const GROUPS = (DATA.group_order && DATA.group_order.length) ? DATA.group_order
  : ["글로벌 브랜드","글로벌 유통","국내 브랜드","국내 패션대기업","국내 OEM","국내 유통"];
const GROUP_ICON = {"글로벌 브랜드":"🌍","글로벌 유통":"🌍","국내 브랜드":"🇰🇷","국내 패션대기업":"🇰🇷","국내 OEM":"🇰🇷","국내 유통":"🇰🇷"};
const GROUP_NOTE = {"국내 OEM":"브랜드 오더의 선행지표","삼성물산(패션부문)":""};
const isKR = t => /\.K[SQ]$/.test(t);
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
      rev:fy.rev, cur:x.currency, rev_yoy:fy.rev_yoy, gm:fy.gm_pct, q_yoy:x.latest_q_yoy,
      inv_yoy:x.inv_yoy, earn:x.earn_date, note:x.note, item:x});
  });
  ((KRD&&KRD.entities)||[]).forEach(e=>{
    const ys=(e.years||[]).filter(y=>y.rev!=null); const last=ys[ys.length-1], prev=ys[ys.length-2];
    const yoy=(last&&prev&&prev.rev)?(last.rev/prev.rev-1)*100:null;
    const opm=(last&&last.op!=null&&last.rev)?last.op/last.rev*100:null;
    const gmk=(last&&last.cogs!=null&&last.rev)?(last.rev-last.cogs)/last.rev*100:null;
    const invy=(last&&prev&&last.inv&&prev.inv)?(last.inv/prev.inv-1)*100:null;
    out.push({key:'krd:'+e.id, name:e.name, group:'국내 법인', flag:'🇰🇷', logo:logoImg('krd:'+e.id,false,e.name), listed:false,
      rev:last?last.rev:null, cur:'KRW', rev_yoy:yoy, gm:gmk, opm, q_yoy:null, inv_yoy:invy, earn:null,
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
  const rk=(r,valHtml)=>`<div class="rk" onclick="goDetail('${r.key}')"><span>${r.logo}${esc(r.name)}<span class="g">${esc(r.group)}${r.basis?' · '+r.basis:''}</span></span>${valHtml}</div>`;
  h+=`<div class="card"><h3>성장 상위 · 매출 전년 대비 <span class="go" onclick="sw('co')">기업 ▸</span></h3>${up.map(r=>rk(r,`<b class="pos">${fmt(r.g,1,true)}</b>`)).join('')||'<div class="na">―</div>'}${outlier.length?`<div class="note">순위 제외(±100% 초과, 기저·인수 효과 가능): ${outlier.map(r=>esc(r.name)+' '+fmt(r.g,0,true)).join(' · ')}</div>`:''}</div>`;
  h+=`<div class="card"><h3>성장 하위 · 매출 전년 대비</h3>${dn.map(r=>rk(r,`<b>${fmt(r.g,1,true)}</b>`)).join('')||'<div class="na">―</div>'}</div>`;
  h+=`<div class="card" id="warnCard"><h3>재고 경고 · 재고 증가율이 매출 증가율보다 높은 곳 <span class="na" style="margin-left:auto;font-size:var(--fs-2xs)">기업을 누르면 상세</span></h3>${warn.slice(0,8).map(r=>rk(r,`<span>재고 <b class="neg">${fmt(r.inv_yoy,1,true)}</b> · 매출 ${fmt(r.rev_yoy,1,true)}</span>`)).join('')||'<div class="na">해당 없음</div>'}</div>`;
  h+=`<div class="card"><h3>다가오는 실적 발표 <span class="go" onclick="sw('cal')">캘린더 ▸</span></h3>${ev.slice(0,5).map(r=>rk(r,`<span>${r.dn<=7?'🔴':'⚪'} D-${r.dn} · ${r.d.getMonth()+1}/${r.d.getDate()}</span>`)).join('')||'<div class="na">90일 내 일정 없음</div>'}</div>`;
  document.getElementById('homeBody').innerHTML=h;
}

/* ── 기업 (A안: 검색·칩·압축 표·행 펼침) ── */
let coFilter='전체', coQuery='';
function buildCoChips(){
  const rows=rows_all();
  const chips=[['전체',rows.length],...CO_GROUPS.map(g=>[g,rows.filter(r=>r.group===g).length]).filter(x=>x[1]>0)];
  document.getElementById('coChips').innerHTML=chips.map(([g,n])=>`<span class="chip ${coFilter===g?'on':''}" data-g="${g}">${g==='전체'?'전체':(GROUP_ICON[g]||'🇰🇷')+' '+g} ${n}</span>`).join('');
  document.querySelectorAll('#coChips .chip').forEach(c=>c.onclick=()=>{coFilter=c.dataset.g;buildCoChips();buildCo();});
}
function buildCo(){
  const rows=rows_all().filter(r=>(coFilter==='전체'||r.group===coFilter)&&(!coQuery||r.name.toLowerCase().includes(coQuery)||r.key.toLowerCase().includes(coQuery)));
  let h=`<tr><th>기업</th><th>매출</th><th>전년 대비</th><th>총이익률</th><th>재고 증감</th></tr>`;
  rows.forEach(r=>{
    const gmCell=(r.gm!=null)?r.gm.toFixed(1)+'%':(r.opm!=null?r.opm.toFixed(1)+'%<span class="na" style="font-size:var(--fs-2xs)"> 영업</span>':'<span class="na">―</span>');
    h+=`<tr class="co" data-k="${r.key}"><td>${r.logo}${esc(r.name)}</td><td>${moneyShort(r.rev,r.cur)}</td><td>${fmt(r.rev_yoy,1,true)}</td><td>${gmCell}</td><td>${fmt(r.inv_yoy,1,true)}</td></tr>`;
    let mini='';
    if(r.listed){
      const x=r.item, s=segOf(r.key);
      const reg=(s&&s.extract.regions||[]).filter(z=>z.revenue!=null); const tot=reg.reduce((a,b)=>a+b.revenue,0);
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
      mini=`<div class="mini"><div>구분: ${esc(r.route==='none'?'DART 공시 미발견':'DART 감사보고서(연간)')}</div><div>기준: ${r.fy_end?ym(r.fy_end)+' 결산':'―'}</div>${r.note?`<div style="grid-column:1/3" class="na">${esc(r.note)}</div>`:''}</div>`;
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
    return {name:r.name, cur:r.revenue, prev, derived, yoy:r.yoy_pct};
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
    h+=`</div>`;
  });
  return h;
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
  h+=`<table><tr><th>결산</th><th>매출</th><th>전년 대비</th><th>영업률</th><th>순이익</th><th>재고</th><th>재고 증감</th></tr>`;
  ys.forEach((y,i)=>{
    const p=i>0?ys[i-1]:null;
    const yoy=(y.rev!=null&&p&&p.rev)?(y.rev/p.rev-1)*100:null;
    const opm=(y.op!=null&&y.rev)?y.op/y.rev*100:null;
    const iy=(y.inv&&p&&p.inv)?(y.inv/p.inv-1)*100:null;
    h+=`<tr><td>${y.fy} <span class="na">${ym(y.end)}</span></td>
      <td>${y.rev!=null?moneyShort(y.rev,'KRW'):'―'}</td><td>${fmt(yoy,1,true)}</td>
      <td>${opm!=null?opm.toFixed(1)+'%':'―'}</td>
      <td>${y.ni!=null?moneyShort(y.ni,'KRW'):'―'}</td>
      <td>${y.inv!=null?moneyShort(y.inv,'KRW'):'―'}</td><td>${fmt(iy,1,true)}</td></tr>`;
  });
  h+=`</table>`;
  const srcs=ys.filter(y=>y.source).map(y=>y.fy+': '+y.source);
  if(srcs.length) h+=`<div class="src">출처: ${esc(srcs.join(' · '))}</div>`;
  h+=`<div class="note">별도(개별) 재무제표 · 원화 · 연간 — 글로벌 실적과 회계기간·기준이 다를 수 있음</div></div>`;
  return h;
}
function renderKrdDetail(id){
  const e=((KRD&&KRD.entities)||[]).find(z=>z.id===id);
  if(!e){ document.getElementById('detBody').innerHTML='<div class="na">미확인</div>'; return; }
  let h=`<div class="det-head">${logoImg('krd:'+e.id,true,e.name)}${esc(e.name)} <span class="tk">🇰🇷</span> <span class="tag">${esc(e.type)}</span></div>`;
  h+=krdCard(e,false);
  if(e.link){
    const g=DATA.items.find(i=>i.ticker===e.link);
    if(g) h+=`<div class="note">글로벌 본사: <a href="#" onclick="goDetail('${e.link}');return false;" style="color:var(--accent)">${logoImg(e.link,false,g.name)}${esc(g.name)} ▸</a></div>`;
  }
  document.getElementById('detBody').innerHTML=h;
}
function renderDetail(t){
  if(String(t).startsWith('krd:')){ renderKrdDetail(t.slice(4)); return; }
  const x=DATA.items.find(i=>i.ticker===t);
  const cur=x.currency||'';
  let h=`<div class="det-head">${logoImg(x.ticker,true,x.name)}${x.name} <span class="tk">${flagOf(x.ticker)} ${x.ticker}</span> <span class="tag">${esc(x.group||'')}</span></div>`;
  if(x.note) h+=`<div class="note" style="margin:-6px 0 12px">ℹ️ ${esc(x.note)}</div>`;
  if(x.fin_source) h+=`<div class="src" style="margin:-4px 0 10px">재무: ${esc(x.fin_source)} · 주가·분기 매출 전년 대비·실적일: Yahoo</div>`;
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
  <div class="kv"><span class="k">재고/매출 비율</span><span>${x.inv_sales_pct!=null?x.inv_sales_pct.toFixed(1)+'%':'―'}</span></div></div>`;

  /* 연결된 국내 법인 (Phase 6) */
  ((KRD&&KRD.entities)||[]).filter(e=>e.link===t).forEach(e=>{ h+=krdCard(e,true); });

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
  h+=`<div class="card"><h3>🌍 지역 분해 — 최근 분기, 당기 vs 전년 <span class="tag">공시 추출</span></h3>`;
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
    let noteTxt="기준: "+(s.extract.period||"―");
    if(s.extract.prev_period) noteTxt+=" · 전년: "+s.extract.prev_period;
    if(s.extract.notes) noteTxt+=" · "+s.extract.notes;
    h+=`<div class="note">${noteTxt}<br>진한 바=당기 / 연한 바=전년 · [역산]=공시에 전년 수치 미기재로 YoY에서 계산(§29-D 구분)</div>`;
    if(s.source) h+=`<div class="src">출처: ${s.source}</div>`;
  } else {
    h+=`<div class="na">미확인${segEntry&&segEntry.error?'('+segEntry.error+')':'(공시에 지역 분해 미기재)'}</div>`;
  }
  h+=`</div>`;
  h+=`<div class="card"><h3>🛒 채널 분해 (DTC/도매) — 최근 분기 <span class="tag">공시 추출</span></h3>`;
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
  <div class="kv"><span class="k">현재가</span><span>${x.price!=null?x.price.toFixed(2)+' '+cur:'―'}</span></div>
  <div class="kv"><span class="k">52주 고점比</span><span>${fmt(x.off_high_pct,1,true)}</span></div></div>`;
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
  if(!items.length){ el.innerHTML='<div class="na">해당 구분의 최근 14일 뉴스 없음</div>'; return; }
  let h=`<div class="note" style="margin:0 0 6px">수집: ${NEWS.generated_at||'―'} · ${items.length}건</div>`;
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
function buildKR(){
  const el=document.getElementById('krBody');
  if(!KR||!KR.series||!Object.keys(KR.series).length){
    el.innerHTML='<div class="na">국내 지표 없음 — 수집 워크플로우(update-kosis) 첫 실행 전이거나 조회 실패(미확인)</div>';
    return;
  }
  let h=`<div class="note" style="margin:0 0 8px">갱신: ${KR.generated_at||'―'}</div>`;
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
  el.querySelectorAll('.krcard').forEach(c=>{
    c.onclick=()=>document.getElementById('krt-'+c.dataset.k).classList.toggle('open');
  });
}

/* ── 탭 / 토글 ── */
function focusCard(id){
  sw('home');
  const el=document.getElementById(id); if(!el) return;
  el.scrollIntoView({behavior:'smooth',block:'start'});
  el.classList.add('flash'); setTimeout(()=>el.classList.remove('flash'),1600);
}
function sw(p){
  document.querySelectorAll('.tab').forEach(x=>x.classList.toggle('on',x.dataset.p===p));
  document.querySelectorAll('.pane').forEach(x=>x.classList.toggle('on',x.id==='p-'+p));
  if(p!=='co') showCoList();
  document.getElementById('content').scrollTo(0,0);
}
document.querySelectorAll('.tab').forEach(t=>{ t.onclick=()=>{ sw(t.dataset.p); showCoList(); }; });
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
buildHome(); buildCoChips(); buildCo(); buildCal(); buildNewsChips(); buildNews(); buildKR();
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
            .replace("__HIST__", json.dumps(hist, ensure_ascii=False))
            .replace("__KRD__", json.dumps(krd, ensure_ascii=False)))
    with open("docs/index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("saved docs/index.html")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
sports-industry-monitor — 단일 HTML 대시보드 빌드
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
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
<title>스포츠 산업 모니터</title>
<style>
:root{
  --bg:#f4f6fa;--card:#ffffff;--line:#dde3ee;--tx:#1c2433;
  --sub:#5f6b80;--pos:#0e9f4f;--neg:#d92d2d;--accent:#2563eb;
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
body{background:var(--bg);color:var(--tx);font-family:-apple-system,'Apple SD Gothic Neo','Malgun Gothic',sans-serif;font-size:var(--fs-base);line-height:1.45;padding-bottom:40px}
header{padding:16px;border-bottom:1px solid var(--line);display:flex;align-items:flex-start}
header h1{font-size:var(--fs-xl);font-weight:700}
header .sub{color:var(--sub);font-size:var(--fs-xs);margin-top:4px}
#themeBtn{margin-left:auto;background:var(--card);border:1px solid var(--line);color:var(--tx);
border-radius:10px;padding:8px 12px;font-size:var(--fs-lg);cursor:pointer}
.tabs{display:flex;border-bottom:1px solid var(--line);position:sticky;top:0;background:var(--bg);z-index:5}
.tab{flex:1;text-align:center;padding:12px 0;color:var(--sub);font-size:var(--fs-base);cursor:pointer}
.tab.on{color:var(--accent);border-bottom:2px solid var(--accent);font-weight:600}
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
<header>
  <div>
    <h1>🏭 스포츠 산업 모니터</h1>
    <div class="sub" id="gen"></div>
  </div>
  <button id="themeBtn" title="테마 전환">🌙</button>
</header>
<div class="tabs">
  <div class="tab on" data-p="sum">서머리</div>
  <div class="tab" data-p="det">브랜드 상세</div>
  <div class="tab" data-p="cal">캘린더</div>
  <div class="tab" data-p="news">뉴스</div>
  <div class="tab" data-p="kr">국내</div>
</div>

<div class="pane on" id="p-sum">
  <table id="sumTbl"></table>
  <div class="note">FY매출·YoY·GM은 연간, 분기YoY는 최근 분기 기준입니다. 행을 누르면 기준 시점(결산월·분기말·재고 기준월·통화)이 펼쳐지고, 종목명 옆 ▸ 아이콘을 누르면 상세로 이동합니다.<br>
  국기 = 브랜드 본사 국가 · "―" = 미확인(소스 미제공, §29-D) · [공시] = 공시 추출값 · 52주比는 브랜드 상세에서 확인(부지표)</div>
</div>

<div class="pane" id="p-det">
  <select id="sel"></select>
  <div id="detBody"></div>
</div>

<div class="pane" id="p-cal">
  <div id="calBody"></div>
  <div class="note">일정 미표시 종목은 소스 미제공(미확인). 🔴 = D-7 이내</div>
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
  "023530.KS":"lotteshopping.com", "004170.KS":"shinsegae.com", "069960.KS":"ehyundai.com"
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
function logoImg(t, large){
  const d = DOMAINS[t];
  if(!d) return "";
  const cls = large ? "logo-lg" : "logo";
  return `<img class="${cls}" loading="lazy" alt="" onerror="this.remove()"
    src="https://www.google.com/s2/favicons?domain=${d}&sz=64">`;
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

/* ── 서머리 ── */
function buildSummary(){
  let h=`<tr><th>종목</th><th>FY매출</th><th>YoY</th><th>GM</th><th>분기YoY</th><th>재고YoY</th></tr>`;
  GROUPS.forEach(g=>{
    const rows=DATA.items.filter(x=>x.group===g);
    if(!rows.length) return;
    const gn=GROUP_NOTE[g]?` <span class="na">· ${GROUP_NOTE[g]}</span>`:'';
    h+=`<tr class="grp ${isKR(rows[0].ticker)?'grp-kr':''}"><td colspan="6">${GROUP_ICON[g]||'━'} <b>${g}</b>${gn} <span class="na">(${rows.length})</span></td></tr>`;
    rows.forEach(x=>{
      const fy=x.fy.length?x.fy[x.fy.length-1]:{};
      const refs=[];
      if(fy.end) refs.push("FY "+ym(fy.end));
      if(x.q_end) refs.push("분기 "+ym(x.q_end));
      if(x.inv_date) refs.push("재고 "+ym(x.inv_date));
      if(x.currency) refs.push(x.currency);
      h+=`<tr class="mrow"><td class="nm">${flagOf(x.ticker)}${logoImg(x.ticker,false)}${x.name}
      <span class="na" style="cursor:pointer" onclick="event.stopPropagation();goDetail('${x.ticker}')">▸</span></td>
      <td class="rev-main">${moneyShort(fy.rev,x.currency)}</td>
      <td>${fmt(fy.rev_yoy,1,true)}</td>
      <td>${fy.gm_pct!=null?fy.gm_pct.toFixed(1)+'%':'<span class="na">―</span>'}</td>
      <td>${fmt(x.latest_q_yoy,1,true)}</td>
      <td>${fmt(x.inv_yoy,1,true)}</td></tr>`;
      h+=`<tr class="refrow"><td colspan="6">기준: ${refs.length?refs.join(' · '):'미확인'}</td></tr>`;
      if(x.ticker==='DKS'){
        const s=segOf('DKS');
        const subs=(s&&s.extract.sub_segments)?s.extract.sub_segments:[];
        subs.forEach(ss=>{
          const label=ss.name==="DICK'S"?'딕스(본체)':'풋락커(부문)';
          const comp=(ss.proforma_comp_pct!=null)
            ?` · comp ${ss.proforma_comp_pct>=0?'+':''}${ss.proforma_comp_pct.toFixed(1)}%`:'';
          h+=`<tr class="subrow"><td>└ ${label} <span class="tag">공시</span></td>
          <td colspan="3">매출 ${segMoney(ss.revenue)} ${ss.yoy_pct!=null?('('+(ss.yoy_pct>=0?'+':'')+ss.yoy_pct.toFixed(1)+'%)'):''}${comp}</td>
          <td colspan="2">재고 ${segMoney(ss.inventory)}</td></tr>`;
        });
      }
    });
  });
  /* 국내 법인(비상장) — 연 1회 DART 수동 갱신 */
  const ents=(KRD&&KRD.entities)?KRD.entities:[];
  if(ents.length){
    h+=`<tr class="grp grp-kr"><td colspan="6">🇰🇷 <b>국내 법인 (비상장·DART)</b> <span class="na">· DART 자동 수집 (${ents.length})</span></td></tr>`;
    ents.forEach(e=>{
      const ys=(e.years||[]).filter(y=>y.rev!=null);
      const last=ys.length?ys[ys.length-1]:null;
      const prev=ys.length>1?ys[ys.length-2]:null;
      const yoy=(last&&prev&&prev.rev)?(last.rev/prev.rev-1)*100:null;
      const opm=(last&&last.op!=null&&last.rev)?last.op/last.rev*100:null;
      h+=`<tr class="mrow"><td class="nm">🇰🇷 ${esc(e.name)}
        <span class="na" style="cursor:pointer" onclick="event.stopPropagation();goDetail('krd:${e.id}')">▸</span></td>
      <td class="rev-main">${last?moneyShort(last.rev,'KRW'):'<span class="na">―</span>'}</td>
      <td>${fmt(yoy,1,true)}</td>
      <td>${opm!=null?opm.toFixed(1)+'%<div class="ref">영업률</div>':'<span class="na">―</span>'}</td>
      <td><span class="na">―</span></td>
      <td><span class="na">―</span></td></tr>`;
      h+=`<tr class="refrow"><td colspan="6">기준: ${last?('FY '+ym(last.end)):(e.route==='none'?'DART 공시 미발견':'수집 대기')} · KRW · DART(연간·별도) · ${esc(e.type)}${e.note?' · '+esc(e.note):''}</td></tr>`;
    });
  }
  document.getElementById('sumTbl').innerHTML=h;
}

/* ── 상세 ── */
function buildSelect(){
  const s=document.getElementById('sel');
  s.innerHTML=GROUPS.map(g=>{
    const rows=DATA.items.filter(x=>x.group===g);
    if(!rows.length) return '';
    return `<optgroup label="${GROUP_ICON[g]||''} ${g}">`+rows.map(x=>`<option value="${x.ticker}">${(FLAGS[x.ticker]||(isKR(x.ticker)?'🇰🇷':''))} ${x.name} (${x.ticker})</option>`).join('')+`</optgroup>`;
  }).join('');
  const ents=(KRD&&KRD.entities)?KRD.entities:[];
  if(ents.length){
    s.innerHTML+=`<optgroup label="🇰🇷 국내 법인 (비상장·DART)">`+ents.map(e=>`<option value="krd:${e.id}">🇰🇷 ${e.name}</option>`).join('')+`</optgroup>`;
  }
  s.onchange=()=>renderDetail(s.value);
  renderDetail(DATA.items[0].ticker);
}
function goDetail(t){
  document.querySelector('.tab[data-p=det]').click();
  document.getElementById('sel').value=t;
  renderDetail(t);
}

/* 페어 바: 당기 vs 전년 (전년 미기재 시 YoY 역산 + [역산] 태그) */
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
  h+=`<table><tr><th>결산</th><th>매출</th><th>YoY</th><th>영업이익</th><th>영업률</th><th>순이익</th></tr>`;
  ys.forEach((y,i)=>{
    const p=i>0?ys[i-1]:null;
    const yoy=(y.rev!=null&&p&&p.rev)?(y.rev/p.rev-1)*100:null;
    const opm=(y.op!=null&&y.rev)?y.op/y.rev*100:null;
    h+=`<tr><td>${y.fy} <span class="na">${ym(y.end)}</span></td>
      <td>${y.rev!=null?moneyShort(y.rev,'KRW'):'―'}</td><td>${fmt(yoy,1,true)}</td>
      <td>${y.op!=null?moneyShort(y.op,'KRW'):'―'}</td><td>${opm!=null?opm.toFixed(1)+'%':'―'}</td>
      <td>${y.ni!=null?moneyShort(y.ni,'KRW'):'―'}</td></tr>`;
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
  let h=`<div class="det-head">🇰🇷 ${esc(e.name)} <span class="tag">${esc(e.type)}</span></div>`;
  h+=krdCard(e,false);
  if(e.link){
    const g=DATA.items.find(i=>i.ticker===e.link);
    if(g) h+=`<div class="note">글로벌 본사: <a href="#" onclick="goDetail('${e.link}');return false;" style="color:var(--accent)">${flagOf(e.link)}${esc(g.name)} ▸</a></div>`;
  }
  document.getElementById('detBody').innerHTML=h;
}
function renderDetail(t){
  if(String(t).startsWith('krd:')){ renderKrdDetail(t.slice(4)); return; }
  const x=DATA.items.find(i=>i.ticker===t);
  const cur=x.currency||'';
  let h=`<div class="det-head">${flagOf(x.ticker)}${logoImg(x.ticker,true)}${x.name} <span class="tk">${x.ticker}</span> <span class="tag">${esc(x.group||'')}</span></div>`;
  if(x.note) h+=`<div class="note" style="margin:-6px 0 12px">ℹ️ ${esc(x.note)}</div>`;
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
  h+=`<div class="card"><h3>💰 수익성 추이 — 연간</h3><table><tr><th>결산월</th><th>GM</th><th>영업이익률</th></tr>`;
  x.fy.forEach(y=>{
    h+=`<tr><td>${ym(y.end)}</td>
    <td>${y.gm_pct!=null?y.gm_pct.toFixed(1)+'%':'―'}</td>
    <td>${y.op_pct!=null?y.op_pct.toFixed(1)+'%':'―'}</td></tr>`;
  });
  h+=`</table></div>`;
  h+=`<div class="card"><h3>📦 재고</h3>
  <div class="kv"><span class="k">기준 시점</span><span>${x.inv_date||'―'}${x.inv_prev_date?' (전년비교: '+x.inv_prev_date+')':''}</span></div>
  <div class="kv"><span class="k">재고자산</span><span>${money(x.inventory,cur)}</span></div>
  <div class="kv"><span class="k">재고 YoY</span><span>${fmt(x.inv_yoy,1,true)}</span></div>
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

/* ── 캘린더 ── */
function buildCal(){
  const today=new Date(); today.setHours(0,0,0,0);
  const rows=DATA.items.filter(x=>x.earn_date).map(x=>{
    const d=new Date(x.earn_date+'T00:00:00');
    return {t:x.ticker,n:x.name,d,dn:Math.round((d-today)/86400000)};
  }).filter(r=>r.dn>=0&&r.dn<=90).sort((a,b)=>a.dn-b.dn);
  let h='';
  rows.forEach(r=>{
    h+=`<div class="cal-item"><div class="dn ${r.dn<=7?'hot':''}">${r.dn<=7?'🔴':'⚪'} D-${r.dn}</div>
    <div>${flagOf(r.t)}${logoImg(r.t,false)}${r.n}</div><div class="dt">${(r.d.getMonth()+1)}/${r.d.getDate()}</div></div>`;
  });
  if(!rows.length) h='<div class="na">90일 이내 확인된 일정 없음(미확인 포함)</div>';
  document.getElementById('calBody').innerHTML=h;
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
document.querySelectorAll('.tab').forEach(t=>{
  t.onclick=()=>{
    document.querySelectorAll('.tab').forEach(x=>x.classList.remove('on'));
    document.querySelectorAll('.pane').forEach(x=>x.classList.remove('on'));
    t.classList.add('on');
    document.getElementById('p-'+t.dataset.p).classList.add('on');
  };
});
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

document.getElementById('gen').textContent='갱신: '+DATA.generated_at+' · 데이터: Yahoo Finance + SEC 공시(추출)';
buildSummary(); buildSelect(); buildCal(); buildNewsChips(); buildNews(); buildKR();
</script>
</body>
</html>
"""


def main():
    with open("docs/data.json", encoding="utf-8") as f:
        data = json.load(f)
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

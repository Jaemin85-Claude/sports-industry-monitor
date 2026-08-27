# -*- coding: utf-8 -*-
"""
sports-industry-monitor — 단일 HTML 대시보드 빌드
v8: 서머리 한 줄 셀(FY매출/YoY 컬럼 분리, 52주比 제거→상세로, 행 클릭 시
    기준 시점·통화 표시) + 지역/채널 당기vs전년 페어 바(비중 변화 병기,
    전년 미기재 시 YoY 역산 + [역산] 태그, §29-D 구분)
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
}
[data-theme="dark"]{
  --bg:#0f1420;--card:#1a2233;--line:#2a3550;--tx:#e8ecf4;--sub:#8b96ad;
  --pos:#3ddc84;--neg:#ff6b6b;--accent:#4d9fff;--accent-prev:#3a4a68;--barbg:#0c101a;
}
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}
body{background:var(--bg);color:var(--tx);font-family:-apple-system,'Apple SD Gothic Neo','Malgun Gothic',sans-serif;font-size:14px;padding-bottom:40px}
header{padding:16px;border-bottom:1px solid var(--line);display:flex;align-items:flex-start}
header h1{font-size:17px}
header .sub{color:var(--sub);font-size:11px;margin-top:4px}
#themeBtn{margin-left:auto;background:var(--card);border:1px solid var(--line);color:var(--tx);
border-radius:10px;padding:8px 12px;font-size:15px;cursor:pointer}
.tabs{display:flex;border-bottom:1px solid var(--line);position:sticky;top:0;background:var(--bg);z-index:5}
.tab{flex:1;text-align:center;padding:12px 0;color:var(--sub);font-size:13px;cursor:pointer}
.tab.on{color:var(--accent);border-bottom:2px solid var(--accent);font-weight:600}
.pane{display:none;padding:12px}
.pane.on{display:block}
table{width:100%;border-collapse:collapse;font-size:12px}
th{color:var(--sub);font-weight:500;padding:8px 4px;text-align:right;border-bottom:1px solid var(--line);font-size:11px}
th:first-child,td:first-child{text-align:left}
td{padding:9px 4px;text-align:right;border-bottom:1px solid var(--line)}
tr.grp td{color:var(--sub);font-size:11px;padding:10px 4px 4px;border-bottom:none}
tr.subrow td{font-size:11px;color:var(--sub)}
tr.subrow td:first-child{padding-left:26px}
tr.mrow{cursor:pointer}
tr.mrow.open td{border-bottom:none}
tr.refrow{display:none}
tr.refrow.open{display:table-row}
tr.refrow td{font-size:10px;color:var(--sub);padding:2px 4px 8px;text-align:left;border-bottom:1px solid var(--line)}
.pos{color:var(--pos)}.neg{color:var(--neg)}.na{color:var(--sub)}
.nm{font-weight:600;white-space:nowrap}
.rev-main{font-weight:600}
.logo{width:18px;height:18px;border-radius:4px;vertical-align:-4px;margin-right:6px;background:#fff;border:1px solid var(--line);object-fit:contain}
.logo-lg{width:28px;height:28px;border-radius:6px;vertical-align:-8px;margin-right:8px;background:#fff;border:1px solid var(--line);object-fit:contain}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px;margin-bottom:12px}
.card h3{font-size:13px;color:var(--sub);margin-bottom:10px;font-weight:500}
.det-head{font-size:16px;font-weight:700;margin-bottom:12px}
.tag{display:inline-block;font-size:10px;color:var(--accent);border:1px solid var(--accent);
border-radius:6px;padding:1px 6px;margin-left:6px;vertical-align:1px}
.tag2{display:inline-block;font-size:9px;color:var(--sub);border:1px solid var(--sub);
border-radius:6px;padding:0 5px;margin-left:4px}
select{width:100%;padding:12px;background:var(--card);color:var(--tx);border:1px solid var(--line);border-radius:10px;font-size:15px;margin-bottom:12px}
.bar-row{display:flex;align-items:center;margin-bottom:8px;font-size:12px}
.bar-row .lb{width:72px;color:var(--sub);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;flex-shrink:0;cursor:pointer}
.bar-row .lb.open{width:auto;max-width:60%;white-space:normal;overflow:visible;word-break:break-word;padding-right:6px}
.bar-wrap{flex:1;background:var(--barbg);border-radius:4px;height:22px;position:relative;min-width:60px}
.bar{height:100%;border-radius:4px;background:var(--accent);opacity:.85}
.bar-val{position:absolute;right:6px;top:0;line-height:22px;font-size:11px;color:var(--tx)}
/* 페어 바 */
.pair{margin-bottom:14px}
.pair .pname{font-size:12px;font-weight:600;margin-bottom:4px;cursor:pointer;
white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.pair .pname.open{white-space:normal;overflow:visible}
.prow{display:flex;align-items:center;margin-bottom:3px;font-size:11px}
.prow .yr{width:38px;color:var(--sub);font-size:10px;flex-shrink:0}
.prow .pw{flex:1;background:var(--barbg);border-radius:4px;height:18px;position:relative;min-width:50px}
.prow .pb{height:100%;border-radius:4px}
.pb.now{background:var(--accent);opacity:.9}
.pb.prev{background:var(--accent-prev)}
.prow .pv{position:absolute;right:6px;top:0;line-height:18px;font-size:10px;color:var(--tx);white-space:nowrap}
.kv{display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid var(--line);font-size:13px}
.kv:last-child{border-bottom:none}
.kv .k{color:var(--sub)}
.note{color:var(--sub);font-size:11px;margin-top:10px;line-height:1.6}
.src{color:var(--sub);font-size:10px;margin-top:8px;word-break:break-all}
.cal-item{display:flex;align-items:center;padding:12px;background:var(--card);border:1px solid var(--line);border-radius:10px;margin-bottom:8px;font-size:13px}
.cal-item .dn{width:56px;font-weight:700}
.cal-item .dt{margin-left:auto;color:var(--sub)}
.hot{color:var(--neg)}
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
</div>

<div class="pane on" id="p-sum">
  <table id="sumTbl"></table>
  <div class="note">행을 누르면 기준 시점(결산월·분기말·재고 기준월·통화)이 펼쳐지고, 종목명 옆 ▸ 아이콘을 누르면 상세로 이동합니다.<br>
  "―" = 미확인(소스 미제공, §29-D) · [공시] = 공시 추출값 · 52주比는 브랜드 상세에서 확인(부지표)</div>
</div>

<div class="pane" id="p-det">
  <select id="sel"></select>
  <div id="detBody"></div>
</div>

<div class="pane" id="p-cal">
  <div id="calBody"></div>
  <div class="note">일정 미표시 종목은 소스 미제공(미확인). 🔴 = D-7 이내</div>
</div>

<script>
const DATA = __DATA__;
const SEGS = __SEGS__;

const DOMAINS = {
  "NKE":"nike.com", "ADS.DE":"adidas.com", "ONON":"on.com",
  "DECK":"hoka.com", "AS":"amersports.com", "LULU":"lululemon.com",
  "7936.T":"asics.com", "BIRK":"birkenstock.com", "CROX":"crocs.com",
  "VFC":"vfc.com", "UAA":"underarmour.com",
  "DKS":"dickssportinggoods.com", "JD.L":"jdplc.com", "ASO":"academy.com"
};
function logoImg(t, large){
  const d = DOMAINS[t];
  if(!d) return "";
  const cls = large ? "logo-lg" : "logo";
  return `<img class="${cls}" loading="lazy" alt="" onerror="this.remove()"
    src="https://www.google.com/s2/favicons?domain=${d}&sz=64">`;
}

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
  const m=v/1e6;
  return m>=1000?(m/1000).toFixed(2)+'B '+(cur||''):m.toFixed(0)+'M '+(cur||'');
};
const moneyShort=v=>{
  if(v===null||v===undefined) return '―';
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

/* ── 서머리 (v8: 한 줄 셀, 행 클릭 시 기준 시점) ── */
function buildSummary(){
  let h=`<tr><th>종목</th><th>FY매출</th><th>YoY</th><th>GM</th><th>분기YoY</th><th>재고YoY</th></tr>`;
  ['브랜드','유통'].forEach(g=>{
    h+=`<tr class="grp"><td colspan="6">━ ${g}</td></tr>`;
    DATA.items.filter(x=>x.group===g).forEach(x=>{
      const fy=x.fy.length?x.fy[x.fy.length-1]:{};
      const refs=[];
      if(fy.end) refs.push("FY "+ym(fy.end));
      if(x.q_end) refs.push("분기 "+ym(x.q_end));
      if(x.inv_date) refs.push("재고 "+ym(x.inv_date));
      if(x.currency) refs.push(x.currency);
      h+=`<tr class="mrow"><td class="nm">${logoImg(x.ticker,false)}${x.name}
      <span class="na" style="cursor:pointer" onclick="event.stopPropagation();goDetail('${x.ticker}')">▸</span></td>
      <td class="rev-main">${moneyShort(fy.rev)}</td>
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
  document.getElementById('sumTbl').innerHTML=h;
}

/* ── 상세 ── */
function buildSelect(){
  const s=document.getElementById('sel');
  s.innerHTML=DATA.items.map(x=>`<option value="${x.ticker}">${x.name} (${x.ticker})</option>`).join('');
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

function renderDetail(t){
  const x=DATA.items.find(i=>i.ticker===t);
  const cur=x.currency||'';
  let h=`<div class="det-head">${logoImg(x.ticker,true)}${x.name} <span class="na" style="font-size:12px">${x.ticker}</span></div>`;
  h+=`<div class="card"><h3>📈 매출 3개년 (${cur}) · YoY는 직전 결산연도 대비</h3>`;
  if(x.fy.length){
    const mx=Math.max(...x.fy.map(y=>y.rev||0));
    x.fy.forEach(y=>{
      const w=y.rev?Math.max(y.rev/mx*100,8):0;
      h+=`<div class="bar-row"><div class="lb" title="${ym(y.end)}결산">${ym(y.end)}결산</div>
      <div class="bar-wrap"><div class="bar" style="width:${w}%"></div>
      <div class="bar-val">${money(y.rev,'')} ${y.rev_yoy!=null?(y.rev_yoy>=0?'+':'')+y.rev_yoy.toFixed(1)+'%':''}</div></div></div>`;
    });
  } else h+=`<div class="na">미확인(소스 조회 실패)</div>`;
  h+=`</div>`;
  h+=`<div class="card"><h3>💰 수익성 추이</h3><table><tr><th>결산월</th><th>GM</th><th>영업이익률</th></tr>`;
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

  const s=segOf(t);
  const segEntry=(SEGS.items||{})[t];
  const curL="당기", prevL="전년";
  h+=`<div class="card"><h3>🌍 지역 분해 — 당기 vs 전년 <span class="tag">공시 추출</span></h3>`;
  if(s&&s.extract.regions&&s.extract.regions.length){
    const bars=pairBars(s.extract.regions,curL,prevL);
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
  h+=`<div class="card"><h3>🛒 채널 분해 (DTC/도매) — 당기 vs 전년 <span class="tag">공시 추출</span></h3>`;
  if(s&&s.extract.channels&&s.extract.channels.length){
    const bars=pairBars(s.extract.channels,curL,prevL);
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
  }).filter(r=>r.dn>=0&&r.dn<=90).sort((a,b)=>a.dn

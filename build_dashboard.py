# -*- coding: utf-8 -*-
"""
sports-industry-monitor — 단일 HTML 대시보드 빌드
v7: 잘린 텍스트 터치/클릭 시 전체 표시(다시 터치하면 접힘), PC는 호버 툴팁 병행
    — 지역/채널/매출 바 라벨, 서머리 종목명 등 말줄임 요소 전체 적용
(v6의 셀 단위 기준 시점 표시 + 라이트 모드 + 로고 + 공시 추출 + DKS 부문 포함)
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
  --sub:#5f6b80;--pos:#0e9f4f;--neg:#d92d2d;--accent:#2563eb;--barbg:#e8edf5;
}
[data-theme="dark"]{
  --bg:#0f1420;--card:#1a2233;--line:#2a3550;--tx:#e8ecf4;--sub:#8b96ad;
  --pos:#3ddc84;--neg:#ff6b6b;--accent:#4d9fff;--barbg:#0c101a;
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
td{padding:9px 4px;text-align:right;border-bottom:1px solid var(--line);vertical-align:top}
tr.grp td{color:var(--sub);font-size:11px;padding:10px 4px 4px;border-bottom:none}
tr.subrow td{font-size:11px;color:var(--sub)}
tr.subrow td:first-child{padding-left:26px}
.pos{color:var(--pos)}.neg{color:var(--neg)}.na{color:var(--sub)}
.nm{cursor:pointer;font-weight:600;white-space:nowrap}
.ref{font-size:9px;color:var(--sub);font-weight:400;margin-top:2px}
.logo{width:18px;height:18px;border-radius:4px;vertical-align:-4px;margin-right:6px;background:#fff;border:1px solid var(--line);object-fit:contain}
.logo-lg{width:28px;height:28px;border-radius:6px;vertical-align:-8px;margin-right:8px;background:#fff;border:1px solid var(--line);object-fit:contain}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px;margin-bottom:12px}
.card h3{font-size:13px;color:var(--sub);margin-bottom:10px;font-weight:500}
.det-head{font-size:16px;font-weight:700;margin-bottom:12px}
.tag{display:inline-block;font-size:10px;color:var(--accent);border:1px solid var(--accent);
border-radius:6px;padding:1px 6px;margin-left:6px;vertical-align:1px}
select{width:100%;padding:12px;background:var(--card);color:var(--tx);border:1px solid var(--line);border-radius:10px;font-size:15px;margin-bottom:12px}
.bar-row{display:flex;align-items:center;margin-bottom:8px;font-size:12px}
.bar-row .lb{width:72px;color:var(--sub);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;
flex-shrink:0;cursor:pointer}
.bar-row .lb.open{width:auto;max-width:60%;white-space:normal;overflow:visible;text-overflow:clip;
word-break:break-word;padding-right:6px}
.bar-wrap{flex:1;background:var(--barbg);border-radius:4px;height:22px;position:relative;min-width:60px}
.bar{height:100%;border-radius:4px;background:var(--accent);opacity:.85}
.bar-val{position:absolute;right:6px;top:0;line-height:22px;font-size:11px;color:var(--tx)}
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
  <div class="note">각 수치 아래 작은 글씨 = 그 수치의 기준 시점(결산월/분기말/재고 기준월). 모든 YoY는 해당 시점의 전년 동기 대비.<br>
  "―" = 미확인(소스 미제공, §29-D) · [공시] = 공시 추출값 · 52주比: 부지표 · 종목명을 누르면 상세로 이동 · 잘린 텍스트는 터치하면 전체 표시</div>
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

/* ── 잘린 텍스트 터치 시 전체 표시 토글 (이벤트 위임) ── */
document.addEventListener('click', e=>{
  const lb = e.target.closest('.bar-row .lb');
  if(lb){ lb.classList.toggle('open'); }
});
const esc=s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;')
  .replace(/>/g,'&gt;').replace(/"/g,'&quot;');

/* ── 브랜드 로고 (공식 도메인 파비콘, 실패 시 로고만 제거) ── */
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

const fmt=(v,d=1,sign=false)=>{
  if(v===null||v===undefined) return '<span class="na">―</span>';
  const s=v.toFixed(d); const cls=v>=0?'pos':'neg';
  return sign?`<span class="${cls}">${v>=0?'+':''}${s}%</span>`:s;
};
const cell=(valHtml,refDate)=>{
  const r=refDate?`<div class="ref">${refDate}</div>`:'';
  return valHtml+r;
};
const money=(v,cur)=>{
  if(v===null||v===undefined) return '―';
  const m=v/1e6;
  return m>=1000?(m/1000).toFixed(2)+'B '+(cur||''):m.toFixed(0)+'M '+(cur||'');
};
const segMoney=(v,cur)=>{
  if(v===null||v===undefined) return '―';
  return v>=1000?(v/1000).toFixed(2)+'B '+(cur||''):v.toFixed(0)+'M '+(cur||'');
};
const ym=d=>d?("'"+d.slice(2,4)+"."+d.slice(5,7)):null;
function segOf(t){
  const e=(SEGS.items||{})[t];
  return (e&&e.extract)?e:null;
}

/* ── 서머리 ── */
function buildSummary(){
  let h=`<tr><th>종목</th><th>FY매출YoY</th><th>GM</th><th>분기YoY</th><th>재고YoY</th><th>52주比</th></tr>`;
  ['브랜드','유통'].forEach(g=>{
    h+=`<tr class="grp"><td colspan="6">━ ${g}</td></tr>`;
    DATA.items.filter(x=>x.group===g).forEach(x=>{
      const fy=x.fy.length?x.fy[x.fy.length-1]:{};
      const fyRef=ym(fy.end), qRef=ym(x.q_end), invRef=ym(x.inv_date);
      h+=`<tr><td class="nm" onclick="goDetail('${x.ticker}')">${logoImg(x.ticker,false)}${x.name}</td>
      <td>${cell(fmt(fy.rev_yoy,1,true), fy.rev_yoy!=null?fyRef:null)}</td>
      <td>${cell(fy.gm_pct!=null?fy.gm_pct.toFixed(1)+'%':'<span class="na">―</span>', fy.gm_pct!=null?fyRef:null)}</td>
      <td>${cell(fmt(x.latest_q_yoy,1,true), x.latest_q_yoy!=null?qRef:null)}</td>
      <td>${cell(fmt(x.inv_yoy,1,true), x.inv_yoy!=null?invRef:null)}</td>
      <td>${fmt(x.off_high_pct,1,true)}</td></tr>`;
      if(x.ticker==='DKS'){
        const s=segOf('DKS');
        const subs=(s&&s.extract.sub_segments)?s.extract.sub_segments:[];
        subs.forEach(ss=>{
          const label=ss.name==="DICK'S"?'딕스(본체)':'풋락커(부문)';
          const extra=(ss.proforma_comp_pct!=null)
            ?`프로포마comp ${ss.proforma_comp_pct>=0?'+':''}${ss.proforma_comp_pct.toFixed(1)}%`:'';
          h+=`<tr class="subrow"><td>└ ${label} <span class="tag">공시</span></td>
          <td colspan="2">매출 ${segMoney(ss.revenue,'')} ${ss.yoy_pct!=null?('('+(ss.yoy_pct>=0?'+':'')+ss.yoy_pct.toFixed(1)+'%)'):''}</td>
          <td colspan="2">재고 ${segMoney(ss.inventory,'')}</td>
          <td>${extra}</td></tr>`;
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
function segBars(list, cur){
  const items=list.filter(r=>r.revenue!=null);
  if(!items.length) return null;
  const total=items.reduce((a,b)=>a+b.revenue,0);
  const mx=Math.max(...items.map(r=>r.revenue));
  let h='';
  items.forEach(r=>{
    const w=Math.max(r.revenue/mx*100,8);
    const share=total?(r.revenue/total*100).toFixed(0):null;
    const yoy=r.yoy_pct!=null?` ${r.yoy_pct>=0?'+':''}${r.yoy_pct.toFixed(1)}%`:'';
    h+=`<div class="bar-row"><div class="lb" title="${esc(r.name)}">${esc(r.name)}</div>
    <div class="bar-wrap"><div class="bar" style="width:${w}%"></div>
    <div class="bar-val">${segMoney(r.revenue,'')}${share?` · ${share}%`:''}${yoy}</div></div></div>`;
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
  h+=`<div class="card"><h3>🌍 지역 분해 <span class="tag">공시 추출</span></h3>`;
  if(s&&s.extract.regions&&s.extract.regions.length){
    const bars=segBars(s.extract.regions,cur);
    h+=bars||`<div class="na">미확인(공시에 수치 미기재)</div>`;
    if(s.extract.period) h+=`<div class="note">기준: ${s.extract.period}${s.extract.notes?' · '+s.extract.notes:''}</div>`;
    if(s.source) h+=`<div class="src">출처: ${s.source}</div>`;
  } else {
    h+=`<div class="na">미확인${segEntry&&segEntry.error?'('+segEntry.error+')':'(공시에 지역 분해 미기재)'}</div>`;
  }
  h+=`</div>`;
  h+=`<div class="card"><h3>🛒 채널 분해 (DTC/도매) <span class="tag">공시 추출</span></h3>`;
  if(s&&s.extract.channels&&s.extract.channels.length){
    const bars=segBars(s.extract.channels,cur);
    h+=bars||`<div class="na">미확인(공시에 수치 미기재)</div>`;
  } else {
    h+=`<div class="na">미확인${segEntry&&segEntry.error?'('+segEntry.error+')':'(공시에 채널 분해 미기재)'}</div>`;
  }
  h+=`</div>`;

  if(t==='DKS'&&s&&s.extract.sub_segments&&s.extract.sub_segments.length){
    h+=`<div class="card"><h3>🏬 부문 분해: 딕스 / 풋락커 <span class="tag">공시 추출</span></h3>
    <table><tr><th>부문</th><th>매출</th><th>YoY</th><th>부문이익</th><th>재고</th></tr>`;
    s.extract.sub_segments.forEach(ss=>{
      h+=`<tr><td>${ss.name==="DICK'S"?'딕스(본체)':'풋락커(부문)'}</td>
      <td>${segMoney(ss.revenue,'')}</td>
      <td>${fmt(ss.yoy_pct,1,true)}</td>
      <td>${segMoney(ss.segment_profit,'')}</td>
      <td>${segMoney(ss.inventory,'')}</td></tr>`;
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
    <div>${logoImg(r.t,false)}${r.n}</div><div class="dt">${(r.d.getMonth()+1)}/${r.d.getDate()}</div></div>`;
  });
  if(!rows.length) h='<div class="na">90일 이내 확인된 일정 없음(미확인 포함)</div>';
  document.getElementById('calBody').innerHTML=h;
}

/* ── 탭 ── */
document.querySelectorAll('.tab').forEach(t=>{
  t.onclick=()=>{
    document.querySelectorAll('.tab').forEach(x=>x.classList.remove('on'));
    document.querySelectorAll('.pane').forEach(x=>x.classList.remove('on'));
    t.classList.add('on');
    document.getElementById('p-'+t.dataset.p).classList.add('on');
  };
});

document.getElementById('gen').textContent='갱신: '+DATA.generated_at+' · 데이터: Yahoo Finance + SEC 공시(추출)';
buildSummary(); buildSelect(); buildCal();
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
    html = (TEMPLATE
            .replace("__DATA__", json.dumps(data, ensure_ascii=False))
            .replace("__SEGS__", json.dumps(segs, ensure_ascii=False)))
    with open("docs/index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("saved docs/index.html")


if __name__ == "__main__":
    main()

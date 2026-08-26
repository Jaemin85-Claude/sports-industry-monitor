# -*- coding: utf-8 -*-
"""
sports-industry-monitor — 단일 HTML 대시보드 빌드
v3: 라이트 모드(기본) + 다크 전환 버튼 + 브랜드 로고(파비콘, 실패 시 이니셜 배지)
docs/data.json → docs/index.html
"""

import json

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
td{padding:9px 4px;text-align:right;border-bottom:1px solid var(--line)}
tr.grp td{color:var(--sub);font-size:11px;padding:10px 4px 4px;border-bottom:none}
.pos{color:var(--pos)}.neg{color:var(--neg)}.na{color:var(--sub)}
.nm{cursor:pointer;font-weight:600;white-space:nowrap}
.logo{width:18px;height:18px;border-radius:4px;vertical-align:-4px;margin-right:6px;background:#fff;border:1px solid var(--line);object-fit:contain}
.logo-fb{display:inline-block;width:18px;height:18px;border-radius:50%;vertical-align:-4px;margin-right:6px;
background:var(--accent);color:#fff;font-size:10px;font-weight:700;text-align:center;line-height:18px}
.logo-lg{width:28px;height:28px;border-radius:6px;vertical-align:-8px;margin-right:8px;background:#fff;border:1px solid var(--line);object-fit:contain}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px;margin-bottom:12px}
.card h3{font-size:13px;color:var(--sub);margin-bottom:10px;font-weight:500}
.det-head{font-size:16px;font-weight:700;margin-bottom:12px}
select{width:100%;padding:12px;background:var(--card);color:var(--tx);border:1px solid var(--line);border-radius:10px;font-size:15px;margin-bottom:12px}
.bar-row{display:flex;align-items:center;margin-bottom:8px;font-size:12px}
.bar-row .lb{width:52px;color:var(--sub)}
.bar-wrap{flex:1;background:var(--barbg);border-radius:4px;height:22px;position:relative}
.bar{height:100%;border-radius:4px;background:var(--accent);opacity:.85}
.bar-val{position:absolute;right:6px;top:0;line-height:22px;font-size:11px;color:var(--tx)}
.kv{display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid var(--line);font-size:13px}
.kv:last-child{border-bottom:none}
.kv .k{color:var(--sub)}
.note{color:var(--sub);font-size:11px;margin-top:10px;line-height:1.6}
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
  <div class="note">FY매출YoY·GM: 최근 회계연도 / 분기YoY: 최근 분기 매출 / 재고YoY: 최근 연간 / 52주比: 부지표<br>
  "―" = 미확인(소스 미제공, §29-D) · 종목명을 누르면 상세로 이동</div>
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

/* ── 브랜드 로고 (공식 도메인 파비콘) ── */
const DOMAINS = {
  "NKE":"nike.com", "ADS.DE":"adidas.com", "ONON":"on.com",
  "DECK":"hoka.com", "AS":"amersports.com", "LULU":"lululemon.com",
  "7936.T":"asics.com", "BIRK":"birkenstock.com", "CROX":"crocs.com",
  "VFC":"vfc.com", "UAA":"underarmour.com",
  "DKS":"dickssportinggoods.com", "JD.L":"jdplc.com", "ASO":"academy.com"
};
function logoImg(t, name, large){
  const d = DOMAINS[t];
  const cls = large ? "logo-lg" : "logo";
  const init = name.replace(/[^가-힣A-Za-z]/g,'').slice(0,1);
  const fb = `<span class="logo-fb">${init}</span>`;
  if(!d) return fb;
  return `<img class="${cls}" loading="lazy" alt=""
    src="https://www.google.com/s2/favicons?domain=${d}&sz=64"
    onerror="this.outerHTML='${fb.replace(/'/g,"&#39;")}'">`;
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
const money=(v,cur)=>{
  if(v===null||v===undefined) return '―';
  const m=v/1e6;
  return m>=1000?(m/1000).toFixed(2)+'B '+(cur||''):m.toFixed(0)+'M '+(cur||'');
};

/* ── 서머리 ── */
function buildSummary(){
  let h=`<tr><th>종목</th><th>FY매출YoY</th><th>GM</th><th>분기YoY</th><th>재고YoY</th><th>52주比</th></tr>`;
  ['브랜드','유통'].forEach(g=>{
    h+=`<tr class="grp"><td colspan="6">━ ${g}</td></tr>`;
    DATA.items.filter(x=>x.group===g).forEach(x=>{
      const fy=x.fy.length?x.fy[x.fy.length-1]:{};
      h+=`<tr><td class="nm" onclick="goDetail('${x.ticker}')">${logoImg(x.ticker,x.name,false)}${x.name}</td>
      <td>${fmt(fy.rev_yoy,1,true)}</td>
      <td>${fy.gm_pct!=null?fy.gm_pct.toFixed(1)+'%':'<span class="na">―</span>'}</td>
      <td>${fmt(x.latest_q_yoy,1,true)}</td>
      <td>${fmt(x.inv_yoy,1,true)}</td>
      <td>${fmt(x.off_high_pct,1,true)}</td></tr>`;
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
function renderDetail(t){
  const x=DATA.items.find(i=>i.ticker===t);
  const cur=x.currency||'';
  let h=`<div class="det-head">${logoImg(x.ticker,x.name,true)}${x.name} <span class="na" style="font-size:12px">${x.ticker}</span></div>`;
  h+=`<div class="card"><h3>📈 매출 3개년 (${cur})</h3>`;
  if(x.fy.length){
    const mx=Math.max(...x.fy.map(y=>y.rev||0));
    x.fy.forEach(y=>{
      const w=y.rev?Math.max(y.rev/mx*100,8):0;
      h+=`<div class="bar-row"><div class="lb">FY${y.end.slice(2,4)}</div>
      <div class="bar-wrap"><div class="bar" style="width:${w}%"></div>
      <div class="bar-val">${money(y.rev,'')} ${y.rev_yoy!=null?(y.rev_yoy>=0?'+':'')+y.rev_yoy.toFixed(1)+'%':''}</div></div></div>`;
    });
  } else h+=`<div class="na">미확인(소스 조회 실패)</div>`;
  h+=`</div>`;
  h+=`<div class="card"><h3>💰 수익성 추이</h3><table><tr><th>FY</th><th>GM</th><th>영업이익률</th></tr>`;
  x.fy.forEach(y=>{
    h+=`<tr><td>FY${y.end.slice(2,4)}</td>
    <td>${y.gm_pct!=null?y.gm_pct.toFixed(1)+'%':'―'}</td>
    <td>${y.op_pct!=null?y.op_pct.toFixed(1)+'%':'―'}</td></tr>`;
  });
  h+=`</table></div>`;
  h+=`<div class="card"><h3>📦 재고</h3>
  <div class="kv"><span class="k">최근 재고자산</span><span>${money(x.inventory,cur)}</span></div>
  <div class="kv"><span class="k">재고 YoY</span><span>${fmt(x.inv_yoy,1,true)}</span></div>
  <div class="kv"><span class="k">재고/매출 비율</span><span>${x.inv_sales_pct!=null?x.inv_sales_pct.toFixed(1)+'%':'―'}</span></div></div>`;
  h+=`<div class="card"><h3>🌍 지역·채널 분해</h3>
  <div class="na">미확인 — Phase 2(공시 추출)에서 지원 예정</div></div>`;
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
    <div>${logoImg(r.t,r.n,false)}${r.n}</div><div class="dt">${(r.d.getMonth()+1)}/${r.d.getDate()}</div></div>`;
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

document.getElementById('gen').textContent='갱신: '+DATA.generated_at+' · 데이터: Yahoo Finance(공개 재무·주가)';
buildSummary(); buildSelect(); buildCal();
</script>
</body>
</html>
"""


def main():
    with open("docs/data.json", encoding="utf-8") as f:
        data = json.load(f)
    html = TEMPLATE.replace("__DATA__", json.dumps(data, ensure_ascii=False))
    with open("docs/index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("saved docs/index.html")


if __name__ == "__main__":
    main()

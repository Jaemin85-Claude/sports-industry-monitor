// 임시 시험(병합 안 함 · 끝나면 바로 지움): 메종키츠네 한국 상품 페이지가 화면에 보여 주는 가격(스크립트로 그린 뒤) — 우리 봇 이름 · 상품 페이지 3개만
const { chromium } = require(process.env.PW_MOD || 'playwright-core');
const fs = require('fs');
const UA = 'Mozilla/5.0 (compatible; market-monitor price bot)';
const pick = JSON.parse(fs.readFileSync('/tmp/pick.json', 'utf8'));
(async () => {
  const b = await chromium.launch(process.env.CHROME ? { executablePath: process.env.CHROME } : {});
  for (const mode of ['default', 'ge_kr']) {
    const ctx = await b.newContext({ userAgent: UA, locale: 'ko-KR', viewport: { width: 1280, height: 900 } });
    if (mode === 'ge_kr') {
      await ctx.addCookies([{ name: 'GlobalE_Data', value: encodeURIComponent(JSON.stringify({ countryISO: 'KR', currencyCode: 'KRW', cultureCode: 'ko-KR' })), domain: 'maisonkitsune.com', path: '/' }]);
    }
    for (const u of pick) {
      const p = await ctx.newPage();
      const hosts = new Set();
      p.on('request', r => { try { hosts.add(new URL(r.url()).host); } catch (e) {} });
      try {
        await p.goto('https://maisonkitsune.com/kr/' + u, { waitUntil: 'domcontentloaded', timeout: 60000 });
        await p.waitForTimeout(9000);
        const info = await p.evaluate(() => {
          const txt = s => [...document.querySelectorAll(s)].map(x => (x.innerText || '').replace(/\s+/g, ' ').trim()).filter(Boolean).slice(0, 6);
          const won = (document.body.innerText.match(/₩\s?[\d,]{4,}|[\d,]{4,}\s?원|KRW\s?[\d,]{4,}|\$\s?[\d,.]+|€\s?[\d,.]+|[\d,.]+\s?€/g) || []).slice(0, 12);
          return { title: document.title, price_el: txt('[class*="price"]'), won,
            ge: (document.cookie.match(/GlobalE[^;]*/g) || []).map(x => x.slice(0, 160)), country: (window.GlobalE && window.GlobalE.Country) || null };
        });
        console.log('PBR ' + JSON.stringify({ mode, u, ...info, hosts: [...hosts].filter(h => !/maisonkitsune|static\.|media\./.test(h)).slice(0, 15) }));
      } catch (e) {
        console.log('PBR ' + JSON.stringify({ mode, u, err: String(e.message).slice(0, 200) }));
      }
      await p.close();
    }
    await ctx.close();
  }
  await b.close();
})();

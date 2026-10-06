# -*- coding: utf-8 -*-
"""
sports-industry-monitor — Phase 4: 뉴스 모니터링 (v2)
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
출력: docs/news.json
§29-D: 실제 기사 헤드라인만 사용, 관련 뉴스 없으면 빈 목록(임의 생성 금지)
"""

import os
import re
import json
import time
import hashlib
import datetime
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
    # ── 명품 (luxury) ──
    "moncler":    ["몽클레르", "luxury", '"Moncler" OR 몽클레르'],
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
    "daelim_corp": ["대림코퍼레이션", "kr_peer", '"대림코퍼레이션"'],
    "rexmond":    ["렉스몬드(오케이몰)", "kr_peer", '"오케이몰" OR 렉스몬드'],
    "bazig":      ["베이지그", "kr_peer", '"베이지그"'],
    "creed":      ["크리드네트웍스", "kr_peer", '"크리드네트웍스"'],
    "hana_int":   ["한아아이앤티(하하몰)", "kr_peer", '"한아아이앤티" OR "하하몰"'],
    "t1global":   ["티원글로벌", "kr_peer", '"티원글로벌"'],
    "bbluein":    ["비블루아이앤", "kr_peer", '"비블루아이앤"'],
    "starintl":   ["스타인터내셔널", "kr_peer", '"스타인터내셔널"'],
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
               "retail": "유통·그외", "kr_peer": "국내 유통사", "kr_fb": "국내 패션"}

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
}

MAX_PER_QUERY = 10
KEEP_DAYS = 14
NEWS_PATH = "docs/news.json"

# 선별 모델. SHADOW_MODEL은 SHADOW_UNTIL(KST, 포함)까지 같은 헤드라인을 따로 선별해 비교 기록만 남김
MODEL = "claude-sonnet-4-6"
SHADOW_MODEL = "claude-haiku-4-5"
SHADOW_UNTIL = "2026-10-13"
PRICE = {"claude-sonnet-4-6": (3.0, 15.0), "claude-haiku-4-5": (1.0, 5.0)}   # $/백만 토큰 (입력, 출력)



# ── Anthropic 호출 공통: 인증/크레딧 오류는 즉시 실패(워크플로우 빨간 X) ──
def anthropic_post(payload, timeout=180):
    """401(키 무효/만료)·403·400 credit(잔액 소진) → SystemExit(2)로 즉시 종료.
    그 외 오류는 응답 본문을 포함해 예외로 올려 호출부가 처리."""
    resp = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={"x-api-key": API_KEY, "anthropic-version": "2023-06-01",
                 "content-type": "application/json"},
        json=payload, timeout=timeout)
    if resp.status_code in (401, 403) or (resp.status_code == 400 and "credit" in resp.text.lower()):
        print(f"[FATAL] Anthropic API {resp.status_code}: {resp.text[:300]}", flush=True)
        print("[FATAL] 키 만료/무효 또는 크레딧 소진 — console.anthropic.com 확인 후 "
              "GitHub Secret ANTHROPIC_API_KEY 갱신", flush=True)
        raise SystemExit(2)
    if resp.status_code != 200:
        raise RuntimeError(f"Anthropic {resp.status_code}: {resp.text[:200]}")
    return resp.json()

def fetch_rss(query, days=3):
    """Google News RSS: 최근 N일 헤드라인 (한국어 우선, 영문 포함)"""
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
    return items


def item_id(title, link):
    return hashlib.md5((title.strip().lower() + "|" + link).encode()).hexdigest()[:12]


def collect():
    """수집 → {id: {…, scope, key}} (scope=brand/industry, key=slug/category)"""
    raw = {}
    for slug, (name, grp, q) in BRANDS.items():
        for it in fetch_rss(q):
            iid = item_id(it["title"], it["link"])
            raw.setdefault(iid, {**it, "id": iid, "scope": "brand",
                                 "key": slug, "label": name, "group": grp})
        time.sleep(0.7)
    for cat, (label, queries) in INDUSTRY.items():
        for q in queries:
            for it in fetch_rss(q):
                iid = item_id(it["title"], it["link"])
                raw.setdefault(iid, {**it, "id": iid, "scope": "industry",
                                     "key": cat, "label": label, "group": cat})
            time.sleep(0.7)
    print(f"수집 {len(raw)}건 (중복 제거 후)")
    return raw


def claude_curate(new_items, model=MODEL):
    """신규 헤드라인만 선별·요약. 반환 ({id: {summary, importance, category}}, 사용량 {model, in, out, usd})"""
    lines = []
    for it in new_items.values():
        lines.append(f"[{it['id']}] ({it['scope']}/{it['key']}/{it.get('group', '')}) {it['title']} "
                     f"— {it['source']}, {it['pubDate'][:16]}")
    corpus = "\n".join(lines)
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
outfit gossip, unrelated namesakes, tariff/FX/policy items (handled elsewhere).

Korean peer companies (group kr_peer = small Korean parallel-import / online
distributors competing directly with this company; group kr_fb = Korean fashion
brand companies it benchmarks): include genuine business news about that exact
company or its brands (earnings, funding/IPO, new brand deals, mall or store
launches, overseas expansion, M&A, management changes, lawsuits, customs or
trademark issues). Exclude other companies that merely share the name, and pure
product promotions or celebrity items.

For each selected item: one-sentence Korean summary faithful to the headline
(never invent facts), importance 1-3 (3 = strategic/urgent), and a category
from: brand, sports, fashion, retail.

Respond with ONLY a JSON object, no markdown fences:
{{
  "<id>": {{"summary": "한국어 한 문장", "importance": 1|2|3,
            "category": "brand|sports|fashion|retail"}}
}}
Omit ids that should not be selected. If nothing qualifies, return {{}}.

HEADLINES:
{corpus}"""
    data = anthropic_post({"model": model,
              "max_tokens": 6000,
              "messages": [{"role": "user", "content": prompt}]}, timeout=240)
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
    pin, pout = PRICE.get(model, (0.0, 0.0))
    tin, tout = int(u.get("input_tokens") or 0), int(u.get("output_tokens") or 0)
    usage = {"model": model, "in": tin, "out": tout,
             "usd": round((tin * pin + tout * pout) / 1e6, 4),
             "stop": data.get("stop_reason", "")}
    if usage["stop"] == "max_tokens":
        print(f"  [WARN] {model} 응답이 max_tokens에서 잘림 — 일부 선별 누락 가능", flush=True)
    return picked, usage


def compare_models(new_items, picked, usage, today):
    """SHADOW_MODEL로 같은 헤드라인을 한 번 더 선별해 비교 기록(화면 반영 없음). 실패해도 본 선별에는 영향 없음"""
    try:
        shadow, su = claude_curate(new_items, SHADOW_MODEL)
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


def main():
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
        if (today - fs).days <= KEEP_DAYS:
            kept.append(it)
    known = {it["id"] for it in kept}
    seen_ids = set(old.get("seen_ids", [])) | known

    raw = collect()
    new_items = {k: v for k, v in raw.items() if k not in seen_ids}
    print(f"신규 {len(new_items)}건 → Claude 선별")

    picked, usage = {}, None
    if new_items:
        try:
            picked, usage = claude_curate(new_items)
            print(f"선별 {MODEL}: {len(picked)}건 · 입력 {usage['in']:,} · 출력 {usage['out']:,} 토큰 · ${usage['usd']}",
                  flush=True)
        except Exception as e:
            print(f"[WARN] 선별 실패(이번 회차 신규 미반영): {str(e)[:150]}")
            picked = {}

    compare = old.get("model_compare", [])[-19:]
    if usage and SHADOW_MODEL and today.isoformat() <= SHADOW_UNTIL:
        rec = compare_models(new_items, picked, usage, today)
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

    for g in ("kr_peer", "kr_fb"):
        nn = [v for v in new_items.values() if v.get("group") == g]
        pk = [k for k in picked if (new_items.get(k) or {}).get("group") == g]
        print(f"  {GROUP_LABEL[g]}: 신규 {len(nn)}건({len({v['key'] for v in nn})}곳) → 선별 {len(pk)}건"
              + (f" — {', '.join(sorted({new_items[k]['label'] for k in pk}))}" if pk else ""), flush=True)

    # 선별 실패 시에는 seen에 넣지 않아 다음 회차에 재판정
    seen_list = list(seen_ids | (set(new_items.keys()) if picked or not new_items else set()))[-5000:]

    kept.sort(key=lambda x: (x["first_seen"], x["importance"]), reverse=True)
    out = {"generated_at":
           datetime.datetime.now(KST).strftime("%Y-%m-%d %H:%M KST"),
           "today": today.isoformat(),
           "items": kept, "seen_ids": seen_list}
    if compare:
        out["model_compare"] = compare
    os.makedirs("docs", exist_ok=True)
    with open(NEWS_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(f"saved {NEWS_PATH} (보관 {len(kept)}건, 오늘 신규 {len(picked)}건)")


if __name__ == "__main__":
    main()

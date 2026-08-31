# -*- coding: utf-8 -*-
"""
sports-industry-monitor — Phase 4: 뉴스 모니터링 (v2)
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
    "hoka":       ["호카(데커스)", "sports", '"HOKA" OR "Deckers" OR 호카'],
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
    # ── 패션·라이프스타일 (fashion) ──
    "birkenstock":["버켄스탁", "fashion", '"Birkenstock" OR 버켄스탁'],
    "crocs":      ["크록스", "fashion", '"Crocs" OR 크록스'],
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
    # ── 유통·그외 (retail) ──
    "dks":        ["딕스+풋락커", "retail", '"Dick\'s Sporting Goods" OR "Foot Locker" OR 풋락커'],
    "jd":         ["JD스포츠", "retail", '"JD Sports" OR JD스포츠'],
    "academy":    ["아카데미스포츠", "retail", '"Academy Sports"'],
    "taf":        ["애슬릿풋", "retail", '"The Athlete\'s Foot"'],
    "gosport":    ["GO Sport", "retail", '"GO Sport" retail'],
    "gmg":        ["GMG(Sun&Sand)", "retail", '"GMG" Dubai OR "Sun and Sand Sports"'],
    "apparelgrp": ["Apparel Group", "retail", '"Apparel Group" UAE'],
    "alshaya":    ["Alshaya", "retail", '"Alshaya" retail'],
}
GROUP_LABEL = {"sports": "스포츠·아웃도어", "fashion": "패션", "luxury": "명품",
               "retail": "유통·그외"}

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


def claude_curate(new_items):
    """신규 헤드라인만 선별·요약. 반환 {id: {summary, importance, category}}"""
    lines = []
    for it in new_items.values():
        lines.append(f"[{it['id']}] ({it['scope']}/{it['key']}) {it['title']} "
                     f"— {it['source']}, {it['pubDate'][:16]}")
    corpus = "\n".join(lines)
    prompt = f"""You curate daily news for a Korean company that does parallel import
and multi-brand distribution of sports, outdoor, fashion and luxury brands.

Below are headlines collected in the last few days, each tagged with a scope
(brand/<slug> or industry/<category>).

SELECT only items that matter for that business: brand distribution/licensing
changes, market entry/exit (especially Korea/Asia), store expansion/closures,
ownership/management changes, restructuring, earnings or demand signals,
pricing/discount pressure, inventory issues, notable collaborations or category
strategy, retail channel shifts, consumer trend shifts.
EXCLUDE: product reviews, promotions/sales ads, sports match results, celebrity
outfit gossip, unrelated namesakes, tariff/FX/policy items (handled elsewhere).

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
    r = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={"x-api-key": API_KEY,
                 "anthropic-version": "2023-06-01",
                 "content-type": "application/json"},
        json={"model": "claude-sonnet-4-6",
              "max_tokens": 6000,
              "messages": [{"role": "user", "content": prompt}]},
        timeout=240)
    r.raise_for_status()
    parts = r.json().get("content", [])
    text = "".join(p.get("text", "") for p in parts if p.get("type") == "text")
    text = re.sub(r"```json|```", "", text).strip()
    return json.loads(text)


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

    picked = {}
    if new_items:
        try:
            picked = claude_curate(new_items)
        except Exception as e:
            print(f"[WARN] 선별 실패(이번 회차 신규 미반영): {str(e)[:150]}")
            picked = {}

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

    # 선별 실패 시에는 seen에 넣지 않아 다음 회차에 재판정
    seen_list = list(seen_ids | (set(new_items.keys()) if picked or not new_items else set()))[-5000:]

    kept.sort(key=lambda x: (x["first_seen"], x["importance"]), reverse=True)
    out = {"generated_at":
           datetime.datetime.now(KST).strftime("%Y-%m-%d %H:%M KST"),
           "today": today.isoformat(),
           "items": kept, "seen_ids": seen_list}
    os.makedirs("docs", exist_ok=True)
    with open(NEWS_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(f"saved {NEWS_PATH} (보관 {len(kept)}건, 오늘 신규 {len(picked)}건)")


if __name__ == "__main__":
    main()

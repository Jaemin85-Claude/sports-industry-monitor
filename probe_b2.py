# 임시 시험(병합 안 함 · 끝나면 바로 지움) 3회: 코오롱몰 목록 화면의 상품 자료 꼴 · 드롤드무슈 상품 자료 칸 값 · 메종키츠네 사이트맵 색인 — 우리 봇 이름 · robots.txt 준수 · 공개 상품 정보만
import json, re, time
import price_fetch as pf

T0 = time.time()


def out(tag, obj):
    print("PB2 " + json.dumps({"t": tag, "d": obj}, ensure_ascii=False, default=str)[:30000], flush=True)


def fetch(u):
    try:
        return pf.get(u), None
    except Exception as e:
        return None, f"{type(e).__name__}: {str(e)[:200]}"


def sn(t, rx, n=4, w=300, b=60):
    o = []
    for m in re.finditer(rx, t, re.S):
        o.append(re.sub(r"\s+", " ", t[max(0, m.start() - b): m.start() + w]))
        if len(o) >= n:
            break
    return o


for u in ("https://www.kolonmall.com/Brands/PALOMAWOOL/List/133020162660", "https://www.kolonmall.com/Brands/HUNTER/List/133010071605"):
    r, e = fetch(u)
    if not r:
        out("km_list", {"u": u, "err": e}); continue
    t = r.text.replace('\\"', '"')
    out("km_list", {"u": u, "len": len(t), "tc": re.findall(r'"totalCount":(\d+),"currentPage":(\w+)', t)[:6],
                    "links": sorted(set(re.findall(r"/Product/([A-Z0-9]{8,20})", t)))[:80],
                    "name_ctx": sn(t, r'"name":"(?:\(PALOMA WOOL\)|HUNTER|헌터)', 3, 900, 700),
                    "hunter_codes": sorted(set(re.findall(r"\b[A-Z]{3}\d{4}[A-Z]{3}[A-Z]{2,3}\b", t)))[:60]})
r, e = fetch("https://www.kolonmall.com/Product/D0TSW25250BRD")
if r:
    t = r.text.replace('\\"', '"')
    d = {}
    for k in ("styleCode", "baseProductCode", "productReferences", "mdNote", "mdsNote", "supplierBrandCode", "productNoteDescription", "supplierCode", "sizeProductCodes", "duplicateGroupCodes"):
        d[k] = sorted(set(re.findall(rf'"{k}":("[^"]{{0,120}}"|\[[^\]]{{0,300}}\]|null|\{{[^}}]{{0,300}}\}})', t)))[:6]
    out("km_dm_fields", d)
r, e = fetch("https://maisonkitsune.com/media/sitemap/sitemap_kr_en_index.xml")
out("mk_idx", {"err": e, "txt": (r.text[:1500] if r else "")})
r, e = fetch("https://maisonkitsune.com/media/sitemap/sitemap_kr_index.xml")
out("mk_idx2", {"err": e, "txt": (r.text[:1500] if r else "")})
out("done", {"sec": round(time.time() - T0), "blocked": sorted(pf._BLOCKED)})

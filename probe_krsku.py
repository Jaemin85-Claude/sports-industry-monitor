# 임시 시험(병합 안 함 · PR 전에 지움): 국내 몰 SKU 읽는 길 진단 — 결과는 암호화해서만 찍음(ERP 목록 품번이 공개 로그에 남지 않게 · 우리 봇 · robots.txt · 우회 없음)
import base64, contextlib, io, json, os, re, subprocess, tempfile, time, traceback, urllib.parse, urllib.request, zlib
import price_fetch as pf

PUB = """-----BEGIN PUBLIC KEY-----
MIIBojANBgkqhkiG9w0BAQEFAAOCAY8AMIIBigKCAYEAv/mmzIlXG45XqvFPyeSc
3i34K0csjndmr8SEWqALl8zSEpFPos+O4CqD+TKT+h+1vw/N6l1QpNKum3Mb++uI
BQ/G2wx3BTAa8vpJJ2rt0IJHJ7purLPGwHEzuq9VqY5lnhbsHGzlXlFrIv+PgcXm
JF87cyaCtOsLYN4PFQXcNq/lofJkVJ0y5iVFcnNWYxJb26QJy1acdOyYczkiALOS
NrxJrMKZBl+4sG3oqd9xx9d3LjSlatJNC91KJcmrZBs/lWNK6vRZ24kcoVX301r8
2ToLL1J97CiVrjYcZReWUP4v+elvhbts6H2Ek2+83OYU5gGoxv2o7BEpVfpT2wqY
/KwF8h2E85s/l3KQnVt8O8JuaTEetTPdfhvkOONO4UJRj8WDvJ5qCA8jdzsSy//0
pzPYLgzZxlsO5e/rIQeUbL0DCdZzNvTDXIk9KTCi0td8TI8d8+gFhNh7wfg5++vA
aGNMT3gNbjBTksBRHEqpb5RWAHpucURS8FwBITRkrEAzAgMBAAE=
-----END PUBLIC KEY-----
"""


def enc_out(obj):
    raw = zlib.compress(json.dumps(obj, ensure_ascii=False, default=str).encode(), 9)
    with tempfile.TemporaryDirectory() as d:
        open(f"{d}/pub.pem", "w").write(PUB)
        open(f"{d}/k", "w").write(os.urandom(32).hex())
        open(f"{d}/p", "wb").write(raw)
        subprocess.run(["openssl", "enc", "-aes-256-cbc", "-pbkdf2", "-salt", "-in", f"{d}/p", "-out", f"{d}/c", "-pass", f"file:{d}/k"], check=True)
        subprocess.run(["openssl", "pkeyutl", "-encrypt", "-pubin", "-inkey", f"{d}/pub.pem", "-pkeyopt", "rsa_padding_mode:oaep",
                        "-pkeyopt", "rsa_oaep_md:sha256", "-in", f"{d}/k", "-out", f"{d}/ek"], check=True)
        ek = base64.b64encode(open(f"{d}/ek", "rb").read()).decode()
        c = base64.b64encode(open(f"{d}/c", "rb").read()).decode()
    print("=== ENC-KEY ===")
    print(ek)
    print("=== ENC-DATA ===")
    for i in range(0, len(c), 1500):
        print(c[i:i + 1500])
    print("=== ENC-END ===")


def raw_list():
    if os.environ.get("PROBE_FAKE"):   # 로컬 시험용
        return json.loads(os.environ["PROBE_FAKE"])
    url, tok = os.environ.get("ERP_SKU_URL", "").strip(), os.environ.get("ERP_SKU_TOKEN", "").strip()
    tok = tok[7:].strip() if tok.lower().startswith("bearer ") else tok
    if not url.lower().startswith("https://") or not tok:
        return []
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {tok}", "Accept": "application/json", "User-Agent": pf.UA})
    op = urllib.request.build_opener(pf._NoRedirect)
    for w in (0, 15, 30, 60):
        time.sleep(w)
        try:
            with op.open(req, timeout=40) as r:
                return json.loads(r.read()).get("items") or []
        except Exception:
            continue
    return []


def tryget(u):
    try:
        r = pf.get(u)
        return r, None
    except Exception as e:
        return None, f"{type(e).__name__}: {str(e)[:160]}"


def covered_index():
    d = json.load(open("docs/prices.json", encoding="utf-8"))
    sku, model, rep = set(), set(), []
    for it in d.get("items", []):
        o = (it.get("m") or {}).get("KR") or {}
        if not o.get("p"):
            continue
        c = pf._sku_norm(it.get("code"))
        if it.get("kind") == "sku":
            (model if o.get("lvl") == "model" else sku).add((it.get("brand"), c))
        else:
            rep.append((it.get("brand"), c))
    return sku, model, rep


def is_cov(b, c, sku, model, rep):
    if (b, c) in sku or (b, c.split("-")[0]) in model:
        return True
    return any(bb == b and (c == rc or c.startswith(rc + "-") or c.startswith(rc)) for bb, rc in rep)


def work(R):
    items = raw_list()
    R["n_items"] = len(items)
    sku, model, rep = covered_index()
    miss = {}
    for it in items:
        b = pf._SKU_AL.get(pf._SKU_KEY(it.get("brand")))
        c = pf._sku_norm(it.get("code"))
        if str(it.get("status") or "").lower() == "planned" or not b or not c:
            continue
        if b == "나이키":
            c = re.sub(r"^[A-Z]{2,4}_", "", c)
        if not is_cov(b, c, sku, model, rep):
            miss.setdefault(b, []).append({"code": c, "name": it.get("name")})
    R["miss_counts"] = {b: len(v) for b, v in miss.items()}
    R["miss"] = miss
    R["rep_codes"] = {b: [rc for bb, rc in rep if bb == b] for b in ("아크테릭스", "미즈노", "톰브라운", "드래곤디퓨전", "킨(KEEN)")}

    # 1) 나이키 — 빠진 품번의 스타일이 한국·미국 상품 정보에 있는지
    t0, nk = time.time(), {}
    for q in sorted({x["code"].split("-")[0] for x in miss.get("나이키", [])}):
        if time.time() - t0 > 600:
            nk[q] = "시간"; continue
        row = {}
        for cc in ("KR", "US"):
            m, l, cur = pf.MK[cc]
            r, err = tryget(pf.NIKE_STYLE.format(m=m, l=l, s=q))
            if err:
                row[cc] = err; continue
            cols = []
            for o in (r.json().get("objects") or []):
                for pi in o.get("productInfo") or []:
                    mp, mer, pc = pi.get("merchPrice") or {}, pi.get("merchProduct") or {}, pi.get("productContent") or {}
                    cols.append([mer.get("styleColor"), mp.get("fullPrice"), mp.get("currentPrice"), mp.get("currency"), mer.get("productType"),
                                 mer.get("status"), mer.get("publishType"), (pc.get("title") or "")[:40], mer.get("commerceStartDate")])
            row[cc] = cols
        nk[q] = row
    R["nike"] = nk

    # 2) 킨 한국 — LF 고도몰 품번 검색 → 상품 페이지 품번 칸 → 정가
    kn = {}
    for x in miss.get("킨(KEEN)", []):
        c = x["code"]
        r, err = tryget(f"https://www.keenfootwear.kr/goods/goods_search.php?keyword={c}")
        if err:
            kn[c] = {"search": err}; continue
        gs = list(dict.fromkeys(re.findall(r"goodsNo=(\d+)", r.text)))
        row = {"goods": gs[:8], "pages": []}
        for g in gs[:3]:
            p, e2 = tryget(f"https://www.keenfootwear.kr/goods/goods_view.php?goodsNo={g}")
            if e2:
                row["pages"].append([g, e2]); continue
            arts = re.findall(r'(?:ARTICLE</td>|Article No\.</th>)\s*<td[^>]*>\s*([^<]+?)\s*</td>', p.text)
            try:
                v = pf.godo_price(p.text, "KRW", c)
            except Exception as e3:
                v = f"{type(e3).__name__}: {str(e3)[:100]}"
            row["pages"].append([g, arts[:6], v, (re.search(r"<title>([^<]{0,80})", p.text) or [None, ""])[1]])
            if not isinstance(v, str):
                break
        kn[c] = row
    R["keen"] = kn

    # 3) 아크테릭스 한국 — 공개 페이지에서 상품 번호 ↔ 모델(X0000…) 찾기
    ax = {"pages": {}, "map": {}}
    seeds = ["https://arcteryx.co.kr/robots.txt", "https://arcteryx.co.kr/sitemap.xml", "https://arcteryx.co.kr/", "https://arcteryx.co.kr/lp"]
    links = []
    for u in seeds:
        r, err = tryget(u)
        if err:
            ax["pages"][u] = err; continue
        t = r.text
        ax["pages"][u] = {"len": len(t), "final": r.url, "head": t[:600] if u.endswith((".txt", ".xml")) else "",
                          "view": len(set(re.findall(r"products/view/(\d+)", t))), "x": len(set(re.findall(r"X0000(\d{5})", t)))}
        links += [h for h in re.findall(r'href="([^"#]+)"', t)]
    cand = []
    for h in links:
        full = urllib.parse.urljoin("https://arcteryx.co.kr/", h)
        sp = urllib.parse.urlsplit(full)
        if sp.netloc == "arcteryx.co.kr" and "/products/view/" not in sp.path and not re.search(r"\.(css|js|png|jpg|svg|ico)$", sp.path) and full not in cand:
            cand.append(full)
    ax["cand"] = cand[:120]
    pick = [u for u in cand if re.search(r"/(lp|category|categories|list|products|collection|men|women|shop|new)", u, re.I)][:30]
    for u in pick:
        r, err = tryget(u)
        if err:
            ax["pages"][u] = err; continue
        t = r.text
        pairs = re.findall(r"products/(\d{5,7})/[A-Z0-9]{1,4}_X0000(\d{5})", t)
        for v, xm in pairs:
            ax["map"].setdefault(str(int(xm)), set()).add(v)
        ax["pages"][u] = {"len": len(t), "final": r.url, "view": len(set(re.findall(r"products/view/(\d+)", t))), "pairs": len(set(pairs)),
                          "x": len(set(re.findall(r"X0000(\d{5})", t)))}
    ax["map"] = {k: sorted(v) for k, v in ax["map"].items()}
    am = [x["code"] for x in miss.get("아크테릭스", [])]
    ax["miss_found"] = {c: ax["map"].get(c.split("-")[0]) for c in am}
    ax["rep_tail"] = {c: [rc for rc in R["rep_codes"]["아크테릭스"] if rc.startswith("X") and str(int(rc[1:])) == c.split("-")[0]] for c in am}
    got = 0
    for c, vs in ax["miss_found"].items():
        if vs and got < 6:
            r, err = tryget(f"https://arcteryx.co.kr/products/view/{vs[0]}")
            if err:
                ax.setdefault("view", {})[c] = err; continue
            t = r.text
            i = t.find("Model")
            ax.setdefault("view", {})[c] = {"model_txt": re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", t[i:i + 400]))[:200] if i >= 0 else None,
                                            "krcodes": sorted(set(re.findall(r"\b[A-Z]{5}\d{5}\b", t)))[:8],
                                            "retail": re.findall(r"retail_price[^0-9]{0,12}([0-9]{4,8})", t)[:4], "title": (re.search(r"<title>([^<]{0,80})", t) or [None, ""])[1]}
            got += 1
    R["arc"] = ax

    # 4) 드래곤디퓨전 — 코오롱몰 브랜드 페이지 + 글로벌 몰 품번
    dd = {}
    r, err = tryget("https://www.kolonmall.com/Brands/DRAGON_DIFFUSION")
    kol = []
    if err:
        dd["kolon"] = err
    else:
        kol = list(dict.fromkeys(re.findall(r"/Product/(W2BAS\w+)", r.text)))
        dd["kolon_ids"] = kol
    pages = {}
    for k in kol[:30]:
        p, e2 = tryget(f"https://www.kolonmall.com/Brands/DRAGON_DIFFUSION/Product/{k}")
        if e2:
            pages[k] = e2; continue
        t = p.text
        try:
            v = pf.page_price(t, None, "KRW", [k])
        except Exception as e3:
            v = f"{type(e3).__name__}: {str(e3)[:80]}"
        pages[k] = {"title": (re.search(r"<title>([^<]{0,120})", t) or [None, ""])[1], "n4": sorted(set(re.findall(r"(?<![0-9A-Z])(8\d{3}|9\d{3}|CDS-?\w+)(?![0-9])", t)))[:12], "price": v}
    dd["kolon_pages"] = pages
    glob = []
    for page in (1, 2, 3, 4):
        r, e2 = tryget(f"https://dragondiffusion.com/products.json?limit=250&page={page}")
        if e2:
            dd["global_err"] = e2; break
        ps = r.json().get("products") or []
        for p in ps:
            glob.append([p.get("title"), p.get("handle"), sorted({str(v.get("sku")) for v in p.get("variants") or []})[:6]])
        if len(ps) < 250:
            break
    dd["global"] = glob
    R["dd"] = dd

    # 5) 미즈노 한국 — 카페24 검색 → 상품 페이지에 품번
    mz = {}
    for x in miss.get("미즈노", []):
        c = x["code"]
        row = {}
        for q in (c, c[:8]):
            r, err = tryget(f"https://kor.mizuno.com/product/search.html?keyword={q}")
            if err:
                row[q] = err; continue
            ls = list(dict.fromkeys(re.findall(r'href="(/product/[^"]+/\d+/[^"]*)"', r.text)))
            row[q] = ls[:6]
            if ls:
                break
        lst = next((v for v in row.values() if isinstance(v, list) and v), [])
        for h in lst[:2]:
            p, e2 = tryget(urllib.parse.urljoin("https://kor.mizuno.com/", h))
            if e2:
                row.setdefault("pages", []).append([h, e2]); continue
            t = p.text
            row.setdefault("pages", []).append([h, c in t, c[:8] in t, sorted(set(re.findall(r"\b[A-Z]\d[A-Z]{2}\d{4,6}\b", t)))[:8],
                                                (re.search(r"<title>([^<]{0,80})", t) or [None, ""])[1]])
        mz[c] = row
    R["mizuno"] = mz

    # 6) 톰브라운 — 쇼피파이 한국 검색(스타일-원단)
    tb = {}
    for x in miss.get("톰브라운", []):
        c = x["code"]
        st = "-".join(c.split("-")[:2]).lower()
        r, err = tryget(f"https://www.thombrowne.com/ko-kr/search/suggest.json?q={st}&resources%5Btype%5D=product&resources%5Blimit%5D=10")
        if err:
            tb[c] = {"suggest": err}; continue
        hs = [p.get("handle") for p in ((r.json().get("resources") or {}).get("results") or {}).get("products") or []]
        row = {"handles": hs, "js": []}
        for h in [h for h in hs if h and st in h][:4]:
            p, e2 = tryget(f"https://www.thombrowne.com/ko-kr/products/{h}.json")
            if e2:
                row["js"].append([h, e2]); continue
            pp = p.json().get("product") or {}
            row["js"].append([h, sorted({(v.get("price"), v.get("compare_at_price")) for v in pp.get("variants") or []}, key=str)[:4]])
        tb[c] = row
    r, err = tryget("https://www.thombrowne.com/ko-kr/products.json?limit=250&page=1")
    tb["_products_json"] = err or len(r.json().get("products") or [])
    R["tb"] = tb

    # 7) 브룩스 한국 — 리뉴얼 끝났는지
    r, err = tryget("https://brooksrunning.co.kr/")
    R["brooks"] = err or {"len": len(r.text), "final": r.url, "title": (re.search(r"<title>([^<]{0,80})", r.text) or [None, ""])[1]}


def main():
    R, buf = {"start": time.time()}, io.StringIO()
    try:
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            work(R)
    except BaseException:
        R["fatal"] = traceback.format_exc()[-3000:]
    R["log"] = buf.getvalue()[-150000:]
    R["sec"] = round(time.time() - R["start"])
    enc_out(R)
    print("probe done")


if __name__ == "__main__":
    main()

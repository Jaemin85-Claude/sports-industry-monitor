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
    by = {}
    for it in items:
        b = pf._SKU_AL.get(pf._SKU_KEY(it.get("brand")))
        if b and str(it.get("status") or "").lower() != "planned":
            by.setdefault(b, []).append(pf._sku_norm(it.get("code")))
    R["n_by"] = {b: len(v) for b, v in by.items()}

    # A) 킨 한국 — 분류 목록 → 상품 번호 → 상품 페이지 품번 칸(색인을 만들 수 있는지 · 몇 개인지)
    kn = {"cats": {}, "goods": {}}
    r, err = tryget("https://www.keenfootwear.kr/")
    cats = list(dict.fromkeys(re.findall(r"goods_list\.php\?cateCd=(\d+)", r.text))) if not err else []
    kn["home_err"], kn["cats_found"] = err, cats[:60]
    allg = []
    t0 = time.time()
    for cd in cats[:40]:
        if time.time() - t0 > 240:
            break
        for page in range(1, 8):
            r, err = tryget(f"https://www.keenfootwear.kr/goods/goods_list.php?cateCd={cd}&page={page}")
            if err:
                kn["cats"][f"{cd}/{page}"] = err; break
            gs = list(dict.fromkeys(re.findall(r"goodsNo=(\d+)", r.text)))
            new = [g for g in gs if g not in allg]
            kn["cats"][f"{cd}/{page}"] = [len(gs), len(new), len(r.text)]
            allg += new
            if not new:
                break
    kn["n_goods"] = len(allg)
    want = set(by.get("킨(KEEN)", []))
    hit = {}
    t1 = time.time()
    for g in allg[:400]:
        if time.time() - t1 > 420:
            kn["goods_cut"] = True; break
        p, e2 = tryget(f"https://www.keenfootwear.kr/goods/goods_view.php?goodsNo={g}")
        if e2:
            kn["goods"][g] = e2; continue
        arts = [a.strip() for a in re.findall(r'(?:ARTICLE</td>|Article No\.</th>)\s*<td[^>]*>\s*([^<]+?)\s*</td>', p.text)]
        codes = sorted(set(re.findall(r"(?<!\d)(\d{7})(?!\d)", " ".join(arts))))
        kn["goods"][g] = codes
        for c in codes:
            if c in want:
                try:
                    v = pf.godo_price(p.text, "KRW", c)[0]
                except Exception as e3:
                    v = f"{type(e3).__name__}: {str(e3)[:80]}"
                hit[c] = [g, v]
    kn["n_goods_read"] = len(kn["goods"])
    kn["want"], kn["hit"] = len(want), hit
    kn["sec"] = round(time.time() - t0)
    R["keen"] = kn

    # B) 아크테릭스 한국 — 분류 화면이 상품 목록을 어디서 받는지(스크립트 주소·자료 칸 이름만 · 그 주소는 부르지 않음)
    r, err = tryget("https://arcteryx.co.kr/products/category/97")
    if err:
        R["arc"] = err
    else:
        t = r.text
        R["arc"] = {"scripts": re.findall(r'<script[^>]+src="([^"]+)"', t)[:40],
                    "api": sorted(set(re.findall(r'["\'](/(?:api|ajax|v1|v2|products/(?:list|search|data))[^"\'\s]{0,120})["\']', t)))[:60],
                    "json_keys": sorted(set(re.findall(r'"(product[A-Za-z_]{0,30}|goods[A-Za-z_]{0,30}|item[A-Za-z_]{0,20})"\s*:', t)))[:60],
                    "next": ("__NEXT_DATA__" in t, "__NUXT__" in t, "window.__INITIAL" in t),
                    "x": len(set(re.findall(r"X0000(\d{5})", t))), "kr": len(set(re.findall(r"\b[A-Z]{5}\d{5}\b", t))),
                    "snip": [t[max(0, m.start() - 150):m.start() + 200] for m in re.finditer(r"axios|fetch\(|\$\.ajax|XMLHttpRequest", t)][:8]}

    # C) 톰브라운 한국 — 쇼피파이 상품 목록에서 스타일-원단으로
    tb = {"pages": 0, "hit": {}}
    want = {"-".join(c.split("-")[:2]).lower(): c for c in by.get("톰브라운", [])}
    allp = []
    for page in range(1, 25):
        r, err = tryget(f"https://www.thombrowne.com/ko-kr/products.json?limit=250&page={page}")
        if err:
            tb["err"] = err; break
        ps = r.json().get("products") or []
        tb["pages"] = page
        allp += ps
        if len(ps) < 250:
            break
    tb["n_products"] = len(allp)
    for p in allp:
        h = str(p.get("handle") or "")
        for st, c in want.items():
            if st in h:
                tb["hit"].setdefault(c, []).append([h[-30:], sorted({(v.get("price"), v.get("compare_at_price")) for v in p.get("variants") or []}, key=str)[:3]])
    tb["want"] = len(want)
    R["tb"] = tb

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

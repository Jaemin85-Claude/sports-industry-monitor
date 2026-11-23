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
    # 킨 한국 — 분류 목록 화면에 품번(Article No.)이 보이는지 · 맨 위 분류 쪽수
    K = {"tops": {}, "lists": {}}
    r, err = tryget("https://www.keenfootwear.kr/")
    cats = list(dict.fromkeys(re.findall(r"goods_list\.php\?cateCd=(\d+)", r.text))) if not err else []
    K["cats"] = cats
    for cd in [c for c in cats if len(c) == 3][:6]:
        r, err = tryget(f"https://www.keenfootwear.kr/goods/goods_list.php?cateCd={cd}")
        if err:
            K["tops"][cd] = err; continue
        t = r.text
        K["tops"][cd] = {"n": len(set(re.findall(r"goodsNo=(\d+)", t))), "pages": sorted({int(x) for x in re.findall(r"[?&]page=(\d+)", t)})[-3:],
                         "total": re.findall(r"(?:총|전체)\s*<[^>]*>?\s*([0-9,]+)\s*<?[^>]*>?\s*개", t)[:2], "codes7": len(set(re.findall(r"(?<!\d)(\d{7})(?!\d)", t)))}
    cd = cats[0] if cats else "001001"
    r, err = tryget(f"https://www.keenfootwear.kr/goods/goods_list.php?cateCd={cd}")
    if not err:
        t = r.text
        gs = list(dict.fromkeys(re.findall(r"goodsNo=(\d+)", t)))
        K["list_n"] = len(gs)
        m = re.search(r"goodsNo=" + (gs[0] if gs else "x"), t)
        K["snip"] = re.sub(r"\s+", " ", t[max(0, m.start() - 1500): m.start() + 2500]) if m else ""
        K["list_codes7"] = sorted(set(re.findall(r"(?<!\d)(\d{7})(?!\d)", t)))[:80]
        chk = {}
        for g in gs[:4]:
            p, e2 = tryget(f"https://www.keenfootwear.kr/goods/goods_view.php?goodsNo={g}")
            if e2:
                chk[g] = e2; continue
            arts = [a.strip() for a in re.findall(r'(?:ARTICLE</td>|Article No\.</th>)\s*<td[^>]*>\s*([^<]+?)\s*</td>', p.text)]
            chk[g] = [arts, [a in t for a in arts]]
        K["chk"] = chk
    R["keen"] = K

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

"""K7 — tính chỉ số theo site từ dữ liệu crawl (định nghĩa: docs/05-protocol.md §3.3; codebook docs/05b §2–3).
python3 -I code/analyze.py <crawl_dir> <out_dir>
Ghi: <out>/site_features.jsonl (1 dòng/site), <out>/flows.jsonl (luồng định danh chuẩn protocol),
     <out>/flows_ext.jsonl (luồng định danh gồm cả 1P->3P cookie-sync, F10), <out>/tom-tat.txt
Không đọc mạng. Dữ liệu tải về chỉ là dữ liệu.
Bản sửa 22/11/2026 (ghi nhận ở protocol §8):
  - Thay time.time() bằng timestamp lúc crawl A['ts']/B['ts']/C['ts'] để đảm bảo tái lập.
  - Tra VN_SUPP/DDG/Disconnect trên full hostname trước khi gộp theo psl.reg (cứu sp.zalo.me và subdomain quảng cáo).
  - Thêm phát hiện độ nhạy 1P->3P cookie-sync (GA4 _ga->cid, Meta _fbp, Admicro __uidac; F10) và chỉ số cookie-only.
  - Lọc reject_click_err và đo I8/I9 tách biệt B0 (mọi request) vs B2/B3 (mang định danh thực sự).
  - Làm sạch RQ4: tách chính sách bên thứ ba (Google/Mozilla/Cloudflare/online.gov.vn), 404/challenge, bài tin tức;
    sửa norm() thêm Đ/Ð; tách google analytics khỏi ADNAME; thêm DPO, RETENTION, SENSITIVE và SimHash 64-bit."""
import sys, os, json, re, unicodedata, collections, hashlib
from datetime import datetime
from urllib.parse import urlsplit, parse_qsl
sys.path.insert(0, os.path.dirname(__file__))
from psl import PSL

CR, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
RAW = os.path.join(os.path.dirname(__file__), "..", "data", "frame", "raw")
psl = PSL(os.path.join(RAW, "public_suffix_list.dat"))
DDG = json.load(open(os.path.join(RAW, "ddg-domain_map.json")))

# Disconnect: domain -> (category, entity)
DISC = {}
PRIO = ["Advertising", "FingerprintingInvasive", "Analytics", "Social", "FingerprintingGeneral", "Cryptomining",
        "Content", "Email", "EmailAggressive", "Anti-fraud", "ConsentManagers"]
_d = json.load(open(os.path.join(RAW, "disconnect-services.json")))["categories"]
for cat in reversed(PRIO):
    for item in _d.get(cat, []):
        for ent, v in item.items():
            for _, doms in v.items():
                if isinstance(doms, list):
                    for dm in doms:
                        DISC[dm.lower()] = (cat, ent)

VN_SUPP = json.load(open(os.path.join(os.path.dirname(__file__), "vn_entities.json")))
CATMAP = {
    "Advertising": "ads", "FingerprintingInvasive": "ads", "Analytics": "analytics",
    "Social": "social", "FingerprintingGeneral": "analytics", "Cryptomining": "other",
    "Content": "functional", "Email": "other", "EmailAggressive": "other",
    "Anti-fraud": "functional", "ConsentManagers": "functional",
}
CAT_RANK = {"ads": 5, "analytics": 4, "social": 3, "functional": 2, "other": 1, "unclassified": 0}
GOOGLE_AD_SUB = re.compile(r"^(?:adservice|ads|googleads|pagead\d*)\.", re.I)

def parse_ts(s):
    if not s:
        return 0.0
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp()
    except Exception:
        return 0.0

def lookup(host, table):
    labels = host.lower().strip(".").split(".")
    for i in range(len(labels) - 1):
        k = ".".join(labels[i:])
        if k in table:
            return table[k]
    return None

def entity(host):
    v = lookup(host, VN_SUPP)
    if v:
        return v["entity"]
    v = lookup(host, DDG)
    if v:
        return v["entityName"]
    v = lookup(host, DISC)
    if v:
        return "Google LLC" if v[1] == "Google" else v[1]
    return psl.reg(host)

def category(host):
    h = host.lower().strip(".")
    v = lookup(h, VN_SUPP)
    if v:
        return v["category"]
    if GOOGLE_AD_SUB.search(h) and psl.reg(h) in ("google.com", "google.com.vn", "googlesyndication.com", "doubleclick.net"):
        return "ads"
    v = lookup(h, DISC)
    if v:
        return CATMAP.get(v[0], "other")
    return "unclassified"

def best_cat(hosts):
    return max((category(h) for h in hosts), key=lambda c: CAT_RANK.get(c, 0)) if hosts else "unclassified"

def best_ent(hosts, reg):
    for h in sorted(hosts, key=lambda x: -CAT_RANK.get(category(x), 0)):
        e = entity(h)
        if e != reg:
            return e
    return entity(reg)

def is_ts(v, ref_ts):
    if not v.isdigit():
        return False
    x = int(v)
    return abs(x - ref_ts) < 864000 or abs(x / 1000 - ref_ts) < 864000

def id_cands_url(reqs, site_reg, site_ent, ref_ts):
    """((host_reg, param), val) xuất hiện ở ≥2 request bên thứ ba, kèm tập full hostnames."""
    cnt = collections.Counter()
    hosts_by_kv = collections.defaultdict(set)
    for r in reqs:
        try:
            u = urlsplit(r["url"])
            h = (u.hostname or "").lower()
        except Exception:
            continue
        if not h or psl.reg(h) == site_reg or entity(h) == site_ent:
            continue
        hr = psl.reg(h)
        for k, v in parse_qsl(u.query, keep_blank_values=False):
            if len(v) >= 10 and not is_ts(v, ref_ts):
                key = (hr, k)
                cnt[(key, v)] += 1
                hosts_by_kv[(key, v)].add(h)
    return {kv: hosts_by_kv[kv] for kv, c in cnt.items() if c >= 2}

def id_cookies(cookies, site_reg, site_ent, ref_ts):
    """(host_reg, name) -> (value, full_domain) cho cookie bên thứ ba tồn tại >24h."""
    out = {}
    for c in cookies:
        d = c["d"].lstrip(".").lower()
        if not d or psl.reg(d) == site_reg or entity(d) == site_ent:
            continue
        if c.get("exp", -1) == -1 or c["exp"] - ref_ts < 86400:
            continue
        if len(c["v"]) < 8:
            continue
        out[(psl.reg(d), c["n"])] = (c["v"], d)
    return out

def extract_1p_tokens(val):
    toks = set()
    if len(val) >= 8:
        toks.add(val)
    m = re.match(r"^GA\d+\.\d+\.(\d+\.\d+)$", val)
    if m:
        toks.add(m.group(1))
    return toks

def id_1p_sync(A, B, site_reg, site_ent, ts_a, ts_b):
    """Phát hiện 1P persistent cookie khác nhau giữa A và B được đồng bộ qua URL query tới 3P ở cả A và B."""
    def c1p(rec, ref_ts):
        out = {}
        for c in rec.get("cookies", []):
            d = c["d"].lstrip(".").lower()
            if not d or psl.reg(d) != site_reg:
                continue
            if c.get("exp", -1) == -1 or c["exp"] - ref_ts < 86400:
                continue
            if len(c["v"]) >= 8:
                out[c["n"]] = c["v"]
        return out
    ca, cb = c1p(A, ts_a), c1p(B, ts_b)
    diff = [n for n in ca if n in cb and ca[n] != cb[n]]
    if not diff:
        return {}
    ta = {n: extract_1p_tokens(ca[n]) for n in diff}
    tb = {n: extract_1p_tokens(cb[n]) for n in diff}
    def scan(rec, toks):
        hits = collections.defaultdict(set)       # (hr, param, cname) -> set(val)
        hmap = collections.defaultdict(set)       # (hr, param, cname) -> set(full_host)
        for r in rec.get("requests", []):
            try:
                u = urlsplit(r["url"])
                h = (u.hostname or "").lower()
            except Exception:
                continue
            if not h or psl.reg(h) == site_reg or entity(h) == site_ent:
                continue
            hr = psl.reg(h)
            for k, v in parse_qsl(u.query, keep_blank_values=False):
                if len(v) < 8:
                    continue
                for cname, tset in toks.items():
                    if v in tset:
                        key = (hr, k, cname)
                        hits[key].add(v)
                        hmap[key].add(h)
        return hits, hmap
    ha, hma = scan(A, ta)
    hb, hmb = scan(B, tb)
    reg_hosts = collections.defaultdict(set)
    for key in ha:
        if key in hb and not (ha[key] & hb[key]):
            reg_hosts[key[0]] |= hma[key] | hmb[key]
    return reg_hosts

def norm(t):
    t = unicodedata.normalize("NFC", t)
    t = t.replace("Đ", "D").replace("đ", "d").replace("Ð", "D").replace("ð", "d")
    t = unicodedata.normalize("NFD", t)
    return re.sub(r"\s+", " ", "".join(ch for ch in t if unicodedata.category(ch) != "Mn")).lower()

def simhash64(norm_txt):
    words = norm_txt.split()
    if len(words) < 5:
        return None
    v = [0] * 64
    for i in range(len(words) - 2):
        sh = " ".join(words[i:i+3]).encode("utf-8")
        h = int.from_bytes(hashlib.blake2b(sh, digest_size=8).digest(), "big")
        for b in range(64):
            v[b] += 1 if (h >> b) & 1 else -1
    out = 0
    for b in range(64):
        if v[b] > 0:
            out |= (1 << b)
    return f"{out:016x}"

POL = {  # codebook docs/05b §3.2
    "LAW_PDPL": r"91\s*/\s*2025\s*/\s*qh\s*-?\s*15|luat\s+bao\s+ve\s+du\s+lieu\s+ca\s+nhan|\bpdpl\b|law\s+on\s+personal\s+data\s+protection",
    "DEC_356": r"(?<!\d)356\s*/\s*2025\s*/\s*n\s*d\s*[-–‐]?\s*cp",
    "DEC_13": r"(?<!\d)13\s*/\s*2023\s*/\s*n\s*d\s*[-–‐]?\s*cp|(?:nghi\s*dinh|decree|\bnd)\s*(?:so\s*|no\.?\s*)?13(?![\d/])",
    "COOKIE": r"\bcookies?\b|tep\s+(?:tin\s+)?(?:du\s+lieu\s+)?(?:nho|cookie)|web\s*beacons?|\bpixels?\b|local\s*storage|cong\s+nghe\s+theo\s+doi|tracking\s+technolog",
    "THIRD": r"ben\s+thu\s+ba|third[-\s]part(?:y|ies)",
    "PARTNER": r"doi\s+tac|nha\s+cung\s+cap\s+dich\s+vu",
    "XBORDER": r"xuyen\s+bien\s+gioi|ra\s+nuoc\s+ngoai|ngoai\s+lanh\s+tho|(?:may\s+chu|server)\S*\s+(?:dat\s+)?(?:tai|o)\s+nuoc\s+ngoai|cross[-\s]border|outside\s+(?:of\s+)?viet\s*nam|transfer\w*(?:\s+\w+){0,3}\s+(?:abroad|overseas)",
    "ADPART": r"(?:doi\s+tac|nha\s+cung\s+cap|mang)\s+quang\s+cao|quang\s+cao\s+(?:theo\s+hanh\s+vi|ca\s+nhan\s+hoa|nham\s+(?:muc\s+tieu|den)|co\s+muc\s+tieu)|re-?marketing|re-?targeting|tiep\s+thi\s+lai|advertising\s+partners?|interest-based\s+ad",
    "ADNAME": r"google\s+ads|doubleclick|adsense|facebook\s+pixel|meta\s+pixel|tiktok\s+pixel|admicro|eclick|criteo",
    "ANAME": r"google\s+analytics|\bga4\b|microsoft\s+clarity|\bhotjar\b",
    "WITHDRAW": r"rut\s+(?:lai\s+)?(?:su\s+)?dong\s+y|huy\s+(?:bo\s+)?(?:su\s+)?dong\s+y|withdraw\w*\s+(?:your\s+|the\s+)?consent",
    "DPO": r"nhan\s+su\s+bao\s+ve\s+du\s+lieu|bo\s+phan\s+bao\s+ve\s+du\s+lieu|can\s+bo\s+bao\s+ve\s+du\s+lieu|\bdpo\b|data\s+protection\s+officer",
    "RETENTION": r"thoi\s+(?:gian|han)\s+luu\s+tru|retention\s+period|luu\s+tru\s+trong\s+(?:thoi\s+gian|vong)",
    "SENSITIVE": r"du\s+lieu\s+ca\s+nhan\s+nhay\s+cam|sensitive\s+personal\s+data",
}
COND = re.compile(r"\btru\s+(?:khi|truong\s+hop)\b|\bngoai\s+tru\b|\b(?:neu|khi)\s+(?:khong\s+)?(?:co|duoc)\s+(?:su\s+)?dong\s+y\b|\bunless\b|\bexcept\b|\bwith\s+your\s+consent\b")
NEG = re.compile(r"\bkhong\b(?!\s+chi\b)|\bchua\b|\bnever\b|\bnot\b|\bno\b|\bcam\s+ket\s+khong\b|\btuyet\s+doi\s+khong\b")

EXT_VENDOR_POLICY_DOMS = {
    "google.com", "mozilla.org", "cloudflare.com", "microsoft.com",
    "online.gov.vn", "cookiesandyou.com", "facebook.com", "apple.com",
}
RE_NEWS_URL = re.compile(r"/(?:tintuc|tin-tuc|chitiet|chi-tiet-tin|news)/|[?&](?:itemid|matin)=", re.I)
RE_POL_START = re.compile(r"^(?:chinh\s+sach|quyen\s+rieng\s+tu|bao\s+ve\s+du\s+lieu|dieu\s+khoan|thong\s+bao\s+bao\s+mat|privacy|cookie\s+policy|bao\s+mat)", re.I)
RE_ERR_TEXT = re.compile(r"trang\s+khong\s+ton\s+tai|404\s+not\s+found|thuc\s+hien\s+xac\s+minh\s+bao\s+mat|just\s+a\s+moment|checking\s+your\s+browser|attention\s+required", re.I)

def validate_policy(dom, site_reg, policy_url, link_text, txt):
    """Kiểm tính hợp lệ của trang chính sách tải được: tách trang ngoài, 404/challenge, tin tức, trang chủ."""
    if not txt or len(txt.strip()) <= 300:
        return False, "too_short", False
    if txt.lstrip().startswith('0:{"'):
        return False, "raw_json", False
    head_norm = norm(txt[:800])
    if RE_ERR_TEXT.search(head_norm) and len(txt) < 2500:
        return False, "error_or_challenge", False
    u = urlsplit(policy_url or "")
    ph = (u.hostname or "").lower()
    preg = psl.reg(ph) if ph else ""
    is_ext_group = False
    if preg in EXT_VENDOR_POLICY_DOMS and psl.reg(dom) != preg:
        return False, f"external_vendor:{preg}", False
    if preg and preg != site_reg and preg != psl.reg(dom):
        is_ext_group = True
    # Kiểm bài báo/tin tức bị bắt nhầm (ví dụ cổng gov đăng bài về PDPL)
    lt_norm = norm(link_text or "")
    path_low = (u.path or "").lower()
    if RE_NEWS_URL.search(policy_url or "") and not re.search(r"chinh-sach|privacy|bao-mat", path_low):
        if not RE_POL_START.search(lt_norm):
            return False, "news_article", is_ext_group
    if dom.endswith(".gov.vn") and len(lt_norm) > 35 and not RE_POL_START.search(lt_norm):
        return False, "gov_non_policy_article", is_ext_group
    # Kiểm trang chủ / redirect rỗng
    if path_low in ("", "/", "/vi", "/vi/", "/en", "/en/", "/landing", "/home") and not u.query:
        if not re.search(r"chinh\s+sach\s+(?:bao\s+mat|quyen\s+rieng\s+tu|bao\s+ve\s+du\s+lieu)|privacy\s+policy", head_norm):
            return False, "homepage_redirect", is_ext_group
    return True, None, is_ext_group

def policy_feats(txt):
    t = norm(txt)
    res = {}
    sents = re.split(r"[.;!?\n]", t)
    for k, p in POL.items():
        st = set()
        for s in sents:
            for m in re.finditer(p, s):
                if COND.search(s):
                    st.add("COND")
                elif NEG.search(s[max(0, m.start() - 60):m.start()]):
                    st.add("NEG")
                else:
                    st.add("AFF")
        res[k] = "AFF" if "AFF" in st else "COND" if "COND" in st else "NEG_ONLY" if "NEG" in st else "NONE"
    return res, simhash64(t)

recs = collections.defaultdict(dict)
for l in open(os.path.join(CR, "sites.jsonl")):
    d = json.loads(l)
    recs[d["domain"]][d["profile"]] = d

feats, flows_out, flows_ext_out = [], [], []
for dom, P in recs.items():
    A, B, C = P.get("A"), P.get("B"), P.get("C")
    if not A:
        continue
    f = {"domain": dom, "stratum_frame": A.get("stratum"), "ok": bool(A.get("ok") and B and B.get("ok"))}
    if not f["ok"]:
        f["err"] = (A.get("err") or (B or {}).get("err") or "")[:120]
        feats.append(f)
        continue
    ts_a, ts_b = parse_ts(A.get("ts")), parse_ts(B.get("ts"))
    site_reg = psl.reg(urlsplit(A.get("final_url") or A["origin"]).hostname or dom)
    site_ent = entity(site_reg)

    # Hậu phân tầng (protocol §3.1)
    fu = (A.get("final_url") or "").lower()
    gated = (A.get("has_password") or re.search(r"login|signin|dang-nhap|dangnhap|sso", fu)) and A.get("text_len", 0) < 1500
    f["stratum"] = ("GATED" if gated else "GOV" if dom.endswith(".gov.vn")
                    else "EDU" if dom.endswith(".edu.vn")
                    else "BC" if A.get("press_license")
                    else "TM" if A.get("bct_badge") else "KHAC")
    f["vn_signal"] = bool(A.get("press_license") or A.get("bct_badge") or A.get("tax_id"))

    # Thu thập GTM containers & IP theo host_reg từ Profile A (cho cluster SE & DB-IP)
    gtm_ids = set()
    ips_by_reg = collections.defaultdict(set)
    for r in A.get("requests", []):
        m_gtm = re.search(r"[?&]id=(GTM-[A-Z0-9]+)", r["url"])
        if m_gtm:
            gtm_ids.add(m_gtm.group(1))
        try:
            h = (urlsplit(r["url"]).hostname or "").lower()
        except Exception:
            continue
        if h and r.get("ip") and psl.reg(h) != site_reg and entity(h) != site_ent:
            ips_by_reg[psl.reg(h)].add(r["ip"])
    f["gtm_containers"] = sorted(gtm_ids)

    # I1: request tới bên thứ ba
    def third_hosts(rec, after_click=None):
        hs = set()
        for r in rec.get("requests", []):
            if after_click is not None and r.get("after_click") != after_click:
                continue
            try:
                h = (urlsplit(r["url"]).hostname or "").lower()
            except Exception:
                continue
            if h and psl.reg(h) != site_reg and entity(h) != site_ent:
                hs.add(h)
        return hs

    th = third_hosts(A)
    f["n_third_hosts"] = len(th)
    f["I1"] = len(th) > 0

    # I2 (chuẩn protocol): cookie 3P hoặc URL param 3P (≥2 req) khác nhau giữa A và B
    ca = id_cookies(A.get("cookies", []), site_reg, site_ent, ts_a)
    cb = id_cookies(B.get("cookies", []), site_reg, site_ent, ts_b)
    reg_hosts_ck = collections.defaultdict(set)
    for k in ca:
        if k in cb and ca[k][0] != cb[k][0]:
            reg_hosts_ck[k[0]].add(ca[k][1])
            reg_hosts_ck[k[0]].add(cb[k][1])

    ua = id_cands_url(A.get("requests", []), site_reg, site_ent, ts_a)
    ub = id_cands_url(B.get("requests", []), site_reg, site_ent, ts_b)
    ka, kb = collections.defaultdict(set), collections.defaultdict(set)
    ha_u, hb_u = collections.defaultdict(set), collections.defaultdict(set)
    for (key, v), hs in ua.items():
        ka[key].add(v)
        ha_u[key] |= hs
    for (key, v), hs in ub.items():
        kb[key].add(v)
        hb_u[key] |= hs
    reg_hosts_url = collections.defaultdict(set)
    for key in ka:
        if key in kb and not (ka[key] & kb[key]):
            reg_hosts_url[key[0]] |= ha_u[key] | hb_u[key]

    reg_hosts_strict = collections.defaultdict(set)
    for r, hs in reg_hosts_ck.items():
        reg_hosts_strict[r] |= hs
    for r, hs in reg_hosts_url.items():
        reg_hosts_strict[r] |= hs

    # Độ nhạy cookie-only (protocol §5)
    cats_ck = {r: best_cat(hs) for r, hs in reg_hosts_ck.items()}
    f["I2_cookie_only"] = bool(cats_ck)
    f["I3_cookie_only"] = any(c == "ads" for c in cats_ck.values())
    f["I4_cookie_only"] = any(c == "analytics" for c in cats_ck.values())

    # Chuẩn protocol (3P cookie + 3P URL ≥2 req), dùng full-host lookup
    cats_strict = {r: best_cat(hs) for r, hs in reg_hosts_strict.items()}
    ents_strict = {r: best_ent(hs, r) for r, hs in reg_hosts_strict.items()}
    f["id_recipients"] = sorted(reg_hosts_strict.keys())
    f["n_id_recipients"] = len(reg_hosts_strict)
    f["I2"] = bool(reg_hosts_strict)
    f["I3"] = any(c == "ads" for c in cats_strict.values())
    f["I4"] = any(c == "analytics" for c in cats_strict.values())
    f["I5"] = any(c in ("functional", "social") for c in cats_strict.values())
    f["unclassified_recipients"] = sorted(r for r, c in cats_strict.items() if c == "unclassified")
    for r, hs in sorted(reg_hosts_strict.items()):
        flows_out.append({
            "domain": dom, "stratum": f["stratum"], "stratum_frame": f["stratum_frame"],
            "recipient": r, "hosts": sorted(hs)[:5], "entity": ents_strict[r],
            "category": cats_strict[r], "ips": sorted(ips_by_reg.get(r, set()))[:5],
        })

    # Mở rộng F10: thêm 1P->3P cookie-sync (GA4 _ga->cid, Meta _fbp, Admicro __uidac...)
    reg_hosts_sync = id_1p_sync(A, B, site_reg, site_ent, ts_a, ts_b)
    reg_hosts_ext = collections.defaultdict(set)
    for r, hs in reg_hosts_strict.items():
        reg_hosts_ext[r] |= hs
    for r, hs in reg_hosts_sync.items():
        reg_hosts_ext[r] |= hs
    cats_ext = {r: best_cat(hs) for r, hs in reg_hosts_ext.items()}
    ents_ext = {r: best_ent(hs, r) for r, hs in reg_hosts_ext.items()}
    f["I2_1psync"] = bool(reg_hosts_sync)
    f["I2_ext"] = bool(reg_hosts_ext)
    f["I3_ext"] = any(c == "ads" for c in cats_ext.values())
    f["I4_ext"] = any(c == "analytics" for c in cats_ext.values())
    f["I5_ext"] = any(c in ("functional", "social") for c in cats_ext.values())
    for r, hs in sorted(reg_hosts_ext.items()):
        src = "both" if (r in reg_hosts_strict and r in reg_hosts_sync) else ("3p_strict" if r in reg_hosts_strict else "1p_sync")
        flows_ext_out.append({
            "domain": dom, "stratum": f["stratum"], "stratum_frame": f["stratum_frame"],
            "recipient": r, "hosts": sorted(hs)[:5], "entity": ents_ext[r],
            "category": cats_ext[r], "source": src, "ips": sorted(ips_by_reg.get(r, set()))[:5],
        })

    # I7 cơ chế đồng ý (gộp), nút, và tiền phân loại C0–C5 (codebook Q-F)
    f["banner_block"] = bool(A.get("banner_blocks"))
    f["cmp_script"] = bool(A.get("cmp_script"))
    f["banner_any"] = f["banner_block"] or f["cmp_script"]
    f["reject_button"] = bool(A.get("reject_buttons"))
    f["reject_in_banner"] = bool(f["banner_any"] and f["reject_button"])
    f["consent_button"] = bool(A.get("consent_buttons"))
    f["consent_mech_auto"] = (
        "C0" if not f["banner_any"] else
        "C3_or_C4" if f["reject_button"] else
        "C2" if f["consent_button"] else "C1"
    )

    # I8/I9 sau khi bấm từ chối: loại trường hợp click lỗi; tách B0 (any req) vs B2/B3 (id-bearing)
    if C and C.get("reject_clicked_at") is not None:
        click_ok = not bool(C.get("reject_click_err"))
        f["reject_click_ok"] = click_ok
        f["reject_click_err"] = C.get("reject_click_err")
        if click_ok:
            ts_c = parse_ts(C.get("ts"))
            # Cookie bền vững trong C (3P và 1P)
            c_3p_regs = set(k[0] for k in id_cookies(C.get("cookies", []), site_reg, site_ent, ts_c))
            c_1p_toks = set()
            for c in C.get("cookies", []):
                d = c["d"].lstrip(".").lower()
                if d and psl.reg(d) == site_reg and c.get("exp", -1) != -1 and c["exp"] - ts_c >= 86400:
                    c_1p_toks |= extract_1p_tokens(c["v"])
            after_hosts_any = set()
            after_hosts_id = set()
            for r in C.get("requests", []):
                if not r.get("after_click"):
                    continue
                try:
                    u = urlsplit(r["url"])
                    h = (u.hostname or "").lower()
                except Exception:
                    continue
                if not h or psl.reg(h) == site_reg or entity(h) == site_ent:
                    continue
                after_hosts_any.add(h)
                hr = psl.reg(h)
                has_id = (hr in c_3p_regs) or any(v in c_1p_toks for _, v in parse_qsl(u.query))
                if has_id:
                    after_hosts_id.add(h)
            f["after_reject_third_hosts"] = len(after_hosts_any)
            f["I8_after_reject_ads_any"] = any(category(h) == "ads" for h in after_hosts_any)
            f["I9_after_reject_analytics_any"] = any(category(h) == "analytics" for h in after_hosts_any)
            f["I8_after_reject_ads"] = any(category(h) == "ads" for h in after_hosts_id)
            f["I9_after_reject_analytics"] = any(category(h) == "analytics" for h in after_hosts_id)

    # Chính sách quyền riêng tư (RQ4): tách bản thô vs bản làm sạch hợp lệ
    pf = os.path.join(CR, "policy", dom + ".txt")
    f["policy_found_raw"] = os.path.exists(pf) and os.path.getsize(pf) > 300
    f["policy_url"] = A.get("policy_url")
    if f["policy_found_raw"]:
        txt = open(pf, encoding="utf-8", errors="replace").read()
        valid, reason, is_ext_grp = validate_policy(dom, site_reg, A.get("policy_url"), A.get("policy_link_text"), txt)
        f["policy_found"] = valid
        f["policy_invalid_reason"] = reason
        f["policy_external_group"] = is_ext_grp
        if valid:
            pf_dict, sh = policy_feats(txt)
            f["policy"] = pf_dict
            f["policy_simhash"] = sh
    else:
        f["policy_found"] = False
        f["policy_invalid_reason"] = None
        f["policy_external_group"] = False

    feats.append(f)

with open(os.path.join(OUT, "site_features.jsonl"), "w") as fo:
    for f in feats:
        fo.write(json.dumps(f, ensure_ascii=False) + "\n")
with open(os.path.join(OUT, "flows.jsonl"), "w") as fo:
    for f in flows_out:
        fo.write(json.dumps(f, ensure_ascii=False) + "\n")
with open(os.path.join(OUT, "flows_ext.jsonl"), "w") as fo:
    for f in flows_ext_out:
        fo.write(json.dumps(f, ensure_ascii=False) + "\n")

ok = [f for f in feats if f["ok"]]
lines = [f"site: {len(feats)} · đo được: {len(ok)}"]
for s in sorted({f["stratum"] for f in ok}):
    g = [f for f in ok if f["stratum"] == s]
    pc = lambda k: f"{sum(bool(x.get(k)) for x in g)}/{len(g)}"
    lines.append(f"{s:6s} n={len(g):4d} I1={pc('I1')} I2={pc('I2')} (ext={pc('I2_ext')}) I3={pc('I3')} (ext={pc('I3_ext')}) I4={pc('I4')} (ext={pc('I4_ext')}) banner={pc('banner_any')} pol={pc('policy_found')} (raw={pc('policy_found_raw')})")
unc = collections.Counter(r for f in ok for r in f.get("unclassified_recipients", []))
lines.append("bên nhận định danh chưa phân loại (top 25): " + ", ".join(f"{k}:{v}" for k, v in unc.most_common(25)))
inv = collections.Counter(f["policy_invalid_reason"] for f in ok if f.get("policy_found_raw") and not f.get("policy_found"))
lines.append("chính sách thô bị loại do không hợp lệ: " + ", ".join(f"{k}:{v}" for k, v in inv.most_common()))
open(os.path.join(OUT, "tom-tat.txt"), "w").write("\n".join(lines) + "\n")
print("\n".join(lines))

"""K7 — toàn bộ phân tích độ nhạy, kiểm định hội tụ và sai số theo cụm (docs/05-protocol.md §4–5; phan-bien-K7 F8–F18).
Chỉ dùng stdlib. Chạy từ 5/:
  python3 -I code/sensitivity.py  → data/analysis/do-nhay.md
Đọc:
  - data/analysis/{site_features.jsonl, flows.jsonl, flows_ext.jsonl}
  - data/analysis-sens30/site_features.jsonl, data/analysis-nomedia/site_features.jsonl
  - data/frame/raw/dbip-country-lite-2026-11.csv.gz (CC BY 4.0)
  - data/frame/raw/easyprivacy.txt, data/frame/raw/easylist.txt
  - code/entity_hq.json, code/vn_entities.json, data/frame/raw/disconnect-services.json"""
import os, sys, json, math, gzip, csv, re, collections, bisect, ipaddress
sys.path.insert(0, os.path.dirname(__file__))
from psl import PSL

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ANA = os.path.join(BASE, "data", "analysis")
RAW = os.path.join(BASE, "data", "frame", "raw")
psl = PSL(os.path.join(RAW, "public_suffix_list.dat"))
HQ = json.load(open(os.path.join(BASE, "code", "entity_hq.json")))

F_MAIN = [json.loads(l) for l in open(os.path.join(ANA, "site_features.jsonl"))]
OK = [f for f in F_MAIN if f["ok"]]
BY_DOM = {f["domain"]: f for f in OK}
FL = [json.loads(l) for l in open(os.path.join(ANA, "flows.jsonl"))]
FL_EXT = [json.loads(l) for l in open(os.path.join(ANA, "flows_ext.jsonl"))]

Z95 = 1.959963984540054

def wilson(k, n, z=Z95):
    if n == 0:
        return (float("nan"),) * 3
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return p, max(0.0, c - h), min(1.0, c + h)

def fmt(k, n):
    p, lo, hi = wilson(k, n)
    return f"{k}/{n} = {100*p:.1f}% [{100*lo:.1f}–{100*hi:.1f}]" if n else "0/0"

def mcnemar_exact(b, c):
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    return min(1.0, 2.0 * sum(math.comb(n, i) for i in range(k + 1)) * (0.5 ** n))

def kappa_stats(pairs):
    """pairs = list of (a_bool, b_bool) -> (agree_pct, kappa, pabak, b_only_a, c_only_b, p_mcnemar)"""
    n = len(pairs)
    if n == 0:
        return 0.0, float("nan"), float("nan"), 0, 0, 1.0
    a11 = sum(1 for x, y in pairs if x and y)
    a10 = sum(1 for x, y in pairs if x and not y)
    a01 = sum(1 for x, y in pairs if not x and y)
    a00 = sum(1 for x, y in pairs if not x and not y)
    po = (a11 + a00) / n
    pe = ((a11 + a10) * (a11 + a01) + (a01 + a00) * (a10 + a00)) / (n * n)
    kap = (po - pe) / (1 - pe) if pe < 1.0 else (1.0 if po == 1.0 else 0.0)
    pabak = 2 * po - 1
    return 100 * po, kap, pabak, a10, a01, mcnemar_exact(a10, a01)

def cluster_ci(items, get_y, get_cluster):
    """Liang-Zeger / sandwich cluster-robust SE for a binary proportion."""
    clusters = collections.defaultdict(list)
    for it in items:
        clusters[get_cluster(it)].append(1 if get_y(it) else 0)
    N = len(items)
    G = len(clusters)
    if N == 0 or G <= 1:
        return float("nan"), float("nan"), float("nan"), float("nan"), G
    p = sum(sum(v) for v in clusters.values()) / N
    var_cr = (G / (G - 1)) * sum((sum(v) - len(v) * p) ** 2 for v in clusters.values()) / (N * N)
    se_cr = math.sqrt(max(0.0, var_cr))
    var_naive = p * (1 - p) / N if 0 < p < 1 else 0.0
    deff = var_cr / var_naive if var_naive > 0 else 1.0
    return p, max(0.0, p - Z95 * se_cr), min(1.0, p + Z95 * se_cr), deff, G

L = ["# Phân tích độ nhạy, hội tụ và sai số theo cụm (tự sinh bởi code/sensitivity.py)", ""]

# ----------------------------------------------------------------------
# 1. SENS30 & NOMEDIA (Protocol §5, §8)
# ----------------------------------------------------------------------
L += ["## 1. Độ nhạy thời gian chờ (30 s vs 15 s) và chặn media (Protocol §5, §8)", ""]
for label, dname in (("Chờ 30 s (`sens30`) vs chính 15 s", "analysis-sens30"), ("Không chặn media (`nomedia`) vs chính", "analysis-nomedia")):
    p = os.path.join(BASE, "data", dname, "site_features.jsonl")
    if not os.path.exists(p):
        L.append(f"- {label}: chưa có `{dname}`")
        continue
    other = {f["domain"]: f for f in (json.loads(l) for l in open(p)) if f["ok"]}
    common = sorted(d for d in other if d in BY_DOM)
    L.append(f"### {label} (n ghép cặp đo được cả hai = {len(common)})")
    L.append("")
    L.append("| Chỉ số | Chính (15 s) | Độ nhạy | Đồng thuận | κ | PABAK | Lệch (+/−) | p McNemar |")
    L.append("|---|---|---|---|---|---|---|---|")
    for k in ("I1", "I2", "I3", "I4", "I2_ext", "I3_ext", "I4_ext", "banner_any", "policy_found"):
        pairs = [(bool(BY_DOM[d].get(k)), bool(other[d].get(k))) for d in common]
        po, kap, pab, a10, a01, pm = kappa_stats(pairs)
        k1 = sum(x for x, _ in pairs)
        k2 = sum(y for _, y in pairs)
        L.append(f"| {k} | {k1}/{len(common)} ({100*k1/len(common):.1f}%) | {k2}/{len(common)} ({100*k2/len(common):.1f}%) | {po:.1f}% | {kap:.3f} | {pab:.3f} | -{a10}/+{a01} | {pm:.4g} |")
    L.append("")

# ----------------------------------------------------------------------
# 2. Định nghĩa định danh (Cookie-only vs Strict vs +1P->3P Sync) & .vn-only
# ----------------------------------------------------------------------
L += ["## 2. Độ nhạy định nghĩa định danh (F10) và khung mẫu `.vn`-only (F8)", ""]
L.append("| Phiên bản định nghĩa | Tất cả (n=946) | Tầng `vn` (n=578) | Chỉ `.vn` (gồm vn+gov+edu, n=920) |")
L.append("|---|---|---|---|")
only_vn_tld = [f for f in OK if f["stratum_frame"] != "nonvn"]
only_vn = [f for f in OK if f["stratum_frame"] == "vn"]
for lbl, k in (
    ("I2 chỉ đếm cookie 3P (`I2_cookie_only`)", "I2_cookie_only"),
    ("I2 chuẩn protocol (3P cookie + 3P URL ≥2 req)", "I2"),
    ("I2 mở rộng F10 (+ 1P→3P cookie-sync)", "I2_ext"),
    ("I3 chỉ đếm cookie 3P (`I3_cookie_only`)", "I3_cookie_only"),
    ("I3 chuẩn protocol (quảng cáo)", "I3"),
    ("I3 mở rộng F10 (+ 1P→3P cookie-sync)", "I3_ext"),
    ("I4 chỉ đếm cookie 3P (`I4_cookie_only`)", "I4_cookie_only"),
    ("I4 chuẩn protocol (analytics)", "I4"),
    ("I4 mở rộng F10 (+ GA4/1P→3P cookie-sync)", "I4_ext"),
):
    L.append(
        f"| {lbl} | {fmt(sum(bool(f.get(k)) for f in OK), len(OK))} "
        f"| {fmt(sum(bool(f.get(k)) for f in only_vn), len(only_vn))} "
        f"| {fmt(sum(bool(f.get(k)) for f in only_vn_tld), len(only_vn_tld))} |"
    )
L.append("")

# ----------------------------------------------------------------------
# 3. Cách đọc hẹp H vs rộng R của Q-A (Codebook §1 Q-A)
# ----------------------------------------------------------------------
L += ["## 3. Độ nhạy cách đọc pháp lý Q-A: H (chỉ entity có tài khoản liên kết danh tính) vs R", ""]
LINK = {"Google LLC", "Facebook, Inc.", "Microsoft Corporation", "ByteDance Ltd.", "VNG Corporation"}
by_dom_fl = collections.defaultdict(list)
for fl in FL:
    by_dom_fl[fl["domain"]].append(fl)
by_dom_flext = collections.defaultdict(list)
for fl in FL_EXT:
    by_dom_flext[fl["domain"]].append(fl)

L.append(f"Tập entity có hệ sinh thái tài khoản người dùng (cách đọc H): {', '.join(sorted(LINK))}.")
L.append("")
L.append("| Tầng khung | I2 chuẩn (R) | I2 cách đọc H | I2 mở rộng F10 (R) | I2 mở rộng F10 (H) |")
L.append("|---|---|---|---|---|")
for st in ("vn", "nonvn", "gov", "edu", None):
    g = [f for f in OK if st is None or f["stratum_frame"] == st]
    k_r = sum(bool(f.get("I2")) for f in g)
    k_h = sum(any(fl["entity"] in LINK for fl in by_dom_fl[f["domain"]]) for f in g)
    k_er = sum(bool(f.get("I2_ext")) for f in g)
    k_eh = sum(any(fl["entity"] in LINK for fl in by_dom_flext[f["domain"]]) for f in g)
    L.append(f"| {st or '**Tất cả**'} | {fmt(k_r, len(g))} | {fmt(k_h, len(g))} | {fmt(k_er, len(g))} | {fmt(k_eh, len(g))} |")
L.append("")

# ----------------------------------------------------------------------
# 4. RQ3: Entity HQ (unknown=VN vs foreign) + DB-IP Lite Server IP (F13)
# ----------------------------------------------------------------------
L += ["## 4. RQ3: Trụ sở pháp nhân (`entity_hq.json`) vs Vị trí máy chủ (DB-IP Lite 2026-11, F13)", ""]
unk_ents = [e for e in {fl["entity"] for fl in FL} if HQ.get(e, {}).get("hq") in (None, "?")]
unk_fl = sum(1 for fl in FL if fl["entity"] in unk_ents)
L.append(f"- Độ phủ trụ sở pháp nhân trên luồng định danh chuẩn protocol: **{len(FL)-unk_fl}/{len(FL)} = {100*(len(FL)-unk_fl)/max(len(FL),1):.1f}%** (chưa rõ: {unk_fl}/{len(FL)} = {100*unk_fl/max(len(FL),1):.1f}%, {len(unk_ents)} entity đuôi dài).")
for mode in ("unknown=VN", "unknown=foreign"):
    def is_for(e):
        h = HQ.get(e, {}).get("hq")
        if h in (None, "?"):
            return mode == "unknown=foreign"
        return h != "VN"
    k = sum(any(is_for(fl["entity"]) for fl in by_dom_fl[f["domain"]]) for f in OK)
    L.append(f"- Site có ≥ 1 luồng định danh tới pháp nhân nước ngoài ({mode}): {fmt(k, len(OK))}")

# DB-IP Lite IP geolocation
dbip_path = os.path.join(RAW, "dbip-country-lite-2026-11.csv.gz")
if os.path.exists(dbip_path):
    v4_s, v4_e, v4_c = [], [], []
    v6_s, v6_e, v6_c = [], [], []
    with gzip.open(dbip_path, "rt", encoding="utf-8") as gf:
        for s_ip, e_ip, cc in csv.reader(gf):
            a = ipaddress.ip_address(s_ip)
            b = ipaddress.ip_address(e_ip)
            if a.version == 4:
                v4_s.append(int(a)); v4_e.append(int(b)); v4_c.append(cc)
            else:
                v6_s.append(int(a)); v6_e.append(int(b)); v6_c.append(cc)

    def ip_cc(ip_str):
        try:
            addr = ipaddress.ip_address(ip_str)
        except Exception:
            return None
        iv = int(addr)
        if addr.version == 4:
            idx = bisect.bisect_right(v4_s, iv) - 1
            if idx >= 0 and iv <= v4_e[idx]:
                return v4_c[idx]
        else:
            idx = bisect.bisect_right(v6_s, iv) - 1
            if idx >= 0 and iv <= v6_e[idx]:
                return v6_c[idx]
        return None

    fl_with_ip = 0
    fl_ip_foreign = 0
    fl_ip_vn = 0
    fl_diverge_hq_for_ip_vn = 0
    fl_diverge_hq_vn_ip_for = 0
    ip_cc_cnt = collections.Counter()
    sites_ip_foreign = set()
    sites_ip_any = set()
    for fl in FL:
        ccs = {ip_cc(ip) for ip in fl.get("ips", []) if ip} - {None, "ZZ"}
        if not ccs:
            continue
        fl_with_ip += 1
        sites_ip_any.add(fl["domain"])
        for cc in ccs:
            ip_cc_cnt[cc] += 1
        has_for_ip = any(cc != "VN" for cc in ccs)
        only_vn_ip = (ccs == {"VN"})
        if has_for_ip:
            fl_ip_foreign += 1
            sites_ip_foreign.add(fl["domain"])
        if only_vn_ip:
            fl_ip_vn += 1
        hq = HQ.get(fl["entity"], {}).get("hq")
        if hq not in (None, "?", "VN") and only_vn_ip:
            fl_diverge_hq_for_ip_vn += 1
        if hq == "VN" and has_for_ip:
            fl_diverge_hq_vn_ip_for += 1

    L.append(f"- **Định vị IP máy chủ (DB-IP Lite 2026-11, CC BY 4.0):** tra được IP cho {fl_with_ip}/{len(FL)} luồng định danh ({100*fl_with_ip/max(len(FL),1):.1f}%).")
    L.append(f"  - Site có ≥ 1 luồng định danh đi tới IP máy chủ ngoài VN: {fmt(len(sites_ip_foreign), len(OK))} (so với trụ sở pháp nhân ngoài VN: {fmt(sum(any(HQ.get(fl['entity'], {}).get('hq') not in (None, '?', 'VN') for fl in by_dom_fl[f['domain']]) for f in OK), len(OK))}).")
    L.append(f"  - Phân bố quốc gia IP của luồng định danh (top 10): " + ", ".join(f"{cc}: {c}" for cc, c in ip_cc_cnt.most_common(10)))
    L.append(f"  - **Mâu thuẫn trụ sở vs IP (anycast/CDN, F13):**")
    L.append(f"    - Pháp nhân nước ngoài nhưng IP chỉ ở VN (edge nội địa): {fl_diverge_hq_for_ip_vn}/{fl_with_ip} ({100*fl_diverge_hq_for_ip_vn/max(fl_with_ip,1):.1f}%) luồng.")
    L.append(f"    - Pháp nhân VN nhưng IP ngoài VN (cloud/CDN nước ngoài): {fl_diverge_hq_vn_ip_for}/{fl_with_ip} ({100*fl_diverge_hq_vn_ip_for/max(fl_with_ip,1):.1f}%) luồng.")
    L.append("  - Lưu ý: crawler không ghi TCP RTT riêng lẻ nên độ lệch anycast đo trực tiếp qua chênh giữa `entity_hq` và DB-IP.")
L.append("")

# ----------------------------------------------------------------------
# 5. Độ hội tụ với EasyPrivacy + EasyList (F16)
# ----------------------------------------------------------------------
L += ["## 5. Độ hội tụ giữa bộ phân loại Disconnect+VN_SUPP và EasyPrivacy/EasyList (F16)", ""]
def parse_adblock_domains(path):
    doms, exc = set(), set()
    if not os.path.exists(path):
        return doms, exc
    for line in open(path, encoding="utf-8", errors="replace"):
        s = line.strip()
        if not s or s.startswith("!") or s.startswith("["):
            continue
        is_exc = s.startswith("@@")
        if is_exc:
            s = s[2:]
        m = re.match(r"^\|\|([a-z0-9.-]+)\^(?:\$([^#]*))?$", s, re.I)
        if not m:
            continue
        dom = m.group(1).lower().strip(".")
        opts = (m.group(2) or "").lower()
        # bỏ quy tắc chỉ giới hạn domain cụ thể (domain=...)
        if "domain=" in opts:
            continue
        if is_exc:
            exc.add(dom)
        else:
            doms.add(dom)
    return doms, exc

ep_d, ep_e = parse_adblock_domains(os.path.join(RAW, "easyprivacy.txt"))
el_d, el_e = parse_adblock_domains(os.path.join(RAW, "easylist.txt"))
ep_all = (ep_d | el_d) - (ep_e | el_e)

def match_list(host, dset):
    labels = host.lower().strip(".").split(".")
    for i in range(len(labels) - 1):
        if ".".join(labels[i:]) in dset:
            return True
    return False

# (a) Mức cặp luồng định danh (FL): Disconnect+VN_SUPP xếp ads/analytics/social vs EasyPrivacy+EasyList
fl_pairs_ep = []
fl_pairs_el_ads = []
for fl in FL:
    hs = fl.get("hosts") or [fl["recipient"]]
    disc_trk = fl["category"] in ("ads", "analytics", "social")
    disc_ads = fl["category"] == "ads"
    ep_hit = any(match_list(h, ep_all) for h in hs) or match_list(fl["recipient"], ep_all)
    el_hit = any(match_list(h, el_d - el_e) for h in hs) or match_list(fl["recipient"], el_d - el_e)
    fl_pairs_ep.append((disc_trk, ep_hit))
    fl_pairs_el_ads.append((disc_ads, el_hit))

po1, k1, pab1, b1, c1, _ = kappa_stats(fl_pairs_ep)
po2, k2, pab2, b2, c2, _ = kappa_stats(fl_pairs_el_ads)

# (b) Mức site (n=946): có ≥1 luồng định danh được Disconnect+VN_SUPP xếp tracker (ads/analytics/social) vs EasyPrivacy+EasyList
site_pairs_trk = []
site_pairs_ads = []
for f in OK:
    fls = by_dom_fl[f["domain"]]
    d_trk = any(fl["category"] in ("ads", "analytics", "social") for fl in fls)
    d_ads = bool(f.get("I3"))
    e_trk = any(any(match_list(h, ep_all) for h in (fl.get("hosts") or [fl["recipient"]])) or match_list(fl["recipient"], ep_all) for fl in fls)
    e_ads = any(any(match_list(h, el_d - el_e) for h in (fl.get("hosts") or [fl["recipient"]])) or match_list(fl["recipient"], el_d - el_e) for fl in fls)
    site_pairs_trk.append((d_trk, e_trk))
    site_pairs_ads.append((d_ads, e_ads))

spo1, sk1, spab1, sb1, sc1, _ = kappa_stats(site_pairs_trk)
spo2, sk2, spab2, sb2, sc2, _ = kappa_stats(site_pairs_ads)

L.append(f"Quy tắc domain tổng quát trích từ `easyprivacy.txt` ({len(ep_d)} domain) và `easylist.txt` ({len(el_d)} domain), bản 22/11/2026.")
L.append("")
L.append("| Mức đối chiếu | So sánh | Đồng thuận | Cohen's κ | PABAK | Chỉ Disconnect | Chỉ EasyList/EP |")
L.append("|---|---|---|---|---|---|---|")
L.append(f"| Mức luồng (n={len(FL)}) | Tracker (ads/analytics/social) vs EP+EL | {po1:.1f}% | {k1:.3f} | {pab1:.3f} | {b1} | {c1} |")
L.append(f"| Mức luồng (n={len(FL)}) | Quảng cáo (`ads`) vs EasyList | {po2:.1f}% | {k2:.3f} | {pab2:.3f} | {b2} | {c2} |")
L.append(f"| Mức site (n={len(OK)}) | Có tracker định danh vs EP+EL | {spo1:.1f}% | {sk1:.3f} | {spab1:.3f} | {sb1} | {sc1} |")
L.append(f"| Mức site (n={len(OK)}) | Có quảng cáo định danh (`I3`) vs EasyList | {spo2:.1f}% | {sk2:.3f} | {spab2:.3f} | {sb2} | {sc2} |")
L.append("")

# ----------------------------------------------------------------------
# 6. Sai số chuẩn theo cụm ngoại sinh (Cluster-Robust SE, Protocol §4 & F9)
# ----------------------------------------------------------------------
L += ["## 6. Sai số chuẩn theo cụm (Cluster-Robust SE, Protocol §4 & F9)", ""]
# Xây dựng cụm NGOẠI SINH (không phụ thuộc biến kết quả I2/I3):
# (a) Cụm chủ sở hữu / quản trị chung: nối các site dùng chung GTM container, hoặc dùng chung GA/FB property ID,
#     hoặc dùng chung mẫu chính sách SimHash (Hamming <= 6 bit).
# Lưu ý: không gom cụm theo "entity quảng cáo chính" (vì biến đó nội sinh với I3).
par_org = {f["domain"]: f["domain"] for f in OK}
def find_org(x):
    while par_org[x] != x:
        par_org[x] = par_org[par_org[x]]
        x = par_org[x]
    return x
def union_org(a, b):
    ra, rb = find_org(a), find_org(b)
    if ra != rb:
        par_org[ra] = rb

# Nối theo GTM container dùng chung
by_gtm = collections.defaultdict(list)
for f in OK:
    for g in f.get("gtm_containers", []):
        by_gtm[g].append(f["domain"])
shared_gtm = {g: ds for g, ds in by_gtm.items() if len(ds) >= 2}
for ds in shared_gtm.values():
    for d in ds[1:]:
        union_org(ds[0], d)

# Nối theo mẫu chính sách SimHash trùng (Hamming <= 6)
pols_ok = [f for f in OK if f.get("policy_found") and f.get("policy_simhash")]
sh_ok = [(f["domain"], int(f["policy_simhash"], 16)) for f in pols_ok]
for i in range(len(sh_ok)):
    di, hi = sh_ok[i]
    for j in range(i + 1, len(sh_ok)):
        dj, hj = sh_ok[j]
        if (hi ^ hj).bit_count() <= 6:
            union_org(di, dj)

# Nối thêm theo hạ tầng hosting: cùng IP trang chủ (từ sites.jsonl Profile A request đầu tiên)
org_groups = collections.defaultdict(list)
for f in OK:
    org_groups[find_org(f["domain"])].append(f["domain"])
org_multi = [g for g in org_groups.values() if len(g) >= 2]

L.append(f"- Định nghĩa cụm ngoại sinh (quản trị chung): nối hai site khi dùng chung **GTM container** ({len(shared_gtm)} container dùng chung) hoặc **mẫu chính sách SimHash** (Hamming ≤ 6 bit). Tổng: **{len(org_groups)} cụm** trên {len(OK)} site ({len(org_multi)} cụm có ≥ 2 site, gồm {sum(len(g) for g in org_multi)} site).")
L.append("- Lý do không gom cụm theo bên nhận quảng cáo (ví dụ mọi site có Google Ads vào 1 cụm): cách gom đó nội sinh với biến kết quả I2/I3 nên sẽ thổi phồng phương sai giả tạo.")
L.append("")
L.append("| Chỉ số & tập | Tỷ lệ | KTC 95% Wilson (độc lập) | KTC 95% Cluster-Robust | Số cụm (G) | DEFF |")
L.append("|---|---|---|---|---|---|")
for lbl, grp, k in (
    ("I2 — Tất cả", OK, "I2"),
    ("I3 — Tất cả", OK, "I3"),
    ("I2 — Tầng `vn`", only_vn, "I2"),
    ("I3 — Tầng `vn`", only_vn, "I3"),
    ("I2_ext — Tất cả", OK, "I2_ext"),
    ("I3_ext — Tất cả", OK, "I3_ext"),
    ("I4_ext — Tất cả", OK, "I4_ext"),
):
    cnt = sum(bool(f.get(k)) for f in grp)
    p, wlo, whi = wilson(cnt, len(grp))
    _, clo, chi, deff, G = cluster_ci(grp, lambda x, kk=k: bool(x.get(kk)), lambda x: find_org(x["domain"]))
    L.append(f"| {lbl} (n={len(grp)}) | {100*p:.1f}% | [{100*wlo:.1f}–{100*whi:.1f}] | [{100*clo:.1f}–{100*chi:.1f}] | {G} | {deff:.2f} |")
L.append("")

# ----------------------------------------------------------------------
# 7. Gom cụm mẫu chính sách bằng SimHash 64-bit (F15)
# ----------------------------------------------------------------------
L += ["## 7. Gom cụm mẫu chính sách dùng chung bằng SimHash 64-bit (F15)", ""]
pols = [f for f in OK if f.get("policy_found") and f.get("policy_simhash")]
# Union-Find trên khoảng cách Hamming <= 6 bit
parent = {f["domain"]: f["domain"] for f in pols}
def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x
def union(a, b):
    ra, rb = find(a), find(b)
    if ra != rb:
        parent[ra] = rb

sh_ints = [(f["domain"], int(f["policy_simhash"], 16)) for f in pols]
for i in range(len(sh_ints)):
    di, hi = sh_ints[i]
    for j in range(i + 1, len(sh_ints)):
        dj, hj = sh_ints[j]
        if (hi ^ hj).bit_count() <= 6:
            union(di, dj)

p_clusters = collections.defaultdict(list)
for f in pols:
    p_clusters[find(f["domain"])].append(f)
multi_clusters = sorted((c for c in p_clusters.values() if len(c) >= 2), key=lambda x: -len(x))
in_shared = sum(len(c) for c in multi_clusters)
L.append(f"- Chính sách hợp lệ có SimHash: {len(pols)} → gom thành **{len(p_clusters)} cụm mẫu độc lập** (ngưỡng Hamming ≤ 6/64 bit).")
L.append(f"- Số site thuộc cụm dùng chung (≥ 2 site cùng mẫu): **{in_shared}/{len(pols)} ({100*in_shared/max(len(pols),1):.1f}%)** trải trên {len(multi_clusters)} cụm.")
L.append("- Top 10 cụm mẫu chính sách dùng chung:")
for idx, cl in enumerate(multi_clusters[:10], 1):
    doms = sorted(x["domain"] for x in cl)
    pdpl_c = sum(x["policy"]["LAW_PDPL"] in ("AFF", "COND") for x in cl)
    L.append(f"  {idx}. **n={len(cl)}** (PDPL={pdpl_c}): {', '.join(doms[:8])}" + (f" … (+{len(doms)-8})" if len(doms) > 8 else ""))
L.append("")

said = lambda f, ks: any(f["policy"].get(k) in ("AFF", "COND") for k in ks)
g3_pol = [f for f in pols if f.get("I3")]
L.append("| Chỉ số RQ4 (trên chính sách hợp lệ) | Tỷ lệ | KTC 95% Wilson | KTC 95% theo cụm SimHash | Số cụm | DEFF |")
L.append("|---|---|---|---|---|---|")
for lbl, grp, fn in (
    ("Viện dẫn PDPL (`LAW_PDPL`)", pols, lambda f: f["policy"]["LAW_PDPL"] in ("AFF", "COND")),
    ("Chỉ viện dẫn NĐ 13/2023", pols, lambda f: f["policy"]["DEC_13"] in ("AFF", "COND") and f["policy"]["LAW_PDPL"] == "NONE" and f["policy"]["DEC_356"] == "NONE"),
    ("Nhắc chuyển ra nước ngoài (`XBORDER`)", pols, lambda f: f["policy"]["XBORDER"] in ("AFF", "COND")),
    ("Có I3 nhưng không nhắc bên thứ ba/quảng cáo", g3_pol, lambda f: not said(f, ("THIRD", "ADPART", "ADNAME"))),
    ("Có I3 nhưng không nhắc cookie", g3_pol, lambda f: not said(f, ("COOKIE",))),
):
    cnt = sum(bool(fn(f)) for f in grp)
    p, wlo, whi = wilson(cnt, len(grp))
    _, clo, chi, deff, G = cluster_ci(grp, fn, lambda x: find(x["domain"]))
    L.append(f"| {lbl} (n={len(grp)}) | {100*p:.1f}% | [{100*wlo:.1f}–{100*whi:.1f}] | [{100*clo:.1f}–{100*chi:.1f}] | {G} | {deff:.2f} |")

out_path = os.path.join(ANA, "do-nhay.md")
open(out_path, "w").write("\n".join(L) + "\n")
print("Wrote", out_path, f"({len(L)} lines)")

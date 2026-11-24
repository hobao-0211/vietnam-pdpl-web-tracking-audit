"""K7 — thống kê đã chốt trước (docs/05-protocol.md §1, §4). Chỉ stdlib.
python3 -I code/stats.py <analysis_dir>   (đọc site_features.jsonl, flows.jsonl, flows_ext.jsonl) → <analysis_dir>/ket-qua.md
- Tỷ lệ + KTC 95% Wilson theo tầng khung (gov/edu/vn/nonvn) và tầng phân tích (GOV/EDU/BC/TM/KHAC/GATED)
- Báo song song chuẩn protocol (I2–I5) và bản mở rộng 1P->3P cookie-sync (I2_ext–I4_ext, F10)
- So sánh tầng khung (4 phép: vn–gov, vn–edu, vn–nonvn, gov–edu), z hai tỷ lệ, hiệu chỉnh Holm, hiệu số + KTC 95% Newcombe-Wilson
- RQ2: cơ chế đồng ý C0–C5 (tự động), nút từ chối, hậu quả bấm từ chối (tách B0 vs B2/B3 mang định danh; loại click lỗi)
- RQ3: phân bố entity của luồng định danh + độ phủ trụ sở pháp nhân (code/entity_hq.json)
- RQ4: chính sách làm sạch (tách bản thô vs bản hợp lệ), nói–làm kèm kiểm định McNemar ghép cặp"""
import sys, os, json, math, collections

D = sys.argv[1]
F = [json.loads(l) for l in open(os.path.join(D, "site_features.jsonl"))]
FL = [json.loads(l) for l in open(os.path.join(D, "flows.jsonl"))]
FL_EXT_P = os.path.join(D, "flows_ext.jsonl")
FL_EXT = [json.loads(l) for l in open(FL_EXT_P)] if os.path.exists(FL_EXT_P) else []
ok = [f for f in F if f["ok"]]

Z95 = 1.959963984540054

def wilson(k, n, z=Z95):
    if n == 0:
        return (float("nan"),) * 3
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return p, max(0.0, c - h), min(1.0, c + h)

def newcombe_diff(k1, n1, k2, n2):
    p1, l1, u1 = wilson(k1, n1)
    p2, l2, u2 = wilson(k2, n2)
    diff = p1 - p2
    lo = diff - math.sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2)
    hi = diff + math.sqrt((u1 - p1) ** 2 + (p2 - l2) ** 2)
    return diff, max(-1.0, lo), min(1.0, hi)

def fmt(k, n):
    p, lo, hi = wilson(k, n)
    return f"{k}/{n} = {100*p:.1f}% [{100*lo:.1f}–{100*hi:.1f}]" if n else "0/0"

def ztest(k1, n1, k2, n2):
    if min(n1, n2) == 0:
        return float("nan")
    p = (k1 + k2) / (n1 + n2)
    se = math.sqrt(p * (1 - p) * (1 / n1 + 1 / n2))
    if se == 0:
        return 1.0
    z = (k1 / n1 - k2 / n2) / se
    return math.erfc(abs(z) / math.sqrt(2))

def mcnemar_exact(b, c):
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    p = 2.0 * sum(math.comb(n, i) for i in range(k + 1)) * (0.5 ** n)
    return min(1.0, p)

def holm(ps):
    order = sorted(range(len(ps)), key=lambda i: ps[i])
    adj = [0.0] * len(ps)
    m = len(ps)
    run = 0.0
    for r, i in enumerate(order):
        run = max(run, min(1.0, (m - r) * ps[i]))
        adj[i] = run
    return adj

L = [
    "# Kết quả K7 (tự sinh bởi code/stats.py — không sửa tay)",
    "",
    f"Site trong dữ liệu: {len(F)} · đo được (A và B ok): {len(ok)} · lỗi: {len(F)-len(ok)} ({100*(len(F)-len(ok))/max(len(F),1):.1f}%)",
    "",
]
err = collections.Counter((f.get("err") or "")[:40] for f in F if not f["ok"])
L.append("Lỗi theo loại: " + "; ".join(f"{k or '?'}: {v}" for k, v in err.most_common(8)))
by_err_s = collections.defaultdict(lambda: [0, 0])
for f in F:
    by_err_s[f["stratum_frame"]][0] += 1
    if not f["ok"]:
        by_err_s[f["stratum_frame"]][1] += 1
L.append("Tỷ lệ lỗi theo tầng khung: " + "; ".join(f"{s}: {e}/{t} ({100*e/t:.1f}%)" for s, (t, e) in sorted(by_err_s.items())) + " (mọi tầng < ngưỡng dừng 20%)")
L.append("")

IND = [
    ("I1", "Có request tới bên thứ ba (B0)"),
    ("I2", "Luồng mang định danh chuẩn protocol (3P cookie + 3P URL ≥2 req, B1)"),
    ("I3", "… tới bên quảng cáo (chuẩn protocol)"),
    ("I4", "… tới bên analytics (chuẩn protocol)"),
    ("I5", "… tới bên chức năng/MXH (chuẩn protocol)"),
    ("I2_ext", "Độ nhạy F10: I2 + 1P→3P cookie-sync (GA4/Meta/Admicro)"),
    ("I3_ext", "Độ nhạy F10: I3 + 1P→3P cookie-sync (quảng cáo)"),
    ("I4_ext", "Độ nhạy F10: I4 + 1P→3P cookie-sync (analytics/GA4)"),
    ("banner_any", "Có cơ chế đồng ý (khối banner HOẶC script CMP)"),
    ("reject_in_banner", "Có nút từ chối trong ngữ cảnh banner/CMP"),
    ("reject_button", "Có nút khớp regex từ chối (gồm cả popup không banner)"),
    ("policy_found", "Có chính sách hợp lệ (đã lọc trang ngoài/404/tin tức)"),
    ("policy_found_raw", "Tìm được trang chính sách thô (>300B, trước lọc)"),
]

for col, title in (("stratum_frame", "tầng khung"), ("stratum", "tầng phân tích")):
    strata = sorted({f[col] for f in ok})
    L += [
        f"## RQ1–RQ2–RQ4: tỷ lệ theo {title} (KTC 95% Wilson)",
        "",
        "| Chỉ số | " + " | ".join(strata) + " | Tất cả |",
        "|---|" + "---|" * (len(strata) + 1),
    ]
    for k, t in IND:
        cells = [fmt(sum(bool(f.get(k)) for f in ok if f[col] == s), sum(1 for f in ok if f[col] == s)) for s in strata]
        L.append(f"| {k} {t} | " + " | ".join(cells) + f" | {fmt(sum(bool(f.get(k)) for f in ok), len(ok))} |")
    L.append("")

# So sánh tầng khung (protocol §1 & §4: 4 phép, Holm, hiệu số kèm KTC 95% Newcombe-Wilson)
L += ["## So sánh tầng khung (z hai tỷ lệ, hiệu chỉnh Holm, hiệu số + KTC 95% Newcombe-Wilson)", ""]
pairs = [("vn", "gov"), ("vn", "edu"), ("vn", "nonvn"), ("gov", "edu")]
for k in ("I2", "I3", "I2_ext", "I3_ext", "I4_ext"):
    rows = []
    for a, b in pairs:
        ga = [f for f in ok if f["stratum_frame"] == a]
        gb = [f for f in ok if f["stratum_frame"] == b]
        ka, kb = sum(bool(f.get(k)) for f in ga), sum(bool(f.get(k)) for f in gb)
        diff, dlo, dhi = newcombe_diff(ka, len(ga), kb, len(gb))
        rows.append((a, b, ka, len(ga), kb, len(gb), diff, dlo, dhi, ztest(ka, len(ga), kb, len(gb))))
    adj = holm([r[-1] for r in rows])
    for (a, b, ka, na, kb, nb, diff, dlo, dhi, p), pa in zip(rows, adj):
        L.append(f"- {k} {a} vs {b}: {100*ka/max(na,1):.1f}% vs {100*kb/max(nb,1):.1f}% · hiệu {100*diff:+.1f} điểm % [{100*dlo:+.1f}, {100*dhi:+.1f}] · p={p:.4f} · p_Holm={pa:.4f}")
L.append("")

# RQ2: phân loại tự động C0–C5 và hiệu quả bấm từ chối
L += ["## RQ2: cơ chế đồng ý (tiền phân loại tự động C0–C5) & sau khi bấm từ chối", ""]
c_mech = collections.Counter(f.get("consent_mech_auto", "C0") for f in ok)
for code in ("C0", "C1", "C2", "C3_or_C4"):
    L.append(f"- {code}: {fmt(c_mech[code], len(ok))}")
L.append("- Lưu ý: phân tách C3 vs C4 và gắn cờ C5 (dark pattern) cần kiểm tra ảnh chụp.")
L.append("")

rej_all = [f for f in ok if "reject_click_ok" in f]
rej_ok = [f for f in rej_all if f["reject_click_ok"]]
rej_ban = [f for f in rej_ok if f.get("banner_any")]
L.append(f"- Site có nút khớp regex từ chối (Profile C): {len(rej_all)} · bấm thành công (không lỗi): {len(rej_ok)} · lỗi click timeout: {len(rej_all)-len(rej_ok)}")
L.append(f"- Trong số bấm thành công: có banner/CMP thật: {len(rej_ban)} · không có banner/CMP (nghi popup thông báo): {len(rej_ok)-len(rej_ban)} (< 30 → CHỈ MÔ TẢ theo luật dừng)")
for label, grp in (("Tất cả bấm thành công", rej_ok), ("Chỉ nhóm có banner/CMP", rej_ban)):
    if grp:
        L.append(f"  - [{label}, n={len(grp)}] Sau bấm vẫn có luồng ĐỊNH DANH quảng cáo (I8, B3): {fmt(sum(bool(f.get('I8_after_reject_ads')) for f in grp), len(grp))}")
        L.append(f"  - [{label}, n={len(grp)}] Sau bấm vẫn có luồng ĐỊNH DANH analytics (I9, B2): {fmt(sum(bool(f.get('I9_after_reject_analytics')) for f in grp), len(grp))}")
        L.append(f"  - [{label}, n={len(grp)}] Sau bấm vẫn có BẤT KỲ request quảng cáo nào (B0): {fmt(sum(bool(f.get('I8_after_reject_ads_any')) for f in grp), len(grp))}")
        L.append(f"  - [{label}, n={len(grp)}] Sau bấm vẫn có BẤT KỲ request analytics nào (B0): {fmt(sum(bool(f.get('I9_after_reject_analytics_any')) for f in grp), len(grp))}")
L.append("")

# RQ3
HQ = {}
hqf = os.path.join(os.path.dirname(__file__), "entity_hq.json")
if os.path.exists(hqf):
    HQ = json.load(open(hqf))

ent = collections.Counter()
ents_site = collections.defaultdict(set)
for fl in FL:
    ent[fl["entity"]] += 1
    ents_site[fl["domain"]].add(fl["entity"])
tot = sum(ent.values())
known_fl = sum(c for e, c in ent.items() if HQ.get(e, {}).get("hq") not in (None, "?"))
L += [
    "## RQ3: bên nhận luồng định danh (theo entity, chuẩn protocol)",
    "",
    f"Tổng luồng (site × bên nhận): {tot} · độ phủ bảng trụ sở `entity_hq.json`: {known_fl}/{tot} = {100*known_fl/max(tot,1):.1f}% (ngưỡng protocol ≥ 95%)",
    "",
    "| Entity | Luồng | % | Số site | Trụ sở |",
    "|---|---|---|---|---|",
]
cum = 0
for e, c in ent.most_common(25):
    cum += c
    L.append(f"| {e} | {c} | {100*c/max(tot,1):.1f}% | {sum(e in s for s in ents_site.values())} | {HQ.get(e, {}).get('hq', '?')} |")
L.append(f"\n25 entity đầu chiếm {100*cum/max(tot,1):.1f}% luồng.")
if HQ:
    by_cc = collections.Counter()
    for e, c in ent.items():
        by_cc[HQ.get(e, {}).get("hq", "?")] += c
    L.append("- Phân bố luồng theo nước trụ sở (top 10): " + ", ".join(f"{cc}: {c} ({100*c/max(tot,1):.1f}%)" for cc, c in by_cc.most_common(10)))
    foreign = [d for d, s in ents_site.items() if any(HQ.get(e, {}).get("hq") not in (None, "VN", "?") for e in s)]
    L.append(f"- Site có ≥ 1 luồng định danh chuẩn protocol tới entity trụ sở ngoài VN: {fmt(len(foreign), len(ok))}")
    if FL_EXT:
        ents_ext = collections.defaultdict(set)
        for fl in FL_EXT:
            ents_ext[fl["domain"]].add(fl["entity"])
        foreign_ext = [d for d, s in ents_ext.items() if any(HQ.get(e, {}).get("hq") not in (None, "VN", "?") for e in s)]
        L.append(f"- Độ nhạy F10 (gồm 1P→3P cookie-sync): site có ≥ 1 luồng tới entity trụ sở ngoài VN: {fmt(len(foreign_ext), len(ok))}")
L.append("")

# RQ4
pol_raw = [f for f in ok if f.get("policy_found_raw")]
pol = [f for f in ok if f.get("policy_found")]
inv = collections.Counter(f["policy_invalid_reason"] for f in pol_raw if not f.get("policy_found"))
L += [
    "## RQ4: chính sách quyền riêng tư (nói–làm, bản đã làm sạch)",
    "",
    f"Trang chính sách thô (>300B): {fmt(len(pol_raw), len(ok))} · sau lọc loại trang không hợp lệ: **{fmt(len(pol), len(ok))}**"
    + (" (< 40% → báo trên TẬP CON theo luật dừng)" if len(pol) < 0.4 * len(ok) else ""),
    "Lý do loại trang thô không hợp lệ: " + (", ".join(f"{k}={v}" for k, v in inv.most_common()) or "không có"),
    "",
]
if pol:
    for k in ("LAW_PDPL", "DEC_356", "DEC_13", "COOKIE", "THIRD", "PARTNER", "ADPART", "ADNAME", "ANAME", "XBORDER", "WITHDRAW", "DPO", "RETENTION", "SENSITIVE"):
        c = collections.Counter(f["policy"].get(k, "NONE") for f in pol)
        L.append(f"- {k}: AFF {c['AFF']} · COND {c['COND']} · NEG_ONLY {c['NEG_ONLY']} · NONE {c['NONE']}  (AFF+COND = {fmt(c['AFF']+c['COND'], len(pol))})")
    only13 = [f for f in pol if f["policy"]["DEC_13"] in ("AFF", "COND") and f["policy"]["LAW_PDPL"] == "NONE" and f["policy"]["DEC_356"] == "NONE"]
    L.append(f"- Chỉ viện dẫn NĐ 13/2023 (không nhắc PDPL/NĐ 356): {fmt(len(only13), len(pol))}")
    said = lambda f, ks: any(f["policy"].get(k) in ("AFF", "COND") for k in ks)
    g3 = [f for f in pol if f.get("I3")]
    L.append(f"- Có luồng quảng cáo (I3) nhưng chính sách không nhắc bên thứ ba/đối tác quảng cáo/tên adtech (đã tách GA): {fmt(sum(not said(f, ('THIRD','ADPART','ADNAME')) for f in g3), len(g3))}")
    L.append(f"- Có luồng quảng cáo (I3) nhưng chính sách không nhắc cookie: {fmt(sum(not said(f, ('COOKIE',)) for f in g3), len(g3))}")
    neg = [f for f in g3 if f["policy"].get("THIRD") == "NEG_ONLY"]
    L.append(f"- Ứng viên mâu thuẫn mạnh (`THIRD==NEG_ONLY` & `I3`, cần kiểm tay ngữ cảnh): {len(neg)} site ({', '.join(f['domain'] for f in neg)})")

    # McNemar ghép cặp "nói–làm" trên tập có chính sách (protocol §4)
    L.append("")
    L.append("### Kiểm định McNemar ghép cặp 'nói–làm' (trên tập có chính sách hợp lệ, n=" + str(len(pol)) + ")")
    # (1) Quan sát I3 vs Công bố đối tác/tên quảng cáo (ADPART hoặc ADNAME)
    b1 = sum(bool(f.get("I3")) and not said(f, ("ADPART", "ADNAME")) for f in pol)
    c1 = sum(not bool(f.get("I3")) and said(f, ("ADPART", "ADNAME")) for f in pol)
    L.append(f"- I3 (làm quảng cáo) vs ADPART/ADNAME (nói quảng cáo): làm-không-nói={b1}, nói-không-làm={c1}, p_McNemar={mcnemar_exact(b1, c1):.4g}")
    # (2) Quan sát I3 vs Công bố cookie
    b2 = sum(bool(f.get("I3")) and not said(f, ("COOKIE",)) for f in pol)
    c2 = sum(not bool(f.get("I3")) and said(f, ("COOKIE",)) for f in pol)
    L.append(f"- I3 (làm quảng cáo) vs COOKIE (nói cookie): làm-không-nói={b2}, nói-không-làm={c2}, p_McNemar={mcnemar_exact(b2, c2):.4g}")
    # (3) Quan sát I6 (luồng nước ngoài) vs Công bố XBORDER
    foreign_set = {d for d, s in ents_site.items() if any(HQ.get(e, {}).get("hq") not in (None, "VN", "?") for e in s)}
    b3 = sum((f["domain"] in foreign_set) and not said(f, ("XBORDER",)) for f in pol)
    c3 = sum((f["domain"] not in foreign_set) and said(f, ("XBORDER",)) for f in pol)
    L.append(f"- I6 (luồng entity nước ngoài) vs XBORDER (nói chuyển ra nước ngoài): làm-không-nói={b3}, nói-không-làm={c3}, p_McNemar={mcnemar_exact(b3, c3):.4g}")

open(os.path.join(D, "ket-qua.md"), "w").write("\n".join(L) + "\n")
print("\n".join(L[:15]))
print("… →", os.path.join(D, "ket-qua.md"))

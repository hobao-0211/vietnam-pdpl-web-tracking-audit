"""K7 — sinh gói kiểm định & đối chiếu thủ công cho tác giả (data/validation/).
Chỉ stdlib. Chạy từ 5/: python3 -I code/build_validation.py
Không gán nhãn thay tác giả; xuất sẵn bằng chứng (snippet, URL, đường dẫn ảnh chụp) và mẫu phân tầng tất định (seed 20261122)."""
import os, json, re, random, collections

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ANA = os.path.join(BASE, "data", "analysis")
CR = os.path.join(BASE, "data", "crawl", "main")
VAL = os.path.join(BASE, "data", "validation")
os.makedirs(VAL, exist_ok=True)

F = [json.loads(l) for l in open(os.path.join(ANA, "site_features.jsonl"))]
OK = [f for f in F if f["ok"]]
BY = {f["domain"]: f for f in OK}
FL_EXT = [json.loads(l) for l in open(os.path.join(ANA, "flows_ext.jsonl"))]
EXT_BY = collections.defaultdict(list)
for fl in FL_EXT:
    EXT_BY[fl["domain"]].append(fl)

RECS = collections.defaultdict(dict)
for l in open(os.path.join(CR, "sites.jsonl")):
    d = json.loads(l)
    RECS[d["domain"]][d["profile"]] = d

# ------------------------------------------------------------------
# 1. Toàn bộ site có banner_any hoặc reject_button
# ------------------------------------------------------------------
bn_sites = sorted([f for f in OK if f.get("banner_any") or f.get("reject_button")], key=lambda x: (not x.get("reject_button"), not x.get("banner_any"), x["domain"]))
L1 = [
    "# Gói kiểm tra toàn bộ cơ chế đồng ý và nút từ chối (tự sinh — CHỜ TÁC GIẢ DUYỆT)",
    "",
    f"Tổng cộng **{len(bn_sites)} site** có `banner_any=True` hoặc `reject_button=True` trong 946 site đo được.",
    "Mục tiêu: xác nhận banner cookie thật vs popup thông báo trình duyệt; phân tách C1–C5 (dark patterns).",
    "",
    "| # | Domain | Tầng | banner_block | cmp_script | reject_btn | click_ok | I8_id / I8_any | Tự động | Ảnh chụp | Đoạn chữ banner / ngữ cảnh |",
    "|---|---|---|---|---|---|---|---|---|---|---|",
]
for i, f in enumerate(bn_sites, 1):
    dom = f["domain"]
    A = RECS[dom]["A"]
    snip = ""
    if A.get("banner_blocks"):
        snip = A["banner_blocks"][0][:140]
    else:
        bh = A.get("body_head", "")
        idx = bh.lower().find("từ chối")
        snip = bh[max(0, idx - 60):idx + 80] if idx >= 0 else bh[:120]
    snip = re.sub(r"[\r\n|]+", " ", snip).strip()
    i8s = f"{int(bool(f.get('I8_after_reject_ads')))}/{int(bool(f.get('I8_after_reject_ads_any')))}" if f.get("reject_click_ok") else ("ERR" if "reject_click_ok" in f else "—")
    shot = f"`data/crawl/main/shots/{dom}.jpg`"
    L1.append(
        f"| {i} | `{dom}` | {f['stratum']} | {int(f['banner_block'])} | {int(f['cmp_script'])} | {int(f['reject_button'])} "
        f"| {f.get('reject_click_ok', '—')} | {i8s} | {f['consent_mech_auto']} | {shot} | {snip} |"
    )
open(os.path.join(VAL, "kiem-tra-banner-va-nut.md"), "w").write("\n".join(L1) + "\n")

# ------------------------------------------------------------------
# 2. Site GOV có quảng cáo, mâu thuẫn mạnh, danh sách PDPL, và chính sách bị loại
# ------------------------------------------------------------------
L2 = [
    "# Gói kiểm tra trọng yếu: GOV có quảng cáo, mâu thuẫn mạnh, PDPL và chính sách bị loại",
    "",
    "> Lưu ý đạo đức (Protocol §6, F20–F21): tên miền GOV chỉ dùng nội bộ để kiểm chứng & gửi thông báo trước 30 ngày; khi đưa vào bản thảo phải dùng mã giả danh (`GOV-01`, …).",
    "",
    "## 1. Tầng GOV có luồng định danh quảng cáo (`I3` chuẩn & `I3_ext` 1P→3P sync)",
    "",
    "| Mã giả danh | Domain (NỘI BỘ) | Tầng | I3 chuẩn | I3_ext | Bên nhận quảng cáo (chuẩn / mở rộng) |",
    "|---|---|---|---|---|---|",
]
gov_ads = sorted([f for f in OK if f["stratum_frame"] == "gov" and (f.get("I3") or f.get("I3_ext"))], key=lambda x: (not x.get("I3"), x["domain"]))
for idx, f in enumerate(gov_ads, 1):
    ads_ext = sorted({f"{fl['recipient']} ({fl['entity']}, {fl['source']})" for fl in EXT_BY[f["domain"]] if fl["category"] == "ads"})
    L2.append(f"| GOV-{idx:02d} | `{f['domain']}` | {f['stratum']} | {int(f['I3'])} | {int(f['I3_ext'])} | {'; '.join(ads_ext)} |")

L2 += ["", "## 2. Ứng viên mâu thuẫn mạnh (`THIRD == NEG_ONLY` & `I3`) — trích nguyên văn câu khớp", ""]
negs = [f for f in OK if f.get("policy_found") and f.get("I3") and f["policy"].get("THIRD") == "NEG_ONLY"]
for f in negs:
    dom = f["domain"]
    txt = open(os.path.join(CR, "policy", dom + ".txt"), encoding="utf-8", errors="replace").read()
    L2.append(f"### `{dom}` (`{f.get('policy_url')}`)")
    for sent in re.split(r"[.;!?\n]", txt):
        if re.search(r"bên thứ ba|third[- ]part", sent, re.I):
            L2.append(f"- > {sent.strip()[:260]}")
    L2.append("")

L2 += ["## 3. Toàn bộ site chính sách hợp lệ viện dẫn PDPL (`LAW_PDPL` AFF/COND)", "", "| # | Domain | Tầng | SimHash | URL chính sách |", "|---|---|---|---|---|"]
pdpls = sorted([f for f in OK if f.get("policy_found") and f["policy"].get("LAW_PDPL") in ("AFF", "COND")], key=lambda x: (x.get("policy_simhash") or "", x["domain"]))
for i, f in enumerate(pdpls, 1):
    L2.append(f"| {i} | `{f['domain']}` | {f['stratum_frame']}/{f['stratum']} | `{f.get('policy_simhash', '')}` | {f.get('policy_url', '')} |")

L2 += ["", "## 4. Toàn bộ trang chính sách thô bị bộ lọc tự động loại khỏi RQ4", "", "| # | Domain | Lý do loại | Chữ link | URL |", "|---|---|---|---|---|"]
excls = sorted([f for f in OK if f.get("policy_found_raw") and not f.get("policy_found")], key=lambda x: (x.get("policy_invalid_reason") or "", x["domain"]))
for i, f in enumerate(excls, 1):
    lt = re.sub(r"[\r\n|]+", " ", (RECS[f["domain"]]["A"].get("policy_link_text") or "")).strip()[:50]
    L2.append(f"| {i} | `{f['domain']}` | `{f['policy_invalid_reason']}` | {lt} | {f.get('policy_url', '')} |")

open(os.path.join(VAL, "kiem-tra-gov-va-mau-thuan.md"), "w").write("\n".join(L2) + "\n")

# ------------------------------------------------------------------
# 3. Mẫu kiểm tay phân tầng (seed 20261122, Protocol §5, F12/F15)
# ------------------------------------------------------------------
rnd = random.Random(20261122)

# (a) Banner: toàn bộ dương (banner_any hoặc reject_button) + 70 âm ngẫu nhiên
b_pos = [f for f in OK if f.get("banner_any") or f.get("reject_button")]
b_neg = [f for f in OK if not f.get("banner_any") and not f.get("reject_button")]
b_samp = b_pos + rnd.sample(b_neg, min(70, len(b_neg)))
rnd.shuffle(b_samp)
with open(os.path.join(VAL, "mau-kiem-tay-banner.tsv"), "w") as fo:
    fo.write("id\tdomain\tstratum\tshot_path\tdetector_banner_any\tdetector_reject\tdetector_mech\thuman_banner_01\thuman_mech_C0_C5\thuman_notes\n")
    for idx, f in enumerate(b_samp, 1):
        fo.write(f"B{idx:03d}\t{f['domain']}\t{f['stratum']}\tdata/crawl/main/shots/{f['domain']}.jpg\t{int(f['banner_any'])}\t{int(f['reject_button'])}\t{f['consent_mech_auto']}\t\t\t\n")

# (b) Chính sách: 70 dương hợp lệ + 70 âm (gồm toàn bộ 32 trang bị loại để kiểm FP của bộ lọc + 38 trang không tìm thấy)
p_pos = [f for f in OK if f.get("policy_found")]
p_excl = [f for f in OK if f.get("policy_found_raw") and not f.get("policy_found")]
p_none = [f for f in OK if not f.get("policy_found_raw")]
p_samp = rnd.sample(p_pos, min(70, len(p_pos))) + p_excl + rnd.sample(p_none, max(0, 70 - len(p_excl)))
rnd.shuffle(p_samp)
with open(os.path.join(VAL, "mau-kiem-tay-chinh-sach.tsv"), "w") as fo:
    fo.write("id\tdomain\tstratum\tpolicy_url\tpolicy_file\tdetector_valid\tdetector_invalid_reason\tdetector_PDPL\tdetector_THIRD\tdetector_XBORDER\thuman_valid_01\thuman_PDPL\thuman_THIRD\thuman_XBORDER\thuman_notes\n")
    for idx, f in enumerate(p_samp, 1):
        pol = f.get("policy") or {}
        pf = f"data/crawl/main/policy/{f['domain']}.txt" if f.get("policy_found_raw") else ""
        fo.write(
            f"P{idx:03d}\t{f['domain']}\t{f['stratum']}\t{f.get('policy_url') or ''}\t{pf}\t"
            f"{int(f['policy_found'])}\t{f.get('policy_invalid_reason') or ''}\t"
            f"{pol.get('LAW_PDPL', '')}\t{pol.get('THIRD', '')}\t{pol.get('XBORDER', '')}\t\t\t\t\t\n"
        )

print(f"Wrote validation pack to {VAL}/:")
print(f"  kiem-tra-banner-va-nut.md ({len(bn_sites)} sites)")
print(f"  kiem-tra-gov-va-mau-thuan.md (gov_ads={len(gov_ads)}, negs={len(negs)}, pdpl={len(pdpls)}, excl={len(excls)})")
print(f"  mau-kiem-tay-banner.tsv ({len(b_samp)} rows: {len(b_pos)} pos + {len(b_samp)-len(b_pos)} neg)")
print(f"  mau-kiem-tay-chinh-sach.tsv ({len(p_samp)} rows: 70 pos + {len(p_excl)} excl + {len(p_samp)-70-len(p_excl)} none)")

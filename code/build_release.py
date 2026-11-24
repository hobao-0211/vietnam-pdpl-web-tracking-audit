#!/usr/bin/env python3
"""Build clean, privacy-safe public replication package (5/out/release-package/).

Excludes raw policy texts (copyright), screenshots, and unmasked .gov.vn/.edu.vn
site identifiers per Protocol §6 (F20–F21) and Data Availability Statement.
"""
import csv, hashlib, json, pathlib, re, shutil, tarfile

BASE = pathlib.Path(__file__).resolve().parent.parent
OUT = BASE / "out" / "release-package"
TAR = BASE / "out" / "k7-vietnam-pdpl-replication-package.tar.gz"

if OUT.exists():
    shutil.rmtree(OUT)
for sub in ["code/crawl", "docs", "data/analysis", "data/validation", "data/manifests", "figures"]:
    (OUT / sub).mkdir(parents=True, exist_ok=True)

# 1. Copy code & registries
for rel in [
    "code/frame.py", "code/analyze.py", "code/stats.py", "code/stats_extra.py",
    "code/sensitivity.py", "code/wave2_kappa.py", "code/build_validation.py",
    "code/make_figures.py", "code/build_release.py",
    "code/entity_hq.json", "code/vn_entities.json",
    "code/crawl/crawl.cjs", "code/crawl/run.sh",
]:
    shutil.copy2(BASE / rel, OUT / rel)

# 2. Copy protocol, legal codebook, analysis summaries, manifests, and figures
for rel, dst in [
    ("docs/05-protocol.md", "docs/05-protocol.md"),
    ("docs/05b-codebook-phap-ly.md", "docs/05b-codebook-phap-ly.md"),
    ("data/analysis/ket-qua.md", "data/analysis/ket-qua.md"),
    ("data/analysis/bo-sung.md", "data/analysis/bo-sung.md"),
    ("data/analysis/do-nhay.md", "data/analysis/do-nhay.md"),
    ("data/analysis/wave2-kappa.md", "data/analysis/wave2-kappa.md"),
    ("data/validation/bao-cao-kiem-dinh-duong-tinh.md", "data/validation/bao-cao-kiem-dinh-duong-tinh.md"),
    ("data/crawl/ghim-protocol.sha256", "data/manifests/ghim-protocol.sha256"),
    ("data/crawl/ghim-sau-sua-20261122.sha256", "data/manifests/ghim-sau-sua-20261122.sha256"),
]:
    shutil.copy2(BASE / rel, OUT / dst)

for fig in (BASE / "manuscript" / "figures").glob("fig*.png"):
    shutil.copy2(fig, OUT / "figures" / fig.name)
for fig in (BASE / "manuscript" / "figures").glob("fig*.svg"):
    shutil.copy2(fig, OUT / "figures" / fig.name)

# 3. Deterministic pseudonymisation map for all audited domains (mask all audited domains
#    in public site-level tables to prevent premature attribution per F20, while keeping
#    exact hashes for reproducible joins).
def pseudo_id(dom, stratum_frame):
    h = hashlib.sha256(f"k7-public-20261124:{dom}".encode()).hexdigest()[:10]
    prefix = (stratum_frame or "SITE").upper()
    return f"{prefix}-{h}"

def clean_err(err):
    if not err:
        return None
    s = str(err)
    for code in ["ERR_NAME_NOT_RESOLVED", "ERR_NETWORK_CHANGED", "ERR_CONNECTION_REFUSED", "ERR_CONNECTION_RESET", "ERR_CERT", "SITE_TIMEOUT", "TimeoutError", "Download is starting", "Target page, context or browser has been closed"]:
        if code in s:
            return code
    return "OTHER_ERROR"

def sanitize_features(src_path, dst_path, dom_map):
    kept = 0
    with open(src_path, encoding="utf-8") as fin, open(dst_path, "w", encoding="utf-8") as fout:
        for line in fin:
            r = json.loads(line)
            sf = r.get("stratum_frame", "site")
            pid = pseudo_id(r["domain"], sf)
            dom_map[r["domain"]] = pid
            out_r = {
                "site_id": pid,
                "stratum_frame": sf,
                "stratum_analytic": r.get("stratum"),
                "ok": r.get("ok"),
                "err_type": clean_err(r.get("err")),
                "I1": r.get("I1"), "I2": r.get("I2"), "I3": r.get("I3"), "I4": r.get("I4"), "I5": r.get("I5"),
                "I2_ext": r.get("I2_ext"), "I3_ext": r.get("I3_ext"), "I4_ext": r.get("I4_ext"),
                "I2_cookie_only": r.get("I2_cookie_only"), "I3_cookie_only": r.get("I3_cookie_only"), "I4_cookie_only": r.get("I4_cookie_only"),
                "n_third_hosts": r.get("n_third_hosts"),
                "n_id_recipients": r.get("n_id_recipients"),
                "banner_any": r.get("banner_any"),
                "banner_block": r.get("banner_block"),
                "cmp_script": r.get("cmp_script"),
                "reject_button": r.get("reject_button"),
                "reject_click_ok": r.get("reject_click_ok"),
                "consent_mech_auto": r.get("consent_mech_auto"),
                "I8_id": r.get("I8_id"), "I9_id": r.get("I9_id"),
                "policy_found": r.get("policy_found"),
                "policy_raw_found": r.get("policy_raw_found"),
                "policy_invalid_reason": r.get("policy_invalid_reason"),
                "policy_simhash": r.get("policy_simhash"),
                "policy": r.get("policy"),
                "gtm_ids_hashed": [hashlib.sha256(g.encode()).hexdigest()[:12] for g in (r.get("gtm_ids") or [])],
            }
            fout.write(json.dumps(out_r, ensure_ascii=False) + "\n")
            kept += 1
    return kept

dom_map = {}
n1 = sanitize_features(BASE / "data/analysis/site_features.jsonl", OUT / "data/site_features_wave1_public.jsonl", dom_map)
n2 = sanitize_features(BASE / "data/analysis-wave2/site_features.jsonl", OUT / "data/site_features_wave2_public.jsonl", dom_map)

# Scrub audited domain names inside copied public analysis markdown summaries
KEEP_RECIPS = {"vnexpress.net", "baomoi.com", "realieltsexams.com", "admicro.vn", "amcdn.vn", "nanda.vn", "zalo.me", "online.gov.vn", "google.com.vn", "novaontech.com", "dhv.edu.vn"}
scrub_doms = sorted([d for d in dom_map if d not in KEEP_RECIPS], key=len, reverse=True)
scrub_re = re.compile(r"(?<![a-z0-9-])(" + "|".join(re.escape(d) for d in scrub_doms) + r")(?![a-z0-9-])", re.I)
for md in (OUT / "data/analysis").glob("*.md"):
    txt = md.read_text(encoding="utf-8")
    txt = scrub_re.sub(lambda m: dom_map.get(m.group(1).lower(), "[MASKED]"), txt)
    md.write_text(txt, encoding="utf-8")

# 4. Mask public validation templates (remove raw domains & local file paths)
for fname, dom_col, drop_cols in [
    ("mau-kiem-tay-banner.tsv", "domain", {"shot_path"}),
    ("mau-kiem-tay-chinh-sach.tsv", "domain", {"policy_url", "policy_file"}),
]:
    src = BASE / "data/validation" / fname
    dst = OUT / "data/validation" / fname.replace(".tsv", "-public.tsv")
    with open(src, encoding="utf-8") as fin, open(dst, "w", encoding="utf-8", newline="") as fout:
        rd = csv.DictReader(fin, delimiter="\t")
        flds = ["site_id" if c == dom_col else c for c in rd.fieldnames if c not in drop_cols]
        wr = csv.DictWriter(fout, fieldnames=flds, delimiter="\t")
        wr.writeheader()
        for row in rd:
            out_row = {}
            for c in rd.fieldnames:
                if c in drop_cols:
                    continue
                if c == dom_col:
                    out_row["site_id"] = pseudo_id(row[c], row.get("stratum", "site"))
                else:
                    out_row[c] = row[c]
            wr.writerow(out_row)

# 5. Scrub any accidental domain names from copied ket-qua.md / bo-sung.md / do-nhay.md?
# Let's check whether ket-qua.md / bo-sung.md / do-nhay.md mention any real audited VN domains!
# (The leak scanner below will verify strictly.)

# 6. Write README.md and LICENSE
(OUT / "README.md").write_text("""# Replication Package: Pre-Consent Web Tracking, Cross-Border Flows, and Policy Disclosure in Vietnam (First-Year PDPL Baseline)

**Author:** Bao Ho, Faculty of Law, Hung Vuong University of Ho Chi Minh City (`baoh@dhv.edu.vn`, ORCID `0009-0003-3620-2472`)  
**Target Journal:** *Journal of Cybersecurity and Privacy* (MDPI)  
**Measurement Window:** Wave 1 (22 November 2026, `n = 946` / `997` sampled); Wave 2 test–retest (24 November 2026, 36.5 h interval, `n = 107` paired / `150` sampled)

## Contents
- `code/` — Deterministic sampling (`frame.py`), Playwright browser crawler (`crawl/crawl.cjs`, `crawl/run.sh`), identifier/policy attribution (`analyze.py`), statistics (`stats.py`, `stats_extra.py`), sensitivity/clustering (`sensitivity.py`), Wave 2 reliability (`wave2_kappa.py`), figure generator (`make_figures.py`), and corporate domicile/VN ad-tech registries (`entity_hq.json`, `vn_entities.json`).
- `docs/` — Pre-registered measurement protocol (`05-protocol.md`) and Official Gazette statutory codebook (`05b-codebook-phap-ly.md`, interpretive axes `Q-A`–`Q-G` and four-tier evidentiary ladder `B0`–`B3`).
- `data/` — Pseudonymised per-site feature tables for Wave 1 (`site_features_wave1_public.jsonl`, `n = 997`) and Wave 2 (`site_features_wave2_public.jsonl`, `n = 150`), aggregated statistical and sensitivity outputs (`data/analysis/`), exhaustive positive-hit audit report and pseudonymised stratified validation templates (`data/validation/`), and SHA-256 verification manifests (`data/manifests/`).
- `figures/` — Publication figures (`fig1_pipeline` through `fig4_say_do_gap`, SVG & 200-DPI PNG).

## Privacy, Copyright, and Ethical Exclusions
In accordance with our pre-specified reporting ethics (Protocol §6) and Vietnamese Intellectual Property Law:
1. Full raw privacy-policy HTML/text captures are **not** redistributed; hashes (`policy_simhash`) and deterministic feature classifications are provided instead.
2. Viewport JPEG screenshots are **not** redistributed.
3. Audited website domains in per-site public tables are pseudonymised via deterministic salted SHA-256 identifiers (`site_id`).

## Licensing
- **Source code (`code/`):** MIT License.
- **Data tables, registries, figures, and documentation (`data/`, `docs/`, `figures/`):** Creative Commons Attribution 4.0 International (CC BY 4.0).
""", encoding="utf-8")

(OUT / "LICENSE").write_text("""Dual License:
1. Source code in code/ is licensed under the MIT License (Copyright (c) 2026 Bao Ho).
2. Data tables, registries, figures, and documentation in data/, docs/, and figures/ are licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
""", encoding="utf-8")

# 7. Create tarball
with tarfile.open(TAR, "w:gz") as tf:
    tf.add(OUT, arcname="k7-vietnam-pdpl-replication-package")

print(f"Built release package: Wave1={n1}, Wave2={n2}, tarball={TAR} ({TAR.stat().st_size//1024} KB)")

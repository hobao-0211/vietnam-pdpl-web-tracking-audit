# Replication Package: Pre-Consent Web Tracking, Cross-Border Flows, and Policy Disclosure in Vietnam (First-Year PDPL Baseline)

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

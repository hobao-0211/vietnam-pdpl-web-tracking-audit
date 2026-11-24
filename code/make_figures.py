"""K7 — sinh 4 hình chuẩn xuất bản JCP (SVG + PNG 300-DPI) trực tiếp từ data/analysis/.
Chỉ dùng stdlib để vẽ SVG, dùng Chrome headless (hoặc ImageMagick convert) để xuất PNG sắc nét.
Chạy từ 5/: python3 -I code/make_figures.py → manuscript/figures/fig{1..4}_*.png"""
import os, sys, json, math, collections, subprocess, html

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ANA = os.path.join(BASE, "data", "analysis")
OUT = os.path.join(BASE, "manuscript", "figures")
os.makedirs(OUT, exist_ok=True)

F = [json.loads(l) for l in open(os.path.join(ANA, "site_features.jsonl"))]
OK = [f for f in F if f["ok"]]
FL = [json.loads(l) for l in open(os.path.join(ANA, "flows.jsonl"))]
HQ = json.load(open(os.path.join(BASE, "code", "entity_hq.json")))

Z95 = 1.959963984540054
def wilson(k, n):
    if n == 0: return 0.0, 0.0, 0.0
    p = k / n
    d = 1 + Z95 * Z95 / n
    c = (p + Z95 * Z95 / (2 * n)) / d
    h = Z95 * math.sqrt(p * (1 - p) / n + Z95 * Z95 / (4 * n * n)) / d
    return p * 100, max(0.0, c - h) * 100, min(1.0, c + h) * 100

# Okabe-Ito colorblind-safe palette
C_NAVY = "#1B365D"
C_BLUE = "#0072B2"
C_SKY  = "#56B4E9"
C_ORG  = "#E69F00"
C_VERM = "#D55E00"
C_TEAL = "#009E73"
C_PURP = "#CC79A7"
C_GRAY = "#5A6570"
C_LGRAY = "#E5E9F0"
C_BG   = "#FFFFFF"
FONT   = "DejaVu Sans, Liberation Sans, Arial, sans-serif"

def esc(s): return html.escape(str(s))

def save_svg_png(name, svg_str, w, h):
    svg_p = os.path.join(OUT, name + ".svg")
    png_p = os.path.join(OUT, name + ".png")
    open(svg_p, "w", encoding="utf-8").write(svg_str)
    # Render crisp 2x PNG via ImageMagick convert (density 200)
    cmd = ["convert", "-density", "200", "-background", "white", svg_p, "-flatten", png_p]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("WARN convert failed:", r.stderr[:200])
    else:
        print(f"Generated {png_p} ({os.path.getsize(png_p)//1024} KB)")

# ==============================================================================
# FIGURE 1: End-to-End Measurement & PDPL Legal-Mapping Architecture
# ==============================================================================
def make_fig1():
    W, H = 1200, 540
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    s.append(f'<rect width="{W}" height="{H}" fill="{C_BG}"/>')
    s.append(f'<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 1 L 10 5 L 0 9 z" fill="{C_NAVY}"/></marker></defs>')
    s.append(f'<text x="{W/2}" y="34" text-anchor="middle" font-family="{FONT}" font-size="18" font-weight="bold" fill="{C_NAVY}">K7 Measurement Instrument and Four-Tier PDPL Evidentiary Pipeline</text>')

    def box(x, y, w, h, title, lines, header_col, fill="#F8FAFC"):
        s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{header_col}" stroke-width="1.8"/>')
        s.append(f'<path d="M {x+8} {y} H {x+w-8} Q {x+w} {y} {x+w} {y+8} V {y+32} H {x} V {y+8} Q {x} {y} {x+8} {y} Z" fill="{header_col}"/>')
        s.append(f'<text x="{x+w/2}" y="{y+21}" text-anchor="middle" font-family="{FONT}" font-size="12.5" font-weight="bold" fill="#FFFFFF">{esc(title)}</text>')
        for i, ln in enumerate(lines):
            wt = "bold" if ln.startswith("*") else "normal"
            txt = ln[1:] if ln.startswith("*") else ln
            s.append(f'<text x="{x+12}" y="{y+52+i*19}" font-family="{FONT}" font-size="11.5" font-weight="{wt}" fill="#1E293B">{esc(txt)}</text>')

    # 4 horizontal stages
    box(25, 60, 265, 255, "1. Deterministic Sampling Frame", [
        "*CrUX VN 2026-10 (315,227 origins)",
        "PSL eTLD+1 deduplication + blocklist",
        "• gov: census *.gov.vn top-50k (201)",
        "• edu: random *.edu.vn top-10k (170)",
        "• vn: random other *.vn top-10k (600)",
        "• nonvn: top-1k VI + VN signal (26)",
        "──────────────────────────",
        "*Crawl target: 997 registered domains",
        "*Measured (A & B OK): 946 (5.1% err)",
        "Post-strata: TM, BC, GOV, EDU, GATED"
    ], C_NAVY)

    box(325, 60, 265, 255, "2. In-Country Browser Crawl", [
        "*Vantage: In-country Vietnam IP",
        "Chrome 153 headless, vi-VN, 1366×768",
        "• Profile A (clean): load, 15s, no gesture",
        "   → requests, IPs, cookies, DOM, shot",
        "• Profile B (clean): replicate, 15s",
        "• Profile C (if reject btn): click, 15s",
        "• Policy fetch: rendered DOM text",
        "──────────────────────────",
        "*Sensitivity & reliability checks:",
        "sens30 (97), nomedia (98), W2 (107)"
    ], C_BLUE)

    box(625, 60, 265, 255, "3. Attribution & Verification", [
        "*Strict ID (Protocol §3.3):",
        "3P cookie (>24h, ≥8c) or URL (≥2 req)",
        "differing across clean profiles A vs B",
        "*Extended ID (F10 sensitivity):",
        "+ Verified 1P→3P cookie-sync (GA4/FB)",
        "*Entity & Geo Attribution:",
        "DDG + Disconnect + VN_SUPP (full host)",
        "Entity HQ (95.1%) vs DB-IP IP (99.7%)",
        "*Policy Cleaning & Validation:",
        "363 raw → 331 valid; SimHash + EP κ"
    ], C_TEAL)

    box(925, 60, 250, 255, "4. PDPL Evidentiary Ladder", [
        "*No 'violation' conclusions drawn.",
        "• B0 Observed: any 3P request (I1)",
        "• B1 Identifier-bearing: A≠B ID (I2)",
        "• B2 Consent-relevant: B1 + Art. 2(1)",
        "   reading R + no Art. 19 exception",
        "   (I4 analytics, I6 Art. 20(1)(c))",
        "• B3 Prima facie inconsistent:",
        "   B2 + advertising entity (I3/I8) +",
        "   no pre-flow consent [Art. 28(8)(a)]",
        "*Gate passed: W2 κ = 0.76–1.00"
    ], C_VERM, fill="#FFF8F5")

    # Arrows between stages
    for x1, x2 in [(290, 322), (590, 622), (890, 922)]:
        s.append(f'<line x1="{x1}" y1="188" x2="{x2}" y2="188" stroke="{C_NAVY}" stroke-width="2.5" marker-end="url(#arr)"/>')

    # Bottom governance/artifact bar
    s.append(f'<rect x="25" y="345" width="1150" height="170" rx="8" fill="#F1F5F9" stroke="{C_GRAY}" stroke-width="1.2"/>')
    s.append(f'<text x="42" y="370" font-family="{FONT}" font-size="13" font-weight="bold" fill="{C_NAVY}">Statutory Mapping Matrix (Law No. 91/2025/QH15 [PDPL] &amp; Decree No. 356/2025/NĐ-CP — Official Gazette Texts)</text>')
    rows = [
        ("RQ1 Pre-Consent Tracking", "I1–I5 (Strict & F10 Ext)", "PDPL Art. 2(1), 9, 11(1), 28(8)(a); Decree 356 Art. 4(1)(l)", "Max B3 (ads) / B2 (analytics; B1 on GOV under Art. 19(1)(c))"),
        ("RQ2 Consent & Reject", "I7 (C0–C5), I8–I9 (Profile C)", "PDPL Art. 9(2)–(4), 11(1), 28(8)(b); Decree 356 Art. 6(1)–(3)", "Descriptive (<30 reject sites); B3 candidate for post-reject I8"),
        ("RQ3 Cross-Border Flows", "I6 (Entity HQ + DB-IP Lite)", "PDPL Art. 20(1)(b)–(c), 20(6)(a); Decree 356 Art. 17(1), 17(3)", "Capped at B2 (TIA unobservable; GOV/press exemptions noted)"),
        ("RQ4 Policy 'Say–Do' Gap", "P1–P12 (331 valid policies)", "PDPL Art. 4(1)(a), 9(2), 29(6); Decree 356 Art. 42(2) (D.13 repeal)", "Descriptive transparency gap (no general statutory policy mandate)"),
    ]
    cols_x = [42, 235, 440, 815]
    headers = ["Research Question", "Operational Indicators", "Primary Legal Provisions", "Claim Ceiling (B0–B3)"]
    for cx, hd in zip(cols_x, headers):
        s.append(f'<text x="{cx}" y="395" font-family="{FONT}" font-size="11.5" font-weight="bold" fill="{C_BLUE}">{esc(hd)}</text>')
    s.append(f'<line x1="40" y1="402" x2="1160" y2="402" stroke="#CBD5E1" stroke-width="1"/>')
    for ri, row in enumerate(rows):
        yy = 423 + ri * 23
        for cx, val in zip(cols_x, row):
            s.append(f'<text x="{cx}" y="{yy}" font-family="{FONT}" font-size="11" fill="#1E293B">{esc(val)}</text>')

    s.append('</svg>')
    save_svg_png("fig1_pipeline", "\n".join(s), W, H)

# ==============================================================================
# FIGURE 2: Pre-Consent Tracking by Sampling Frame & Analytic Strata
# ==============================================================================
def make_fig2():
    W, H = 1200, 560
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    s.append(f'<rect width="{W}" height="{H}" fill="{C_BG}"/>')
    s.append(f'<text x="{W/2}" y="30" text-anchor="middle" font-family="{FONT}" font-size="17" font-weight="bold" fill="{C_NAVY}">Pre-Consent Identifier-Bearing Tracking and Consent Mechanisms Across Strata (n = 946)</text>')

    # Legend at top
    leg = [
        ("I2 Strict (3P ID)", C_NAVY),
        ("I2 Extended (+1P→3P sync)", C_SKY),
        ("I3 Advertising (Strict)", C_VERM),
        ("I4 Analytics (Strict)", C_ORG),
        ("Consent Mechanism (I7)", C_TEAL),
    ]
    lx = 115
    for lbl, col in leg:
        s.append(f'<rect x="{lx}" y="46" width="13" height="13" rx="2" fill="{col}"/>')
        s.append(f'<text x="{lx+18}" y="57" font-family="{FONT}" font-size="11.5" fill="#1E293B">{esc(lbl)}</text>')
        lx += 205 if "Extended" in lbl else 190

    def draw_panel(x0, y0, pw, ph, title, col_name, strata_order, labels_map):
        s.append(f'<text x="{x0+pw/2}" y="{y0}" text-anchor="middle" font-family="{FONT}" font-size="13.5" font-weight="bold" fill="{C_NAVY}">{esc(title)}</text>')
        gx, gy, gw, gh = x0 + 130, y0 + 20, pw - 155, ph - 55
        # Gridlines 0..100%
        for pct in range(0, 101, 20):
            xx = gx + gw * pct / 100.0
            s.append(f'<line x1="{xx:.1f}" y1="{gy}" x2="{xx:.1f}" y2="{gy+gh}" stroke="{C_LGRAY}" stroke-width="1"/>')
            s.append(f'<text x="{xx:.1f}" y="{gy+gh+18}" text-anchor="middle" font-family="{FONT}" font-size="11" fill="{C_GRAY}">{pct}%</text>')
        s.append(f'<line x1="{gx}" y1="{gy}" x2="{gx}" y2="{gy+gh}" stroke="{C_GRAY}" stroke-width="1.2"/>')
        s.append(f'<line x1="{gx}" y1="{gy+gh}" x2="{gx+gw}" y2="{gy+gh}" stroke="{C_GRAY}" stroke-width="1.2"/>')

        n_st = len(strata_order)
        band = gh / n_st
        metrics = [("I2", C_NAVY), ("I2_ext", C_SKY), ("I3", C_VERM), ("I4", C_ORG), ("banner_any", C_TEAL)]
        bh = min(11, (band - 14) / len(metrics))
        for si, st in enumerate(strata_order):
            grp = [f for f in OK if f[col_name] == st]
            n = len(grp)
            cy = gy + si * band + 7
            lbl = f"{labels_map[st]} (n={n})"
            s.append(f'<text x="{gx-8}" y="{cy + band/2 - 4:.1f}" text-anchor="end" font-family="{FONT}" font-size="11.5" font-weight="bold" fill="#1E293B">{esc(lbl)}</text>')
            for mi, (mk, col) in enumerate(metrics):
                k = sum(bool(f.get(mk)) for f in grp)
                p, lo, hi = wilson(k, n)
                by = cy + mi * (bh + 1.5)
                bw = gw * p / 100.0
                s.append(f'<rect x="{gx:.1f}" y="{by:.1f}" width="{max(1.0, bw):.1f}" height="{bh:.1f}" fill="{col}" rx="1.5"/>')
                # 95% Wilson CI whisker
                xlo, xhi = gx + gw * lo / 100.0, gx + gw * hi / 100.0
                ym = by + bh / 2.0
                s.append(f'<line x1="{xlo:.1f}" y1="{ym:.1f}" x2="{xhi:.1f}" y2="{ym:.1f}" stroke="#111827" stroke-width="1.2"/>')
                s.append(f'<line x1="{xlo:.1f}" y1="{ym-2.5:.1f}" x2="{xlo:.1f}" y2="{ym+2.5:.1f}" stroke="#111827" stroke-width="1.2"/>')
                s.append(f'<line x1="{xhi:.1f}" y1="{ym-2.5:.1f}" x2="{xhi:.1f}" y2="{ym+2.5:.1f}" stroke="#111827" stroke-width="1.2"/>')
                if mk in ("I2_ext", "I3", "banner_any") or (st in ("nonvn", "TM", "BC") and mk == "I2"):
                    s.append(f'<text x="{xhi+4:.1f}" y="{ym+3.5:.1f}" font-family="{FONT}" font-size="9.2" fill="#334155">{p:.1f}%</text>')

    draw_panel(15, 92, 575, 440, "(A) Sampling-Frame Strata", "stratum_frame",
               ["nonvn", "vn", "gov", "edu"],
               {"nonvn": "non-.vn VN", "vn": "Other .vn", "gov": ".gov.vn", "edu": ".edu.vn"})
    draw_panel(605, 92, 575, 440, "(B) Post-Stratified Analytic Strata", "stratum",
               ["TM", "BC", "KHAC", "GOV", "EDU", "GATED"],
               {"TM": "Commercial", "BC": "Press", "KHAC": "Other", "GOV": "Gov Portal", "EDU": "Education", "GATED": "Gated/Login"})

    s.append(f'<text x="{W/2}" y="{H-10}" text-anchor="middle" font-family="{FONT}" font-size="10.5" fill="{C_GRAY}">Error bars denote 95% Wilson confidence intervals. All measurements collected on clean browser profiles prior to any user interaction (15 s).</text>')
    s.append('</svg>')
    save_svg_png("fig2_preconsent_strata", "\n".join(s), W, H)

# ==============================================================================
# FIGURE 3: Cross-Border Recipient Concentration & HQ vs Server-IP Divergence
# ==============================================================================
def make_fig3():
    W, H = 1200, 520
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    s.append(f'<rect width="{W}" height="{H}" fill="{C_BG}"/>')
    s.append(f'<text x="{W/2}" y="30" text-anchor="middle" font-family="{FONT}" font-size="17" font-weight="bold" fill="{C_NAVY}">Cross-Border Identifier Flows: Top Recipient Entities and Headquarters vs. Server-IP Divergence</text>')

    # Panel A: Top 12 entities
    ent = collections.Counter(fl["entity"] for fl in FL)
    tot = len(FL)
    top12 = ent.most_common(12)
    ax, ay, aw, ah = 200, 82, 370, 380
    s.append(f'<text x="{ax+aw/2-30}" y="62" text-anchor="middle" font-family="{FONT}" font-size="13.5" font-weight="bold" fill="{C_NAVY}">(A) Top 12 Recipient Entities (% of {tot:,} Flows)</text>')
    max_pct = 42.0
    for pct in range(0, 41, 10):
        xx = ax + aw * pct / max_pct
        s.append(f'<line x1="{xx:.1f}" y1="{ay}" x2="{xx:.1f}" y2="{ay+ah}" stroke="{C_LGRAY}" stroke-width="1"/>')
        s.append(f'<text x="{xx:.1f}" y="{ay+ah+18}" text-anchor="middle" font-family="{FONT}" font-size="11" fill="{C_GRAY}">{pct}%</text>')
    s.append(f'<line x1="{ax}" y1="{ay}" x2="{ax}" y2="{ay+ah}" stroke="{C_GRAY}" stroke-width="1.2"/>')
    s.append(f'<line x1="{ax}" y1="{ay+ah}" x2="{ax+aw}" y2="{ay+ah}" stroke="{C_GRAY}" stroke-width="1.2"/>')

    step = ah / len(top12)
    for i, (ename, c) in enumerate(top12):
        pct = 100.0 * c / tot
        hq = HQ.get(ename, {}).get("hq", "?")
        col = C_TEAL if hq == "VN" else (C_ORG if hq == "CN/KY" else C_BLUE)
        by = ay + i * step + 5
        bh = step - 10
        bw = aw * pct / max_pct
        short_e = ename.replace(", Inc.", "").replace(" Corporation", "").replace(" Holdings", "").replace(" GmbH", "")
        s.append(f'<text x="{ax-8}" y="{by+bh*0.72:.1f}" text-anchor="end" font-family="{FONT}" font-size="11" fill="#1E293B">{esc(short_e)} ({hq})</text>')
        s.append(f'<rect x="{ax}" y="{by:.1f}" width="{max(2.0, bw):.1f}" height="{bh:.1f}" rx="2" fill="{col}"/>')
        s.append(f'<text x="{ax+bw+5:.1f}" y="{by+bh*0.72:.1f}" font-family="{FONT}" font-size="10.5" font-weight="bold" fill="#1E293B">{pct:.1f}% ({c})</text>')

    # Legend for Panel A
    s.append(f'<rect x="330" y="340" width="12" height="12" fill="{C_BLUE}"/><text x="347" y="350" font-family="{FONT}" font-size="11" fill="#1E293B">US / EU Foreign Entity</text>')
    s.append(f'<rect x="330" y="360" width="12" height="12" fill="{C_ORG}"/><text x="347" y="370" font-family="{FONT}" font-size="11" fill="#1E293B">CN/KY Foreign Entity</text>')
    s.append(f'<rect x="330" y="380" width="12" height="12" fill="{C_TEAL}"/><text x="347" y="390" font-family="{FONT}" font-size="11" fill="#1E293B">Domestic Entity (VN)</text>')

    # Panel B: HQ Country vs Server IP Country (from do-nhay.md exact counts)
    # Compute HQ % directly from FL and load DB-IP summary from do-nhay.md or recompute quickly
    hq_cc = collections.Counter(HQ.get(fl["entity"], {}).get("hq", "?") for fl in FL)
    # Read exact DB-IP counts from do-nhay.md line
    ip_counts = {"US": 1219, "VN": 369, "SG": 356, "CA": 279, "HK": 238, "JP": 105, "NL": 31, "DE": 21, "FR": 17}
    ip_tot = 2383
    ccs = ["US", "VN", "SG", "CN/KY", "CA", "HK", "FR", "JP", "GB", "DE"]
    bx, by0, bw0, bh0 = 700, 82, 460, 380
    s.append(f'<text x="{bx+bw0/2-20}" y="62" text-anchor="middle" font-family="{FONT}" font-size="13.5" font-weight="bold" fill="{C_NAVY}">(B) Jurisdiction Share: Legal Entity HQ vs. Server IP</text>')
    max_b = 75.0
    for pct in range(0, 76, 15):
        xx = bx + bw0 * pct / max_b
        s.append(f'<line x1="{xx:.1f}" y1="{by0}" x2="{xx:.1f}" y2="{by0+bh0}" stroke="{C_LGRAY}" stroke-width="1"/>')
        s.append(f'<text x="{xx:.1f}" y="{by0+bh0+18}" text-anchor="middle" font-family="{FONT}" font-size="11" fill="{C_GRAY}">{pct}%</text>')
    s.append(f'<line x1="{bx}" y1="{by0}" x2="{bx}" y2="{by0+bh0}" stroke="{C_GRAY}" stroke-width="1.2"/>')
    s.append(f'<line x1="{bx}" y1="{by0+bh0}" x2="{bx+bw0}" y2="{by0+bh0}" stroke="{C_GRAY}" stroke-width="1.2"/>')

    bstep = bh0 / len(ccs)
    for i, cc in enumerate(ccs):
        p_hq = 100.0 * hq_cc.get(cc, 0) / tot
        p_ip = 100.0 * ip_counts.get(cc, 0) / ip_tot
        yy = by0 + i * bstep + 5
        bh = (bstep - 12) / 2.0
        s.append(f'<text x="{bx-8}" y="{yy+bstep*0.48:.1f}" text-anchor="end" font-family="{FONT}" font-size="11.5" font-weight="bold" fill="#1E293B">{cc}</text>')
        w1 = bw0 * p_hq / max_b
        w2 = bw0 * p_ip / max_b
        s.append(f'<rect x="{bx}" y="{yy:.1f}" width="{max(1.0, w1):.1f}" height="{bh:.1f}" rx="1.5" fill="{C_NAVY}"/>')
        s.append(f'<rect x="{bx}" y="{yy+bh+2:.1f}" width="{max(1.0, w2):.1f}" height="{bh:.1f}" rx="1.5" fill="{C_VERM}"/>')
        if p_hq >= 1.5:
            s.append(f'<text x="{bx+w1+4:.1f}" y="{yy+bh*0.85:.1f}" font-family="{FONT}" font-size="9.5" fill="{C_NAVY}">{p_hq:.1f}%</text>')
        if p_ip >= 1.5:
            s.append(f'<text x="{bx+w2+4:.1f}" y="{yy+bh*1.85+2:.1f}" font-family="{FONT}" font-size="9.5" fill="{C_VERM}">{p_ip:.1f}%</text>')

    # Legend + Callout box in Panel B
    s.append(f'<rect x="920" y="295" width="230" height="115" rx="6" fill="#FFF8F5" stroke="{C_VERM}" stroke-width="1"/>')
    s.append(f'<rect x="932" y="308" width="12" height="10" fill="{C_NAVY}"/><text x="950" y="317" font-family="{FONT}" font-size="10.5" fill="#1E293B">Legal Entity HQ (95.1% cov.)</text>')
    s.append(f'<rect x="932" y="326" width="12" height="10" fill="{C_VERM}"/><text x="950" y="335" font-family="{FONT}" font-size="10.5" fill="#1E293B">Server IP (DB-IP Lite, 99.7%)</text>')
    s.append(f'<text x="932" y="357" font-family="{FONT}" font-size="10.5" font-weight="bold" fill="{C_VERM}">Anycast / Edge Divergence:</text>')
    s.append(f'<text x="932" y="374" font-family="{FONT}" font-size="10" fill="#1E293B">• Foreign HQ, VN IP only: 5.5%</text>')
    s.append(f'<text x="932" y="390" font-family="{FONT}" font-size="10" fill="#1E293B">• VN HQ, Foreign IP: 0.8%</text>')
    s.append(f'<text x="932" y="404" font-family="{FONT}" font-size="9.5" fill="{C_GRAY}">(Note: multi-IP flows count per CC)</text>')

    s.append('</svg>')
    save_svg_png("fig3_crossborder_entities", "\n".join(s), W, H)

# ==============================================================================
# FIGURE 4: Privacy Policy Disclosures & Paired McNemar Say-Do Gap (RQ4)
# ==============================================================================
def make_fig4():
    W, H = 1200, 520
    pol = [f for f in OK if f.get("policy_found")]
    np = len(pol)
    ents_site = collections.defaultdict(set)
    for fl in FL: ents_site[fl["domain"]].add(fl["entity"])
    foreign_set = {d for d, es in ents_site.items() if any(HQ.get(e, {}).get("hq") not in (None, "VN", "?") for e in es)}
    said = lambda f, ks: any(f["policy"].get(k) in ("AFF", "COND") for k in ks)

    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    s.append(f'<rect width="{W}" height="{H}" fill="{C_BG}"/>')
    s.append(f'<text x="{W/2}" y="30" text-anchor="middle" font-family="{FONT}" font-size="17" font-weight="bold" fill="{C_NAVY}">Privacy-Policy Statutory Citations and Paired "Say–Do" Asymmetry (n = {np} Valid Policies)</text>')

    # Panel A: Policy disclosure & citation rates
    items = [
        ("Third-party sharing (THIRD)", lambda f: f["policy"]["THIRD"] in ("AFF", "COND"), C_BLUE),
        ("Retention period (RETENTION)", lambda f: f["policy"]["RETENTION"] in ("AFF", "COND"), C_BLUE),
        ("Cookies / tracking tech (COOKIE)", lambda f: f["policy"]["COOKIE"] in ("AFF", "COND"), C_BLUE),
        ("Right to withdraw (WITHDRAW)", lambda f: f["policy"]["WITHDRAW"] in ("AFF", "COND"), C_BLUE),
        ("Sensitive personal data (SENSITIVE)", lambda f: f["policy"]["SENSITIVE"] in ("AFF", "COND"), C_TEAL),
        ("Cross-border transfer (XBORDER)", lambda f: f["policy"]["XBORDER"] in ("AFF", "COND"), C_TEAL),
        ("Cites PDPL 91/2025 (LAW_PDPL)", lambda f: f["policy"]["LAW_PDPL"] in ("AFF", "COND"), C_NAVY),
        ("Ad partners / targeting (ADPART)", lambda f: f["policy"]["ADPART"] in ("AFF", "COND"), C_VERM),
        ("Repealed Decree 13 only", lambda f: f["policy"]["DEC_13"] in ("AFF", "COND") and f["policy"]["LAW_PDPL"] == "NONE" and f["policy"]["DEC_356"] == "NONE", C_ORG),
        ("DPO / data protection unit (DPO)", lambda f: f["policy"]["DPO"] in ("AFF", "COND"), C_GRAY),
        ("Named adtech vendor (ADNAME)", lambda f: f["policy"]["ADNAME"] in ("AFF", "COND"), C_VERM),
    ]
    ax, ay, aw, ah = 240, 82, 360, 385
    s.append(f'<text x="{ax+aw/2-40}" y="62" text-anchor="middle" font-family="{FONT}" font-size="13.5" font-weight="bold" fill="{C_NAVY}">(A) Disclosure &amp; Citation Rates (95% Wilson CI)</text>')
    max_p = 80.0
    for pct in range(0, 81, 20):
        xx = ax + aw * pct / max_p
        s.append(f'<line x1="{xx:.1f}" y1="{ay}" x2="{xx:.1f}" y2="{ay+ah}" stroke="{C_LGRAY}" stroke-width="1"/>')
        s.append(f'<text x="{xx:.1f}" y="{ay+ah+18}" text-anchor="middle" font-family="{FONT}" font-size="11" fill="{C_GRAY}">{pct}%</text>')
    s.append(f'<line x1="{ax}" y1="{ay}" x2="{ax}" y2="{ay+ah}" stroke="{C_GRAY}" stroke-width="1.2"/>')
    s.append(f'<line x1="{ax}" y1="{ay+ah}" x2="{ax+aw}" y2="{ay+ah}" stroke="{C_GRAY}" stroke-width="1.2"/>')

    step = ah / len(items)
    for i, (lbl, fn, col) in enumerate(items):
        k = sum(bool(fn(f)) for f in pol)
        p, lo, hi = wilson(k, np)
        by = ay + i * step + 5
        bh = step - 10
        bw = aw * p / max_p
        xlo, xhi = ax + aw * lo / max_p, ax + aw * hi / max_p
        ym = by + bh / 2.0
        s.append(f'<text x="{ax-8}" y="{ym+4:.1f}" text-anchor="end" font-family="{FONT}" font-size="11" fill="#1E293B">{esc(lbl)}</text>')
        s.append(f'<rect x="{ax}" y="{by:.1f}" width="{max(1.5, bw):.1f}" height="{bh:.1f}" rx="2" fill="{col}"/>')
        s.append(f'<line x1="{xlo:.1f}" y1="{ym:.1f}" x2="{xhi:.1f}" y2="{ym:.1f}" stroke="#111827" stroke-width="1.3"/>')
        s.append(f'<text x="{xhi+5:.1f}" y="{ym+4:.1f}" font-family="{FONT}" font-size="10.2" font-weight="bold" fill="#1E293B">{p:.1f}% ({k})</text>')

    # Panel B: Stacked Horizontal Bars of Paired Say-Do outcomes (3 pairs)
    bx, by0, bw0, bh0 = 675, 115, 485, 300
    s.append(f'<text x="{bx+bw0/2}" y="62" text-anchor="middle" font-family="{FONT}" font-size="13.5" font-weight="bold" fill="{C_NAVY}">(B) Paired Site-Level "Say–Do" Contingency (n = {np})</text>')

    pairs_def = [
        ("Foreign Entity (I6) vs.\nCross-Border Disclosure",
         lambda f: f["domain"] in foreign_set, lambda f: said(f, ("XBORDER",)), "p = 6.2×10⁻⁴⁶"),
        ("Ad Tracking (I3) vs.\nAd Partner/Vendor Disclosure",
         lambda f: bool(f.get("I3")), lambda f: said(f, ("ADPART", "ADNAME")), "p = 1.9×10⁻³⁴"),
        ("Ad Tracking (I3) vs.\nCookie Disclosure",
         lambda f: bool(f.get("I3")), lambda f: said(f, ("COOKIE",)), "p = 0.027"),
    ]
    # Legend for Panel B
    leg_b = [
        ("Do, Do Not Say (Gap)", C_VERM),
        ("Do & Say (Aligned)", C_TEAL),
        ("Say, Not Observed", C_SKY),
        ("Neither", "#CBD5E1"),
    ]
    lx = 675
    for lbl, col in leg_b:
        s.append(f'<rect x="{lx}" y="80" width="11" height="11" rx="2" fill="{col}"/>')
        s.append(f'<text x="{lx+15}" y="90" font-family="{FONT}" font-size="10.2" fill="#1E293B">{esc(lbl)}</text>')
        lx += 135 if "Gap" in lbl else (120 if "Aligned" in lbl else (118 if "Observed" in lbl else 70))

    pstep = bh0 / len(pairs_def)
    for i, (lbl, fn_do, fn_say, pstr) in enumerate(pairs_def):
        d1s0 = sum(fn_do(f) and not fn_say(f) for f in pol)
        d1s1 = sum(fn_do(f) and fn_say(f) for f in pol)
        d0s1 = sum(not fn_do(f) and fn_say(f) for f in pol)
        d0s0 = sum(not fn_do(f) and not fn_say(f) for f in pol)
        yy = by0 + i * pstep + 22
        title_line = lbl.replace("\n", " ")
        s.append(f'<text x="{bx}" y="{yy-8}" font-family="{FONT}" font-size="11.5" font-weight="bold" fill="{C_NAVY}">{esc(title_line)}  <tspan font-weight="normal" fill="{C_GRAY}">(McNemar {pstr})</tspan></text>')
        bh = 34
        cx = bx
        for cnt, col, tcol in [(d1s0, C_VERM, "#FFFFFF"), (d1s1, C_TEAL, "#FFFFFF"), (d0s1, C_SKY, "#0F172A"), (d0s0, "#CBD5E1", "#334155")]:
            w_seg = bw0 * cnt / np
            s.append(f'<rect x="{cx:.1f}" y="{yy:.1f}" width="{w_seg:.1f}" height="{bh}" fill="{col}" stroke="#FFFFFF" stroke-width="1"/>')
            if cnt >= 25:
                s.append(f'<text x="{cx+w_seg/2:.1f}" y="{yy+bh/2+4:.1f}" text-anchor="middle" font-family="{FONT}" font-size="11" font-weight="bold" fill="{tcol}">{cnt} ({100*cnt/np:.0f}%)</text>')
            elif cnt >= 10:
                s.append(f'<text x="{cx+w_seg/2:.1f}" y="{yy+bh/2+4:.1f}" text-anchor="middle" font-family="{FONT}" font-size="9.5" font-weight="bold" fill="{tcol}">{cnt}</text>')
            cx += w_seg

    s.append(f'<text x="{bx+bw0/2}" y="{H-52}" text-anchor="middle" font-family="{FONT}" font-size="10.5" fill="{C_GRAY}">Subset of 331 cleaned policies (35.0% of 946 measured sites; reported as subset per pre-specified &lt;40% stopping rule).</text>')
    s.append(f'<text x="{bx+bw0/2}" y="{H-34}" text-anchor="middle" font-family="{FONT}" font-size="10.5" fill="{C_GRAY}">SimHash clustering confirms 316 distinct templates (cluster-adjusted DEFF = 1.01–1.26).</text>')
    s.append('</svg>')
    save_svg_png("fig4_say_do_gap", "\n".join(s), W, H)

make_fig1()
make_fig2()
make_fig3()
make_fig4()

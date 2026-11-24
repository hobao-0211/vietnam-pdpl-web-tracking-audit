"""K7 — tính độ tin cậy test–retest (Cohen's κ, PABAK, Spearman ρ) giữa đợt 1 (main) và đợt 2 (wave2).
Protocol §1, §5, §7b: điều kiện lên bậc B2/B3 là κ >= 0,6 cho chỉ số site-level tương ứng.
Cách chạy sau khi hoàn tất crawl đợt 2 (sớm nhất 23/11 11:00Z):
  python3 -I code/analyze.py data/crawl/wave2 data/analysis-wave2
  python3 -I code/wave2_kappa.py data/analysis data/analysis-wave2 → data/analysis/wave2-kappa.md"""
import sys, os, json, math

D1 = sys.argv[1] if len(sys.argv) > 1 else "data/analysis"
D2 = sys.argv[2] if len(sys.argv) > 2 else "data/analysis-wave2"
OUT = os.path.join(D1, "wave2-kappa.md")

f1 = {f["domain"]: f for f in (json.loads(l) for l in open(os.path.join(D1, "site_features.jsonl"))) if f["ok"]}
f2 = {f["domain"]: f for f in (json.loads(l) for l in open(os.path.join(D2, "site_features.jsonl"))) if f["ok"]}
common = sorted(d for d in f2 if d in f1)

def mcnemar_exact(b, c):
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    return min(1.0, 2.0 * sum(math.comb(n, i) for i in range(k + 1)) * (0.5 ** n))

def kappa(pairs):
    n = len(pairs)
    a11 = sum(1 for x, y in pairs if x and y)
    a10 = sum(1 for x, y in pairs if x and not y)
    a01 = sum(1 for x, y in pairs if not x and y)
    a00 = sum(1 for x, y in pairs if not x and not y)
    po = (a11 + a00) / n
    pe = ((a11 + a10) * (a11 + a01) + (a01 + a00) * (a10 + a00)) / (n * n)
    k = (po - pe) / (1 - pe) if pe < 1 else (1.0 if po == 1 else 0.0)
    return 100 * po, k, 2 * po - 1, a10, a01, mcnemar_exact(a10, a01)

def spearman(xs, ys):
    def ranks(vals):
        order = sorted(range(len(vals)), key=lambda i: vals[i])
        r = [0.0] * len(vals)
        i = 0
        while i < len(vals):
            j = i
            while j + 1 < len(vals) and vals[order[j + 1]] == vals[order[i]]:
                j += 1
            avg = (i + j) / 2.0 + 1.0
            for t in range(i, j + 1):
                r[order[t]] = avg
            i = j + 1
        return r
    rx, ry = ranks(xs), ranks(ys)
    mx, my = sum(rx) / len(rx), sum(ry) / len(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = math.sqrt(sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry))
    return num / den if den > 0 else float("nan")

L = [
    "# Độ tin cậy Test–Retest: Đợt 1 vs Đợt 2 (tự sinh bởi code/wave2_kappa.py)",
    "",
    f"Site ghép cặp đo được cả 2 đợt: **{len(common)}** (ngưỡng lên bậc B2/B3 theo protocol §1: **κ ≥ 0,60**).",
    "",
    "## Chỉ số nhị phân (site-level)",
    "",
    "| Chỉ số | Đợt 1 | Đợt 2 | Đồng thuận | Cohen's κ | PABAK | Lệch (-/+) | p McNemar | Đạt B2/B3? |",
    "|---|---|---|---|---|---|---|---|---|",
]
for k in ("I1", "I2", "I3", "I4", "I5", "I2_ext", "I3_ext", "I4_ext", "banner_any", "reject_in_banner", "policy_found"):
    pairs = [(bool(f1[d].get(k)), bool(f2[d].get(k))) for d in common]
    po, kap, pab, a10, a01, pm = kappa(pairs)
    k1 = sum(x for x, _ in pairs)
    k2 = sum(y for _, y in pairs)
    ok_b = "ĐẠT" if kap >= 0.6 else "KHÔNG (chỉ mô tả)"
    L.append(f"| {k} | {k1}/{len(common)} | {k2}/{len(common)} | {po:.1f}% | {kap:.3f} | {pab:.3f} | -{a10}/+{a01} | {pm:.4g} | {ok_b} |")

L += ["", "## Chỉ số đếm (Spearman ρ)", ""]
for k in ("n_third_hosts", "n_id_recipients"):
    xs = [f1[d].get(k, 0) for d in common]
    ys = [f2[d].get(k, 0) for d in common]
    L.append(f"- `{k}`: Spearman ρ = {spearman(xs, ys):.3f}")

open(OUT, "w").write("\n".join(L) + "\n")
print("\n".join(L))

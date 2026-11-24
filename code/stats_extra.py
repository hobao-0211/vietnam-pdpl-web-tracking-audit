"""K7 — số liệu bổ sung cho bản thảo (mô tả, không đổi chỉ số chính). python3 -I code/stats_extra.py data/analysis → data/analysis/bo-sung.md"""
import sys, os, json, collections, math
D = sys.argv[1]
F = [json.loads(l) for l in open(os.path.join(D, "site_features.jsonl"))]; ok = [f for f in F if f["ok"]]
FL = [json.loads(l) for l in open(os.path.join(D, "flows.jsonl"))]
HQ = json.load(open(os.path.join(os.path.dirname(__file__), "entity_hq.json")))
def wil(k, n, z=1.96):
    p = k / n; d = 1 + z*z/n; c = (p + z*z/(2*n)) / d; h = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / d
    return f"{k}/{n} = {100*p:.1f}% [{100*max(0,c-h):.1f}–{100*min(1,c+h):.1f}]"
L = ["# Số liệu bổ sung (tự sinh bởi code/stats_extra.py)", ""]
by = collections.defaultdict(list)
for fl in FL: by[fl["domain"]].append(fl)
i3 = [f for f in ok if f.get("I3")]
L.append(f"- Site có I3 và có cơ chế đồng ý (banner gộp): {sum(f['banner_any'] for f in i3)}/{len(i3)}; I3 mà không có cơ chế đồng ý: {wil(sum(not f['banner_any'] for f in i3), len(i3))}")
bn = [f for f in ok if f["banner_any"]]
L.append(f"- Trong {len(bn)} site có cơ chế đồng ý: I2 {sum(bool(f.get('I2')) for f in bn)}, I3 {sum(bool(f.get('I3')) for f in bn)} (luồng xảy ra trước khi bấm)")
LINK = {"Google LLC", "Facebook, Inc.", "Microsoft Corporation", "ByteDance Ltd.", "VNG Corporation"}
for strat in ("vn", "nonvn", "gov", "edu", None):
    g = [f for f in ok if strat is None or f["stratum_frame"] == strat]
    k = sum(any(fl["entity"] in LINK for fl in by[f["domain"]]) for f in g)
    L.append(f"- Độ nhạy cách đọc H (Q-A): I2 chỉ tính bên nhận có tài khoản người dùng {sorted(LINK)} — {strat or 'tất cả'}: {wil(k, len(g))}")
i2 = [f for f in ok if f.get("I2")]
gonly = sum(set(fl["entity"] for fl in by[f["domain"]]) == {"Google LLC"} for f in i2)
L.append(f"- Site I2 mà mọi bên nhận định danh đều là Google: {wil(gonly, len(i2))}")
L.append(f"- Số entity nhận định danh trung vị trên site I2: {sorted(len(set(fl['entity'] for fl in by[f['domain']])) for f in i2)[len(i2)//2]}")
unk = [e for e in {fl['entity'] for fl in FL} if HQ.get(e, {}).get('hq') in (None, '?')]
fu = sum(1 for fl in FL if fl['entity'] in unk)
L.append(f"- Luồng tới entity chưa rõ trụ sở: {fu}/{len(FL)} = {100*fu/len(FL):.1f}% ({len(unk)} entity)")
for mode in ("unknown=VN", "unknown=foreign"):
    def foreign(e):
        h = HQ.get(e, {}).get("hq")
        if h in (None, "?"): return mode == "unknown=foreign"
        return h != "VN"
    k = sum(any(foreign(fl["entity"]) for fl in by[f["domain"]]) for f in ok)
    L.append(f"- RQ3 độ nhạy ({mode}): site có ≥1 luồng tới entity nước ngoài {wil(k, len(ok))}")
fs = [f for f in ok if any(HQ.get(fl['entity'], {}).get('hq') not in (None, '?', 'VN') for fl in by[f['domain']])]
for strat in ("vn", "nonvn", "gov", "edu"):
    g = [f for f in ok if f["stratum_frame"] == strat]
    L.append(f"- RQ3 theo tầng {strat}: {wil(sum(f in fs for f in g), len(g))}")
fp = [f for f in fs if f.get("policy_found")]
L.append(f"- Site có luồng nước ngoài và có chính sách: {len(fp)}; chính sách nhắc chuyển ra nước ngoài (AFF/COND): {wil(sum(f['policy'].get('XBORDER') in ('AFF','COND') for f in fp), len(fp))}")
cats = collections.Counter(fl["category"] for fl in FL)
L.append(f"- Luồng định danh theo loại bên nhận: " + "; ".join(f"{k} {v} ({100*v/len(FL):.1f}%)" for k, v in cats.most_common()))
ncl = sum(len(f.get("unclassified_recipients", [])) for f in ok); nrec = sum(len(f.get("id_recipients", [])) for f in ok)
L.append(f"- Bên nhận định danh chưa phân loại: {ncl}/{nrec} cặp site×host")
open(os.path.join(D, "bo-sung.md"), "w").write("\n".join(L) + "\n"); print("\n".join(L))

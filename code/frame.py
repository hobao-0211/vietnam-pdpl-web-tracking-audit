"""K7 — dựng khung mẫu tất định (G4/G5). Chạy từ 5/:
python3 -I code/frame.py data/frame
Đầu vào (ghim trong data/frame/raw/): crux-vn-202610.csv.gz, public_suffix_list.dat
Đầu ra: data/frame/sites.tsv (domain, origin, stratum_frame), data/frame/flow.md (sơ đồ luồng mẫu), data/frame/nonvn_prepass.jsonl
Quy tắc (chốt trước khi crawl; xem docs/05-protocol.md §3):
  đơn vị = tên miền đăng ký (PSL); origin đại diện = origin hạng tốt nhất, ưu tiên https://www.<d> rồi https://<d>, rồi theo thứ tự chữ cái
  gov  = mọi *.gov.vn trong top-50k (tổng điều tra)
  edu  = ngẫu nhiên 170 trong *.edu.vn top-10k
  vn   = ngẫu nhiên 600 trong *.vn khác top-10k
  nonvn= tên miền không .vn trong top-1k, HTML tĩnh là tiếng Việt (lang vi hoặc ≥ 2% ký tự có dấu); điều kiện site VN (BCT/giấy phép báo chí/MST) xét SAU render
  loại trước: blocklist regex (người lớn, cờ bạc) trên tên miền; seed 20261122"""
import http.client, sys, os, gzip, csv, json, re, random, ssl, zlib, urllib.request
from urllib.parse import urlsplit
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(__file__)); from psl import PSL
OUT = sys.argv[1]; RAW = os.path.join(OUT, "raw"); SEED = 20261122
psl = PSL(os.path.join(RAW, "public_suffix_list.dat"))
rows = [(o, int(r)) for o, r in list(csv.reader(gzip.open(os.path.join(RAW, "crux-vn-202610.csv.gz"), "rt")))[1:]]
BLOCK = re.compile(r"sex|porn|xxx|jav|vlx|phimheo|18\+|casino|cacuoc|ca-cuoc|nhacai|nha-cai|bet\d|\d+bet|w88|fb88|m88|188bet|789bet|kubet|okvip|jun88|new88|hi88|f8bet|shbet|8xbet|xoilac|cakhia|vebo|mitom|socolive|thapcam|hentai|lauxanh|gaixinh|gai-goi|lu88|bong88|vn88|sv388|da88|ae888|b52|go88|sunwin|789club|iwin|rikvip", re.I)
flow = []
def pick_origin(d, origins):
    best = min(r for _, r in origins); cands = sorted(o for o, r in origins if r == best)
    for pref in (f"https://www.{d}", f"https://{d}"):
        if pref in cands: return pref, best
    return cands[0], best
def regs(maxrank):
    m = {}
    for o, r in rows:
        if r <= maxrank: m.setdefault(psl.reg(urlsplit(o).hostname), []).append((o, r))
    return m
R10, R50, R1 = regs(10000), regs(50000), regs(1000)
flow.append(f"CrUX VN 202610: {len(rows)} origin; top-10k → {len(R10)} tên miền đăng ký; top-50k → {len(R50)}; top-1k → {len(R1)}")
def blocked(ds): b = [d for d in ds if BLOCK.search(d)]; return [d for d in ds if not BLOCK.search(d)], b
gov_all = sorted(d for d in R50 if d.endswith(".gov.vn")); gov, gb = blocked(gov_all)
edu_all = sorted(d for d in R10 if d.endswith(".edu.vn")); edu_ok, eb = blocked(edu_all)
vn_all = sorted(d for d in R10 if d.endswith(".vn") and not d.endswith((".gov.vn", ".edu.vn"))); vn_ok, vb = blocked(vn_all)
rnd = random.Random(SEED); edu = sorted(rnd.sample(edu_ok, min(170, len(edu_ok)))); vn = sorted(rnd.sample(vn_ok, min(600, len(vn_ok))))
flow.append(f"gov: {len(gov_all)} *.gov.vn top-50k, loại blocklist {len(gb)} → tổng điều tra {len(gov)}")
flow.append(f"edu: {len(edu_all)} *.edu.vn top-10k, loại blocklist {len(eb)} → còn {len(edu_ok)} → rút ngẫu nhiên {len(edu)}")
flow.append(f"vn: {len(vn_all)} *.vn khác top-10k, loại blocklist {len(vb)} → còn {len(vn_ok)} → rút ngẫu nhiên {len(vn)}")
# nonvn prepass
ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36"
VNCH = re.compile(r"[ăâđêôơưạảấầẩẫậắằẳẵặẹẻẽếềểễệỉịọỏốồổỗộớờởỡợụủứừửữựỳỵỷỹ]", re.I)
SIG = {"bct": re.compile(r"online\.gov\.vn|dathongbao|bocongthuong|Bộ Công Thương", re.I),
       "press": re.compile(r"giấy phép (hoạt động )?(báo|tạp chí|thiết lập trang thông tin)|giấy phép số", re.I),
       "tax": re.compile(r"(mã số (doanh nghiệp|thuế)|MST|ĐKKD|đăng ký (kinh doanh|doanh nghiệp))\s*:?\s*\d{10}", re.I)}
def pre(d):
    o, rank = pick_origin(d, R1[d]); rec = {"domain": d, "origin": o, "rank": rank}
    try:
        r = urllib.request.urlopen(urllib.request.Request(o, headers={"User-Agent": UA, "Accept-Language": "vi-VN,vi;q=0.9", "Accept-Encoding": "gzip"}), timeout=15, context=ctx)
        try: b = r.read(3_000_000)
        except http.client.IncompleteRead as e: b = e.partial
        if b[:2] == b"\x1f\x8b": b = zlib.decompressobj(16 + zlib.MAX_WBITS).decompress(b)
        h = b.decode(r.headers.get_content_charset() or "utf-8", "replace")
        txt = re.sub(r"<[^>]+>", " ", re.sub(r"(?is)<(script|style).*?</\1>", " ", h))
        letters = sum(c.isalpha() for c in txt) or 1
        m = re.search(r'<html[^>]*\blang=["\']?([a-zA-Z-]+)', h, re.I)
        rec.update(ok=True, lang=(m.group(1).lower() if m else ""), vi_ratio=round(len(VNCH.findall(txt)) / letters, 4), **{k: bool(p.search(h)) for k, p in SIG.items()})
    except Exception as e:
        rec.update(ok=False, err=type(e).__name__)
    return rec
nonvn_all = sorted(d for d in R1 if not d.endswith(".vn")); nonvn_ok, nb = blocked(nonvn_all)
with ThreadPoolExecutor(12) as ex: pres = list(ex.map(pre, nonvn_ok))
with open(os.path.join(OUT, "nonvn_prepass.jsonl"), "w") as f:
    for p in pres: f.write(json.dumps(p, ensure_ascii=False) + "\n")
okp = [p for p in pres if p.get("ok")]
# Pha tĩnh chỉ lọc NGÔN NGỮ; điều kiện "site VN" (BCT/giấy phép báo chí/MST) xét sau render (code/analyze), vì footer thường do JS render
nonvn = sorted(p["domain"] for p in okp if (p["lang"].startswith("vi") or p["vi_ratio"] >= 0.02))
flow.append(f"nonvn: {len(nonvn_all)} tên miền không .vn top-1k, loại blocklist {len(nb)} → tải được {len(okp)}/{len(nonvn_ok)} → tiếng Việt (lang vi hoặc ≥2% ký tự có dấu): {len(nonvn)} ứng viên; điều kiện site VN xét sau render; {len(nonvn_ok)-len(okp)} không tải được tĩnh bị loại (ghi nhận là giới hạn)")
sample = [(d, pick_origin(d, R50[d])[0], "gov") for d in gov] + [(d, pick_origin(d, R10[d])[0], "edu") for d in edu] + \
         [(d, pick_origin(d, R10[d])[0], "vn") for d in vn] + [(d, pick_origin(d, R1[d])[0], "nonvn") for d in nonvn]
with open(os.path.join(OUT, "sites.tsv"), "w") as f:
    f.write("domain\torigin\tstratum_frame\n")
    for d, o, s in sample: f.write(f"{d}\t{o}\t{s}\n")
flow.append(f"TỔNG MẪU: {len(sample)} tên miền → data/frame/sites.tsv")
open(os.path.join(OUT, "flow.md"), "w").write("# Sơ đồ luồng mẫu (tự sinh bởi code/frame.py)\n\n" + "\n".join("- " + x for x in flow) + "\n\nBị loại do blocklist: " + ", ".join(gb + eb + vb + nb) + "\n")
print("\n".join(flow))

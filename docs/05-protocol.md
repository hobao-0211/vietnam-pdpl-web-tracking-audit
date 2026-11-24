# Protocol nghiên cứu K7 — viết TRƯỚC khi chạy đợt crawl chính

Chốt ngày 22/11/2026. Hash của file này, cùng code và khung mẫu, ghi trong `data/crawl/ghim-protocol.sha256` **trước** khi crawl đợt chính. Mọi thay đổi sau thời điểm đó ghi ở §8 kèm lý do.

Nguồn thiết kế:
- Phản biện độc lập: `data/novelty/phan-bien-K7.md`.
- Codebook pháp lý (bản nháp, Anh duyệt): `docs/05b-codebook-phap-ly.md`.
- Nguyên văn luật: `references/nguon-luat.md`.

**Phạm vi tuyên bố.** Bài **không kết luận vi phạm pháp luật**. Mọi phát biểu theo thang 4 bậc B0–B3: Observed → Identifier-bearing → Consent-relevant → Prima facie inconsistent (`phan-bien-K7.md` §3, codebook §2).

## 1. Câu hỏi nghiên cứu và tiêu chí trả lời

Mọi RQ là bài toán **ước lượng**. Không có giả thuyết "muốn ra có"; kết quả thấp cũng báo cáo như kết quả cao.

| RQ | Câu hỏi | Đo bằng gì (chỉ số codebook) | Tiêu chí trả lời (chốt trước) |
|---|---|---|---|
| RQ1 | Tỷ lệ site gửi luồng mang định danh tới bên thứ ba **trước mọi tương tác** là bao nhiêu? Tách theo loại bên nhận (quảng cáo / analytics / chức năng) và theo tầng | I1, I2, I3, I4, I5 trên profile A và B. Đơn vị: tên miền đăng ký | Trả lời khi mỗi tầng có ước lượng tỷ lệ kèm KTC 95% Wilson. Nửa độ rộng KTC ≤ 6 điểm % cho tầng `vn` (n ≈ 600) và ≤ 8 điểm % cho gov và edu. So sánh giữa tầng: tối đa 4 phép (vn–gov, vn–edu, vn–nonvn, gov–edu), kiểm định hai tỷ lệ, hiệu chỉnh Holm, α = 0,05. Báo cả hiệu số kèm KTC |
| RQ2 | Có bao nhiêu site có cơ chế đồng ý, thuộc loại nào (C0–C5, codebook Q-F)? Bấm "từ chối" có làm dừng luồng quảng cáo không? | I7: banner gộp = khối banner HOẶC script CMP; nút từ chối. I8, I9: luồng I3/I4 **sau khi bấm** từ chối (profile C) | Tỷ lệ C0–C5 kèm KTC 95%. Hiệu quả từ chối = % site có nút từ chối mà vẫn có I3 sau khi bấm. **Luật dừng:** < 30 site có nút từ chối thì RQ2b chỉ báo dạng mô tả, không suy luận |
| RQ3 | Bao nhiêu luồng mang định danh đi tới pháp nhân **trụ sở ở nước ngoài**? Bên nhận chính là ai? | I6. Chính: trụ sở pháp nhân (bảng entity, §3.4). Phụ: vị trí IP máy chủ (DB-IP Lite), báo riêng, ghi rõ giới hạn anycast/CDN | % site có ≥ 1 luồng I6, kèm KTC. Phân bố theo entity (top-10) và theo nước. Không khẳng định có hay không có TIA, vì TIA không quan sát được |
| RQ4 | Chính sách quyền riêng tư của chính site có nói tới những gì quan sát được không ("nói–làm")? | Tìm link chính sách trong DOM đã render, tải bản render. Từ điển P1–P12 (codebook §3), ba trạng thái: có / không / không xác định. P12 = văn bản viện dẫn (PDPL 91/2025, NĐ 356/2025, NĐ 13/2023 đã hết hiệu lực) | % site có chính sách. Trong số có chính sách: % nhắc cookie, bên thứ ba, quảng cáo, chuyển ra nước ngoài; % chỉ viện dẫn NĐ 13. Độ lệch "nói–làm" = % site có I3 (hoặc I6) mà chính sách không nhắc tới. **Luật dừng:** tìm được chính sách ở < 40% site thì RQ4 chỉ báo trên tập con, kèm cảnh báo chọn mẫu |
| RQ5 | **ĐÃ BỎ 22/11/2026** theo luật dừng: Wayback CDX trả 429 suốt 40 lần thử (khoảng 60 phút) nên không đo được P2. Ghi vào Limitations. (phụ, có điều kiện) Chính sách thay đổi gì quanh mốc 01/01/2026? | Wayback CDX | Chỉ làm nếu CDX hết 429 và ≥ 50% URL chính sách có bản lưu cả trước lẫn sau mốc (ngưỡng P2 của pilot). Không đạt thì bỏ RQ5 và ghi vào Limitations |

**Độ tin cậy là điều kiện để lên bậc B2/B3:** κ test–retest ≥ 0,6 cho chỉ số site-level tương ứng (§5). Không đạt thì chỉ số đó chỉ báo dạng mô tả (B0–B1).

## 2. Nhánh

**Kết hợp.**
- **Thực nghiệm đo lường web:** RQ1–RQ4.
- **Luật normative:** codebook diễn giải PDPL 91/2025 và NĐ 356/2025, ma trận chỉ số × điều khoản × ngoại lệ Đ.19 × tầng. Anh duyệt và chịu trách nhiệm phần diễn giải.

## 3. Dữ liệu và nguồn (đã ghim)

| Dữ liệu | Phiên bản / ghim | License | File |
|---|---|---|---|
| CrUX top list theo quốc gia VN | tháng 202610, `github.com/zakird/crux-top-lists`; sha256 trong `data/frame/raw/psl.sha256` | CC BY 4.0 (CrUX) `[CẦN KIỂM]` | `data/frame/raw/crux-vn-202610.csv.gz` |
| Public Suffix List | tải 22/11/2026, sha256 đã ghi | MPL 2.0 | `data/frame/raw/public_suffix_list.dat` |
| DuckDuckGo Tracker Radar (entity map, domain map) | commit `815b4d9a` (11/11/2026) | CC BY-NC-SA 4.0 `[CẦN KIỂM]`: chỉ dùng cho nghiên cứu, không phát hành lại file gốc | `data/frame/raw/ddg-*.json` |
| Disconnect services (danh mục) | commit `7a9e2be5` (20/11/2026) | GPL-3.0 | `data/frame/raw/disconnect-services.json` |
| DB-IP Lite country (IP → nước) | tải lúc phân tích, ghi tháng | CC BY 4.0 | `data/frame/raw/` |
| Văn bản luật | Công báo: PDPL (số 971+972/2025), NĐ 356 (số 18/2026) | văn bản QPPL, không có bản quyền | `references/nguon-luat.md` |
| Dữ liệu đo | crawl 22/11/2026 trở đi | sẽ phát hành dạng đặc trưng tổng hợp (§6) | `data/crawl/main/` |

### 3.1. Khung mẫu (tất định, `code/frame.py`, seed 20261122)
- Đơn vị mẫu là tên miền đăng ký (PSL). Origin đại diện là origin có hạng tốt nhất, ưu tiên `https://www.<d>`, rồi `https://<d>`, rồi theo thứ tự chữ cái.
- Các tầng khung:
  - **gov:** tổng điều tra *.gov.vn trong top-50k (201).
  - **edu:** rút ngẫu nhiên 170 trong 246 *.edu.vn của top-10k.
  - **vn:** rút ngẫu nhiên 600 trong 1.275 *.vn khác của top-10k.
  - **nonvn:** tên miền không đuôi `.vn` trong top-1k có trang tiếng Việt. Chỉ giữ site qua pha sơ loại bằng trình duyệt, có ≥ 1 tín hiệu "site VN" sau khi render: huy hiệu Bộ Công Thương, dòng giấy phép báo chí, hoặc MST/ĐKKD 10 số.
- Blocklist regex (người lớn, cờ bạc) áp trên tên miền, ghi trong `code/frame.py`. Số bị loại ở từng bước: `data/frame/flow.md`.
- **Tầng phân tích (hậu phân tầng, tất định, theo thứ tự ưu tiên):**
  1. GATED: có ô mật khẩu, hoặc URL cuối chứa `login|signin|dang-nhap|sso`, và văn bản < 1.500 ký tự.
  2. GOV, EDU theo đuôi tên miền.
  3. BC (báo chí): có dòng giấy phép báo chí.
  4. TM (thương mại): có huy hiệu Bộ Công Thương.
  5. KHÁC.

### 3.2. Quy trình đo (`code/crawl/crawl.cjs`, chạy qua `code/crawl/run.sh`)
- **Môi trường:** Chrome for Testing 153.0.8010.12 bản đầy đủ (headless), Playwright 1.66.0-alpha, locale vi-VN, múi giờ Asia/Ho_Chi_Minh, khung nhìn 1366×768, UA Chrome chuẩn (không có chuỗi "Headless"). Điểm đo: IP dân dụng tại Việt Nam.
- **Profile A và B:** hai context sạch, nạp origin, **không tương tác**, chờ 15 s. Ghi mọi request (URL, loại, frame, thời điểm, IP máy chủ, Set-Cookie), cookie và localStorage.
- **Riêng profile A:** ảnh chụp; dò khối banner (khối fixed/sticky có chữ cookie/dữ liệu và chữ đồng ý), script CMP, nút từ chối và nút đồng ý; tìm link chính sách trong DOM; tải bản render của trang chính sách; ghi tín hiệu tầng.
- **Profile C** (chỉ khi thấy nút từ chối): nạp trang, chờ 4 s, bấm từ chối, chờ 15 s, ghi các request sau khi bấm.

### 3.3. Định nghĩa vận hành
- **Bên thứ ba:** host có tên miền đăng ký khác site, **và** entity (DDG) khác entity của site. Tên miền không có trong DDG thì entity = chính tên miền đăng ký.
- **Định danh (I2):** dựa trên hai profile A và B, gồm:
  - cookie bên thứ ba có hạn > 24 giờ, giá trị ≥ 8 ký tự, giá trị khác nhau giữa A và B (cùng tên và cùng domain);
  - giá trị tham số URL ≥ 10 ký tự, xuất hiện ở ≥ 2 request bên thứ ba trong cùng profile, khác giữa A và B. Điều kiện "≥ 2 request" dùng để loại cache-buster;
  - loại các giá trị giống timestamp (chỉ chứa số và nằm trong ±10 ngày quanh thời điểm đo).
- **Loại bên nhận:** Disconnect (Advertising / Analytics / Social / Content / Fingerprinting…) cộng bảng bổ sung entity VN (admicro/VCCorp, eclick, Adtima/VNG…). Bảng bổ sung lập trước khi tính kết quả, mỗi dòng có nguồn. Chưa phân loại được thì ghi "unclassified" và báo tỷ lệ.
- **Nước của bên nhận (RQ3):** bảng trụ sở pháp nhân cho các entity chiếm ≥ 95% luồng I2, mỗi dòng có nguồn (website pháp nhân hoặc hồ sơ đăng ký). Phần còn lại ghi "unknown".

## 4. Phương pháp phân tích
- **Ước lượng tỷ lệ:** KTC 95% Wilson. Sai số theo cụm nhà cung cấp tag (GTM container/entity) để phân tích độ nhạy.
- **So sánh tầng:** tối đa 4 phép, hiệu chỉnh Holm.
- **Trước/sau khi bấm từ chối:** McNemar ghép cặp. **"Nói–làm":** bảng chéo hành vi × công bố kèm KTC.
- **Baseline so sánh** (không phải đối chứng thống kê):
  - bài Thái Lan (10.2139/ssrn.6603943);
  - Singh và cộng sự, IMC 2025 (10.1145/3730567.3764427);
  - RegTrack (arXiv 2603.02679).

  Bảng định vị (Table 1) đặt trong bài.

## 5. Threats to validity và cách chặn

| Threat | Chặn bằng | Ở đâu |
|---|---|---|
| Bộ dò banner/nút từ chối sai | Đối chứng dương 4 site CMP (onetrust, cookiebot, didomi, cookieyes): dò được 4/4 script CMP, 4/4 nút từ chối, 3/4 khối banner → chỉ số banner dùng dạng **gộp**. Kiểm tay mẫu phân tầng 70 site có cờ + 70 site không cờ trên ảnh chụp, báo PPV/NPV | `data/crawl/ctrl/`; kiểm tay ở P1, file `data/validation/` |
| Chặn tải media làm đổi hành vi trang | Request media vẫn được ghi; tracker gần như không phải resource type media. Tiểu mẫu độ nhạy (P1) chạy lại không chặn | `code/crawl/crawl.cjs` |
| Bot detection, chế độ headless | Chrome bản đầy đủ, UA chuẩn, tắt cờ AutomationControlled. Tiểu mẫu 100 site so headless với headful (P1) | `code/crawl/crawl.cjs` |
| Thời gian chờ cố định 15 s | Tiểu mẫu 100 site so 15 s với 30 s (P1) | — |
| Dao động theo lần nạp (đấu giá quảng cáo) | Test–retest: đợt 2 cách ≥ 24 giờ trên 150 site ngẫu nhiên, κ cho từng chỉ số site-level; điều kiện κ ≥ 0,6 để lên B2/B3 | `data/crawl/wave2/` |
| Định danh dương tính giả (cache-buster) | Điều kiện ≥ 2 request, loại timestamp; so tỷ lệ với cách chỉ đếm cookie | §3.3 |
| `.vn` không đồng nghĩa với "site VN" | Thêm tầng nonvn có tín hiệu VN; phân tích độ nhạy chỉ trên `.vn` | `code/frame.py` |
| Danh sách tracker thiếu bên VN | Bảng bổ sung entity VN lập trước khi tính; báo tỷ lệ unclassified | §3.3 |
| Định vị IP sau anycast/CDN | Định nghĩa chính theo trụ sở pháp nhân; định vị IP chỉ là phụ | §3.3 |
| Diễn giải pháp lý sai | Thang B0–B3; codebook công bố kèm bài; Anh duyệt nguyên văn từ Công báo | `docs/05b` |
| Một người kiểm (không có người thứ hai) | Đối chứng dương; tự mã hoá lại sau ≥ 14 ngày, báo κ nội người mã hoá; mọi quy tắc tất định | P1 |

## 6. Đạo đức và dữ liệu
- **Cách crawl:** chỉ GET các trang công khai. Không gửi form, không đăng nhập, không vượt CAPTCHA hay WAF. Không ai phải trả lời câu hỏi nào, nên không có người tham gia; IRB ghi "Not applicable" kèm lý do.
- **Tải lên site:** mỗi site khoảng 3–5 lần nạp trang trong vài phút. Có thể có thêm một lần ở đợt 2.
- **Lưu trữ:**
  - Văn bản chính sách và ảnh chụp chỉ lưu nội bộ, không phát hành nguyên văn.
  - Phát hành: mã nguồn, danh sách tên miền, đặc trưng tổng hợp theo site, codebook.
  - Tầng gov chỉ báo tổng hợp, ví dụ thì dùng mã giả danh.
- **Thông báo:** báo trước 30 ngày cho các site gov/edu có quảng cáo theo hành vi, trước khi công bố preprint (P2). Thông báo là hành động một chiều, Anh duyệt riêng.

## 7. Kế hoạch tính toán
- **Smoke test 20 site** (22/11): 20/20 OK, 3 phút ở par=4, khoảng 6 site/phút. RAM trống của máy ≥ 2 GB suốt lúc chạy.
- **Sự cố 22/11:** lần sơ loại đầu chạy par=6 làm máy **hết RAM**. OOM killer giết `flatpak-session-helper`, trình duyệt chết, 217/234 site lỗi. Kết quả lần đó bị bỏ toàn bộ.
  - OOM lần 2 lúc 17:29 (par=3, có chốt RAM mềm): một trang nặng làm RAM tăng vọt nhanh hơn chốt kịp phản ứng.
  - Từ đó crawler chạy như **dịch vụ user của systemd có giới hạn RAM cứng** (`MemoryMax=2200M`, `MemoryHigh=1800M`, không swap; `code/crawl/run.sh`). Vượt giới hạn thì chỉ crawler bị giết, ứng dụng khác của máy không bị ảnh hưởng.
  - par=2, mỗi trình duyệt tối đa 2 renderer.
  - RAM khả dụng (MemAvailable) < 900 MB thì tạm dừng mở site mới.
  - Trình duyệt chết thì tự khởi động lại và đưa site về hàng đợi.
  - Chặn tải luồng media (video/audio). Request media vẫn được ghi; chỉ không tải nội dung.
- **Sơ loại nonvn:** 234 ứng viên, par=3, chờ 6 s. Ước lượng khoảng 15 phút (ASSUMED).
- **Đợt chính:** khoảng 1.000 site, par=2, chờ 15 s. Ước lượng khoảng 5–6 giờ chạy nền (ASSUMED, sẽ đo lại theo tốc độ sơ loại). Chạy nền, có checkpoint (`done.txt`) nên ngắt rồi chạy tiếp được, heartbeat mỗi 60 s.
- **Đợt 2** (≥ 24 giờ sau): 150 site, khoảng 25 phút (ASSUMED).
- **Kaggle:** không dùng. Điểm đo phải đặt tại Việt Nam.

## 7b. Điều kiện dừng / đổi hướng
- Tỷ lệ site lỗi > 20% ở bất kỳ tầng nào → dừng, kiểm bot detection, sửa rồi chạy lại tầng đó.
- RAM trống < 800 MB kéo dài → giảm par.
- I2 < 10% ở mọi tầng → bài đổi trọng tâm thành "mức tuân thủ cao hơn kỳ vọng"; RQ vẫn giữ nguyên.
- κ test–retest < 0,6 cho I2/I3 → chỉ báo mô tả, bỏ các ô B2/B3.
- Codebook bị Anh sửa ở Q-A/Q-B/Q-D → chỉ đổi cột bậc trong ma trận; không đổi dữ liệu và không đổi định nghĩa vận hành.

## 8. Nhật ký thay đổi sau khi ghim
- **22/11 10:59Z:** par 3 → 5. **11:07Z:** par 5 → 6, MemoryMax 3200M. **11:13Z:** par 6 → 8, MemoryMax 4000M, MIN_FREE 1000 MB (RAM máy khả dụng 5,3 GB). Không đổi phép đo.
- **22/11 11:07Z, đổi thứ tự hàng đợi, không đổi mẫu:** `data/crawl/main-order.tsv`. Khối 1 gồm gov, edu, nonvn và 300 site vn rút ngẫu nhiên (seed 20261123, danh sách ở `data/crawl/vn-half1.txt`). Khối 2 là 300 site vn còn lại.
  - Lý do: Anh cần kết quả sớm hơn.
  - n = 300 vẫn đạt tiêu chí RQ1 ở §1 (nửa độ rộng KTC Wilson ≤ 6 điểm %, trường hợp xấu nhất p = 0,5).
  - Phân tích chính dùng đủ 600 site vn nếu khối 2 hoàn tất. Nếu chỉ báo trên khối 1 thì ghi rõ trong bài.
- **22/11 12:30Z, phân tích độ nhạy (§5) trên 100 site rút ngẫu nhiên từ `data/crawl/main.tsv` (seed 20261125, `data/crawl/sens-list.tsv`):** (a) chờ 30 s → `data/crawl/sens30/`; (b) không chặn media (cờ mới `--no-block-media` trong `crawl.cjs`, không đổi phép đo chính) → `data/crawl/nomedia/`. Hai đợt chạy song song, cùng giờ, nên khác biệt gồm cả dao động theo lần nạp. **Bỏ** tiểu mẫu headless/headful: chế độ headful mở cửa sổ trên máy của tác giả; ghi vào Limitations.
- **22/11 15:45Z, sửa lỗi phân tích và hoàn thiện các phân tích độ nhạy đã cam kết (§1, §3–§5) — KHÔNG thay đổi dữ liệu crawl đợt 1 (`main/sites.jsonl` giữ nguyên hash):**
  1. **Tái lập thời gian (`code/analyze.py`):** thay `time.time()` bằng timestamp lúc crawl (`A["ts"]`/`B["ts"]`/`C["ts"]`) trong `is_ts()` và `id_cookies()` để kết quả không trôi khi chạy lại về sau.
  2. **Phân loại theo full hostname (`code/analyze.py`):** tra `VN_SUPP`, `DDG`, `Disconnect` trên full hostname trước khi gộp theo `psl.reg`, sửa lỗi bỏ sót `analytics.google.com` và subdomain quảng cáo (`I4` chuẩn protocol tăng từ 190 lên 295 site; `I2`/`I3` không đổi).
  3. **Bổ sung độ nhạy 1P→3P cookie-sync (F10) và cookie-only (§5):** giữ nguyên chỉ số chính chuẩn protocol (`I2`–`I5`), báo song song `I2_ext`–`I4_ext` (cookie bên thứ nhất bền vững như `_ga`, `_fbp`, `__uidac` khác nhau giữa A và B được đồng bộ qua URL query tới bên thứ ba) và `I2_cookie_only`.
  4. **Sửa RQ2b (`code/analyze.py`, `code/crawl/crawl.cjs` cho đợt 2):** loại 2 site lỗi click timeout (`reject_click_err != null`) khỏi mẫu bấm được; tách riêng nhóm có banner/CMP thật (`n=17`) khỏi popup không phải banner (`n=4`); tách `I8`/`I9` mang định danh thực sự (B2/B3) khỏi mọi request (B0); thêm tiền phân loại tự động `C0–C5`. Trong `crawl.cjs`, chỉ gán `reject_clicked_at` sau khi `.click()` thành công và ưu tiên link chính sách cùng tên miền (áp dụng từ đợt 2; không đổi phép đo Profile A/B).
  5. **Làm sạch RQ4 (`code/analyze.py`, `code/stats.py`):** lọc 32 trang chính sách thô không hợp lệ (8 trang `policies.google.com/privacy`, 3 `online.gov.vn`, 1 Mozilla/Microsoft/Cloudflare/cookiesandyou, 5 bài tin tức/tạp chí, 9 redirect trang chủ, 3 trang 404/challenge/JSON) → còn 331/946 chính sách hợp lệ (báo song song cả 363 thô); sửa `norm()` thêm ký tự eth `Ð`/`ð`; tách `google analytics` (`ANAME`) khỏi `ADNAME`; thêm `DPO`, `RETENTION`, `SENSITIVE`, kiểm định McNemar ghép cặp và gom cụm mẫu chính sách bằng SimHash 64-bit.
  6. **Mở rộng `code/entity_hq.json` đạt ngưỡng ≥ 95% (§3.3):** mở rộng từ 60 lên 121 entity kèm trường `source`, đưa độ phủ luồng định danh từ 80,9% lên **95,1%** (2.273/2.391 luồng).
  7. **Hoàn thiện dữ liệu tham chiếu & độ nhạy (`code/sensitivity.py` → `data/analysis/do-nhay.md`):** tải DB-IP Lite 2026-11 (`CC BY 4.0`, tra được 99,7% luồng để so trụ sở vs IP), EasyPrivacy + EasyList 22/11/2026 (độ hội tụ site-level κ = 0,941–0,954), phân tích `sens30` (κ = 0,976–1,000) & `nomedia` (κ = 0,954–1,000), sai số chuẩn theo cụm ngoại sinh (GTM + SimHash, DEFF = 1,02–1,07), hiệu số kèm KTC 95% Newcombe-Wilson.
  8. **Khôi phục gói kiểm định thủ công (`data/validation/`):** thay vì bỏ kiểm tay để dùng LLM (mâu thuẫn với F16 và JCP 153), xuất sẵn gói kiểm định cho tác giả gồm toàn bộ 39 site banner/nút từ chối, 6 site `gov` có quảng cáo, 5 ứng viên mâu thuẫn mạnh, 37 site PDPL, và mẫu phân tầng tất định (seed 20261122: 39 dương + 70 âm cho banner; 70 dương + 70 âm cho chính sách). Hash mới ghi riêng tại `data/crawl/ghim-sau-sua-20261122.sha256` (giữ nguyên `ghim-protocol.sha256` gốc).
  9. **Hoàn tất Đợt 2 test–retest (24/11/2026, cách Đợt 1 36,5 giờ) & kiểm định toàn diện 100% tập dương tính:** Đợt 2 chạy trên `data/crawl/wave2.tsv` (150 site, nút thoát Cloudflare WARP tại Việt Nam `AS13335`, SHA-256 `data/crawl/wave2/sites.jsonl` = `05cccbf54c2d390a...`) đạt 112 site đợt 2 và **107 site ghép cặp** (`data/analysis/wave2-kappa.md`): toàn bộ chỉ số chính vượt ngưỡng κ ≥ 0,60 (`I1` 0,967; `I2` 0,775; `I3` 0,757; `I4` 0,776; `I2_ext` 0,777; `I3_ext` 0,816; `I4_ext` 0,849; `banner_any` 0,824; `reject_in_banner` 1,000; `policy_found` 0,918; Spearman ρ = 0,976/0,825), duy nhất `I5` (κ = 0,560) giữ ở bậc mô tả `B1` đúng luật dừng §1. Kiểm định 100% ảnh chụp nhóm banner/nút (39/39) và 100% câu khớp RQ4 (`data/validation/bao-cao-kiem-dinh-duong-tinh.md`) xác minh 33/946 (3,5%) banner hiển thị thật (gồm ≥ 4 ca `C5` nút gạt bật sẵn), 8/20 (40,0%) quảng cáo sau từ chối và 32/37 (86,5%) viện dẫn PDPL VN thật. Ghi rõ giới hạn chưa có hội đồng hai người chấm cho mẫu âm tính (recall) ở Mục 7 bản thảo.

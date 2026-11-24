# Kết quả K7 (tự sinh bởi code/stats.py — không sửa tay)

Site trong dữ liệu: 997 · đo được (A và B ok): 946 · lỗi: 51 (5.1%)

Lỗi theo loại: Error: page.goto: net::ERR_NAME_NOT_RESO: 13; Error: SITE_TIMEOUT: 12; Error: page.waitForTimeout: Target page,: 7; Error: browser.newContext: Target page, : 5; Error: page.goto: net::ERR_CONNECTION_RE: 4; TimeoutError: page.goto: Timeout 45000ms: 2; Error: page.goto: Download is starting
C: 2; Error: page.goto: Target page, context o: 2
Tỷ lệ lỗi theo tầng khung: edu: 3/170 (1.8%); gov: 26/201 (12.9%); nonvn: 0/26 (0.0%); vn: 22/600 (3.7%) (mọi tầng < ngưỡng dừng 20%)

## RQ1–RQ2–RQ4: tỷ lệ theo tầng khung (KTC 95% Wilson)

| Chỉ số | edu | gov | nonvn | vn | Tất cả |
|---|---|---|---|---|---|
| I1 Có request tới bên thứ ba (B0) | 121/167 = 72.5% [65.2–78.7] | 132/175 = 75.4% [68.5–81.2] | 26/26 = 100.0% [87.1–100.0] | 511/578 = 88.4% [85.5–90.8] | 790/946 = 83.5% [81.0–85.7] |
| I2 Luồng mang định danh chuẩn protocol (3P cookie + 3P URL ≥2 req, B1) | 35/167 = 21.0% [15.5–27.7] | 38/175 = 21.7% [16.2–28.4] | 21/26 = 80.8% [62.1–91.5] | 358/578 = 61.9% [57.9–65.8] | 452/946 = 47.8% [44.6–51.0] |
| I3 … tới bên quảng cáo (chuẩn protocol) | 9/167 = 5.4% [2.9–9.9] | 4/175 = 2.3% [0.9–5.7] | 21/26 = 80.8% [62.1–91.5] | 248/578 = 42.9% [38.9–47.0] | 282/946 = 29.8% [27.0–32.8] |
| I4 … tới bên analytics (chuẩn protocol) | 18/167 = 10.8% [6.9–16.4] | 15/175 = 8.6% [5.3–13.7] | 18/26 = 69.2% [50.0–83.5] | 244/578 = 42.2% [38.3–46.3] | 295/946 = 31.2% [28.3–34.2] |
| I5 … tới bên chức năng/MXH (chuẩn protocol) | 22/167 = 13.2% [8.9–19.1] | 21/175 = 12.0% [8.0–17.6] | 21/26 = 80.8% [62.1–91.5] | 277/578 = 47.9% [43.9–52.0] | 341/946 = 36.0% [33.0–39.2] |
| I2_ext Độ nhạy F10: I2 + 1P→3P cookie-sync (GA4/Meta/Admicro) | 49/167 = 29.3% [23.0–36.6] | 67/175 = 38.3% [31.4–45.7] | 24/26 = 92.3% [75.9–97.9] | 418/578 = 72.3% [68.5–75.8] | 558/946 = 59.0% [55.8–62.1] |
| I3_ext Độ nhạy F10: I3 + 1P→3P cookie-sync (quảng cáo) | 12/167 = 7.2% [4.2–12.1] | 6/175 = 3.4% [1.6–7.3] | 24/26 = 92.3% [75.9–97.9] | 303/578 = 52.4% [48.3–56.5] | 345/946 = 36.5% [33.5–39.6] |
| I4_ext Độ nhạy F10: I4 + 1P→3P cookie-sync (analytics/GA4) | 37/167 = 22.2% [16.5–29.0] | 50/175 = 28.6% [22.4–35.7] | 22/26 = 84.6% [66.5–93.8] | 375/578 = 64.9% [60.9–68.7] | 484/946 = 51.2% [48.0–54.3] |
| banner_any Có cơ chế đồng ý (khối banner HOẶC script CMP) | 0/167 = 0.0% [0.0–2.2] | 0/175 = 0.0% [0.0–2.1] | 2/26 = 7.7% [2.1–24.1] | 32/578 = 5.5% [3.9–7.7] | 34/946 = 3.6% [2.6–5.0] |
| reject_in_banner Có nút từ chối trong ngữ cảnh banner/CMP | 0/167 = 0.0% [0.0–2.2] | 0/175 = 0.0% [0.0–2.1] | 2/26 = 7.7% [2.1–24.1] | 16/578 = 2.8% [1.7–4.4] | 18/946 = 1.9% [1.2–3.0] |
| reject_button Có nút khớp regex từ chối (gồm cả popup không banner) | 0/167 = 0.0% [0.0–2.2] | 0/175 = 0.0% [0.0–2.1] | 3/26 = 11.5% [4.0–29.0] | 20/578 = 3.5% [2.3–5.3] | 23/946 = 2.4% [1.6–3.6] |
| policy_found Có chính sách hợp lệ (đã lọc trang ngoài/404/tin tức) | 40/167 = 24.0% [18.1–31.0] | 7/175 = 4.0% [2.0–8.0] | 25/26 = 96.2% [81.1–99.3] | 259/578 = 44.8% [40.8–48.9] | 331/946 = 35.0% [32.0–38.1] |
| policy_found_raw Tìm được trang chính sách thô (>300B, trước lọc) | 42/167 = 25.1% [19.2–32.2] | 16/175 = 9.1% [5.7–14.3] | 25/26 = 96.2% [81.1–99.3] | 280/578 = 48.4% [44.4–52.5] | 363/946 = 38.4% [35.3–41.5] |

## RQ1–RQ2–RQ4: tỷ lệ theo tầng phân tích (KTC 95% Wilson)

| Chỉ số | BC | EDU | GATED | GOV | KHAC | TM | Tất cả |
|---|---|---|---|---|---|---|---|
| I1 Có request tới bên thứ ba (B0) | 30/30 = 100.0% [88.6–100.0] | 72/94 = 76.6% [67.1–84.0] | 157/244 = 64.3% [58.2–70.1] | 96/118 = 81.4% [73.4–87.4] | 237/262 = 90.5% [86.3–93.5] | 198/198 = 100.0% [98.1–100.0] | 790/946 = 83.5% [81.0–85.7] |
| I2 Luồng mang định danh chuẩn protocol (3P cookie + 3P URL ≥2 req, B1) | 21/30 = 70.0% [52.1–83.3] | 23/94 = 24.5% [16.9–34.0] | 40/244 = 16.4% [12.3–21.6] | 34/118 = 28.8% [21.4–37.6] | 158/262 = 60.3% [54.3–66.0] | 176/198 = 88.9% [83.8–92.5] | 452/946 = 47.8% [44.6–51.0] |
| I3 … tới bên quảng cáo (chuẩn protocol) | 12/30 = 40.0% [24.6–57.7] | 9/94 = 9.6% [5.1–17.2] | 5/244 = 2.0% [0.9–4.7] | 4/118 = 3.4% [1.3–8.4] | 100/262 = 38.2% [32.5–44.2] | 152/198 = 76.8% [70.4–82.1] | 282/946 = 29.8% [27.0–32.8] |
| I4 … tới bên analytics (chuẩn protocol) | 18/30 = 60.0% [42.3–75.4] | 10/94 = 10.6% [5.9–18.5] | 24/244 = 9.8% [6.7–14.2] | 13/118 = 11.0% [6.6–17.9] | 99/262 = 37.8% [32.1–43.8] | 131/198 = 66.2% [59.3–72.4] | 295/946 = 31.2% [28.3–34.2] |
| I5 … tới bên chức năng/MXH (chuẩn protocol) | 11/30 = 36.7% [21.9–54.5] | 17/94 = 18.1% [11.6–27.1] | 20/244 = 8.2% [5.4–12.3] | 20/118 = 16.9% [11.2–24.7] | 110/262 = 42.0% [36.2–48.0] | 163/198 = 82.3% [76.4–87.0] | 341/946 = 36.0% [33.0–39.2] |
| I2_ext Độ nhạy F10: I2 + 1P→3P cookie-sync (GA4/Meta/Admicro) | 30/30 = 100.0% [88.6–100.0] | 32/94 = 34.0% [25.3–44.1] | 53/244 = 21.7% [17.0–27.3] | 58/118 = 49.2% [40.3–58.1] | 198/262 = 75.6% [70.0–80.4] | 187/198 = 94.4% [90.3–96.9] | 558/946 = 59.0% [55.8–62.1] |
| I3_ext Độ nhạy F10: I3 + 1P→3P cookie-sync (quảng cáo) | 21/30 = 70.0% [52.1–83.3] | 10/94 = 10.6% [5.9–18.5] | 9/244 = 3.7% [2.0–6.9] | 6/118 = 5.1% [2.4–10.7] | 128/262 = 48.9% [42.9–54.9] | 171/198 = 86.4% [80.9–90.5] | 345/946 = 36.5% [33.5–39.6] |
| I4_ext Độ nhạy F10: I4 + 1P→3P cookie-sync (analytics/GA4) | 30/30 = 100.0% [88.6–100.0] | 23/94 = 24.5% [16.9–34.0] | 38/244 = 15.6% [11.6–20.7] | 43/118 = 36.4% [28.3–45.4] | 171/262 = 65.3% [59.3–70.8] | 179/198 = 90.4% [85.5–93.8] | 484/946 = 51.2% [48.0–54.3] |
| banner_any Có cơ chế đồng ý (khối banner HOẶC script CMP) | 0/30 = 0.0% [0.0–11.4] | 0/94 = 0.0% [0.0–3.9] | 0/244 = 0.0% [0.0–1.5] | 0/118 = 0.0% [0.0–3.2] | 20/262 = 7.6% [5.0–11.5] | 14/198 = 7.1% [4.3–11.5] | 34/946 = 3.6% [2.6–5.0] |
| reject_in_banner Có nút từ chối trong ngữ cảnh banner/CMP | 0/30 = 0.0% [0.0–11.4] | 0/94 = 0.0% [0.0–3.9] | 0/244 = 0.0% [0.0–1.5] | 0/118 = 0.0% [0.0–3.2] | 10/262 = 3.8% [2.1–6.9] | 8/198 = 4.0% [2.1–7.8] | 18/946 = 1.9% [1.2–3.0] |
| reject_button Có nút khớp regex từ chối (gồm cả popup không banner) | 0/30 = 0.0% [0.0–11.4] | 0/94 = 0.0% [0.0–3.9] | 1/244 = 0.4% [0.1–2.3] | 0/118 = 0.0% [0.0–3.2] | 11/262 = 4.2% [2.4–7.4] | 11/198 = 5.6% [3.1–9.7] | 23/946 = 2.4% [1.6–3.6] |
| policy_found Có chính sách hợp lệ (đã lọc trang ngoài/404/tin tức) | 5/30 = 16.7% [7.3–33.6] | 35/94 = 37.2% [28.1–47.3] | 11/244 = 4.5% [2.5–7.9] | 5/118 = 4.2% [1.8–9.5] | 112/262 = 42.7% [36.9–48.8] | 163/198 = 82.3% [76.4–87.0] | 331/946 = 35.0% [32.0–38.1] |
| policy_found_raw Tìm được trang chính sách thô (>300B, trước lọc) | 5/30 = 16.7% [7.3–33.6] | 35/94 = 37.2% [28.1–47.3] | 16/244 = 6.6% [4.1–10.4] | 13/118 = 11.0% [6.6–17.9] | 119/262 = 45.4% [39.5–51.5] | 175/198 = 88.4% [83.2–92.1] | 363/946 = 38.4% [35.3–41.5] |

## So sánh tầng khung (z hai tỷ lệ, hiệu chỉnh Holm, hiệu số + KTC 95% Newcombe-Wilson)

- I2 vn vs gov: 61.9% vs 21.7% · hiệu +40.2 điểm % [+32.4, +46.9] · p=0.0000 · p_Holm=0.0000
- I2 vn vs edu: 61.9% vs 21.0% · hiệu +41.0 điểm % [+33.1, +47.7] · p=0.0000 · p_Holm=0.0000
- I2 vn vs nonvn: 61.9% vs 80.8% · hiệu -18.8 điểm % [-30.3, +0.2] · p=0.0520 · p_Holm=0.1041
- I2 gov vs edu: 21.7% vs 21.0% · hiệu +0.8 điểm % [-8.0, +9.4] · p=0.8645 · p_Holm=0.8645
- I3 vn vs gov: 42.9% vs 2.3% · hiệu +40.6 điểm % [+35.4, +44.9] · p=0.0000 · p_Holm=0.0000
- I3 vn vs edu: 42.9% vs 5.4% · hiệu +37.5 điểm % [+31.5, +42.3] · p=0.0000 · p_Holm=0.0000
- I3 vn vs nonvn: 42.9% vs 80.8% · hiệu -37.9 điểm % [-49.3, -18.8] · p=0.0001 · p_Holm=0.0003
- I3 gov vs edu: 2.3% vs 5.4% · hiệu -3.1 điểm % [-7.8, +1.2] · p=0.1335 · p_Holm=0.1335
- I2_ext vn vs gov: 72.3% vs 38.3% · hiệu +34.0 điểm % [+25.7, +41.7] · p=0.0000 · p_Holm=0.0000
- I2_ext vn vs edu: 72.3% vs 29.3% · hiệu +43.0 điểm % [+34.7, +50.2] · p=0.0000 · p_Holm=0.0000
- I2_ext vn vs nonvn: 72.3% vs 92.3% · hiệu -20.0 điểm % [-26.7, -3.2] · p=0.0244 · p_Holm=0.0488
- I2_ext gov vs edu: 38.3% vs 29.3% · hiệu +8.9 điểm % [-1.1, +18.7] · p=0.0807 · p_Holm=0.0807
- I3_ext vn vs gov: 52.4% vs 3.4% · hiệu +49.0 điểm % [+43.4, +53.4] · p=0.0000 · p_Holm=0.0000
- I3_ext vn vs edu: 52.4% vs 7.2% · hiệu +45.2 điểm % [+38.8, +50.3] · p=0.0000 · p_Holm=0.0000
- I3_ext vn vs nonvn: 52.4% vs 92.3% · hiệu -39.9 điểm % [-46.8, -22.9] · p=0.0001 · p_Holm=0.0001
- I3_ext gov vs edu: 3.4% vs 7.2% · hiệu -3.8 điểm % [-9.0, +1.1] · p=0.1199 · p_Holm=0.1199
- I4_ext vn vs gov: 64.9% vs 28.6% · hiệu +36.3 điểm % [+28.2, +43.5] · p=0.0000 · p_Holm=0.0000
- I4_ext vn vs edu: 64.9% vs 22.2% · hiệu +42.7 điểm % [+34.8, +49.5] · p=0.0000 · p_Holm=0.0000
- I4_ext vn vs nonvn: 64.9% vs 84.6% · hiệu -19.7 điểm % [-29.8, -1.2] · p=0.0381 · p_Holm=0.0761
- I4_ext gov vs edu: 28.6% vs 22.2% · hiệu +6.4 điểm % [-2.8, +15.5] · p=0.1733 · p_Holm=0.1733

## RQ2: cơ chế đồng ý (tiền phân loại tự động C0–C5) & sau khi bấm từ chối

- C0: 912/946 = 96.4% [95.0–97.4]
- C1: 7/946 = 0.7% [0.4–1.5]
- C2: 9/946 = 1.0% [0.5–1.8]
- C3_or_C4: 18/946 = 1.9% [1.2–3.0]
- Lưu ý: phân tách C3 vs C4 và gắn cờ C5 (dark pattern) cần kiểm tra ảnh chụp.

- Site có nút khớp regex từ chối (Profile C): 23 · bấm thành công (không lỗi): 21 · lỗi click timeout: 2
- Trong số bấm thành công: có banner/CMP thật: 17 · không có banner/CMP (nghi popup thông báo): 4 (< 30 → CHỈ MÔ TẢ theo luật dừng)
  - [Tất cả bấm thành công, n=21] Sau bấm vẫn có luồng ĐỊNH DANH quảng cáo (I8, B3): 8/21 = 38.1% [20.8–59.1]
  - [Tất cả bấm thành công, n=21] Sau bấm vẫn có luồng ĐỊNH DANH analytics (I9, B2): 11/21 = 52.4% [32.4–71.7]
  - [Tất cả bấm thành công, n=21] Sau bấm vẫn có BẤT KỲ request quảng cáo nào (B0): 10/21 = 47.6% [28.3–67.6]
  - [Tất cả bấm thành công, n=21] Sau bấm vẫn có BẤT KỲ request analytics nào (B0): 15/21 = 71.4% [50.0–86.2]
  - [Chỉ nhóm có banner/CMP, n=17] Sau bấm vẫn có luồng ĐỊNH DANH quảng cáo (I8, B3): 7/17 = 41.2% [21.6–64.0]
  - [Chỉ nhóm có banner/CMP, n=17] Sau bấm vẫn có luồng ĐỊNH DANH analytics (I9, B2): 7/17 = 41.2% [21.6–64.0]
  - [Chỉ nhóm có banner/CMP, n=17] Sau bấm vẫn có BẤT KỲ request quảng cáo nào (B0): 7/17 = 41.2% [21.6–64.0]
  - [Chỉ nhóm có banner/CMP, n=17] Sau bấm vẫn có BẤT KỲ request analytics nào (B0): 11/17 = 64.7% [41.3–82.7]

## RQ3: bên nhận luồng định danh (theo entity, chuẩn protocol)

Tổng luồng (site × bên nhận): 2391 · độ phủ bảng trụ sở `entity_hq.json`: 2273/2391 = 95.1% (ngưỡng protocol ≥ 95%)

| Entity | Luồng | % | Số site | Trụ sở |
|---|---|---|---|---|
| Google LLC | 890 | 37.2% | 388 | US |
| Facebook, Inc. | 223 | 9.3% | 213 | US |
| Microsoft Corporation | 177 | 7.4% | 96 | US |
| ByteDance Ltd. | 96 | 4.0% | 95 | CN/KY |
| VCCorp | 81 | 3.4% | 41 | VN |
| The Trade Desk Inc | 34 | 1.4% | 34 | US |
| Criteo SA | 33 | 1.4% | 33 | FR |
| IPONWEB GmbH | 25 | 1.0% | 20 | DE |
| nanda.vn | 24 | 1.0% | 24 | VN |
| LiveRamp Holdings, Inc. | 24 | 1.0% | 17 | US |
| VNG Corporation | 21 | 0.9% | 21 | VN |
| Magnite, Inc. | 21 | 0.9% | 21 | US |
| PubMatic, Inc. | 20 | 0.8% | 20 | US |
| TripleLift | 19 | 0.8% | 19 | US |
| Smartadserver S.A.S | 18 | 0.8% | 18 | FR |
| Improve Digital BV | 17 | 0.7% | 17 | NL |
| RhythmOne | 15 | 0.6% | 15 | US |
| Index Exchange, Inc. | 15 | 0.6% | 15 | CA |
| Media.net Advertising FZ-LLC | 15 | 0.6% | 15 | AE |
| Unruly Group Limited | 15 | 0.6% | 15 | GB |
| DTS Technology | 12 | 0.5% | 6 | IL |
| Supership Inc | 12 | 0.5% | 12 | JP |
| Taboola, Inc. | 12 | 0.5% | 12 | US/IL |
| Geniee, inc. | 11 | 0.5% | 5 | JP |
| Teads ( Luxenbourg ) SA | 11 | 0.5% | 11 | LU |

25 entity đầu chiếm 77.0% luồng.
- Phân bố luồng theo nước trụ sở (top 10): US: 1618 (67.7%), VN: 159 (6.6%), ?: 118 (4.9%), CN/KY: 96 (4.0%), FR: 61 (2.6%), JP: 45 (1.9%), GB: 43 (1.8%), DE: 34 (1.4%), CA: 33 (1.4%), IL: 30 (1.3%)
- Site có ≥ 1 luồng định danh chuẩn protocol tới entity trụ sở ngoài VN: 434/946 = 45.9% [42.7–49.1]
- Độ nhạy F10 (gồm 1P→3P cookie-sync): site có ≥ 1 luồng tới entity trụ sở ngoài VN: 545/946 = 57.6% [54.4–60.7]

## RQ4: chính sách quyền riêng tư (nói–làm, bản đã làm sạch)

Trang chính sách thô (>300B): 363/946 = 38.4% [35.3–41.5] · sau lọc loại trang không hợp lệ: **331/946 = 35.0% [32.0–38.1]** (< 40% → báo trên TẬP CON theo luật dừng)
Lý do loại trang thô không hợp lệ: homepage_redirect=9, external_vendor:google.com=8, news_article=3, external_vendor:online.gov.vn=3, gov_non_policy_article=2, external_vendor:mozilla.org=1, external_vendor:microsoft.com=1, external_vendor:cloudflare.com=1, external_vendor:cookiesandyou.com=1, error_or_challenge=1, too_short=1, raw_json=1

- LAW_PDPL: AFF 36 · COND 1 · NEG_ONLY 0 · NONE 294  (AFF+COND = 37/331 = 11.2% [8.2–15.0])
- DEC_356: AFF 21 · COND 1 · NEG_ONLY 0 · NONE 309  (AFF+COND = 22/331 = 6.6% [4.4–9.9])
- DEC_13: AFF 29 · COND 0 · NEG_ONLY 0 · NONE 302  (AFF+COND = 29/331 = 8.8% [6.2–12.3])
- COOKIE: AFF 168 · COND 0 · NEG_ONLY 0 · NONE 163  (AFF+COND = 168/331 = 50.8% [45.4–56.1])
- THIRD: AFF 198 · COND 19 · NEG_ONLY 12 · NONE 102  (AFF+COND = 217/331 = 65.6% [60.3–70.5])
- PARTNER: AFF 178 · COND 0 · NEG_ONLY 0 · NONE 153  (AFF+COND = 178/331 = 53.8% [48.4–59.1])
- ADPART: AFF 32 · COND 0 · NEG_ONLY 2 · NONE 297  (AFF+COND = 32/331 = 9.7% [6.9–13.3])
- ADNAME: AFF 17 · COND 0 · NEG_ONLY 0 · NONE 314  (AFF+COND = 17/331 = 5.1% [3.2–8.1])
- ANAME: AFF 33 · COND 0 · NEG_ONLY 0 · NONE 298  (AFF+COND = 33/331 = 10.0% [7.2–13.7])
- XBORDER: AFF 54 · COND 0 · NEG_ONLY 1 · NONE 276  (AFF+COND = 54/331 = 16.3% [12.7–20.7])
- WITHDRAW: AFF 94 · COND 3 · NEG_ONLY 6 · NONE 228  (AFF+COND = 97/331 = 29.3% [24.7–34.4])
- DPO: AFF 24 · COND 0 · NEG_ONLY 0 · NONE 307  (AFF+COND = 24/331 = 7.3% [4.9–10.6])
- RETENTION: AFF 169 · COND 11 · NEG_ONLY 1 · NONE 150  (AFF+COND = 180/331 = 54.4% [49.0–59.7])
- SENSITIVE: AFF 60 · COND 2 · NEG_ONLY 5 · NONE 264  (AFF+COND = 62/331 = 18.7% [14.9–23.3])
- Chỉ viện dẫn NĐ 13/2023 (không nhắc PDPL/NĐ 356): 24/331 = 7.3% [4.9–10.6]
- Có luồng quảng cáo (I3) nhưng chính sách không nhắc bên thứ ba/đối tác quảng cáo/tên adtech (đã tách GA): 57/196 = 29.1% [23.2–35.8]
- Có luồng quảng cáo (I3) nhưng chính sách không nhắc cookie: 89/196 = 45.4% [38.6–52.4]
- Ứng viên mâu thuẫn mạnh (`THIRD==NEG_ONLY` & `I3`, cần kiểm tay ngữ cảnh): 5 site (EDU-056a5331a7, VN-4710976f38, VN-9a8258aa2a, VN-bd4092662a, VN-f7408cc298)

### Kiểm định McNemar ghép cặp 'nói–làm' (trên tập có chính sách hợp lệ, n=331)
- I3 (làm quảng cáo) vs ADPART/ADNAME (nói quảng cáo): làm-không-nói=173, nói-không-làm=16, p_McNemar=1.85e-34
- I3 (làm quảng cáo) vs COOKIE (nói cookie): làm-không-nói=89, nói-không-làm=61, p_McNemar=0.02715
- I6 (luồng entity nước ngoài) vs XBORDER (nói chuyển ra nước ngoài): làm-không-nói=196, nói-không-làm=10, p_McNemar=6.221e-46

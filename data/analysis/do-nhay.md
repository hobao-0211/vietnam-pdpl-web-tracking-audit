# Phân tích độ nhạy, hội tụ và sai số theo cụm (tự sinh bởi code/sensitivity.py)

## 1. Độ nhạy thời gian chờ (30 s vs 15 s) và chặn media (Protocol §5, §8)

### Chờ 30 s (`sens30`) vs chính 15 s (n ghép cặp đo được cả hai = 97)

| Chỉ số | Chính (15 s) | Độ nhạy | Đồng thuận | κ | PABAK | Lệch (+/−) | p McNemar |
|---|---|---|---|---|---|---|---|
| I1 | 75/97 (77.3%) | 75/97 (77.3%) | 100.0% | 1.000 | 1.000 | -0/+0 | 1 |
| I2 | 46/97 (47.4%) | 45/97 (46.4%) | 99.0% | 0.979 | 0.979 | -1/+0 | 1 |
| I3 | 30/97 (30.9%) | 29/97 (29.9%) | 99.0% | 0.976 | 0.979 | -1/+0 | 1 |
| I4 | 33/97 (34.0%) | 34/97 (35.1%) | 99.0% | 0.977 | 0.979 | -0/+1 | 1 |
| I2_ext | 53/97 (54.6%) | 53/97 (54.6%) | 100.0% | 1.000 | 1.000 | -0/+0 | 1 |
| I3_ext | 35/97 (36.1%) | 34/97 (35.1%) | 99.0% | 0.978 | 0.979 | -1/+0 | 1 |
| I4_ext | 48/97 (49.5%) | 48/97 (49.5%) | 100.0% | 1.000 | 1.000 | -0/+0 | 1 |
| banner_any | 6/97 (6.2%) | 5/97 (5.2%) | 99.0% | 0.904 | 0.979 | -1/+0 | 1 |
| policy_found | 29/97 (29.9%) | 30/97 (30.9%) | 99.0% | 0.976 | 0.979 | -0/+1 | 1 |

### Không chặn media (`nomedia`) vs chính (n ghép cặp đo được cả hai = 98)

| Chỉ số | Chính (15 s) | Độ nhạy | Đồng thuận | κ | PABAK | Lệch (+/−) | p McNemar |
|---|---|---|---|---|---|---|---|
| I1 | 76/98 (77.6%) | 76/98 (77.6%) | 100.0% | 1.000 | 1.000 | -0/+0 | 1 |
| I2 | 47/98 (48.0%) | 47/98 (48.0%) | 100.0% | 1.000 | 1.000 | -0/+0 | 1 |
| I3 | 31/98 (31.6%) | 31/98 (31.6%) | 100.0% | 1.000 | 1.000 | -0/+0 | 1 |
| I4 | 34/98 (34.7%) | 32/98 (32.7%) | 98.0% | 0.954 | 0.959 | -2/+0 | 0.5 |
| I2_ext | 54/98 (55.1%) | 54/98 (55.1%) | 100.0% | 1.000 | 1.000 | -0/+0 | 1 |
| I3_ext | 36/98 (36.7%) | 36/98 (36.7%) | 100.0% | 1.000 | 1.000 | -0/+0 | 1 |
| I4_ext | 49/98 (50.0%) | 49/98 (50.0%) | 100.0% | 1.000 | 1.000 | -0/+0 | 1 |
| banner_any | 6/98 (6.1%) | 4/98 (4.1%) | 98.0% | 0.790 | 0.959 | -2/+0 | 0.5 |
| policy_found | 29/98 (29.6%) | 30/98 (30.6%) | 99.0% | 0.976 | 0.980 | -0/+1 | 1 |

## 2. Độ nhạy định nghĩa định danh (F10) và khung mẫu `.vn`-only (F8)

| Phiên bản định nghĩa | Tất cả (n=946) | Tầng `vn` (n=578) | Chỉ `.vn` (gồm vn+gov+edu, n=920) |
|---|---|---|---|
| I2 chỉ đếm cookie 3P (`I2_cookie_only`) | 364/946 = 38.5% [35.4–41.6] | 299/578 = 51.7% [47.7–55.8] | 344/920 = 37.4% [34.3–40.6] |
| I2 chuẩn protocol (3P cookie + 3P URL ≥2 req) | 452/946 = 47.8% [44.6–51.0] | 358/578 = 61.9% [57.9–65.8] | 431/920 = 46.8% [43.6–50.1] |
| I2 mở rộng F10 (+ 1P→3P cookie-sync) | 558/946 = 59.0% [55.8–62.1] | 418/578 = 72.3% [68.5–75.8] | 534/920 = 58.0% [54.8–61.2] |
| I3 chỉ đếm cookie 3P (`I3_cookie_only`) | 202/946 = 21.4% [18.9–24.1] | 175/578 = 30.3% [26.7–34.1] | 185/920 = 20.1% [17.6–22.8] |
| I3 chuẩn protocol (quảng cáo) | 282/946 = 29.8% [27.0–32.8] | 248/578 = 42.9% [38.9–47.0] | 261/920 = 28.4% [25.6–31.4] |
| I3 mở rộng F10 (+ 1P→3P cookie-sync) | 345/946 = 36.5% [33.5–39.6] | 303/578 = 52.4% [48.3–56.5] | 321/920 = 34.9% [31.9–38.0] |
| I4 chỉ đếm cookie 3P (`I4_cookie_only`) | 96/946 = 10.1% [8.4–12.2] | 78/578 = 13.5% [10.9–16.5] | 87/920 = 9.5% [7.7–11.5] |
| I4 chuẩn protocol (analytics) | 295/946 = 31.2% [28.3–34.2] | 244/578 = 42.2% [38.3–46.3] | 277/920 = 30.1% [27.2–33.2] |
| I4 mở rộng F10 (+ GA4/1P→3P cookie-sync) | 484/946 = 51.2% [48.0–54.3] | 375/578 = 64.9% [60.9–68.7] | 462/920 = 50.2% [47.0–53.4] |

## 3. Độ nhạy cách đọc pháp lý Q-A: H (chỉ entity có tài khoản liên kết danh tính) vs R

Tập entity có hệ sinh thái tài khoản người dùng (cách đọc H): ByteDance Ltd., Facebook, Inc., Google LLC, Microsoft Corporation, VNG Corporation.

| Tầng khung | I2 chuẩn (R) | I2 cách đọc H | I2 mở rộng F10 (R) | I2 mở rộng F10 (H) |
|---|---|---|---|---|
| vn | 358/578 = 61.9% [57.9–65.8] | 341/578 = 59.0% [54.9–62.9] | 418/578 = 72.3% [68.5–75.8] | 409/578 = 70.8% [66.9–74.3] |
| nonvn | 21/26 = 80.8% [62.1–91.5] | 21/26 = 80.8% [62.1–91.5] | 24/26 = 92.3% [75.9–97.9] | 24/26 = 92.3% [75.9–97.9] |
| gov | 38/175 = 21.7% [16.2–28.4] | 33/175 = 18.9% [13.8–25.3] | 67/175 = 38.3% [31.4–45.7] | 63/175 = 36.0% [29.3–43.3] |
| edu | 35/167 = 21.0% [15.5–27.7] | 35/167 = 21.0% [15.5–27.7] | 49/167 = 29.3% [23.0–36.6] | 49/167 = 29.3% [23.0–36.6] |
| **Tất cả** | 452/946 = 47.8% [44.6–51.0] | 430/946 = 45.5% [42.3–48.6] | 558/946 = 59.0% [55.8–62.1] | 545/946 = 57.6% [54.4–60.7] |

## 4. RQ3: Trụ sở pháp nhân (`entity_hq.json`) vs Vị trí máy chủ (DB-IP Lite 2026-11, F13)

- Độ phủ trụ sở pháp nhân trên luồng định danh chuẩn protocol: **2273/2391 = 95.1%** (chưa rõ: 118/2391 = 4.9%, 92 entity đuôi dài).
- Site có ≥ 1 luồng định danh tới pháp nhân nước ngoài (unknown=VN): 434/946 = 45.9% [42.7–49.1]
- Site có ≥ 1 luồng định danh tới pháp nhân nước ngoài (unknown=foreign): 445/946 = 47.0% [43.9–50.2]
- **Định vị IP máy chủ (DB-IP Lite 2026-11, CC BY 4.0):** tra được IP cho 2383/2391 luồng định danh (99.7%).
  - Site có ≥ 1 luồng định danh đi tới IP máy chủ ngoài VN: 440/946 = 46.5% [43.4–49.7] (so với trụ sở pháp nhân ngoài VN: 434/946 = 45.9% [42.7–49.1]).
  - Phân bố quốc gia IP của luồng định danh (top 10): US: 1219, VN: 369, SG: 356, CA: 279, HK: 238, JP: 105, NL: 31, DE: 21, FR: 17, RU: 10
  - **Mâu thuẫn trụ sở vs IP (anycast/CDN, F13):**
    - Pháp nhân nước ngoài nhưng IP chỉ ở VN (edge nội địa): 132/2383 (5.5%) luồng.
    - Pháp nhân VN nhưng IP ngoài VN (cloud/CDN nước ngoài): 19/2383 (0.8%) luồng.
  - Lưu ý: crawler không ghi TCP RTT riêng lẻ nên độ lệch anycast đo trực tiếp qua chênh giữa `entity_hq` và DB-IP.

## 5. Độ hội tụ giữa bộ phân loại Disconnect+VN_SUPP và EasyPrivacy/EasyList (F16)

Quy tắc domain tổng quát trích từ `easyprivacy.txt` (47461 domain) và `easylist.txt` (48029 domain), bản 22/11/2026.

| Mức đối chiếu | So sánh | Đồng thuận | Cohen's κ | PABAK | Chỉ Disconnect | Chỉ EasyList/EP |
|---|---|---|---|---|---|---|
| Mức luồng (n=2391) | Tracker (ads/analytics/social) vs EP+EL | 84.1% | 0.642 | 0.682 | 335 | 45 |
| Mức luồng (n=2391) | Quảng cáo (`ads`) vs EasyList | 83.8% | 0.671 | 0.675 | 363 | 25 |
| Mức site (n=946) | Có tracker định danh vs EP+EL | 97.1% | 0.941 | 0.943 | 26 | 1 |
| Mức site (n=946) | Có quảng cáo định danh (`I3`) vs EasyList | 98.1% | 0.954 | 0.962 | 17 | 1 |

## 6. Sai số chuẩn theo cụm (Cluster-Robust SE, Protocol §4 & F9)

- Định nghĩa cụm ngoại sinh (quản trị chung): nối hai site khi dùng chung **GTM container** (4 container dùng chung) hoặc **mẫu chính sách SimHash** (Hamming ≤ 6 bit). Tổng: **928 cụm** trên 946 site (9 cụm có ≥ 2 site, gồm 27 site).
- Lý do không gom cụm theo bên nhận quảng cáo (ví dụ mọi site có Google Ads vào 1 cụm): cách gom đó nội sinh với biến kết quả I2/I3 nên sẽ thổi phồng phương sai giả tạo.

| Chỉ số & tập | Tỷ lệ | KTC 95% Wilson (độc lập) | KTC 95% Cluster-Robust | Số cụm (G) | DEFF |
|---|---|---|---|---|---|
| I2 — Tất cả (n=946) | 47.8% | [44.6–51.0] | [44.5–51.0] | 928 | 1.04 |
| I3 — Tất cả (n=946) | 29.8% | [27.0–32.8] | [26.8–32.8] | 928 | 1.06 |
| I2 — Tầng `vn` (n=578) | 61.9% | [57.9–65.8] | [57.9–65.9] | 569 | 1.03 |
| I3 — Tầng `vn` (n=578) | 42.9% | [38.9–47.0] | [38.8–47.0] | 569 | 1.02 |
| I2_ext — Tất cả (n=946) | 59.0% | [55.8–62.1] | [55.8–62.2] | 928 | 1.04 |
| I3_ext — Tất cả (n=946) | 36.5% | [33.5–39.6] | [33.3–39.6] | 928 | 1.07 |
| I4_ext — Tất cả (n=946) | 51.2% | [48.0–54.3] | [47.9–54.4] | 928 | 1.05 |

## 7. Gom cụm mẫu chính sách dùng chung bằng SimHash 64-bit (F15)

- Chính sách hợp lệ có SimHash: 331 → gom thành **316 cụm mẫu độc lập** (ngưỡng Hamming ≤ 6/64 bit).
- Số site thuộc cụm dùng chung (≥ 2 site cùng mẫu): **23/331 (6.9%)** trải trên 8 cụm.
- Top 10 cụm mẫu chính sách dùng chung:
  1. **n=8** (PDPL=0): EDU-f5a53c18be, EDU-c9dde478d0, EDU-1951a64a6d, EDU-338dae0bd1, EDU-2591f47880, EDU-df41c0cff7, EDU-f96b4ec573, EDU-1c540c05c9
  2. **n=3** (PDPL=3): NONVN-d80a9d758d, NONVN-79c3c220b5, VN-f82a0ab871
  3. **n=2** (PDPL=0): VN-6fa1649a87, VN-182be427ae
  4. **n=2** (PDPL=0): VN-0a6afc6a26, VN-925dacb02c
  5. **n=2** (PDPL=2): VN-926004c1bf, VN-2b93512495
  6. **n=2** (PDPL=0): VN-3c1486786a, VN-7678f367ec
  7. **n=2** (PDPL=1): VN-654d7ee5ae, VN-c6134574ec
  8. **n=2** (PDPL=2): VN-e2f043bd40, VN-244cb7eb49

| Chỉ số RQ4 (trên chính sách hợp lệ) | Tỷ lệ | KTC 95% Wilson | KTC 95% theo cụm SimHash | Số cụm | DEFF |
|---|---|---|---|---|---|
| Viện dẫn PDPL (`LAW_PDPL`) (n=331) | 11.2% | [8.2–15.0] | [7.4–15.0] | 316 | 1.26 |
| Chỉ viện dẫn NĐ 13/2023 (n=331) | 7.3% | [4.9–10.6] | [4.4–10.1] | 316 | 1.01 |
| Nhắc chuyển ra nước ngoài (`XBORDER`) (n=331) | 16.3% | [12.7–20.7] | [12.0–20.6] | 316 | 1.17 |
| Có I3 nhưng không nhắc bên thứ ba/quảng cáo (n=196) | 29.1% | [23.2–35.8] | [22.6–35.5] | 192 | 1.03 |
| Có I3 nhưng không nhắc cookie (n=196) | 45.4% | [38.6–52.4] | [38.3–52.5] | 192 | 1.05 |

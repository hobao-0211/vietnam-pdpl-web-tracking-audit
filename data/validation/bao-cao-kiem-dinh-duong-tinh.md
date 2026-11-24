# Báo cáo kiểm định toàn diện các tập dương tính trọng yếu (24/11/2026)

> Tài liệu nội bộ tổng hợp kết quả rà soát trực quan 100% ảnh chụp màn hình và 100% đoạn trích câu khớp của toàn bộ các tập dương tính trọng yếu trong Wave 1 (`n = 946` site đo được). Số liệu chính trong bài vẫn giữ nguyên đầu ra tất định theo protocol đã ghim; báo cáo này cung cấp độ chính xác (positive precision) đã xác minh và bóc tách các chế độ lỗi cụ thể cho Mục 5.3, Mục 5.5, Mục 5.6 và Bảng 9.
> Lưu ý đạo đức F20: không trích tên miền thật của website kiểm toán vào bản thảo tiếng Anh/tiếng Việt.

## 1. Kiểm định trực quan 39/39 ảnh chụp nhóm Banner & Nút từ chối (`data/crawl/main/shots/*.jpg`)

| Phân nhóm tự động | Số site | Xác minh trực quan trên ảnh chụp | Độ chính xác dương tính | Ghi chú cấu trúc & dark pattern |
|---|---:|---|---:|---|
| `banner_any = 1` (gộp `banner_block` ∨ `cmp_script`) | 34 | **29** banner cookie/quyền riêng tư hiển thị thật; **4** script CMP ẩn theo vùng địa lý VN (`cmp_script=1, banner_block=0`, không thấy banner trên ảnh); **1** hộp kiểm form tư vấn/ưu đãi (`banner_block` dương tính giả) | **29/34 (85,3%)** cho banner hiển thị (33/34 = 97,1% nếu tính hiện diện script CMP) | 1 trang trong số này (`C2` tự động) thực tế hiển thị đủ nút `TỪ CHỐI` + `ĐỒNG Ý TẤT CẢ` (`C3`), bộ dò nút tự động bỏ sót |
| `reject_btn = 1` nhưng `banner_any = 0` | 5 | **4** banner cookie thật có sẵn **3 nút gạt bật sẵn (`C5` dark pattern)** (bị `banner_block` bỏ sót do kích thước thẻ lớn/khác chuẩn; 1 trang bị popup khuyến mãi che mặt trước gây lỗi timeout khi bấm); **1** popup xin quyền gửi thông báo trình duyệt (không phải cookie) | **4/5 (80,0%)** là banner cookie thật (`C5`) | Bổ sung phát hiện trực diện cho Điều 6(3) NĐ 356/2025 (cấm mặc định đồng ý) |
| **Tổng hợp 39 ca dương tính** | **39** | **33/946 (3,5%)** site có banner cookie/quyền riêng tư hiển thị thật trên màn hình | — | Trong 33 banner hiển thị: có ít nhất **4 ca `C5` xác nhận rõ nút gạt bật sẵn** (3 site cùng cụm mẫu 3 nút gạt + 1 nhà thuốc 2 nút gạt) và 1 ca mẫu tương tự bị modal khuyến mãi che |
| **Profile C (nhóm bấm thành công `click_ok=True`)** | 21 | **20/21** là banner cookie thật (17 thuộc `banner_block=1` + 3 thuộc `C5` có nút gạt bật sẵn); chỉ **1/21** là popup thông báo trình duyệt | **20/21 (95,2%)** | Sau bấm từ chối: **7/17 (41,2%)** theo bộ lọc `banner_block` chặt và **8/20 (40,0%)** trên toàn bộ 20 banner cookie xác minh trực quan vẫn phát luồng quảng cáo mang định danh (`I8`) |

## 2. Kiểm định 100% đoạn trích câu khớp của các nhóm chính sách trọng yếu (`n = 331` chính sách hợp lệ)

| Chỉ số RQ4 | Số khớp tự động | Xác minh 100% nguyên văn câu khớp | Độ chính xác dương tính | Tỷ lệ thực xác minh (/331) | Nguyên nhân dương tính giả (nếu có) |
|---|---:|---|---:|---:|---|
| `LAW_PDPL` | 37 | **32** viện dẫn trực tiếp Luật BVDLCN 91/2025/QH15 (hoặc Đ.19/NĐ 356 đi kèm); **4** cụm chung *"pháp luật bảo vệ DLCN hiện hành"*; **1** mẫu toàn cầu dịch tiếng Việt trích Luật BVDLCN số 30/2018 của **Bahrain** | **32/37 (86,5%)** | **9,7%** (so với 11,2% tự động) | Nhánh regex `luat bao ve du lieu ca nhan` không loại tiền tố `phap ` và tên luật nước ngoài dịch sang tiếng Việt |
| `DEC_356` | 22 | **22/22** trích đích danh `356/2025/NĐ-CP` (trong đó có chính sách viện dẫn trực tiếp **Đ.4(1)(l) NĐ 356** về dữ liệu hành vi nhạy cảm) | **22/22 (100,0%)** | **6,6%** | Không có dương tính giả |
| `DEC_13`-only | 24 | **24/24** trích đích danh `13/2023/NĐ-CP` và không nhắc PDPL hay NĐ 356 | **24/24 (100,0%)** | **7,3%** | Không có dương tính giả |
| `ADNAME` | 17 | **17/17** nêu đích danh hãng/nền tảng adtech (`DoubleClick`, `Google Ads/AdSense`, `Facebook/Meta Pixel`, `TikTok Pixel`) | **17/17 (100,0%)** | **5,1%** | Không có dương tính giả |
| `ADPART` | 32 | **31/32** công bố đối tác quảng cáo / tiếp thị lại / quảng cáo cá nhân hóa; **1** ca phủ định đặt sau từ khóa (*"quảng cáo cá nhân hóa đã được tắt"*) | **31/32 (96,9%)** | **9,4%** | Phủ định hậu vị (*"đã được tắt"*) ngoài cửa sổ phủ định 60 ký tự phía trước |
| `XBORDER` | 54 | **50/54** công bố chuyển/lưu trữ dữ liệu cá nhân ra nước ngoài; **4** ca biên (1 giới hạn vùng phát video *"ngoài lãnh thổ được cấp quyền"*, 1 *"giao dịch xuyên biên giới"* ngân hàng, 2 đề mục *"7. Chuyển dữ liệu ra nước ngoài"* khớp AFF trước câu phủ định ngay sau) | **50/54 (92,6%)** | **15,1%** | Khớp tiêu đề mục trước mệnh đề phủ định; đa nghĩa cụm *"ngoài lãnh thổ"* / *"xuyên biên giới"* |
| `DPO` | 24 | **23/24** công bố đầu mối DPO / Bộ phận bảo vệ DLCN của chính đơn vị; **1** liên kết chính sách nhà cung cấp LMS bên thứ ba | **23/24 (95,8%)** | **6,9%** | Trang chính sách nhúng của bên cung cấp phần mềm LMS |
| `NEG_ONLY` (mâu thuẫn mạnh) | 5 | **3/5** cam kết phủ định rộng không bán/tiết lộ/chuyển giao thông tin khách hàng cho bất kỳ bên thứ ba nào; **2** ca hẹp phạm vi (chỉ thẻ thanh toán; miễn trừ link quảng cáo bên ngoài) | **3/5 (60,0%)** | — | Phạm vi mệnh đề phủ định hẹp hơn toàn bộ dữ liệu duyệt web |
| Chính sách thô bị loại | 32 | **32/32** xác nhận thực sự không phải chính sách hợp lệ của site (15 trang bên thứ ba/Google/Cloudflare/Microsoft/Mozilla/online.gov.vn; 9 redirect trang chủ; 5 bài tin tức; 3 trang lỗi/JSON/quá ngắn) | **32/32 (100,0%)** | — | Không loại nhầm chính sách hợp lệ nào |
| `GOV-01..06` có quảng cáo | 6 | **6/6** xác nhận lưu lượng định danh quảng cáo thật (4 chặt 3P + 2 đồng bộ 1P→3P) | **6/6 (100,0%)** | — | Không có dương tính giả |

## 3. Phạm vi giới hạn trung thực (đưa vào Mục 5.6 & Mục 7)
- Báo cáo trên xác minh **100% độ chính xác dương tính (precision)** của mọi tập dương tính trọng yếu và mọi ca bị loại.
- Tỷ lệ bỏ sót (false-negative rate / recall) trên 907 site âm tính banner và 583 site không tìm thấy chính sách chưa được đánh giá bằng hội đồng hai người mã hóa độc lập (nghiên cứu một tác giả); do đó tỷ lệ banner hiển thị (3,5% xác minh / 3,6% tự động) và độ phủ chính sách hợp lệ (35,0%) được diễn giải là **cận dưới thận trọng**. Hai gói mẫu phân tầng có seed cố định (`mau-kiem-tay-banner.tsv`, `n = 109`; `mau-kiem-tay-chinh-sach.tsv`, `n = 140`, seed `20261122`) được phát hành mở kèm tài liệu bổ sung S4 để cộng đồng độc lập tái lập.

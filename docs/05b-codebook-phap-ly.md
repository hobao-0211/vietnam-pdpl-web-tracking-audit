# Codebook pháp lý K7 (05b)

> **TRẠNG THÁI CHỐT (24/11/2026):** Đã chốt toàn bộ 7 lựa chọn mặc định `MĐ` cho `Q-A`–`Q-G` theo ủy quyền hoàn thiện của tác giả ngày 24/11/2026, đồng thời đã xác minh đầy đủ các định nghĩa luật liên quan (NĐ 147/2024/NĐ-CP Đ.3, Luật Viễn thông 24/2023/QH15 Đ.3(8), Luật Giáo dục đại học Đ.7(1), Luật Căn cước 26/2023/QH15 Đ.12(1), NĐ 13/2023/NĐ-CP Đ.2(3)(k) & Đ.13). Tác giả vẫn có thể điều chỉnh từng công tắc `H`/`R` ở §4 trước khi bấm Submit trên SuSy nếu muốn.
> Nguyên văn và bản dịch tiếng Anh không chính thức nằm ở `5/references/nguon-luat.md`, ký hiệu §x.y. Mọi trích dẫn tiếng Việt trong file đó đã được so bằng script với lớp chữ PDF Công báo (`/tmp/luat/`).
> Thang 4 bậc lấy từ `5/data/novelty/phan-bien-K7.md` mục 3:
> - **B0** Observed
> - **B1** Identifier-bearing third-party flow
> - **B2** Consent-relevant under PDPL
> - **B3** Prima facie inconsistent with Art. 28(8)(a)
>
> Không bao giờ dùng "vi phạm / violates / illegal / non-compliant" như một kết luận.

| Mức rủi ro | Blast radius | Đảo ngược | Độ tin cậy | Trạng thái |
|---|---|---|---|---|
| CRITICAL (claim pháp lý về site có tên thật) | Bài K7: Methods, Scope of Claims, Table ánh xạ | Codebook sửa được (HAI CHIỀU); toàn bộ site kiểm toán đã ẩn danh trong bài báo | Cao về nguyên văn (Công báo) và văn bản dẫn chiếu. Trung bình về cách đọc (chưa có thông tư hướng dẫn hay án lệ) | **Đã chốt bản mặc định `MĐ` (24/11/2026)** |

**TL;DR**
- Đã có nguyên văn chính thức (Công báo) cho toàn bộ PDPL và NĐ 356. Có ba điểm làm đổi khung phân tích so với `phan-bien-K7.md`:
  - **NĐ 356 Đ.4.1(l)** xếp "dữ liệu theo dõi hành vi … trên không gian mạng" vào nhóm **DLCN nhạy cảm**;
  - **PDPL Đ.11.1** đòi đồng ý **trước khi thu thập**, áp dụng chung, không riêng cho quảng cáo;
  - **NĐ 356 Đ.6.3** cấm "phương thức mặc định đồng ý".
- Cả PDPL lẫn NĐ 356 **không có** điều chung về nội dung bắt buộc của thông báo hay chính sách quyền riêng tư. Riêng Đ.29.6 có nghĩa vụ này, nhưng chỉ cho mạng xã hội và dịch vụ truyền thông trực tuyến. Vì vậy RQ4 ("nói–làm") nên báo dạng mô tả minh bạch, không gắn với một nghĩa vụ công bố cụ thể.
- Đ.28.8 và Đ.29 không được NĐ 356 hướng dẫn. Các cách đọc dưới đây dựa trên chữ của luật, chưa có văn bản hướng dẫn, quyết định thực thi hay án lệ nào.

---

## 1. Câu hỏi diễn giải

Mỗi câu gồm: điều khoản liên quan; cách đọc hẹp (H) và rộng (R); cách đọc đề xuất làm mặc định (MĐ); hệ quả cho chỉ số đo.

### Q-A. Cookie hoặc định danh trực tuyến có phải DLCN không?

**Điều khoản:**
- PDPL Đ.2.1 (§1.2): "xác định hoặc giúp xác định một con người cụ thể".
- PDPL Đ.2.11: khử nhận dạng là tạo ra dữ liệu "không thể giúp xác định".
- NĐ 356 Đ.3.11 (§2.2): "Các thông tin khác gắn liền với một con người cụ thể hoặc giúp xác định một con người cụ thể…".
- NĐ 356 Đ.3.10: "Thông tin về tài khoản số của cá nhân".
- NĐ 356 **Đ.4.1(l)** (§2.3): "Dữ liệu theo dõi hành vi, hoạt động sử dụng … các dịch vụ khác trên không gian mạng".
- NĐ 356 Đ.10.2 (§2.5): tiêu chí "có thể được sử dụng để xác định hoặc giúp xác định".

Không văn bản nào nêu đích danh cookie hay định danh trực tuyến là DLCN. Chữ "cookies" chỉ xuất hiện ở PDPL Đ.29.3, trong ngữ cảnh mạng xã hội.

**Cách đọc:**
- **H (hẹp):** chuỗi định danh ngẫu nhiên trong cookie, khi chưa gắn với tên, số điện thoại, email hay tài khoản đăng nhập, chưa "giúp xác định một con người cụ thể". Chỉ khi bên nhận liên kết được với danh tính (đăng nhập, khớp email đã băm, đồng bộ ID với nền tảng có tài khoản) thì mới là DLCN. Đ.4.1(l) chỉ áp dụng cho dữ liệu theo dõi đã là DLCN.
- **R (rộng):** "giúp xác định" là tiêu chí *khả năng*, khớp với chữ "có thể được sử dụng" ở NĐ 356 Đ.10.2. Một định danh bền vững, riêng cho từng trình duyệt, đi kèm URL trang, IP và dấu vân tay thiết bị, cho phép tách riêng (single out) và theo dõi một người qua nhiều site, nên "giúp xác định". Dữ liệu này cộng lịch sử duyệt web thuộc Đ.4.1(l), tức là **DLCN nhạy cảm**.

**MĐ (đề xuất, INFERRED):**
- Dùng R cho *luồng mang định danh bền vững* (B1), H cho *cookie nói chung*:
  - Luồng B1 tới bên thứ ba được coi là **có thể là DLCN theo cách đọc R** và đủ điều kiện xét lên B2.
  - Cookie không mang định danh khác nhau giữa hai profile sạch (cookie đồng ý, chống bot, cân bằng tải) **không** được coi là DLCN.
- Riêng nhãn "nhạy cảm" theo Đ.4.1(l): **không đưa vào chỉ số**. Chỉ nêu ở phần Discussion như hệ quả của cách đọc R. Lý do: hệ quả pháp lý lớn mà chưa có hướng dẫn. Chỗ này cần tác giả quyết định.
- Lý do chọn R cho luồng B1: chữ "giúp xác định" ở cả luật lẫn nghị định, cộng việc NĐ 356 đặt riêng một điểm về "dữ liệu theo dõi hành vi … trên không gian mạng", cho thấy nhà làm luật đã tính tới dữ liệu theo dõi trực tuyến.

**Hệ quả cho chỉ số:**
- Mọi câu ở bậc B2 phải có hậu tố "theo cách đọc R của Đ.2.1 (xem Legal Interpretation)".
- Phân tích độ nhạy theo H: chỉ đếm luồng tới entity có tài khoản người dùng hoặc khả năng liên kết danh tính (Google, Meta, TikTok, Zalo…). Danh sách entity "có khả năng liên kết" là ASSUMED, phải chốt trước.
- Nếu tác giả nhận Đ.4.1(l) theo R, có thêm chỉ số mô tả: "banner hoặc chính sách có báo dữ liệu là nhạy cảm không" (NĐ 356 Đ.6.4). Dự kiến gần như luôn là "không", và đây là một quan sát đáng nêu.

### Q-B. Phạm vi Đ.28.8: chỉ quảng cáo theo hành vi, hay rộng hơn?

**Điều khoản:**
- PDPL Đ.28.8 câu dẫn (§1.11): "Tổ chức, cá nhân khi sử dụng dữ liệu cá nhân để quảng cáo theo hành vi hoặc có mục tiêu cụ thể hoặc cá nhân hóa quảng cáo…"
- Điểm (a): "Chỉ được thu thập dữ liệu cá nhân thông qua việc theo dõi trang thông tin điện tử, cổng thông tin điện tử, ứng dụng khi có sự đồng ý…"
- Điểm (b): phương thức từ chối; thời gian lưu trữ; xoá.
- Khoản 1–7 dùng chủ thể khác: "Tổ chức, cá nhân **kinh doanh dịch vụ quảng cáo**".

**Hai trục cần tách:**
- (i) *Mục đích* nào thì thuộc khoản 8.
- (ii) *Chủ thể* nào bị ràng buộc.

**Cách đọc:**
- **H:**
  - (i) Chỉ việc thu thập để phục vụ quảng cáo theo hành vi, nhắm mục tiêu hoặc cá nhân hoá. Quảng cáo theo ngữ cảnh, analytics, chat, video nhúng và CDN không thuộc.
  - (ii) Chỉ bên trực tiếp "sử dụng DLCN để quảng cáo", tức là mạng quảng cáo hoặc DSP, cùng nhà quảng cáo. Website chỉ nhúng thẻ thì không phải chủ thể.
- **R:**
  - (i) Mọi việc "theo dõi trang thông tin điện tử" mà dữ liệu *có thể* được dùng cho quảng cáo cá nhân hoá. Ví dụ: GA4 bật Google Signals hoặc liên kết Google Ads; pixel chuyển đổi của Meta hay TikTok.
  - (ii) Cả website (bên kiểm soát quyết định nhúng thẻ, Đ.2.7) lẫn adtech (khoản 8 dùng "Tổ chức, cá nhân khi sử dụng", không giới hạn ở "kinh doanh dịch vụ quảng cáo").

**MĐ (đề xuất, INFERRED):**
- Trục (i): hẹp. Chỉ luồng tới entity có nhãn quảng cáo theo phân loại chốt trước được nối với 28.8(a). Đề xuất: Tracker Radar category `Advertising` / `Ad Motivated Tracking`, kèm danh sách adtech VN như admicro hay eclick do tác giả duyệt.
- Trục (ii): rộng. Câu trong bài mô tả hành vi *của trang*: "trang X để entity quảng cáo Y thu định danh trước khi có đồng ý". Không gán trách nhiệm riêng cho bên nào.
- Analytics không nối với 28.8. Analytics nối với Đ.9 và Đ.11.1 ở bậc B2.

**Hệ quả cho chỉ số:**
- B3 chỉ dành cho: luồng B1, tới entity quảng cáo, trước tương tác, và không có cơ chế đồng ý hiển thị trước luồng.
- Chữ "cổng thông tin điện tử" có trong Đ.28.8(a). Đây là thuật ngữ gắn với site cơ quan nhà nước, nên **tầng gov không được loại khỏi 28.8 vì lý do loại hình trang** (INFERRED).
- Phân tích độ nhạy: thêm GA4 có tín hiệu quảng cáo (request tới `googleads`/`doubleclick` cùng lượt tải) vào nhóm quảng cáo.

### Q-C. Đ.29 áp dụng cho loại chủ thể nào?

**Điều khoản:**
- PDPL Đ.29, câu dẫn (§1.12): "Tổ chức, cá nhân cung cấp dịch vụ mạng xã hội, dịch vụ truyền thông trực tuyến".
- Khoản 3 (cookies), khoản 4 ("không theo dõi"), khoản 6 (công khai chính sách bảo mật).
- PDPL không định nghĩa "mạng xã hội" hay "dịch vụ truyền thông trực tuyến". NĐ 356 không hướng dẫn Đ.29 (§2.1).
- Định nghĩa ở văn bản khác (Luật Viễn thông 2023, nghị định về dịch vụ Internet và thông tin trên mạng, Luật Báo chí): [CẦN KIỂM].

**Cách đọc:**
- **H:** chỉ nền tảng mạng xã hội (tài khoản người dùng, nội dung do người dùng tạo, tương tác) và dịch vụ liên lạc trực tuyến (OTT nhắn tin, gọi điện; khoản 5 nhắc "ghi âm cuộc gọi và đọc tin nhắn" ủng hộ cách hiểu này). Báo điện tử, site thương mại, cổng gov và edu không thuộc.
- **R:** "dịch vụ truyền thông trực tuyến" gồm mọi dịch vụ cung cấp nội dung trên mạng: báo điện tử, trang tin tổng hợp, nền tảng video hoặc stream, diễn đàn. Khi đó tầng báo chí cũng phải có lựa chọn từ chối cookie (29.3) và "không theo dõi" (29.4).

**MĐ (đề xuất, ASSUMED cho tới khi kiểm định nghĩa):**
- Dùng H. Đ.29 chỉ áp dụng cho tầng **nền tảng**: mạng xã hội, diễn đàn, nền tảng UGC hoặc video có tài khoản. Tầng này xác định bằng quy tắc chốt trước, ví dụ có giấy phép mạng xã hội ở footer: [CẦN KIỂM] cách dò.
- Tầng báo chí: chạy phân tích độ nhạy theo R, báo riêng.
- Lý do: khoản 5 cho thấy nhà làm luật nghĩ tới dịch vụ liên lạc. Báo chí có luật chuyên ngành riêng.

**Hệ quả cho chỉ số:**
- Với tầng nền tảng, thêm hai chỉ số Đ.29: có lựa chọn từ chối cookie (29.3) và có lựa chọn không theo dõi (29.4). Hai chỉ số này được lên B2.
- Đ.29.4 nói "chỉ được theo dõi hoạt động sử dụng mạng xã hội …". Phạm vi này là hoạt động *trên chính dịch vụ*, nên việc nhúng tracker bên thứ ba thì phải lập luận thêm. B3 không áp dụng cho Đ.29, vì thang B3 gắn riêng với 28.8(a).
- Nếu tác giả chọn R, tầng báo chí thêm các chỉ số 29.3, 29.4, 29.6. Rủi ro claim tăng, cần ghi rõ.

### Q-D. Ngoại lệ Đ.19 áp dụng cho tầng nào?

**Điều khoản:** PDPL Đ.19.1(a)–(đ) (§1.9). Đ.19.2 đòi bên xử lý không cần đồng ý phải có "cơ chế giám sát". Đ.10.1 loại các trường hợp Đ.19 khỏi quyền rút đồng ý.

**Cách đọc từng điểm:**

| Điểm | H | R | MĐ (đề xuất) |
|---|---|---|---|
| (a) bảo vệ tính mạng…; "bảo vệ quyền hoặc lợi ích chính đáng của mình … một cách cần thiết trước hành vi xâm phạm" | Chỉ tình huống cụ thể có hành vi xâm phạm (gian lận, tấn công) | Cookie chống bot hoặc DDoS (`__cf_bm`), chống gian lận thanh toán, áp cho mọi tầng | R **chỉ cho** luồng bảo mật kỹ thuật của chính site hoặc CDN bảo mật. Không bao giờ cho quảng cáo hay analytics. Nguyên văn đặt trách nhiệm chứng minh vào bên xử lý |
| (b) khẩn cấp, an ninh, phòng chống tội phạm | Không liên quan tracking web | — | Không áp dụng cho bất kỳ chỉ số nào |
| (c) "Phục vụ hoạt động của cơ quan nhà nước, hoạt động quản lý nhà nước theo quy định của pháp luật" | Chỉ xử lý mà cơ quan nhà nước cần để thực hiện nhiệm vụ *có căn cứ pháp luật*, và chủ thể xử lý là cơ quan nhà nước. Analytics bên thứ ba không phải "theo quy định của pháp luật" | Mọi xử lý trên cổng của cơ quan nhà nước, kể cả analytics để cải thiện dịch vụ công | **Gov:** analytics *có thể* thuộc (c) theo R. Vì vậy analytics trên gov dừng ở B1. Quảng cáo theo hành vi trên gov **không** thuộc (c): không có căn cứ hợp lý, nên vẫn lên được B3. **Edu công lập:** trường là đơn vị sự nghiệp công lập, không phải "cơ quan nhà nước" theo H. Đề xuất không áp (c) cho edu (INFERRED, [CẦN KIỂM] khái niệm "cơ quan nhà nước") |
| (d) "Thực hiện thỏa thuận của chủ thể … với cơ quan, tổ chức, cá nhân có liên quan theo quy định của pháp luật" | Chỉ xử lý cần để thực hiện thoả thuận *đã có* (tài khoản, hợp đồng), ví dụ cookie phiên đăng nhập | Mọi xử lý nêu trong "điều khoản sử dụng" mà người dùng mặc nhiên chấp nhận khi vào trang | H. Crawler là khách mới, chưa đăng nhập, chưa có thoả thuận, nên (d) **không** áp cho trạng thái trước tương tác ở mọi tầng. Ở tầng **gated**, (d) có thể áp cho cookie phiên và xác thực của chính site, không áp cho bên thứ ba quảng cáo. Theo R, "điều khoản mặc nhiên" đụng Đ.9.4(d) và NĐ 356 Đ.6.3; đề xuất bác R |
| (đ) "Trường hợp khác theo quy định của pháp luật" | Phải chỉ ra được luật cụ thể | — | Không áp, trừ khi tác giả tìm được luật cụ thể, ví dụ luật chuyên ngành báo chí hay giáo dục: [CẦN KIỂM] |

**Báo chí:** Đ.19 không có ngoại lệ nào cho hoạt động báo chí. Miễn trừ duy nhất liên quan là NĐ 356 Đ.17.3(a), và miễn trừ này chỉ miễn **TIA**, không miễn đồng ý (§2.6). MĐ: tầng báo chí xử lý như tầng thương mại về đồng ý.

**Hệ quả cho chỉ số:** xem ma trận §2.

### Q-E. Đ.20 áp dụng thế nào cho việc nhúng tracker của pháp nhân nước ngoài? Các trường hợp miễn

**Điều khoản:**
- PDPL Đ.20.1(a)–(c), 20.2 (TIA trong 60 ngày), 20.6 (miễn TIA) (§1.10).
- NĐ 356 Đ.17.1(a)–(c) và 17.3(a)–(đ) (§2.6).
- PDPL Đ.1.2(c): phạm vi áp dụng với pháp nhân nước ngoài.

**Mô tả kỹ thuật** (để tác giả đọc luật cho đúng): khi site nhúng thẻ của Google hay Meta, *trình duyệt của người dùng* gửi request thẳng tới máy chủ của pháp nhân nước ngoài. Site không tự gửi bản sao dữ liệu đang lưu tại VN. Trường hợp server-side tagging thì khác: máy chủ của site gửi đi.

**Cách đọc:**
- **H:**
  - Điểm (a) không khớp, vì dữ liệu không "đang lưu trữ tại Việt Nam".
  - Điểm (b) đòi "cơ quan, tổ chức, cá nhân tại Việt Nam chuyển". Với thẻ phía client, site không trực tiếp chuyển.
  - Pháp nhân nước ngoài tự thu thập, nên thuộc phạm vi luật theo Đ.1.2(c), nhưng không phải "chuyển xuyên biên giới" của site.
  - Đ.20 chỉ áp cho server-side tagging hoặc khi site gửi dữ liệu khách hàng (danh sách email, chuyển đổi offline) cho nền tảng nước ngoài.
- **R:**
  - Điểm (c) có chủ thể rộng: "Cơ quan, tổ chức, cá nhân tại Việt Nam **hoặc ở nước ngoài** sử dụng nền tảng ở ngoài lãnh thổ … để xử lý dữ liệu cá nhân được thu thập tại Việt Nam" (chữ đậm do người soạn nhấn mạnh).
  - Site dùng GA hay Meta Pixel là "sử dụng nền tảng ở ngoài lãnh thổ" để xử lý (phân tích, đo lường) dữ liệu thu tại VN. NĐ 356 Đ.17.1(c) nhắc lại: "chuyển đến nền tảng ở ngoài lãnh thổ … để tiếp tục xử lý".
  - Pháp nhân nước ngoài tự thu cũng thuộc (c), vì chủ thể "ở nước ngoài" cũng nằm trong câu chữ.
- **Miễn TIA** (chỉ miễn TIA, không miễn đồng ý):
  - PDPL 20.6(a): cơ quan nhà nước có thẩm quyền, liên quan tầng **gov**.
  - 20.6(b): dữ liệu người lao động trên đám mây, không liên quan.
  - 20.6(c): chủ thể tự chuyển. Có thể có người lập luận rằng trình duyệt của người dùng tự gửi, nên chủ thể "tự chuyển". Đề xuất **bác**, vì người dùng không chủ động chuyển.
  - NĐ 356 17.3(a) "Hoạt động báo chí, truyền thông theo quy định của pháp luật": H = chỉ dòng dữ liệu phục vụ tác nghiệp báo chí; R = mọi luồng của cơ quan báo chí, kể cả adtech.
  - 17.3(b) "Việc chuyển dữ liệu cá nhân xuyên biên giới đã được công khai theo quy định của pháp luật": H = dữ liệu được chuyển là dữ liệu đã công khai hợp pháp; R = việc chuyển đã được công bố công khai, ví dụ trong chính sách quyền riêng tư. **Theo R, việc chính sách có công bố chuyển ra nước ngoài trở thành điều kiện miễn TIA. Khi đó chỉ số RQ4 "chính sách có nói về chuyển ra nước ngoài không" có hệ quả pháp lý trực tiếp.** Tác giả cần quyết.

**MĐ (đề xuất, INFERRED):**
- Lấy R cho phạm vi 20.1(c), nhưng claim dừng ở **B2** cho mọi tầng (đúng thang của `phan-bien-K7.md` mục 3). Câu mẫu: "luồng mang định danh tới pháp nhân có trụ sở ở nước ngoài; nếu là DLCN theo cách đọc R của Đ.2.1 thì thuộc diện Đ.20.1(c); việc lập TIA không quan sát được".
- Gov: thêm "thuộc diện miễn TIA theo Đ.20.6(a)". Không nói gì về TIA.
- Báo chí: dùng H cho 17.3(a), nghĩa là adtech trên báo không được miễn TIA. Ghi rõ đây là cách đọc.
- 17.3(b): dùng H làm mặc định; nêu R trong Discussion như một hệ quả chính sách.
- **Không** dùng chữ "trái Điều 20" (F2).

**Hệ quả cho chỉ số:**
- "Nước ngoài" theo định nghĩa chính là trụ sở pháp nhân (F13), khớp chữ "tổ chức, cá nhân ở nước ngoài" ở 20.1(b) và "nền tảng ở ngoài lãnh thổ" ở 20.1(c).
- Định nghĩa phụ (vị trí máy chủ) khớp 20.1(a) và NĐ 356 17.1(a) "hệ thống máy chủ đặt ngoài lãnh thổ". Nên báo cả hai.

### Q-F. Thế nào là "đồng ý hợp lệ"? Banner chỉ có nút "OK", hoặc "tiếp tục duyệt = đồng ý", có đạt không?

**Điều khoản:**
- PDPL Đ.9.2: tự nguyện và biết rõ loại dữ liệu, mục đích, bên kiểm soát, quyền.
- Đ.9.3: rõ ràng, cụ thể, in hoặc sao chép được, kiểm chứng được.
- Đ.9.4: (a) từng mục đích; (b) không ép đồng ý mục đích khác; (d) "Sự im lặng hoặc không phản hồi không được coi là sự đồng ý".
- **Đ.11.1**: đồng ý **trước khi** thu thập.
- Đ.28.8(b): phương thức từ chối.
- NĐ 356 Đ.6.1: kiểm chứng được ai, khi nào, đồng ý gì. Điểm (d) "trên trang thông tin điện tử … có thiết lập kỹ thuật xin sự đồng ý".
- NĐ 356 Đ.6.2: lưu sự đồng ý; bên kiểm soát chịu nghĩa vụ chứng minh.
- **NĐ 356 Đ.6.3**: "không được thiết lập phương thức mặc định đồng ý hoặc tạo ra các chỉ dẫn không rõ ràng, gây hiểu lầm giữa đồng ý và không đồng ý".

**Phân loại cơ chế** (quan sát được, dùng làm biến mã hoá):

| Mã | Mô tả | H (khoan dung) | R (chặt) | MĐ (đề xuất) |
|---|---|---|---|---|
| C0 | Không có banner hay thông báo | Không có đồng ý | Không có đồng ý | Không có đồng ý |
| C1 | Thông báo, không có nút; hoặc "tiếp tục sử dụng nghĩa là đồng ý" | Có thể coi tiếp tục duyệt là hành vi chấp nhận | Tiếp tục duyệt là "không phản hồi" với banner (9.4(d)), đồng thời là "mặc định đồng ý" (NĐ 356 6.3) | **Không đạt**. Căn cứ chữ khá trực tiếp, đề xuất gắn nhãn CONFIRMED về chữ và INFERRED về áp dụng |
| C2 | Chỉ có nút "OK", "Đồng ý" hoặc "Tôi hiểu", không có nút từ chối | Bấm nút là hành vi chủ động, rõ ràng | Không có lựa chọn thì không "tự nguyện" (9.2). Không phân theo "từng mục đích" (9.4(a)). Với quảng cáo, thiếu "phương thức … từ chối" (28.8(b)) | **Không đạt cho quảng cáo** (28.8(b) là chữ rõ). Với analytics: "chưa chắc đạt", báo riêng |
| C3 | Có nút chấp nhận và nút từ chối ngang hàng ở lớp đầu | Đạt | Đạt nếu nêu đủ thông tin theo 9.2 và theo từng mục đích | Có thể đạt về hình thức. Chất lượng thông tin là biến riêng |
| C4 | Tuỳ chỉnh theo mục đích, ô chưa tick sẵn | Đạt | Đạt | Có thể đạt về hình thức |
| C5 | Ô tick sẵn hoặc nút đồng ý nổi bật, từ chối bị ẩn | Có thể đạt | "Mặc định đồng ý" hoặc "chỉ dẫn … gây hiểu lầm" (NĐ 356 6.3) | Gắn cờ "có dấu hiệu chỉ dẫn gây hiểu lầm". Mã hoá bằng tay, cần quy tắc chốt trước |

**Nguyên tắc thời điểm (MĐ):** bất kể mã C nào, **luồng xảy ra trước tương tác thì xảy ra trước đồng ý** (Đ.11.1 "trước khi thu thập"). Vì vậy câu hỏi "banner có hợp lệ không" chỉ thêm thông tin, không cứu được luồng trước tương tác.

**Giới hạn phải nêu (L7):** người dùng cũ có thể đã đồng ý trước đó, kể cả theo NĐ 13 và được giữ theo PDPL Đ.39.1. Phép đo chỉ nói về *khách mới, profile sạch*.

**Hệ quả cho chỉ số:**
- Biến `consent_mech ∈ {C0..C5}` do bộ dò gán, rồi kiểm định như F12.
- B3 đòi "không có cơ chế đồng ý hiển thị trước luồng". MĐ: luồng trước tương tác thoả điều kiện này với mọi mã C.
- RQ2 (sau khi bấm từ chối) chỉ áp cho C3–C4.

### Q-G. Chính sách quyền riêng tư phải công bố những gì?

**Điều khoản:**
- PDPL và NĐ 356 **không có điều chung** về nội dung bắt buộc của chính sách hay thông báo quyền riêng tư (§1.7, §2.9).
- Các căn cứ rải rác:
  - PDPL Đ.4.1(a): quyền được biết.
  - PDPL Đ.9.2: thông tin phải biết rõ thì đồng ý mới có hiệu lực (loại dữ liệu, mục đích, bên kiểm soát, quyền và nghĩa vụ).
  - PDPL Đ.3.2–3: mục đích cụ thể; thời hạn lưu trữ phù hợp.
  - PDPL Đ.28.8(b): phương thức từ chối; thời gian lưu trữ.
  - PDPL **Đ.29.6**, chỉ cho chủ thể của Đ.29: "Công khai chính sách bảo mật, giải thích rõ cách thức thu thập, sử dụng và chia sẻ … bảo vệ dữ liệu cá nhân của công dân Việt Nam khi chuyển dữ liệu xuyên biên giới".
  - NĐ 356 Đ.5.1: chủ thể được biết thủ tục thực hiện quyền.
  - NĐ 356 Đ.6.4: báo khi dữ liệu là nhạy cảm.
  - NĐ 356 Đ.10.3: xử lý tự động.
  - NĐ 356 Đ.15.3, 16.3: công khai thông tin DPO *thuê ngoài*.
  - NĐ 356 Đ.23.7: chủ thể phải biết tổ chức cung cấp dịch vụ xử lý.
  - NĐ 356 Đ.8.2: chỉ cho ngành tài chính; có "các bên thu thập, chia sẻ".

**Cách đọc:**
- **H:** chính sách quyền riêng tư không phải hình thức bắt buộc, trừ chủ thể của Đ.29. Không có nghĩa vụ chữ nào buộc kê tên bên thứ ba hay nói về chuyển ra nước ngoài, trừ Đ.29.6 với chủ thể Đ.29. "Không nhắc" chỉ là sự kiện mô tả.
- **R:** chính sách là phương tiện chính để đáp ứng Đ.4.1(a) và Đ.9.2. Nếu site dựa vào đồng ý, nội dung mà chủ thể phải "biết rõ" gồm loại dữ liệu, mục đích, bên kiểm soát, quyền. Với luồng tới adtech, bên thứ ba có thể là bên kiểm soát độc lập, nên tên của họ cũng thuộc "bên kiểm soát" phải biết (INFERRED). Chuyển ra nước ngoài thì liên quan Đ.29.6 (theo R ở Q-C) và NĐ 356 17.3(b) (theo R ở Q-E).

**MĐ (đề xuất):**
- RQ4 báo dạng **mô tả minh bạch "nói–làm"**: "chính sách không đề cập [X] dù [X] được quan sát". Không gắn B2 hay B3 cho tầng ngoài Đ.29.
- Bảng danh mục nội dung đề xuất mã hoá, mỗi mục ghi căn cứ:

| Mục mã hoá | Căn cứ gần nhất | Loại căn cứ |
|---|---|---|
| P1 Loại dữ liệu thu thập | PDPL 9.2(a); 29.1 | Điều kiện hiệu lực của đồng ý; nghĩa vụ riêng của nền tảng |
| P2 Mục đích | PDPL 3.2, 9.2(a), 9.4(a) | Nguyên tắc; điều kiện đồng ý |
| P3 Danh tính bên kiểm soát | PDPL 9.2(b) | Điều kiện đồng ý |
| P4 Cookie hoặc công nghệ theo dõi | PDPL 29.3 (nền tảng); 28.8(a) | Nền tảng; quảng cáo |
| P5 Bên thứ ba hoặc đối tác nhận dữ liệu | PDPL 29.6 "chia sẻ" (nền tảng); NĐ 356 23.7 | Gián tiếp |
| P6 Đối tác quảng cáo, quảng cáo cá nhân hoá | PDPL 28.3, 28.8 | Quảng cáo |
| P7 Chuyển ra nước ngoài | PDPL 29.6 (nền tảng); NĐ 356 17.3(b) theo R | Gián tiếp |
| P8 Quyền rút đồng ý và cách làm | PDPL 4.1(b), 9.2(c); NĐ 356 5.1 | Quyền; thủ tục |
| P9 Cách từ chối hoặc opt-out quảng cáo | PDPL 28.3, 28.5, 28.8(b) | Quảng cáo |
| P10 Thời gian lưu trữ | PDPL 3.3, 28.8(b) | Nguyên tắc; quảng cáo |
| P11 Liên hệ DPO hoặc bộ phận bảo vệ DLCN | NĐ 356 15.3, 16.3 (chỉ khi thuê ngoài) | Gián tiếp |
| P12 Văn bản được viện dẫn (PDPL, NĐ 356, NĐ 13) | NĐ 356 Đ.42.2 (NĐ 13 hết hiệu lực từ 01/01/2026) | Sự kiện. Viện dẫn NĐ 13 không phải là "sai" |

**Hệ quả cho chỉ số:**
- Mỗi mục P có ba trạng thái (F15): không tìm thấy chính sách / tìm thấy, không nhắc / có nhắc. "Có nhắc" tách tiếp thành khẳng định / phủ định / có điều kiện (§3).
- Riêng P12: "chỉ viện dẫn NĐ 13" là sự kiện mô tả, được phép nói: "viện dẫn văn bản đã hết hiệu lực từ 01/01/2026". **Không** suy ra "không tuân thủ". PDPL Đ.39.1 còn giữ hiệu lực cho các đồng ý đã lấy theo NĐ 13.

---

## 2. Ma trận chỉ số × điều khoản × ngoại lệ Đ.19 × tầng mẫu

Mỗi ô ghi **bậc cao nhất được phép nói** theo MĐ ở §1; nếu đổi theo cách đọc khác thì ghi trong ngoặc. Ký hiệu:
- "—" = chỉ số không áp dụng cho tầng đó;
- "Mô tả" = chỉ được báo sự kiện, không gắn điều khoản;
- "(19c?)" = ngoại lệ Đ.19 có thể áp, nên bậc bị giữ thấp hơn.

**Tầng** (xác định tất định, xem F7–F9):
- **TM** thương mại;
- **BC** báo chí;
- **GOV** `gov.vn` và cổng TTĐT;
- **EDU** `edu.vn`;
- **GATED** cổng có ô mật khẩu hoặc trang `/login`.

Tầng **NT** (nền tảng mạng xã hội, theo Q-C) chỉ dùng cho các hàng Đ.29.

| # | Chỉ số (đo trên profile sạch, T giây đầu, không cử chỉ) | Điều khoản nối | Ngoại lệ Đ.19 cần xét | TM | BC | GOV | EDU | GATED |
|---|---|---|---|---|---|---|---|---|
| I1 | Có request tới host khác pháp nhân | — | — | B0 | B0 | B0 | B0 | B0 |
| I2 | Có luồng mang định danh bền vững tới bên thứ ba (khác nhau giữa 2 profile) | — | — | B1 | B1 | B1 | B1 | B1 |
| I3 | I2 với bên nhận là entity **quảng cáo** | PDPL 28.8(a); 11.1; 9 | (a) không; (c) không hợp lý cho quảng cáo; (d) không (chưa có thoả thuận) | **B3** | **B3** (không có ngoại lệ báo chí cho đồng ý) | **B3** (28.8(a) có chữ "cổng thông tin điện tử"; 19c không hợp lý) | **B3** | **B3** cho trang đích trước đăng nhập |
| I4 | I2 với bên nhận là **analytics hoặc đo lường** (không quảng cáo) | PDPL 11.1; 9; (Q-A cách đọc R) | (c) cho GOV; (d) cho GATED chỉ nếu cần cho dịch vụ; (a) không | B2 | B2 | **B1** (19c?) (B2 nếu tác giả chọn H cho 19c) | B2 (B1 nếu tác giả coi trường công là "cơ quan nhà nước") | B2 (bên thứ ba analytics không cần cho thoả thuận) |
| I5 | I2 với bên nhận là **chức năng** (chat, video nhúng, bản đồ, CAPTCHA, CDN bảo mật) | PDPL 11.1; 9 | (a) cho CAPTCHA/chống bot; (d) cho GATED | B1 (B2 cho video hoặc chat đặt ID bền vững trước khi người dùng bấm) | B1 (như TM) | B1 | B1 | B1 |
| I6 | Luồng B1 tới pháp nhân **trụ sở nước ngoài** | PDPL 20.1(b)(c); NĐ 356 17.1 | Đ.19 không liên quan TIA. Miễn TIA: 20.6(a) GOV; NĐ 356 17.3(a) BC (theo R) | B2 ("thuộc diện Đ.20; TIA không quan sát được") | B2 (ghi: miễn TIA nếu đọc 17.3(a) theo R) | B2 ("thuộc diện Đ.20.1; miễn TIA theo 20.6(a)") | B2 | B2 |
| I7 | Cơ chế đồng ý `C0–C5` (Q-F) | PDPL 9.2–9.4; NĐ 356 6.1–6.3; 28.8(b) | — | Mô tả, kèm nhận định "không đạt 9.4(d)/6.3 theo MĐ" cho C1; cho C2 với quảng cáo | như TM | như TM | như TM | như TM |
| I8 | Sau khi bấm **từ chối** (C3–C4), vẫn có luồng I3 | PDPL 28.8(a)(b); 9.4(d) | như I3 | **B3** | **B3** | **B3** | **B3** | **B3** |
| I9 | Sau khi bấm từ chối, vẫn có luồng I4 | PDPL 9; 10 | như I4 | B2 | B2 | B1 (19c?) | B2 | B2 |
| I10 | Banner hoặc chính sách báo dữ liệu là **nhạy cảm** (NĐ 356 6.4, nếu nhận Đ.4.1(l)) | NĐ 356 4.1(l), 6.4 | — | Mô tả (Discussion) | Mô tả | Mô tả | Mô tả | Mô tả |
| I11 | Chính sách: P1–P11 có hay không, ba trạng thái | §1 Q-G | — | Mô tả "nói–làm" | Mô tả | Mô tả | Mô tả | Mô tả |
| I12 | Chính sách viện dẫn văn bản (P12) | NĐ 356 42.2; PDPL 39 | — | Mô tả | Mô tả | Mô tả | Mô tả | Mô tả |
| I13 | **NT:** có lựa chọn từ chối cookie (29.3) / "không theo dõi" (29.4) / chính sách nêu cách chia sẻ (29.6) | PDPL 29.3, 29.4, 29.6 | (d) cho chức năng cốt lõi của tài khoản | Chỉ áp dụng cho NT: **B2** nếu thiếu lựa chọn. Tầng BC: B2 chỉ khi tác giả chọn R ở Q-C | | | | |

**Điều kiện cộng thêm cho mọi ô B2 và B3:**
1. Đạt độ tin cậy test–retest κ ≥ 0,6 (F14).
2. Câu viết phải nêu cách đọc đã dùng (Q-A R; Q-B; Q-D).
3. Ô B3 phải có cụm "subject to the limitations in Section X".

---

## 3. Từ điển "nói" (regex) để dò chính sách tiếng Việt — BẢN NHÁP

> Từ điển này là **bản nháp**. Phải chốt trước đợt phân tích, ghi vào bản đăng ký trước (OSF/Zenodo), và kiểm định bằng mẫu phân tầng như F12/F15 (khoảng 70 + 70 văn bản). Em đã chạy thử trên 10 câu tự viết, không chạy trên chính sách thật. Kết quả thử ở cuối mục.

### 3.1. Chuẩn hoá trước khi so khớp
Bỏ dấu để một mẫu bắt được cả văn bản có dấu lẫn không dấu. Đổi `Đ`/`đ` và `Ð`/`ð` thành `d`: chữ eth `Ð` (U+00D0) hay bị dùng nhầm cho `Đ` (U+0110) trong văn bản VN. Chuyển về chữ thường, gộp khoảng trắng.

```python
import re, unicodedata
def norm(s: str) -> str:
    s = unicodedata.normalize("NFC", s)
    s = s.replace("Đ", "D").replace("đ", "d").replace("Ð", "D").replace("ð", "d")
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", s.lower())
```

### 3.2. Mẫu (áp trên văn bản đã chuẩn hoá)

| Khoá | Ý nghĩa | Regex (Python, sau `norm`) | Ghi chú độ chính xác |
|---|---|---|---|
| `LAW_PDPL` | Viện dẫn PDPL | `91\s*/\s*2025\s*/\s*qh\s*-?\s*15\|luat\s+bao\s+ve\s+du\s+lieu\s+ca\s+nhan\|\bpdpl\b\|law\s+on\s+personal\s+data\s+protection` | Tên luật đủ đặc hiệu (chỉ có một luật mang tên này) |
| `DEC_356` | Viện dẫn NĐ 356 | `(?<!\d)356\s*/\s*2025\s*/\s*n\s*d\s*[-–‐]?\s*cp` | Bắt các dạng `356/2025/NĐ-CP`, `356/2025/ND-CP`, `356/2025/NĐCP`, có khoảng trắng |
| `DEC_13` | Viện dẫn NĐ 13 (hết hiệu lực) | `(?<!\d)13\s*/\s*2023\s*/\s*n\s*d\s*[-–‐]?\s*cp\|(?:nghi\s*dinh\|decree\|\bnd)\s*(?:so\s*\|no\.?\s*)?13(?![\d/])` | Nhánh thứ hai ("Nghị định 13", "NĐ 13") kém đặc hiệu hơn; gắn cờ `DEC_13_short`, kiểm tay |
| `COOKIE` | Cookie, công nghệ theo dõi | `\bcookies?\b\|tep\s+(?:tin\s+)?(?:du\s+lieu\s+)?(?:nho\|cookie)\|web\s*beacons?\|\bpixels?\b\|local\s*storage\|cong\s+nghe\s+theo\s+doi\|tracking\s+technolog` | `pixel` có thể dương tính giả (ảnh) |
| `THIRD` | Bên thứ ba, đối tác | `ben\s+thu\s+ba\|third[-\s]part(?:y\|ies)\|doi\s+tac\|nha\s+cung\s+cap\s+dich\s+vu` | `doi tac` rất rộng; nên báo riêng `ben thu ba` (chặt) và `doi tac` (lỏng) |
| `XBORDER` | Chuyển ra nước ngoài | `xuyen\s+bien\s+gioi\|ra\s+nuoc\s+ngoai\|ngoai\s+lanh\s+tho\|(?:may\s+chu\|server)\S*\s+(?:dat\s+)?(?:tai\|o)\s+nuoc\s+ngoai\|cross[-\s]border\|outside\s+(?:of\s+)?viet\s*nam\|transfer\w*(?:\s+\w+){0,3}\s+(?:abroad\|overseas)` | Bắt cả thuật ngữ cũ "ra nước ngoài" (NĐ 13; PDPL Đ.39.2) và mới "xuyên biên giới" |
| `ADPART` | Đối tác quảng cáo, quảng cáo cá nhân hoá | `(?:doi\s+tac\|nha\s+cung\s+cap\|mang)\s+quang\s+cao\|quang\s+cao\s+(?:theo\s+hanh\s+vi\|ca\s+nhan\s+hoa\|nham\s+(?:muc\s+tieu\|den)\|co\s+muc\s+tieu)\|re-?marketing\|re-?targeting\|tiep\s+thi\s+lai\|advertising\s+partners?\|interest-based\s+ad` | Nên bổ sung tên adtech (google ads, doubleclick, facebook pixel, meta pixel, tiktok pixel, admicro, eclick, criteo) thành khoá phụ `ADNAME` |
| `WITHDRAW` | Quyền rút đồng ý | `rut\s+(?:lai\s+)?(?:su\s+)?dong\s+y\|huy\s+(?:bo\s+)?(?:su\s+)?dong\s+y\|withdraw\w*\s+(?:your\s+\|the\s+)?consent` | |
| `DPO` | Liên hệ DPO hoặc bộ phận bảo vệ DLCN | `nhan\s+su\s+bao\s+ve\s+du\s+lieu\|bo\s+phan\s+bao\s+ve\s+du\s+lieu\|can\s+bo\s+bao\s+ve\s+du\s+lieu\|\bdpo\b\|data\s+protection\s+officer` | Chỉ tính "có liên hệ" khi trong cùng đoạn có email hoặc số điện thoại. Che giá trị trước khi lưu (F15) |

Trong bảng, dấu `\|` là ký tự `|` đã được escape cho Markdown. Khi copy vào code, bỏ dấu `\` đứng trước.

### 3.3. Xử lý phủ định và điều kiện (theo câu)
Tách câu theo `[.;!?]` hoặc xuống dòng. Với mỗi lần khớp:
- **COND** nếu trong câu có mẫu điều kiện: `\btru\s+(?:khi|truong\s+hop)\b|\bngoai\s+tru\b|\b(?:neu|khi)\s+(?:khong\s+)?(?:co|duoc)\s+(?:su\s+)?dong\s+y\b|\bunless\b|\bexcept\b|\bwith\s+your\s+consent\b`. Ví dụ: "không chia sẻ với bên thứ ba **trừ khi** có sự đồng ý".
- Ngược lại là **NEG** nếu trong 60 ký tự *trước* chỗ khớp có: `\bkhong\b(?!\s+chi\b)|\bchua\b|\bnever\b|\bnot\b|\bno\b|\bcam\s+ket\s+khong\b|\btuyet\s+doi\s+khong\b`. Mẫu loại "không chỉ … mà còn" vì đó không phải phủ định.
- Còn lại là **AFF**.

Cách tính cho mỗi chính sách × khoá:
- `AFF` nếu có ít nhất một lần khớp AFF;
- `NEG_ONLY` nếu mọi lần khớp đều là NEG;
- `COND` nếu có COND và không có AFF;
- `NONE` nếu không khớp lần nào.

"Nói–làm" chỉ so với `AFF`/`COND`. Trường hợp `NEG_ONLY` mà luồng vẫn được quan sát thì báo riêng, vì đây là mâu thuẫn mạnh nhất. Ví dụ: "không chia sẻ với bên thứ ba" trong khi quan sát được luồng tới adtech.

**Giới hạn đã biết:**
- Cửa sổ 60 ký tự dễ bắt nhầm chữ "không" của một mệnh đề khác trong cùng câu dài.
- Không xử lý phủ định kép.
- Không hiểu cấu trúc liệt kê ("chúng tôi không: (i) bán…; (ii) chia sẻ…").

Cần kiểm định trước khi dùng.

### 3.4. Kết quả chạy thử (10 câu tự viết, `python3 -I`, 22/11/2026)
- "…tuân thủ Nghị định 13/2023/NĐ-CP và Luật Bảo vệ dữ liệu cá nhân số 91/2025/QH15." → `LAW_PDPL` AFF ×2, `DEC_13` AFF. Đúng.
- "Theo Nghi dinh 356/2025/ND-CP, chúng tôi dùng cookie." → `DEC_356`, `COOKIE`. Đúng.
- "Chúng tôi không chia sẻ dữ liệu với bên thứ ba." → `THIRD` NEG. Đúng.
- "…không chỉ chia sẻ với bên thứ ba mà còn với đối tác quảng cáo." → `THIRD` AFF, `ADPART` AFF. Đúng.
- "…không chia sẻ với bên thứ ba trừ khi có sự đồng ý của bạn." → `THIRD` COND. Đúng.
- "…lưu trữ trên máy chủ đặt tại nước ngoài." → `XBORDER` AFF. Đúng.
- "theo Nghị định 13/2013" → không khớp. Đúng.
- "We may transfer data abroad." → **không khớp ở phiên bản thử**. Đã sửa mẫu `XBORDER`, thêm `transfer\w*(?:\s+\w+){0,3}\s+(?:abroad|overseas)` như trong bảng ở §3.2. Đã chạy lại với 5 câu: khớp "transfer data abroad", "transferred to servers overseas", "máy chủ đặt tại nước ngoài", "xuyên biên giới"; không khớp "không lưu trữ dữ liệu". Đúng như mong đợi.

---

## 4. Trạng thái chốt quyết định & nguồn đối chiếu (cập nhật 24/11/2026)

**Quyết định diễn giải (đã chốt bản mặc định `MĐ` vào bản thảo ngày 24/11/2026):**
- [x] **Q-A (Chốt `MĐ`):** Áp cách đọc rộng `R` của Đ.2.1 cho luồng mang định danh bền vững (`B1` → đủ điều kiện xét `B2`) kèm phân tích độ nhạy hẹp `H` trên 5 nền tảng liên kết tài khoản; giữ Đ.4.1(l) NĐ 356 (*dữ liệu theo dõi hành vi trên không gian mạng là DLCN nhạy cảm*) làm chỉ số mô tả (`SENSITIVE`) và phân tích chính sách ở Mục 6.2.
- [x] **Q-B (Chốt `MĐ`):** Trục (i) hẹp (chỉ pháp nhân `Advertising`/`Ad Motivated Tracking` trong Disconnect/Tracker Radar + danh sách adtech VN `vn_entities.json` nối với Đ.28.8(a); tách riêng `ADNAME` và `ANAME`; GA4 thuần giữ ở `I4` analytics); trục (ii) rộng (mô tả hành vi cấp trang, không gán lỗi pháp lý riêng cho chủ site hay mạng quảng cáo).
- [x] **Q-C (Chốt `MĐ`):** Áp cách đọc hẹp `H` cho Đ.29 (chỉ áp cho mạng xã hội theo **NĐ 147/2024/NĐ-CP Đ.3** — hệ thống cho phép người dùng cung cấp, trao đổi, tương tác, chia sẻ thông tin — và dịch vụ viễn thông cơ bản trên Internet/OTT theo **Luật Viễn thông 24/2023/QH15 Đ.3(8)**; không tự động gộp báo điện tử `BC` vào Đ.29, báo cáo tầng `BC` riêng).
- [x] **Q-D (Chốt `MĐ`):** Tầng `GOV`: giữ analytics `I4` ở trần `B1` do khả năng viện dẫn Đ.19.1(c), nhưng giữ quảng cáo hành vi `I3` ở trần `B3` (không có căn cứ quản lý nhà nước cho quảng cáo thương mại). Tầng `EDU`: theo **Luật Giáo dục đại học Đ.7(1)** và **Luật Viên chức**, trường đại học công lập là *đơn vị sự nghiệp công lập* cung cấp dịch vụ công chứ không phải *cơ quan nhà nước* thực hiện quyền lực hành chính nhà nước → không tự động áp ngoại lệ Đ.19.1(c) hay miễn TIA Đ.20.6(a) cho `EDU`. Điểm (d) chỉ áp cho cookie phiên/xác thực của chính site ở tầng `GATED`, bác cách đọc rộng "điều khoản mặc nhiên".
- [x] **Q-E (Chốt `MĐ`):** Áp cách đọc rộng `R` cho phạm vi Đ.20.1(c) ở trần `B2` (nhúng thẻ phía client gửi dữ liệu thu tại VN sang nền tảng ngoài lãnh thổ; TIA không quan sát được); `GOV` ghi chú miễn TIA theo Đ.20.6(a); `BC` đọc hẹp Đ.17.3(a) NĐ 356 (adtech thương mại không thuộc tác nghiệp báo chí); Đ.17.3(b) mặc định đọc hẹp `H`, phân tích hệ quả cách đọc rộng `R` ở Mục 6.2.
- [x] **Q-F (Chốt `MĐ`):** Thời điểm trước tương tác vi phạm điều kiện "trước khi thu thập" (Đ.11.1) bất kể mã `C0`–`C5`; `C1` không đạt Đ.9.4(d)/NĐ 356 Đ.6.3; `C2` không đạt cho quảng cáo (Đ.28.8(b)) và ghi "chưa chắc đạt" cho analytics; RQ2b chỉ đánh giá trên `C3`–`C4`.
- [x] **Q-G (Chốt `MĐ`):** Báo cáo RQ4 ở dạng **mô tả minh bạch "nói–làm"** trên tập con 331 chính sách hợp lệ, không gắn bậc `B2`/`B3` cho nghĩa vụ công bố (trừ nhận xét khung Đ.29.6).

**Nguồn đã đối chiếu bổ sung (24/11/2026):**
- [x] **NĐ 13/2023/NĐ-CP** (ban hành 17/04/2023, hiệu lực 01/07/2023, hết hiệu lực 01/01/2026 theo NĐ 356 Đ.42.2): **Đ.2(3)(k)** từng xếp *"dữ liệu cá nhân phản ánh hoạt động, lịch sử hoạt động trên không gian mạng"* vào nhóm *DLCN cơ bản* (nay NĐ 356 Đ.4(1)(l) nâng lên *DLCN nhạy cảm*), và **Đ.13** từng đặt nghĩa vụ chung *"Thông báo xử lý DLCN"* một lần trước khi xử lý (gồm mục đích, loại dữ liệu, cách thức, bên liên quan, hậu quả không mong muốn, thời gian bắt đầu/kết thúc) — giải thích trực tiếp vì sao nhiều chính sách cũ vẫn có mục "Thông báo xử lý DLCN" viện dẫn NĐ 13 trong khi PDPL/NĐ 356 bỏ danh mục thông báo ngang này.
- [x] **Luật Căn cước 26/2023/QH15 Đ.12(1):** *"Số định danh cá nhân"* (nhắc ở NĐ 356 Đ.3.7) là dãy 12 chữ số do CSDL quốc gia về dân cư cấp cho công dân — hoàn toàn tách biệt với định danh trực tuyến trong cookie; xác nhận việc neo `Q-A` vào PDPL Đ.2(1), NĐ 356 Đ.10(2) và Đ.4(1)(l) là chuẩn xác.
- [x] **NĐ 147/2024/NĐ-CP Đ.3 & Luật Viễn thông 24/2023/QH15 Đ.3(8):** Làm rõ ranh giới *mạng xã hội* và *dịch vụ viễn thông cơ bản trên Internet (OTT)* cho `Q-C`.
- [x] **Luật Giáo dục đại học Đ.7(1) & Luật Viên chức:** Xác nhận phân biệt *đơn vị sự nghiệp công lập* (trường đại học công lập) với *cơ quan nhà nước* cho `Q-D`.
- [x] **NĐ 330/2026 (xử phạt hành chính):** Chỉ nhắc khái quát ở Mục 7 rằng khung xử phạt hành chính triển khai muộn trong năm 2026; không trích số điều khoản chi tiết khi chưa có PDF Công báo gốc (giữ kỷ luật nguồn).

**Đã giải quyết so với `phan-bien-K7.md`:**
- F3: Đ.2.1 nay đã có nguồn chính thức. Danh mục DLCN cơ bản của NĐ 356 **không** có điểm riêng về hoạt động trên mạng; điểm đó đã được nâng lên danh mục **nhạy cảm** (Đ.4.1(l)) so với Đ.2(3)(k) NĐ 13/2023.
- F4: Đ.19.1(a)–(đ) nguồn chính thức khớp với bản thứ cấp lawplayer.
- F2: nghĩa vụ "thông báo" cụ thể của NĐ 356 mà F2 để [CẦN KIỂM] **không tồn tại** dưới dạng điều chung (thay đổi trực tiếp so với Đ.13 NĐ 13/2023; xem Q-G).

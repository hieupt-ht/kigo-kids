# Kigo — Tool lấy dữ liệu (thiết kế)

Ngày: 2026-11-24 · Trạng thái: bản nháp chờ duyệt

## 1. Mục đích và lý do

Kigo là app học tiếng Anh cho trẻ 6–10 tuổi, có linh vật là chú corgi Kigo và 12 con giáp. Trước khi làm app và video, cần một **kho dữ liệu nền** gồm:

1. **Phương pháp và chương trình dạy tiếng Anh cho trẻ**: phương pháp đang thịnh hành và có nghiên cứu ủng hộ, khung từ vựng/ngữ pháp theo cấp độ. Ưu tiên nguồn chính thống (Cambridge, Oxford, Khan Academy, cơ quan giáo dục, nghiên cứu học thuật).
2. **Nội dung Việt Nam**: truyện cổ tích, lịch sử, văn hoá đặc trưng, dễ hiểu với trẻ 6–10 tuổi.

Kho này dùng ngay để làm **20 video demo** (dự án riêng, làm sau), và lâu dài là nguồn cho rất nhiều video và bài học khác. Vì thế lần này **lấy đầy đủ nhất có thể**, không chỉ đủ cho 20 video.

## 2. Mục tiêu, không phải mục tiêu, phản mục tiêu

**Mục tiêu**
- Thu thập đầy đủ các nhóm dữ liệu ở mục 5, mỗi mục ghi rõ nguồn, link và giấy phép.
- Gắn nhãn giấy phép 3 mức cho từng mục (mục 4) để chủ dự án duyệt.
- Phân loại theo **phương pháp** và theo **nội dung/chủ đề**, để sau này lọc ra làm video.
- Kể lại truyện và nội dung Việt Nam bằng lời mới, hợp với trẻ 6–10 tuổi.
- Xuất ra một định dạng thống nhất, đưa lên Google Drive.

**Không phải mục tiêu (lần này)**
- Làm video, kịch bản video, thiết kế nhân vật. Đó là dự án sau.
- Chạy định kỳ hay tự động cập nhật xu hướng. Lần này chỉ chạy một lần, nhưng cấu trúc phải để sau này nâng lên được.
- Xây app, cơ sở dữ liệu hay giao diện web.

**Phản mục tiêu (làm ra mà dính những thứ này thì coi như hỏng)**
- Chứa nội dung chép nguyên văn từ nguồn có bản quyền mà lại gắn nhãn "dùng được".
- Mục dữ liệu không có nguồn hoặc không có nhãn giấy phép.
- Nội dung không phù hợp trẻ em (bạo lực chi tiết, đáng sợ quá mức, ...) mà không được đánh dấu.

## 3. Ràng buộc

- Chỉ dùng nội dung công khai. Không vượt tường đăng nhập, không phá chặn bot, tôn trọng robots.txt và điều khoản của trang.
- Khan Academy dùng giấy phép CC BY-NC-SA, cấm thương mại: chỉ tham khảo cách thiết kế, không lấy nội dung.
- Máy chủ dự án: Windows 11, làm việc trong Claude Code. Chưa có repo git và chưa có code.
- Phần chọn lọc, tóm tắt, kể lại do Claude làm ngay trong Claude Code, không gọi Claude API (không cần API key).

## 4. Nhãn giấy phép

| Nhãn | Nghĩa | Ví dụ |
|---|---|---|
| 🟢 `usable` | Dùng thương mại được, kể cả nội dung | Public domain, CC0, CC BY, Open Government Licence |
| 🟡 `reference` | Có bản quyền, nhưng lấy ý tưởng, phương pháp, khung chương trình hay sự kiện để tự viết lại thì được | Danh sách từ Cambridge, bài báo khoa học, sách hướng dẫn |
| 🔴 `excluded` | Cấm thương mại, hoặc không xác định được giấy phép | Khan Academy (NC), trang không ghi giấy phép |

- CC BY-SA (ví dụ Wikipedia) xếp 🟡: dùng làm nguồn tra cứu, nội dung đưa vào kho luôn là bản viết lại.
- Bản kể lại do Claude viết thì nhãn của bản kể là 🟢, nhưng vẫn giữ link tới nguồn gốc.
- Tool chỉ gắn nhãn sơ bộ. Mỗi mục có cột `reviewed` để chủ dự án duyệt tay.
- *(Quyết định của Claude)* **Từ vựng Cambridge**: từng từ tiếng Anh thông dụng không có bản quyền, nên danh sách từ (từ, loại từ, cấp, chủ đề) được dùng thẳng trong sản phẩm. Phần không chép là câu ví dụ, tranh minh hoạ, định dạng tài liệu và đề thi. File từ vựng ghi chú điều này.

## 5. Dữ liệu cần lấy (ước lượng vài trăm mục)

### 5A. Tiếng Anh: chương trình và phương pháp
| Nhóm | Nguồn chính | Ước lượng |
|---|---|---|
| Từ vựng theo cấp, chủ đề, ngữ pháp | Cambridge Pre A1 Starters / A1 Movers / A2 Flyers (wordlist và handbook công khai) | ~1.400–1.500 từ, ~20 chủ đề |
| Mô tả năng lực theo trình độ | CEFR (Council of Europe), bản cho trẻ em | Pre A1–A2 |
| Phonics | Letters and Sounds (Bộ Giáo dục Anh, kiểm tra giấy phép OGL) | ~44 âm, 6 giai đoạn |
| Phương pháp | Bài tổng quan và nghiên cứu (OpenAlex, ERIC, Semantic Scholar), British Council TeachingEnglish, Cambridge và Oxford (bài viết công khai) | ~10–15 phương pháp, ~50–100 bài nghiên cứu |
| Xu hướng | Google Trends, các app tiếng Anh trẻ em nổi bật (phân tích tính năng) | ~10 app, danh sách xu hướng |
| Cách thiết kế bài học | Khan Academy Kids, Khan Academy (chỉ mô tả cách làm) | 1 bản tổng hợp |

Mỗi **phương pháp** là một "thẻ phương pháp": tên, mô tả, hợp với độ tuổi nào, bằng chứng nghiên cứu, cách áp dụng trong video hoặc bài học, ví dụ hoạt động, nguồn.

### 5B. Việt Nam: truyện, lịch sử, văn hoá
| Nhóm | Nguồn chính | Ước lượng |
|---|---|---|
| Truyện cổ tích, truyền thuyết | Wikisource tiếng Việt (Lĩnh Nam chích quái, tuyển tập truyện cổ đã hết bản quyền), Wikipedia tiếng Việt để tra cứu | ~60–100 truyện |
| Lịch sử (**chỉ trước 1945**) | Wikipedia tiếng Việt, văn bản sử cũ trên Wikisource (Đại Việt sử ký toàn thư...) | ~30–50 nhân vật/sự kiện |
| Văn hoá | Wikipedia tiếng Việt và các nguồn chính thống | ~30–50 chủ đề (Tết, Trung thu, ẩm thực, trò chơi dân gian, áo dài, 12 con giáp...) |

Mỗi mục Việt Nam có: tóm tắt cốt truyện hoặc sự kiện, nhân vật, bài học rút ra, **bản kể lại cho trẻ 6–10 tuổi (tiếng Việt)**, một danh sách từ tiếng Anh liên quan (liên kết sang từ vựng Cambridge nếu có), độ nhạy cảm và ghi chú phù hợp lứa tuổi, nguồn.

**Đúng sự thật, không bịa (yêu cầu của chủ dự án)**
- Lịch sử chỉ lấy giai đoạn **trước 1945**, theo cách hiểu lịch sử chính thống của Việt Nam.
- Tách rõ **truyền thuyết** (Lạc Long Quân, Thánh Gióng...) và **sự kiện lịch sử** có ghi chép (Hai Bà Trưng năm 40, Ngô Quyền năm 938...). Mỗi mục có trường `type: legend | history`.
- Mỗi tên, năm, sự kiện trong mục lịch sử phải **trích được từ nguồn**, có link. Không có nguồn thì không viết.
- Bản kể lại chỉ được **làm đơn giản** cho dễ hiểu. Không thêm tình tiết, lời thoại hay sự kiện mà nguồn không có. Nếu cần chi tiết cho sinh động (ví dụ lời thoại) thì đánh dấu là phần thêm.
- Có một lượt kiểm tra: đối chiếu từng bản kể với nguồn và liệt kê những chỗ chưa có nguồn để chủ dự án xem.
- Claude vẫn có thể sai. Phần lịch sử nên có người hiểu sử (giáo viên sử) duyệt trước khi đưa vào sản phẩm.

*(Quyết định của Claude)* **Bản kể lại**: mỗi truyện có 2 bản, tóm tắt 3–5 câu và bản đọc to cho trẻ khoảng 3 phút (~400–500 chữ), chia theo cảnh. Kịch bản video viết sau, trong dự án video, dựa trên các cảnh này.

*(Quyết định của Claude)* **Xu hướng**: thị trường Việt Nam là chính, tham khảo thêm thế giới. Google Trends không có API chính thức nên không cào. Chủ dự án có thể xuất file từ Google Trends bằng tay rồi bỏ vào `raw/`. Nếu không có thì bỏ qua phần này.

*(Quyết định của Claude)* **"Lấy hết" nghĩa là**: trước tiên làm **đầy đủ mọi trường** cho các mục cốt lõi (toàn bộ từ vựng Cambridge, 10–15 phương pháp, khoảng 30 truyện phổ biến nhất). Sau đó mới mở rộng ra hết phần ước lượng ở bảng trên. Như vậy lúc nào cũng có một phần dùng được ngay.

## 6. Cách làm đã chọn: kết hợp (phương án C)

**Các phương án đã cân nhắc**
- **A. Không viết tool, Claude tự nghiên cứu**: nhanh nhất, nhưng khó chạy lại và khó kiểm chứng nguồn.
- **B. Tool Python đầy đủ cộng Claude API cộng Google API**: chạy lại được và tự động hoá được, nhưng lâu và thừa với nhu cầu lấy một lần.
- **C. Kết hợp** ⭐ (đã chọn): script nhỏ lo phần có cấu trúc, Claude trong Claude Code lo chọn lọc, tóm tắt, gắn nhãn và kể lại. Gần nhanh bằng A mà vẫn giữ dấu vết nguồn. Sau này nâng thành B được.

**Hai lớp**
1. **Lớp thu thập (script Python)**: tải và tách dữ liệu thô từ các nguồn có cấu trúc: PDF wordlist của Cambridge, trang Wikisource và Wikipedia (qua API MediaWiki), OpenAlex/Semantic Scholar API. Lưu bản thô kèm thông tin nguồn (URL, ngày lấy, giấy phép ghi trên trang).
2. **Lớp xử lý (Claude trong Claude Code)**: đọc bản thô, chọn lọc, viết thẻ phương pháp, kể lại truyện, gắn tag và nhãn giấy phép, rồi ghi ra định dạng chuẩn.

## 7. Định dạng đầu ra

```
kigo-data/
  english/
    curriculum/   (từ vựng và chủ đề theo cấp, phonics, CEFR)
    methods/      (mỗi phương pháp một file)
    research/     (tóm tắt nghiên cứu)
    trends/
  vietnam/
    folktales/
    history/
    culture/
  raw/            (bản thô từ lớp thu thập, không đưa vào dùng trực tiếp)
  index.csv       (bảng tổng hợp mọi mục, mở được bằng Google Sheets)
```

- Mỗi mục là một file Markdown, phần đầu có thông tin cố định: `id, title, category, tags_method, tags_topic, age_range, cefr_level, license_label, license_detail, source_url, retrieved_at, reviewed`.
- `index.csv` chứa đúng các cột đó cho mọi mục, để lọc trong Google Sheets.
- *(Quyết định của Claude)* **Duyệt ở đâu**: chủ dự án duyệt trong Google Sheets (`reviewed`, sửa `license_label`). Có một script nhỏ đọc file CSV đã sửa rồi cập nhật lại phần đầu của các file Markdown. Bảng là nơi quyết định nhãn, file Markdown là nơi chứa nội dung.
- Danh sách từ vựng lưu thêm ở dạng CSV (từ, loại từ, cấp, chủ đề).

## 8. Đưa lên Google Drive

Cách của mình: đặt `kigo-data/` trong thư mục được **Google Drive for desktop** đồng bộ, hoặc tải tay cả thư mục lên. Không cần viết code gọi Google API. Nếu máy chưa cài Google Drive for desktop thì tải tay.

## 9. Để lại cho người làm
- Chọn thư viện Python, cách tách PDF, cách chia script.
- Danh sách cụ thể từng truyện, nhân vật, chủ đề (theo ước lượng ở mục 5, chọn những cái phổ biến và hợp lứa tuổi).
- Thứ tự thu thập các nhóm.

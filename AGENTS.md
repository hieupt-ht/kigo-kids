# Hướng dẫn cho agent làm dữ liệu Kigo

## Mục tiêu

Kigo là ứng dụng học tiếng Anh cho trẻ em Việt Nam 6–10 tuổi. Linh vật là chú chó corgi tên Kigo, cùng 12 con giáp. Bộ dữ liệu `kigo-data/` được thu thập một lần: giáo trình và phương pháp dạy tiếng Anh, truyện dân gian, lịch sử trước 1945 và văn hóa Việt Nam. Sau đó dữ liệu được dùng để làm khoảng 20 video demo và nhiều video nữa, nên **mọi chi tiết phải đúng nguồn, không bịa**. Dữ liệu sẽ được tải lên Google Drive bằng tay.

Toàn bộ kế hoạch gốc: `docs/superpowers/plans/2026-11-24-kigo-data-collection.md` (Task 10–12 là phần còn lại). Thiết kế việc giao cho bạn: `docs/superpowers/specs/2026-11-25-codex-handoff-design.md`.

## Việc cần làm

1. **Đọc `kigo-data/PROGRESS.md` đầu tiên.** Nó ghi mục nào đã xong, đợt kế tiếp là gì.
2. Làm tiếp theo thứ tự: phần còn lại của truyện dân gian, rồi lịch sử trước 1945 (29 mục lõi `*` trước), rồi văn hóa, `trends/apps.md`, `index.csv` và `README.md`. Mỗi đợt khoảng 10 mục.
3. Không làm lại các mục đã xong.

## Công cụ

Dùng môi trường Python của repo: `source .venv/Scripts/activate` (Git Bash) hoặc `.venv\Scripts\Activate.ps1` (PowerShell), và đặt `PYTHONIOENCODING=utf-8`.

- Đọc nguồn Wikipedia/Wikisource tiếng Việt (cần tên bài **chính xác**): `python tools/read_source.py wiki "Bà Mụ"` (thêm `--site vi.wikisource` nếu cần; trang dài thì đọc từng phần bằng `--offset` và `--max`).
- Đọc một trang web khác: `python tools/read_source.py url "https://..." --keyword "từ khóa trong bài"` (`--keyword` để bỏ qua phần menu).
- Cả hai đi qua bộ tải lịch sự (có cache, theo robots.txt). Cần quyền mạng. Trang bị chặn hoặc lỗi thì bỏ qua và ghi lại, không cố vượt qua.
- Tên file: `from kigo_collect.entry import slugify` (tạo slug ASCII hợp lệ trên Windows).
- Kiểm tra: `python -m kigo_collect check` (phải ra `0 problem(s)`) và `python -m pytest -q` (phải xanh).
- Từ vựng Cambridge: `kigo-data/english/curriculum/vocabulary.csv` (cột `word`, `pos`, `level` = starters/movers/flyers).

## Định dạng một mục

Mỗi mục là một file Markdown có phần đầu YAML (front matter) rồi nội dung. Xem ba mục mẫu: `kigo-data/vietnam/folktales/thuan-thien-kiem.md` (mẫu chung), `ba-giai.md` (cách ghi lưu ý khi truyện có nội dung không hợp trẻ em), `tu-thuc.md` (cách ghi chỗ hai nguồn lệch nhau).

Front matter bắt buộc đủ 12 trường: `id, title, category, tags_method, tags_topic, age_range, cefr_level, license_label, license_detail, source_url, retrieved_at, reviewed`. Mục thuộc `vietnam/` thêm `type: legend` hoặc `type: history`, và `added_details`.

| Loại | `category` | `id` | `type` |
|---|---|---|---|
| Truyện dân gian | `vietnam/folktales` | `folktale-<slug>` | `legend` |
| Lịch sử | `vietnam/history` | `history-<slug>` | `history` (hoặc `legend` cho nhân vật/sự kiện truyền thuyết như Hùng Vương) |
| Văn hóa | `vietnam/culture` | `culture-<slug>` | `history` cho tục lệ có nguồn gốc ghi chép, `legend` cho truyền thuyết nguồn gốc |

Các giá trị cố định cho mục Việt Nam: `tags_method: [storytelling]`, `age_range: 6-10`, `cefr_level: Pre-A1 – A1`, `reviewed: false`, `retrieved_at` là ngày bạn đọc nguồn (YYYY-MM-DD). `source_url` là **danh sách mọi trang đã dùng**. `added_details` là danh sách (rỗng `[]` nếu không thêm gì).

Phần thân, theo thứ tự: `# Tên`, dòng nghiêng thể loại, `## Tóm tắt` (3–5 câu), `## Nhân vật`, `## Bài học` (gợi ý để cha mẹ trò chuyện với bé, ghi rõ không phải chi tiết của truyện gốc), `## Kể cho bé` (chia `### Cảnh 1 – ...`), `## Từ tiếng Anh liên quan` (từ trong danh sách Cambridge; từ ngoài danh sách vẫn được dùng nhưng ghi rõ "ngoài danh sách Cambridge Starters/Movers/Flyers"), `## Lưu ý độ tuổi`, `## Nguồn`. Với lịch sử, `## Từ tiếng Anh liên quan` không bắt buộc.

## Quy tắc nội dung

- **Không có nguồn thì không có câu.** Không thêm tên, năm, địa danh, lời thoại hay chi tiết mà nguồn đã đọc không có. Nếu buộc phải thêm một chi tiết để câu chuyện liền mạch, bọc nó trong `[thêm]…[/thêm]` và ghi vào `added_details`. Số dấu `[thêm]` phải bằng số mục trong `added_details` (`check` sẽ báo lỗi nếu lệch).
- **Viết lại bằng lời mới**, không chép câu, đoạn thoại hay cụm từ đặc trưng của nguồn.
- **Độ dài:** phần `## Kể cho bé` khoảng 400–500 từ khi nguồn đủ phong phú. Nếu nguồn ngắn, để ngắn, **không kéo dài cho đủ**. Ghi tên các mục ngắn hơn 400 từ vào `PROGRESS.md`.
- **Dị bản:** chỉ dùng khi ghi rõ dị bản đó lấy từ nguồn nào (ví dụ "Trang vi.wikipedia ghi một cách kể khác...").
- **Nguồn mâu thuẫn nhau** (tên, năm, cốt truyện): đừng đoán xem cái nào đúng. Kể theo nguồn chính, liệt kê chỗ lệch trong `## Lưu ý độ tuổi` hoặc trong `## Nguồn`, và không nêu con số còn tranh cãi trong phần kể cho bé.
- **Nội dung cho bé 6–10 tuổi:** cảnh bạo lực, giết chóc, khỏa thân, cảnh coi người như tài sản, từ ngữ kỳ thị (ví dụ bệnh tật) thì làm nhẹ bằng cách bỏ hoặc nói khác đi, và **ghi rõ đã làm nhẹ gì** trong `## Lưu ý độ tuổi`. Nếu phần lớn nguồn phổ biến không hợp trẻ em, đừng kể lại phần đó (xem `ba-giai.md`).
- **Từ tiếng Anh:** ưu tiên từ Cambridge Starters/Movers/Flyers; kiểm bằng `vocabulary.csv`.
- **Không dùng ngôi thứ nhất** ("mình", "tôi") trong nội dung mục.
- **Lịch sử:** chỉ trước 1945, theo sử chính thống Việt Nam. Ngay sau mỗi câu có tên người, năm hoặc sự kiện, đặt link Markdown tới một trang có trong `source_url`. Câu nào không có nguồn thì bỏ. Chỗ nghi ngờ ghi vào `kigo-data/vietnam/history/_can-kiem-tra.md` (một dòng: mục, câu nghi ngờ, vì sao) để giáo viên lịch sử xem. Đừng đưa Cách mạng tháng Tám hay Tuyên ngôn Độc lập 1945 vào; với nhân vật sống qua 1945 (như Hồ Chí Minh) chỉ dùng phần trước 1945.
- Trang Wikipedia không phải là nguồn tuyệt đối: nếu trang tự ghi "cần nguồn" hoặc tự mâu thuẫn, nói điều đó trong mục.

## Giấy phép (`license_label`)

- Mặc định là `reference`. Ghi lý do ngắn trong `license_detail`.
- `usable` chỉ khi trang nguồn ghi rõ giấy phép cho dùng thương mại (CC0, CC BY, phạm vi công cộng, OGL). Tự nhớ hay đoán không đủ.
- Wikipedia là CC BY-SA nên luôn `reference`; trang thương mại, blog, trang không rõ tác giả cũng `reference`.
- `excluded` cho nội dung không được dùng (ví dụ nội dung bị cấm sao chép).

## Quy trình một đợt

1. Lấy ~10 mục kế tiếp trong `PROGRESS.md`.
2. Với từng mục: đọc nguồn (xem phần Công cụ), tìm thêm một nguồn thứ hai để đối chiếu nếu có, rồi viết file mục.
3. Chạy `python -m kigo_collect check` (phải `0 problem(s)`) và `python -m pytest -q`.
4. Cập nhật `kigo-data/PROGRESS.md` (chuyển các mục vào "đã xong", đặt đợt kế tiếp, ghi các mục ngắn hơn 400 từ).
5. `git add` và commit, tên commit dạng `data: <nội dung> batch N` (không thêm dòng Co-Authored-By của Claude).
6. **Dừng lại**, báo cho chủ dự án là đợt đã sẵn sàng để Claude kiểm. Không làm đợt tiếp theo khi chưa được nói.

## Dừng và hỏi chủ dự án khi

- Không có mạng hoặc không mở được trang nguồn. **Không viết từ trí nhớ.**
- Nguồn quá mỏng để kể lại, hoặc chỉ có một trang duy nhất mà trang đó có vẻ sai.
- Nội dung nhạy cảm với trẻ em mà không chắc cách làm nhẹ.
- Không chắc giấy phép.
- `check` hoặc pytest lỗi mà không sửa được bằng cách sửa mục của bạn.

## Không được làm

- `git push`, đổi nhánh, merge, hay đụng nhánh `main`. Làm việc trên nhánh hiện tại (`feature/data-collection-tools`). Chủ dự án sẽ push.
- Sửa `tools/` hoặc `tests/`.
- Làm lại hoặc sửa các mục đã xong (trừ khi Claude yêu cầu sau khi kiểm).
- Đổi nhãn sang `usable` khi trang nguồn không nói rõ.
- Commit `kigo-data/raw/` (đã nằm trong `.gitignore`).
- Dùng Google Trends hoặc vượt qua chặn bot, đăng nhập, hay CAPTCHA.

## Claude sẽ kiểm thế nào

Khi chủ dự án báo "kiểm đợt N", Claude chạy `check` và pytest, chọn vài mục mẫu (truyện 2–3 trên 10, lịch sử 4–5 trên 10, văn hóa/ứng dụng 3 trên 10), mở các trang trong `source_url` và so từng tên, năm, chi tiết với bản kể. Vì vậy:

- Liệt kê **mọi trang đã dùng** trong `source_url`.
- Trong `## Nguồn`, ghi rõ phần nào lấy từ trang nào.
- Nếu Claude thấy một chi tiết bịa hoặc sai nghiêm trọng, Claude kiểm cả đợt đó, và bạn sửa rồi Claude kiểm lại chỗ sửa.

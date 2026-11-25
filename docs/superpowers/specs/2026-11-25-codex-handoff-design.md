# Giao phần dữ liệu còn lại cho Codex – thiết kế ngắn

Ngày: 2026-11-25. Trạng thái: chờ người dùng duyệt.

## Vì sao

Dữ liệu cho Kigo (app tiếng Anh cho bé Việt 6–10 tuổi, 20 video demo đến sau) đang được Claude làm từng đợt trong phiên chat. Cách này tốn token: đọc trang nguồn, viết tiếng Việt, và đọc lại sổ ghi chép sau mỗi lần compact. Người dùng muốn Codex làm phần còn lại; Claude chỉ kiểm.

## Mục tiêu

- Codex làm hết phần còn lại của kế hoạch `docs/superpowers/plans/2026-11-24-kigo-data-collection.md`:
  - Task 10: khoảng 40 mục truyện ngoài danh sách cốt lõi và 3 sách tham khảo (`kigo-data/content-lists/folktales.txt`).
  - Task 11: lịch sử Việt Nam trước 1945 (`history.txt`, 94 dòng).
  - Task 12: văn hóa, ứng dụng tiếng Anh cho trẻ, `index.csv`, `kigo-data/README.md`.
- Chất lượng ngang các mục đã làm: đúng nguồn, không bịa, nhãn giấy phép đúng.
- Claude chỉ kiểm mẫu từng đợt, không viết lại.

## Không phải mục tiêu / điều phải tránh

- Không làm lại các mục đã xong (39 mục truyện, Task 1–9).
- Điều tệ nhất: một chi tiết bịa lọt vào dữ liệu mà không ai biết. Mọi quy trình dưới đây nhằm tránh điều này.
- Không để Codex tự nâng nhãn giấy phép lên `usable` khi không chắc; mặc định là `reference`.

## Ràng buộc

- Chỉ lịch sử trước 1945; mỗi tên, năm, sự kiện có link nguồn ngay trong bài; chỗ nghi ngờ ghi vào `kigo-data/vietnam/history/_can-kiem-tra.md`, không đoán.
- Tải trang bằng `kigo_collect.fetch` (lịch sự, có cache, tôn trọng robots.txt) và dựng/kiểm bằng `python -m kigo_collect check`; pytest phải xanh.
- Nhánh: tiếp tục `feature/data-collection-tools` (cắt từ `develop`); không đụng `main`. Codex commit theo đợt khoảng 10 mục và **không push**; người dùng push.
- Codex cần quyền mạng khi chạy (mặc định thường bị chặn); người dùng bật.

## Các cách đã cân nhắc

- **A (chọn):** Codex làm hết, Claude chỉ kiểm mẫu. Rẻ nhất cho Claude, vì kiểm một mục có sẵn link rẻ hơn viết mới.
- **B:** Codex làm truyện và văn hóa, Claude tự làm 29 mục lịch sử cốt lõi. Chắc hơn cho lịch sử nhưng Claude vẫn tốn 3–4 đợt viết.
- **C (bỏ):** Claude điều phối nhiều agent Claude nhỏ hơn. Token vẫn tính vào phía Claude, không giải quyết nỗi lo của người dùng.

## Thiết kế (A)

1. **`AGENTS.md` ở gốc repo** (Codex đọc tự động). Nội dung: mục tiêu; cấu trúc `kigo-data/`; định dạng một mục (trỏ tới plan và các mục mẫu `ba-giai.md`, `tu-thuc.md`, `thuan-thien-kiem.md`); các quy tắc nội dung đã dùng ở Task 10 (kể bằng lời mới, 400–500 từ khi nguồn đủ và không kéo dài khi nguồn ngắn, làm nhẹ cảnh bạo lực/khỏa thân/xem người như tài sản và ghi trong "Lưu ý độ tuổi", chỉ dùng dị bản khi ghi rõ nguồn, mục nào cũng ghi chỗ nguồn mâu thuẫn, không chép nguyên văn, ưu tiên từ Cambridge Starters/Movers/Flyers); quy trình một đợt; khi nào phải dừng và hỏi người dùng (nguồn không mở được, nội dung nhạy cảm, không chắc giấy phép).
2. **`kigo-data/PROGRESS.md` trong repo**: danh sách đợt đã xong và đợt kế tiếp, để Codex biết đang ở đâu (sổ của Claude nằm trong thư mục git-ignored, Codex không thấy).
3. **Quy trình kiểm của Claude** khi người dùng báo "kiểm đợt N":
   - Chạy `check` và pytest.
   - Chọn mẫu: truyện 2–3 trên 10 mục; lịch sử 4–5 trên 10 mục; văn hóa/ứng dụng 3 trên 10 mục.
   - Với mỗi mục mẫu: mở các `source_url`, đối chiếu từng tên, năm, chi tiết với bản kể; kiểm các quy tắc nội dung (lời mới, làm nhẹ, dị bản có ghi nguồn, nhãn giấy phép).
   - Báo kết quả theo mục. Nếu thấy một chi tiết bịa hoặc sai nghiêm trọng thì kiểm toàn bộ đợt đó. Codex sửa rồi Claude kiểm lại chỗ sửa.
4. **Xong khi:** toàn bộ danh sách trong `content-lists` đã có mục (hoặc ghi lý do bỏ), `check` 0 lỗi, mỗi đợt có biên bản kiểm, `index.csv` được tạo và commit, README có.

## Để người dựng quyết

- Câu chữ cụ thể của `AGENTS.md`.
- Có đưa một vài kiểm tra tự động vào `check` hay không (ví dụ cờ cảnh báo từ "mình" ngôi thứ nhất, khoảng số từ).

## Những quyết định của Claude (người dùng chỉ chọn "Claude kiểm")

- Chọn cách A thay vì B.
- Tỉ lệ mẫu kiểm ở mục 3.
- Codex không push.
- Dùng `PROGRESS.md` trong repo thay cho sổ SDD.
- Thêm `tools/read_source.py` (script đứng riêng, không thuộc gói `kigo_collect`): lệnh `wiki` của gói chỉ in tên bài và nhãn, không in nội dung, nên Codex sẽ không đọc được nguồn nếu không có script này. Đã chạy thử trên một trang Wikipedia, một trang web khác và một tên bài không tồn tại. Không có test tự động.

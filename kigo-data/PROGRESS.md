# Tiến độ thu thập dữ liệu Kigo

## Cách dùng

- Đọc file này đầu tiên, trước khi làm bất cứ việc gì. Quy tắc làm việc nằm ở `AGENTS.md` (gốc repo).
- Mỗi đợt khoảng 10 mục, theo đúng thứ tự trong `kigo-data/content-lists/*.txt`. Làm xong một đợt thì cập nhật file này và commit cùng đợt đó.
- Slug là tên file không có `.md`, ví dụ `kigo-data/vietnam/folktales/<slug>.md`.
- Đợt 1–8 do Claude làm. Các đợt sau do Codex làm, Claude kiểm mẫu.

## Truyện dân gian (`kigo-data/vietnam/folktales/`) – đã xong 39 mục

Bộ lõi (29): `son-tinh-thuy-tinh`, `thanh-giong`, `ho-hoan-kiem`, `lang-lieu`, `su-tich-trau-cau`, `mai-an-tiem`, `con-rong-chau-tien`, `coc-kien-troi`, `tam-cam`, `thach-sanh`, `cay-tre-tram-dot`, `cay-khe`, `so-dua`, `chu-dong-tu`, `chu-cuoi-cung-trang`, `thang-bom`, `nang-to-thi`, `truong-chi`, `rua-than-kim-quy`, `an-duong-vuong`, `thay-boi-xem-voi`, `ret-nang-ban`, `cong-va-qua`, `su-tich-con-thach-sung`, `su-tich-hoa-phuong`, `ho-ba-be`, `ngu-hanh-son`, `ho-nui-coc`, `ba-giai`.

Đợt 8, ngoài lõi (10): `lac-long-quan`, `au-co`, `kinh-duong-vuong`, `tien-dung`, `my-chau`, `trong-thuy`, `thuan-thien-kiem`, `son-tinh`, `thuy-tinh`, `tu-thuc`.

### Đợt kế tiếp (đợt 9): dòng 43–52 của `folktales.txt`

1. Quan án xử kiện
2. Hồn Trương Ba, da hàng thịt
3. Ngưu Lang Chức Nữ
4. Dã tràng
5. Lý Ông Trọng
6. Thuồng luồng
7. Rồng Việt Nam
8. Liễu Hạnh Công chúa
9. Tứ bất tử
10. Bà Mụ

### Còn lại sau đợt 9

- 30 mục: dòng 53–82 của `folktales.txt`, từ Hằng Nga đến Lục Vân Tiên, làm tiếp theo thứ tự, khoảng 10 mục một đợt.
- Ba sách nguồn ở cuối danh sách (Truyền kỳ mạn lục, Lĩnh Nam chích quái, Việt điện u linh tập): làm sau cùng. Mỗi sách một mục ngắn mô tả sách (thời kỳ, nội dung chính), lấy từ trang vi.wikipedia của sách, nhãn `reference`.

## Lịch sử trước 1945 (`kigo-data/vietnam/history/`) – chưa bắt đầu

- `kigo-data/content-lists/history.txt` có 90 mục, trong đó 29 mục lõi đánh dấu `*`. Làm 29 mục lõi trước, theo thứ tự trong file, rồi mới làm các mục còn lại.
- Mỗi tên, năm, sự kiện trong bài phải có link nguồn ngay trong bài. Chỗ nghi ngờ ghi vào `kigo-data/vietnam/history/_can-kiem-tra.md` (tạo khi cần), không đoán.

## Văn hóa, ứng dụng tiếng Anh, chỉ mục, README – chưa bắt đầu

Làm sau lịch sử, theo thứ tự:
1. `kigo-data/vietnam/culture/<slug>.md`: `kigo-data/content-lists/culture.txt` có 61 mục, 25 mục lõi `*`. Mười hai con giáp mỗi con một mục (Mão là Mèo).
2. `kigo-data/english/trends/apps.md`: phân tích khoảng 10 ứng dụng tiếng Anh cho trẻ em, từ trang cửa hàng công khai. Phần Google Trends bỏ qua, ghi rõ là đã bỏ, trừ khi có file xuất trong `kigo-data/raw/trends/`.
3. Chạy `python -m kigo_collect index`, rồi `python -m kigo_collect check` (kết quả phải là 0 problem). Commit `kigo-data/index.csv`.
4. `kigo-data/README.md`: cấu trúc thư mục, ý nghĩa ba nhãn giấy phép, cách duyệt bằng Google Sheets, cách chạy `python -m kigo_collect sync-review`, và ghi chú tải lên Google Drive bằng tay.

## Ghi chú cho đợt sau

- Mục truyện ngắn hơn 400 từ vì nguồn ngắn thì không kéo dài; ghi tên mục vào đây.
- Sự tích hoa phượng là truyện hiện đại của Phạm Hổ (có thể còn bản quyền), nên chỉ giữ nhãn `reference`. Không đổi nhãn.

## Nhật ký kiểm của Claude

| Đợt | Ngày | Mục đã kiểm | Kết quả | Ghi chú |
|---|---|---|---|---|

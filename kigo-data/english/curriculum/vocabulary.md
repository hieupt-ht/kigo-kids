---
id: vocabulary-cambridge-yle
title: Từ vựng Cambridge Pre A1 Starters, A1 Movers, A2 Flyers (bản 2025)
category: english/curriculum
tags_method:
- picture-word
- spaced-repetition
tags_topic:
- vocabulary
- cambridge-yle
age_range: 6-10
cefr_level: Pre-A1 – A2
license_label: reference
license_detail: © Cambridge University Press & Assessment. Bảng từ (từ, loại từ, cấp,
  chủ đề) dùng thẳng làm dữ liệu vì từng từ tiếng Anh thông dụng không có bản quyền;
  KHÔNG chép câu ví dụ, tranh, cách trình bày hay đề thi.
source_url:
- https://www.cambridgeenglish.org/Images/739104-starters-movers-flyers-word-list-2025.pdf
retrieved_at: '2026-11-24'
reviewed: false
---

# Từ vựng Cambridge Young Learners (bản 2025)

## Nội dung
`vocabulary.csv` (cùng thư mục) có **1.407 dòng**, lấy từ bảng A–Z của ba cấp trong tài liệu
*Pre A1 Starters, A1 Movers and A2 Flyers Wordlists* của Cambridge English:

| Cấp | CEFR | Số dòng (từ mới của cấp đó) |
|---|---|---|
| Starters | Pre A1 | 495 |
| Movers | A1 | 399 |
| Flyers | A2 | 513 |

Mỗi cấp chỉ liệt kê **từ mới của cấp đó**; muốn biết toàn bộ vốn từ của Flyers thì cộng cả ba cấp.

## Các cột
- `word`: từ hoặc cụm từ (ví dụ `ice cream`, `go to bed`, `foot/feet`).
- `pos`: loại từ theo tài liệu: n, v, adj, adv, prep, pron, det, conj, excl, int, dis (từ nối lời nói), poss, title; có thể ghép như `n + v`. Chỉ `a.m.` và `p.m.` không ghi loại từ vì tài liệu không ghi.
- `level`: `starters`, `movers` hoặc `flyers`.
- `topic`: chủ đề theo bảng "thematic vocabulary list" của Cambridge, có thể có nhiều chủ đề, cách nhau bằng `; ` (18 chủ đề: Animals, The body and the face, Clothes, Colours, Family and friends, Food and drink, Health, The home, Materials, Places and directions, School, Sports and leisure, Time, Toys, Transport, Weather, Work, The world around us). **844 dòng có chủ đề.** Từ chức năng và tính từ chung như `a`, `and`, `big`, `good` không thuộc chủ đề nào nên để trống.
- `note`: ghi chú trong ngoặc của Cambridge, ví dụ `UK flat`, `US color`, `as sports equipment` (nghĩa của từ), `of place` (cách dùng).

## Lưu ý sử dụng (quan trọng)
- Được dùng: danh sách từ, loại từ, cấp, chủ đề.
- **Không chép**: câu ví dụ, tranh minh hoạ, cách trình bày tài liệu, đề thi và bài mẫu của Cambridge.
- Chính tả Anh và Mỹ lẫn nhau trong tài liệu (`colour` kèm `US color`). Với app Kigo giọng Mỹ, lấy cột `note` để đổi sang cách Mỹ khi cần.
- Tên riêng trong tài liệu (Alex, Ann/Anna...) có trong bảng A–Z, nhưng danh sách tên riêng cuối mỗi cấp thì không đưa vào.
- Bảng này sinh tự động bằng `python -m kigo_collect wordlist --layout az2025` từ văn bản trích từ PDF; 20 dòng ngẫu nhiên đã đối chiếu với văn bản trích đó (không sai dòng nào), chưa đối chiếu bằng mắt với trang PDF. Cần người xem thêm các dòng có chủ đề hơi lạ (ví dụ `floor` xếp vào School) trước khi dùng cho bài học.

## Nguồn
- [Pre A1 Starters, A1 Movers and A2 Flyers Wordlists (2025)](https://www.cambridgeenglish.org/Images/739104-starters-movers-flyers-word-list-2025.pdf), lấy ngày 2026-11-24.

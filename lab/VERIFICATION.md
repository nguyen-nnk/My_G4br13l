# Lab Verification — Kết quả chạy thử

**Ngày kiểm tra:** 2026-10-10  
**Phạm vi:** Lab Flask + SQLite độc lập  
**Kết quả:** **PASS — 6/6 checks**

Đây là biên bản ghi lại lần chạy Lab mô phỏng trong môi trường sạch. Xin nhắc lại một chút để khỏi đọc nhầm: kết quả này xác nhận hành vi của **mô hình Flask + SQLite**, không phải kết quả kiểm thử production của Gabriel.

## Kết quả quan sát

| Trường hợp | Trước khi bật kiểm tra | Sau khi bật kiểm tra |
|---|---:|---:|
| Huynh trưởng A đọc điểm danh lớp A | 200 | 200 |
| Huynh trưởng A đọc điểm danh lớp B | 200 | 403 |
| Huynh trưởng B đọc điểm danh lớp B | 200 | 200 |

Test script kiểm tra cả HTTP status code và danh sách mã Thiếu nhi mà endpoint trả về.

## Kết luận

Trong Lab độc lập, khi bật bước kiểm tra phân công, tài khoản được gán lớp A không lấy được dữ liệu điểm danh lớp B; hai trường hợp truy cập đúng lớp vẫn hoạt động. Kết quả khớp với quy tắc được mô phỏng.

## Giới hạn

- Đây là ứng dụng Flask + SQLite mô phỏng.
- Lab không thực thi production source của Gabriel.
- Authentication được mô phỏng bằng cách tạo sẵn test session.
- Chính sách phân quyền thực tế vẫn cần Team Dev xác nhận.
- Hành vi production chưa được xác minh.

Vậy nên: **6/6 PASS là một kết quả tốt cho Lab này**, nhưng không nên diễn giải xa hơn những gì bài test thực sự kiểm tra.

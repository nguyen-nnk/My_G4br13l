# G4br13l — Nhật ký điều tra bảo mật

> **Từ một dòng decorator bị vô hiệu hóa đến thí nghiệm kiểm tra phân quyền trên localhost.**

G4br13l là project tự học cá nhân tôi, bắt đầu từ việc đọc mã nguồn ứng dụng web Gabriel. Khi tình cờ thấy decorator `@permission` bị comment out, tôi đặt câu hỏi về sự khác nhau giữa đăng nhập và quyền truy cập. Sau đó, tôi thu hẹp phạm vi điều tra vào một tình huống cụ thể: **Huynh trưởng phụ trách lớp A có xem được sổ điểm danh của lớp B hay không?**

## Các phần của project

| Phần | Nội dung |
|---|---|
| [Nhật ký điều tra](docs/01.G4br13l_WriteUp.md) | Câu chuyện từ lúc quan sát code, hình thành giả thuyết, thử nghiệm, đề xuất sửa và kiểm thử lại. |
| [Sổ tay thí nghiệm](docs/02.G4br13l_Investigation.md) | Lệnh chạy, dữ liệu thử nghiệm và ghi chú khi kiểm tra bản source trên môi trường local. |
| [Lab mô phỏng độc lập](lab/README.md) | Ứng dụng Flask + SQLite nhỏ để minh họa quy tắc phân quyền, không cần source Gabriel. |
| [Kết quả Verify Lab](lab/VERIFICATION.md) | Ghi lại kết quả chạy bộ test mô phỏng độc lập (6/6 lượt kiểm tra PASS) và giới hạn của kết quả. |
| [Tài liệu dành cho review nội bộ](internal/README.md) | Bản diff đề xuất và ghi chú schema chỉ dùng khi rà soát bản source trên máy local. |

## Quan sát chính

Trong thí nghiệm local với dữ liệu giả gồm hai Huynh trưởng và hai lớp, trước khi thêm bước kiểm tra phân công, API điểm danh trả dữ liệu của lớp B khi tài khoản Huynh trưởng A yêu cầu, dù A chỉ được phân công lớp A.

Tôi đề xuất kiểm tra phân công lớp còn hiệu lực trước khi trả dữ liệu điểm danh. Kết quả kiểm thử trên bản source local được ghi nhận như sau:

| Trường hợp | Trước khi sửa | Sau khi sửa |
|---|---:|---:|
| Huynh trưởng A xem lớp A | `200 OK` | `200 OK` |
| Huynh trưởng A xem lớp B | `200 OK` | `403 Forbidden` |
| Huynh trưởng B xem lớp B | `200 OK` | `200 OK` |

Đây là kết quả từ môi trường local và dữ liệu giả. Nó **không chứng minh production có cùng hành vi**, cũng chưa xác nhận quy tắc được thử nghiệm hoàn toàn trùng với chính sách nghiệp vụ của Team Dev.

## Lab mô phỏng độc lập

Thư mục `lab/` chứa mô hình Flask + SQLite dùng dữ liệu giả và Flask test client. Lab không import, không chạy và không cần sao chép ứng dụng Gabriel. Mục tiêu là giúp người đọc tự chạy lại các ca kiểm thử để hiểu vì sao cần kiểm tra quyền trên từng lớp.

Bắt đầu tại [hướng dẫn chạy lab](lab/README.md) hoặc xem [kết quả Verify Lab](lab/VERIFICATION.md).

## Tiến độ

- [x] Đọc route liên quan và tìm hiểu logic phân công lớp.
- [x] Ghi lại thí nghiệm local với dữ liệu giả.
- [x] Đề xuất một bản sửa để review nội bộ.
- [x] Tạo lab mô phỏng độc lập.
- [x] Chạy lab từ môi trường sạch và lưu kết quả kiểm thử.
- [ ] Nhờ Team Dev xác nhận chính sách xem điểm danh theo lớp.
- [ ] Kiểm tra thêm hành vi cache khi phân công thay đổi hoặc bị thu hồi.
- [ ] Chỉ cân nhắc tạo pull request sau khi được review và cho phép.

## Phạm vi và giới hạn

- Thí nghiệm với ứng dụng gốc được thực hiện trên môi trường phát triển local và dùng dữ liệu giả.
- Flask test client tạo sẵn phiên đã xác thực; thí nghiệm không kiểm tra luồng đăng nhập thật.
- Lab độc lập chỉ minh họa nguyên tắc, không phải bản tái tạo toàn bộ ứng dụng Gabriel.
- Bản sửa đề xuất chưa được triển khai lên production và chưa có pull request.
- Hành vi production và chính sách phân quyền cuối cùng vẫn cần được xác nhận.

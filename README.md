# My_G4br13l — Từ một dòng `@permission` đến câu hỏi phân quyền

> Một project tự học và điều tra bảo mật cá nhân. Bắt đầu từ việc tò mò khi đọc code, rồi thử biến sự tò mò đó thành giả thuyết và thí nghiệm có thể kiểm tra lại.

## Chuyện bắt đầu khá tình cờ

Tôi đã dùng website quản lý Thiếu nhi này suốt ba năm trong vai trò Huynh trưởng. Nhưng dùng một website và hiểu code bên trong nó là hai chuyện hoàn toàn khác nhau.

Tôi vốn quen với Computer Architecture, Operating Systems, Computer Networks và gần đây là System Programming. Còn Web Development thì… nói thật là một thế giới khác. Sau khi có cơ hội tiếp cận source code, tôi bắt đầu đọc thử. Chiến thuật học cũng đơn giản thôi: không hiểu chỗ nào thì hỏi chỗ đó, thiếu kiến thức nào thì đắp kiến thức ấy rồi quay lại đọc tiếp.

Trong lúc loay hoay với Python decorator, tôi gặp một dòng `@permission` đang bị comment out.

*Ủa, vậy permission ở đây dùng để làm gì? Nếu nó không chạy thì route đang dựa vào đâu để quyết định ai được xem dữ liệu?*

Từ một dòng code như thế, tôi bắt đầu tìm hiểu **Authentication (AuthN)** và **Authorization (AuthZ)**, rồi đặt giả thuyết để kiểm tra. Càng đọc tôi càng nhận ra thấy một đoạn code đáng ngờ chưa đủ để kết luận có vulnerability. Cần phải hiểu tính năng, xác định hành vi mong đợi, rồi mới tìm cách kiểm chứng.

## Từ nghi vấn ban đầu đến bài toán cụ thể

Lúc đầu tôi thử kiểm tra một API tra cứu thông tin người dùng. Nhưng kết quả trả về chưa chắc đã là lỗi: một Huynh trưởng xem được thông tin cơ bản của Huynh trưởng khác có thể hoàn toàn phù hợp với cách website được thiết kế.

Thế nên tôi chuyển sang một tình huống có ranh giới rõ hơn: **Huynh trưởng phụ trách lớp A có được xem sổ điểm danh của lớp B không?**

Tôi tạo dữ liệu giả cho hai Huynh trưởng và hai lớp, chạy ứng dụng trên môi trường local, rồi kiểm tra các trường hợp truy cập. Trên bản source local trước khi thêm bước kiểm tra, tài khoản phụ trách lớp A vẫn nhận được dữ liệu điểm danh của lớp B với HTTP `200`. Đây là bằng chứng đáng chú ý hơn, với giả định cần được Team Dev xác nhận rằng quyền xem điểm danh phải theo lớp được phân công.

Tôi thử đề xuất kiểm tra phân công còn hiệu lực trước khi trả dữ liệu và kiểm thử lại trên local:

| Trường hợp | Trước khi sửa | Sau khi sửa |
|---|---:|---:|
| Huynh trưởng A xem lớp A | `200 OK` | `200 OK` |
| Huynh trưởng A xem lớp B | `200 OK` | `403 Forbidden` |
| Huynh trưởng B xem lớp B | `200 OK` | `200 OK` |

Vậy là tôi có một kết quả khớp với quy tắc đang thử nghiệm. Nhưng khoan — **đây là kết quả trên môi trường local, chưa phải kết luận về production**, và quy tắc nghiệp vụ vẫn cần được Team Dev xác nhận. Tôi muốn giữ rõ ranh giới đó thay vì viết cho hoành tráng rồi lỡ bị hỏi sâu lại không có bằng chứng.

## Đi một vòng trong repository

| Phần | Có gì ở đây? |
|---|---|
| [WriteUp](docs/01.G4br13l_WriteUp.md) | Câu chuyện từ lúc gặp `@permission`, đặt giả thuyết, thử nghiệm, đề xuất sửa và kiểm thử lại. |
| [Investigation Notes](docs/02.G4br13l_Investigation.md) | Các lệnh và ghi chú để lần lại thí nghiệm trên source chạy local. |
| [Lab mô phỏng](lab/README.md) | Một ứng dụng Flask + SQLite độc lập để thử nguyên tắc phân quyền bằng dữ liệu giả. |
| [Lab Verification](lab/VERIFICATION.md) | Kết quả chạy bộ test của mô hình độc lập: 6/6 checks PASS. |
| [Tài liệu kỹ thuật bổ sung](internal/README.md) | Bản diff đề xuất và ghi chú schema phục vụ việc review source local. |

## Vì sao còn có một Lab riêng?

Tôi muốn có một ví dụ nhỏ mà người đọc có thể tự chạy, không cần dựng cả ứng dụng Gabriel. Vì thế thư mục `lab/` có một mô hình Flask + SQLite tách biệt, dùng dữ liệu giả để so sánh hành vi trước và sau khi bật kiểm tra phân công lớp.

Lab này cũng đã được chạy từ môi trường sạch và cả 6 checks đều PASS. Nhưng lưu ý giúp tôi một chút: **6/6 PASS là kết quả của Lab mô phỏng độc lập**, không phải bằng chứng rằng production đã được kiểm thử. Hai phần có mục đích khác nhau nên tôi ghi riêng.

Bắt đầu từ [hướng dẫn chạy Lab](lab/README.md), hoặc xem [biên bản Verification](lab/VERIFICATION.md).

## Tiến độ hiện tại

- [x] Đọc route liên quan và lần theo logic phân công lớp.
- [x] Thử nghiệm trên source local với dữ liệu giả.
- [x] Đề xuất bản sửa kiểm tra quyền truy cập theo lớp.
- [x] Dựng Lab mô phỏng độc lập.
- [x] Chạy Lab từ môi trường sạch và ghi lại kết quả.
- [ ] Nhờ Team Dev xác nhận chính sách xem điểm danh theo lớp.
- [ ] Chỉ cân nhắc contribution hoặc pull request sau khi quy tắc và bản sửa được review.

## Mấy điều cần nói rõ

- Thí nghiệm với ứng dụng gốc diễn ra trong môi trường phát triển local và dùng dữ liệu giả.
- Phiên đăng nhập trong một số kiểm thử được tạo sẵn; chưa kiểm tra đầy đủ luồng đăng nhập thật.
- Lab Flask + SQLite là mô hình minh họa riêng, không import hay chạy source Gabriel.
- Bản sửa vẫn là đề xuất local, chưa được merge, chưa triển khai lên production và chưa gửi pull request.
- Hành vi production và chính sách phân quyền cuối cùng chưa được xác nhận.

Tôi làm project này để học cách đi từ một nghi vấn đến một thí nghiệm có thể kiểm tra lại — chứ không phải để tuyên bố mình đã tìm ra một lỗi production. Nếu có điều gì tôi học được từ quá trình này, thì đó là: **thấy code đáng ngờ mới chỉ là điểm bắt đầu; evidence mới là thứ giúp mình tiến gần hơn đến kết luận.**

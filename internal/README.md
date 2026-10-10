# Tài liệu kỹ thuật bổ sung — G4br13l

Nếu muốn xem kỹ phần tôi đề xuất sửa, thư mục này là chỗ để bắt đầu. Tôi để riêng hai file này vì chúng phục vụ việc review source chạy local, không phải hướng dẫn chạy Lab mô phỏng.

## Có gì ở đây?

- `attendance-access-control.diff` — Bản diff đề xuất kiểm tra xem người đang đăng nhập có được phân công vào lớp còn hiệu lực hay không, trước khi trả dữ liệu điểm danh.
- `schema-local-prereqs.sql` — Ghi chú về những điều chỉnh schema từng cần để chạy bản source mirror với database thử nghiệm local.

## Một vài lưu ý trước khi xem

Bản diff là **đề xuất cục bộ để review**, chưa được merge và chưa triển khai lên production. File SQL cũng chỉ là ghi chú điều kiện của môi trường local, không phải migration chính thức cho dự án gốc.

Còn một điểm quan trọng nữa: quy tắc “chỉ được xem điểm danh lớp mình phụ trách” là giả định được dùng trong thí nghiệm hiện tại. Tôi vẫn cần Team Dev xác nhận chính sách nghiệp vụ trước khi xem đây là quy tắc chính thức.

Nếu chỉ muốn hiểu nguyên tắc kiểm tra quyền mà không dựng source Gabriel, hãy qua [Lab mô phỏng độc lập](../lab/README.md). Hai phần có liên quan, nhưng không phải cùng một môi trường kiểm thử.

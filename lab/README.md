# Lab mô phỏng — Huynh trưởng A có xem được điểm danh lớp B không?

Trong lúc thử nghiệm với source chạy local, tôi muốn có một mô hình nhỏ để minh họa một nguyên tắc: đã đăng nhập không có nghĩa là được xem mọi tài nguyên.

Thay vì bắt người đọc dựng cả ứng dụng Gabriel, tôi tạo Lab này bằng **Flask + SQLite** và dữ liệu giả. Nó độc lập hoàn toàn: không import, không cần clone và không chạy mã nguồn Gabriel/G4br13l.

## Lab này thử điều gì?

Có hai chế độ để đặt cạnh nhau:

- **Trước khi bật kiểm tra:** server không kiểm tra phân công lớp trước khi trả dữ liệu điểm danh.
- **Sau khi bật kiểm tra:** chỉ cho phép Huynh trưởng hoặc trợ giảng có phân công còn hiệu lực xem điểm danh của lớp đó.

Tôi dùng ba trường hợp đơn giản: A xem lớp A, A xem lớp B, và B xem lớp B. Nếu quy tắc phân công được áp dụng, trường hợp truy cập lớp khác phải bị từ chối, còn hai trường hợp hợp lệ vẫn hoạt động.

Đây là mô hình học tập nhỏ, không tái tạo toàn bộ ứng dụng Gabriel và **không chứng minh production có cùng hành vi**. Lab giúp ta nhìn vào nguyên tắc và chạy lại các ca kiểm thử; nó không thay thế việc review source thật hay xác nhận chính sách nghiệp vụ.

## Các file trong Lab

| File | Dùng để làm gì? |
|---|---|
| `demo_app.py` | Ứng dụng Flask nhỏ, có thể bật/tắt bước kiểm tra phân công. |
| `seed.sql` | Schema SQLite và dữ liệu thử nghiệm giả. |
| `test_attendance_access.py` | Chạy các trường hợp trước/sau bằng Flask test client. |
| `requirements.txt` | Các thư viện cần cài. |
| `VERIFICATION.md` | Kết quả đã chạy, kết luận và các giới hạn. |

## Chạy thử

Yêu cầu: Python 3.10 trở lên.

Mở Terminal tại thư mục `lab/`, sau đó chạy:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python test_attendance_access.py
```

Không cần MySQL, backend Gabriel hay cấu hình Casdoor. Nếu chỉ muốn xem code thì có thể bắt đầu từ `demo_app.py`; nếu muốn hiểu các tình huống test thì mở `test_attendance_access.py`.

## Kết quả mong đợi

| Trường hợp | Trước kiểm tra (mô phỏng) | Sau kiểm tra (mô phỏng) |
|---|---:|---:|
| Huynh trưởng A xem lớp A | **200** | **200** |
| Huynh trưởng A xem lớp B | **200** | **403** |
| Huynh trưởng B xem lớp B | **200** | **200** |

Script kiểm tra cả HTTP status code lẫn danh sách mã Thiếu nhi được trả về. Nếu kết quả lệch khỏi kỳ vọng, script in `FAIL` và kết thúc với exit code khác 0.

Tôi đã chạy Lab trong môi trường clone sạch và ghi nhận **6/6 checks PASS**. Chi tiết nằm ở [Lab Verification](VERIFICATION.md).

## Phạm vi và giới hạn — đừng bỏ qua phần này nhé

- Mọi mã định danh và dữ liệu điểm danh đều là dữ liệu giả.
- Phiên đăng nhập trong test được tạo trực tiếp; không kiểm tra đăng nhập thật hay Casdoor.
- Hai chế độ chỉ mô phỏng nguyên tắc trước/sau; chúng không chạy source Gabriel trước/sau bản sửa.
- Chính sách nghiệp vụ cần được Team Dev xác nhận.
- Lab chưa kiểm tra cache, thu hồi phân công, production hoặc triển khai thực tế.

## Muốn đọc thêm?

- [WriteUp — câu chuyện điều tra](../docs/01.G4br13l_WriteUp.md)
- [Investigation Notes — cách chạy thí nghiệm trên source local](../docs/02.G4br13l_Investigation.md)
- [Tài liệu kỹ thuật bổ sung và bản diff đề xuất](../internal/README.md)

Bản diff cho source gốc và ghi chú schema local được giữ riêng để review. Chúng không phải thành phần của Lab độc lập này.

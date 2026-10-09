# Lab mô phỏng — Phân quyền xem điểm danh

Đây là **mô hình học tập độc lập** để minh họa việc kiểm tra quyền xem điểm danh theo lớp. Lab dùng Flask + SQLite và dữ liệu giả; **không import, không cần clone và không chạy mã nguồn Gabriel/G4br13l**.

Lab có hai chế độ để so sánh:

- **Trước khi thêm bước kiểm tra:** không kiểm tra phân công lớp trước khi trả dữ liệu điểm danh.
- **Sau khi thêm bước kiểm tra:** chỉ cho phép Huynh trưởng/trợ giảng có phân công còn hiệu lực xem điểm danh lớp đó.

Đây là mô hình nhỏ để hiểu nguyên tắc, không phải bản tái tạo toàn bộ ứng dụng Gabriel và không chứng minh production có cùng hành vi.

## Các tệp trong lab

| Tệp | Công dụng |
|---|---|
| `demo_app.py` | Ứng dụng Flask nhỏ, có thể bật/tắt bước kiểm tra phân công |
| `seed.sql` | Cấu trúc SQLite và dữ liệu thử nghiệm giả |
| `test_attendance_access.py` | So sánh ba trường hợp trước/sau bằng Flask test client |
| `requirements.txt` | Thư viện cần cài để chạy lab |

## Cách chạy

Yêu cầu: Python 3.10 trở lên.

Mở Terminal tại thư mục `lab/` rồi chạy:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python test_attendance_access.py
```

Không cần MySQL, backend Gabriel hay cấu hình Casdoor.

## Kết quả mong đợi

| Trường hợp | Trước kiểm tra (mô phỏng) | Sau kiểm tra (mô phỏng) |
|---|---:|---:|
| Huynh trưởng A xem lớp A | **200** | **200** |
| Huynh trưởng A xem lớp B | **200** | **403** |
| Huynh trưởng B xem lớp B | **200** | **200** |

Script kiểm tra cả mã HTTP và danh sách mã Thiếu nhi được trả về. Nếu kết quả không đúng như kỳ vọng, script in `FAIL` và kết thúc với mã lỗi khác 0.

## Phạm vi và giới hạn

- Tất cả mã định danh và dữ liệu điểm danh đều là dữ liệu giả.
- Phiên đăng nhập trong kiểm thử được tạo trực tiếp; không kiểm tra đăng nhập thật hay Casdoor.
- Hai chế độ chỉ mô phỏng nguyên tắc trước/sau, không chạy source Gabriel trước/sau bản sửa.
- Chính sách nghiệp vụ cần được Team Dev xác nhận.
- Chưa kiểm tra cache, việc thu hồi phân công, hành vi production hay triển khai thực tế.

## Liên quan đến quá trình điều tra

- [Nhật ký điều tra bảo mật](../docs/Project_G4br13l.md)
- [Sổ tay thí nghiệm trên bản source local](../docs/G4br13l_Investigation.md)

Bản diff dành cho source gốc và ghi chú schema local được giữ riêng để review nội bộ; chúng không phải thành phần của lab mô phỏng độc lập.

# Standalone Lab — Attendance Authorization

Đây là một **mô hình học tập độc lập** để minh họa kiểm tra quyền truy cập điểm danh theo lớp. Lab dùng Flask + SQLite và dữ liệu giả; **không import, không cần clone và không chạy source code Gabriel/G4br13l**.

Lab mô phỏng hai chế độ:
- **Before patch:** không kiểm tra phân công lớp trước khi trả attendance.
- **After patch:** chỉ cho phép Teacher/Assistant có phân công còn hiệu lực xem lớp đó.

Đây là mô hình nhỏ để tái hiện nguyên lý, không phải bản tái hiện nguyên vẹn ứng dụng Gabriel và không chứng minh production có cùng hành vi.

## Files

| File | Purpose |
|---|---|
| **demo_app.py** | Ứng dụng Flask nhỏ với toggle bật/tắt kiểm tra phân công |
| **seed.sql** | Schema SQLite và dữ liệu thử nghiệm giả |
| **test_attendance_access.py** | So sánh ba ca trước/sau patch bằng Flask test client |
| **requirements.txt** | Dependency tối thiểu |

## Run

Requirements: Python 3.10+

Từ thư mục lab:

~~~bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python test_attendance_access.py
~~~

Không cần MySQL, không cần backend Gabriel, không cần cấu hình Casdoor.

## Expected result

| Test case | Before (simulated) | After (simulated) |
|---|---:|---:|
| Teacher A → Class A | **200** | **200** |
| Teacher A → Class B | **200** | **403** |
| Teacher B → Class B | **200** | **200** |

Script kiểm tra cả HTTP status và danh sách mã Thiếu nhi trả về; nếu kết quả không khớp kỳ vọng, nó in FAIL và thoát với exit code khác 0.

## Scope and limitations

- Tất cả identifiers và dữ liệu điểm danh đều giả.
- Session trong test được tạo trực tiếp; không kiểm tra login thật hay Casdoor.
- Hai chế độ là mô hình minh họa, không phải chạy bản source Gabriel trước/sau patch.
- Chính sách nghiệp vụ vẫn cần Team Dev xác nhận.
- Cache, phân công bị thu hồi, production behavior và deployment chưa được kiểm tra.

## Relation to the original investigation

- [Security WriteUp](../docs/Project_G4br13l.md)
- [Source-specific Lab Notebook](../docs/G4br13l_Investigation.md)

Source-specific patch diff và schema prerequisite cho bản mirror gốc được giữ riêng để review nội bộ; chúng không phải thành phần của lab độc lập này.

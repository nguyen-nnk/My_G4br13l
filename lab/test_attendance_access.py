"""So sánh endpoint điểm danh mô phỏng trước và sau khi kiểm tra phân công.

Chạy bằng:
    python test_attendance_access.py

Chỉ dùng demo_app.py, Flask test client và dữ liệu SQLite giả. Không import Gabriel.
"""
from demo_app import create_app

CASES = [
    ("Huynh trưởng A xem lớp A", "HQ261009T1", "HQ261009A", ["HQ261009S1"]),
    ("Huynh trưởng A xem lớp B", "HQ261009T1", "HQ261009B", ["HQ261009S2"]),
    ("Huynh trưởng B xem lớp B", "HQ261009T2", "HQ261009B", ["HQ261009S2"]),
]


def make_client(app, teacher_code):
    client = app.test_client()
    with client.session_transaction() as session:
        session["teacher_code"] = teacher_code
    return client


def returned_student_codes(body):
    return [
        row.get("student_code")
        for day in (body.get("data", []) or [])
        for row in (day.get("attendances", []) or [])
        if row.get("student_code")
    ]


def run_group(title, enforce_assignment):
    app = create_app(enforce_assignment=enforce_assignment)
    all_passed = True
    print(f"\n{title}")
    print("-" * len(title))

    try:
        for label, teacher_code, course_code, expected_codes in CASES:
            expected_status = (
                403 if enforce_assignment and label == "Huynh trưởng A xem lớp B" else 200
            )
            expected_response_codes = [] if expected_status == 403 else expected_codes
            response = make_client(app, teacher_code).get(
                f"/v1/courses/{course_code}/attendances"
            )
            body = response.get_json(silent=True) or {}
            codes = returned_student_codes(body)

            passed = (
                response.status_code == expected_status
                and codes == expected_response_codes
            )
            all_passed = all_passed and passed
            print(f"{'PASS' if passed else 'FAIL'} | {label}")
            print(f"  Mã HTTP: {response.status_code} (mong đợi {expected_status})")
            print(f"  Mã Thiếu nhi: {codes} (mong đợi {expected_response_codes})")
    finally:
        app.config["LAB_DB"].close()
    return all_passed


def main():
    before_ok = run_group("TRƯỚC KHI THÊM BƯỚC KIỂM TRA (mô phỏng: đã tắt kiểm tra phân công)", False)
    after_ok = run_group("SAU KHI THÊM BƯỚC KIỂM TRA (mô phỏng: đã bật kiểm tra phân công)", True)
    if not (before_ok and after_ok):
        raise SystemExit(1)
    print("\nPASS: mô phỏng cho kết quả trước/sau đúng như mong đợi.")
    print("Lưu ý: đây là mô hình học tập, không phải kiểm thử mã nguồn Gabriel.")


if __name__ == "__main__":
    main()

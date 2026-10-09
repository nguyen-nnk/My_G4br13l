**Project:** G4br13l  
**Investigation:** Kiểm tra quyền truy cập dữ liệu điểm danh giữa các lớp  
**Environment:** Local development environment, Flask test client, MySQL  
**Status:** Đã tái hiện hành vi trên dữ liệu giả và kiểm thử bản sửa cục bộ
## 1. Environment Setup

### 1.1. Check MySQL container

```bash
docker exec gabriel-mysql mysqladmin -u gabriel -pgabriel ping
```

Expected result:

```text
mysqld is alive
```

### 1.2. Check local backend

```bash
curl -s -o /dev/null -w "HTTP %{http_code}\n" \
  http://127.0.0.1:9001/api/guest
```

Expected result:

```text
HTTP 200
```


## 2. Test Data

**Database:** `gabriel_dev`

**Fake entities:**

| Entity    | Code         | Assigned class |
| --------- | ------------ | -------------- |
| Teacher A | `HQ261009T1` | `HQ261009A`    |
| Teacher B | `HQ261009T2` | `HQ261009B`    |
| Student A | `HQ261009S1` | `HQ261009A`    |
| Student B | `HQ261009S2` | `HQ261009B`    |
Các câu lệnh SQL trong database `gabriel_dev`

```sql
START TRANSACTION;

INSERT INTO grade (code, name, year_code, created_by)
VALUES ('HQ261009G', 'LAB Test Grade', '2023-2024', 'HQ-LAB');

INSERT INTO course (code, name, grade_code, shift_id, created_by)
VALUES
('HQ261009A', 'LAB Test Class A', 'HQ261009G', NULL, 'HQ-LAB'),
('HQ261009B', 'LAB Test Class B', 'HQ261009G', NULL, 'HQ-LAB');

INSERT INTO user
(code, level, baptism_name, last_name, first_name, gender,
 is_active, is_verified, created_by)
VALUES
('HQ261009T1', 'teacher', 'Test', 'Teacher', 'A',
 'male', 1, 1, 'HQ-LAB'),
('HQ261009T2', 'teacher', 'Test', 'Teacher', 'B',
 'female', 1, 1, 'HQ-LAB'),
('HQ261009S1', 'student', 'Test', 'Student', 'A',
 'male', 1, 1, 'HQ-LAB'),
('HQ261009S2', 'student', 'Test', 'Student', 'B',
 'female', 1, 1, 'HQ-LAB');

INSERT INTO users_courses
(user_code, course_code, level, is_abandoned, created_by)
VALUES
('HQ261009T1', 'HQ261009A', 'teacher', 0, 'HQ-LAB'),
('HQ261009S1', 'HQ261009A', 'student', 0, 'HQ-LAB'),
('HQ261009T2', 'HQ261009B', 'teacher', 0, 'HQ-LAB'),
('HQ261009S2', 'HQ261009B', 'student', 0, 'HQ-LAB');

INSERT INTO timetable
(course_code, date, title, is_required, is_day_off, created_by)
VALUES
('HQ261009A', '2024-01-07', 'LAB Attendance A', 1, 0, 'HQ-LAB'),
('HQ261009B', '2024-01-07', 'LAB Attendance B', 1, 0, 'HQ-LAB');

INSERT INTO attendance
(code, course_code, date, status, reason, created_by)
VALUES
('HQ261009S1', 'HQ261009A', '2024-01-07',
 'attendant', NULL, 'HQ-LAB'),
('HQ261009S2', 'HQ261009B', '2024-01-07',
 'absence_no_reason', NULL, 'HQ-LAB');

COMMIT;
```


Lệnh chạy thử nghiệm:

```bash
python - <<'PY'
import config
from app import app

def make_client(teacher_code):
    client = app.test_client()
    with client.session_transaction() as session:
        session[config.SESSION_AUTH_KEY] = {
            "code": teacher_code,
            "name": teacher_code,
            "level": "teacher",
            "isActive": True,
            "isForbidden": False,
        }
    return client

tests = [
    ("A xem lớp A", "HQ261009T1", "HQ261009A"),
    ("A xem lớp B", "HQ261009T1", "HQ261009B"),
    ("B xem lớp B", "HQ261009T2", "HQ261009B"),
]

for label, teacher_code, course_code in tests:
    client = make_client(teacher_code)
    response = client.get(
        f"/v1/courses/{course_code}/attendances"
    )
    body = response.get_json(silent=True) or {}

    student_codes = []
    for day in body.get("data", []) or []:
        for row in day.get("attendances", []) or []:
            student_codes.append(row.get("student_code"))

    print(f"\n--- {label} ---")
    print("HTTP:", response.status_code)
    print("Trạng thái:", body.get("status"))
    print("Mã Thiếu nhi trả về:", student_codes)
    print("Thông báo:", body.get("message"))
PY
```

Kết quả trước khi sửa:

| Trường hợp  | HTTP | Dữ liệu trả về |
| ----------- | ---: | -------------- |
| A xem lớp A |  200 | `HQ261009S1`   |
| A xem lớp B |  200 | `HQ261009S2`   |
| B xem lớp B |  200 | `HQ261009S2`   |
## 3. Implementing a local fix

Trong thư mục  server/route/course.py: 

Thêm ngay phía trên dòng (vì cần kiểm tra trước khi thực thi):

```python
rows = course_service.getAttendancesByCourseCode(course_code=code, date=date)
```

Đoạn code fix:

```python
user_courses = course_service.getUserCourses(
    user_code=g.user.code,
    year_code=course.get('year_code')
)

has_access = any(
    c.get('code') == code
    and c.get('level') in (
        UserLevel.TEACHER.value,
        UserLevel.ASSISTANT.value
    )
    and not c.get('is_abandoned')
    for c in user_courses
)

if not has_access:
    abort(403, "Bạn không có quyền xem điểm danh chi đoàn này")
## 5. Test Results

Endpoint:

```http
GET /v1/courses/<code>/attendances
```

Kết quả:

|Test case|Before patch|After patch|
|---|--:|--:|
|Teacher A → Class A|`200 OK`|`200 OK`|
|Teacher A → Class B|`200 OK`|`403 Forbidden`|
|Teacher B → Class B|`200 OK`|`200 OK`|

## 4. Patch Verification

```bash
git diff -- server/route/course.py
```

**Expected:** A new course-assignment authorization check in `getAttendancesByCourse()` before querying attendance records.

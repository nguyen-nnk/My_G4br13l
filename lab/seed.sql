-- Dữ liệu SQLite cho lab mô phỏng phân quyền điểm danh G4br13l.
-- Mọi mã định danh và bản ghi điểm danh đều là dữ liệu giả; không dùng schema Gabriel.
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS courses (
    code TEXT PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    code TEXT PRIMARY KEY,
    role TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS users_courses (
    user_code TEXT NOT NULL,
    course_code TEXT NOT NULL,
    level TEXT NOT NULL,
    is_abandoned INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (user_code, course_code, level),
    FOREIGN KEY (user_code) REFERENCES users(code),
    FOREIGN KEY (course_code) REFERENCES courses(code)
);

CREATE TABLE IF NOT EXISTS attendance (
    student_code TEXT NOT NULL,
    course_code TEXT NOT NULL,
    attendance_date TEXT NOT NULL,
    status TEXT NOT NULL,
    reason TEXT,
    PRIMARY KEY (student_code, course_code, attendance_date),
    FOREIGN KEY (student_code) REFERENCES users(code),
    FOREIGN KEY (course_code) REFERENCES courses(code)
);

INSERT INTO courses (code, name) VALUES
    ('HQ261009A', 'Lớp thử nghiệm A'),
    ('HQ261009B', 'Lớp thử nghiệm B')
ON CONFLICT(code) DO UPDATE SET name = excluded.name;

INSERT INTO users (code, role) VALUES
    ('HQ261009T1', 'teacher'),
    ('HQ261009T2', 'teacher'),
    ('HQ261009S1', 'student'),
    ('HQ261009S2', 'student')
ON CONFLICT(code) DO UPDATE SET role = excluded.role;

INSERT INTO users_courses (user_code, course_code, level, is_abandoned) VALUES
    ('HQ261009T1', 'HQ261009A', 'teacher', 0),
    ('HQ261009S1', 'HQ261009A', 'student', 0),
    ('HQ261009T2', 'HQ261009B', 'teacher', 0),
    ('HQ261009S2', 'HQ261009B', 'student', 0)
ON CONFLICT(user_code, course_code, level)
DO UPDATE SET is_abandoned = excluded.is_abandoned;

INSERT INTO attendance (student_code, course_code, attendance_date, status, reason) VALUES
    ('HQ261009S1', 'HQ261009A', '2024-01-07', 'attendant', NULL),
    ('HQ261009S2', 'HQ261009B', '2024-01-07', 'absence_no_reason', NULL)
ON CONFLICT(student_code, course_code, attendance_date)
DO UPDATE SET status = excluded.status, reason = excluded.reason;

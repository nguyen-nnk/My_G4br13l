"""Mô hình Flask/SQLite độc lập để minh họa phân quyền điểm danh theo lớp.

Đây là mô hình học tập, không phải ứng dụng Gabriel hay mã nguồn của ứng dụng đó.
"""
from pathlib import Path
import sqlite3

from flask import Flask, jsonify, session

LAB_DIR = Path(__file__).resolve().parent


def create_app(enforce_assignment: bool = True, database_path: str | None = None) -> Flask:
    """Tạo ứng dụng minh họa; có thể bật/tắt kiểm tra phân công để so sánh."""
    app = Flask(__name__)
    app.secret_key = "local-demo-only-do-not-use-in-production"
    app.config["ENFORCE_ASSIGNMENT"] = enforce_assignment

    db = sqlite3.connect(database_path or ":memory:", check_same_thread=False)
    db.row_factory = sqlite3.Row
    db.executescript((LAB_DIR / "seed.sql").read_text(encoding="utf-8"))
    db.commit()
    app.config["LAB_DB"] = db

    @app.get("/v1/courses/<course_code>/attendances")
    def get_attendances(course_code: str):
        teacher_code = session.get("teacher_code")
        if not teacher_code:
            return jsonify(status="unauthorized", data=[], message="Vui lòng đăng nhập"), 401

        course = db.execute(
            "SELECT code FROM courses WHERE code = ?", (course_code,)
        ).fetchone()
        if course is None:
            return jsonify(status="not_found", data=[], message="Không tìm thấy lớp"), 404

        if app.config["ENFORCE_ASSIGNMENT"]:
            assignment = db.execute(
                """SELECT 1 FROM users_courses
                   WHERE user_code = ? AND course_code = ?
                     AND level IN ('teacher', 'assistant')
                     AND is_abandoned = 0
                   LIMIT 1""",
                (teacher_code, course_code),
            ).fetchone()
            if assignment is None:
                return jsonify(
                    status="forbidden",
                    data=[],
                    message="Bạn không được phân công phụ trách lớp này",
                ), 403

        rows = db.execute(
            """SELECT student_code, attendance_date, status, reason
               FROM attendance
               WHERE course_code = ?
               ORDER BY attendance_date, student_code""",
            (course_code,),
        ).fetchall()
        grouped = {}
        for row in rows:
            grouped.setdefault(
                row["attendance_date"],
                {"date": row["attendance_date"], "attendances": []},
            )["attendances"].append({
                "student_code": row["student_code"],
                "status": row["status"],
                "reason": row["reason"],
            })
        return jsonify(status="ok", data=list(grouped.values()), message=None), 200

    return app


"""Small standalone Flask/SQLite model of class-level attendance authorization.

This is an educational simulation, not the Gabriel application or its source.
"""
from pathlib import Path
import sqlite3

from flask import Flask, jsonify, session

LAB_DIR = Path(__file__).resolve().parent


def create_app(enforce_assignment: bool = True, database_path: str | None = None) -> Flask:
    """Create a demo app; assignment enforcement can be toggled for comparison."""
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
            return jsonify(status="unauthorized", data=[], message="Login required"), 401

        course = db.execute(
            "SELECT code FROM courses WHERE code = ?", (course_code,)
        ).fetchone()
        if course is None:
            return jsonify(status="not_found", data=[], message="Course not found"), 404

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
                    message="You are not assigned to this class",
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


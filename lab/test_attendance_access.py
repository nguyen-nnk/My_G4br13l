"""Compare a simplified attendance endpoint before/after an assignment check.

Run with:
    python test_attendance_access.py

Uses only demo_app.py, Flask's test client, and SQLite fake data. It does NOT import Gabriel.
"""
from demo_app import create_app

CASES = [
    ("Teacher A -> Class A", "HQ261009T1", "HQ261009A", ["HQ261009S1"]),
    ("Teacher A -> Class B", "HQ261009T1", "HQ261009B", ["HQ261009S2"]),
    ("Teacher B -> Class B", "HQ261009T2", "HQ261009B", ["HQ261009S2"]),
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
                403 if enforce_assignment and label == "Teacher A -> Class B" else 200
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
            print(f"  HTTP: {response.status_code} (expected {expected_status})")
            print(f"  Student codes: {codes} (expected {expected_response_codes})")
    finally:
        app.config["LAB_DB"].close()
    return all_passed


def main():
    before_ok = run_group("BEFORE PATCH (simulated: assignment check disabled)", False)
    after_ok = run_group("AFTER PATCH (simulated: assignment check enabled)", True)
    if not (before_ok and after_ok):
        raise SystemExit(1)
    print("\nPASS: simulation produced the expected before/after behavior.")
    print("Note: this is an educational model, not a test of the Gabriel source code.")


if __name__ == "__main__":
    main()

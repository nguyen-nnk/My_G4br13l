# Lab Verification Record

- Date: 2026-10-10
- Scope: Standalone Flask + SQLite authorization demo
- Result: PASS — 6/6 checks

## Observed results

| Scenario | Before enforcement | After enforcement |
|---|---:|---:|
| Teacher A reads class A | 200 | 200 |
| Teacher A reads class B | 200 | 403 |
| Teacher B reads class B | 200 | 200 |

The test script verified both HTTP status codes and the
student codes returned by the endpoint.

## Conclusion

The standalone lab behaves as expected: a teacher assigned
to class A cannot retrieve class B attendance when assignment
enforcement is enabled, while legitimate access remains available.

## Limitations

- This is a simulated Flask + SQLite application.
- It does not execute the Gabriel production source.
- Authentication is simulated by creating a test session.
- The actual authorization policy must still be confirmed
  with the development team.
- Production behavior has not been verified.

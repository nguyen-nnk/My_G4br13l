# G4br13l — Security Case Study

> **From a commented-out decorator to a local authorization investigation.**

G4br13l is a student-led security case study based on exploring the Gabriel web application's source code. The investigation began after noticing a commented-out `@permission` decorator, then focused on a narrower question: should a teacher be able to read attendance records for a class they are not assigned to?

## Project map

| Part | Purpose |
|---|---|
| [Investigation WriteUp](docs/Project_G4br13l.md) | The investigation narrative: observation, hypotheses, proposed fix, retest and lessons learned. |
| [Lab Notebook](docs/G4br13l_Investigation.md) | Commands, experimental setup and notes from the original local investigation. |
| [Standalone Lab](lab/README.md) | A small Flask + SQLite model that demonstrates the authorization rule without importing Gabriel's source. |
| [Internal Review Artifacts](internal/README.md) | Source-specific patch and local schema prerequisites, kept separate from the standalone lab. |

## Finding under investigation

The original local experiment used fake assignments for two teachers and two classes. Before adding a class-assignment check, the local endpoint returned attendance data for Class B when requested by Teacher A, who was assigned only to Class A.

A proposed local fix checked the user's active class assignments before returning attendance. The recorded before/after results were:

| Test case | Before change | After change |
|---|---:|---:|
| Teacher A → Class A | `200 OK` | `200 OK` |
| Teacher A → Class B | `200 OK` | `403 Forbidden` |
| Teacher B → Class B | `200 OK` | `200 OK` |

These results are evidence from the local test setup, not confirmation that production has the same behavior or that the proposed rule matches the full business policy.

## Standalone lab

The self-contained lab in `lab/` uses Flask, SQLite, fake identifiers and Flask's test client. It is an educational simulation: it does not load, copy or execute the Gabriel application. Its purpose is to make the principle and expected test cases easy to reproduce.

Start with the [lab instructions](lab/README.md).

## Current status

- [x] Read the relevant route and related assignment logic.
- [x] Record the local experiment and its results.
- [x] Prepare a source-specific patch proposal for internal review.
- [x] Build a standalone teaching model with fake data.
- [ ] Run the standalone lab from a clean local environment and record the output.
- [ ] Confirm the intended class-access policy with Team Dev.
- [ ] Investigate cache behavior when assignments change or are revoked.
- [ ] Request review before considering a pull request.

## Scope and limitations

- The original app test used fake data on a local development setup.
- Its Flask test client simulated an already-authenticated session; the real login flow was not tested.
- The standalone demo is a model of the rule, not a reproduction of the entire Gabriel application.
- The proposed source patch has not been deployed and no pull request has been submitted.
- Production behavior and the final business authorization policy remain unconfirmed.

This repository is private while the investigation, source-specific artifacts and permissions are being reviewed. Do not make it public or share internal artifacts until the project owner/team has confirmed what may be disclosed.

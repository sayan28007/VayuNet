# VayuNet Release Candidate

Phase 13 freezes the repository for final hackathon submission.

## Freeze rule

After this phase, do not add new product features unless a change fixes a submission-blocking defect.

Allowed changes:
- build failures
- broken API contracts
- security or secret-leak fixes
- broken demo flow
- incorrect documentation
- deployment-blocking configuration errors

## Release checks

From the repository root:

```bash
python scripts/release_check.py
python scripts/submission_manifest.py
```

Then complete the backend and frontend checks documented in `docs/FINAL_QA.md`.

## Evidence rule

Every capability shown in the final demo must be either:
- verified by a live response,
- clearly documented as configured, or
- clearly labelled as synthetic/demo data.

Never present synthetic/demo data as live external monitoring.

# VayuNet Final QA

Phase 11 is the final verification layer after the Google Cloud integration work.

## 1. Repository hygiene

From the repository root:

```bash
python scripts/verify_repo.py
```

This must finish with a clean result. It checks for generated artifacts and credential-like files that should not be committed.

## 2. Backend checks

```bash
cd apps/backend
python -m compileall -q .
pytest -q
cd ../..
```

The Phase 11 tests cover:

- system health
- Google Cloud status surface
- hotspot API availability
- alert API availability
- federated status availability

These tests do not require a live Google Cloud project.

## 3. Frontend checks

```bash
cd apps/command-center
npm install
npm run build
cd ../..
```

Do not commit `node_modules/` or `.next/`.

## 4. Optional local smoke test

Start the backend first, then from the repository root:

```bash
python scripts/smoke_test.py
```

Or point it at another environment:

```bash
VAYUNET_API_URL="https://YOUR-BACKEND-URL/api/v1" python scripts/smoke_test.py
```

The smoke test only performs read-only requests.

## 5. Cloud verification rule

A service must not be described as live merely because its configuration exists.

For each Google Cloud service, record the actual observed state:

- configured
- unavailable
- not configured
- verified by a successful live request

Keep credentials in Secret Manager or the deployment environment, never in Git.

## 6. Final acceptance

Before submission:

- repository contains source files only
- no generated Python or frontend build artifacts
- no secrets or credentials
- backend tests pass
- frontend production build passes
- smoke test passes against the intended environment
- demo runbook has been followed once end-to-end

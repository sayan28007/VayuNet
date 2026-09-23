# VayuNet Submission Checklist

## Repository

- [ ] Final branch is pushed.
- [ ] Latest commit is visible on GitHub.
- [ ] No `.DS_Store`.
- [ ] No `__pycache__/`.
- [ ] No `.pyc`.
- [ ] No `node_modules/`.
- [ ] No `.next/`.
- [ ] No `.env`.
- [ ] No credentials, API keys, private keys, or service-account JSON files.

## Backend

- [ ] `python -m compileall -q .` passes.
- [ ] `pytest -q` passes.
- [ ] `/api/v1/health` responds.
- [ ] `/api/v1/cloud/status` responds.
- [ ] `/api/v1/hotspots` responds.
- [ ] `/api/v1/alerts` responds.
- [ ] `/api/v1/federation/status` responds.

## Frontend

- [ ] `npm run build` passes.
- [ ] Production API URL is supplied through `NEXT_PUBLIC_API_URL`.
- [ ] No secrets are embedded in the frontend.

## Google Cloud

- [ ] Cloud Run configuration is documented.
- [ ] Secret Manager usage is documented.
- [ ] BigQuery configuration is documented.
- [ ] Vertex AI/Gemini configuration is documented.
- [ ] Earth Engine configuration is documented.
- [ ] Any live-service claim has been verified by an actual request.

## Demo

- [ ] End-to-end demo run completed once.
- [ ] Demo can recover from an unavailable subsystem.
- [ ] Grounded Gemini answers use backend data.
- [ ] Federation status is visible.
- [ ] No hardcoded operational metric is presented as live.

## Submission

- [ ] README points to setup/deployment documentation.
- [ ] Architecture documentation is present.
- [ ] Demo runbook is present.
- [ ] Final QA is complete.

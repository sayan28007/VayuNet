# VayuNet Phase 7 Deployment

## Artifact Registry

```bash
gcloud artifacts repositories create vayunet-repo \
  --repository-format=docker \
  --location=us-central1 \
  --description="VayuNet Docker repository"
```

## Backend — Cloud Run

```bash
cd apps/backend
gcloud run deploy vayunet-backend \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars="GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID,BIGQUERY_DATASET=vayunet_prod" \
  --set-secrets="GEMINI_API_KEY=gemini-api-key:latest"
```

## Frontend — Cloud Build + Cloud Run

Run from the repository root after obtaining the deployed backend URL:

```bash
gcloud builds submit . \
  --config cloudbuild.frontend.yaml \
  --substitutions=_NEXT_PUBLIC_API_URL="https://BACKEND-URL/api/v1",_IMAGE="us-central1-docker.pkg.dev/YOUR_PROJECT_ID/vayunet-repo/vayunet-frontend:latest"
```

Then:

```bash
gcloud run deploy vayunet-frontend \
  --image us-central1-docker.pkg.dev/YOUR_PROJECT_ID/vayunet-repo/vayunet-frontend:latest \
  --region us-central1 \
  --allow-unauthenticated
```

## Notes

- Keep Gemini credentials in Secret Manager rather than committing them to the repository.
- Cloud Run supplies `PORT`; the backend container uses it at runtime.
- `NEXT_PUBLIC_API_URL` is embedded during the Next.js build, so pass the backend API URL to Cloud Build.
- IAM permissions and required Google Cloud APIs depend on the project configuration and should be enabled before deployment.

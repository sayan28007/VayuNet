# VayuNet Phase 10 — Google Cloud Integration

Phase 10 connects the existing VayuNet backend and command center to Google Cloud services without committing credentials.

## Services

- BigQuery stores a synchronized observation table.
- Secret Manager can supply the Gemini API key when a direct `GEMINI_API_KEY` environment variable is not available.
- Vertex AI is the preferred Gemini path when `GEMINI_USE_VERTEX_AI=true` and a Google Cloud project is configured.
- Earth Engine exposes recent Sentinel-5P NO2 collection metadata through a backend endpoint.
- Google Maps JavaScript API renders hotspot locations in the command center.

Google's current Python guidance uses client libraries for BigQuery and Secret Manager, and the current Vertex AI guidance uses the Google Gen AI SDK; Earth Engine supports Application Default Credentials for unattended workloads. citeturn364916search1turn364916search0turn417292search1turn417292search2

## Enable APIs

```bash
gcloud services enable \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com \
  bigquery.googleapis.com \
  secretmanager.googleapis.com \
  aiplatform.googleapis.com \
  earthengine.googleapis.com
```

## BigQuery

`POST /api/v1/cloud/bigquery/sync` creates the configured dataset/table when the runtime identity is permitted to do so, then writes the current observation repository contents. `GET /api/v1/cloud/bigquery/observations?limit=50` reads recent rows.

Default dataset: `vayunet_prod`.

Default table: `observations`.

## Secret Manager

Create the secret used by the Gemini fallback path:

```bash
echo -n "YOUR_GEMINI_API_KEY" | gcloud secrets versions add gemini-api-key --data-file=-
```

Grant the Cloud Run runtime service account access to the secret. Never commit secret values or service-account JSON keys.

## Vertex AI

The preferred production Gemini path uses the Google Gen AI SDK with Vertex AI and Application Default Credentials:

```text
GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID
GOOGLE_CLOUD_LOCATION=global
GEMINI_USE_VERTEX_AI=true
VERTEX_AI_MODEL_NAME=gemini-2.5-flash
```

Google's current Vertex AI quickstart uses `google-genai` and `genai.Client(..., vertexai=True, project=..., location=...)`. citeturn417292search1turn417292search9

## Earth Engine

The default collection is:

```text
COPERNICUS/S5P/NRTI/L3_NO2
```

Google's Earth Engine Data Catalog documents this as a near-real-time Sentinel-5P/TROPOMI NO2 collection. citeturn361040search1

Endpoint:

```text
GET /api/v1/cloud/earth-engine/latest?days=7
```

For local authentication, Earth Engine documents `ee.Authenticate()` and `ee.Initialize(project='PROJECT_ID')`. For unattended environments, Application Default Credentials are supported. citeturn417292search0turn417292search2

## Google Maps

Set the frontend build-time variable:

```text
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=YOUR_RESTRICTED_BROWSER_KEY
```

The key should be restricted to the deployed web origins. Google currently documents direct script loading and the `@googlemaps/js-api-loader` package as supported Maps JavaScript loading approaches; this implementation uses the direct script loader and adds no new frontend package. citeturn364916search3turn364916search7

## Local authentication

```bash
gcloud auth application-default login
```

Application Default Credentials are used by the Google Cloud client libraries in this phase. citeturn364916search0turn417292search0

## Cloud Run notes

Use the Cloud Run runtime service account for production authentication. Keep sensitive values in Secret Manager and pass only non-sensitive configuration through environment variables.

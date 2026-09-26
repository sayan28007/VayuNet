# VayuNet: AI-Powered Federated Climate Action Platform

VayuNet is an AI-powered climate and pollution intelligence platform designed to detect hyper-local pollution events, combine heterogeneous evidence, forecast near-term risk, estimate exposure, coordinate authority response, and learn across participating city nodes without requiring raw local data to leave the node.

VayuNet follows a closed operational loop:

**OBSERVE → UNDERSTAND → DETECT → PREDICT → ALERT → COORDINATE → LEARN**

---

## What VayuNet Does

VayuNet is built around a multi-layered intelligence pipeline for pollution and climate-action workflows.

### 1. Observe

The platform supports multiple observation types:

- `citizen_report`
- `local_sensor`
- `official_monitor`
- `meteorological`
- `satellite`
- `synthetic_demo`

Observation data is accessed through a repository abstraction so the application logic is separated from the underlying storage implementation.

### 2. Detect

The intelligence layer identifies hyper-local pollution hotspots by combining available evidence and scoring signals such as:

- evidence count
- source diversity
- anomaly score
- spatial score
- data quality
- confidence
- pollutant information

The platform is designed to surface a **likely incident/source with uncertainty**, rather than making an unsupported exact-facility claim.

### 3. Predict

For a selected hotspot, VayuNet provides:

- near-term AQI forecasts
- plume/spread projections
- population exposure estimates
- corridor-level predictions
- time-to-peak and confidence information

### 4. Respond

The Command Center provides a state-machine driven alert workflow:

```text
DETECTED
   ↓
VALIDATING
   ↓
HIGH_CONFIDENCE
   ↓
ROUTED
   ↓
ACKNOWLEDGED
   ↓
ACTION_IN_PROGRESS
   ↓
RESOLVED
```

Authority actions include routing, acknowledgement, action deployment, and resolution.

### 5. Ask Gemini

The backend provides a tool-using Gemini agent endpoint for operational questions.

The agent can use backend intelligence results and return:

- answer
- tools used
- grounding information
- data sources
- selected language

The system is designed so the assistant is grounded in application data rather than acting as a decorative standalone chatbot.

### 6. Learn Across Nodes

VayuNet includes a federated-learning prototype with three simulated city nodes:

- Delhi
- Visakhapatnam
- Mumbai

The federation layer demonstrates:

- local model training
- weighted aggregation
- FedAvg-style global updates
- model versioning
- node health/failure handling
- global federation status

Raw local observations do not need to be centrally pooled for the federation workflow.

---

# System Architecture

```text
                         ┌──────────────────────────┐
                         │   Next.js Command Center  │
                         │   Maps + Dashboard + AI   │
                         └────────────┬─────────────┘
                                      │
                                      ▼
                         ┌──────────────────────────┐
                         │      FastAPI Backend      │
                         │      API / Gateway        │
                         └────────────┬─────────────┘
                                      │
          ┌───────────────────────────┼───────────────────────────┐
          │                           │                           │
          ▼                           ▼                           ▼
┌──────────────────┐       ┌──────────────────┐       ┌──────────────────┐
│ Data Ingestion   │       │ Intelligence / ML │       │ Response / Alerts│
│ Observations     │       │ Hotspots          │       │ Routing          │
│ Evidence         │       │ Forecast          │       │ Workflow         │
└────────┬─────────┘       │ Plume            │       └────────┬─────────┘
         │                 │ Exposure         │                │
         │                 │ Corridors        │                │
         │                 └────────┬─────────┘                │
         │                          │                          │
         └──────────────────────────┼──────────────────────────┘
                                    ▼
                         ┌──────────────────────────┐
                         │ Federation / FedAvg      │
                         │ Delhi / Vizag / Mumbai   │
                         └────────────┬─────────────┘
                                      │
                                      ▼
                         ┌──────────────────────────┐
                         │ Google Cloud Integrations│
                         │ BigQuery                 │
                         │ Secret Manager            │
                         │ Vertex AI / Gemini        │
                         │ Earth Engine              │
                         │ Maps                      │
                         │ Cloud Run / Cloud Build   │
                         └──────────────────────────┘
```

---

# Repository Structure

```text
VayuNet/
├── apps/
│   ├── backend/
│   │   ├── app/
│   │   │   ├── agent/
│   │   │   ├── cloud/
│   │   │   ├── data/
│   │   │   ├── federation/
│   │   │   ├── intelligence/
│   │   │   ├── models/
│   │   │   ├── prediction/
│   │   │   ├── repositories/
│   │   │   ├── response/
│   │   │   ├── routers/
│   │   │   ├── services/
│   │   │   └── utils/
│   │   ├── Dockerfile
│   │   ├── main.py
│   │   └── requirements.txt
│   │
│   └── command-center/
│       ├── app/
│       ├── components/
│       ├── lib/
│       ├── types/
│       ├── package.json
│       ├── next.config.mjs
│       └── ...
│
├── docs/
│   ├── ARCHITECTURE.md
│   ├── DEMO.md
│   ├── DEMO_PRESENTATION.md
│   ├── DEMO_RUNBOOK.md
│   ├── DEPLOYMENT.md
│   ├── FINAL_QA.md
│   ├── FINAL_SUBMISSION.md
│   ├── PHASE10_CLOUD_SETUP.md
│   ├── RELEASE_CANDIDATE.md
│   ├── SCREENSHOT_GUIDE.md
│   ├── SUBMISSION_CHECKLIST.md
│   └── VIVA_QA.md
│
├── scripts/
│   ├── release_check.py
│   ├── smoke_test.py
│   ├── submission_manifest.py
│   └── verify_repo.py
│
├── cloudbuild.frontend.yaml
├── docker-compose.yml
└── README.md
```

---

# Technology Stack

## Frontend

- Next.js 14
- React 18
- TypeScript
- Tailwind CSS
- Lucide React
- Google Maps JavaScript API integration

The command center includes dashboard views for:

- overview metrics
- hotspots
- alerts
- predictions
- corridors
- federated learning
- Gemini interaction
- cloud-service status
- demo flow and impact story

## Backend

- Python 3.11
- FastAPI
- Pydantic
- Uvicorn
- repository abstractions
- intelligence/prediction services
- federation services
- Gemini/Google Cloud integrations

## Google Cloud

The repository contains integration paths for:

- BigQuery
- Secret Manager
- Vertex AI / Gemini
- Earth Engine
- Google Maps
- Cloud Run
- Cloud Build
- Artifact Registry

---

# Core API Areas

The backend exposes versioned APIs under:

```text
/api/v1
```

Important route groups include:

```text
GET  /api/v1/health
GET  /api/v1/readiness

GET  /api/v1/hotspots
GET  /api/v1/alerts
GET  /api/v1/alerts/{event_id}

POST /api/v1/alerts/{event_id}/route
POST /api/v1/alerts/{event_id}/acknowledge
POST /api/v1/alerts/{event_id}/action
POST /api/v1/alerts/{event_id}/resolve

GET  /api/v1/predictions/forecast/{hotspot_id}
GET  /api/v1/predictions/plume/{hotspot_id}
GET  /api/v1/predictions/exposure/{hotspot_id}
GET  /api/v1/predictions/corridors

GET  /api/v1/federation/status
GET  /api/v1/federation/nodes
GET  /api/v1/federation/rounds
POST /api/v1/federation/round

POST /api/v1/agent/chat

POST /api/v1/demo/run
POST /api/v1/demo/reset

GET  /api/v1/cloud/status
POST /api/v1/cloud/bigquery/sync
GET  /api/v1/cloud/bigquery/observations
GET  /api/v1/cloud/earth-engine/latest
GET  /api/v1/cloud/secret-manager/status
POST /api/v1/cloud/vertex-ai/generate
```

---

# Local Development

## Prerequisites

Recommended:

- Python 3.11
- Node.js compatible with the Next.js project
- npm
- Git

---

## Run the Backend

```bash
cd apps/backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Backend:

```text
http://localhost:8000
```

API base:

```text
http://localhost:8000/api/v1
```

---

## Run the Command Center

Open another terminal:

```bash
cd apps/command-center
npm install
npm run dev
```

Frontend:

```text
http://localhost:3000
```

---

# Environment Variables

The backend configuration supports environment-based configuration for local and cloud deployments.

Important variables include:

```text
APP_NAME
APP_VERSION
ENVIRONMENT
LOG_LEVEL

BACKEND_HOST
BACKEND_PORT
CORS_ORIGINS

GCP_PROJECT_ID
GOOGLE_CLOUD_PROJECT
GOOGLE_CLOUD_LOCATION

GEMINI_API_KEY
GEMINI_SECRET_ID
GEMINI_MODEL_NAME
GEMINI_USE_VERTEX_AI

BIGQUERY_DATASET
BIGQUERY_OBSERVATIONS_TABLE

VERTEX_AI_MODEL_NAME
EARTH_ENGINE_COLLECTION
```

Typical cloud configuration:

```text
GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID
GOOGLE_CLOUD_LOCATION=global
GEMINI_USE_VERTEX_AI=true
VERTEX_AI_MODEL_NAME=gemini-2.5-flash
BIGQUERY_DATASET=vayunet_prod
BIGQUERY_OBSERVATIONS_TABLE=observations
EARTH_ENGINE_COLLECTION=COPERNICUS/S5P/NRTI/L3_NO2
```

Do not commit API keys, service-account JSON files, or other secrets.

---

# Google Cloud Integration

Phase 10 adds the cloud integration layer.

## BigQuery

The backend can synchronize observation data into the configured dataset/table.

Default:

```text
Dataset: vayunet_prod
Table:   observations
```

Endpoints:

```text
POST /api/v1/cloud/bigquery/sync
GET  /api/v1/cloud/bigquery/observations?limit=50
```

## Secret Manager

Gemini credentials can be resolved through Secret Manager when a direct API-key environment variable is not available.

Example secret name:

```text
gemini-api-key
```

## Vertex AI / Gemini

Vertex AI is the preferred production Gemini path when:

```text
GEMINI_USE_VERTEX_AI=true
```

and a Google Cloud project is configured.

## Earth Engine

The project exposes recent Sentinel-5P NO2 collection metadata using:

```text
COPERNICUS/S5P/NRTI/L3_NO2
```

Endpoint:

```text
GET /api/v1/cloud/earth-engine/latest?days=7
```

## Google Maps

The frontend can use:

```text
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY
```

Use a browser-restricted key for deployed environments.

---

# Docker

Backend container:

```bash
cd apps/backend
docker build -t vayunet-backend .
docker run -p 8000:8000 vayunet-backend
```

The repository also includes:

```text
docker-compose.yml
```

for local multi-service development.

---

# Deployment

The repository contains deployment configuration and documentation for Google Cloud.

## Backend — Cloud Run

The backend is containerized and can be deployed to Cloud Run.

Typical flow:

```bash
cd apps/backend

gcloud run deploy vayunet-backend \
  --source . \
  --region us-central1 \
  --allow-unauthenticated
```

The backend uses the Cloud Run `PORT` environment variable at runtime.

## Frontend — Cloud Build / Cloud Run

The repository contains:

```text
cloudbuild.frontend.yaml
```

The Next.js frontend requires the backend API URL at build time.

Example:

```bash
gcloud builds submit . \
  --config cloudbuild.frontend.yaml \
  --substitutions=_NEXT_PUBLIC_API_URL="https://BACKEND-URL/api/v1"
```

The generated frontend can then be deployed to Cloud Run.

## Vercel

The command center can also be deployed as a standalone Next.js application using:

```text
Root Directory: apps/command-center
Build Command: npm run build
```

The production frontend should point `NEXT_PUBLIC_API_URL` at the deployed backend API.

---

# Demo Flow

The final demo is designed around a five-minute operational story.

## 1. Problem

Pollution information is fragmented across sensors, citizens, official monitors, weather and satellite signals.

## 2. Detect

Show the Command Center and hotspot list.

Explain that VayuNet fuses evidence and surfaces a likely incident with uncertainty.

## 3. Predict

Select a hotspot and show:

- AQI forecast
- plume projection
- population exposure

## 4. Respond

Open the authority response panel and demonstrate:

```text
Route → Acknowledge → Deploy Action → Resolve
```

## 5. Ask Gemini

Ask an operational question and show the tools/data used to ground the response.

## 6. Learn

Open the federation panel and show the three simulated nodes and global model version.

Final loop:

```text
Detect → Predict → Explain → Route → Learn
```

---

# Demonstration and Data Integrity

VayuNet distinguishes between:

- live/verified external service responses
- configured integrations
- synthetic/demo data

Synthetic data must never be presented as live external monitoring.

The release candidate follows the rule:

> Every capability shown in the final demo must be verified by a live response, clearly documented as configured, or clearly labelled as synthetic/demo data.

---

# Testing and QA

Repository validation scripts include:

```bash
python scripts/verify_repo.py
python scripts/smoke_test.py
python scripts/release_check.py
python scripts/submission_manifest.py
```

Frontend production build:

```bash
cd apps/command-center
npm install
npm run build
```

Backend tests and final QA are documented in:

```text
docs/FINAL_QA.md
docs/SUBMISSION_CHECKLIST.md
```

---

# Release Candidate

Phase 13 freezes VayuNet for final submission.

Release rule:

After the release-candidate freeze, do not add new product features unless the change fixes a submission-blocking defect.

Allowed post-freeze changes include:

- build failures
- broken API contracts
- security or secret-leak fixes
- broken demo flow
- incorrect documentation
- deployment-blocking configuration errors

Release checks:

```bash
python scripts/release_check.py
python scripts/submission_manifest.py
```

---

# Documentation

Detailed documentation is available in `docs/`:

| Document | Purpose |
|---|---|
| `ARCHITECTURE.md` | Technical architecture |
| `DEMO.md` | Demo workflow |
| `DEMO_PRESENTATION.md` | Five-minute presentation flow |
| `DEMO_RUNBOOK.md` | Demo execution checklist |
| `DEPLOYMENT.md` | Cloud deployment |
| `FINAL_QA.md` | Final QA checks |
| `FINAL_SUBMISSION.md` | Submission requirements |
| `PHASE10_CLOUD_SETUP.md` | Google Cloud setup |
| `RELEASE_CANDIDATE.md` | Release freeze rules |
| `SCREENSHOT_GUIDE.md` | Screenshot guidance |
| `SUBMISSION_CHECKLIST.md` | Submission checklist |
| `VIVA_QA.md` | Viva/demo questions and answers |

---

# Project Principles

VayuNet is built around the following principles:

- **Evidence over unsupported claims**
- **Uncertainty is explicit**
- **Local data stays local where federation allows**
- **Operational actions are state-machine driven**
- **AI is grounded in backend tools and results**
- **Cloud credentials are never committed**
- **Synthetic data is clearly identified**
- **Production builds and demo flows are validated before submission**

---

# Final Architecture Summary

```text
OBSERVE
   ↓
UNDERSTAND
   ↓
DETECT
   ↓
PREDICT
   ↓
EXPLAIN
   ↓
ALERT
   ↓
ROUTE
   ↓
RESPOND
   ↓
LEARN
   ↓
FEDERATE
```

VayuNet is intended to turn fragmented pollution signals into an operational intelligence loop that can support faster detection, prediction, coordinated response, and privacy-aware learning across participating locations.

---

## License

This project is currently maintained as a hackathon / prototype project. Add the final project license here before public production distribution.

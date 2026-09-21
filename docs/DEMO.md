# VayuNet Phase 9 Demo Runbook

Phase 9 hardens the existing VayuNet pipeline for a repeatable local demo. Synthetic/demo signals remain explicitly identified by the backend where used.

## Start

Backend:

```bash
cd apps/backend
python -m uvicorn main:app --reload
```

Frontend:

```bash
cd apps/command-center
npm run dev
```

## Readiness

Check:

```text
GET /api/v1/health
GET /api/v1/ready
```

The readiness endpoint checks the observation repository, federation availability, and baseline configuration.

## Demo controls

The Command Center exposes **Run Demo** and **Reset Demo**.

```text
POST /api/v1/demo/run
POST /api/v1/demo/reset
```

Run Demo evaluates current hotspots, initializes alerts when needed, and executes one federated learning round.

Reset Demo clears alert and federation shared state, resets prediction caching, and rebuilds the baseline demo state from the existing observation repository.

## Alert workflow

The operational state machine can now be demonstrated end-to-end:

```text
HIGH_CONFIDENCE -> ROUTED -> ACKNOWLEDGED -> ACTION_IN_PROGRESS -> RESOLVED
```

## Expected flow

```text
Telemetry
   -> Hotspot detection
   -> Prediction / plume / exposure
   -> Alert generation
   -> Authority response state machine
   -> Gemini grounded query
   -> Federated learning round
```

## Failure handling

The UI keeps alert, prediction, corridor, federation, and Gemini failures isolated. A failed subsystem is shown as unavailable instead of taking down the complete Command Center.

Unexpected backend exceptions return a generic `500` response while detailed exceptions are logged server-side.

## Scope

Phase 9 does not claim live BigQuery, Firebase, Vertex AI, government, or satellite connectivity. Those remain separate integration work unless a service explicitly reports otherwise.

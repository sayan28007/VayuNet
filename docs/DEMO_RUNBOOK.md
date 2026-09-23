# VayuNet Final Demo Runbook

Target demo flow:

1. Open the Command Center.
2. Confirm backend/system status is visible.
3. Show active pollution hotspots.
4. Select a hotspot and show:
   - AQI forecast
   - plume movement
   - population exposure
5. Show corridor risk predictions.
6. Show authority alerts and their state-machine workflow.
7. Ask Gemini a grounded question such as:
   - "Which hotspot needs attention and why?"
   - "What is the predicted AQI trend?"
   - "How many people are estimated to be exposed?"
8. Show federated learning status and the current global model version.
9. Show Google Cloud service status.
10. Run the demo sequence/reset only when needed.

## Demo discipline

Use only values returned by the application.

When a service is unavailable, show the application state and explain that the integration is configured for deployment but the live service is not currently reachable.

Do not invent live AQI, population, satellite, or cloud-service results.

## Fast recovery

If one subsystem fails:

- continue with the other panels
- use the visible error state
- retry the read-only request
- use the demo/reset control only when appropriate

The goal is to demonstrate graceful degradation rather than hide an unavailable service.

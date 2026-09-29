# VayuNet Vercel Standalone Demo Fix

Deadline-safe frontend fix: Vercel runs the full demo without any backend.

REPLACE
- apps/command-center/lib/api.ts
- apps/command-center/components/Hotspots.tsx

What changes
- Stops localhost:8000 API calls in the deployed demo by default.
- Supplies realistic demo hotspots, alerts, forecasts, plume, exposure, corridors and federation data.
- Run Demo / Reset Demo work entirely in the browser.
- Gemini panel gets a grounded demo response in English/Hindi/Telugu.
- Alert response buttons update demo state locally.
- Hotspot score displays as a percentage.

Later, when a real backend is available, set NEXT_PUBLIC_DEMO_MODE=false and set NEXT_PUBLIC_API_URL to the backend API base.

Commit message:
fix: make Vercel command center self-contained for demo

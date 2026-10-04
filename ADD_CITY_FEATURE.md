# VayuNet Add City Feature

## Files
1. `apps/command-center/components/CitySelector.tsx` -> NEW
2. `apps/command-center/app/page.tsx` -> REPLACE
3. `ADD_CITY_FEATURE.md` -> NEW

## What it adds
- City selector at the top of the command center
- All Cities view
- Visakhapatnam, Delhi and Mumbai as initial cities
- Add City button with browser-local persistence
- Hotspots and alerts filtered by selected city
- Map filtered to the selected city
- Selected hotspot resets when city changes

Current demo data only contains the three existing cities. A newly added city will appear in the selector immediately; its real AQI/hotspot data will populate once the real data ingestion phase is connected.

Commit:
`feat: add multi-city command center selector`

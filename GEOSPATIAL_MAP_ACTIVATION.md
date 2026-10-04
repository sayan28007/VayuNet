# VayuNet Geospatial Map Activation

## REPLACE
`apps/command-center/app/page.tsx`

The repo already contains `apps/command-center/components/OperationalMap.tsx`. This change replaces the placeholder map with the live Google Maps component.

## Vercel Environment Variable
Add:
`NEXT_PUBLIC_GOOGLE_MAPS_API_KEY`

Google Maps JavaScript API requires an API key. Standard usage requires billing; Google also provides a Maps Demo Key for no-billing prototyping. Restrict a standard browser key to the Vercel website and Maps JavaScript API.

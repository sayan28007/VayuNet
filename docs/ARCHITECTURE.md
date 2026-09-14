# VayuNet Technical Architecture Specification
Reactive and predictive loop: OBSERVE -> UNDERSTAND -> DETECT -> PREDICT -> ALERT -> COORDINATE -> LEARN

## Phase 2: Data Ingestion & Geospatial Foundation
### Storage Abstraction
The system utilizes a Repository Pattern (`ObservationRepository`). This decouples business logic from the database layer, allowing seamless transition from local memory-based development to Google BigQuery/Cloud SQL in production.

### Geospatial Filtering
Coordinates are validated via strict Pydantic rules (Lat -90 to 90, Lon -180 to 180). Geospatial boundaries are calculated using the Haversine formula for radius searches and standard coordinate boundaries for bounding boxes.

### Source Types
Data is classified strictly into: `citizen_report`, `local_sensor`, `official_monitor`, `meteorological`, `satellite`, and `synthetic_demo`.


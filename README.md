# VayuNet: AI-Powered Federated Climate Action Platform

VayuNet is a multi-layered climate intelligence platform designed to detect hyper-local pollution events.

## Current Status: Phase 2 Complete (Data Ingestion & Geospatial Foundation)
- Typed data models for pollution & meteorological observations.
- Extensible repository pattern (currently using in-memory local storage, BigQuery-ready).
- Geospatial utilities for bounding box and radius filtering.
- Synthetic demo data generation for Indian cities and economic corridors.
- Typed Next.js API client and real-time data dashboard.

## Quick Start (Local Development)
1. **Backend API Gateway:**
   ```bash
   cd apps/backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   uvicorn main:app --reload --port 8000


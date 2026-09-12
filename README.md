# VayuNet: AI-Powered Federated Climate Action Platform

VayuNet is a multi-layered climate intelligence platform designed to detect hyper-local pollution events.

## Quick Start (Local Development)

### Backend API Gateway

```bash
cd apps/backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend Command Center

```bash
cd apps/command-center
npm install
npm run dev
```

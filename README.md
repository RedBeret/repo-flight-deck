# Repo Flight Deck

Repo Flight Deck is a full-stack control center for engineering teams that need a fast read on repository health, CI status, security alerts, release readiness, and risky pull requests.

This project is designed to show the developer-platform and internal-tooling side of the portfolio:

- operational dashboards for software teams
- structured API design for repo health data
- release readiness workflows instead of raw data dumps
- clear, credible UI for engineering leads and maintainers

## Current MVP

- Repo catalog with search and risk filtering
- Selected repo dashboard with CI health, release gate, and signal cards
- Pull request board with ownership, risk, and merge blockers
- Security alert panel and release-readiness checklist
- Exportable JSON risk packet for handoff or review

## Stack

- Frontend: React, TypeScript, Vite
- Backend: FastAPI
- Data: seeded internal-tool style repository data

## Local Development

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8020
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The Vite dev server proxies API traffic to `http://127.0.0.1:8020`.

## Verification

- `python -m unittest discover -s backend\tests -v`
- `python -m compileall backend\app`
- `npm run build`

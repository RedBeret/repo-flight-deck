# Repo Flight Deck

Repo Flight Deck gives platform and release engineers a structured view of repository health, open pull requests, security alerts, and release gate status. When a repo is close to cutting or is in a hotfix channel, this is the tool that tells you what is actually blocking you.

The risk engine scores each repo on a 0-100 scale. Scores below 80 put the repo in `low` status. Between 80-89 it is `review`. Above 90 it is `high`. Risk level determines which repos surface first in the queue and what shows up in the risk export.

## What the dashboard shows you

- All repos with health score, open PR count, security alert count, and release readiness
- Filter by risk level, team, or search by repo name
- Select a repo to see detailed signals, individual PR risk ratings, alert severity breakdown, and the release readiness checklist
- One-click risk export as JSON for handoffs or tooling

## How the risk score is calculated

The health score is the primary input. A `high` risk repo has a health score below 80 and one or more of the following:

- 3 or more open security alerts
- 6 or more open pull requests
- Release readiness checklist with 2 or more blocked items
- CI failure rate above 20% on the default branch

A `review` repo is in the 80-89 health band with at least one open alert or PR. A `low` repo is healthy enough to cut without flags.

PRs within a repo are rated individually. A PR is `high` risk if it touches CI configuration, security scanning, or release workflows. It is `medium` if it changes core application logic. `low` if it is docs, tooling, or dependency updates.

## Risk export output

When you need to hand off a repo status to a lead or write up a release summary, the risk export gives you a structured packet:

```json
{
  "repoId": "RFD-102",
  "repoName": "edge-agent-runtime",
  "lead": "Platform rotation",
  "releaseChannel": "hotfix",
  "risk": "high",
  "executiveSummary": "edge-agent-runtime is currently rated high with 4 open PRs and 4 security alerts. Highest-priority concern: Container base image CVE.",
  "checks": [
    {"name": "Unit tests", "status": "review"},
    {"name": "Container publish", "status": "failed"},
    {"name": "Security scan", "status": "review"},
    {"name": "Release build", "status": "failed"}
  ],
  "actions": [
    "Land the cache-restore retry PR and rerun the release build.",
    "Patch the base image CVE before approving the runtime dependency upgrade.",
    "Reduce the open PR queue before taking on the larger runtime branch."
  ]
}
```

The goal is to get from "I need to know the status of this repo" to "here is what is blocking the release and what needs to happen next" in one copy-paste.

## Local development

### Backend

```bash
cd backend
python -m venv .venv
.venv/bin/activate
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

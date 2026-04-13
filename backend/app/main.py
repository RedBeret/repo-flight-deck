from __future__ import annotations

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .data import get_dashboard
from .data import get_release_packet
from .data import get_repo_detail
from .data import get_risk_export

app = FastAPI(title="Repo Flight Deck API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/repos")
def repo_dashboard() -> dict:
    return get_dashboard()


@app.get("/api/repos/{repo_id}")
def repo_detail(repo_id: str) -> dict:
    try:
        return get_repo_detail(repo_id)
    except KeyError as error:
        raise HTTPException(status_code=404, detail="Repository not found") from error


@app.get("/api/repos/{repo_id}/release-packet")
def release_packet(repo_id: str) -> dict:
    try:
        return get_release_packet(repo_id)
    except KeyError as error:
        raise HTTPException(status_code=404, detail="Release packet not found") from error


@app.get("/api/repos/{repo_id}/risk-export")
def risk_export(repo_id: str) -> dict:
    try:
        return get_risk_export(repo_id)
    except KeyError as error:
        raise HTTPException(status_code=404, detail="Risk export not found") from error

from __future__ import annotations

from copy import deepcopy
from statistics import mean
from typing import Any


REPOS: list[dict[str, Any]] = [
    {
        "id": "RFD-101",
        "name": "mission-console",
        "team": "operator-ui",
        "risk": "review",
        "health": 88,
        "openPrs": 6,
        "securityAlerts": 2,
        "releaseReady": False,
        "summary": "Operator dashboard is stable overall, but a stale auth refactor and one flaky visual test are blocking the next cut.",
    },
    {
        "id": "RFD-102",
        "name": "edge-agent-runtime",
        "team": "platform",
        "risk": "high",
        "health": 72,
        "openPrs": 9,
        "securityAlerts": 4,
        "releaseReady": False,
        "summary": "Runtime branch is carrying too many open changes and CI is failing on cross-platform packaging checks.",
    },
    {
        "id": "RFD-103",
        "name": "telemetry-ingest",
        "team": "data-platform",
        "risk": "low",
        "health": 94,
        "openPrs": 3,
        "securityAlerts": 1,
        "releaseReady": True,
        "summary": "Ingest service is healthy with one low-priority alert and a release candidate that is ready once docs land.",
    },
]


REPO_DETAILS: dict[str, dict[str, Any]] = {
    "RFD-101": {
        "id": "RFD-101",
        "name": "mission-console",
        "team": "operator-ui",
        "risk": "review",
        "health": 88,
        "releaseChannel": "candidate",
        "lead": "Steven",
        "summary": "UI branch is close to ready, but one auth cleanup PR and a flaky visual snapshot suite are still creating drag.",
        "signals": [
            {"label": "CI success rate", "value": "93%", "trend": "up"},
            {"label": "Review turnaround", "value": "14h", "trend": "down"},
            {"label": "Security alerts", "value": "2", "trend": "flat"},
        ],
        "checks": [
            {"name": "Unit tests", "status": "passed", "detail": "12m average runtime across the last five runs."},
            {"name": "Visual snapshots", "status": "review", "detail": "Failing intermittently in Safari viewport coverage."},
            {"name": "Security scan", "status": "passed", "detail": "No blocking issues in the latest scan."},
            {"name": "Release build", "status": "review", "detail": "Waiting on auth refactor PR before cutting release candidate."},
        ],
        "pullRequests": [
            {"id": 412, "title": "Refactor auth token refresh flow", "owner": "frontend", "risk": "high", "status": "needs changes"},
            {"id": 418, "title": "Improve dashboard event grouping", "owner": "ux-platform", "risk": "medium", "status": "ready"},
            {"id": 421, "title": "Reduce duplicate polling on run cards", "owner": "frontend", "risk": "low", "status": "in review"},
        ],
        "alerts": [
            {"severity": "medium", "title": "Outdated markdown renderer", "detail": "Low exposure path, but should be bumped before next public release."},
            {"severity": "low", "title": "Lint rule drift in CI config", "detail": "No direct release risk, but still causing noise in branch checks."},
        ],
        "releaseReadiness": [
            {"label": "CI green on default branch", "status": "done"},
            {"label": "Auth cleanup merged", "status": "blocked"},
            {"label": "Release notes drafted", "status": "done"},
            {"label": "Final smoke test completed", "status": "todo"},
        ],
        "actions": [
            "Finish auth refactor review and merge it before the release cut.",
            "Stabilize Safari visual snapshots or mark the flaky spec as quarantined.",
            "Run one full smoke pass after the dashboard polling fix merges.",
        ],
    },
    "RFD-102": {
        "id": "RFD-102",
        "name": "edge-agent-runtime",
        "team": "platform",
        "risk": "high",
        "health": 72,
        "releaseChannel": "hotfix",
        "lead": "Platform rotation",
        "summary": "Packaging checks are red, the open PR queue is overloaded, and the repo is carrying too many release-candidate changes at once.",
        "signals": [
            {"label": "CI success rate", "value": "71%", "trend": "down"},
            {"label": "Review turnaround", "value": "29h", "trend": "up"},
            {"label": "Security alerts", "value": "4", "trend": "up"},
        ],
        "checks": [
            {"name": "Unit tests", "status": "review", "detail": "Linux is green, but Windows packaging failures are trending upward."},
            {"name": "Container publish", "status": "failed", "detail": "Hotfix image publish is failing on dependency cache restore."},
            {"name": "Security scan", "status": "review", "detail": "One critical and three medium alerts still open in the branch."},
            {"name": "Release build", "status": "failed", "detail": "Cross-platform artifact bundle is not being produced consistently."},
        ],
        "pullRequests": [
            {"id": 884, "title": "Retry package cache restore on Windows runner", "owner": "platform", "risk": "medium", "status": "ready"},
            {"id": 887, "title": "Upgrade runtime dependency graph", "owner": "runtime", "risk": "high", "status": "in review"},
            {"id": 889, "title": "Add fallback publish step for hotfix images", "owner": "platform", "risk": "medium", "status": "needs changes"},
            {"id": 891, "title": "Tighten secrets scanning in release workflows", "owner": "security", "risk": "low", "status": "ready"},
        ],
        "alerts": [
            {"severity": "high", "title": "Container base image CVE", "detail": "Needs to be patched before the release gate can clear."},
            {"severity": "medium", "title": "Dependency audit regression", "detail": "Introduced by the runtime upgrade branch and still unresolved."},
            {"severity": "medium", "title": "Secrets scan bypass in legacy workflow", "detail": "Coverage is incomplete for one older release workflow."},
            {"severity": "low", "title": "Pinned action version drift", "detail": "Not blocking, but should be cleaned during the next workflow pass."},
        ],
        "releaseReadiness": [
            {"label": "Critical alerts resolved", "status": "blocked"},
            {"label": "Packaging checks stable across OS targets", "status": "blocked"},
            {"label": "Hotfix release notes drafted", "status": "done"},
            {"label": "Rollback plan attached", "status": "todo"},
        ],
        "actions": [
            "Land the cache-restore retry PR and rerun the release build on all supported runners.",
            "Patch the base image CVE before approving the runtime dependency upgrade.",
            "Reduce the open PR queue by merging low-risk release work before taking on the larger runtime branch.",
        ],
    },
    "RFD-103": {
        "id": "RFD-103",
        "name": "telemetry-ingest",
        "team": "data-platform",
        "risk": "low",
        "health": 94,
        "releaseChannel": "minor",
        "lead": "Data platform",
        "summary": "Healthy repo with strong CI performance, one minor alert, and a release candidate that is effectively ready.",
        "signals": [
            {"label": "CI success rate", "value": "98%", "trend": "up"},
            {"label": "Review turnaround", "value": "9h", "trend": "down"},
            {"label": "Security alerts", "value": "1", "trend": "flat"},
        ],
        "checks": [
            {"name": "Unit tests", "status": "passed", "detail": "Stable for the last ten default-branch runs."},
            {"name": "Schema migration checks", "status": "passed", "detail": "Latest migration bundle is green in validation."},
            {"name": "Security scan", "status": "review", "detail": "One low-priority alert is still open but not release-blocking."},
            {"name": "Release build", "status": "passed", "detail": "Artifacts are cut and ready for docs sign-off."},
        ],
        "pullRequests": [
            {"id": 203, "title": "Add ingest backpressure metrics", "owner": "data-platform", "risk": "low", "status": "ready"},
            {"id": 205, "title": "Update release documentation", "owner": "docs", "risk": "low", "status": "in review"},
        ],
        "alerts": [
            {"severity": "low", "title": "Minor dependency update available", "detail": "Safe to land after the release cut if desired."},
        ],
        "releaseReadiness": [
            {"label": "CI green on release branch", "status": "done"},
            {"label": "Migration validation complete", "status": "done"},
            {"label": "Release docs reviewed", "status": "review"},
            {"label": "Final sign-off packet attached", "status": "done"},
        ],
        "actions": [
            "Finish doc review and cut the minor release.",
            "Bundle the new metrics screenshots into the release notes.",
        ],
    },
}


def list_repos() -> list[dict[str, Any]]:
    return deepcopy(REPOS)


def get_dashboard() -> dict[str, Any]:
    return {
        "overview": {
            "repos": len(REPOS),
            "avgHealth": round(mean(repo["health"] for repo in REPOS)),
            "openPrs": sum(repo["openPrs"] for repo in REPOS),
            "securityAlerts": sum(repo["securityAlerts"] for repo in REPOS),
        },
        "repos": list_repos(),
        "defaultRepoId": "RFD-102",
    }


def get_repo_detail(repo_id: str) -> dict[str, Any]:
    if repo_id not in REPO_DETAILS:
        raise KeyError(repo_id)

    return deepcopy(REPO_DETAILS[repo_id])


def get_release_packet(repo_id: str) -> dict[str, Any]:
    detail = get_repo_detail(repo_id)
    blocked = [item["label"] for item in detail["releaseReadiness"] if item["status"] == "blocked"]
    review = [item["label"] for item in detail["releaseReadiness"] if item["status"] == "review"]
    done = [item["label"] for item in detail["releaseReadiness"] if item["status"] == "done"]

    return {
        "repoId": detail["id"],
        "repoName": detail["name"],
        "risk": detail["risk"],
        "releaseChannel": detail["releaseChannel"],
        "summary": detail["summary"],
        "blockedItems": blocked,
        "reviewItems": review,
        "doneItems": done,
        "recommendedActions": detail["actions"],
        "securityAlertCount": len(detail["alerts"]),
        "pullRequestCount": len(detail["pullRequests"]),
    }


def get_risk_export(repo_id: str) -> dict[str, Any]:
    detail = get_repo_detail(repo_id)
    highest_alert = detail["alerts"][0]["title"] if detail["alerts"] else "None"

    return {
        "repoId": detail["id"],
        "repoName": detail["name"],
        "lead": detail["lead"],
        "releaseChannel": detail["releaseChannel"],
        "risk": detail["risk"],
        "executiveSummary": (
            f"{detail['name']} is currently rated {detail['risk']} with "
            f"{len(detail['pullRequests'])} open PRs and {len(detail['alerts'])} security alerts. "
            f"Highest-priority concern: {highest_alert}."
        ),
        "checks": detail["checks"],
        "actions": detail["actions"],
    }

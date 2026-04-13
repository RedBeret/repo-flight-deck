from __future__ import annotations

import sys
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.main import app


class RepoFlightDeckApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.client = TestClient(app)

    def test_healthcheck(self) -> None:
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_repo_dashboard(self) -> None:
        response = self.client.get("/api/repos")
        payload = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(payload["defaultRepoId"], "RFD-102")
        self.assertGreaterEqual(len(payload["repos"]), 3)

    def test_repo_detail(self) -> None:
        response = self.client.get("/api/repos/RFD-102")
        payload = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(payload["id"], "RFD-102")
        self.assertGreaterEqual(len(payload["pullRequests"]), 3)
        self.assertGreaterEqual(len(payload["alerts"]), 1)

    def test_release_packet(self) -> None:
        response = self.client.get("/api/repos/RFD-102/release-packet")
        payload = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(payload["repoId"], "RFD-102")
        self.assertIn("blockedItems", payload)

    def test_risk_export(self) -> None:
        response = self.client.get("/api/repos/RFD-101/risk-export")
        payload = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(payload["repoName"], "mission-console")
        self.assertIn("executiveSummary", payload)

    def test_missing_repo_returns_404(self) -> None:
        response = self.client.get("/api/repos/RFD-999")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Repository not found")


if __name__ == "__main__":
    unittest.main()

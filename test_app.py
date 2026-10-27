import unittest
from app import app


class IncidentOpsTests(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_dashboard_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Reliability Console", response.data)

    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "ok")

    def test_incident_creation(self):
        response = self.client.post(
            "/incidents",
            data={
                "service": "Test API",
                "owner": "Platform Team",
                "severity": "High",
                "status": "Investigating",
            },
        )
        self.assertEqual(response.status_code, 302)


if __name__ == "__main__":
    unittest.main()
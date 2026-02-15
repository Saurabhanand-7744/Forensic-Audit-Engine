from fastapi.testclient import TestClient
from app_api import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "Online"

def test_get_audit_results():
    # Hum limit=1 de rahe hain taaki sirf test ho sake
    response = client.get("/audit-results?limit=1")
    assert response.status_code == 200
    # Check karein ki records list hai ya nahi
    assert isinstance(response.json()["records"], list)

def test_404_error():
    response = client.get("/non-existent-path")
    assert response.status_code == 404

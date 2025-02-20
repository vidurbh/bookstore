from fastapi.testclient import TestClient
from bookstore.main import app

client = TestClient(app)

def test_get_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "up"}

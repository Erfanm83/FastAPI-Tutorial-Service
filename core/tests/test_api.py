from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_root_response_200():
    response = client.get("/")
    assert response.status_code == 200
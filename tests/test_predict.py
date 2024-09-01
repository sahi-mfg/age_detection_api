from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_predict():
    filepath = "tests/files/picture.jpeg"
    with open(filepath, "rb") as file:
        response = client.post(
            "/predict", files={"file": ("filename", file, "image/jpeg")}
        )
    assert response.status_code == 200

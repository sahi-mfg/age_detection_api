from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_predict():
    filepath = "tests/files/picture.jpeg"
    response = client.post("/predict", files={"file": ("filename", open(filepath, "rb"), "image/jpeg")})
    assert response.status_code == 200

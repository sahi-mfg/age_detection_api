import io
from fastapi.testclient import TestClient  # type: ignore
from PIL import Image  # type: ignore
from unittest.mock import patch

from app.main import app, Prediction

client = TestClient(app)


def test_greeting():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "Message": "Age detection API from images",
        "version": "0.1",
    }


def test_predict_valid_image():
    # Create a test image
    img = Image.new("RGB", (100, 100), color="red")
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format="PNG")
    img_byte_arr = img_byte_arr.getvalue()

    with patch("app.main.predict") as mock_predict:
        mock_predict.return_value = "25-35 years"
        response = client.post(
            "/predict", files={"file": ("test.png", img_byte_arr, "image/png")}
        )

    assert response.status_code == 200
    prediction = Prediction(**response.json())
    assert prediction.filename == "test.png"
    assert prediction.content_type == "image/png"
    assert prediction.predictions == "25-35 years"


def test_predict_invalid_file():
    response = client.post(
        "/predict", files={"file": ("test.txt", b"hello world", "text/plain")}
    )
    assert response.status_code == 400
    assert "File provided is not an image" in response.text

from io import BytesIO

from fastapi import FastAPI, File, HTTPException, UploadFile  # type: ignore
from PIL import Image  # type: ignore
from pydantic import BaseModel  # type: ignore

from api.model import load_feature_extractor, load_model, predict, prepare_image

api_description = """
This is an API that provides predictions of age range of a person in an image.

It uses a pre-trained model ViT (Vision Transformer) from Hugging Face to perform the predictions.

You can upload an image and get the predicted age range. Images should contain a single face for best results.

## Endpoints
- `/predict`: Upload an image and get the predicted age range.

"""
app = FastAPI(title="Age Detection", description=api_description, version="0.1")

model = load_model()
feature_extractor = load_feature_extractor()


@app.get("/", tags=["Welcome"])
def greeting():
    return {"Message": "Age detection API from images"}


# Define the response JSON
class Prediction(BaseModel):
    filename: str
    content_type: str
    predictions: str


@app.post("/predict", response_model=Prediction, tags=["Prediction"])
async def prediction(file: UploadFile = File(...)):
    # Ensure that the file is an image
    if file.content_type is None or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File provided is not an image.")

    content = await file.read()
    image = Image.open(BytesIO(content)).convert("RGB")

    # preprocessing of the image and prepare it for classification
    inputs = prepare_image(image, feature_extractor)

    response = predict(inputs, model)

    # return the response as a JSON
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "predictions": response,
    }

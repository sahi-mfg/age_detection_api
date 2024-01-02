from io import BytesIO

import uvicorn
from fastapi import FastAPI, File, HTTPException, UploadFile
from PIL import Image
from pydantic import BaseModel

from .model import load_model, predict, prepare_image

app = FastAPI(title="Age Detection", description="API to predict age from images", version="0.1")

model = load_model()


@app.get("/", tags=["Welcome"])
def greeting():
    return {"Message": "Age detection API from images", "version": "0.1"}


# Define the response JSON
class Prediction(BaseModel):
    filename: str
    content_type: str
    predictions: str


@app.post("/predict", response_model=Prediction, tags=["Prediction"])
async def prediction(file: UploadFile = File(...)):
    # Ensure that the file is an image
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File provided is not an image.")

    content = await file.read()
    image = Image.open(BytesIO(content)).convert("RGB")

    # preprocess the image and prepare it for classification
    inputs = prepare_image(image)

    response = predict(inputs)

    # return the response as a JSON
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "predictions": response,
    }


if __name__ == "__main__":
    uvicorn.run("app.main:app", port=5001)

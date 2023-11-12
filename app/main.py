from io import BytesIO

import uvicorn
from fastapi import FastAPI, File, HTTPException, UploadFile
from model import load_model, predict, prepare_image
from PIL import Image
from pydantic import BaseModel


app = FastAPI()

model = load_model()


@app.get("/")
def greeting():
    return "Welcome to the Age Classification API!"


# Define the response JSON
class Prediction(BaseModel):
    filename: str
    content_type: str
    predictions: str


@app.post("/predict", response_model=Prediction)
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
    uvicorn.run("main:app", port=5000)

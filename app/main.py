from io import BytesIO

import uvicorn  # type: ignore
from fastapi import FastAPI, File, HTTPException, UploadFile  # type: ignore
from PIL import Image  # type: ignore
from pydantic import BaseModel  # type: ignore

from app.model import load_feature_extractor, load_model, predict, prepare_image

app = FastAPI(
	title="Age Detection", description="API to predict age from images", version="0.1"
)

model = load_model()
feature_extractor = load_feature_extractor()


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


if __name__ == "__main__":
	uvicorn.run("app.main:app", port=8000)

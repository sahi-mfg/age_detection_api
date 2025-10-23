from io import BytesIO

from fastapi import FastAPI, File, HTTPException, UploadFile
from PIL import Image  # type: ignore
from pydantic import BaseModel, Field  # type: ignore

from app.model import load_feature_extractor, load_model, predict, prepare_image


# Response models
class HealthResponse(BaseModel):
    """Response model for health check"""

    Message: str = Field(
        ..., description="API status message", example="Age detection API from images"
    )


class Prediction(BaseModel):
    """Response model for age prediction"""

    filename: str = Field(
        ..., description="Name of the uploaded image file", example="portrait.jpg"
    )
    content_type: str = Field(
        ..., description="MIME type of the uploaded image", example="image/jpeg"
    )
    predictions: str = Field(..., description="Predicted age range", example="20-29")

    class Config:
        json_schema_extra = {
            "example": {
                "filename": "portrait.jpg",
                "content_type": "image/jpeg",
                "predictions": "25-35",
            }
        }


api_description = """
# Age Detection API

An REST API that allow us to predict age ranges from images using a pre-trained Vision Transformer (ViT) model from Hugging Face.

## Model Information
- **Architecture**: Vision Transformer (ViT)
- **Source**: Hugging Face (`nateraw/vit-age-classifier`)
- **Input**: RGB images (automatically resized to 224x224)
- **Output**: Age range categories

## Age Range Categories
The model classifies images into these age ranges:
- **0-2**: Infants and toddlers
- **3-9**: Children
- **10-19**: Teenagers
- **20-29**: Young adults
- **30-39**: Adults
- **40-49**: Middle-aged adults
- **50-59**: Mature adults
- **60-69**: Senior adults
- **70-79**: Elderly
- **80+**: Very elderly

## Usage Tips
- Use clear, front-facing portraits for best results
- Ensure good lighting conditions
- Single person per image recommended
- Supported formats: JPEG, PNG, GIF, BMP, TIFF

## Endpoints
- **GET /**: Health check endpoint
- **POST /predict**: Upload image and get age prediction
"""

app = FastAPI(
    title="Age Detection API",
    description=api_description,
    version="1.0.0",
    contact={
        "name": "Age Detection API",
        "url": "https://github.com/sahi-mfg/age_detection_api",
    },
)

model = load_model()
feature_extractor = load_feature_extractor()


@app.get(
    "/",
    response_model=HealthResponse,
    tags=["Health Check"],
    summary="API Health Check",
    description="Verify that the Age Detection API is running and accessible",
)
def greeting():
    """
    **Health Check Endpoint**

    Returns a simple message to confirm the API is operational.

    - **Returns**: Confirmation message that the API is running
    - **Use case**: Service monitoring and health checks
    """
    return {"Message": "Age detection API from images"}


@app.post(
    "/predict",
    response_model=Prediction,
    tags=["Age Prediction"],
    summary="Predict Age Range from Image",
    description="Upload an image to get age range prediction using Vision Transformer model",
)
async def prediction(
    file: UploadFile = File(
        ...,
        description="Image file to analyze for age prediction",
        media_type="image/*",
    ),
):
    """
    **Age Prediction from Image**

    Upload an image containing a person's face to get an age range prediction.

    **Supported formats:** JPEG, PNG, GIF, BMP, TIFF

    **Age ranges:** 0-2, 3-9, 10-19, 20-29, 30-39, 40-49, 50-59, 60-69, 70-79, 80+

    **Best results with:**
    - Clear, front-facing portraits
    - Good lighting conditions
    - Single person per image
    - High resolution images

    **Model:** Vision Transformer (ViT) from Hugging Face (`nateraw/vit-age-classifier`)

    **Processing:** Images are automatically resized to 224x224 pixels and normalized
    """
    # Ensure that the file is an image
    if file.content_type is None or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="File provided is not an image. Supported formats: JPEG, PNG, GIF, BMP, TIFF",
        )

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

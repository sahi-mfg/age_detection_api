import os
from datetime import datetime, timedelta
from io import BytesIO

import uvicorn
from doten import load_dotenv  # type: ignore
from fastapi import Depends, FastAPI, File, HTTPException, UploadFile, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt  # type: ignore
from passlib.context import CryptContext  # type: ignore
from PIL import Image
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String  # type: ignore
from sqlalchemy.ext.declarative import declarative_base  # type: ignore

from .model import load_model, predict, prepare_image

app = FastAPI(title="Age Detection", description="API to predict age from images", version="0.1")

model = load_model()

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)


class Token(BaseModel):
    access_token: str
    token_type: str


class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(users, username: str, password: str):
    user = users.get(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_acess_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@app.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(users, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_acess_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


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

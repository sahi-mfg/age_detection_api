import io

import requests  # type: ignore
import streamlit as st  # type: ignore
from PIL import Image  # type: ignore

# st.set_page_config(page_title="Age Detection App", layout="wide")


st.title("Age Detection App")
st.header("This app predicts the age range of a person from an image.")


def api_call():
    response = requests.post(
        "https://fastapi-app-ml-msze6264nq-od.a.run.app/predict",
        files={"file": ("image.png", img_bytes, "image/png")},
    )
    return response


# Upload the image
uploaded_file = st.file_uploader(
    "Please upload an image of a person to predict their age range",
    type=["jpg", "jpeg", "png"],
)
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

    # Convert the image to bytes
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format="PNG")
    img_bytes = img_byte_arr.getvalue()

    # Send a POST request to the API endpoint
    response = api_call()
    req = response.json()
    prediction = req["predictions"]

    # Display the response
    if response.status_code == 200:
        st.success(f"L'âge de cette personne est dans la tranche:  {prediction} ans.")
    else:
        st.error("Failed to get a response from the API.")

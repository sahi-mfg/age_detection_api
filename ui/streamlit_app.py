import io

import requests  # type: ignore
import streamlit as st
from PIL import Image  # type: ignore

# st.set_page_config(page_title="Age Detection App", layout="wide")


st.title("Age Detection App")
st.image(
    "https://visagetechnologies.com/app/uploads/2023/07/Age-estimation_FaceAnalysis_Visage-Technologies.webp",
    caption="Age Detection",
    use_column_width=True,
)

# Upload the image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

    # Convert the image to bytes
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format="PNG")
    img_bytes = img_byte_arr.getvalue()

    # Send a POST request to the API endpoint
    response = requests.post(
        "http://localhost:8000/predict",
        files={"file": ("image.png", img_bytes, "image/png")},
    )

    # Display the response
    if response.status_code == 200:
        st.success("Predicted Age Range:  {}".format(response.json()["predictions"]))
    else:
        st.error("Failed to get a response from the API.")

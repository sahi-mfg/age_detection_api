# Import necessary modules
import streamlit as st
import requests
import io

# Create a Streamlit app with a file uploader
st.title("Age Classification")

st.info("This app uses a deep learning model to predict the age range of a person from their picture.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

# When a file is uploaded, read the file and send it to the API
if uploaded_file is not None:
    file_bytes = io.BytesIO(uploaded_file.getvalue())
    url = "http://localhost:5000/predict"
    response = requests.post(url, files={"file": file_bytes})

    # Check if the request was successful
    if response.status_code == 200:
        # Display the prediction result
        prediction = response.json()
        st.write(f"The predicted age range is: {prediction['age_range']}")
    else:
        st.write("An error occurred while making the prediction.")

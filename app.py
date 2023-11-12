import streamlit as st

with st.sidebar:
    st.title("Age detection app")
    st.info("Upload a picture and the app will tell you the age of the person in the picture")


uploaded_file = st.file_uploader("Upload your file here...", type=["jpg", "png", "jpeg"])

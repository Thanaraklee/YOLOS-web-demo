import streamlit as st
import requests
from io import StringIO
from PIL import Image
import os
from dotenv import load_dotenv
import time

load_dotenv()
# -------------------------------- API config -------------------------------- #
API_URL = "https://api-inference.huggingface.co/models/hustvl/yolos-small"
headers = {"Authorization": f"Bearer {os.environ['API']}"}

# ------------------------------- model config ------------------------------- #

def query(uploaded_file):
    # Read the uploaded file's content as bytes
    data = uploaded_file.getvalue()
    
    # Send the data as a POST request
    response = requests.post(API_URL, headers=headers, data=data)
    
    # Check if the response is successful (status code 200)
    if response.status_code == 200:
        try:
            # Try to decode the JSON response
            return response.json()
        except ValueError:
            # If response is not valid JSON, return a message
            st.error("Failed to decode the response as JSON. Response content: " + response.text)
            return None
    elif response.status_code == 503:
        time.sleep(10)
        response = requests.post(API_URL, headers=headers, data=data)
        try:
            # Try to decode the JSON response
            return response.json()
        except ValueError:
            # If response is not valid JSON, return a message
            st.error("Failed to decode the response as JSON. Response content: " + response.text)
            return None
    else:
        # Handle unsuccessful responses (non-200 status codes)
        st.error(f"Request failed with status code {response.status_code}. Response content: {response.text}")
        return None

st.title('YOLOS - Small Demo 😊')

uploaded_file = st.file_uploader("Choose a file", type=["jpg"])

if uploaded_file is not None:
    # Display the image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)
    
    # Send the image data to the API
    output = query(uploaded_file)
    
    # If the response is not None, display the output
    if output:
        for _ in output:
            st.markdown(f"- {_['label']} | {_['score']}", unsafe_allow_html=True)
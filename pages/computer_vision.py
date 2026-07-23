import json
import streamlit as st
from google.cloud import vision

# Initialize the Google Cloud Vision client

#google key
credentials_dict = json.loads(st.secrets["google_credentials"], strict=False)
client = vision.ImageAnnotatorClient.from_service_account_info(info=credentials_dict)

#initialize the defnation of the function to detect labels in an image

#picture option and API call
@st.cache_data
def get_response(content):
    image = vision.Image(content=content)
    response = client.label_detection(image=image)
    return response

# show part of the app
st.markdown("# Intentify the picture to text")
# upload the image
file = st.file_uploader("Upload an image")

if file is not None:
    # show the uploaded image
    content = file.getvalue()
    st.image(content)
#analyze the image and get the response
if st.button("Analyze"):
    response = get_response(content)
    labels = response.label_annotations
    st.write("Labels:")
    if response.error.message:
        raise Exception(f"{response.error.message}\nFor more info on error messages, check: https://cloud.google.com/apis/design/errors")
    # indentify the text in the image and display it
    # st.write(response)
    for label in labels:
        st.write(label.description)
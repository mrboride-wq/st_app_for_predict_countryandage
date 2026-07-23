# -*- coding: utf-8 -*-
import json
import streamlit as st
from google.cloud import vision

google_credentials = st.secrets["google_credentials"]
credentials_dict = json.loads(google_credentials, strict=False)
client = vision.ImageAnnotatorClient.from_service_account_info(info=credentials_dict)

img_path = "people.png"
with open(img_path, 'rb') as f:
    img = f.read()

image = vision.Image(content=img)
response = client.label_detection(image=image)
print(response.label_annotations)
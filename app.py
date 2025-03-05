import streamlit as st
import os
# import cv2
import numpy as np
from PIL import Image
import google.generativeai as genai

# Initialize the Gemini model
genai.configure(api_key="AIzaSyCfpV-W8HOZ61pAj8shqcuYI_yQcNxphVo")
model = genai.GenerativeModel("gemini-1.5-flash")

def process_text_image(image, text_prompt="What is the name of this object? Give a short answer inside {}"):
    """ Process an image and generate a text response """
    response = model.generate_content([text_prompt, image])
    return response.text

def extract_food_name(response_text):
    """ Extract the food name from the AI-generated response """
    start, end = response_text.find("{"), response_text.find("}")
    return response_text[start+1:end].strip() if start != -1 and end != -1 else None

# Initialize session state for grocery list if not already present
if "grocery_list" not in st.session_state:
    st.session_state.grocery_list = []

st.title("Grocery Image Recognizer")

uploaded_file = st.file_uploader("Upload an image of a grocery item", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    st.write("Identifying...")
    response_text = process_text_image(image)
    food_name = extract_food_name(response_text)

    if food_name:
        # User input fields to modify name, add description, and quantity
        new_name = st.text_input("Item Name", value=food_name)
        description = st.text_area("Description (Optional)", "")
        quantity = st.number_input("Quantity", min_value=1, value=1, step=1)

        if st.button("Add to List"):
            item = {"name": new_name, "description": description, "quantity": quantity}
            st.session_state.grocery_list.append(item)
            st.success(f"Added {new_name} to the list!")
    else:
        st.error("Could not identify the grocery item. Try another image.")

# Display the updated grocery list
st.write("### Current Grocery List:")
for item in st.session_state.grocery_list:
    st.write(f"- **{item['name']}** (x{item['quantity']}) - {item['description']}")

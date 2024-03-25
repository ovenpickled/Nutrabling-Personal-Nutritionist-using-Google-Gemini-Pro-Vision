import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv

load_dotenv() ## load all the environment variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Google Gemini Pro Vision API And get response

def get_gemini_repsonse(input_prompt,image):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input_prompt,image[0]])
    return response.text

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
##initialize our streamlit app

st.set_page_config(page_title="Nutrabling")

st.title("Nutrabling 🤖")
st.header("Welcome to Nutrabling, your personal Nutritionist!")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)


submit=st.button("Tell me the total calories")

input_prompt="""
I want you to act like a professional personal Nutritionist who has a vast knowledge of food and nutrition. You will be provided input in the form of
image, you will display the calories of the food item in the following format

               1. Item 1 - no of calories
               2. Item 2 - no of calories
               ----
               ----

additionally, i want you to display the nutritional profile of the food item as well. Make sure to include the amount of protein, carbohydrates,
fats, fibre etc. present in the food. Give the percentages of micronutrients as well. Finally, state whether the food item is healthy or not. Additonally,
state how the given food item can be made healthy if the food item is unhealthy, and how it can be made more healthy if it is already healthy.

"""

# If submit button is clicked

if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_repsonse(input_prompt,image_data)
    st.subheader("The Response is")
    st.write(response)


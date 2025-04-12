import streamlit as st
from PIL import Image
import google.generativeai as genai # type: ignore
import os
from dotenv import load_dotenv # type: ignore

# Load API key from .env file if available
load_dotenv()

# App title and instructions
st.title("Poem Generator from Photos")
st.write("This app uses the Google Gemini API to generate poems from images. An API key is required to access this service.")
st.write("If you don't have an API key, you can sign up for one at [Google AI Studio](https://makersuite.google.com/).")

# API key input field (masked for security)
api_key_input = st.text_input("Google API Key", type="password").strip()

# Determine which API key to use
if api_key_input:
    API_KEY = api_key_input
else:
    API_KEY = os.getenv('GOOGLE_API_KEY')

# Check if an API key is provided
if not API_KEY:
    st.error("API key is required. Please enter your API key or set it in the .env file.")
else:
    # Configure the Gemini API with the provided key
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # App description
    st.write("Upload an image and generate a poem inspired by it.")

    # File uploader for image
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png", "webp"])

    # Prompt input with default value
    prompt = st.text_input("Prompt", value="Write a short poem inspired by this image")

    # Creativity slider (temperature)
    temperature = st.slider("Creativity Level", min_value=0.0, max_value=1.0, value=0.7, step=0.1)

    # Generate button
    if st.button("Generate Poem"):
        if uploaded_image is None:
            st.warning("Please upload an image first.")
        else:
            with st.spinner("Generating poem..."):
                try:
                    # Read the image
                    image = Image.open(uploaded_image)

                    # Prepare content for the API
                    content = [prompt, image]

                    # Configure generation settings
                    config = {
                        "temperature": temperature,
                        "max_output_tokens": 150  # Limits poem length
                    }

                    # Generate the poem
                    response = model.generate_content(content, generation_config=config)
                    poem = response.text

                    # Create two columns for side-by-side display
                    col1, col2 = st.columns(2)

                    # Display the image in the first column
                    with col1:
                        st.image(image, caption="Uploaded Image", use_column_width=True)

                    # Display the poem in the second column with serif font
                    with col2:
                        st.subheader("Generated Poem")
                        st.markdown(
                            f'<div style="font-family: serif; font-size: 16px; line-height: 1.5;">{poem}</div>',
                            unsafe_allow_html=True
                        )
                except Exception as e:
                    st.error(f"An error occurred: {e}")
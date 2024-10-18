from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai

# Configure the API key for Google Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load the Gemini Pro model and start chat session
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

# Function to get response from Gemini model
def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

# Set up Streamlit app configuration
st.set_page_config(page_title="ECO GROW")

# Page header
st.header("ECO GROW: AI-Driven Q&A")

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Create form using Streamlit for input and file upload
with st.form(key='input_form'):
    input_text = st.text_input("Input your question here:", key="input")
    uploaded_file = st.file_uploader("Upload an image (optional)", type=["jpg", "jpeg", "png"])
    submit = st.form_submit_button("Ask the question")

# Process input and uploaded file when the form is submitted
if submit:
    if uploaded_file is not None:
        # Handle image upload (here you can process the image)
        image_data = uploaded_file.read()  # Read the file content
        
        # You can add code here to process the image with your model
        question = "Can you analyze this image?"
        response = get_gemini_response(question)
        
        # Update chat history with image upload info
        st.session_state['chat_history'].append(("You", "Image uploaded"))

    elif input_text:
        # Get the Gemini response for text input
        response = get_gemini_response(input_text)
        st.session_state['chat_history'].append(("You", input_text))

        try:
            full_response = []
            for chunk in response:
                if hasattr(chunk, 'text'):
                    full_response.append(chunk.text)
            
            response.resolve()
            
            if full_response:
                for text in full_response:
                    st.write(text)
                    st.session_state['chat_history'].append(("Bot", text))
            else:
                st.write("No content found in response.")
                st.session_state['chat_history'].append(("Bot", "No content found in response."))
        except Exception as e:
            st.write(f"An error occurred: {e}")
            st.session_state['chat_history'].append(("Bot", f"An error occurred: {e}"))

# Display the chat history
st.subheader("Chat History:")
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")


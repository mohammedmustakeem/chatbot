from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load the Gemini Pro model and get a response
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

st.set_page_config(page_title="Q&A Demo")

st.header("ECO GROW")

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Create a form for input and file upload
with st.form(key='input_form'):
    input_text = st.text_input("Input:", key="input")
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    submit = st.form_submit_button("Ask the question")

# Process the input and uploaded file
if submit:
    if uploaded_file is not None:
        # Read the image data
        image_data = uploaded_file.read()  # You can process this as needed

        # Ask a question related to the image
        question = "Can you analyze this image?"  # Customize this based on your needs
        response = get_gemini_response(question)
        
        st.session_state['chat_history'].append(("You", "Image uploaded"))
        
        # Extracting text from the response
        try:
            # Collect all chunks until completion
            full_response = []
            for chunk in response:
                if hasattr(chunk, 'text'):
                    full_response.append(chunk.text)

            # Resolve the response to ensure all data is accumulated
            response.resolve()

            # Display the accumulated content
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
    
    elif input_text:
        response = get_gemini_response(input_text)
        st.session_state['chat_history'].append(("You", input_text))
        
        # Extracting text from the response
        try:
            full_response = []
            for chunk in response:
                if hasattr(chunk, 'text'):
                    full_response.append(chunk.text)

            # Resolve the response to ensure all data is accumulated
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

st.subheader("The Chat History is")
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")

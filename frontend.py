import streamlit as st
import requests

st.title("Mental Health Support Chatbot")

user_message = st.text_input("You:", "")

if st.button("Send"):
    if user_message:
        try:
            url = "http://127.0.0.1:8000/chat"  # Make sure this matches your backend
            data = {"message": user_message}
            response = requests.post(url, json=data)

            if response.status_code == 200:
                bot_response = response.json().get("response")
                st.text_area("Bot:", value=bot_response, height=150)
            else:
                st.error("Bot responded with error code: " + str(response.status_code))
        except requests.exceptions.ConnectionError:
            st.error("❌ Could not connect to the chatbot API. Please make sure the backend (Flask) is running.")
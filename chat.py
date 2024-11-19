import streamlit as st
import requests
import json

st.title("Payment Collection Bot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # static testing url for now
        url = 'https://ae6d-182-0-144-8.ngrok-free.app/prompt'
        myobj = {'prompt': dict(st.session_state.messages[-1])['content']}
        response = requests.post(url, json=myobj)  # Store the response object
        if response.status_code == 200:  # Check if the request was successful
            response_dict = response.json()  # Parse the JSON response
        else:
            response_dict = {"response": "Error: Unable to get a valid response."}  # Handle error case
        st.write(response_dict['response'])
    
    st.session_state.messages.append({"role": "assistant", "content": response_dict['response']})
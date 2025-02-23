import streamlit as st
import requests
import json
import uuid  # Import the uuid module
import logging  # Import the logging module

# static testing url for now
# url = 'https://a66e-111-108-27-62.ngrok-free.app'
url = 'https://f2ed-111-108-27-62.ngrok-free.app'
url = f'{url}/prompt'

# for debugging, uncomment line below
# logging.basicConfig(level=logging.DEBUG)

def callLLM(prompt):
    requestPayload = {'prompt': prompt}
    headers = {'Session-Id': st.session_state.uuid}
    response = requests.post(url, headers=headers, json=requestPayload)  # Send request and store the response object
    if response.status_code == 200:  # Check if the request was successful
        response_dict = response.json()  # Parse the JSON response
        return response_dict['response']
    else:
        response_dict = {"response": "Error: Unable to get a valid response."}  # Handle error case
        return response_dict['response']
    
def initialize():
    # Your one-time initialization code here
    st.session_state.initialized = True

    # TODO: change this to user based id in the future
    st.session_state.uuid = str(uuid.uuid4())  # Generate and store UUID as a string
    
    # Initial call to callLLM
    response = callLLM("Please initiate the conversation.")
    st.session_state.messages.append({"role": "assistant", "content": response})  # Store the response

# Check if the initialization has already been done
if "initialized" not in st.session_state:
    st.session_state.messages = []  # Initialize messages if not already done
    initialize()

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

    response = callLLM(dict(st.session_state.messages[-1])['content'])

    with st.chat_message("assistant"):
        st.write(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
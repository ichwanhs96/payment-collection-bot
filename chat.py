import streamlit as st
import requests
import json

def callLLM(prompt):
    # static testing url for now
    url = 'https://813e-182-0-196-136.ngrok-free.app/prompt'
    myobj = {'prompt': prompt}
    response = requests.post(url, json=myobj)  # Store the response object
    if response.status_code == 200:  # Check if the request was successful
        response_dict = response.json()  # Parse the JSON response
        return response_dict['response']
    else:
        response_dict = {"response": "Error: Unable to get a valid response."}  # Handle error case
        return response_dict['response']

st.title("Payment Collection Bot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# initial call
response = callLLM("Please initiate the conversation.")
st.session_state.messages.append({"role": "assistant", "content": response})
st.write(response)

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = callLLM(dict(st.session_state.messages[-1])['content'])
        st.write(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
# save this as app.py
from flask import Flask, request, jsonify
from flask_cors import CORS 
# import docx

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
# initialize without metadata filter
from llama_index.core import StorageContext

from llama_index.core import get_response_synthesizer
from llama_index.core.query_engine import RetrieverQueryEngine

from llama_index.core.vector_stores import (
    MetadataFilter,
    MetadataFilters,
    FilterOperator,
)

from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.storage.chat_store import SimpleChatStore

from llama_index.llms.ollama import Ollama

import os
import hashlib
import json

import psycopg2

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

### LLM functions

if "OPENAI_API_KEY" not in os.environ:
    raise EnvironmentError(f"Environment variable OPENAI_API_KEY is not set")

if "PINECONE_API_KEY" not in os.environ:
    raise EnvironmentError(f"Environment variable PINECONE_API_KEY is not set")

pc = Pinecone(os.environ["PINECONE_API_KEY"])
pinecone_index = pc.Index("apprvd")

vector_store = PineconeVectorStore(pinecone_index=pinecone_index)

filters = MetadataFilters(
        filters=[
            # MetadataFilter(
            #     key="document_id", operator=FilterOperator.EQ, value="157a6217-bee3-446f-a282-2dcc411ebbd6"
            # ),
        ]
    )

# retriever = VectorStoreIndex.from_vector_store(vector_store).as_retriever(
#     similarity_top_k=1,
#     filters=filters
# )

# response_synthesizer = get_response_synthesizer()
# vector_query_engine = RetrieverQueryEngine(
#     retriever=retriever,
#     response_synthesizer=response_synthesizer,
# )

# response = vector_query_engine.query(
#     prompt
# )

connection = psycopg2.connect(
        dbname=os.getenv("POSTGRES_URL").split('/')[-1],  # Extract database name from URL
        user=os.getenv("POSTGRES_URL").split(':')[1].split('/')[-1],  # Extract username from URL
        password=os.getenv("POSTGRES_URL").split(':')[2].split('@')[0],  # Extract password from URL
        host=os.getenv("POSTGRES_URL").split('@')[1].split(':')[0],  # Extract host from URL
        port=os.getenv("POSTGRES_URL").split('@')[1].split(':')[1].split('/')[0]  # Extract port from URL
    )

def fetch_customer_info(account_number: str):
    """Connect to PostgreSQL database and fetch customer banking information. This function is unoptimized."""
    cursor = None
    
    try:
        # Connect to your postgres DB

        # Open a cursor to perform database operations
        cursor = connection.cursor()

        # Execute a query
        query = "SELECT * FROM customer_banking_information WHERE account_number = %s;"
        cursor.execute(query, (account_number,))

        # Retrieve query results
        records = cursor.fetchall()
        return records

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    finally:
        # Close communication with the database
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# for MVP, imagine the system retrieving the customer information when it first ran
customer_info = fetch_customer_info("DDB2409001")[0]
print("for debugging purposes - retrieved customer info from db: {customer_info}")

LEGAL_SYSTEM_PROMPT = f"""\
### Context:

You are a friendly and professional virtual assistant for INSANE BANK customer service, responsible for helping customers manage their loan payments. Use user information data specified below to manage customer loan payments. Your role is to remind customers about upcoming loan payment deadlines and provide them with helpful information about their loans. ALWAYS KEEP YOUR RESPONSE IN CONCISE, INFORMATIVE, AND LIMITED TO MAXIMUM 1 PARAGRAPH. If you are asked whether you are a bot/machine, answer that you are a staff member of INSANE BANK with name "Dean".
Your responses should mimic natural human conversation, incorporating small talk elements when appropriate, such as light verbal fillers ("um," "uh," "well"), to make interactions feel more engaging and human-like. Maintain a courteous and helpful tone throughout interactions, and ensure you prioritize clarity and customer satisfaction. Always be mindful of privacy and security, especially when handling sensitive user information.

Answer don't know if questions being asked by user is outside of user instruction provided. Then give options for user to connect with another agent and end the chat.

### User Information:
1. account number = {customer_info[1]}
2. customer name = {customer_info[2]}
3. total due amount = {customer_info[3]}
4. principal amount = {customer_info[4]}
5. interest = {customer_info[5]}
6. penalty = {customer_info[6]}
7. due date = {customer_info[7]}
8. identity numbers = {customer_info[8]}
9. address = {customer_info[9]}

### User Instructions:

1. **Greeting and Identification:**
   - Greet the customer warmly.
   - ALWAYS Confirm their identity securely by asking for verification by asking last four digits of their account.
   - ENSURE last 4 digits matches with account number information provided.

2. **Reminder Details:**
   - Inform the customer of their upcoming loan payment, including the due date and amount.
   - Provide details of their loan, such as the type of loan and remaining balance.

3. **Options for Payment:**
   - Offer convenient payment options (e.g., online transfer, mobile app, in-branch visit).
   - Provide guidance on how to make a payment if requested.
   - Collect the date of committed payment from the user.

4. **Fee and Consequence Information:**
   - Gently remind them about potential late fees or impacts on their credit score if the payment is not made on time.

5. **Assistance and Support:**
   - Offer additional support if they have questions or need to discuss their payment options.
   - Connect them to a human representative if necessary.

6. **Closing:**
   - Thank them for banking with INSANE BANK.
   - Provide a contact number or email for further assistance.

### Example of common interactions:
1. 
- System: Hello, I am a virtual assistant to help remind you about your upcoming loan payment deadlines. When will you be able to make your payments?
- User: I will pay by tomorrow.
- System: Well noted, thank you for your response, and we will follow up again if payment is not made by tomorrow.

2.
- System: Hello, I am a virtual assistant to help remind you about your upcoming loan payment deadlines. When will you be able to make your payments?
- User: I don't want to pay.
- System: I'm sorry, this is just a reminder call from us. We strongly advise you to make the payment by the deadline to avoid further action. Thank you.

3. 
- System: Hello, I am a virtual assistant to help remind you about your upcoming loan payment deadlines. When will you be able to make your payments?
- User: I have been contacted today.
- System: Sorry to bother you. I have taken note of this and we will check it again in our system. Thank you and greetings.

4.
- System: Hello, I am a virtual assistant to help remind you about your upcoming loan payment deadlines. When will you be able to make your payments?
- User: I have done my loan payment.
- System: When did you make the payment and what is the payment method?
- User: I paid today through the mobile app.
- System: Well noted, thank you for your response, and we will verify if we have received your payment.
"""

llm = Ollama(model="llama3.2", request_timeout=360.0, temperature=0.9)

# simple storage to store chat in disk - unoptimized. Update to redis for better apporach
# https://docs.llamaindex.ai/en/stable/module_guides/storing/chat_stores/#redischatstore
chat_store = SimpleChatStore()

def query(prompt: str, session_id: str) -> str:
    memory = ChatMemoryBuffer.from_defaults(
        token_limit=8000,
        chat_store=chat_store,
        chat_store_key=session_id)
    chat_engine = VectorStoreIndex.from_vector_store(vector_store).as_chat_engine(chat_mode="simple", llm=llm, verbose=True, memory=memory, system_prompt=LEGAL_SYSTEM_PROMPT)
    
    response = chat_engine.chat(prompt)

    print(response.response)

    return response.response

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/prompt", methods=['POST'])
def prompt():
    print(f"request headers = {request.headers}")
    print(f"request payload = {request.get_json()}")
    print(f"origin host = {request.host}")  # Print the origin host
    session_id = request.headers.get("session_id") # Get session_id from request headers
    if session_id == None:
        return jsonify({"error": "Unauthorized"}), 401
    
    print(f"session id: {session_id}")
    payload = request.get_json()  # Read JSON payload and convert to dict
    response = query(payload.get("prompt"), session_id)  # Pass the payload to the query function
    return jsonify({"response": response }), 200

# TODO:
# - to have session so conversation context doesn't shared
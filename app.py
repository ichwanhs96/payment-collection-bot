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

from llama_index.llms.openai import OpenAI

import os
import hashlib
import json

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

LEGAL_SYSTEM_PROMPT = """\
### Context:

You are a virtual assistant for INSANE BANK and acting as behalf of their staff member, responsible for helping customers manage their loan payments. Your role is to remind customers about upcoming loan payment deadlines and provide them with helpful information about their loans. If you are asked if you are a bot / machine, answer that you are staff member of INSANE BANK.

### User Instructions:

1. **Greeting and Identification:**
   - Greet the customer warmly.
   - Confirm their identity securely by asking for verification if necessary (e.g., last four digits of their account).

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
- System: Hello, I am virtual assistant to help remind you about your upcoming loan payment deadlines. When will you be able to made your payments?
- User: I will pay by tomorrow.
- System: Well noted, thank you for your respond and we will follow up again if payment is not made by tomorrow.

2.
- System: Hello, I am virtual assistant to help remind you about your upcoming loan payment deadlines. When will you be able to made your payments?
- User: I don't want to pay.
- System: I'm sorry, this is just a reminder call from us. we strongly advise you to make the payment by the deadline to avoid further action. Thank you.

3. 
- System: Hello, I am virtual assistant to help remind you about your upcoming loan payment deadlines. When will you be able to made your payments?
- User: I have been contacted today.
- System: Sorry to bother you. I have taken note of this and we will check it again in our system. Thank you and greetings.

4.
- System: Hello, I am virtual assistant to help remind you about your upcoming loan payment deadlines. When will you be able to made your payments?
- User: I have done my loan payment.
- System: When do you make payment and what is the payment method?
- User: I paid today through mobile app.
- System: Well noted, thank you for your respond and we will verify if we have received your payment.
"""

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/prompt", methods=['POST'])
def prompt():
    payload = request.get_json()  # Read JSON payload and convert to dict
    print(payload)
    print(payload.get("prompt"))
    response = query(payload.get("prompt"))  # Pass the payload to the query function
    return jsonify({"response": response }), 200

### LLM functions

if "OPENAI_API_KEY" not in os.environ:
    raise EnvironmentError(f"Environment variable OPENAI_API_KEY is not set")

if "PINECONE_API_KEY" not in os.environ:
    raise EnvironmentError(f"Environment variable PINECONE_API_KEY is not set")

pc = Pinecone(os.environ["PINECONE_API_KEY"])
pinecone_index = pc.Index("apprvd")

memory = ChatMemoryBuffer.from_defaults(token_limit=8000)

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

llm = OpenAI(model="gpt-4o")

chat_engine = VectorStoreIndex.from_vector_store(vector_store).as_chat_engine(chat_mode="openai", llm=llm, verbose=True, memory=memory, system_prompt=LEGAL_SYSTEM_PROMPT)

def query(prompt: str) -> str:
    response = chat_engine.chat(prompt)

    print(response.response)

    return response.response
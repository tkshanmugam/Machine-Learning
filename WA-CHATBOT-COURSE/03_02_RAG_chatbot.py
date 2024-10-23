import warnings
warnings.filterwarnings("ignore")

from langchain_together import ChatTogether
import api_key

from flask import Flask, request
from langchain_community.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA

from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

llm = ChatTogether(api_key=api_key.api,temperature=0.0, model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo")

embedding = HuggingFaceEmbeddings()

db = FAISS.load_local("airline_db", embedding, allow_dangerous_deserialization=True)
qa_chain = RetrievalQA.from_chain_type(
    llm,
    retriever=db.as_retriever()
)

# Route to test if server is running
@app.route("/ping", methods=['GET'])
def pinger():
    return "<p>Hello world!</p>"

# Route to answer queries based on the document embeddings
@app.route('/answer', methods=['POST'])
def answer():
    query = request.form.get('Body')  # Get the JSON data from the request body
    result = qa_chain({"query": query})
    resp = MessagingResponse()
    msg = resp.message()
    msg.body(result["result"])
    return str(resp)

if __name__ == '__main__':
    app.run(port=4040)




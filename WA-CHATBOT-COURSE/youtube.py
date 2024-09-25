import warnings
warnings.filterwarnings("ignore")

# Import necessary libraries
import re
from langchain_together import ChatTogether
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain_community.document_loaders import YoutubeLoader
from langchain import LLMChain
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Initialize the language model
llm = ChatTogether(api_key='34bbeca4f0724f9e5203a3753eb2dae899919d4da90b7350af5d2f6dba12cae7',temperature=0.0, model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo")

def is_youtube_url(url):
    # Regular expression pattern to match YouTube URLs
    youtube_regex = re.compile(
        r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/'
        r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

    # Match the URL against the regex pattern
    match = youtube_regex.match(url)

    # Return True if it's a valid YouTube URL, else False
    return bool(match)

def summarise(video_url):
    # Get youtube video transcript
    loader = YoutubeLoader.from_youtube_url(video_url, add_video_info=False)
    data = loader.load()

    # Define the prompt template for summarization
    product_description_template = PromptTemplate(
        input_variables=["video_transcript"],
        template="""
        Read through the entire transcript carefully.
    Provide a concise summary of the video's main topic and purpose.
    Extract and list the five most interesting or important points from the transcript. For each point: State the key idea clearly and concisely

    Ensure your summary and key points capture the essence of the video without including unnecessary details.
    Use clear, engaging language that is accessible to a general audience.
    If the transcript includes any statistical data, expert opinions, or unique insights, prioritize including these in your summary or key points.

        video transcript: {video_transcript}    """
    )

    # Create a chain using the language model and prompt template
    chain = LLMChain(llm=llm, prompt=product_description_template)

    # Generate summary using the chain
    summary = chain.invoke({
        "video_transcript": data[0].page_content
    })

    return (summary['text'])

# Route to test if server is running
@app.route("/ping", methods=['GET'])
def pinger():
    return "<p>Hello world!</p>"

# Route to summarize YouTube video from a given URL
@app.route('/summary', methods=['POST'])
def summary():
    url = request.form.get('Body')  # Get the JSON data from the request body
    print(url)
    if is_youtube_url(url):
        response = summarise(url)
    else:
        response = "please check if this is a correct youtube video url"
    print(response)
    resp = MessagingResponse()
    msg = resp.message()
    msg.body(response)
    return str(resp)

# Run the Flask app
if __name__ == '__main__':
    app.run(port=4040)
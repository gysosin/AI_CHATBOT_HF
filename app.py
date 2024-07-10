import os
import requests
from flask import Flask, session, redirect
from flask_session import Session
from flask_restx import Api, Resource, fields
from dotenv import load_dotenv
import gradio as gr

# Load environment variables from .env file
load_dotenv()

# Retrieve the Hugging Face token from environment variable
hf_token = os.getenv('HUGGINGFACE_TOKEN')

if not hf_token:
    raise ValueError("Hugging Face token not found. Please set the HUGGINGFACE_TOKEN environment variable in the .env file.")

# Define the API URL for the Mistral model
MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.2"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_NAME}"

# Define headers for the API request
headers = {"Authorization": f"Bearer {hf_token}", "Content-Type": "application/json"}

def query(payload):
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as err:
        print(f"Other error occurred: {err}")
    except ValueError as json_err:
        print(f"JSON decode error occurred: {json_err}")
    return None

# Initialize Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a secure secret key
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Define the Gradio chat interface
system_prompt = {
    "role": "system",
    "content": "You are a useful assistant. You reply with efficient answers."
}

def chat_mistral(message, history):
    if history is None:
        history = []

    messages = [system_prompt]
    for msg in history:
        messages.append({"role": "user", "content": str(msg[0])})
        messages.append({"role": "assistant", "content": str(msg[1])})
    messages.append({"role": "user", "content": str(message)})

    response_content = ''
    payload = {
        "inputs": messages,
        "parameters": {
            "max_tokens": 1024,
            "temperature": 1.3,
            "stream": False
        }
    }

    response = query(payload)
    if response is None:
        response_content = "I'm sorry, I couldn't generate a response."
    elif 'error' in response:
        response_content = f"Error: {response['error']}"
    elif response and isinstance(response, list) and 'generated_text' in response[0]:
        response_content = response[0]['generated_text'].split("Assistant:")[-1].strip()
    
    return response_content

# Initialize Gradio interface within Flask
def create_demo():
    demo = gr.Interface(
        fn=chat_mistral,
        inputs=[gr.Textbox(label="Message"), gr.State()],
        outputs=[gr.Textbox(label="Response"), gr.State()],
        live=True
    )
    return demo

demo = create_demo()

@app.route("/")
def home():
    return redirect("/gradio")

@app.route("/gradio")
def gradio_interface():
    return demo.launch(share=True, inline=False)

if __name__ == '__main__':
    app.run(debug=True)

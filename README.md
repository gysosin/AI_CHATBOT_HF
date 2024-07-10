### README.md

# Chatbot API with Swagger and Docker

This project is a Python-based chatbot API using Hugging Face's Inference API for text generation. Built with Flask and Flask-RESTX, it includes Swagger documentation for easy API testing. The application is containerized using Docker for consistent deployment.

## Key Features
- **Chatbot API**: Processes user inputs and conversation history to generate responses using Hugging Face's language models.
- **Swagger UI**: Provides interactive documentation for testing API endpoints.
- **Dockerized**: Ensures consistent deployment across environments.

## Setup Instructions

### 1. Clone the Repository
```sh
git clone https://github.com/gysosin/aichatbot_API_HF.git
cd aichatbot_API_HF
```

### 2. Create and Configure `.env` File
Create a `.env` file in the root directory of the project and add your Hugging Face token:
```
HUGGINGFACE_TOKEN=your_hugging_face_token
```

### 3. Build and Run the Docker Container
```sh
docker build -t chatbot-api .
docker run -d -p 5000:5000 --name chatbot-api-container --env-file .env chatbot-api
```

### 4. Access the Swagger UI
Open your web browser and navigate to `http://127.0.0.1:5000` to access the Swagger UI for testing the API.

## Project Structure
- **Dockerfile**: Contains the instructions to build the Docker image.
- **.dockerignore**: Specifies which files and directories to ignore during the Docker build process.
- **requirements.txt**: Lists the dependencies required by the project.
- **app.py**: The main application file containing the Flask setup, API endpoints, and business logic.
- **.env**: (Not included in the repository) A file to store environment variables securely.

## API Endpoints

### POST /chatbot/
- **Description**: Generate a response from the chatbot.
- **Request Body**:
  ```json
  {
    "input_text": "Can you please let us know more details about your services?",
    "history": []
  }
  ```
- **Response Body**:
  ```json
  {
    "response_text": "Sure! Our services include ...",
    "history": [
      "User: Can you please let us know more details about your services?",
      "Chatbot: Sure! Our services include ..."
    ]
  }
  ```

## Dependencies
- **Python 3.10**
- **Flask**
- **Flask-RESTX**
- **Requests**
- **Hugging Face Hub**
- **python-dotenv**

This project provides a scalable and easy-to-use interface for interacting with Hugging Face's powerful language models, making it suitable for various chatbot applications. The integration with Swagger UI and Docker ensures it is developer-friendly and ready for deployment.
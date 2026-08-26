# Voice Agent Management API

A FastAPI-based backend that provides a unified API for creating AI voice agents through Vapi and Retell AI.

Instead of building separate backend endpoints for each voice AI provider, this project exposes a single `/create-agent` endpoint and routes the request to the selected provider.

## Features

- FastAPI backend
- REST API for voice-agent creation
- Support for Vapi and Retell AI
- Unified agent creation endpoint
- Pydantic request validation
- Environment-based API key management
- Async HTTP requests using HTTPX
- Automatic Swagger API documentation
- Health-check endpoint
- Structured error handling

## Tech Stack

- Python
- FastAPI
- Pydantic
- HTTPX
- python-dotenv
- Vapi AI
- Retell AI
- REST APIs

## Project Structure

```text
voice-agent-api/
├── main.py
├── requirements.txt
├── README.md
└── .gitignore

Installation
1. Clone the repository
git clone <your-github-repository-url>
cd voice-agent-api
2. Create a virtual environment

For Windows:

python -m venv venv
venv\Scripts\activate

For macOS/Linux:

python3 -m venv venv
source venv/bin/activate
3. Install dependencies
pip install -r requirements.txt

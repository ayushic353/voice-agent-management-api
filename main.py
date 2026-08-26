import os
from typing import Literal

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()

# Initialize FastAPI
app = FastAPI(
    title="Voice Agent Management API",
    description="Unified API for creating voice agents using Vapi and Retell AI.",
    version="1.0.0",
)

# API keys from environment variables
VAPI_API_KEY = os.getenv("VAPI_API_KEY")
RETELL_API_KEY = os.getenv("RETELL_API_KEY")


# -----------------------------
# Request Models
# -----------------------------

class AgentCreateRequest(BaseModel):
    provider: Literal["vapi", "retell"]
    agent_name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=500)
    voice: str = Field(..., min_length=1)


# -----------------------------
# Health Check
# -----------------------------

@app.get("/")
def health_check():
    return {
        "status": "running",
        "service": "Voice Agent Management API",
        "version": "1.0.0"
    }


# -----------------------------
# Create Agent
# -----------------------------

@app.post("/create-agent")
async def create_agent(request: AgentCreateRequest):

    if request.provider == "vapi":
        return await create_vapi_agent(request)

    if request.provider == "retell":
        return await create_retell_agent(request)

    raise HTTPException(
        status_code=400,
        detail="Unsupported provider"
    )


# -----------------------------
# Vapi Agent
# -----------------------------

async def create_vapi_agent(request: AgentCreateRequest):

    if not VAPI_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="VAPI_API_KEY is not configured"
        )

    url = "https://api.vapi.ai/assistants"

    headers = {
        "Authorization": f"Bearer {VAPI_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "name": request.agent_name,
        "description": request.description,
        "voice": {
            "provider": "11labs",
            "voiceId": request.voice
        },
        "transcriber": {
            "provider": "deepgram"
        }
    }

    async with httpx.AsyncClient(timeout=30) as client:

        response = await client.post(
            url,
            headers=headers,
            json=payload
        )

    if response.is_error:
        raise HTTPException(
            status_code=response.status_code,
            detail={
                "provider": "vapi",
                "error": response.text
            }
        )

    return {
        "success": True,
        "provider": "vapi",
        "agent": response.json()
    }


# -----------------------------
# Retell Agent
# -----------------------------

async def create_retell_agent(request: AgentCreateRequest):

    if not RETELL_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="RETELL_API_KEY is not configured"
        )

    url = "https://api.retellai.com/create-agent"

    headers = {
        "Authorization": f"Bearer {RETELL_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "agent_name": request.agent_name,
        "voice_id": request.voice,
        "response_engine": {
            "type": "retell-llm"
        }
    }

    async with httpx.AsyncClient(timeout=30) as client:

        response = await client.post(
            url,
            headers=headers,
            json=payload
        )

    if response.is_error:
        raise HTTPException(
            status_code=response.status_code,
            detail={
                "provider": "retell",
                "error": response.text
            }
        )

    return {
        "success": True,
        "provider": "retell",
        "agent": response.json()
    }

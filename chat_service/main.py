from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import requests
import httpx
import json

app = FastAPI()

# Allow frontend (React, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MessageRequest(BaseModel):
    session_id: str
    message: str

@app.post("/chat/")
async def chat(request: MessageRequest):
    user_message = request.message
    session_id = request.session_id
    assistant_reply = ""

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            ollama_response = await client.post(
                "http://localhost:11434/api/chat",
                json={
                    "model": "mistral",
                    "stream": True,
                    "messages": [
                        {"role": "user", "content": user_message}
                    ]
                },
                timeout=60.0
            )

            # Stream and collect response chunks
            async for line in ollama_response.aiter_lines():
                if line.strip():
                    try:
                        data = json.loads(line)
                        assistant_reply += data.get("message", {}).get("content", "")
                    except Exception as e:
                        print("Chunk parse error:", e)

    except Exception as e:
        print("Ollama error:", e)
        assistant_reply = "Sorry, I couldn't respond right now."

    # Save to history
    for payload in [
        {
            "session_id": session_id,
            "role": "user",
            "message": user_message,
            "timestamp": datetime.utcnow().isoformat(),
        },
        {
            "session_id": session_id,
            "role": "assistant",
            "message": assistant_reply,
            "timestamp": datetime.utcnow().isoformat(),
        },
    ]:
        try:
            requests.post("http://localhost:8003/history/", json=payload)
        except:
            pass

    return {"reply": assistant_reply}

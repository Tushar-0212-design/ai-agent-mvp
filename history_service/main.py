from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from pymongo import MongoClient
from datetime import datetime
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MONGODB_URI = os.getenv("MONGODB_URI", "your_mongo_uri_here")
client = MongoClient(MONGODB_URI)
db = client["ai_agent"]
history_collection = db["chat_history"]

class HistoryEntry(BaseModel):
    session_id: str
    role: str  # "user" or "assistant"
    message: str
    timestamp: datetime = datetime.utcnow()

@app.post("/history/")
def save_message(entry: HistoryEntry):
    data = entry.dict()
    history_collection.insert_one(data)
    return {"inserted_id": str(data)}

@app.get("/history/{session_id}", response_model=List[HistoryEntry])
def get_history(session_id: str):
    results = history_collection.find({"session_id": session_id}).sort("timestamp")
    return [HistoryEntry(**{**doc, "timestamp": doc["timestamp"]}) for doc in results]

@app.delete("/history/{session_id}")
def delete_history(session_id: str):
    result = history_collection.delete_many({"session_id": session_id})
    return {"deleted_count": result.deleted_count}

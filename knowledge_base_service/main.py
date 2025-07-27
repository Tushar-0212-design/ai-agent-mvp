from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Query(BaseModel):
    query: str

@app.post("/retrieve_context")
async def retrieve_context(query: Query):
    user_message = query.query.lower()

    if "ai" in user_message:
        answer = "AI stands for Artificial Intelligence. It's used in various industries."
    elif "weather" in user_message:
        answer = "Weather today is mostly sunny with a chance of rain."
    else:
        answer = ""

    return {"answer": answer}

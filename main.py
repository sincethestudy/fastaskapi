from typing import Union, List
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv(override=True)

app = FastAPI()

client = OpenAI(
    api_key=os.getenv("CEREBRAS_API_KEY"),
    base_url="https://api.cerebras.ai/v1"
)

# Lazy Supabase init — only connect when leaderboard logging is needed
_supabase = None

def get_supabase():
    global _supabase
    if _supabase is None:
        from supabase import create_client
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_KEY")
        if url and key:
            _supabase = create_client(url, key)
    return _supabase

class Message(BaseModel):
    role: str
    content: str

class Query(BaseModel):
    messages: List[Message]
    log: bool = False
    user: str = ""


@app.post("/itsfast")
async def answer_question(query: Query):

    completion = client.chat.completions.create(
        messages=[message.model_dump() for message in query.messages],
        model="llama-3.3-70b",
        stream=False,
    )

    resp = completion.choices[0].message.content

    if query.log:
        sb = get_supabase()
        if sb:
            sb.table("leaderboard").insert(
                {
                    "user": str(query.user),
                    "query": str(query.messages),
                    "response": str(resp),
                }
            ).execute()

    return {"response": resp}

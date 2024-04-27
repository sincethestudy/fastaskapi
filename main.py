from typing import Union, List
from fastapi import FastAPI
from pydantic import BaseModel
from openai import AzureOpenAI
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv(override=True)

app = FastAPI()

import os
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# resource = os.environ.get("AZURE_RESOURCE_GROUP")
# deployment_name=os.environ.get("AZURE_DEPLOYMENT_NAME")

# client = AzureOpenAI(
#     api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
#     api_version="2024-03-01-preview",
#     azure_endpoint = "https://{}.openai.azure.com".format(resource),
# )

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

class Message(BaseModel):
    role: str
    content: str

class Query(BaseModel):
    messages: List[Message]
    log: bool = False
    user: str = ""


@app.post("/itsfast")
async def answer_question(query: Query):

    completion_stream = client.chat.completions.create(
        messages=[message.model_dump() for message in query.messages],
        model="llama3-70b-8192",
        stream=False,
    )
    
    resp = completion_stream.choices[0].message.content
    
    if query.log:
        supabase.table("leaderboard").insert(
            {
                "user": str(query.user),
                "query": str(query.messages),
                "response": str(resp),
            }
        ).execute()
        
    return {"response": resp}


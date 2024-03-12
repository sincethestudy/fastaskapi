from typing import Union, List
from fastapi import FastAPI
from pydantic import BaseModel
from openai import AzureOpenAI
from dotenv import load_dotenv
import os

load_dotenv(override=True)

app = FastAPI()

resource = os.environ.get("AZURE_RESOURCE_GROUP")
deployment_name=os.environ.get("AZURE_DEPLOYMENT_NAME")

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
    api_version="2024-03-01-preview",
    azure_endpoint = "https://{}.openai.azure.com".format(resource),
)

class Message(BaseModel):
    role: str
    content: str

class Query(BaseModel):
    messages: List[Message]


@app.post("/itsfast")
async def answer_question(query: Query):

    completion_stream = client.chat.completions.create(
        messages=[message.model_dump() for message in query.messages],
        model=deployment_name,
        stream=False,
    )

    return {"response": completion_stream.choices[0].message.content}

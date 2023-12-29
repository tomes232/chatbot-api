from fastapi import FastAPI

from enum import Enum

from pydantic import BaseModel

from contextlib import asynccontextmanager

from dotenv import load_dotenv



from app.models import answer_resume

from openai import OpenAI, AsyncOpenAI

from app.mongo import get_client, get_database, get_collection, get_document, read_file

from app.load import FileJson

import os

import time

import socket


class ModelName(str, Enum):
    distilbert = "distilbert"
    openai = "openai"
    #lenet = "lenet"

class input(BaseModel):
    input: str
    session_id: float | None = None

load_dotenv()


assistant = {}
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

#api_key = os.getenv("OPENAI_API_KEY")


def get_ip_address():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address




@asynccontextmanager
async def lifespan(app: FastAPI):
    print(os.getenv("OPENAI_API_KEY"))
    print(os.getenv("MONGODB_USERNAME"))
    print(os.getenv("MONGODB_PASSWORD"))
    print(get_ip_address())
    db_username = os.getenv("MONGODB_USERNAME")
    db_password = os.getenv("MONGODB_PASSWORD")
    #check if ./text/resume.txt exists
    if not os.path.exists("./text_json/resume.json"):
        db = get_database(get_client(db_username, db_password))
        collection = get_collection(db, "reume12_23")
        file = get_document(collection)
        os.makedirs("./text_json", exist_ok=True)   
        if file is None:
            print("Error: resume.json not found in database")
            return
        resume = FileJson(text = file['doc']['text'], filename = 'resume', 
                          tags=file['doc']['metadata']['tags'], 
                            url=file['doc']['metadata']['url'],
                            file=file['doc']['metadata']['file'])
        resume.save_json()
    
    # check if ./pdfs/Thomas Pickup Resume 12_23.pdf exists
    if not os.path.exists("./pdfs/Thomas Pickup Resume 12_23.pdf"):
        db = get_database(get_client(db_username, db_password))
        collection = get_collection(db, "resume")
        os.makedirs("./pdfs", exist_ok=True)  
        read_file(db, "Thomas Pickup Resume 12_23.pdf")








    # Load the ML models
    print("Loading models...")
    file = await client.files.create(file=open("./pdfs/Thomas Pickup Resume 12_23.pdf", "rb"),
                                         purpose="assistants")
    
    
    assistant['openai'] = await client.beta.assistants.create(
        name = "Portfolio Chatbot",
        instructions = "You are a chatbot on my portfolio website. You can answer questions about me from my resume.",
        tools = [{"type": "retrieval"}],    
        model = "gpt-3.5-turbo-1106",
        file_ids = [file.id]
    )

    # Make the models available
    print("Models loaded, waiting for requests...")
    
    yield

    print("Cleaning up...")
    # Clean up the ML models and release the resources
    await client.beta.assistants.files.delete(assistant_id=assistant['openai'].id, file_id=file.id)

    await client.beta.assistants.delete(assistant_id=assistant['openai'].id)
    assistant.clear()



app = FastAPI(lifespan=lifespan)



@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.put("/model/{model_name}")
async def answer(model_name: ModelName, input: input):
    if model_name == ModelName.distilbert:
        answer = answer_resume(input.input)
        return {"model": model_name, "output": answer, "session_id": input.session_id}
    
    elif model_name == ModelName.openai:

        if input.session_id is None:
            thread = await client.beta.threads.create()
            input.session_id = thread.id

        #print(thread.id)

        #print(assistant['openai'])

        message = await client.beta.threads.messages.create(thread_id=input.session_id, 
                                         role="user",
                                         content=input.input)
        #print(message)
        run = await client.beta.threads.runs.create(thread_id=input.session_id,
                                         assistant_id=assistant['openai'].id)
        #print("before run")
        #print(run.status)
        while run.status != "completed":
            time.sleep(1)
            print(run.status)

            run = await client.beta.threads.runs.retrieve(thread_id=input.session_id, run_id=run.id)
        #print("after run")
        #print(run)
        

        messages = await client.beta.threads.messages.list(thread_id=input.session_id)

        #print(run)


        #print(messages)

        #print(messages.data[0].content[0].text.value)

        #for message in reversed(messages):
        #    if message.role == "bot":
        #        return {"model": model_name, "output": message.content[0], "session_id": input.session_id}

        return {"model": model_name, "output": messages.data[0].content[0].text.value, "session_id": input.session_id}

        

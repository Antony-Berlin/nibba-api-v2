import google.generativeai as genai
from fastapi import FastAPI
from pydantic import BaseModel
import chromadb
from functions import *


from langchain_text_splitters import CharacterTextSplitter
import os
from fastapi.middleware.cors import CORSMiddleware
api = FastAPI()
api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (replace * with specific origins if needed)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)
#====DB LOAD====##====DB LOAD====##====DB LOAD====##====DB LOAD====##====DB LOAD====##====DB LOAD====##====DB LOAD====#
# load it into Chroma

client = chromadb.PersistentClient(path="vector_DB")

db = client.get_collection(name="collection_1")


#======LLM SETUP======##======LLM SETUP======##======LLM SETUP======##======LLM SETUP======##======LLM SETUP======##======LLM SETUP======#
genai.configure(api_key="AIzaSyC1SlRZ6XMyW-idxY8NX1Us8EipTWcGPrQ")

# Set up the model
generation_config = {
  "temperature": 0.3,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)  





#======API CODE======##======API CODE======##======API CODE======##======API CODE======##======API CODE======#
class ChatRequest(BaseModel):
    contents: list

@api.get("/")
async def root():
    return {"message": "Hello World"}

@api.get("/test/")
async def test():
    return {"test":"ok"}

@api.post("/chat/")
async def chat(chat_request: ChatRequest):
    question = chat_request.contents[-1]["parts"][-1]["text"] 
    if(question.lower()=="check eligibilty"):
        ques = get_elgibilty_ques(search(get_scheme_name(chat_request.contents,model)),model)
      
    query = get_search_keywords(chat_request.contents,model)
    
    chat_request.contents[-1]["parts"][-1]["text"] = make_rag_prompt(question,search(query,db))
    response = get_response(chat_request.contents,model)

    return {"response": response}

 

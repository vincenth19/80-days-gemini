from typing import Union, Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
from pydantic import BaseModel
from dotenv import load_dotenv

import os
from app.lib.file import read_yaml_file

load_dotenv()
api_key=os.getenv('GEMINI_API_KEY')
gemini_model=os.getenv('GEMINI_MODEL', 'gemini-1.5-flash')
if not api_key:
    raise ValueError("No GEMINI_API_KEY found in environment variables")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

tags_metadata = [
    {
        "name": "root",
        "description": "Redirect to docs",
    },
    {
        "name": "start",
        "description": "Get Items by ID",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]

app = FastAPI(openapi_tags=tags_metadata)
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1",
    "http://127.0.0.1:8000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
     return RedirectResponse("/docs")

@app.post('/start-game', tags=['start'])
async def start_game():
    '''
    Start the game with this endpoint
    '''
    try:
        prompts = read_yaml_file('./static/prompts.yaml')
        start_prompt = prompts.get('start', None)
        
        if not start_prompt:
            raise "No starting prompt"

        response = model.generate_content(start_prompt, stream=True)
        def generate():
            for chunk in response:
                yield chunk.text
        return StreamingResponse(generate(), media_type="text/plain")
        
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
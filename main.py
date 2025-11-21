from fastapi import FastAPI
from pydantic import BaseModel
from ellabs import elevenlabs_tts, elevenlabs_stt
from mangum import Mangum
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv
from elevenlabs import ElevenLabs

load_dotenv()

elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")

if not elevenlabs_api_key:
    raise ValueError("ELEVENLABS_API_KEY not found. Please set it in .env or Lambda environment.")

# Create the client
elevenlabs = ElevenLabs(api_key=elevenlabs_api_key)

app = FastAPI()

class Model(BaseModel):
    text: str

@app.post("/text-to-speech")
async def choose(payload: Model):
    if payload.text != "":
        return elevenlabs_tts(payload.text)
    else:
        return {"error": "Text must be added."}

@app.post("/speech-to-text")
async def select(payload: Model):
    transcript = elevenlabs_stt()
    return JSONResponse(content={"Transcript": transcript})              

handler = Mangum(app)
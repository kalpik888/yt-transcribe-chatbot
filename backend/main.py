from fastapi import FastAPI, Request , Response
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from youtube_transcriber import download_youtube_audio, transcribe_audio, ask_question
from fastapi.responses import FileResponse
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class TranscribeRequest(BaseModel):
    url: str

class AskRequest(BaseModel):
    transcript: str
    question: str

@app.get('/')
def home():
    return "backend is running"

@app.get("/download-transcript")
def download_transcript():
    transcript_path = "transcript.txt"
    
    # Let's say you already wrote transcript to this file
    if os.path.exists(transcript_path):
        return FileResponse(transcript_path, media_type='text/plain', filename='transcript.txt')
    else:
        return Response(content="Transcript not found", status_code=404)

@app.post("/transcribe")
def transcribe(data: TranscribeRequest):
    audio_path = download_youtube_audio(data.url)
    transcript = transcribe_audio(audio_path)
    return {"transcript": transcript}

@app.post("/ask")
def ask(data: AskRequest):
    answer = ask_question(data.transcript, data.question)
    return {"answer": answer}

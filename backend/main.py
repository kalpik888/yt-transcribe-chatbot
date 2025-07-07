from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from youtube_transcriber import download_youtube_audio, transcribe_audio, ask_question

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

@app.post("/transcribe")
def transcribe(data: TranscribeRequest):
    audio_path = download_youtube_audio(data.url)
    transcript = transcribe_audio(audio_path)
    return {"transcript": transcript}

@app.post("/ask")
def ask(data: AskRequest):
    answer = ask_question(data.transcript, data.question)
    return {"answer": answer}

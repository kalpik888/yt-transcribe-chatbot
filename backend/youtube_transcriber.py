import os
import subprocess
import tempfile
from openai import OpenAI
import whisper
import requests


# Step 1: Download YouTube Audio using yt-dlp
def download_youtube_audio(youtube_url):
    temp_dir = tempfile.mkdtemp()
    output_path = os.path.join(temp_dir, "audio.%(ext)s")

    command = [
        "python", "-m", "yt_dlp",
        "-x", "--audio-format", "mp3",
        "-o", output_path,
        youtube_url
    ]

    print("Downloading audio from YouTube...")
    subprocess.run(command, check=True)

    # Try to find the actual file saved in temp_dir
    for f in os.listdir(temp_dir):
        if f.startswith("audio.") and f.endswith((".mp3", ".m4a", ".webm")):
            return os.path.join(temp_dir, f)

    raise FileNotFoundError("Audio file not found.")

# Step 2: Transcribe the audio using OpenAI Whisper
def transcribe_audio(file_path):
    print("Transcribing using Whisper (local)...")
    model = whisper.load_model("base")
    result = model.transcribe(file_path)
    transcript_text = result["text"]

    # ✅ Save to file
    with open("transcript.txt", "w", encoding="utf-8") as f:
        f.write(transcript_text)

    print("Transcript saved to transcript.txt")
    return transcript_text

# Step 3: Ask groq questions about the transcript
def ask_question(transcript_text, user_question):
    api_key = "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"  
    endpoint = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    system_prompt = "You are an assistant that answers questions based on a transcript from a YouTube video."
    user_input = f"The transcript is:\n{transcript_text}\n\nUser question: {user_question}"

    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.5
    }

    response = requests.post(endpoint, headers=headers, json=payload)
    response.raise_for_status()  # Raise an error for bad responses
    return response.json()["choices"][0]["message"]["content"]

# Main execution
if __name__ == "__main__":
    yt_url = input("🔗 Enter YouTube URL: ").strip()
    try:
        audio_path = download_youtube_audio(yt_url)
        transcript = transcribe_audio(audio_path)
        print("\n✅ Transcription complete! You can now ask questions.")

        while True:
            question = input("\n❓ Ask a question (or type 'exit'): ").strip()
            if question.lower() == "exit":
                break
            answer = ask_question(transcript, question)
            print("\n💬 Answer:", answer)

    except subprocess.CalledProcessError:
        print("❌ yt-dlp failed. Make sure it's installed with: pip install yt-dlp")
    except Exception as e:
        print(f"❌ Error: {e}")

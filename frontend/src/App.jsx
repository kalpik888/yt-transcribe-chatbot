import React, { useState } from 'react';
import './App.css';

function App() {
  const [videoUrl, setVideoUrl] = useState('');
  const [transcript, setTranscript] = useState('');
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState([]);
  const [question, setQuestion] = useState('');

  const handleTranscribe = async () => {
    if (!videoUrl.trim()) return;
    setLoading(true);
    setTranscript('');
    setMessages([]);
    try {
      const res = await fetch('http://localhost:8000/transcribe', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: videoUrl })
      });
      const data = await res.json();
      setTranscript(data.transcript);
    } catch (err) {
      alert('Error transcribing video.');
    } finally {
      setLoading(false);
    }
  };

  const handleAsk = async () => {
    if (!question.trim()) return;
    const userMessage = { sender: 'user', text: question };
    setMessages([...messages, userMessage]);
    setQuestion('');
    try {
      const res = await fetch('http://localhost:8000/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ transcript, question })
      });
      const data = await res.json();
      const botMessage = { sender: 'bot', text: data.answer };
      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      alert('Failed to get response');
    }
  };

  const downloadTranscript = () => {
    fetch('http://localhost:8000/download-transcript')
      .then(response => response.blob())
      .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'transcript.txt';
        a.click();
        window.URL.revokeObjectURL(url);
      });
  };

  return (
    <div className="main-container">
      <div className="left-section">
        <h1>🎥 YouTube Chatbot</h1>
        <p className="description">
          Paste a YouTube video link, and this chatbot will transcribe the audio
          using AI and let you ask questions about the video content.
        </p>
        <ul>
          <li>⏱️ Transcribes long videos fast</li>
          <li>🧠 Answers your questions from the transcript</li>
          <li>📄 Displays the full transcript for reference</li>
        </ul>
        <p className="note">Powered by Whisper + GPT API</p>
      </div>

      <div className="right-section">
        <div className="input-area">
          <input
            type="text"
            placeholder="Paste YouTube URL..."
            value={videoUrl}
            onChange={(e) => setVideoUrl(e.target.value)}
          />
          <button onClick={handleTranscribe}>Transcribe</button>
          <button onClick={downloadTranscript} className="px-4 py-2 bg-blue-500 text-white rounded">
            Download Transcript (.txt)
          </button>
        </div>

        {loading && <div className="loading">⏳ Transcribing...</div>}

        {transcript && (
          <>
            <div className="transcript-box">
              <h3>📄 Transcript</h3>
              <div className="transcript">{transcript}</div>
            </div>

            <div className="chat-area">
              <h3>💬 Ask about the video</h3>
              <div className="chat-messages">
                {messages.map((msg, index) => (
                  <div key={index} className={`chat-bubble ${msg.sender}`}>
                    {msg.text}
                  </div>
                ))}
              </div>

              <div className="chat-input">
                <input
                  type="text"
                  placeholder="Ask something..."
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && handleAsk()}
                />
                <button onClick={handleAsk}>Send</button>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default App;
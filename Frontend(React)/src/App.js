import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);

  // ---------------- UPLOAD PDF ----------------
  const uploadPDF = async () => {
    if (!file) return alert("Select a PDF first");

    const formData = new FormData();
    formData.append("file", file);

    const res = await axios.post(
      "http://127.0.0.1:8000/upload-pdf",
      formData
    );

    alert(res.data.message + " | Chunks: " + res.data.chunks_created);
  };

  // ---------------- ASK QUESTION ----------------
  const askQuestion = async () => {
    if (!question) return;

    const userMsg = { type: "user", text: question };
    setMessages((prev) => [...prev, userMsg]);

    const res = await axios.post(
      "http://127.0.0.1:8000/ask",
      null,
      {
        params: { question }
      }
    );

    const aiMsg = { type: "ai", text: res.data.answer };

    setMessages((prev) => [...prev, aiMsg]);
    setQuestion("");
  };

  return (
    <div className="container">
      <h2>🤖 Agentic RAG AI Chatbot</h2>

      {/* Upload */}
      <div className="upload-box">
        <input type="file" onChange={(e) => setFile(e.target.files[0])} />
        <button onClick={uploadPDF}>Upload PDF</button>
      </div>

      {/* Chat */}
      <div className="chat-box">
        {messages.map((msg, i) => (
          <div key={i} className={msg.type === "user" ? "user-msg" : "ai-msg"}>
            {msg.text}
          </div>
        ))}
      </div>

      {/* Input */}
      <div className="input-box">
        <input
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask something..."
        />
        <button onClick={askQuestion}>Send</button>
      </div>
    </div>
  );
}

export default App;
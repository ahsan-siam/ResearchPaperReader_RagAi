# 🤖 Agentic RAG AI Chatbot (Full Stack)

A full-stack **Agentic AI + RAG (Retrieval-Augmented Generation)** web application that allows users to upload PDF documents and ask questions based on their content. The system uses vector search + LLM (Ollama) to generate intelligent answers.

---

# 🚀 Features

- 📄 Upload PDF documents
- 🧠 AI-powered question answering
- 🔍 RAG (Retrieval-Augmented Generation)
- 🧩 Vector database (ChromaDB)
- 🤖 Local LLM using Ollama (Llama3)
- ⚡ FastAPI backend
- 🌐 React.js frontend
- 📱 Mobile responsive UI
- 🧠 Multi-step AI reasoning (agent-style flow)

---

# 🏗️ Tech Stack

## Frontend
- React.js
- Axios
- HTML/CSS

## Backend
- FastAPI
- Python
- PyPDF
- LangChain (text splitting + embeddings)
- ChromaDB (vector database)
- Ollama (LLM - Llama3)

---

# 📁 Project Structure
rag-agentic-ai/
│
├── backend/
│   ├── main.py                # FastAPI backend (RAG + AI logic)
│   ├── requirements.txt       # Python dependencies
│   ├── uploads/              # Uploaded PDF files
│   └── db/                   # ChromaDB vector storage
│
├── frontend/
│   ├── public/
│   │   └── index.html
│   │
│   ├── src/
│   │   ├── App.js            # Main React UI
│   │   ├── App.css           # Styling (mobile responsive UI)
│   │   ├── index.js
│   │   └── components/       # Optional future expansion
│   │
│   ├── package.json
│   └── node_modules/         # ignored in git (.gitignore)
│
├── .gitignore
└── README.md

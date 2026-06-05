from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader
import os
import shutil

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

import ollama

app = FastAPI()

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

vectorstore = None


# ---------------- HOME ----------------
@app.get("/")
def home():
    return {"message": "Agentic RAG System Running"}


# ---------------- UPLOAD PDF ----------------
@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    global vectorstore

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # -------- extract text --------
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text

    if not text.strip():
        return {"error": "No text found in PDF (maybe scanned image PDF)"}

    # -------- split text --------
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=150
    )

    chunks = splitter.split_text(text)

    # -------- embeddings --------
    embedding = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    # -------- vector DB --------
    vectorstore = Chroma.from_texts(
        texts=chunks,
        embedding=embedding,
        persist_directory="db"
    )

    return {
        "message": "PDF processed successfully",
        "chunks_created": len(chunks)
    }


# ---------------- ASK (FIXED RAG) ----------------
@app.post("/ask")
async def ask(question: str):
    global vectorstore

    if vectorstore is None:
        return {"answer": "Please upload a PDF first"}

    # -------- retrieval --------
    docs = vectorstore.similarity_search(question, k=5)

    if not docs:
        return {"answer": "No relevant information found in document"}

    context = "\n\n".join([d.page_content for d in docs])

    # DEBUG (IMPORTANT)
    print("\n========== RETRIEVED CONTEXT ==========\n")
    print(context[:1000])
    print("\n=======================================\n")

    # -------- strict RAG prompt --------
    prompt = f"""
You are a strict document-based AI assistant.

RULES:
- Use ONLY the given context
- If answer not in context, say "Not found in document"
- Do not guess

CONTEXT:
{context}

QUESTION:
{question}
"""

    response = ollama.chat(
        model="llama3",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return {
        "question": question,
        "answer": response["message"]["content"],
        "context_length": len(context)
    }
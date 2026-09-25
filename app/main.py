from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from langchain_community.vectorstores import Chroma

import os


from rag.full_pipeline import EnterpriseRAG
from rag.document_processor import process_document

from shadowmemory.pipeline import analyze_context





app = FastAPI(

    title="ShadowMemory Enterprise RAG",

    description="Secure AI assistant with RAG + ShadowMemory + Gemini",

    version="1.0"

)





# ==========================
# CORS
# ==========================


app.add_middleware(

    CORSMiddleware,

    allow_origins=[

        "http://localhost:5173",

        "http://127.0.0.1:5173"

    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],

)







# ==========================
# Load RAG System
# ==========================


rag_system = EnterpriseRAG()







# ==========================
# Request Models
# ==========================


class QuestionRequest(BaseModel):

    question: str






class Document(BaseModel):

    text: str

    source: str

    author: str | None = None






class AnalyzeRequest(BaseModel):

    documents: list[Document]








# ==========================
# Health
# ==========================


@app.get("/")

def home():

    return {

        "system":
            "ShadowMemory",


        "status":
            "running"

    }







@app.get("/health")

def health():

    return {

        "api":
            "healthy",


        "rag":
            "connected",


        "security":
            "enabled",


        "llm":
            "gemini"

    }









# ==========================
# ShadowMemory Only
# ==========================


@app.post("/analyze")

def analyze(

    request: AnalyzeRequest

):


    result = analyze_context(

        request.documents

    )


    return result







# ==========================
# Full RAG + Gemini
# ==========================


@app.post("/ask")

def ask(

    request: QuestionRequest

):


    result = rag_system.ask(

        request.question

    )


    return result







# ==========================
# PDF Upload
# ==========================


@app.post("/upload")

async def upload_document(

    file: UploadFile = File(...)

):


    upload_folder = "data/raw_documents"



    os.makedirs(

        upload_folder,

        exist_ok=True

    )





    file_path = os.path.join(

        upload_folder,

        file.filename

    )







    # Save file

    with open(

        file_path,

        "wb"

    ) as f:


        content = await file.read()


        f.write(content)







    # Process PDF

    result = process_document(

        file_path

    )







    # Refresh Chroma after upload

    rag_system.vector_db = Chroma(

        persist_directory="data/chroma_db",

        embedding_function=

        rag_system.embedding_model

    )






    return result
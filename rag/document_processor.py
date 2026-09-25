import os
import hashlib

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
DB_PATH = "data/chroma_db"



def generate_file_id(file_path):

    with open(file_path,"rb") as f:

        return hashlib.md5(
            f.read()
        ).hexdigest()



def process_document(file_path):


    # =========================
    # Load PDF
    # =========================


    loader = PyPDFLoader(
        file_path
    )


    documents = loader.load()



    if not documents:

        return {

            "status":"failed",

            "message":"No content extracted"

        }



    file_name = os.path.basename(
        file_path
    )



    file_id = generate_file_id(
        file_path
    )




    # =========================
    # Metadata
    # =========================


    for doc in documents:


        doc.metadata.update({

            "company_file":
                file_name,


            "source":
                file_path,


            "author":
                "company_upload",


            "document_id":
                file_id,


            "page_label":
                str(
                    doc.metadata.get(
                        "page",
                        0
                    ) + 1
                )


        })





    # =========================
    # Chunking
    # =========================


    splitter = RecursiveCharacterTextSplitter(

        chunk_size=1200,

        chunk_overlap=200

    )


    chunks = splitter.split_documents(

        documents

    )





    # =========================
    # Embeddings
    # =========================


    embeddings = HuggingFaceEmbeddings(

        model_name=
        "all-MiniLM-L6-v2"

    )





    # =========================
    # Chroma Update
    # =========================


    db = Chroma(

        persist_directory=DB_PATH,

        embedding_function=embeddings

    )



    # Avoid duplicate upload


    existing = db.get(

        where={

            "document_id":file_id

        }

    )



    if existing["ids"]:


        return {

            "status":"already_exists",

            "file":file_name,

            "chunks_added":0

        }




    db.add_documents(

        chunks

    )




    return {


        "status":

            "success",


        "file":

            file_name,


        "chunks_added":

            len(chunks)

    }
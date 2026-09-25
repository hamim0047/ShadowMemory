from langchain_community.vectorstores import Chroma

from langchain_community.embeddings import HuggingFaceEmbeddings

from loader import load_company_documents
from chunker import create_chunks



embedding_model = HuggingFaceEmbeddings(

model_name="all-MiniLM-L6-v2"

)



documents=load_company_documents(

"data/raw_documents"

)



chunks=create_chunks(
    documents
)



db=Chroma.from_documents(

documents=chunks,

embedding=embedding_model,

persist_directory="data/chroma_db"

)


print(
"Real company knowledge base created"
)
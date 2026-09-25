from loader import load_pdf
from chunker import split_documents
from rag.create_vector_db import create_database



pdf="data/company_docs/hr_policy.pdf"



docs=load_pdf(pdf)


chunks=split_documents(
    docs
)


db=create_database(
    chunks
)


print(
"Company RAG database created"
)
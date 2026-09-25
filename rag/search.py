from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings


embedding_model = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)


db = Chroma(
    persist_directory="data/chroma_db",
    embedding_function=embedding_model
)


question = """
What are the major business risks mentioned in the annual report?
"""


results = db.similarity_search(
    question,
    k=3
)


for i, doc in enumerate(results):

    print("\n====================")
    print("RESULT:", i+1)
    print("====================")

    print(
        doc.page_content[:1000]
    )

    print(
        "SOURCE:",
        doc.metadata
    )
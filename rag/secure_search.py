import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

from shadowmemory.pipeline import analyze_context



embedding_model = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)


db = Chroma(
    persist_directory="data/chroma_db",
    embedding_function=embedding_model
)



question = """
What are the major risks mentioned in Tesla annual report?
"""



# Retrieve documents

results = db.similarity_search(
    question,
    k=3
)



# Convert retrieved chunks for ShadowMemory

shadow_documents=[]


for doc in results:

    shadow_documents.append(

        type(
            "Document",
            (),
            {

            "text":
            doc.page_content,


            "source":
            doc.metadata.get(
                "company_file",
                "unknown"
            ),


            "author":
            "public_company"

            }
        )

    )



# Security analysis

combined_text = "\n\n".join(
    [
        doc.page_content
        for doc in results
    ]
)


combined_document = type(
    "Document",
    (),
    {

    "text": combined_text,

    "source":
        "retrieved_context",

    "author":
        "public_company"

    }
)


security_result = analyze_context(
    [combined_document]
)



print("\nQUESTION:")
print(question)


print("\nSHADOWMEMORY RESULT:")

for result in security_result:

    print("===================")

    print(
        "Source:",
        result["source"]
    )

    print(
        "Risk:",
        result["risk_level"]
    )

    print(
        "Risk Score:",
        result["risk_score"]
    )

    print(
        "Trust:",
        result["trust_score"]
    )

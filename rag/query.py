from rag.create_vector_db import embedding_model
from langchain_community.vectorstores import Chroma

from shadowmemory.pipeline import analyze_context



db = Chroma(

persist_directory="./chroma_db",

embedding_function=embedding_model

)



def ask_company(question):


    retriever=db.as_retriever(
        search_kwargs={
            "k":3
        }
    )


    documents=retriever.invoke(
        question
    )


    shadow_input=[]


    for doc in documents:


        shadow_input.append(

            type(
                "Document",
                (),
                {

                "text":
                doc.page_content,


                "source":
                doc.metadata.get(
                    "source",
                    "unknown"
                ),

                "author":
                None

                }

            )

        )


    security_result=analyze_context(
        shadow_input
    )


    return security_result
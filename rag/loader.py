from langchain_community.document_loaders import PyPDFLoader
import os



def load_company_documents(folder):


    documents=[]


    for file in os.listdir(folder):


        if file.endswith(".pdf"):


            path=os.path.join(
                folder,
                file
            )


            loader=PyPDFLoader(
                path
            )


            docs=loader.load()


            for doc in docs:

                doc.metadata["company_file"]=file


            documents.extend(
                docs
            )


    return documents
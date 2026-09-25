from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings


from shadowmemory.pipeline import analyze_context
from shadowmemory.sanitizer import sanitize
from shadowmemory.logger import save_log


from rag.gemini_rag import generate_answer





class EnterpriseRAG:



    def __init__(self):


        self.embedding_model = HuggingFaceEmbeddings(

            model_name="all-MiniLM-L6-v2"

        )


        self.vector_db = Chroma(

            persist_directory="data/chroma_db",

            embedding_function=self.embedding_model

        )






    # ==================================================
    # STEP 1 : DOCUMENT RETRIEVAL
    # ==================================================


    def retrieve_documents(self, question):


        results = self.vector_db.similarity_search_with_score(

            question,

            k=15

        )


        documents=[]



        for doc, score in results:


            content=doc.page_content.lower()



            if (

                "table of contents" in content

                and len(content)<800

            ):

                continue



            documents.append(doc)





        keywords=[


            "employee",
            "policy",
            "procedure",
            "attendance",
            "leave",
            "benefit",
            "salary",
            "security",
            "confidential",
            "company",


            "risk",
            "business",
            "financial",
            "market",
            "customer",
            "operation",
            "production",
            "supply",
            "cost",
            "demand",
            "competition"

        ]



        filtered=[]



        for doc in documents:


            text=doc.page_content.lower()



            score=sum(

                1

                for word in keywords

                if word in text

            )



            if score>=2:

                filtered.append(doc)



        return filtered[:5]









    # ==================================================
    # STEP 2 : SHADOWMEMORY SECURITY + SANITIZATION
    # ==================================================


    def run_shadowmemory(self, documents):


        shadow_documents=[]



        for doc in documents:


            shadow_documents.append(

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

                        doc.metadata.get(

                            "author",

                            None

                        ),


                    "metadata":

                        doc.metadata


                    }

                )

            )





        security_results = analyze_context(

            shadow_documents

        )




        print(

            "\n===== DOCUMENT SECURITY RESULTS ====="

        )



        for result in security_results:


            print(

                result["source"],

                "=>",

                result["risk_level"],

                result["risk_score"]

            )







        # ================================
        # SANITIZE EVERY DOCUMENT
        # ================================


        safe_context=[]

        removed_content=[]



        for result in security_results:


            cleaned=sanitize(

                result["sanitized_context"]

            )



            safe_context.append(

                cleaned["clean_text"]

            )


            removed_content.extend(

                cleaned["removed"]

            )







        highest_risk=max(

            security_results,

            key=lambda x:

            x["risk_score"]

        )





        highest_risk["sanitized_context"] = "\n\n".join(

            safe_context

        )



        highest_risk["removed_content"]=removed_content



        if removed_content:


            highest_risk["sanitization_status"]="Applied"


        else:


            highest_risk["sanitization_status"]="Not Required"



        return highest_risk










    # ==================================================
    # STEP 3 : MAIN RAG PIPELINE
    # ==================================================


    def ask(self, question):


        documents=self.retrieve_documents(

            question

        )




        if not documents:


            return {


                "status":"FAILED",


                "message":

                    "No relevant documents found"

            }







        print(

            "\n===== RETRIEVED DOCUMENTS ====="

        )



        for doc in documents:


            print(

                "SOURCE:",

                doc.metadata.get(

                    "company_file",

                    "unknown"

                )

            )


            print(

                "PAGE:",

                doc.metadata.get(

                    "page_label",

                    "unknown"

                )

            )


            print(

                doc.page_content[:300]

            )


            print("----------------")








        # ShadowMemory

        security=self.run_shadowmemory(

            documents

        )





        print(

            "\n===== SHADOWMEMORY ====="

        )


        print(

            "Risk:",

            security["risk_level"]

        )


        print(

            "Score:",

            security["risk_score"]

        )








        # ================================
        # BLOCK ONLY IF NOTHING REMAINS
        # ================================


        if len(

            security["sanitized_context"].strip()

        ) < 50:



            save_log(

                {


                "query":

                    question,


                "risk_level":

                    security["risk_level"],


                "risk_score":

                    security["risk_score"],


                "removed_content":

                    security.get(

                        "removed_content",

                        []

                    ),


                "action":

                    "BLOCKED"

                }

            )



            return {


                "status":

                    "BLOCKED",


                "reason":

                    "No safe information remained after sanitization",


                "security":

                    security

            }









        # ================================
        # GEMINI RESPONSE
        # ================================


        answer=generate_answer(

            question,

            security["sanitized_context"]

        )









        # ================================
        # SOURCE INFORMATION
        # ================================


        sources=[]



        for doc in documents:


            sources.append(

                {


                "file":

                    doc.metadata.get(

                        "company_file",

                        "unknown"

                    ),


                "page":

                    doc.metadata.get(

                        "page_label",

                        "unknown"

                    )

                }

            )









        # ================================
        # AUDIT LOG
        # ================================


        save_log(

            {


            "query":

                question,


            "source":

                sources,


            "risk_level":

                security["risk_level"],


            "risk_score":

                security["risk_score"],


            "removed_content":

                security.get(

                    "removed_content",

                    []

                ),


            "action":

                "SANITIZED_AND_PASSED"

                if security["removed_content"]

                else

                "PASSED"

            }

        )









        # ================================
        # FRONTEND SECURITY DATA
        # ================================


        security_summary={


            "source":

                security.get(

                    "source",

                    "unknown"

                ),



            "risk_level":

                security.get(

                    "risk_level"

                ),



            "risk_score":

                security.get(

                    "risk_score"

                ),



            "trust_score":

                security.get(

                    "trust_score"

                ),



            "removed_content":

                security.get(

                    "removed_content",

                    []

                ),



            "sanitized_context":

    security.get(

        "sanitized_context",

        ""

    )[:500],



            "sanitization_status":

                security.get(

                    "sanitization_status",

                    "Not Required"

                )

        }







        return {


            "status":

                "SUCCESS",


            "answer":

                answer,


            "sources":

                sources,


            "security":

                security_summary

        }
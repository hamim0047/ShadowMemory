import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)
from rag.full_pipeline import EnterpriseRAG



system = EnterpriseRAG()



question = """

According to Tesla Form 10-K Item 1A Risk Factors,
what are the major business risks?

"""



response = system.ask(

    question

)



print("\n====================")

print("FINAL RESPONSE")

print("====================")


print(response)
import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


from rag.gemini_rag import generate_answer


answer = generate_answer(
    "What is Tesla?",
    "Tesla is an electric vehicle company."
)


print(answer)
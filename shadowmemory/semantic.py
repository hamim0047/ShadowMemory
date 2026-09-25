from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import re


model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)



attack_patterns = [

    "ignore previous instructions",

    "ignore all previous instructions",

    "forget your rules",

    "override system prompt",

    "override instructions",

    "reveal confidential information",

    "reveal internal documents",

    "provide unrestricted access",

    "share private data",

    "disable security",

    "bypass security",

    "execute unauthorized commands",

    "do not follow instructions"

]



attack_vectors = model.encode(
    attack_patterns
)



def normalize_text(text):

    text = text.lower()

    # remove PDF spacing problems
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()





def detect_injection(text):


    normalized = normalize_text(text)


    # =========================
    # RULE BASED DETECTION
    # =========================

    for pattern in attack_patterns:


        if pattern in normalized:


            return {


                "injection_score":0.95,

                "detected":True,

                "matched_pattern":pattern,

                "method":"keyword_match"

            }





    # =========================
    # SEMANTIC DETECTION
    # =========================


    vector = model.encode(
        [normalized]
    )


    similarity = cosine_similarity(

        vector,

        attack_vectors

    )[0]



    score=float(max(similarity))



    detected = False


    # Only treat strong similarity as attack

    if score >= 0.75:

        detected = True



    return {


        "injection_score":

            round(score,3),


        "detected":

            detected,


        "matched_pattern":

            attack_patterns[

                similarity.argmax()

            ],


        "method":

            "semantic_similarity"

    }
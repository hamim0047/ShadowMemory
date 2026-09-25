
from .parser import parse_document
from .semantic import detect_injection
from .trust import calculate_trust
from .risk import calculate_risk,risk_level
from .sanitizer import sanitize
from .logger import save_log



def analyze_context(documents):


    results=[]



    for doc in documents:


        parsed=parse_document(
            doc
        )


        injection=detect_injection(
            parsed["content"]
        )


        trust=calculate_trust(
            parsed["metadata"]
        )



        risk=calculate_risk(

    injection["injection_score"],

    trust,

    injection["detected"]

)


        cleaned=sanitize(
            parsed["content"]
        )


        output={


            "source":
                parsed["metadata"]["source"],


            "injection":
                injection,


            "trust_score":
                trust,


            "risk_score":
                risk,


            "risk_level":
                risk_level(risk),


            "sanitized_context":
                cleaned["clean_text"],


            "removed_content":
                cleaned["removed"]

        }



        save_log(output)


        results.append(output)



    return results

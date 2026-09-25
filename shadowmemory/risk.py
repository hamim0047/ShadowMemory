def calculate_risk(injection_score, trust_score, detected):


    # If actual injection pattern detected
    if detected:


        risk = (

            injection_score * 0.90

            +

            (1 - trust_score) * 0.10

        )


    else:


        # Normal enterprise documents
        # Reduce impact of semantic similarity

        risk = (

            injection_score * 0.30

            +

            (1 - trust_score) * 0.70

        )


    return round(risk,3)





def risk_level(score):


    if score >= 0.70:

        return "HIGH"


    elif score >= 0.40:

        return "MEDIUM"


    else:

        return "LOW"
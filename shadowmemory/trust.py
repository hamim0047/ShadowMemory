def calculate_trust(metadata):


    score = 1.0



    source = metadata.get(
        "source",
        ""
    ).lower()



    author = metadata.get(
        "author",
        ""
    )



    company_file = metadata.get(
        "company_file",
        ""
    )



    document_id = metadata.get(
        "document_id"
    )



    # =========================
    # Source Verification
    # =========================


    if not source or source == "unknown":

        score -= 0.4



    # External source penalty

    if "external" in source:

        score -= 0.2



    # =========================
    # Author Verification
    # =========================


    if not author:

        score -= 0.2



    if author == "company_upload":

        score += 0.05



    # =========================
    # File Metadata
    # =========================


    if not company_file:

        score -= 0.1



    # =========================
    # Document Identity
    # =========================


    if not document_id:

        score -= 0.1




    # =========================
    # Final score
    # =========================


    return round(

        max(

            min(score,1),

            0

        ),

        3

    )

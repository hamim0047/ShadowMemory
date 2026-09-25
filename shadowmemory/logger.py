import json
import os
from datetime import datetime



FILE = "data/audit_logs.json"





def save_log(data):


    os.makedirs(

        "data",

        exist_ok=True

    )



    logs = []



    # Load existing logs

    if os.path.exists(FILE):


        try:

            with open(FILE, "r") as f:

                logs = json.load(f)


        except json.JSONDecodeError:

            logs = []






    log_entry = {


        "timestamp":

            str(datetime.now()),



        "query":

            data.get(

                "query",

                ""

            ),



        "source":

            data.get(

                "source",

                []

            ),



        "risk_level":

            data.get(

                "risk_level",

                "UNKNOWN"

            ),



        "risk_score":

            data.get(

                "risk_score",

                0

            ),



        "injection_detected":

            data.get(

                "injection_detected",

                False

            ),



        "matched_pattern":

            data.get(

                "matched_pattern",

                None

            ),



        "action":

            data.get(

                "action",

                "UNKNOWN"

            ),



        "removed_content":

            data.get(

                "removed_content",

                []

            )

    }





    logs.append(log_entry)





    with open(

        FILE,

        "w"

    ) as f:


        json.dump(

            logs,

            f,

            indent=4

        )



    return log_entry
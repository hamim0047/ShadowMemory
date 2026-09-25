import requests
import os


documents = {

    "tesla_10k_2024.pdf":
    "https://www.annualreports.com/HostedData/AnnualReportArchive/t/NASDAQ_TSLA_2024.pdf",


    "microsoft_annual_report_2024.pdf":
    "https://www.annualreports.com/HostedData/AnnualReportArchive/m/NASDAQ_MSFT_2024.pdf"

}


os.makedirs(
    "data/raw_documents",
    exist_ok=True
)


for filename, url in documents.items():

    print("Downloading:", filename)


    response = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0"
        },
        timeout=60
    )


    print(
        "Status:",
        response.status_code
    )

    print(
        "Type:",
        response.headers.get("content-type")
    )


    if response.status_code == 200:

        path=os.path.join(
            "data/raw_documents",
            filename
        )


        with open(path,"wb") as f:

            f.write(
                response.content
            )


        print(
            "Saved:",
            path
        )


print("Download completed")
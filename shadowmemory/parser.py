def parse_document(document):

    return {

        "content":
            document.text.strip(),

        "metadata":{

            "source":
                document.source,

            "author":
                document.author

        }

    }

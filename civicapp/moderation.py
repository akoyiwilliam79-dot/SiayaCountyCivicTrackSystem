from langdetect import detect


BAD_WORDS = [
    "idiot",
    "stupid",
    "fool",
    "mjinga",
    "mpumbavu"
]


def detect_language(text):

    try:
        return detect(text)
    except:
        return "unknown"



def detect_abuse(text):

    text = text.lower()

    found = []

    for word in BAD_WORDS:
        if word in text:
            found.append(word)


    if found:
        return {
            "flagged": True,
            "words": found
        }


    return {
        "flagged": False
    }
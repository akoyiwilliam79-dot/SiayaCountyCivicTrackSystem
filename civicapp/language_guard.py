from langdetect import detect


BAD_WORDS = [
    "idiot",
    "stupid",
    "fool",
    "mjinga",
    "mpumbavu",
    "shenzi",
    "mchoyo",
    "mnyanyasaji",
    "wajinga",
]


def check_language(text):

    try:
        language = detect(text)
    except:
        language = "unknown"


    text_lower = text.lower()


    detected = []

    for word in BAD_WORDS:
        if word in text_lower:
            detected.append(word)


    if detected:

        return {
            "allowed": False,
            "language": language,
            "message":
            "Please use respectful language. "
            "Abusive or inappropriate language is not allowed."
        }


    return {
        "allowed": True,
        "language": language
    }
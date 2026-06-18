BAD_WORDS = [
    "stupid",
    "idiot",
    "useless",
    "lazy",
    "corrupt",
    "fool",
    "trash",
]


SUGGESTIONS = {
    "poor road": "Road infrastructure challenge",
    "bad road": "Road maintenance concern",
    "terrible drainage": "Drainage improvement need",
    "garbage everywhere": "Waste management concern",
    "dirty environment": "Environmental cleanliness concern",
    "broken streetlight": "Street lighting issue",
    "no water": "Water supply challenge",
    "unsafe area": "Public safety concern",
    "bad service": "Service improvement opportunity",
}


def check_abuse(text):

    text = text.lower()

    for word in BAD_WORDS:
        if word in text:
            return True

    return False



def suggest_wording(text):

    text = text.lower()

    for word, suggestion in SUGGESTIONS.items():
        if word in text:
            return suggestion

    return None



def check_report(text):

    result = {
        "allowed": True,
        "suggestion": None,
        "reason": None
    }


    if check_abuse(text):
        result["allowed"] = False
        result["reason"] = "Please use respectful language."

        return result


    suggestion = suggest_wording(text)

    if suggestion:
        result["suggestion"] = suggestion


    if len(text.strip()) < 20:
        result["allowed"] = False
        result["reason"] = "Please provide more details."


    return result
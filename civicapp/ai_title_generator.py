import re


def generate_title(text):

    text = text.lower()


    # remove extra spaces
    text = re.sub(r"\s+", " ", text)


    issues = {


        "Road infrastructure concerns - damaged road sections requiring attention":
        [
            "road",
            "roads",
            "pothole",
            "hole",
            "tarmac",
            "murram",
            "path",
            "street",
            "vehicle cannot pass",
            "car cannot pass",
            "road destroyed",
            "road damaged",
            "road broken",
            "road condition",
            "impassable",
            "rough road",
            "bad network",
        ],



        "Drainage improvement and maintenance concerns":
        [
            "drain",
            "drainage",
            "sewer",
            "blocked water",
            "open drainage",
            "dirty water",
            "waste water",
            "water channel",
        ],



        "Flood mitigation and water management concerns":
        [
            "flood",
            "flooding",
            "water everywhere",
            "rain water",
            "houses flooded",
            "water entering house",
        ],



        "Waste management and environmental cleanliness concerns":
        [
            "garbage",
            "trash",
            "rubbish",
            "dump",
            "dumping",
            "dirty",
            "smell",
            "waste",
            "litter",
            "environment",
        ],



        "Street lighting infrastructure issues":
        [
            "light",
            "streetlight",
            "lamp",
            "dark",
            "no lights",
            "night darkness",
        ],



        "Water supply challenges requiring intervention":
        [
            "water",
            "tap",
            "dry tap",
            "no water",
            "water shortage",
            "pipes",
            "leak",
        ],



        "Electricity supply and infrastructure concerns":
        [
            "electricity",
            "power",
            "token",
            "blackout",
            "transformer",
            "lights off",
        ],



        "Public safety and security concerns":
        [
            "unsafe",
            "crime",
            "thieves",
            "robbery",
            "danger",
            "security",
            "fear",
        ],



        "Healthcare service delivery concerns":
        [
            "hospital",
            "clinic",
            "doctor",
            "nurse",
            "medicine",
            "drugs",
            "health",
        ],



        "Education infrastructure and service concerns":
        [
            "school",
            "teacher",
            "class",
            "student",
            "learning",
            "desk",
            "classroom",
        ],



        "Market infrastructure and management concerns":
        [
            "market",
            "stall",
            "business",
            "vendor",
            "trader",
        ],



        "Sanitation and public health concerns":
        [
            "toilet",
            "latrine",
            "sewage",
            "sanitation",
            "hygiene",
        ],



        "Transport and mobility concerns":
        [
            "traffic",
            "jam",
            "matatu",
            "transport",
            "parking",
        ],



        "Building safety and construction concerns":
        [
            "building",
            "construction",
            "house",
            "collapsed",
            "wall",
            "unsafe building",
        ],



        "Animal control and community safety concerns":
        [
            "dog",
            "stray",
            "animal",
            "livestock",
        ],



        "Service improvement and operational concerns":
        [
            "slow",
            "delay",
            "waiting",
            "ignored",
            "no response",
            "worker",
            "office",
        ],



        "Public service delivery and accountability concerns":
        [
            "bribe",
            "corrupt",
            "corruption",
            "asked money",
            "officer",
        ],


    }



    scores = {}



    # scoring system
    for title, keywords in issues.items():

        score = 0

        for word in keywords:

            if word in text:
                score += 1


        scores[title] = score



    best_match = max(
        scores,
        key=scores.get
    )



    # only suggest if confidence exists
    if scores[best_match] > 0:

        return best_match


    return None
from nbsap.database import mongo

def add_language_fields_to_indicators():

    indicators = mongo.db.indicators.find()
    keys = ["status", "classification", "sources", "question", "measurer",
            "sub_indicator", "head_indicator", "requirements", "name"]

    for indicator in indicators:
        for k, v in indicator.items():
            if k in keys:
                indicator[k] = { "en": v,
                      "fr": "",
                      "nl": ""
                    }

        if indicator.get('links'):
            for link in indicator["links"]:
                link[0] = { "en": link[0],
                            "fr" : "",
                            "nl": ""
                          }
        mongo.db.indicators.save(indicator)

extra_shell_context = {
    "add_language_fields_to_indicators": add_language_fields_to_indicators
}

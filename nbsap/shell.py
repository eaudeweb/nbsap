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

def indicator_link_list_to_dict():

    indicators = mongo.db.indicators.find()

    for indicator in indicators:

        if indicator.get('links'):

            old_list = indicator['links']
            indicator['links'] = []

            for link in old_list:
                link = { "url_name": link[0],
                         "url": link[1]
                       }
                indicator['links'].append(link)

        mongo.db.indicators.save(indicator)

def split_scale_in_list():

    indicators = mongo.db.indicators.find()

    for indicator in indicators:

        if indicator.get('scale'):
            indicator['scale'] = indicator['scale'].split(', ')

        mongo.db.indicators.save(indicator)

def convert_indicator_ids_to_int():

    indicators = mongo.db.indicators.find()

    for indicator in indicators:
        indicator['id'] = int(indicator['id'])
        mongo.db.indicators.save(indicator)

def update_indicators():
    add_language_fields_to_indicators()
    indicator_link_list_to_dict()
    split_scale_in_list()
    convert_indicator_ids_to_int()

def clean_whitespace():
    from nbsap.schema.refdata import language
    goals = mongo.db.goals.find()
    targets = mongo.db.targets.find()

    for goal in goals:
        for lang in language.keys():
            if goal['description'][lang] == '\n\n':
                goal['description'][lang] = ''
                mongo.db.goals.save(goal)

    for target in targets:
        for lang in language.keys():
            if target['description'][lang] == '\n\n':
                target['description'][lang] = ''
                mongo.db.targets.save(target)

extra_shell_context = {
    "add_language_fields_to_indicators": add_language_fields_to_indicators,
    "indicator_link_list_to_dict": indicator_link_list_to_dict,
    "update_indicators": update_indicators,
    "split_scale_in_list": split_scale_in_list,
    "convert_indicator_ids_to_int": convert_indicator_ids_to_int,
    "clean_whitespace": clean_whitespace
}

import schema

from nbsap.database import mongo

def update_actions_into_objectives():
    actions = mongo.db.actions.find()
    objectives = mongo.db.objectives.find()

    for objective in objectives:
        if 'actions' not in objective.keys():
            objective['actions'] = []

        for subobj1 in objective['subobjs']:
            if 'actions' not in subobj1.keys():
                subobj1['actions'] = []

            for subobj2 in subobj1['subobjs']:
                if 'actions' not in subobj2:
                    subobj2['actions']= []

                for subobj3 in subobj2['subobjs']:
                    if 'actions' not in subobj3:
                        subobj3['actions'] = []

                    for subobj4 in subobj3['subobjs']:
                        if 'actions' not in subobj4:
                            subobj4['actions'] = []

        mongo.db.objectives.save(objective)

    for action in actions:
        obj_id = action['id']
        for sub_action in action['actions']:
            subobj_id = sub_action['id']

            objectives = mongo.db.objectives.find()

            for objective in objectives:
                if objective['id'] == obj_id:
                    for subobj in objective['subobjs']:
                        if subobj['id'] == subobj_id:
                            subobj['actions'].append(sub_action)
                            subobj['actions'][0]['id'] = 1

                mongo.db.objectives.save(objective)

def update_objectives():
    objectives = mongo.db.objectives.find()

    for objective in objectives:
        if 'subobjs' not in objective.keys():
            objective['subobjs'] = []
        else:
            for subobj in objective['subobjs']:
               if 'subobjs' not in subobj:
                   subobj['subobjs'] = []

        mongo.db.objectives.save(objective)

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
    actions = mongo.db.actions.find()

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

    for action in actions:
        for sub_action in action['actions']:
            for lang in language.keys():
                if sub_action['body'][lang] == '\n\n':
                    sub_action['body'][lang] = ''
        mongo.db.actions.save(action)

extra_shell_context = {
    "add_language_fields_to_indicators": add_language_fields_to_indicators,
    "indicator_link_list_to_dict": indicator_link_list_to_dict,
    "update_indicators": update_indicators,
    "split_scale_in_list": split_scale_in_list,
    "convert_indicator_ids_to_int": convert_indicator_ids_to_int,
    "clean_whitespace": clean_whitespace,
    "update_objectives": update_objectives,
    "update_actions_into_objectives": update_actions_into_objectives
}

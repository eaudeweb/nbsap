from functools import wraps

import flask
import flatland.out.markup

def get_indicator_editable_fields():
    keys = ["status", "classification", "sources", "question", "measurer",
            "sub_indicator", "head_indicator", "requirements", "name"]

    return keys

def get_session_language():
    if flask.session.get('language'):
        return flask.session['language'][0]
    else:
        return flask.request.accept_languages.best_match(['en', 'fr', 'nl'])

def translate(field):
    language = get_session_language()
    if field[language] == '':
        return field['en']
    else:
        return field[language]

def subobjs_dfs(smask, amask, objective, result_list):
    s_list = objective['subobjs']
    s_sorted_list = sorted(s_list, key=lambda k: k['id'])

    for s in s_sorted_list:
        subobjective = {}
        subobjective['key'] = ".".join([smask, str(s['id'])])
        subobjective['value'] = s
        subobjective['actions'] = []

        for act in s['actions']:
            act = {}
            act['key'] = ".".join([(".".join([amask, str(s['id'])])),
                                str(a['id'])])
            act['value'] = a
            subobjective['actions'].append(act)

        result_list.append(subobjective)

    for s in s_sorted_list:
        new_smask = ".".join([smask, str(s['id'])])
        new_amask = ".".join([amask, str(s['id'])])
        subobjs_dfs(new_mask, s, result_list)

def get_subobjs_by_dfs(o_id):
    from nbsap import mongo
    objective = mongo.db.objectives.find_one_or_404({'id': o_id})

    subobj_list = []
    smask = "s%s" % (str(objective['id']))
    amask = "a%s" % (str(objective['id']))

    subobjs_dfs(smask, amask, objective, subobj_list)
    return subobj_list

def actions_dfs(mask, objective, result_list):
    for a in objective['actions']:
        action = {}
        action['key'] = ".".join([mask, str(a['id'])])
        action['value'] = a
        result_list.append(action)

    subobj_list = objective['subobjs']
    subobj_sorted_list = sorted(subobj_list, key=lambda k: k['id'])

    for s in subobj_sorted_list:
        new_mask = ".".join([mask, str(s['id'])])
        actions_dfs(new_mask, s, result_list)

def get_actions_by_dfs(o_id):
    from nbsap.database import mongo
    objective = mongo.db.objectives.find_one_or_404({'id': o_id})

    action_list = []
    mask = str(objective['id'])

    actions_dfs(mask, objective, action_list)
    return action_list

def mydfs(mask, index, objective, subobjective):
    objective[index].append(mask + '.' + str(subobjective['id']))
    for s in subobjective['subobjs']:
        new_mask = mask + '.' + str(subobjective['id'])
        mydfs(new_mask, index, objective, s)


def generate_objectives():
    from nbsap.database import mongo
    objectives = {i['id']:"" for i in mongo.db.objectives.find()}

    for id in objectives.keys():
        objectives[id] = []

        for subobj in mongo.db.objectives.find_one({'id': id})['subobjs']:
            mask = str(id)
            mydfs(mask, id, objectives, subobj)

    return objectives

def templated(template=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            template_name = template
            ctx = f(*args, **kwargs)
            if ctx is None:
                ctx = {}
            elif not isinstance(ctx, dict):
                return ctx
            if template_name is None: template_name = ctx.pop("template")
            return flask.render_template(template_name, **ctx)
        decorated_function.not_templated = f
        return decorated_function
    return decorator

class MarkupGenerator(flatland.out.markup.Generator):

    def __init__(self, template):
        super(MarkupGenerator, self).__init__("html")
        self.template = template

    def children_order(self, field):
        if isinstance(field, flatland.Mapping):
            return [kid.name for kid in field.field_schema]
        else:
            return []

    def widget(self, element, widget_name=None):
        if widget_name is None:
            widget_name = element.properties.get("widget", "input")
        session = flask.session
        widget_macro = getattr(self.template.make_module({'session': session}), widget_name)
        return widget_macro(self, element)

    def properties(self, field, id=None):
        properties = {}

        if id:
            properties["id"] = id
        if field.properties.get("css_class", None):
            properties["class"] = field.properties["css_class"]
        if not field.optional:
            properties["required"] = ""
            if "not_empty_error" in field.properties:
                properties["title"] = field.properties["not_empty_error"]
        if field.properties.get("attr", None):
            properties.update(field.properties["attr"])
        return properties


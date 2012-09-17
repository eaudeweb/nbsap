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

def generate_objectives():
    from nbsap.database import mongo
    objectives = {i['id']:"" for i in mongo.db.objectives.find()}
    for id in objectives.keys():
        objectives[id] = {i['id']:"%s.%s" % (id, i['id'])
                            for i in mongo.db.objectives.find_one({"id": id})['subobjs']}
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
        language = get_session_language()
        widget_macro = getattr(self.template.make_module({'lang': language}), widget_name)
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


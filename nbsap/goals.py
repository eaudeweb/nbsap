import flask
from flaskext.babel import gettext as _

import sugar
import schema
from database import mongo
from auth import auth_required

goals = flask.Blueprint("goals", __name__)


def initialize_app(app):
    _my_extensions = (app.jinja_options["extensions"] + ["jinja2.ext.do"] +
                      ["jinja2.ext.loopcontrols"] + ["jinja2.ext.i18n"])
    app.jinja_options = dict(app.jinja_options, extensions=_my_extensions)
    app.register_blueprint(goals)


@goals.route("/admin")
@auth_required
def admin():
    return flask.redirect(flask.url_for('goals.list_goals'))


@goals.route("/set_language", methods=['POST', 'GET'])
def set_language():
    language = flask.request.args.getlist('language')
    flask.session['language'] = language
    return flask.redirect(flask.request.referrer)


@goals.route("/")
@goals.route("/goals")
@goals.route("/goals/<string:goal_short_title>")
@sugar.templated("homepage.html")
def homepage_goals(goal_short_title='A'):
    goals_list = mongo.db.goals.find()
    aichi_goal = mongo.db.goals.find_one_or_404({'short_title':
                                                 goal_short_title})
    aichi_targets = [t for t in mongo.db.targets.find({'goal_id':
                                                      goal_short_title})]

    for target in aichi_targets:
        target['relevant_indicators'] = []
        target['other_indicators'] = []
        target['objective_ids'] = []
        relevant_indicators = mongo.db.indicators.find({"relevant_target":
                                                        target['id']})
        other_indicators = mongo.db.indicators.find({'other_targets':
                                                    {"$in": [target['id']]}})
        mapping = mongo.db.mapping.find({"$or": [{"main_target": target['id']},
                                                 {'other_targets':
                                                  {"$in": [target['id']]}}]})

        for indicator in relevant_indicators:
            target['relevant_indicators'].append({'id': indicator['id'],
                                                  'name': indicator['name']})
        for indicator in other_indicators:
            target['other_indicators'].append({'id': indicator['id'],
                                               'name': indicator['name']})
        for _map in mapping:
            target['objective_ids'].append(_map['objective'].split('.'))

    return {
        "goals_list": goals_list,
        "goal": aichi_goal,
        "targets": aichi_targets
    }


@goals.route("/admin/goals")
@auth_required
@sugar.templated("/goals/goals_listing.html")
def list_goals():
    aichi_goals = [i for i in mongo.db.goals.find()]

    return {
        "goals": aichi_goals,
    }


@goals.route("/default_mapping")
@sugar.templated("mapping/default_mapping.html")
def default_mapping_routing():
    return {}


@goals.route("/admin/mapping")
@sugar.templated('mapping/listing.html')
def mapping():
    mappings = [mapping for mapping in mongo.db.mapping.find()]
    goals = [goal for goal in mongo.db.goals.find()]

    for mapping in mappings:
        mapping['objective'] = mapping['objective'].split('.')
        goal_id = [goal['id'] for goal in goals
                   if goal['short_title'] == mapping['goal']][0]
        mapping['goal'] = {'id': goal_id, 'name': mapping['goal']}

    return {
        "mappings": mappings,
        "eu_actions_urls": schema.common.get_urls_for_actions(),
    }


@goals.route("/admin/mapping/<string:mapping_id>/delete", methods=["DELETE"])
def mapping_delete(mapping_id):
    import bson
    from pymongo.errors import OperationFailure

    objectid = bson.objectid.ObjectId(oid=mapping_id)
    try:
        mongo.db.mapping.remove(spec_or_id=objectid)
        flask.flash(_("Mapping deleted"), "success")
    except OperationFailure:
        flask.flash(_("Errors encountered while deleting mapping"), "errors")

    return flask.jsonify({'status': 'success'})


@goals.route("/admin/mapping/new", methods=["GET", "POST"])
@goals.route("/admin/mapping/<string:mapping_id>/edit",
             methods=["GET", "POST"])
@sugar.templated('mapping/edit.html')
def mapping_edit(mapping_id=None):
    # check if valid objectives exist
    objs = mongo.db.objectives.find()
    valid_mapping = [True for obj in objs if obj['subobjs']]
    if not valid_mapping:
        return flask.redirect(flask.url_for('goals.default_mapping_routing'))

    import bson
    app = flask.current_app
    objectives = sugar.generate_objectives()

    if mapping_id:
        objectid = bson.objectid.ObjectId(oid=mapping_id)
        mapping = mongo.db.mapping.find_one_or_404({'_id': objectid})

        ms = schema.MappingSchema(mapping)
        ms.set_objectives(objectives)
        ms['objective'].set(mapping['objective'])
        ms['main_target'].valid_values = map(str,
                                             ms['main_target'].valid_values)
        ms['main_target'].set(mapping['main_target'])
    else:
        ms = schema.MappingSchema({})
        ms.set_objectives(objectives)

    if flask.request.method == "POST":
        initial_form = flask.request.form
        form_data = initial_form.to_dict()
        targets_list = initial_form.getlist('other_targets')
        eu_actions_list = initial_form.getlist('eu_actions')
        eu_targets_list = initial_form.getlist('eu_targets')
        try:
            targets_list.remove(form_data['main_target'])
        except ValueError:
            pass
        if mapping_id:
            ms['goal'].set(form_data['goal'])
        else:
            ms = schema.MappingSchema.from_flat(form_data)
            ms.set_objectives(objectives)

        ms['objective'].set(form_data['objective'])
        ms['other_targets'].set(targets_list)
        ms['eu_actions'].set(eu_actions_list)
        ms['eu_targets'].set(eu_targets_list)
        ms['main_target'].valid_values = map(str,
                                             ms['main_target'].valid_values)
        ms['main_target'].set(form_data['main_target'])

        if ms.validate():
            if mapping_id:
                mapping.update(ms.flatten())
                mapping['_id'] = bson.objectid.ObjectId(oid=mapping_id)
            else:
                mapping = ms.flatten()
                mapping['_id'] = bson.objectid.ObjectId()
            mongo.db.mapping.save(mapping)
            flask.flash(_("Mapping saved"), "success")
            return flask.redirect(flask.url_for('goals.mapping'))

        else:
            flask.flash(_("Errors in mapping information"), "error")

    return {
        "mk": sugar.MarkupGenerator(app.jinja_env.get_template
                                    ("widgets/widgets_edit_data.html")),
        "mapping_schema": ms,
        "mapping_id": mapping_id
    }


@goals.route("/goals/data")
def goal_data():
    try:
        goal_short_title = flask.request.args.getlist('goal_short_title')[0]
    except IndexError:
        return flask.jsonify({'result': ''})

    aichi_goal = mongo.db.goals.find_one_or_404({"short_title":
                                                 goal_short_title})
    result = {'result': sugar.translate(aichi_goal['description'])}

    return flask.jsonify(result)


@goals.route("/admin/goals/<string:goal_id>/edit", methods=["GET", "POST"])
@auth_required
@sugar.templated("goals/edit.html")
def edit(goal_id):
    goal = mongo.db.goals.find_one_or_404({'id': goal_id})
    goal_schema = schema.Goal(goal)

    # default display language is English
    try:
        lang = flask.request.args.getlist('lang')[0]
    except IndexError:
        lang = u'en'

    if flask.request.method == "POST":
        data = flask.request.form.to_dict()
        lang = data['language']
        goal_schema['title'][lang].set(data['title-' + lang])
        goal_schema['description'][lang].set(data['body-' + lang])

        if goal_schema.validate():
            goal['title'][lang] = data['title-' + lang]
            goal['description'][lang] = data['body-' + lang]
            flask.flash(_("Saved changes."), "success")
            mongo.db.goals.save(goal)

    return {
        "language": lang,
        "goal": goal,
        "schema": goal_schema
    }

import flask
import sugar
import schema
from database import mongo
from auth import auth_required

goals = flask.Blueprint("goals", __name__)


def initialize_app(app):
    _my_extensions = app.jinja_options["extensions"] + ["jinja2.ext.do"]
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
    aichi_goal = mongo.db.goals.find_one_or_404({'short_title': goal_short_title})
    aichi_targets = [t for t in mongo.db.targets.find({'goal_id': goal_short_title})]

    for target in aichi_targets:
        target['relevant_indicators'] = []
        target['other_indicators'] = []
        target['objective_ids'] = []

        relevant_indicators = mongo.db.indicators.find({"relevant_target": target['id']})
        other_indicators = mongo.db.indicators.find({'other_targets': {"$in": [target['id']]}})
        mapping = mongo.db.mapping.find({"$or": [{"main_target": target['id']},
                                                   {'other_targets': {"$in": [target['id']]}}]
                                       })

        for indicator in relevant_indicators:
            target['relevant_indicators'].append({'id': indicator['id'],
                                                  'name': indicator['name']
                                                 })

        for indicator in other_indicators:
            target['other_indicators'].append({'id': indicator['id'],
                                               'name': indicator['name']
                                              })

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
            "mappings": mappings
           }


@goals.route("/admin/mapping/<string:mapping_id>/delete", methods=["DELETE"])
def mapping_delete(mapping_id):
    import bson
    from pymongo.errors import OperationFailure

    objectid = bson.objectid.ObjectId(oid=mapping_id)

    try:
        mongo.db.mapping.remove(spec_or_id=objectid)
        flask.flash("Mapping deleted", "success")
    except OperationFailure:
        flask.flash("Errors encountered while deleting mapping", "errors")

    return flask.jsonify({'status': 'success'})


@goals.route("/admin/mapping/new", methods=["GET", "POST"])
@goals.route("/admin/mapping/<string:mapping_id>/edit", methods=["GET", "POST"])
@sugar.templated('mapping/edit.html')
def mapping_edit(mapping_id=None):
    import bson
    app = flask.current_app
    objectives = sugar.generate_objectives()

    if mapping_id:
        objectid = bson.objectid.ObjectId(oid=mapping_id)
        mapping = mongo.db.mapping.find_one_or_404({'_id': objectid})

        mapping_schema = schema.MappingSchema(mapping)
        mapping_schema.set_objectives(objectives)

        mapping_schema['objective'].set(mapping['objective'])
        mapping_schema['main_target'].valid_values = map(str, mapping_schema['main_target'].valid_values)
        mapping_schema['main_target'].set(mapping['main_target'])

    else:
        mapping_schema = schema.MappingSchema({})
        mapping_schema.set_objectives(objectives)

    if flask.request.method == "POST":
        initial_form = flask.request.form
        form_data = initial_form.to_dict()
        targets_list = initial_form.getlist('other_targets')

        try:
            targets_list.remove(form_data['main_target'])
        except ValueError:
            pass

        if mapping_id:
            mapping_schema['goal'].set(form_data['goal'])
        else:
            mapping_schema = schema.MappingSchema(form_data)
            mapping_schema.set_objectives(objectives)

        mapping_schema['objective'].set(form_data['objective'])
        mapping_schema['other_targets'].set(targets_list)
        mapping_schema['main_target'].valid_values = map(str, mapping_schema['main_target'].valid_values)
        mapping_schema['main_target'].set(form_data['main_target'])

        if mapping_schema.validate():

            if mapping_id:
                mapping.update(mapping_schema.flatten())
                mapping['_id'] = bson.objectid.ObjectId(oid=mapping_id)
            else:
                mapping = mapping_schema.flatten()
                mapping['_id'] = bson.objectid.ObjectId()

            mongo.db.mapping.save(mapping)
            flask.flash("Mapping saved", "success")
            return flask.redirect(flask.url_for('goals.mapping'))

        else:
            flask.flash("Errors in mapping information", "error")

    return {
                 "mk": sugar.MarkupGenerator(
                    app.jinja_env.get_template("widgets/widgets_edit_data.html")
                  ),
                 "mapping_schema": mapping_schema,
                 "mapping_id": mapping_id
            }

@goals.route("/goals/data")
def goal_data():
    try:
        goal_short_title = flask.request.args.getlist('goal_short_title')[0]
    except IndexError:
        return flask.jsonify({'result': ''})

    aichi_goal = mongo.db.goals.find_one_or_404({"short_title": goal_short_title})

    result = {'result': aichi_goal['description']['en']}
    return flask.jsonify(result)

@goals.route("/admin/goals/<string:goal_id>/edit", methods=["GET", "POST"])
@auth_required
@sugar.templated("goals/edit.html")
def edit(goal_id):

    goal = mongo.db.goals.find_one_or_404({'id': goal_id})
    goal_schema = schema.Goal(goal)

    # default display language is English
    try:
        selected_language = flask.request.args.getlist('lang')[0]
    except IndexError:
        selected_language = u'en'

    if flask.request.method == "POST":
        data = flask.request.form.to_dict()

        selected_language = data['language']

        goal_schema['title'][selected_language].set(data['title-' + selected_language])
        goal_schema['description'][selected_language].set(data['body-' + selected_language])

        if goal_schema.validate():
            goal['title'][selected_language] = data['title-' + selected_language]
            goal['description'][selected_language] = data['body-' + selected_language]

            flask.flash("Saved changes.", "success")
            mongo.db.goals.save(goal)

    return {
                "language": selected_language,
                "goal": goal,
                "schema": goal_schema
           }

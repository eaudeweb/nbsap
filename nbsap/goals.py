import flask
import sugar
import schema
from database import mongo

goals = flask.Blueprint("goals", __name__)

def initialize_app(app):
    _my_extensions = app.jinja_options["extensions"] + ["jinja2.ext.do"]
    app.jinja_options = dict(app.jinja_options, extensions=_my_extensions)
    app.register_blueprint(goals)

@goals.route("/")
@sugar.templated('homepage.html')
def home():
    return

@goals.route("/homepage_goals")
@goals.route("/homepage_goals/<string:goal_short_title>")
@sugar.templated("aichi_view.html")
def homepage_goals(goal_short_title='A'):

    goals_list = mongo.db.goals.find()
    aichi_goal = mongo.db.goals.find_one_or_404({'short_title': goal_short_title})
    aichi_targets = [t for t in mongo.db.targets.find({'goal_id': goal_short_title})]

    for target in aichi_targets:
        target['indicator_ids'] = []
        target['objective_ids'] = []

        indicators = mongo.db.indicators.find({ "$or" : [{"relevant_target": target['id']},
                                                         {'other_targets': {"$in": [target['id']]}}
                                                        ]
                                              })
        mapping = mongo.db.mapping.find({ "$or" : [{"main_target": target['id']},
                                                   {'other_targets': {"$in": [target['id']]}}
                                                  ]
                                         })

        for indicator in indicators:
            target['indicator_ids'].append(indicator['id'])

        for _map in mapping:
            target['objective_ids'].append(_map['objective'].split('.'))

    return {
            "goals_list": goals_list,
            "goal": aichi_goal,
            "targets": aichi_targets
           }


@goals.route("/goals")
@sugar.templated("/goals/goals_listing.html")
def list_goals():

    aichi_goals = [i for i in mongo.db.goals.find()]

    return {
            "goals": aichi_goals,
           }

@goals.route("/mapping", methods=["GET", "POST"])
@sugar.templated('mapping.html')
def mapping():
    app = flask.current_app

    if flask.request.method == "POST":
        initial_form = flask.request.form
        form_data = initial_form.to_dict()
        targets_list = initial_form.getlist('other_targets')

        try:
            targets_list.remove(form_data['main_target'])
        except ValueError:
            pass

        mapping_schema = schema.MappingSchema(form_data)

        objectives = sugar.generate_objectives()
        mapping_schema.set_objectives(objectives)
        mapping_schema['objective'].set(form_data['objective'])
        mapping_schema['other_targets'].set(targets_list)

        mapping_schema['main_target'].valid_values = map(str, mapping_schema['main_target'].valid_values)
        mapping_schema['main_target'].set(form_data['main_target'])

        if mapping_schema.validate():
            mongo.db.mapping.save(mapping_schema.flatten())
            flask.flash("Mapping saved", "success")

    else:
        mapping_schema = schema.MappingSchema({})
        objectives = sugar.generate_objectives()
        mapping_schema.set_objectives(objectives)

    return {
                 "mk": sugar.MarkupGenerator(
                    app.jinja_env.get_template("widgets/widgets_edit_data.html")
                  ),
                 "mapping_schema": mapping_schema,
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

@goals.route("/goals/<string:goal_id>/edit", methods=["GET", "POST"])
@sugar.templated("goals/edit.html")
def edit(goal_id):

    goal = mongo.db.goals.find_one_or_404({'id': goal_id})
    goal_schema = schema.Goal(goal)

    # default display language is English
    try:
        selected_language = flask.request.args.getlist('lang')[0]
    except IndexError:
        selected_language = u'en'

    app = flask.current_app

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

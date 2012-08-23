import flask
import sugar
import schema
from database import mongo

goals = flask.Blueprint("goals", __name__)

def initialize_app(app):
    app.register_blueprint(goals)

@goals.route("/")
@sugar.templated('homepage.html')
def home():
    return

@goals.route("/goals")
@sugar.templated("goals_listing.html")
def list_goals():

    aichi_goals = [i for i in mongo.db.goals.find()]
    aichi_targets = mongo.db.targets.find()
    target_dict = {aichi_goals[i]['short_title']:[] for i in range(len(aichi_goals))}

    for target in aichi_targets:
        target_dict[target['goal_id']].append(target)

    return {
            "goals": aichi_goals,
            "target_dict": target_dict
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


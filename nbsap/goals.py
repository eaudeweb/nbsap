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
    mapping_schema = schema.MappingSchema({})

    if flask.request.method == "POST":
        initial_form = flask.request.form
        form_data = initial_form.to_dict()
        mapping_schema = schema.MappingSchema(form_data)
        mapping_schema['other_targets'].set(initial_form.getlist('other_targets'))
        mapping_schema['main_target'].value = mapping_schema['main_target'].u

        if mapping_schema.validate():
            print mapping_schema['objective']
            print mapping_schema.value
            #mongo.db.objectives.save(form_data)

    objectives = sugar.generate_objectives()
    mapping_schema.set_objectives(objectives)

    return {
                 "mk": sugar.MarkupGenerator(
                    app.jinja_env.get_template("widgets/widgets_edit_data.html")
                  ),
                 "mapping_schema": mapping_schema,
            }

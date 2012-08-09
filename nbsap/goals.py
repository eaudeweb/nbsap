import flask
import sugar

from schema.refdata import _load_json

goals = flask.Blueprint("goals", __name__)

def initialize_app(app):
    app.register_blueprint(goals)

@goals.route('/')
@sugar.templated('homepage.html')
def home():
    return

@goals.route('/goals')
@sugar.templated("goals_listing.html")
def list_goals():
    aichi_goals = _load_json("../refdata/aichi_goals.json")
    aichi_targets = _load_json("../refdata/aichi_targets.json")

    target_dict = {aichi_goals[i]['short_title']:[] for i in range(len(aichi_goals))}

    for target in aichi_targets:
        target_dict[target['goal_id']].append(target)

    return {
            "goals": aichi_goals,
            "target_dict": target_dict
           }


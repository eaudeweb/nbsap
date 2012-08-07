import flask
import sugar

from flaskext.babel import gettext
from schema.refdata import _load_json

goals = flask.Blueprint("goals", __name__)

def initialize_app(app):
    app.register_blueprint(goals)

@goals.route('/')
@goals.route('/goals')
@sugar.templated("goals_listing.html")
def home():
    app = flask.current_app
    babel = app.extensions['babel']
    babel.locale_selector_func = lambda: flask.request.args.get('lang', 'en')

    aichi_goals = _load_json("../refdata/aichi_goals.json")
    aichi_targets = _load_json("../refdata/aichi_targets.json")

    target_dict = {aichi_goals[i]['short_title']:[] for i in range(len(aichi_goals))}

    for target in aichi_targets:
        target_dict[target['goal_id']].append(target)

    return {
            "goals": aichi_goals,
            "target_dict": target_dict
           }

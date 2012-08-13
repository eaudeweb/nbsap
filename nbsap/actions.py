import flask
import sugar

from schema.refdata import _load_json

actions = flask.Blueprint("actions", __name__)

def initialize_app(app):
    app.register_blueprint(actions)

@actions.route("/objective/<int:objective_id>/<int:subobj_id>/action")
@sugar.templated("actions/view.html")
def view(objective_id, subobj_id):
    actions = _load_json("../refdata/be_actions.json")
    related_actions = [a['actions'] for a in actions if a['id'] == objective_id][0]
    action = [a for a in related_actions if a['id'] == subobj_id][0]

    return {
                "objective_id": objective_id,
                "subobj_id": subobj_id,
                "action": action
           }


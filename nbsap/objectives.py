import flask
import sugar

from schema.refdata import _load_json

objectives = flask.Blueprint("objectives", __name__)

def initialize_app(app):
    app.register_blueprint(objectives)

@objectives.route("/objective/<int:objective_id>/<int:subobj_id>")
@sugar.templated("objectives/subobj_view.html")
def view_subobj(objective_id, subobj_id):
    objectives = _load_json("../refdata/be_objectives.json")
    objective = [o for o in objectives if o['id'] == objective_id][0]

    subobj = [s for s in objective['subobjs'] if s['id'] == subobj_id][0]

    actions = _load_json("../refdata/be_actions.json")
    objective_related_actions = [a for a in actions if a['id'] == objective_id][0]
    related_action = [a for a in objective_related_actions['actions']
                                if int(a['title']['en'].split('.')[1]) == subobj_id][0]

    return {
                "objective_id": objective_id,
                "subobj": subobj,
                "action": related_action
           }

@objectives.route("/objective/<int:objective_id>")
@sugar.templated("objectives/view.html")
def view(objective_id):
    objectives = _load_json("../refdata/be_objectives.json")
    objective = [o for o in objectives if o['id'] == objective_id][0]

    actions = _load_json("../refdata/be_actions.json")
    related_actions = [a['actions'] for a in actions if a['id'] == objective_id][0]

    return {
                "objective": objective,
                "actions": related_actions
           }

@objectives.route("/objectives")
@sugar.templated("objectives/objectives_listing.html")
def list_objectives():
    objectives = _load_json("../refdata/be_objectives.json")

    return {
            "objectives": objectives,
           }


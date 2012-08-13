import flask
import sugar

objectives = flask.Blueprint("objectives", __name__)

def initialize_app(app):
    app.register_blueprint(objectives)

@objectives.route("/objective/<int:objective_id>/<int:subobj_id>")
@sugar.templated("objectives/subobj_view.html")
def view_subobj(objective_id, subobj_id):
    from app import mongo

    objective = mongo.db.objectives.find_one_or_404({"id": objective_id})

    try:
        subobj = [s for s in objective['subobjs'] if s['id'] == subobj_id][0]
    except IndexError:
        flask.abort(404)

    objective_related_actions = mongo.db.actions.find_one({"id": objective_id})

    if objective_related_actions:
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
    from app import mongo

    objective = mongo.db.objectives.find_one_or_404({'id': objective_id})
    actions = mongo.db.actions.find_one({'id': objective_id})

    if actions:
        related_actions = actions.get('actions', None)

    return {
                "objective": objective,
                "actions": related_actions
           }

@objectives.route("/objectives")
@sugar.templated("objectives/objectives_listing.html")
def list_objectives():
    from app import mongo

    objectives = mongo.db.objectives.find()

    return {
            "objectives": objectives,
           }


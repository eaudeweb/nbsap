import flask
import sugar

actions = flask.Blueprint("actions", __name__)

def initialize_app(app):
    app.register_blueprint(actions)

@actions.route("/objective/<int:objective_id>/<int:subobj_id>/action")
@sugar.templated("actions/view.html")
def view(objective_id, subobj_id):
    from app import mongo

    related_actions = mongo.db.actions.find_one_or_404({"id": objective_id})['actions']

    try:
        action = [a for a in related_actions if a['id'] == subobj_id][0]
    except IndexError:
        flask.abort(404)

    return {
                "objective_id": objective_id,
                "subobj_id": subobj_id,
                "action": action
           }


import schema
import flask
import sugar
from database import mongo
from auth import auth_required

actions = flask.Blueprint("actions", __name__)

def initialize_app(app):
    app.register_blueprint(actions)

@actions.route("/admin/objectives/<int:objective_id>/<int:subobj_id>/action")
@auth_required
@sugar.templated("actions/view.html")
def view(objective_id, subobj_id):

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

@actions.route("/admin/objectives/<int:objective_id>/<int:subobj_id>/action/edit", methods=["GET", "POST"])
@auth_required
@sugar.templated("actions/edit.html")
def edit(objective_id, subobj_id):

    # sub-objectives are 0-indexed
    subobj_id -= 1

    action = mongo.db.actions.find_one_or_404({'id': objective_id})

    # actions list by default sorted like (1, 10).
    tmp_list = action['actions']
    tmp_list = sorted(tmp_list, key=lambda k: k['id'])
    action['actions'] = tmp_list

    action_schema = schema.Action(action)

    # default display language is English
    try:
        selected_language = flask.request.args.getlist('lang')[0]
    except IndexError:
        selected_language = u'en'

    if flask.request.method == "POST":
        data = flask.request.form.to_dict()

        selected_language = data['language']

        action_schema['actions'][subobj_id]['body'][selected_language].set(data['body-' + selected_language])

        if action_schema.validate():

            action['actions'][subobj_id]['body'][selected_language] = data['body-' + selected_language]

            flask.flash("Saved changes.", "success")
            mongo.db.actions.save(action)

    return {
                "language": selected_language,
                "action": action,
                "schema": action_schema,
                "objective_id": objective_id,
                "subobj_id": subobj_id
    }

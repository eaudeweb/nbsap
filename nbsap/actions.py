import schema
import flask
import sugar
from database import mongo
from auth import auth_required

actions = flask.Blueprint("actions", __name__)

def initialize_app(app):
    app.register_blueprint(actions)

@actions.route("/admin/objectives/<int:objective_id>/"
                  "action/<int:action_id>")
@actions.route("/admin/objectives/<int:objective_id>/"
                  "<int:so1_id>/action/<int:action_id>")
@actions.route("/admin/objectives/<int:objective_id>/"
                  "<int:so1_id>/<int:so2_id>/action/<int:action_id>")
@actions.route("/admin/objectives/<int:objective_id>/"
                  "<int:so1_id>/<int:so2_id>/<int:so3_id>"
                  "/action/<int:action_id>")
@actions.route("/admin/objectives/<int:objective_id>/"
                  "<int:so1_id>/<int:so2_id>/<int:so3_id>/"
                  "<int:so4_id>/action/<int:action_id>")
@auth_required
@sugar.templated("actions/view.html")
def view(objective_id, action_id,
    so1_id=None, so2_id = None, so3_id = None, so4_id = None):

    myargs = ['objective_id', 'so1_id', 'so2_id', 'so3_id', 'so4_id']
    parents = [(i, locals()[i]) for i in myargs if locals()[i] != None]

    objective = mongo.db.objectives.find_one_or_404({'id': objective_id})

    father = objective
    for i in range(1, len(parents)):
        son_id = parents[i][1]
        try:
            son = [s for s in father['subobjs'] if s['id'] == son_id][0]
        except IndexError:
            flask.abort(404)
        father = son

    matrix = []
    for i, x in enumerate(parents):
        tmp_L = [y for j, y in enumerate(parents) if j < i]
        tmp_L.append(x)

        matrix.append((dict(tmp_L), x[1]))

    # find specified action
    try:
        related_action = [a for a in father['actions']
                            if a['id'] == action_id][0]
    except IndexError:
        flask.abort(404)

    action_parents = { 'action_id': action_id}
    action_parents.update(dict(parents))

    return {
                "action": related_action,
                "action_parents": action_parents,
                "chain_matrix": matrix,
           }

@actions.route("/admin/objectives/<int:objective_id>/"
                  "action/<int:action_id>/edit", methods=["GET", "POST"])
@actions.route("/admin/objectives/<int:objective_id>/"
                  "<int:so1_id>/action/<int:action_id>/edit", methods=["GET", "POST"])
@actions.route("/admin/objectives/<int:objective_id>/"
                  "<int:so1_id>/<int:so2_id>/action/"
                  "<int:action_id>/edit", methods=["GET", "POST"])
@actions.route("/admin/objectives/<int:objective_id>/"
                  "<int:so1_id>/<int:so2_id>/<int:so3_id>"
                  "/action/<int:action_id>/edit", methods=["GET", "POST"])
@actions.route("/admin/objectives/<int:objective_id>/"
                  "<int:so1_id>/<int:so2_id>/<int:so3_id>/"
                  "<int:so4_id>/action/<int:action_id>"
                  "/edit", methods=["GET", "POST"])
@auth_required
@sugar.templated("actions/edit.html")
def edit(objective_id, action_id,
    so1_id=None, so2_id = None, so3_id = None, so4_id = None):

    myargs = ['objective_id', 'so1_id', 'so2_id', 'so3_id', 'so4_id']
    parents = [(i, locals()[i]) for i in myargs if locals()[i] != None]

    objective = mongo.db.objectives.find_one_or_404({'id': objective_id})

    father = objective
    for i in range(1, len(parents)):
        son_id = parents[i][1]
        try:
            son = [s for s in father['subobjs'] if s['id'] == son_id][0]
        except IndexError:
            flask.abort(404)
        father = son

    matrix = []
    for i, x in enumerate(parents):
        tmp_L = [y for j, y in enumerate(parents) if j < i]
        tmp_L.append(x)

        matrix.append((dict(tmp_L), x[1]))

    # find specified action
    try:
        related_action = [a for a in father['actions']
                            if a['id'] == action_id][0]
    except IndexError:
        flask.abort(404)

    action_parents = { 'action_id': action_id }
    action_parents.update(dict(parents))

    action_schema = schema.Action(related_action)

    # default display language is English
    try:
        selected_language = flask.request.args.getlist('lang')[0]
    except IndexError:
        selected_language = u'en'

    if flask.request.method == "POST":
        data = flask.request.form.to_dict()
        selected_language = data['language']

        action_schema['title'][selected_language].set(data['title-' + selected_language])
        action_schema['body'][selected_language].set(data['body-' + selected_language])

        if action_schema.validate():
            action_index = None
            for idx, item in enumerate(father['actions']):
                if item['id'] == action_id:
                    action_index = idx
                    break

            father['actions'][action_index]['title'][selected_language] = data['title-' + selected_language]
            father['actions'][action_index]['body'][selected_language] = data['body-' + selected_language]

            flask.flash("Saved changes.", "success")
            mongo.db.objectives.save(objective)

    return {
                "language": selected_language,
                "action": related_action,
                "chain_matrix": matrix,
                "schema": action_schema,
                "action_parents": action_parents,
    }

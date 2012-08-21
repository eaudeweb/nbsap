import flask
import sugar
from database import mongo

objectives = flask.Blueprint("objectives", __name__)

def initialize_app(app):
    app.register_blueprint(objectives)

@objectives.route("/objectives/<int:objective_id>/<int:subobj_id>")
@sugar.templated("objectives/subobj_view.html")
def view_subobj(objective_id, subobj_id):

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

@objectives.route("/objectives/<int:objective_id>")
@sugar.templated("objectives/view.html")
def view(objective_id):

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

    objectives = mongo.db.objectives.find()

    return {
            "objectives": objectives,
           }

@objectives.route("/objectives/data")
def objective_data():
    id_code = flask.request.args.getlist('id_code')[0]
    objective_id = int(id_code.split('.')[0])
    subobjective_id = int(id_code.split('.')[1])

    objective = mongo.db.objectives.find_one_or_404({"id": objective_id})
    subobjective = [s for s in objective['subobjs'] if s['id'] == subobjective_id][0]

    return flask.jsonify(subobjective)

@objectives.route("/objective/<int:objective_id>/edit", methods=["GET", "POST"])
@sugar.templated("objectives/edit.html")
def edit(objective_id):

    objective = mongo.db.objectives.find_one_or_404({'id': objective_id})

    from schema import GenericEditSchema
    app = flask.current_app

    if flask.request.method == "POST":
        data = flask.request.form.to_dict()
        schema = GenericEditSchema(data)

        if schema.validate():

            objective['title']['en'] = schema['title'].value
            objective['body']['en'] = schema['body'].value
            mongo.db.objectives.save(objective)

    else:
        schema = GenericEditSchema({})
        schema['title'].set(objective['title']['en'])
        schema['body'].set(objective['body']['en'])

    return {
                 "mk": sugar.MarkupGenerator(
                    app.jinja_env.get_template("widgets/widgets_edit_data.html")
                  ),
                "objective": objective,
                "schema": schema
           }

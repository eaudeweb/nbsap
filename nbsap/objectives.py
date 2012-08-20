import schema
import flask
import sugar
from database import mongo

objectives = flask.Blueprint("objectives", __name__)

def initialize_app(app):
    app.register_blueprint(objectives)

@objectives.route("/objective/<int:objective_id>/<int:subobj_id>")
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

@objectives.route("/objective/<int:objective_id>")
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

@objectives.route("/objective/<int:objective_id>/edit", methods=["GET", "POST"])
@sugar.templated("objectives/edit.html")
def edit(objective_id):

    objective = mongo.db.objectives.find_one_or_404({'id': objective_id})

    app = flask.current_app

    if flask.request.method == "POST":
        data = flask.request.form.to_dict()

        for lang in ['en', 'fr', 'nl']:
            data['objective_body_' + lang] = data[lang]
            del data[lang]

        edit_schema = schema.GenericEditSchema.from_flat(data)

        if edit_schema.validate():
            selected_language = edit_schema['language'].value

            objective['title'][selected_language] = \
                        edit_schema['objective']['title'][selected_language].value

            objective['body'][selected_language] = \
                        edit_schema['objective']['body'][selected_language].value

            flask.flash("Information saved", "success")
            mongo.db.objectives.save(objective)

    edit_schema = schema.GenericEditSchema({})
    edit_schema['objective'] = schema.Objective(objective)

    return {
                 "mk": sugar.MarkupGenerator(
                    app.jinja_env.get_template("widgets/widgets_edit_data.html")
                  ),
                "objective": objective,
                "schema": edit_schema
           }

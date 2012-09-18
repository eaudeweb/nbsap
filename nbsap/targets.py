import flask
import schema
import sugar
from database import mongo
from auth import auth_required

targets = flask.Blueprint("targets", __name__)

def initialize_app(app):
    app.register_blueprint(targets)

@targets.route("/admin/targets")
@auth_required
@sugar.templated("targets/targets_listing.html")
def list_targets():

    aichi_targets = mongo.db.targets.find()

    return {
            "targets": aichi_targets
           }

@targets.route("/targets/data")
def target_data():
    target_ids = flask.request.args.getlist('other_targets', None)
    aichi_targets = []
    lang = sugar.get_session_language()

    for target_id in target_ids:
       aichi_target = mongo.db.targets.find_one_or_404({"id": target_id})
       data = { 'title': aichi_target['title'][lang],
                'description': aichi_target['description'][lang]
              }
       aichi_targets.append(data)

    result = {'result': aichi_targets}
    return flask.jsonify(result)

@targets.route("/admin/targets/<string:target_id>/edit", methods=["GET", "POST"])
@auth_required
@sugar.templated("targets/edit.html")
def edit(target_id):

    target = mongo.db.targets.find_one_or_404({'id': target_id})
    target_schema = schema.Target(target)

    # default display language is English
    try:
        selected_language = flask.request.args.getlist('lang')[0]
    except IndexError:
        selected_language = u'en'

    if flask.request.method == "POST":
        data = flask.request.form.to_dict()

        selected_language = data['language']

        target_schema['title'][selected_language].set(data['title-' + selected_language])
        target_schema['description'][selected_language].set(data['body-' + selected_language])

        if target_schema.validate():
            target['title'][selected_language] = data['title-' + selected_language]
            target['description'][selected_language] = data['body-' + selected_language]

            flask.flash("Saved changes.", "success")
            mongo.db.targets.save(target)

    return {
                "language": selected_language,
                "target": target,
                "schema": target_schema
           }

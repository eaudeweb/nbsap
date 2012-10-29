import flask
from flaskext.babel import gettext as _

import schema
import sugar
from database import mongo
from auth import auth_required

eu_strategy = flask.Blueprint("eu_strategy", __name__)


def initialize_app(app):
    app.register_blueprint(eu_strategy)

@eu_strategy.route("/admin/eu_targets")
@auth_required
@sugar.templated("eu_strategy/targets_listing.html")
def list_targets():
    eu_targets = mongo.db.eu_targets.find()

    return {
        "targets": eu_targets,
    }


@eu_strategy.route("/admin/eu_targets/add", methods=["GET", "POST"])
@auth_required
@sugar.templated("eu_strategy/add_target.html")
def add_target():
    target_schema = schema.EUTarget({})
    tmp_collection = mongo.db.eu_targets.find().sort('id', -1)
    try:
        new_index = tmp_collection[0]['id'] + 1
    except IndexError:
        new_index = 1
    target_schema['id'] = new_index

    if flask.request.method == "POST":
        data = flask.request.form.to_dict()
        target_schema['title']['en'].set(data['title-en'])
        target_schema['body']['en'].set(data['body-en'])

        if target_schema.validate():
            target = target_schema.flatten()
            sugar.get_none_fields_for_schema(target)
            flask.flash(_("EU target successfully added."), "success")
            mongo.db.eu_targets.save(target)
            return flask.redirect(flask.url_for('eu_strategy.list_targets'))
        else:
            flask.flash(_("Error in adding an EU target."), "error")

    return {
        "schema": target_schema,
    }


@eu_strategy.route("/admin/eu_targets/<int:target_id>")
@auth_required
@sugar.templated("eu_strategy/view_target.html")
def view_target(target_id):
    target = mongo.db.eu_targets.find_one_or_404({'id': target_id})

    return {
        "target": target,
    }

@eu_strategy.route("/admin/eu_targets/<int:target_id>/edit",
                   methods=["GET", "POST"])
@auth_required
@sugar.templated("eu_strategy/edit_target.html")
def edit_target(target_id):
    return {
    }

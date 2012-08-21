import flask
import sugar
from database import mongo

targets = flask.Blueprint("targets", __name__)

def initialize_app(app):
    app.register_blueprint(targets)

@targets.route("/targets")
@sugar.templated("targets_listing.html")
def list_targets():

    aichi_targets = mongo.db.targets.find()

    return {
            "targets": aichi_targets
           }

@targets.route("/targets/data")
def target_data():
    target_ids = flask.request.args.getlist('other_targets', None)
    aichi_targets = []

    for target_id in target_ids:
       aichi_target = mongo.db.targets.find_one_or_404({"id": target_id})
       aichi_target.pop('_id', None)
       aichi_targets.append(aichi_target)

    result = {'result': aichi_targets}
    return flask.jsonify(result)


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


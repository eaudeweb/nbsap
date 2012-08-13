import flask
import sugar

targets = flask.Blueprint("targets", __name__)

def initialize_app(app):
    app.register_blueprint(targets)

@targets.route("/targets")
@sugar.templated("targets_listing.html")
def list_targets():
    from app import mongo

    aichi_targets = mongo.db.targets.find()

    return {
            "targets": aichi_targets
           }


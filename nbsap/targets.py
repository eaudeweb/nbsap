import flask
import sugar

from schema.refdata import _load_json

targets = flask.Blueprint("targets", __name__)

def initialize_app(app):
    app.register_blueprint(targets)

@targets.route('/targets')
@sugar.templated("targets_listing.html")
def list_targets():
    aichi_targets = _load_json("../refdata/aichi_targets.json")
    return {
            "targets": aichi_targets
           }



import flask
import sugar

from schema.refdata import _load_json

indicators = flask.Blueprint("indicators", __name__)

def initialize_app(app):
    app.register_blueprint(indicators)

@indicators.route('/indicators')
@sugar.templated("indicators_listing.html")
def list_indicators():
    aichi_indicators = _load_json("../refdata/aichi_indicators.json")
    return {
            "indicators": aichi_indicators
           }



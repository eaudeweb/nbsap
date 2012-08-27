import flask
import sugar
from database import mongo

from schema.refdata import _load_json

indicators = flask.Blueprint("indicators", __name__)

def initialize_app(app):
    app.register_blueprint(indicators)

@indicators.route("/indicators")
@sugar.templated("indicators/indicators_listing.html")
def list_indicators():

    aichi_indicators = mongo.db.indicators.find()

    return {
            "indicators": aichi_indicators
           }

@indicators.route("/indicators/<string:indicator_id>")
@sugar.templated("indicators/view.html")
def view(indicator_id):

    indicator = mongo.db.indicators.find_one_or_404({'id': indicator_id})
    aichi_indicator_keys = _load_json("../refdata/aichi_indicator_keys.json")
    aichi_order = _load_json("../refdata/aichi_indicator_keys_order.json")

    return {
            "indicator": indicator,
            "transit_dict": aichi_indicator_keys,
            "order": aichi_order['order']
           }


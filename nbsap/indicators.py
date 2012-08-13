import flask
import sugar

from schema.refdata import _load_json

indicators = flask.Blueprint("indicators", __name__)

def initialize_app(app):
    app.register_blueprint(indicators)

@indicators.route("/indicators")
@sugar.templated("indicators/indicators_listing.html")
def list_indicators():
    from app import mongo

    aichi_indicators = mongo.db.indicators.find()

    return {
            "indicators": aichi_indicators
           }

@indicators.route("/indicators/<int:indicator_id>")
@sugar.templated("indicators/view.html")
def view(indicator_id):
    from app import mongo

    aichi_indicators = mongo.db.indicators.find()
    aichi_indicator_keys = _load_json("../refdata/aichi_indicator_keys.json")
    aichi_order = _load_json("../refdata/aichi_indicator_keys_order.json")

    # Online targets are 1-indexed but in json database it is 0-indexed
    correct_index = int(indicator_id)-1
    specified_indicator = aichi_indicators[correct_index]

    return {
            "indicator": specified_indicator,
            "transit_dict": aichi_indicator_keys,
            "order": aichi_order['order']
           }


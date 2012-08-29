import flask
import sugar
import schema
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

@indicators.route("/indicators/<string:indicator_id>/edit", methods=["GET", "POST"])
@sugar.templated("indicators/edit.html")
def edit(indicator_id):
    app = flask.current_app

    indicator = mongo.db.indicators.find_one_or_404({'id': indicator_id})
    aichi_indicator_keys = _load_json("../refdata/aichi_indicator_keys.json")
    aichi_order = _load_json("../refdata/aichi_indicator_keys_order.json")

    indicator_schema = schema.Indicator(indicator)
    indicator_schema['relevant_target'].valid_values = map(str, indicator_schema['relevant_target'].valid_values)
    indicator_schema['relevant_target'].set(str(indicator['relevant_target']))

    # default display language is English
    try:
        selected_language = flask.request.args.getlist('lang')[0]
    except IndexError:
        selected_language = u'en'

    if flask.request.method == "POST":
        data = flask.request.form.to_dict()

        selected_language = data['language']

        if indicator_schema.validate():
            flask.flash("Saved changes.", "success")

    return {
                "language": selected_language,
                "indicator": indicator,
                "transit_dict": aichi_indicator_keys,
                "order": aichi_order['order'],
                "schema": indicator_schema,
                "mk": sugar.MarkupGenerator(
                    app.jinja_env.get_template("widgets/widgets_edit_data.html")
                  )
    }


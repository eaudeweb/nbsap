import flask
import sugar
import schema
from database import mongo

from schema.refdata import _load_json

indicators = flask.Blueprint("indicators", __name__)

def initialize_app(app):
    app.register_blueprint(indicators)

@indicators.route("/indicators")
@sugar.templated("indicators/homepage.html")
def homepage_indicators():
    page = int(flask.request.args.get('page', 1))

    if page not in range(1, 6):
        return flask.abort(404)

    # Use some math to generate the index intervals from the page number.
    get_start_index = lambda (x) : 20 * x - 19

    # Render 20 indicators per page.
    start_index = get_start_index(page)
    end_index = start_index + 19

    indicators = [i for i in mongo.db.indicators.find({ '$and': [{'id': {'$gte': start_index}},
                                                                 {'id': {'$lte': end_index}}]
                                                     }).sort('id')]

    goals = [g for g in mongo.db.goals.find()]
    targets = [t for t in mongo.db.targets.find()]
    mapping = schema.refdata.mapping
    aichi_indicator_keys = _load_json("../refdata/aichi_indicator_keys.json")
    aichi_order = _load_json("../refdata/aichi_indicator_keys_order.json")

    return {
             'indicators': indicators,
             'goals': goals,
             'targets': targets,
             'transit_dict': aichi_indicator_keys,
             'order': aichi_order['order'],
             'scale_labels': schema.refdata.indicator_data['scale'],
             'mapping': mapping
           }

@indicators.route("/admin/indicators")
@sugar.templated("indicators/indicators_listing.html")
def list_indicators():

    aichi_indicators = mongo.db.indicators.find()

    return {

            "editable_keys": sugar.get_indicator_editable_fields(),
            "indicators": aichi_indicators
           }

@indicators.route("/admin/indicators/<int:indicator_id>")
@sugar.templated("indicators/view.html")
def view(indicator_id):
    indicator = mongo.db.indicators.find_one_or_404({'id': indicator_id})
    aichi_indicator_keys = _load_json("../refdata/aichi_indicator_keys.json")
    aichi_order = _load_json("../refdata/aichi_indicator_keys_order.json")

    goal_description = None
    if indicator.get('goal'):
        goal_description = mongo.db.goals.find_one({'short_title': indicator['goal']})

    main_target_description = None
    if indicator.get('relevant_target'):
        main_target_description = mongo.db.targets.find_one({'id': indicator['relevant_target']})

    other_targets_descriptions = []
    if indicator.get('other_targets'):
        other_targets_descriptions = [target['description']['en'] for target in
                mongo.db.targets.find({'id': {'$in': indicator.get('other_targets')}})]

    return {
            "indicator": indicator,
            "transit_dict": aichi_indicator_keys,
            "order": aichi_order['order'],
            "scale_labels": schema.refdata.indicator_data['scale'],
            "goal_description": goal_description['description']['en'],
            "main_target_description": main_target_description['description']['en'],
            "other_targets_descriptions": other_targets_descriptions
           }

@indicators.route("/admin/indicators/<int:indicator_id>/edit", methods=["GET", "POST"])
@sugar.templated("indicators/edit.html")
def edit(indicator_id):
    app = flask.current_app

    indicator = mongo.db.indicators.find_one_or_404({'id': indicator_id})

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
        other_targets = flask.request.form.getlist('other_targets')
        scale = flask.request.form.getlist('scale')

        text_keys = ["status", "classification", "sources", "question", "measurer",
                "sub_indicator", "head_indicator", "requirements", "name"]

        for key in text_keys:
            value = data.get(key + '_' + selected_language, '')
            indicator_schema[key][selected_language].set(value)

        enum_keys = ["goal", "relevant_target", "sensitivity",
                    "validity", "ease_of_communication"]

        for key in enum_keys:
            value = data.get(key, '')
            indicator_schema[key].set(value)

        indicator_schema['other_targets'].set(other_targets)
        indicator_schema['scale'].set(scale)
        indicator_schema['conventions'].set(data['conventions'])

        for i in range(len(indicator_schema['links'])):
            indicator_schema['links'][i]['url'].set(data['url_' + str(i)])
            indicator_schema['links'][i]['url_name'][selected_language].set(data['url_name_' + selected_language + '_' + str(i)])

        if indicator_schema.validate():
            flask.flash("Saved changes.", "success")
            indicator.update(indicator_schema.flatten())
            mongo.db.indicators.save(indicator)

    return {
                "language": selected_language,
                "indicator": indicator,
                "schema": indicator_schema,
                "mk": sugar.MarkupGenerator(
                    app.jinja_env.get_template("widgets/widgets_edit_data.html")
                  ),
    }


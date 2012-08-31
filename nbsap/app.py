import flask
from flaskext.babel import Babel
from database import mongo

import goals
import targets
import indicators
import objectives
import actions

from raven.contrib.flask import Sentry
from flaskext.markdown import Markdown

default_config = {
        "MONGO_DBNAME": "nbsap",
}

babel = Babel()
sentry = Sentry()

def create_app(instance_path=None, testing_config=None):
    app = flask.Flask(__name__,
                      instance_path=instance_path,
                      instance_relative_config=True)

    app.config.update(default_config)

    if testing_config:
        app.config.update(testing_config)
    else:
        app.config.from_pyfile("settings.py", silent=True)

    sentry.init_app(app)

    goals.initialize_app(app)
    targets.initialize_app(app)
    indicators.initialize_app(app)
    objectives.initialize_app(app)
    actions.initialize_app(app)

    mongo.init_app(app)
    babel.init_app(app)

    Markdown(app)

    @app.route('/ping')
    def ping():
        return "nbsap is okay"

    @app.route('/crashme')
    def crashme():
        raise ValueError("Crashing, as requested.")

    return app

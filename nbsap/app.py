import flask
from flaskext.babel import Babel

import goals
import targets

default_config = {
}

babel = Babel()

def create_app(instance_path=None):
    app = flask.Flask(__name__,
                      instance_path=instance_path,
                      instance_relative_config=True)

    app.config.from_pyfile("settings.py", silent=True)

    goals.initialize_app(app)
    targets.initialize_app(app)

    babel.init_app(app)

    @app.route('/ping')
    def ping():
        return "nbsap is okay"

    @app.route('/crashme')
    def crashme():
        raise ValueError("Crashing, as requested.")

    return app

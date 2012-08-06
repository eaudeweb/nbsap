import flask
from flaskext.babel import gettext

homepage = flask.Blueprint("homepage", __name__)

def initialize_app(app):
    app.register_blueprint(homepage)

@homepage.route('/')
def home():
    app = flask.current_app
    babel = app.extensions['babel']
    babel.locale_selector_func = lambda: flask.request.args.get('lang', 'en')
    return gettext('Hello world my friends!')



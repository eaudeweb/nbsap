import flask

homepage = flask.Blueprint("homepage", __name__)

def initialize_app(app):
    app.register_blueprint(homepage)

@homepage.route('/')
def home():
    return 'Hello world my friends!'




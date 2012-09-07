import flask

from functools import wraps

auth = flask.Blueprint("auth", __name__)

def initialize_app(app):
    app.register_blueprint(auth)

def auth_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if flask.g.user is None:
            login_url = flask.url_for("goals.home", next=flask.request.url)
            return flask.redirect(login_url)
        return view(*args, **kwargs)
    return wrapper

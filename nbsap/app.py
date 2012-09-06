import flask
from flaskext.babel import Babel
from database import mongo, User, db_session
from flaskext.openid import OpenID

import goals
import targets
import indicators
import objectives
import actions
import auth

from raven.contrib.flask import Sentry
from flaskext.markdown import Markdown

default_config = {
        "MONGO_DBNAME": "nbsap",
}

oid = OpenID()
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

    goals.initialize_app(app)
    targets.initialize_app(app)
    indicators.initialize_app(app)
    objectives.initialize_app(app)
    actions.initialize_app(app)
    auth.initialize_app(app)

    mongo.init_app(app)
    babel.init_app(app)
    sentry.init_app(app)
    oid.init_app(app)

    Markdown(app)

    @app.route('/ping')
    def ping():
        return "nbsap is okay"

    @app.route('/crashme')
    def crashme():
        raise ValueError("Crashing, as requested.")

    @app.route('/index')
    def index():
        return flask.render_template('index.html')

    @app.before_request
    def before_request():
        flask.g.user = None
        if 'openid' in flask.session:
            flask.g.user = User.query.filter_by(openid=flask.session['openid']).first()

    @app.after_request
    def after_request(response):
        db_session.remove()
        return response

    @app.route("/login", methods=['GET', 'POST'])
    @oid.loginhandler
    def login():
        # if already logged in, go back to were came from
        if flask.g.user is not None:
            return flask.redirect(oid.get_next_url())
        if flask.request.method == 'POST':
            openid = flask.request.form.get('openid')
            if openid:
                return oid.try_login(openid)

        return flask.render_template('login.html', next=oid.get_next_url(),
                                error = oid.fetch_error())

    @oid.after_login
    def create_or_login(resp):
        flask.session['openid'] = resp.identity_url
        user = User.query.filter_by(openid=resp.identity_url).first()

        if user is not None:
            flask.flash(u'Successfully signed in.', "success")
            flask.g.user = user
            return flask.redirect(oid.get_next_url())

        return flask.redirect(flask.url_for('add_new_user', next=oid.get_next_url()))

    @app.route("/add-new-user", methods=['GET', 'POST'])
    def add_new_user():
        if flask.g.user is not None or 'openid' not in flask.session:
            return flask.redirect(oid.get_next_url())

        flask.flash('Newcomer admin. Welcome!', "success")
        db_session.add(User(flask.session['openid']))
        db_session.commit()

        return flask.redirect(oid.get_next_url())

    @app.route('/logout')
    def logout():
        flask.session.pop('openid', None)
        flask.flash(u'Successfully signed out.', "success")
        return flask.redirect(oid.get_next_url())

    return app


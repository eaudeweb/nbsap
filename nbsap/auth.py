import flask
from flaskext.babel import gettext as _

from database import oid, User, db_session
from functools import wraps
from flaskext.openid import COMMON_PROVIDERS

auth = flask.Blueprint("auth", __name__)


def initialize_app(app):
    app.register_blueprint(auth)


@auth.route('/index')
def index():
    return flask.render_template('index.html')


@auth.route("/login", methods=['GET', 'POST'])
@oid.loginhandler
def login():
    # if already logged in, go back to were came from
    if flask.g.user is not None:
        return flask.redirect(oid.get_next_url())

    return flask.render_template('login.html', next=oid.get_next_url(),
                                 error=oid.fetch_error())


@auth.route("/google_login", methods=['GET'])
@oid.loginhandler
def google_login():
    if flask.g.user is not None:
        return flask.redirect(oid.get_next_url())

    return oid.try_login(COMMON_PROVIDERS['google'], ask_for=['email',
                         'fullname', 'nickname'])


@auth.route("/yahoo_login", methods=['GET'])
@oid.loginhandler
def yahoo_login():
    if flask.g.user is not None:
        return flask.redirect(oid.get_next_url())

    return oid.try_login(COMMON_PROVIDERS['yahoo'], ask_for=['email',
                         'fullname', 'nickname'])


@oid.after_login
def create_or_login(resp):
    flask.session['openid'] = resp.identity_url
    user = User.query.filter_by(openid=resp.identity_url).first()

    if user is not None:
        flask.flash(_(u'Successfully signed in.'), "success")
        flask.g.user = user
        return flask.redirect(oid.get_next_url())

    return flask.redirect(flask.url_for('auth.add_new_user',
                          next=oid.get_next_url(), name=resp.fullname or
                          resp.nickname, email=resp.email))


@auth.route("/add-new-user")
def add_new_user():
    if flask.g.user is not None or 'openid' not in flask.session:
        return flask.redirect(oid.get_next_url())

    try:
        name = flask.request.args.getlist('name')[0]
    except IndexError:
        name = None
    try:
        email = flask.request.args.getlist('email')[0]
    except IndexError:
        email = None

    flask.flash(_('Newcomer admin. Welcome!'), "success")
    db_session.add(User(name, email, flask.session['openid']))
    db_session.commit()

    return flask.redirect(oid.get_next_url())


@auth.route('/logout')
def logout():
    flask.session.pop('openid', None)
    flask.flash(_(u'Successfully signed out.'), "success")
    return flask.redirect(oid.get_next_url())


def auth_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if flask.current_app.config.get("BYPASS_LOGIN", False):
            pass
        elif flask.g.user is None:
            login_url = flask.url_for("auth.login", next=flask.request.url)
            return flask.redirect(login_url)
        return view(*args, **kwargs)
    return wrapper

import flask

from database import oid, User, db_session
from functools import wraps

auth = flask.Blueprint("auth", __name__)

def initialize_app(app):
    app.register_blueprint(auth)

@auth.before_request
def before_request():
    flask.g.user = None
    if 'openid' in flask.session:
        flask.g.user = User.query.filter_by(openid=flask.session['openid']).first()

@auth.after_request
def after_request(response):
    db_session.remove()
    return response

@auth.route('/index')
def index():
    return flask.render_template('index.html')

@auth.route("/login", methods=['GET', 'POST'])
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

    return flask.redirect(flask.url_for('auth.add_new_user', next=oid.get_next_url()))

@auth.route("/add-new-user", methods=['GET', 'POST'])
def add_new_user():
    if flask.g.user is not None or 'openid' not in flask.session:
        return flask.redirect(oid.get_next_url())

    flask.flash('Newcomer admin. Welcome!', "success")
    db_session.add(User(flask.session['openid']))
    db_session.commit()

    return flask.redirect(oid.get_next_url())

@auth.route('/logout')
def logout():
    flask.session.pop('openid', None)
    flask.flash(u'Successfully signed out.', "success")
    return flask.redirect(oid.get_next_url())

def auth_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if flask.g.user is None:
            login_url = flask.url_for("goals.home", next=flask.request.url)
            return flask.redirect(login_url)
        return view(*args, **kwargs)
    return wrapper

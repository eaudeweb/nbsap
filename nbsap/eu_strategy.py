import flask
from flaskext.babel import gettext as _

import schema
import sugar
from database import mongo
from auth import auth_required

eu_strategy = flask.Blueprint("eu_strategy", __name__)


def initialize_app(app):
    app.register_blueprint(eu_strategy)


@eu_strategy.route("/default_eutargets")
@sugar.templated("/eu_strategy/default_homepage.html")
def homepage_default():
    return {}


@eu_strategy.route("/eu_targets")
@eu_strategy.route("/eu_targets/<int:target_id>")
@sugar.templated("eu_strategy/homepage.html")
def homepage_eutargets(target_id=1):
    count_entries = mongo.db.eu_targets.count()
    if count_entries == 0:
        return flask.redirect(flask.url_for('eu_strategy.homepage_default'))

    target_ids = mongo.db.eu_targets.find({}, {'id': 1})
    target = mongo.db.eu_targets.find_one_or_404({'id': target_id})

    actions_list = []
    amask = "a%s" % (str(target['id']))

    # iterate over actions
    a_list = sorted(target['actions'], key=lambda k: k['id'])
    for a in a_list:
        action = {}
        action['key'] = ".".join([amask, str(a['id'])])
        action['title-key'] = action['key'][1:]
        action['body'] = a['body']
        action['title'] = a['title']
        actions_list.append(action)

        # for each action iterate over subactions
        sa_list = sorted(a['subactions'], key=lambda k: k['id'])
        for sa in sa_list:
            saction = {}
            saction['key'] = ".".join([action['key'], str(sa['id'])])
            saction['title-key'] = saction['key'][1:]
            saction['body'] = sa['body']
            saction['title'] = sa['title']
            actions_list.append(saction)

    return {
        "target_ids": target_ids,
        "target": target,
        "actions_list": actions_list,
    }


@eu_strategy.route("/admin/eu_targets")
@auth_required
@sugar.templated("eu_strategy/targets_listing.html")
def list_targets():
    eu_targets = mongo.db.eu_targets.find()

    return {
        "targets": eu_targets,
    }


@eu_strategy.route("/admin/eu_targets/add", methods=["GET", "POST"])
@auth_required
@sugar.templated("eu_strategy/add_target.html")
def add_target():
    target_schema = schema.EUTarget({})
    tmp_collection = mongo.db.eu_targets.find().sort('id', -1)
    try:
        new_index = tmp_collection[0]['id'] + 1
    except IndexError:
        new_index = 1
    target_schema['id'] = new_index

    if flask.request.method == "POST":
        data = flask.request.form.to_dict()
        target_schema['title']['en'].set(data['title-en'])
        target_schema['body']['en'].set(data['body-en'])

        if target_schema.validate():
            target = target_schema.flatten()
            sugar.get_none_fields_for_schema(target)
            flask.flash(_("EU target successfully added."), "success")
            mongo.db.eu_targets.save(target)
            return flask.redirect(flask.url_for('eu_strategy.list_targets'))
        else:
            flask.flash(_("Error in adding an EU target."), "error")

    return {
        "schema": target_schema,
    }


@eu_strategy.route("/admin/eu_targets/<int:target_id>/action/add",
                   methods=["GET", "POST"])
@auth_required
@sugar.templated("eu_strategy/add_action.html")
def add_action(target_id):
    target = mongo.db.eu_targets.find_one_or_404({'id': target_id})
    try:
        current_index = max(v['id'] for idx, v in enumerate(target['actions']))
    except ValueError:
        current_index = 0
    new_index = current_index + 1

    action_schema = schema.EUAction({})
    action_schema['id'] = new_index

    if flask.request.method == "POST":
        data = flask.request.form.to_dict()
        lang = data['language']

        action_schema['title'][lang].set(data['title-' + lang])
        action_schema['body'][lang].set(data['body-' + lang])

        if action_schema.validate():
            action = action_schema.flatten()
            sugar.get_none_fields_for_schema(action)
            target['actions'].append(action)
            flask.flash(_("Action successfully added."), "success")
            mongo.db.eu_targets.save(target)

            return flask.redirect(flask.url_for('eu_strategy.view_target',
                                                target_id=target['id']))
        else:
            flask.flash(_("Error in adding an action."), "error")

    return {
        "schema": action_schema,
        "target": target,
    }


@eu_strategy.route("/admin/eu_targets/<int:target_id>/action/"
                   "<int:action_id>/subaction/add", methods=["GET", "POST"])
@auth_required
@sugar.templated("eu_strategy/add_subaction.html")
def add_subaction(target_id, action_id):
    target = mongo.db.eu_targets.find_one_or_404({'id': target_id})

    # find specified action
    try:
        related_action = [a for a in target['actions']
                          if a['id'] == action_id][0]
    except IndexError:
        flask.abort(500)
    try:
        current_index = max(v['id'] for idx, v in
                            enumerate(related_action['subactions']))
    except ValueError:
        current_index = 0
    new_index = current_index + 1

    subaction_schema = schema.EUSubAction({})
    subaction_schema['id'] = new_index

    if flask.request.method == "POST":
        data = flask.request.form.to_dict()
        lang = data['language']

        subaction_schema['title'][lang].set(data['title-' + lang])
        subaction_schema['body'][lang].set(data['body-' + lang])

        if subaction_schema.validate():
            subaction = subaction_schema.flatten()
            sugar.get_none_fields_for_schema(subaction)
            related_action['subactions'].append(subaction)
            flask.flash(_("Subaction successfully added."), "success")
            mongo.db.eu_targets.save(target)

            return flask.redirect(flask.url_for('eu_strategy.view_action',
                                                target_id=target['id'],
                                                action_id=related_action['id']))
        else:
            flask.flash(_("Error in adding an subaction."), "error")

    return {
        "schema": subaction_schema,
        "action": related_action,
        "target": target,
    }


@eu_strategy.route("/admin/eu_targets/<int:target_id>")
@auth_required
@sugar.templated("eu_strategy/view_target.html")
def view_target(target_id):
    target = mongo.db.eu_targets.find_one_or_404({'id': target_id})

    return {
        "target": target,
    }


@eu_strategy.route("/admin/eu_targets/<int:target_id>/actions/<int:action_id>")
@auth_required
@sugar.templated("eu_strategy/view_action.html")
def view_action(target_id, action_id):
    target = mongo.db.eu_targets.find_one_or_404({'id': target_id})

    # find specified action
    try:
        related_action = [a for a in target['actions']
                          if a['id'] == action_id][0]
    except IndexError:
        flask.abort(500)

    return {
        "target": target,
        "action": related_action,
    }


@eu_strategy.route("/admin/eu_targets/<int:target_id>/action/"
                   "<int:action_id>/subaction/<int:subaction_id>",
                   methods=["GET", "POST"])
@auth_required
@sugar.templated("eu_strategy/view_subaction.html")
def view_subaction(target_id, action_id, subaction_id):
    target = mongo.db.eu_targets.find_one_or_404({'id': target_id})

    # find specified action
    try:
        related_action = [a for a in target['actions']
                          if a['id'] == action_id][0]
    except IndexError:
        flask.abort(500)

    try:
        related_subaction = [a for a in related_action['subactions']
                             if a['id'] == subaction_id][0]
    except IndexError:
        flask.abort(500)

    return {
        "target": target,
        "action": related_action,
        "subaction": related_subaction,
    }


@eu_strategy.route("/admin/eu_targets/<int:target_id>/edit",
                   methods=["GET", "POST"])
@auth_required
@sugar.templated("eu_strategy/edit_target.html")
def edit_target(target_id):
    target = mongo.db.eu_targets.find_one_or_404({'id': target_id})
    target_schema = schema.EUTarget(target)

    #default display language is English
    try:
        lang = flask.request.args.getlist('lang')[0]
    except IndexError:
        lang = u'en'

    if flask.request.method == "POST":
        data = flask.request.form.to_dict()
        lang = data['language']
        target_schema['title'][lang].set(data['title-' + lang])
        target_schema['body'][lang].set(data['body-' + lang])

        if target_schema.validate():
            target['title'][lang] = data['title-' + lang]
            target['body'][lang] = data['body-' + lang]
            flask.flash(_("Saved changes."), "success")
            mongo.db.eu_targets.save(target)
        else:
            flask.flash(_("Error in editing an EU target."), "error")

    return {
        "target": target,
        "schema": target_schema,
        "language": lang,
    }


@eu_strategy.route("/admin/eu_targets/<int:target_id>/actions/"
                   "<int:action_id>/edit", methods=["GET", "POST"])
@auth_required
@sugar.templated("eu_strategy/edit_action.html")
def edit_action(target_id, action_id):
    target = mongo.db.eu_targets.find_one_or_404({'id': target_id})
    try:
        related_action = [a for a in target['actions']
                          if a['id'] == action_id][0]
    except IndexError:
        flask.abort(500)
    action_schema = schema.EUAction(related_action)

    #default display language is English
    try:
        lang = flask.request.args.getlist('lang')[0]
    except IndexError:
        lang = u'en'

    if flask.request.method == "POST":
        data = flask.request.form.to_dict()
        lang = data['language']
        action_schema['title'][lang].set(data['title-' + lang])
        action_schema['body'][lang].set(data['body-' + lang])

        if action_schema.validate():
            related_action['title'][lang] = data['title-' + lang]
            related_action['body'][lang] = data['body-' + lang]
            flask.flash(_("Saved changes."), "success")
            mongo.db.eu_targets.save(target)
        else:
            flask.flash(_("Error in editing an EU action."), "error")

    return {
        "action": related_action,
        "target": target,
        "schema": action_schema,
        "language": lang,
    }


@eu_strategy.route("/admin/eu_targets/<int:target_id>/action/"
                   "<int:action_id>/subaction/<int:subaction_id>/edit",
                   methods=["GET", "POST"])
@auth_required
@sugar.templated("eu_strategy/edit_subaction.html")
def edit_subaction(target_id, action_id, subaction_id):
    target = mongo.db.eu_targets.find_one_or_404({'id': target_id})
    try:
        related_action = [a for a in target['actions']
                          if a['id'] == action_id][0]
    except IndexError:
        flask.abort(500)

    try:
        related_subaction = [a for a in related_action['subactions']
                             if a['id'] == subaction_id][0]
    except IndexError:
        flask.abort(500)
    subaction_schema = schema.EUSubAction(related_subaction)

    try:
        lang = flask.request.args.getlist('lang')[0]
    except IndexError:
        lang = u'en'

    if flask.request.method == "POST":
        data = flask.request.form.to_dict()
        lang = data['language']
        subaction_schema['title'][lang].set(data['title-' + lang])
        subaction_schema['body'][lang].set(data['body-' + lang])

        if subaction_schema.validate():
            related_subaction['title'][lang] = data['title-' + lang]
            related_subaction['body'][lang] = data['body-' + lang]
            flask.flash(_("Saved changes."), "success")
            mongo.db.eu_targets.save(target)
        else:
            flask.flash(_("Error in editing an EU subaction."), "error")

    return {
        "action": related_action,
        "subaction": related_subaction,
        "target": target,
        "schema": subaction_schema,
        "language": lang,
    }

@eu_strategy.route("/eu_targets/data")
def eu_targets_data():
    try:
        eu_target_id = flask.request.args.getlist('eu_target_id')[0]
    except IndexError:
        return flask.jsonify({'result': ''})

    eu_target = mongo.db.eu_targets.find_one_or_404({'id': int(eu_target_id)})
    result = {'result': sugar.translate(eu_target['title'])}

    return flask.jsonify(result)


@eu_strategy.route("/eu_actions/data")
def eu_actions_data():
    myactions = schema.common.get_bodies_for_actions()
    actions_ids = flask.request.args.getlist('eu_actions', None)

    eu_actions = []

    for action_id in actions_ids:
        data = {
            'title': sugar.translate(myactions[action_id]['title']),
            'description': sugar.translate(myactions[action_id]['body'])
        }
        eu_actions.append(data)

    result = {'result': eu_actions}
    return flask.jsonify(result)

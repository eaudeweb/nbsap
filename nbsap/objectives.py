import flask
from flaskext.babel import gettext as _

import schema
import sugar
from database import mongo
from auth import auth_required

objectives = flask.Blueprint("objectives", __name__)


def initialize_app(app):
    app.register_blueprint(objectives)


@objectives.route("/default_objectives")
@sugar.templated("/objectives/default_objectives.html")
def default_objectives_routing():
    return {}


@objectives.route("/default_actions")
@sugar.templated("/objectives/default_actions.html")
def default_actions_routing():
    return {}


@objectives.route("/objectives")
@objectives.route("/objectives/<int:objective_id>")
@sugar.templated("/objectives/homepage.html")
def homepage_objectives(objective_id=1):
    count_entries = mongo.db.objectives.count()
    if count_entries == 0:
        return flask.redirect(flask.url_for('objectives.'
                                            'default_objectives_routing'))

    objective_ids = mongo.db.objectives.find({}, {'id': 1})
    objective = mongo.db.objectives.find_one_or_404({'id': objective_id})
    mapping = schema.refdata.mapping

    subobj_list = sugar.get_subobjs_by_dfs(objective['id'])
    my_actions = sugar.get_actions_by_objective_id(objective['id'])

    for subobj in subobj_list:
        code_id = subobj['title-key']
        subobj['mapping'] = [m for m in
                             mongo.db.mapping.find({'objective': code_id})]
        for m in subobj['mapping']:
            m['goal'] = {
                'short_title': m['goal'],
                'description':
                mongo.db.goals.find_one_or_404(
                    {'short_title': m['goal']}
                )['description']
            }
            m['main_target'] = {
                'number': m['main_target'],
                'description': mongo.db.targets.find_one_or_404(
                    {'id': m['main_target']})['description']
            }

            for target in range(len(m['other_targets'])):
                m['other_targets'][target] = \
                    {
                        'number': m['other_targets'][target],
                        'description': mongo.db.targets.find_one_or_404(
                            {'id': m['other_targets'][target]})['description']
                    }

    return {
        "objective_ids": objective_ids,
        "objective": objective,
        "my_actions": my_actions,
        "subobj_list": subobj_list,
        'mapping': mapping
    }


@objectives.route("/actions")
@objectives.route("/objectives/<int:objective_id>/actions")
@sugar.templated("/objectives/implementation.html")
def homepage_actions(objective_id=1):
    count_entries = mongo.db.objectives.count()
    if count_entries == 0:
        return flask.redirect(flask.url_for('objectives.'
                                            'default_actions_routing'))

    objective_ids = mongo.db.objectives.find({}, {'id': 1})
    objective = mongo.db.objectives.find_one_or_404({'id': objective_id})

    mapping = schema.refdata.mapping

    actions_list = sugar.get_actions_by_dfs(objective['id'])
    for action in actions_list:
        code_id = action['corresponding_objective']
        action['mapping'] = [m for m in
                             mongo.db.mapping.find({'objective': code_id})]
        for m in action['mapping']:
            m['goal'] = {
                'short_title': m['goal'],
                'description':
                mongo.db.goals.find_one_or_404(
                    {'short_title': m['goal']}
                )['description']
            }
            m['main_target'] = {
                'number': m['main_target'],
                'description': mongo.db.targets.find_one_or_404(
                    {'id': m['main_target']})['description']
            }

            for target in range(len(m['other_targets'])):
                m['other_targets'][target] = \
                    {
                        'number': m['other_targets'][target],
                        'description': mongo.db.targets.find_one_or_404(
                            {'id': m['other_targets'][target]})['description']
                    }

    return {
        "objective_ids": objective_ids,
        "objective": objective,
        "actions": actions_list,
        "mapping": mapping,
    }


@objectives.route("/admin/objectives/add", methods=["GET", "POST"])
@auth_required
@sugar.templated("objectives/add.html")
def add():
    objective_schema = schema.Objective({})
    tmp_collection = mongo.db.objectives.find().sort('id', -1)
    try:
        new_index = tmp_collection[0]['id'] + 1
    except IndexError:
        new_index = 1
    objective_schema['id'] = new_index

    if flask.request.method == "POST":
        data = flask.request.form.to_dict()
        objective_schema['title']['en'].set(data['title-en'])
        objective_schema['body']['en'].set(data['body-en'])

        if objective_schema.validate():
            objective = objective_schema.flatten()
            sugar.get_none_fields_for_schema(objective)
            flask.flash(_("Objective successfully added."), "success")
            mongo.db.objectives.save(objective)
            return flask.redirect(flask.url_for('objectives.list_objectives'))
        else:
            flask.flash(_("Error in adding an objective."), "error")

    return {
        "schema": objective_schema
    }


@objectives.route("/admin/objectives/<int:objective_id>")
@objectives.route("/admin/objectives/<int:objective_id>/"
                  "<int:so1_id>")
@objectives.route("/admin/objectives/<int:objective_id>/"
                  "<int:so1_id>/<int:so2_id>")
@objectives.route("/admin/objectives/<int:objective_id>/"
                  "<int:so1_id>/<int:so2_id>/<int:so3_id>")
@objectives.route("/admin/objectives/<int:objective_id>/"
                  "<int:so1_id>/<int:so2_id>/<int:so3_id>/<int:so4_id>")
@auth_required
@sugar.templated("objectives/view.html")
def view(objective_id,
         so1_id=None, so2_id=None, so3_id=None, so4_id=None):
    myargs = ['objective_id', 'so1_id', 'so2_id', 'so3_id', 'so4_id']
    parents = [(i, locals()[i]) for i in myargs if locals()[i] is not None]
    objective = mongo.db.objectives.find_one_or_404({'id': objective_id})

    # get objective id
    father = objective
    for i in range(1, len(parents)):
        # get id of subsequent subobjective in parents list
        son_id = parents[i][1]
        try:
            son = [s for s in father['subobjs'] if s['id'] == son_id][0]
        except IndexError:
            flask.abort(404)
        father = son

    matrix = []
    for i, x in enumerate(parents):
        tmp_L = [y for j, y in enumerate(parents) if j < i]
        tmp_L.append(x)
        # send dict and its label
        matrix.append((dict(tmp_L), x[1]))

    subobj_parents = {}
    hit_max_depth = True if len(parents) >= len(myargs) else False

    if not hit_max_depth:
        try:
            tmp_dict = dict(parents)
            for s in father['subobjs']:
                subobj_parents[s['id']] = {myargs[len(parents)]: s['id']}
                subobj_parents[s['id']].update(tmp_dict)
        except IndexError:
            hit_max_depth = True
            pass

    actions_parents = {}

    try:
        tmp_dict = dict(parents)
        for a in father['actions']:
            actions_parents[a['id']] = {"action_id": a['id']}
            actions_parents[a['id']].update(tmp_dict)
    except IndexError:
        flask.abort(404)

    return {
        "max_depth": hit_max_depth,
        "chain_matrix": matrix,
        "subobj_parents": subobj_parents,
        "parents": dict(parents),
        "objective": father,
        "actions_parents": actions_parents,
    }


@objectives.route("/objectives/data")
def objective_data():
    try:
        id_code = flask.request.args.getlist('id_code')[0]
    except IndexError:
        return flask.jsonify({'result': ''})

    objective_ids = map(int, id_code.split('.'))
    subobj = mongo.db.objectives.find_one_or_404({"id": objective_ids[0]})

    for depth in range(len(objective_ids) - 1):
        subobj = [s for s in subobj['subobjs'] if
                  s['id'] == objective_ids[depth + 1]][0]

    result = {'result': sugar.translate(subobj['title'])}
    return flask.jsonify(result)


@objectives.route("/admin/objectives/<int:objective_id>/edit",
                  methods=["GET", "POST"])
@objectives.route("/admin/objectives/<int:objective_id>/"
                  "<int:so1_id>/edit", methods=["GET", "POST"])
@objectives.route("/admin/objectives/<int:objective_id>/"
                  "<int:so1_id>/<int:so2_id>/edit",
                  methods=["GET", "POST"])
@objectives.route("/admin/objectives/<int:objective_id>/"
                  "<int:so1_id>/<int:so2_id>/<int:so3_id>/edit",
                  methods=["GET", "POST"])
@objectives.route("/admin/objectives/<int:objective_id>/"
                  "<int:so1_id>/<int:so2_id>/<int:so3_id>/<int:so4_id>"
                  "/edit", methods=["GET", "POST"])
@auth_required
@sugar.templated("objectives/edit.html")
def edit(objective_id,
         so1_id=None, so2_id=None, so3_id=None, so4_id=None):
    myargs = ['objective_id', 'so1_id', 'so2_id', 'so3_id', 'so4_id']
    parents = [(i, locals()[i]) for i in myargs if locals()[i] is not None]
    objective = mongo.db.objectives.find_one_or_404({'id': objective_id})

    father = objective
    for i in range(1, len(parents)):
        son_id = parents[i][1]
        try:
            son = [s for s in father['subobjs'] if s['id'] == son_id][0]
        except IndexError:
            flask.abort(404)
        father = son

    matrix = []
    for i, x in enumerate(parents):
        tmp_L = [y for j, y in enumerate(parents) if j < i]
        tmp_L.append(x)
        matrix.append((dict(tmp_L), x[1]))

    objective_schema = schema.Objective(father)

    # default display language is English
    try:
        lang = flask.request.args.getlist('lang')[0]
    except IndexError:
        lang = u'en'

    if flask.request.method == "POST":
        data = flask.request.form.to_dict()
        lang = data['language']
        objective_schema['title'][lang].set(data['title-' + lang])
        objective_schema['body'][lang].set(data['body-' + lang])

        if objective_schema.validate():
            father['title'][lang] = data['title-' + lang]
            father['body'][lang] = data['body-' + lang]
            flask.flash(_("Saved changes."), "success")
            mongo.db.objectives.save(objective)
        else:
            flask.flash(_("Error in editing an objective."), "error")

    return {
        "parents": dict(parents),
        "chain_matrix": matrix,
        "language": lang,
        "objective": father,
        "schema": objective_schema
    }


@objectives.route("/admin/objectives/<int:objective_id>/add_subobj",
                  methods=["GET", "POST"])
@objectives.route("/admin/objectives/<int:objective_id>/"
                  "<int:so1_id>/add_subobj", methods=["GET", "POST"])
@objectives.route("/admin/objectives/<int:objective_id>/"
                  "<int:so1_id>/<int:so2_id>/add_subobj",
                  methods=["GET", "POST"])
@objectives.route("/admin/objectives/<int:objective_id>/"
                  "<int:so1_id>/<int:so2_id>/<int:so3_id>/add_subobj",
                  methods=["GET", "POST"])
@objectives.route("/admin/objectives/<int:objective_id>/"
                  "<int:so1_id>/<int:so2_id>/<int:so3_id>/<int:so4_id>"
                  "/add_subobj", methods=["GET", "POST"])
@auth_required
@sugar.templated("objectives/subobj_add.html")
def add_subobj(objective_id,
               so1_id=None, so2_id=None, so3_id=None, so4_id=None):
    objective = mongo.db.objectives.find_one_or_404({'id': objective_id})
    myargs = ['objective_id', 'so1_id', 'so2_id', 'so3_id', 'so4_id']
    parents = [(i, locals()[i]) for i in myargs if locals()[i] is not None]

    father = objective
    for i in range(1, len(parents)):
        son_id = parents[i][1]
        try:
            son = [s for s in father['subobjs'] if s['id'] == son_id][0]
        except IndexError:
            flask.abort(404)
        father = son

    matrix = []
    for i, x in enumerate(parents):
        tmp_L = [y for j, y in enumerate(parents) if j < i]
        tmp_L.append(x)
        matrix.append((dict(tmp_L), x[1]))

    subobj_schema = schema.Objective({})

    # find its largest existing 'subobjs' index
    subobj_list = father['subobjs']
    sorted_list = sorted(subobj_list, key=lambda k: k['id'], reverse=True)

    if sorted_list:
        new_index = sorted_list[0]['id'] + 1
    else:
        new_index = 1

    subobj_schema['id'] = new_index

    if flask.request.method == "POST":
        data = flask.request.form.to_dict()

        subobj_schema['title']['en'].set(data['title-en'])
        subobj_schema['body']['en'].set(data['body-en'])

        if subobj_schema.validate():
            subobj = subobj_schema.flatten()
            sugar.get_none_fields_for_schema(subobj)
            father['subobjs'].append(subobj)
            flask.flash(_("Subobjective successfully added."), "success")
            mongo.db.objectives.save(objective)

            return flask.redirect(flask.url_for('objectives.view',
                                                **dict(parents)))
        else:
            flask.flash(_("Error in adding an subobjective."), "error")

    return {
        "objective": father,
        "schema": subobj_schema,
        "parents": dict(parents),
        "chain_matrix": matrix
    }


@objectives.route("/admin/objectives/<int:objective_id>/delete",
                  methods=["GET", "POST", "DELETE"])
@objectives.route("/admin/objectives/<int:objective_id>/"
                  "<int:so1_id>/delete", methods=["GET", "POST", "DELETE"])
@objectives.route("/admin/objectives/<int:objective_id>/"
                  "<int:so1_id>/<int:so2_id>/delete",
                  methods=["GET", "POST", "DELETE"])
@objectives.route("/admin/objectives/<int:objective_id>/"
                  "<int:so1_id>/<int:so2_id>/<int:so3_id>/delete",
                  methods=["GET", "POST", "DELETE"])
@objectives.route("/admin/objectives/<int:objective_id>/"
                  "<int:so1_id>/<int:so2_id>/<int:so3_id>/<int:so4_id>"
                  "/delete", methods=["GET", "POST", "DELETE"])
@auth_required
def delete(objective_id,
           so1_id=None, so2_id=None, so3_id=None, so4_id=None):
    myargs = ['objective_id', 'so1_id', 'so2_id', 'so3_id', 'so4_id']
    parents = [(i, locals()[i]) for i in myargs if locals()[i] is not None]
    objective = mongo.db.objectives.find_one_or_404({'id': objective_id})

    from pymongo.errors import OperationFailure

    if len(parents) == 1:
        subobj_list = sugar.generate_objectives()[objective_id]
        # clean up entire object
        try:
            mongo.db.objectives.remove(spec_or_id=objective['_id'], safe=True)
            flask.flash(_("Objective deleted."), "success")
        except OperationFailure:
            flask.flash(_("Errors found when deleting objective."), "errors")
            pass
    else:
        mask = str(objective['id'])
        father = objective
        parent = objective
        for i in range(1, len(parents)):
            son_id = parents[i][1]
            try:
                son = [s for s in father['subobjs'] if s['id'] == son_id][0]
            except IndexError:
                flask.abort(404)
            parent = father
            father = son
            mask = ".".join([mask, str(son['id'])])

        subobj_list = sugar.get_subobjs_of_subobj(father, mask)
        # clean up entire subobjective from its parent list
        parent['subobjs'] = [s for s in parent['subobjs'] if s['id'] !=
                             father['id']]
        try:
            mongo.db.objectives.save(objective, safe=True)
            flask.flash(_("Objective deleted."), "success")
        except OperationFailure:
            flask.flash(_("Errors found when deleting objective."), "errors")
            pass

    # clean up all mappings for subobjectives
    for subobj_id in subobj_list:
        mappings = mongo.db.mapping.find()
        related_mappings_ids = [m['_id'] for m in mappings
                                if m['objective'] == subobj_id]
        for mapping_id in related_mappings_ids:
            try:
                mongo.db.mapping.remove(spec_or_id=mapping_id)
            except OperationFailure:
                flask.flash(_("Errors found when deleting"
                              "corresponding mappings."), "errors")
                pass

    return flask.jsonify({'status': 'success'})


@objectives.route("/admin/objectives")
@auth_required
@sugar.templated("objectives/objectives_listing.html")
def list_objectives():
    objectives = mongo.db.objectives.find()

    return {
        "objectives": objectives,
    }

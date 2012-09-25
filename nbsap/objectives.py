import flask
from flaskext.babel import gettext as _

import schema
import sugar
from database import mongo
from auth import auth_required

objectives = flask.Blueprint("objectives", __name__)


def initialize_app(app):
    app.register_blueprint(objectives)


@objectives.route("/objectives")
@objectives.route("/objectives/<int:objective_id>")
@sugar.templated("/objectives/homepage.html")
def homepage_objectives(objective_id=1):

    objective_ids = mongo.db.objectives.find({}, {'id': 1})
    objective = mongo.db.objectives.find_one_or_404({'id': objective_id})

    mapping = schema.refdata.mapping

    for subobj in objective['subobjs']:
        code_id = str(objective['id']) + '.' + str(subobj['id'])
        subobj['mapping'] = [m for m in
                             mongo.db.mapping.find({'objective': code_id})]
        for m in subobj['mapping']:
            m['goal'] = {'short_title': m['goal'],
                         'description': \
                         mongo.db.goals.find_one(
                                                 {'short_title': m['goal']})\
                                                ['description']
                        }
            m['main_target'] = { 'number': m['main_target'],
                                 'description': mongo.db.targets.find_one({'id': m['main_target']})['description']
                                }

            for target in range(len(m['other_targets'])):
                m['other_targets'][target] = \
                    {
                     'number': m['other_targets'][target],
                     'description': mongo.db.targets.find_one({'id': m['other_targets'][target]})['description']
                    }

    return {
        'objective_ids': objective_ids,
        'objective': objective,
        'mapping': mapping
    }

@objectives.route("/admin/objectives/add", methods=["GET", "POST"])
@auth_required
@sugar.templated("objectives/add.html")
def add():
    objective_schema = schema.Objective({})

    tmp_collection = mongo.db.objectives.find().sort('id', -1)
    new_index = tmp_collection[0]['id'] + 1

    objective_schema['id'] = new_index

    if flask.request.method == "POST":
        data = flask.request.form.to_dict()

        objective_schema['title']['en'].set(data['title-en'])
        objective_schema['body']['en'].set(data['body-en'])

        if objective_schema.validate():
            objective = objective_schema.flatten()
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
    so1_id=None, so2_id = None, so3_id = None, so4_id = None):

    myargs = ['objective_id', 'so1_id', 'so2_id', 'so3_id', 'so4_id']
    parents = [(i, locals()[i]) for i in myargs if locals()[i] != None]

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
               subobj_parents[s['id']] = { myargs[len(parents)]: s['id'] }
               subobj_parents[s['id']].update(tmp_dict)
        except IndexError:
           hit_max_depth = True
           pass

    return {
        "max_depth": hit_max_depth,
        "chain_matrix": matrix,
        "subobj_parents": subobj_parents,
        "parents": dict(parents),
        "objective": father,
    }


@objectives.route("/objectives/data")
def objective_data():

    try:
        id_code = flask.request.args.getlist('id_code')[0]
    except IndexError:
        return flask.jsonify({'result': ''})

    objective_ids = map(int, id_code.split('.'))
    subobjective = mongo.db.objectives.find_one_or_404({"id": objective_ids[0]})

    for depth in range(len(objective_ids) - 1):
        subobjective = [s for s in subobjective['subobjs'] if
                            s['id'] == objective_ids[depth + 1]][0]

    result = {'result': sugar.translate(subobjective['title'])}
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
    so1_id=None, so2_id = None, so3_id = None, so4_id = None):

    myargs = ['objective_id', 'so1_id', 'so2_id', 'so3_id', 'so4_id']
    parents = [(i, locals()[i]) for i in myargs if locals()[i] != None]

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
        selected_language = flask.request.args.getlist('lang')[0]
    except IndexError:
        selected_language = u'en'

    if flask.request.method == "POST":
        data = flask.request.form.to_dict()
        selected_language = data['language']

        objective_schema['title'][selected_language].set(
                                        data['title-' + selected_language])
        objective_schema['body'][selected_language].set(
                                        data['body-' + selected_language])

        if objective_schema.validate():
            father['title'][selected_language] = data['title-' +
                                                         selected_language]
            father['body'][selected_language] = data['body-' +
                                                        selected_language]
            flask.flash(_("Saved changes."), "success")
            mongo.db.objectives.save(objective)

    return {
        "parents": dict(parents),
        "chain_matrix": matrix,
        "language": selected_language,
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
    so1_id=None, so2_id = None, so3_id = None, so4_id = None):

    objective = mongo.db.objectives.find_one_or_404({'id': objective_id})
    myargs = ['objective_id', 'so1_id', 'so2_id', 'so3_id', 'so4_id']
    parents = [(i, locals()[i]) for i in myargs if locals()[i] != None]

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
            father['subobjs'].append(subobj)
            flask.flash(_("Subobjective successfully added."), "success")
            mongo.db.objectives.save(objective)

            return flask.redirect(flask.url_for('objectives.view', **dict(parents)))
        else:
            flask.flash(_("Error in adding an subobjective."), "error")

    return {
        "objective": father,
        "schema": subobj_schema,
        "parents": dict(parents),
        "chain_matrix": matrix
    }

@objectives.route("/admin/objectives")
@auth_required
@sugar.templated("objectives/objectives_listing.html")
def list_objectives():

    objectives = mongo.db.objectives.find()

    return {
        "objectives": objectives,
    }



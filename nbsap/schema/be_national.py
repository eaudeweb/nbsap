import flatland

from common import I18nString, CommonString, CommonList, CommonInteger

Subobjective = flatland.Dict.of(
            I18nString.named('title'),
            I18nString.named('body'),
            CommonString.named('id'),
        )

_ObjectiveSchemaDefinition = flatland.Dict.of(
            I18nString.named('title'),
            I18nString.named('body'),
            CommonString.named('id'),
            CommonList.named('subobjs').of(Subobjective),
        )

GenericEditSchema = flatland.Dict.with_properties(widget="form").of(
            CommonString.named('title')
                .using(label=u'Title', optional=False)
                .with_properties(widget="input"),
            CommonString.named('body')
                .using(label=u'Description', optional=False)
                .with_properties(widget="edit_textarea"),

        )

_action = flatland.Dict.of(
            I18nString.named('title'),
            I18nString.named('body'),
            CommonInteger.named('id'),
        )

_ActionsSchemaDefinition = flatland.Dict.of(
            I18nString.named('title'),
            CommonInteger.named('id'),
            CommonList.named('actions').of(_action),
        )

class Objective(_ObjectiveSchemaDefinition):

    def __init__(self, init_objective):
        objective = dict(init_objective)
        objective.pop('_id', None)
        self.set(objective)

    def flatten(self):
        return self.value

class Action(_ActionsSchemaDefinition):

    def __init__(self, init_action):
        action = dict(init_action)
        action.pop('_id', None)
        self.set(action)

    def flatten(self):
        return self.value


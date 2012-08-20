import flatland

from flatland.validation import Present

from common import I18nString, CommonString, CommonList

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

class Objective(_ObjectiveSchemaDefinition):

    def __init__(self, init_objective):
        objective = dict(init_objective)
        objective.pop('_id', None)
        self.set(objective)

    def flatten(self):
        return self.value

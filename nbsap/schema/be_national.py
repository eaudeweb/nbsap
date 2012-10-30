import flatland

from common import I18nString, CommonString, CommonList, CommonInteger, I18nStringOptional

_subobj_list = CommonList.named('subobjs').with_properties(widget="hidden")

_action = flatland.Dict.of(
            I18nString.named('title')
                .using(label=u'Title'),
            I18nString.named('body')
                .using(label=u'Description'),
            CommonInteger.named('id'),
        )

_ObjectiveSchemaDefinition = flatland.Dict.named("objective").with_properties(widget="edit").of(
            I18nString.named('title')
                .using(label=u'Title')
                .with_properties(css_class="span4"),
            I18nStringOptional.named('body')
                .using(label=u'Description')
                .with_properties(field_widget="edit_textarea",
                                 css_class="input-xlarge"),
            CommonInteger.named('id')
                .with_properties(widget="hidden"),
            _subobj_list,
            CommonList.named('actions').of(_action)
        )

_subobj_list.member_schema = _ObjectiveSchemaDefinition

class Objective(_ObjectiveSchemaDefinition):

    def __init__(self, init_objective):
        objective = dict(init_objective)
        objective.pop('_id', None)
        self.set(objective)

    def flatten(self):
        return self.value

class Action(_action):

    def __init__(self, init_action):
        action = dict(init_action)
        action.pop('_id', None)
        self.set(action)

    def flatten(self):
        return self.value


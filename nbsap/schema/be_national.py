import flatland

from flatland.validation import Present

from .refdata import language
from common import I18nString, CommonString, CommonList, CommonEnum

Subobjective = flatland.Dict.of(
            I18nString.named('title')
                .with_properties(css_class="span4"),
            I18nString.named('body')
                .with_properties(field_widget="edit_textarea",
                                css_class="input-xlarge"),
            CommonString.named('id')
        )

_ObjectiveSchemaDefinition = flatland.Dict.named("objective").with_properties(widget="edit").of(
            I18nString.named('title')
                .using(label=u'Title', optional=False)
                .with_properties(css_class="span4"),
            I18nString.named('body')
                .using(label=u'Description', optional=False)
                .with_properties(field_widget="edit_textarea",
                                 css_class="input-xlarge"),
            CommonString.named('id')
                .with_properties(widget="hidden"),
            CommonList.named('subobjs').of(Subobjective)
                .with_properties(widget="hidden")
        )

GenericEditSchema = flatland.Dict.with_properties(widget="edit").of(
            CommonEnum.named('language')
                .using(label=u'Language', optional=False)
                .valued(*sorted(language.keys()))
                .with_properties(value_labels=language,
                                 widget="select",
                                 css_class="language-select"),

            _ObjectiveSchemaDefinition.using(label=u'')
    )

class Objective(_ObjectiveSchemaDefinition):

    def __init__(self, init_objective):
        objective = dict(init_objective)
        objective.pop('_id', None)
        self.set(objective)

    def flatten(self):
        return self.value

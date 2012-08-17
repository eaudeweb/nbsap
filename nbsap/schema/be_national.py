import flatland

from flatland.validation import Present

from .refdata import language
from common import I18nString, CommonString, CommonList, CommonEnum

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

GenericEditSchema = flatland.Dict.with_properties(widget="edit").of(
            CommonEnum.named('language')
                .using(label=u'Language', optional=False)
                .valued(*sorted(language.keys()))
                .with_properties(value_labels=language,
                                 widget="select",
                                 css_class="language-select"),

            CommonString.named('title')
                .using(label=u'Title', optional=False)
                .with_properties(widget="input",
                                 css_class="span6"),

            CommonString.named('body')
                .using(label=u'Description', optional=False)
                .with_properties(widget="edit_textarea",
                                 css_class="input-xlarge"),

    )

class Objective(_ObjectiveSchemaDefinition):

    def __init__(self, init_objective):
        objective = dict(init_objective)
        objective.pop('_id', None)
        self.set(objective)

    def flatten(self):
        return self.value

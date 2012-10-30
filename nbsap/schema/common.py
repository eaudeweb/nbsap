import flatland

from flatland.validation import Validator
from flatland.schema.base import NotEmpty
from flatland.signals import validator_validated

@validator_validated.connect
def validated(sender, element, result, **kwargs):
    if sender is NotEmpty:
        if not result:
            label = getattr(element, 'label', element.name)
            if element.name == 'en':
                label = getattr(element.parent, 'label', element.parent.name)
            msg = element.properties.get("not_empty_error",
                                         u"%s is required" % label)
            element.add_error(msg)


class GoalEnumValue(Validator):

    fail = None

    def validate(self, element, state):
        related_element =  element.find('../goal',single=True)
        self.fail = flatland.validation.base.N_(u'Target %(u)s is not related to Goal '
                                                    + str(related_element.value))

        if element.value and related_element:
            if element.properties['mapping'][element.value] != related_element.value:
                return self.note_error(element, state, 'fail')

        return True

class EnumValue(Validator):

    fail = None

    def validate(self, element, state):
        self.fail = flatland.validation.base.N_(u'%(u)s is not a valid value for %(label)s')

        if element.valid_values:
            if element.value not in map(str, element.valid_values):
                return self.note_error(element, state, 'fail')

        return True


class ListElements(Validator):

    def validate(self, element, state):
        if not (element.optional or element.value):
            self.fail = flatland.validation.base.N_('Select at least one value')
            return self.note_error(element, state, 'fail')

        for e in element.children:
            e.validate()

        return True

class ListValue(Validator):

    fail = None

    def validate(self, element, state):
        self.fail = flatland.validation.base.N_(u'%(u)s is not a valid value for %(label)s')

        if not (element.optional or element.value):
            self.fail = flatland.validation.base.N_('Select at least one value')
            return self.note_error(element, state, 'fail')

        for e in element.value:
            if e not in map(str, element.properties['valid_values']):
                return self.note_error(element, state, 'fail')

        return True

CommonInteger = flatland.Integer.using(optional=True)
CommonString = flatland.String.using(optional=True)
CommonList = flatland.List.using(optional=True)
CommonEnum = flatland.Enum.using(optional=True)\
                        .including_validators(EnumValue())\
                        .with_properties(value_labels=None)

I18nStringOptional = flatland.Dict.with_properties(widget="i18nstring").of(
            CommonString.named("en")
                .using(label=u"English"),
            CommonString.named("fr")
                .using(label=u"French"),
            CommonString.named("nl")
                .using(label="Netherlands")
        )

I18nString = flatland.Dict.with_properties(widget="i18nstring").of(
            CommonString.named("en")
                .using(optional=False,
                       label=u"English"),
            CommonString.named("fr")
                .using(label=u"French"),
            CommonString.named("nl")
                .using(label="Netherlands")
        )

CommonI18nString = flatland.Dict.with_properties(widget="i18nstring").of(
                   CommonString.named("en")
                       .using(label=u"English"),
                   CommonString.named("fr")
                       .using(label=u"French"),
                   CommonString.named("nl")
                       .using(label="Netherlands")
                )


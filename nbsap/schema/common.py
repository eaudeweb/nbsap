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


class EnumValue(Validator):

    fail = None

    def validate(self, element, state):
        self.fail = flatland.validation.base.N_(u'%(u)s is not a valid value for %(label)s')

        if element.valid_values:
            if element.value not in map(str, element.valid_values):
                return self.note_error(element, state, 'fail')

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

I18nString = flatland.Dict.with_properties(widget="i18nstring").of(
            CommonString.named("en")
                .using(optional=False,
                       label=u"English")
                .with_properties(widget="input"),
            CommonString.named("fr")
                .using(label=u"French")
                .with_properties(widget="input"),
            CommonString.named("nl")
                .using(label="Netherlands")
                .with_properties(widget="input")
        )


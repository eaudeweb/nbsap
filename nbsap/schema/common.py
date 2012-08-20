import flatland
from flatland.validation import Validator

class EnumValue(Validator):

    fail = None

    def validate(self, element, state):
        self.fail = flatland.validation.base.N_(u'%(u)s is not a valid value for %(label)s')

        if element.valid_values:
            if element.value not in element.valid_values:
                return self.note_error(element, state, 'fail')

        return True


class ListValue(Validator):

    fail = None

    def validate(self, element, state):
        self.fail = flatland.validation.base.N_(u'%(u)s is not a valid value for %(label)s')

        for e in element.value:
            if e not in element.properties['valid_values']:
                return self.note_error(element, state, 'fail')

        return True

CommonString = flatland.String.using(optional=True)
CommonList = flatland.List.using(optional=True)
CommonList = flatland.List.using(optional=True)\
                        .including_validators(ListValue())
CommonEnum = flatland.Enum.using(optional=True)\
                        .including_validators(EnumValue())\
                        .with_properties(value_labels=None)

I18nString = flatland.Dict.with_properties(widget="i18nstring").of(
            CommonString.named("en")
                .using(label=u"English")
                .with_properties(widget="input"),
            CommonString.named("fr")
                .using(label=u"French")
                .with_properties(widget="input"),
            CommonString.named("nl")
                .using(label="Netherlands")
                .with_properties(widget="input")
        )


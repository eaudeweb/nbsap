import flatland
from flatland.validation import Validator

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

        for e in element.value:
            if e not in map(str, element.properties['valid_values']):
                return self.note_error(element, state, 'fail')

        return True

CommonString = flatland.String.using(optional=True)
CommonList = flatland.List.using(optional=True)
CommonList = flatland.List.using(optional=True)\
                        .including_validators(ListValue())
CommonEnum = flatland.Enum.using(optional=True)\
                        .including_validators(EnumValue())\
                        .with_properties(value_labels=None)

I18nString = flatland.Dict.of(
            CommonString.named("en"),
            CommonString.named("fr"),
            CommonString.named("nl"),
        )


import flatland

from flatland.validation import Validator
from flatland.schema.base import NotEmpty
from flatland.signals import validator_validated

from .refdata import language

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


def split_after_colon(mystring):
    if mystring == '' or mystring is None:
        return mystring
    if mystring.find(':') < 0:
        raise ValueError('Wrong title naming. Usage <Title (nr): (desc)>')
    return mystring.split(':')[0]


def shorten_title(i18nstring):
    for k in language.keys():
        i18nstring[k] = split_after_colon(i18nstring[k])


def get_eu_targets_from_db():
    from nbsap.database import mongo
    targets = {t['id']: t['title'] for t in mongo.db.eu_targets.find()}
    for value in targets.values():
        shorten_title(value)
    return targets

def get_full_eu_actions_from_db():
    from nbsap.database import mongo
    targets = mongo.db.eu_targets.find()
    actions = []

    for target in targets:
        amask = "a%s" % (str(target['id']))
        tmp_list = sorted(target['actions'], key=lambda k: k['id'])
        for action in tmp_list:
            act = {
                'key': ".".join([amask, str(action['id'])]),
                'title': action['title'],
                'body': action['body'],
            }
            actions.append(act)
            stmp_list = sorted(action['subactions'], key=lambda k: k['id'])
            for saction in stmp_list:
                sact = {
                    'key': ".".join([act['key'], str(saction['id'])]),
                    'title': saction['title'],
                    'body': saction['body'],
                }
                actions.append(sact)

    return actions

def get_bodies_for_actions():
    actions = get_full_eu_actions_from_db()
    result = {
                a['key']: {
                    'body': a['body'],
                    'title': a['title']
                } for a in actions
             }
    return result

def get_eu_actions_from_db():
    actions = get_full_eu_actions_from_db()
    result = {a['key']:a['title'] for a in actions}
    return result


class MyCommonEnum(CommonEnum):
    @property
    def valid_values(self):
        targets = get_eu_targets_from_db()
        return tuple(sorted(targets.keys()))

    @property
    def value_labels(self):
        return get_eu_targets_from_db()

class MyCommonList(CommonList):
    @property
    def valid_values(self):
        actions  = get_eu_actions_from_db()
        return tuple(sorted(actions.keys()))

    @property
    def value_labels(self):
        return get_eu_actions_from_db()

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


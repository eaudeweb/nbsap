import flatland

from common import I18nString, CommonList, CommonInteger

_EUsubaction = flatland.Dict.of(
            I18nString.named('body')
                .using(label=u'Description'),
            CommonInteger.named('id'),
       )

_EUaction = flatland.Dict.of(
            I18nString.named('body')
                .using(label=u'Description'),
            CommonInteger.named('id'),
            CommonList.named('subactions').of(_EUsubaction),
       )


_EUTargetSchemaDefiniton = flatland.Dict.of(
            I18nString.named('title')
                .using(label=u'Title'),
            I18nString.named('body')
                .using(label=u'Description'),
            CommonInteger.named('id'),
            CommonList.named('actions').of(_EUaction),
       )

class EUTarget(_EUTargetSchemaDefiniton):
    def __init__(self, init_target):
        eu_target = dict(init_target)
        eu_target.pop('_id', None)
        self.set(eu_target)

    def flatten(self):
        return self.value

class EUAction(_EUaction):
    def __init__(self, init_action):
        action = dict(init_action)
        action.pop('_id', None)
        self.set(action)

    def flatten(self):
        return self.value

class EUSubAction(_EUsubaction):
    def __init__(self, init_subaction):
        subaction = dict(init_subaction)
        subaction.pop('_id', None)
        self.set(subaction)

    def flatten(self):
        return self.value

import flatland

from common import I18nString

_GoalSchemaDefinition = flatland.Dict.of(
            flatland.String.named('short_title'),
            I18nString.named('title'),
            I18nString.named('description'),
            flatland.String.named('id'),
        )

_IndicatorSchemaDefinition = flatland.Dict.of(
            flatland.String.named('status'),
            flatland.String.named('classification'),
            flatland.String.named('scale'),
            flatland.String.named('other_targets'),
            flatland.String.named('goal'),
            flatland.String.named('relevant_target'),
            flatland.String.named('sources'),
            flatland.String.named('sensitivity'),
            flatland.String.named('question'),
            flatland.String.named('links'),
            flatland.String.named('validity'),
            flatland.String.named('measurer'),
            flatland.String.named('sub_indicator'),
            flatland.String.named('head_indicator'),
            flatland.String.named('ease_of_communication'),
            flatland.String.named('requirements'),
            flatland.String.named('id'),
            flatland.String.named('name'),

        )

_TargetSchemaDefinition = flatland.Dict.of(
            flatland.String.named('goal_id'),
            I18nString.named('title'),
            I18nString.named('description'),
            flatland.String.named('id'),
        )

class Goal(_GoalSchemaDefinition):

    def __init__(self, init_goal):
        goal = dict(init_goal)
        goal.pop('_id', None)
        self.set(goal)

    def flatten(self):
        return self.value

class Indicator(_IndicatorSchemaDefinition):

    def __init__(self, init_indicator):
        indicator = dict(init_indicator)
        indicator.pop('_id', None)
        self.set(indicator)

    def flatten(self):
        return self.value

class Target(_TargetSchemaDefinition):

    def __init__(self, init_target):
        target = dict(init_target)
        target.pop('_id', None)
        self.set(target)

    def flatten(self):
        return self.value

import flatland

from common import I18nString, CommonString, CommonEnum, CommonList

_GoalSchemaDefinition = flatland.Dict.of(
            CommonString.named('short_title'),
            I18nString.named('title'),
            I18nString.named('description'),
            CommonString.named('id'),
        )

_IndicatorSchemaDefinition = flatland.Dict.of(
            CommonString.named('status'),
            CommonString.named('classification'),
            CommonString.named('scale'),
            CommonString.named('other_targets'),
            CommonString.named('goal'),
            CommonString.named('relevant_target'),
            CommonString.named('sources'),
            CommonString.named('sensitivity'),
            CommonString.named('question'),
            CommonString.named('links'),
            CommonString.named('validity'),
            CommonString.named('measurer'),
            CommonString.named('sub_indicator'),
            CommonString.named('head_indicator'),
            CommonString.named('ease_of_communication'),
            CommonString.named('requirements'),
            CommonString.named('id'),
            CommonString.named('name'),

        )

_TargetSchemaDefinition = flatland.Dict.of(
            CommonString.named('goal_id'),
            I18nString.named('title'),
            I18nString.named('description'),
            CommonString.named('id'),
        )

MappingSchema = flatland.Dict.with_properties(widget="form").of(
            CommonEnum.named('objective')
                        .using(label="National Objective", optional=False)
                        .valued()
                        .with_properties(widget="select", value_labels=""),
            CommonEnum.named('goal')
                        .using(label="Strategic Goal", optional=False)
                        .valued()
                        .with_properties(widget="select", value_labels=""),
            CommonEnum.named('main_target')
                        .using(label="Relevant AICHI target", optional=False)
                        .valued()
                        .with_properties(widget="select", value_labels=""),
            CommonList.named('other_targets')
                        .of(CommonString.named('other_targets'))
                        .using(label="Other AICHI targets", optional=False)
                        .with_properties(widget="list", valid_values="", value_labels=""),
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

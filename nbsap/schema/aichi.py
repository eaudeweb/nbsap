import flatland

from common import I18nString, CommonString, CommonEnum, CommonList, ListValue,\
                   GoalEnumValue
from .refdata import goals, targets, mapping, indicator_data

_GoalSchemaDefinition = flatland.Dict.of(
            CommonString.named('short_title'),
            I18nString.named('title'),
            I18nString.named('description'),
            CommonString.named('id'),
        )

_IndicatorSchemaDefinition = flatland.Dict.of(
            I18nString.named('status')
                .with_properties(widget="edit_textarea")
                .using(label="Status of development"),
            I18nString.named('classification')
                .with_properties(widget="edit_textarea")
                .using(label="Operational Classification"),
            CommonEnum.named('scale')
                .valued(*sorted(indicator_data['scale']))
                .with_properties(widget="select")
                .using(label="Scale (global, regional, national, sub-national)"),
            CommonList.named('other_targets')
                .of(CommonString.named('other_targets'))
                .including_validators(ListValue())
                .using(label="Other Relevant Aichi Targets")
                .with_properties(widget="list",
                                 valid_values=targets.keys(),
                                 value_labels=targets,
                                 css_class="chzn-select",
                                 multiple="multiple"),
            CommonEnum.named('goal')
                .valued(*sorted(goals.keys()))
                .using(label="Strategic Goal")
                .with_properties(widget="select", value_label=goals),
            CommonEnum.named('relevant_target')
                .including_validators(GoalEnumValue())
                .valued(*sorted(targets.keys()))
                .with_properties(widget="select", value_label=targets)
                .using(label="Most Relevant Aichi Target"),
            I18nString.named('sources')
                .with_properties(widget="edit_textarea")
                .using(label="Data Sources"),
            CommonEnum.named('sensitivity')
                .valued(*sorted(indicator_data['sensitivity']))
                .with_properties(widget="select")
                .using(label="Sensitivity (can it be used to make assessment by 2015?)"),
            I18nString.named('question')
                .with_properties(widget="edit_textarea")
                .using(label="Communication Question"),
            CommonList.named('links').of(CommonString.named('links'))
                .using(label="Related Links"),
            CommonEnum.named('validity')
                .valued(*sorted(indicator_data['validity']))
                .with_properties(widget="select")
                .using(label="Scientific Validity"),
            I18nString.named('measurer')
                .with_properties(widget="edit_textarea")
                .using(label="Who's responsible for measuring?"),
            I18nString.named('sub_indicator')
                .with_properties(widget="edit_textarea")
                .using(label="Indicator Sub-topics"),
            I18nString.named('head_indicator')
                .with_properties(widget="edit_textarea")
                .using(label="Headline Indicator"),
            CommonEnum.named('ease_of_communication')
                .valued(*sorted(indicator_data['ease_of_communication']))
                .with_properties(widget="select")
                .using(label="How easy can it be communicated?"),
            I18nString.named('requirements')
                .with_properties(widget="edit_textarea")
                .using(label="Data Requirements"),
            CommonString.named('id'),
            I18nString.named('name')
                .with_properties(widget="edit_textarea")
                .using(label="Operational Indicator")

        )

_TargetSchemaDefinition = flatland.Dict.of(
            CommonString.named('goal_id'),
            I18nString.named('title'),
            I18nString.named('description'),
            CommonString.named('id'),
        )

_MappingSchema = flatland.Dict.with_properties(widget="form").of(
            CommonEnum.named('objective')
                        .using(label="National Objective", optional=False)
                        .with_properties(widget="obj_select"),
            CommonEnum.named('goal')
                        .using(label="AICHI strategic goal", optional=False)
                        .valued(*sorted(goals.keys()))
                        .with_properties(widget="select",
                            value_labels=goals,
                            css_class="span2"),
            CommonEnum.named('main_target')
                        .including_validators(GoalEnumValue())
                        .using(label="Relevant AICHI target", optional=False)
                        .valued(*sorted(targets.keys()))
                        .with_properties(widget="select",
                            mapping=mapping,
                            value_labels=targets,
                            css_class="span2"),
            CommonList.named('other_targets')
                        .of(CommonString.named('other_targets'))
                        .including_validators(ListValue())
                        .using(label="Other AICHI targets")
                        .with_properties(widget="list",
                            valid_values=targets.keys(),
                            value_labels=targets,
                            css_class="chzn-select",
                            multiple="multiple"),
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

class MappingSchema(_MappingSchema):

    def set_objectives(self, objectives):
        self['objective'].valid_values = [j for i in objectives.keys() for j in objectives[i].values()]
        self['objective'].properties['groups'] = objectives
        return self

    def flatten(self):
        return self.value


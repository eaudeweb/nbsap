import flatland
from flatland.validation import URLValidator

from common import I18nString, CommonString, CommonEnum, CommonList, ListValue,\
                   GoalEnumValue, CommonI18nString, ListElements
from .refdata import goals, targets, mapping, indicator_data

_GoalSchemaDefinition = flatland.Dict.of(
            CommonString.named('short_title'),
            I18nString.named('title')
                .using(label=u'Title'),
            I18nString.named('description')
                .using(label=u"Description"),
            CommonString.named('id'),
        )

_IndicatorSchemaDefinition = flatland.Dict.with_properties(widget="tabel").of(
            CommonString.named('id')
                .with_properties(widget="hidden"),
            CommonI18nString.named('name')
                .using(label="Operational Indicator"),
            CommonI18nString.named('question')
                .using(label="Communication Question"),
            CommonEnum.named('goal')
                .valued(*sorted(goals.keys()))
                .using(label="Strategic Goal")
                .with_properties(widget="select", value_labels=goals),
            CommonI18nString.named('head_indicator')
                .using(label="Headline Indicator"),
            CommonI18nString.named('sub_indicator')
                .using(label="Indicator Sub-topics"),
            CommonEnum.named('relevant_target')
                .including_validators(GoalEnumValue())
                .valued(*sorted(targets.keys()))
                .with_properties(widget="select", value_labels=targets, mapping=mapping)
                .using(label="Most Relevant Aichi Target"),
            CommonList.named('other_targets')
                .of(CommonString.named('other_targets'))
                .including_validators(ListValue())
                .using(label="Other Relevant Aichi Targets")
                .with_properties(widget="list",
                                 valid_values=targets.keys(),
                                 value_labels=targets,
                                 css_class="chzn-select",
                                 multiple="multiple"),
            CommonI18nString.named('classification')
                .using(label="Operational Classification"),
            CommonI18nString.named('status')
                .using(label="Status of development"),
            CommonEnum.named('sensitivity')
                .valued(*sorted(indicator_data['sensitivity']))
                .with_properties(widget="select")
                .using(label="Sensitivity (can it be used to make assessment by 2015?)"),
            CommonList.named('scale')
                .of(CommonString.named('scale'))
                .including_validators(ListValue())
                .using(label="Scale (global, regional, national, sub-national)")
                .with_properties(widget="list",
                                 valid_values=indicator_data['scale'],
                                 value_labels=indicator_data['scale'],
                                 css_class="chzn-select",
                                 multiple="multiple"),
            CommonEnum.named('validity')
                .valued(*sorted(indicator_data['validity']))
                .with_properties(widget="select")
                .using(label="Scientific Validity"),
            CommonEnum.named('ease_of_communication')
                .valued(*sorted(indicator_data['ease_of_communication']))
                .with_properties(widget="select")
                .using(label="How easy can it be communicated?"),
            CommonI18nString.named('sources')
                .using(label="Data Sources"),
            CommonI18nString.named('requirements')
                .using(label="Data Requirements"),
            CommonI18nString.named('measurer')
                .using(label="Who's responsible for measuring?"),
            CommonString.named('conventions')
                .using(label="Other conventions/processes using indicator")
                .with_properties(widget="edit_input"),
            CommonList.named('links')
                    .including_validators(ListElements())
                    .with_properties(widget='general')
                    .of(
                    flatland.Dict.named('links').with_properties(widget='general').of(
                        CommonI18nString.named('url_name')
                            .using(label="Link name"),
                        CommonString.named('url')
                            .including_validators(URLValidator())
                            .with_properties(widget="edit_input")
                            .using(label="Link URL"),
                    )
                ).using(label="Related Links")
        )

_TargetSchemaDefinition = flatland.Dict.of(
            CommonString.named('goal_id'),
            I18nString.named('title')
                .using(label=u'Title'),
            I18nString.named('description')
                .using(label=u'Description'),
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


import flatland
from flaskext.babel import gettext as _

from common import I18nString, CommonString, CommonEnum, CommonList, ListValue,\
                   GoalEnumValue, CommonI18nString, CommonInteger, EnumValue, \
                   RuntimeCommonEnum, RuntimeCommonList, RuntimeListValue, \
                   RuntimeEnumValue
from .refdata import goals, targets, mapping, indicator_data

_GoalSchemaDefinition = flatland.Dict.of(
            CommonString.named('short_title'),
            I18nString.named('title')
                .using(label=_(u'Title')),
            I18nString.named('description')
                .using(label=_(u"Description")),
            CommonString.named('id'),
        )

_IndicatorSchemaDefinition = flatland.Dict.with_properties(widget="tabel_form").of(
            CommonInteger.named('id')
                .with_properties(widget="hidden"),
            CommonI18nString.named('name')
                .using(label=_("Operational Indicator")),
            CommonI18nString.named('question')
                .using(label=_("Communication Question")),
            CommonEnum.named('goal')
                .valued(*sorted(goals.keys()))
                .using(label=_("Strategic Goal"))
                .with_properties(widget="select", value_labels=goals),
            CommonI18nString.named('head_indicator')
                .using(label=_("Headline Indicator")),
            CommonI18nString.named('sub_indicator')
                .using(label=_("Indicator Sub-topics")),
            CommonEnum.named('relevant_target')
                .including_validators(GoalEnumValue())
                .valued(*sorted(targets.keys()))
                .with_properties(widget="select", value_labels=targets, mapping=mapping)
                .using(label=_("Most Relevant Aichi Target")),
            CommonList.named('other_targets')
                .of(CommonString.named('other_targets'))
                .including_validators(ListValue())
                .using(label=_("Other Relevant Aichi Targets"))
                .with_properties(widget="list",
                                 valid_values=targets.keys(),
                                 value_labels=targets,
                                 css_class="chzn-select",
                                 multiple="multiple"),
            CommonI18nString.named('classification')
                .using(label=_("Operational Classification")),
            CommonI18nString.named('status')
                .with_properties(field_widget='edit_textarea')
                .using(label=_("Status of development")),
            CommonEnum.named('sensitivity')
                .including_validators(EnumValue())
                .valued(*sorted(indicator_data['sensitivity'].keys()))
                .with_properties(widget="select", value_labels=indicator_data['sensitivity'])
                .using(label=_("Sensitivity (can it be used to make assessment by 2015?)")),
            CommonList.named('scale')
                .of(CommonString.named('scale'))
                .including_validators(ListValue())
                .using(label=_("Scale (global, regional, national, sub-national)"))
                .with_properties(widget="list",
                                 valid_values=indicator_data['scale'].keys(),
                                 value_labels=indicator_data['scale'],
                                 css_class="chzn-select",
                                 multiple="multiple"),
            CommonEnum.named('validity')
                .including_validators(EnumValue())
                .valued(*sorted(indicator_data['validity'].keys()))
                .with_properties(widget="select", value_labels=indicator_data['validity'])
                .using(label=_("Scientific Validity")),
            CommonEnum.named('ease_of_communication')
                .valued(*sorted(indicator_data['ease_of_communication'].keys()))
                .including_validators(EnumValue())
                .with_properties(widget="select",
                        value_labels=indicator_data['ease_of_communication'])
                .using(label=_("How easy can it be communicated?")),
            CommonI18nString.named('sources')
                .using(label=_("Data Sources")),
            CommonI18nString.named('requirements')
                .with_properties(field_widget='edit_textarea')
                .using(label=_("Data Requirements")),
            CommonI18nString.named('measurer')
                .with_properties(field_widget='edit_textarea')
                .using(label=_("Who's responsible for measuring?")),
            CommonString.named('conventions')
                .using(label=_("Other conventions/processes using indicator"))
                .with_properties(widget="edit_input"),
            CommonList.named('links')
                    .with_properties(widget='general_pairs')
                    .of(
                    flatland.Dict.named('links').with_properties(widget='general').of(
                        CommonI18nString.named('url_name')
                            .using(label=_("Link name")),
                        CommonString.named('url')
                            .with_properties(widget="edit_input")
                            .using(label=_("Link URL")),
                    )
                ).using(label=_("Related Links"))
        )

_TargetSchemaDefinition = flatland.Dict.of(
            CommonString.named('goal_id'),
            I18nString.named('title')
                .using(label=_(u'Title')),
            I18nString.named('description')
                .using(label=_(u'Description')),
            CommonString.named('id'),
        )

_MappingSchema = flatland.Dict.with_properties(widget="form").of(
            CommonString.named('_id')
                .with_properties(widget="hidden"),
            CommonEnum.named('objective')
                        .using(label=_("National Objective"), optional=False)
                        .with_properties(widget="obj_select"),
            CommonEnum.named('goal')
                        .using(label=_("AICHI strategic goal"), optional=False)
                        .valued(*sorted(goals.keys()))
                        .with_properties(widget="select",
                            value_labels=goals,
                            css_class="span2"),
            CommonEnum.named('main_target')
                        .including_validators(GoalEnumValue())
                        .using(label=_("Relevant AICHI target"), optional=False)
                        .valued(*sorted(targets.keys()))
                        .with_properties(widget="select",
                            mapping=mapping,
                            value_labels=targets,
                            css_class="span2"),
            CommonList.named('other_targets')
                        .of(CommonString.named('other_targets'))
                        .including_validators(ListValue())
                        .using(label=_("Other AICHI targets"))
                        .with_properties(widget="list",
                            valid_values=targets.keys(),
                            value_labels=targets,
                            css_class="chzn-select",
                            multiple="multiple"),
            RuntimeCommonEnum.named('main_eu_target')
                        .validated_by(RuntimeEnumValue())
                        .using(label=_("EU strategic target"), optional=False)
                        .with_properties(widget="select",
                            css_class="span2"),
            RuntimeCommonList.named('eu_actions')
                        .of(CommonString.named('eu_actions'))
                        .including_validators(RuntimeListValue())
                        .using(label=_("EU related actions"))
                        .with_properties(widget="list",
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
        self['objective'].valid_values = []

        for id in objectives.keys():
            self['objective'].valid_values.extend(objectives[id])

        self['objective'].properties['groups'] = objectives
        return self

    def flatten(self):
        return self.value


import flatland

I18nString = flatland.Dict.of(
            flatland.String.named("en"),
            flatland.String.named("fr"),
            flatland.String.named("nl"),
        )

_GoalSchemaDefinition = flatland.Dict.of(
            flatland.String.named('short_title'),
            I18nString.named('title'),
            I18nString.named('description'),
            flatland.String.named('id'),
        )

class GoalSchema(_GoalSchemaDefinition):

    @property
    def value(self):
        return super(GoalSchema, self).value

    def flatten(self):
        return self.value

class Goal(dict):

    @staticmethod
    def from_flat(init_goal):
        goal = GoalSchema.from_flat(init_goal)
        goal['description'] = I18nString.from_flat(init_goal['description'])
        goal['title'] = I18nString.from_flat(init_goal['title'])

        return goal


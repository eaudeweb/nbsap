import flatland

CommonString = flatland.String.using(optional=True)
CommonList = flatland.List.using(optional=True)

I18nString = flatland.Dict.of(
            CommonString.named("en"),
            CommonString.named("fr"),
            CommonString.named("nl"),
        )


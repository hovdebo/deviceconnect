from ._intraday_activity import ActivityIntraday


class CaloriesIntraday(ActivityIntraday):
    ACTIVITY_TYPE = "calories"

    def __init__(self, json_dict):
        super().__init__(json_dict)

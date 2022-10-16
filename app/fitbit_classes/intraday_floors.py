from ._intraday_activity import ActivityIntraday


class FloorsIntraday(ActivityIntraday):
    ACTIVITY_TYPE = "floors"

    def __init__(self, json_dict):
        super().__init__(json_dict)

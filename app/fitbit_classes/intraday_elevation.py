from ._intraday_activity import ActivityIntraday


class ElevationIntraday(ActivityIntraday):
    ACTIVITY_TYPE = "elevation"

    def __init__(self, json_dict):
        super().__init__(json_dict)

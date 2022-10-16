from ._intraday_activity import ActivityIntraday


class DistanceIntraday(ActivityIntraday):
    ACTIVITY_TYPE = "distance"

    def __init__(self, json_dict):
        super().__init__(json_dict)


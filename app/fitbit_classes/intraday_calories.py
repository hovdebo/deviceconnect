from ._intraday_activity import IntradayActivity


class IntradayCalories(IntradayActivity):
    def __init__(self, json_dict):
        super().__init__(json_dict, "calories")

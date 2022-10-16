import pandas as pd
from . util import normalize
from . _base import FitbitSummary, FitbitIntraday


class ActivitySummary(FitbitSummary):
    def __init__(self, json_dict, activity_type):
        super().__init__(json_dict)

        activities = self.json[f"activities-{activity_type}"]
        if len(activities) > 1:
            raise RuntimeError(f"More than one date specified in {self.json}")
        activities = activities[0]

        self._date = activities["dateTime"]
        self._df = pd.DataFrame([activities["value"]], columns=[activity_type])
        self._df = normalize(self._df, self._date, "00:00:00")

    @classmethod
    def url(cls, user, date):
        pass


class ActivityIntraday(FitbitIntraday):
    ACTIVITY_TYPE = "BASE"

    def __init__(self, json_dict):
        super().__init__(json_dict)

        self._summary = ActivitySummary(json_dict, self.ACTIVITY_TYPE)
        activities_intraday = json_dict[f"activities-{self.ACTIVITY_TYPE}-intraday"]
        self._df = pd.json_normalize(activities_intraday, "dataset")
        self._df = normalize(self._df, self._summary.date, self._df["time"])
        self._df.rename(columns={"value": self.ACTIVITY_TYPE}, inplace=True)

    @classmethod
    def url(cls, user, date, resolution="1min"):
        return_val = f"/1/user/{user}/activities/{cls.ACTIVITY_TYPE}/date/{date}/1d/{resolution}.json"
        return return_val


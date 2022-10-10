import pandas as pd
from . util import normalize


class IntradayActivity:
    def __init__(self, json_dict, activity_type):
        self.date = None

        activities = json_dict[f"activities-{activity_type}"]
        if len(activities) > 1:
            raise RuntimeError(f"More than one date specified in {json_dict}")
        activities = activities[0]
        date = activities["dateTime"]
        total = activities["value"]

        activities_intraday = json_dict[f"activities-{activity_type}-intraday"]
        self.df = pd.json_normalize(activities_intraday, "dataset")
        self.df = normalize(self.df, date, self.df["time"])
        self.df.rename(columns={"value": activity_type}, inplace=True)

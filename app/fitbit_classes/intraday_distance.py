import pandas as pd
from . util import normalize


class IntradayDistance:
    def __init__(self, json_dict):
        self.date = None

        activities = json_dict["activities-distance"]
        if len(activities) > 1:
            raise RuntimeError(f"More than one date specified in {json_dict}")
        activities = activities[0]
        date = activities["dateTime"]
        total = activities["value"]

        activities_intraday = json_dict["activities-distance-intraday"]
        self.activities_df = pd.json_normalize(activities_intraday, "dataset")
        self.activities_df = normalize(self.activities_df, date, self.activities_df["time"])
        self.activities_df.rename(columns={"value": "distance"}, inplace=True)

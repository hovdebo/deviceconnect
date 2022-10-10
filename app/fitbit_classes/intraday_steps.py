import pandas as pd
from . util import normalize


class IntradaySteps:
    def __init__(self, json_dict):
        self.date = None

        activities = json_dict["activities-steps"]
        if len(activities) > 1:
            raise RuntimeError(f"More than one date specified in {json_dict}")
        activities = activities[0]
        date = activities["dateTime"]
        total = activities["value"]

        activities_intraday = json_dict["activities-steps-intraday"]
        self.df = pd.json_normalize(activities_intraday, "dataset")
        self.df = normalize(self.df, date, self.df["time"])
        self.df.rename(columns={"value": "steps"}, inplace=True)


if __name__ == "__main__":
    json_dict = {
        "activities-steps": [
            {
                "dateTime": "2019-01-01",
                "value": "0"
            }
        ],
        "activities-steps-intraday": {
            "dataset": [
                {
                    "time": "08:00:00",
                    "value": 0
                },
                {
                    "time": "08:01:00",
                    "value": 0
                },
                {
                    "time": "08:02:00",
                    "value": 0
                },
                {
                    "time": "08:30:00",
                    "value": 0
                }
            ],
            "datasetInterval": 1,
            "datasetType": "minute"
        }
    }

    activities = IntradaySteps(json_dict)
    print(activities.df)
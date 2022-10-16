import pandas as pd
from . _base import FitbitSummary, FitbitIntraday


class Spo2Summary(FitbitSummary):
    def __init__(self, json_dict):
        super().__init__(json_dict)

        self._date = json_dict['dateTime']
        self._df = pd.DataFrame([pd.to_datetime(self._date)], columns=["time"])

    @classmethod
    def url(cls, user, date):
        pass


class Spo2Intraday(FitbitIntraday):
    def __init__(self, json_dict):
        super().__init__(json_dict)

        self._summary = Spo2Summary(json_dict)

        minutes = json_dict['minutes']
        self._df = pd.json_normalize(minutes, None, ["value", "minute"])
        self._df["minute"] = pd.to_datetime(self._df["minute"])
        self._df.rename(columns={"minute": "time", "value": "spo2"}, inplace=True)

    @classmethod
    def url(cls, user, date):
        return_val = f"/1/user/{user}/spo2/date/{date}/all.json"
        return return_val


if __name__ == "__main__":
    json_dict = {
        "dateTime": "2021-10-04",
        "minutes": [
            {
                "value": 95.7,
                "minute": "2021-10-04T04:02:17"
            },
            {
                "value": 99.5,
                "minute": "2021-10-04T04:03:17"
            },
            {
                "value": 99.0,
                "minute": "2021-10-04T04:04:17"
            },
        ]
    }

    spo2 = Spo2Intraday(json_dict)
    print(spo2.dataframe)
    print(spo2.summary.dataframe)

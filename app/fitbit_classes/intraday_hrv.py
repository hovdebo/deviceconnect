import pandas as pd
from . _base import FitbitSummary, FitbitIntraday


class HrvSummary(FitbitSummary):
    def __init__(self, json_dict):
        super().__init__(json_dict)

        hrv = json_dict["hrv"]
        if len(hrv) > 1:
            raise RuntimeError(f"More than one date specified in {json_dict}")
        hrv = hrv[0]
        self._date = hrv['dateTime']
        self._df = pd.DataFrame([pd.to_datetime(self._date)], columns=["time"])

    @classmethod
    def url(cls, user, date):
        pass


class HrvIntraday(FitbitIntraday):
    def __init__(self, json_dict):
        super().__init__(json_dict)

        self._summary = HrvSummary(json_dict)

        hrv = json_dict["hrv"]
        if len(hrv) > 1:
            raise RuntimeError(f"More than one date specified in {json_dict}")
        hrv = hrv[0]
        minutes = hrv['minutes']
        self._df = pd.json_normalize(minutes, None, ["value", "minute"])
        self._df["minute"] = pd.to_datetime(self._df["minute"])
        self._df.rename(columns={"minute": "time"}, inplace=True)
        new_column_names = {old_name: old_name.split("value.")[1] for old_name in self._df.columns if len(old_name.split("value.")) ==2 }
        self._df.rename(columns=new_column_names, inplace=True)

    @classmethod
    def url(cls, user, date):
        return_val = f"/1/user/{user}/hrv/date/{date}/all.json"
        return return_val


if __name__ == "__main__":
    json_dict = {
        "hrv": [
            {
                "minutes": [
                    {
                        "minute": "2021-10-25T09:10:00.000",
                        "value": {
                            "rmssd": 26.617,
                            "coverage": 0.935,
                            "hf": 126.514,
                            "lf": 471.897
                        }
                    },
                    {
                        "minute": "2021-10-25T09:15:00.000",
                        "value": {
                            "rmssd": 34.845,
                            "coverage": 0.988,
                            "hf": 344.342,
                            "lf": 1422.947
                        }
                    },
                    {
                        "minute": "2021-10-25T09:20:00.000",
                        "value": {
                            "rmssd": 36.893,
                            "coverage": 0.981,
                            "hf": 328.704,
                            "lf": 298.071
                        }
                    },
                    {
                        "minute": "2021-10-25T09:25:00.000",
                        "value": {
                            "rmssd": 65.946,
                            "coverage": 0.972,
                            "hf": 1088.794,
                            "lf": 979.685
                        }
                    },
                ],
                "dateTime": "2021-10-25"
            }
        ]
    }

    hrv = HrvIntraday(json_dict)
    print(hrv.dataframe)
    print(hrv.summary.dataframe)

import pandas as pd
from . util import normalize
from . _base import FitbitSummary, FitbitIntraday


class HeartRateSummary(FitbitSummary):
    def __init__(self, json_dict):
        super().__init__(json_dict)
        self._date = None
        self._df = None
        self._resting_heart_rate = None

        activities_heart = json_dict["activities-heart"]
        if len(activities_heart) > 1:
            raise RuntimeError(f"More than one date specified in {self.json}")
        activities_heart = activities_heart[0]
        self._date = activities_heart["dateTime"]

        zones = activities_heart["value"]
        self._resting_heart_rate = zones["restingHeartRate"]

        custom_zones_df = pd.json_normalize(zones["customHeartRateZones"])
        custom_zones_df = normalize(custom_zones_df, self._date, "00:00:00")

        zones_df = pd.json_normalize(zones["heartRateZones"])
        zones_df = normalize(zones_df, self._date, "00:00:00")
        self._df = pd.concat([custom_zones_df, zones_df], ignore_index=True)

    @property
    def url(self, user, date, period='1d'):
        return_val = "1/user/{user}/activities/heart/date/{date}/{period}.json".format(user=user,
                                                                                       date=date,
                                                                                       period=period)
        return return_val


class HeartRateIntraday(FitbitIntraday):
    def __init__(self, json_dict):
        super().__init__(json_dict)
        self._summary = HeartRateSummary(json_dict)

        activities_heart_intraday = json_dict["activities-heart-intraday"]
        heart_rate_intraday = activities_heart_intraday["dataset"]
        heart_rate_intraday_df = pd.json_normalize(heart_rate_intraday)
        self._df = normalize(heart_rate_intraday_df, self._summary.date, heart_rate_intraday_df["time"])
        self._df.rename(columns={"value": "heart_rate"}, inplace=True)
        self._df["dataset_interval"] = activities_heart_intraday["datasetInterval"]
        self._df["dataset_type"] = activities_heart_intraday["datasetType"]

    @classmethod
    def url(cls, user, date, resolution="1d"):
        return_val = "1.2/user/{user}/activities/heart/date/{date}/{resolution}.json".format(user=user,
                                                                                             date=date,
                                                                                             resolution=resolution)
        return return_val


if __name__ == "__main__":
    json_dict = {
      "activities-heart": [
        {
          "dateTime": "2019-05-08",
          "value": {
            "customHeartRateZones": [
              {
                "caloriesOut": 1164.09312,
                "max": 90,
                "min": 30,
                "minutes": 718,
                "name": "Below"
              },
              {
                "caloriesOut": 203.65344,
                "max": 110,
                "min": 90,
                "minutes": 74,
                "name": "Custom Zone"
              },
              {
                "caloriesOut": 330.76224,
                "max": 220,
                "min": 110,
                "minutes": 42,
                "name": "Above"
              }
            ],
            "heartRateZones": [
              {
                "caloriesOut": 979.43616,
                "max": 86,
                "min": 30,
                "minutes": 626,
                "name": "Out of Range"
              },
              {
                "caloriesOut": 514.16208,
                "max": 121,
                "min": 86,
                "minutes": 185,
                "name": "Fat Burn"
              },
              {
                "caloriesOut": 197.92656,
                "max": 147,
                "min": 121,
                "minutes": 18,
                "name": "Cardio"
              },
              {
                "caloriesOut": 6.984,
                "max": 220,
                "min": 147,
                "minutes": 5,
                "name": "Peak"
              }
            ],
            "restingHeartRate": 76
          }
        }
      ],
      "activities-heart-intraday": {
        "dataset": [
          {
            "time": "00:00:00",
            "value": 78
          },
          {
            "time": "00:01:00",
            "value": 78
          },
          {
            "time": "00:02:00",
            "value": 77
          },
          {
            "time": "00:03:00",
            "value": 77
          },
          {
            "time": "00:04:00",
            "value": 77
          }
        ],
        "datasetInterval": 1,
        "datasetType": "minute"
      }
    }
    intraday = HeartRateIntraday(json_dict)
    print(intraday.dataframe)
    print(intraday.summary.dataframe)

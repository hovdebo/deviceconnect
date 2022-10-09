import datetime
import pandas as pd
from skimpy import clean_columns


def normalize(df, date, time):
    df["time"] = pd.to_datetime(date + " " + time)
    df = clean_columns(df)
    return df


class IntradayHeartRate:
    def __init__(self, json_dict):
        self.zones_df = None
        self.heart_rate_df = None
        self.resting_heart_rate = None
        self.dataset_interval = None
        self.dataset_type = None

        activities_heart = json_dict["activities-heart"]
        if len(activities_heart) > 1:
            raise RuntimeError(f"More than one date specified in {json_dict}")
        activities_heart = activities_heart[0]
        date = activities_heart["dateTime"]
        zones = activities_heart["value"]

        custom_zones_df = pd.json_normalize(zones["customHeartRateZones"])
        custom_zones_df = normalize(custom_zones_df, date, "00:00:00")

        zones_df = pd.json_normalize(zones["heartRateZones"])
        self.zones_df = normalize(zones_df, date, "00:00:00")
        self.zones_df = pd.concat([custom_zones_df, self.zones_df])

        self.resting_heart_rate = zones["restingHeartRate"]

        activities_heart_intraday = json_dict["activities-heart-intraday"]
        heart_rate_intraday = activities_heart_intraday["dataset"]
        heart_rate_intraday_df = pd.json_normalize(heart_rate_intraday)
        self.heart_rate_df = normalize(heart_rate_intraday_df, date, heart_rate_intraday_df["time"])
        self.heart_rate_df.rename(columns={"value": "heart_rate"}, inplace=True)
        self.dataset_interval = activities_heart_intraday["datasetInterval"]
        self.dataset_type = activities_heart_intraday["datasetType"]


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
    intraday = IntradayHeartRate(json_dict)
    print(intraday.zones_df)
  #  print(intraday.heart_rate)
  #  for heart_rate in intraday.heart_rate:
  #      print(heart_rate.date_time, heart_rate.heart_rate)
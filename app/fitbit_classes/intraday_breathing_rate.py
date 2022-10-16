import pandas as pd
from .util import normalize
from ._base import FitbitSummary, FitbitIntraday


class BreathingRateSummary(FitbitSummary):
    def __init__(self, json_dict):
        super().__init__(json_dict)

        br = json_dict["br"]
        if len(br) > 1:
            raise RuntimeError(f"More than one date specified in {json_dict}")
        br = br[0]
        value = br["value"]
        self._date = br['dateTime']
        self._df = pd.DataFrame([pd.to_datetime(self._date)], columns=["time"])

    @classmethod
    def url(cls, user, date):
        pass


class BreathingRateIntraday(FitbitIntraday):
    def __init__(self, json_dict):
        super().__init__(json_dict)

        br = json_dict["br"]
        if len(br) > 1:
            raise RuntimeError(f"More than one date specified in {json_dict}")
        br = br[0]
        values = br["value"]

        # The summary for an intraday call is a bit different than that for an actual summary call.  So fake a summary
        # call
        faked_json_dict = {
            "br": [
                {
                    "value": {
                        "breathingRate": values["fullSleepSummary"]["breathingRate"]
                    },
                    "dateTime": br["dateTime"]
                }
            ]
        }
        self._summary = BreathingRateSummary(faked_json_dict)

        self._df = pd.json_normalize(values, meta="breathingRate")
        self._df = pd.melt(self._df, var_name="stage")
        self._df.replace(to_replace={
            "deepSleepSummary.breathingRate": "deep",
            "remSleepSummary.breathingRate": "rem",
            "fullSleepSummary.breathingRate": "full",
            "lightSleepSummary.breathingRate": "light"}, inplace=True)
        self._df.rename(columns={"value": "rate"}, inplace=True)
        self._df = normalize(self._df, self._summary.date, "00:00:00")

    @classmethod
    def url(cls, user, date, resolution="1d"):
        return_val = "1/user/{user}/br/date/{date}.json".format(user=user,
                                                                date=date)
        return return_val


if __name__ == "__main__":
    json_dict = {
      "br": [
        {
          "value": {
            "deepSleepSummary": {
              "breathingRate": 16.8
            },
            "remSleepSummary": {
              "breathingRate": -1
            },
            "fullSleepSummary": {
              "breathingRate": 17.8
            },
            "lightSleepSummary": {
              "breathingRate": 16.8
            }
          },
          "dateTime": "2021-10-25"
        }
      ]
    }

    br = BreathingRateIntraday(json_dict)
    print(br.dataframe)
    print(br.summary.dataframe)

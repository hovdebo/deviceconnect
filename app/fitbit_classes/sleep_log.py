import pandas as pd
from skimpy import clean_columns
from .util import normalize
from ._base import FitbitSummary, FitbitIntraday


class SleepSummary(FitbitSummary):

    def __init__(self, json_dict):
        super().__init__(json_dict)

        sleep = json_dict["sleep"]
        if len(sleep) > 1:
            raise RuntimeError(f"More than one date specified in {json_dict}")
        sleep = sleep[0]
        self._date = sleep["dateOfSleep"]

        summary = json_dict["summary"]

        df = pd.json_normalize(summary)
        df.rename(columns={
            "stages.deep": "deep_minutes",
            "stages.light": "light_minutes",
            "stages.rem": "rem_minutes",
            "stages.wake": "wake_minutes"
        }, inplace=True)
        self._df = normalize(df, self._date, "00:00:00")

    @classmethod
    def url(cls, user, date):
        pass


class SleepLog(FitbitIntraday):

    LEVELS = [
        "deep",
        "light",
        "rem",
        "wake"
    ]

    META_COLS = [
        "dateOfSleep",
        "duration",
        "efficiency",
        "endTime",
        "infoCode",
        "isMainSleep",
        "logId",
        "minutesAfterWakeup",
        "minutesAsleep",
        "minutesAwake",
        "minutesToFallAsleep",
        "logType",
        "startTime",
        "timeInBed",
        "type"
    ]

    def __init__(self, json_dict):
        super().__init__(json_dict)

        self._summary = SleepSummary(json_dict)

        sleeps = json_dict["sleep"]

        meta_dfs = []
        stage_dfs = []
        for sleep in sleeps:
            meta_dict = {key: sleep[key] for key in self.META_COLS}
            meta_df = clean_columns(pd.json_normalize(meta_dict))
            meta_df["end_time"] = pd.to_datetime(meta_df["end_time"])
            meta_df["start_time"] = pd.to_datetime(meta_df["start_time"])

            summary_df = pd.json_normalize(sleep["levels"]["summary"])
            summary_df = clean_columns(summary_df)
            meta_df = meta_df.join(summary_df)
            meta_dfs.append(meta_df)

            stage_df = pd.json_normalize(sleep, record_path=["levels", "data"])
            stage_df["log_id"] = meta_df["log_id"].iloc[0]
            stage_df.rename(columns={"dateTime": "time"}, inplace=True)
            stage_df["time"] = pd.to_datetime(stage_df["time"])
            stage_dfs.append(stage_df)

        self._meta_df = pd.concat(meta_dfs)
        self._df = pd.concat(stage_dfs)

    @property
    def meta_dataframe(self):
        return self._meta_df

    @staticmethod
    def url(user, date):
        return_val = "/1.2/user/{user}/sleep/date/{date}.json".format(user=user,
                                                                      date=date)
        return return_val


if __name__ == "__main__":
    json_dict = {
        "sleep": [
            {
                "dateOfSleep": "2020-02-21",
                "duration": 27720000,
                "efficiency": 96,
                "endTime": "2020-02-21T07:03:30.000",
                "infoCode": 0,
                "isMainSleep": True,
                "levels": {
                    "data": [
                        {
                            "dateTime": "2020-02-20T23:21:30.000",
                            "level": "wake",
                            "seconds": 630
                        },
                        {
                            "dateTime": "2020-02-20T23:32:00.000",
                            "level": "light",
                            "seconds": 30
                        },
                        {
                            "dateTime": "2020-02-20T23:32:30.000",
                            "level": "deep",
                            "seconds": 870
                        },
                        {
                            "dateTime": "2020-02-21T06:32:30.000",
                            "level": "light",
                            "seconds": 1860
                        }
                    ],
                    "shortData": [
                        {
                            "dateTime": "2020-02-21T00:10:30.000",
                            "level": "wake",
                            "seconds": 30
                        },
                        {
                            "dateTime": "2020-02-21T00:15:00.000",
                            "level": "wake",
                            "seconds": 30
                        },
                        {
                            "dateTime": "2020-02-21T06:18:00.000",
                            "level": "wake",
                            "seconds": 60
                        }
                    ],
                    "summary": {
                        "deep": {
                            "count": 5,
                            "minutes": 104,
                            "thirtyDayAvgMinutes": 69
                        },
                        "light": {
                            "count": 32,
                            "minutes": 205,
                            "thirtyDayAvgMinutes": 202
                        },
                        "rem": {
                            "count": 11,
                            "minutes": 75,
                            "thirtyDayAvgMinutes": 87
                        },
                        "wake": {
                            "count": 30,
                            "minutes": 78,
                            "thirtyDayAvgMinutes": 55
                        }
                    }
                },
                "logId": 26013218219,
                "minutesAfterWakeup": 0,
                "minutesAsleep": 384,
                "minutesAwake": 78,
                "minutesToFallAsleep": 0,
                "logType": "auto_detected",
                "startTime": "2020-02-20T23:21:30.000",
                "timeInBed": 462,
                "type": "stages"
            }
        ],
        "summary": {
            "stages": {
                "deep": 104,
                "light": 205,
                "rem": 75,
                "wake": 78
            },
            "totalMinutesAsleep": 384,
            "totalSleepRecords": 1,
            "totalTimeInBed": 462
        }
    }

    #sleep = SleepLog(json_dict)
    #print(sleep.meta_df)
    #print(sleep.stage_df)

    log = SleepLog(json_dict)
    print(log.meta_dataframe)
    print(log.dataframe)
    print(log.summary.dataframe)

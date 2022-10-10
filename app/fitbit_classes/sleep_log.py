from dateutil import parser
import pandas as pd
from skimpy import clean_columns

class SleepLog:

    LEVELS = [
        "deep",
        "light",
        "rem",
        "wake"
    ]

    def __init__(self, json_dict):

        sleeps = json_dict["sleep"]
        meta_cols = [
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

        meta_dfs = []
        stage_dfs = []
        for sleep in sleeps:
            meta_dict = {key: sleep[key] for key in meta_cols}
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

        self.meta_df = pd.concat(meta_dfs)
        self.stage_df = pd.concat(stage_dfs)
        for column in self.meta_df.columns:
            print(column, self.meta_df[column].iloc[0])

        #print(self.meta_df)
        #print(self.stage_df)
        #all = pd.json_normalize(sleeps, record_path=["levels", "data"], meta=meta_cols)

        #print(all)
        # for sleep in sleeps:
        #     date = sleep["dateOfSleep"]
        #     duration = sleep["duration"]
        #     efficiency = sleep["efficiency"]
        #     end_time = parser.parse(sleep["endTime"])
        #     info_code = sleep["infoCode"]
        #     is_main_sleep = sleep["isMainSleep"]
        #     log_id = sleep["logId"]
        #     minutes_after_wakeup = sleep["minutesAfterWakeup"]
        #     minutes_asleep = sleep["minutesAsleep"]
        #     minutes_awake = sleep["minutesAwake"]
        #     minutes_to_fall_asleep = sleep["minutesToFallAsleep"]
        #     log_type = sleep["logType"]
        #     start_time = parser.parse(sleep["startTime"])
        #     time_in_bed = sleep["timeInBed"]
        #     type = sleep["type"]
        #
        # levels = sleep["levels"]
        # data_df = pd.json_normalize(levels["data"])
        # self.data_df.rename(columns={"dateTime": "time"}, inplace=True)
        # data_df["time"] = pd.to_datetime(self.data_df["time"])
        #
        # short_data_df = None
        # if self.type == "stages":
        #     short_data_df = pd.json_normalize(levels["shortData"])
        #     self.short_data_df.rename(columns={"dateTime": "time"}, inplace=True)
        #     short_data_df["time"] = pd.to_datetime(self.short_data_df["time"])
        #
        # summary = levels["summary"]
        # summary_df = pd.DataFrame(summary).transpose()
        # summary_df["time"] = pd.to_datetime(self.date)
        # summary_df.index.name = "stage"
        # self.summary_df.reset_index(inplace=True)
        #
        # print(self.summary_df)
        # print(self.short_data_df)
        # print(self.data_df)


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

    sleep = SleepLog(json_dict)
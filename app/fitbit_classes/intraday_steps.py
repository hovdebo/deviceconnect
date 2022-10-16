from ._intraday_activity import ActivityIntraday


class StepsIntraday(ActivityIntraday):
    ACTIVITY_TYPE = "steps"

    def __init__(self, json_dict):
        super().__init__(json_dict)


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

    activities = StepsIntraday(json_dict)
    print(activities.dataframe)
    print(activities.summary.dataframe)
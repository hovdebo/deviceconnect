import pandas as pd


class IntradayHrv:
    def __init__(self, json_dict):
        self.hrv_df = None

        hrv = json_dict["hrv"]
        if len(hrv) > 1:
            raise RuntimeError(f"More than one date specified in {json_dict}")
        hrv = hrv[0]
        minutes = hrv['minutes']
        hrv_df = pd.json_normalize(minutes, None, ["value", "minute"])
        hrv_df["minute"] = pd.to_datetime(hrv_df["minute"])
        hrv_df.rename(columns={"minute": "time"}, inplace=True)
        new_column_names = {old_name: old_name.split("value.")[1] for old_name in hrv_df.columns if len(old_name.split("value.")) ==2 }
        hrv_df.rename(columns=new_column_names, inplace=True)
        self.hrv_df = hrv_df


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

    hrv = IntradayHrv(json_dict)
    print(hrv.hrv_df)


import pandas as pd


class IntradaySpo2:
    def __init__(self, json_dict):
        self.spo2_df = None

        minutes = json_dict['minutes']
        df = pd.json_normalize(minutes, None, ["value", "minute"])
        df["minute"] = pd.to_datetime(df["minute"])
        df.rename(columns={"minute": "time", "value": "spo2"}, inplace=True)
        self.spo2_df = df


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

    hrv = IntradaySpo2(json_dict)
    print(hrv.spo2_df)

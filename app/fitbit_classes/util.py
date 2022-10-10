import pandas as pd
from skimpy import clean_columns

def normalize(df, date, time):
    df["time"] = pd.to_datetime(date + " " + time)
    df = clean_columns(df)
    return df

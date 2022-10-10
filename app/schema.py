

ZONE_TABLE = ""
ZONE_SCHEMA = [
    {
        "name": "id",
        "type": "STRING",
        "description": "Primary Key",
    },
    {
        "name": "calories_out",
        "type": "FLOAT",
        "description": "Number of calories burned while in zone"
    },
    {
        "name": "max",
        "type": "INTEGER",
        "description": "Maximum heart rate while in zone"
    },
    {
        "name": "min",
        "type": "INTEGER",
        "description": "Minimum heart rate while in zone"
    },
    {
        "name": "minutes",
        "type": "INTEGER",
        "description": "Minutes in zone"
    },
    {
        "name": "name",
        "type": "STRING",
        "time": "Timestamp for day recorded"
    }
]

HEART_RATE_TABLE = "heart_rate"
HEART_RATE_SCHEMA = [
    {
        "name": "id",
        "type": "STRING",
        "description": "User id, Primary Key",
    },
    {
        "name": "time",
        "type": "TIMESTAMP",
        "description": "Timestamp of the data"
    },
    {
        "name": "heart_rate",
        "type": "INTEGER",
        "description": "Recorded heart rate"
    },
]

HRV_TABLE = "hrv"
HRV_SCHEMA = [
    {
        "name": "id",
        "type": "STRING",
        "description": "User id, Primary Key",
    },
    {
        "name": "time",
        "type": "TIMESTAMP",
        "description": "Timestamp of the data"
    },
    {
        "name": "rmmsd",
        "type": "FLOAT",
        "description": "The Root Mean Square of Successive Differences (RMSSD) between heart beats. It measures "
                       "short-term variability in the user’s heart rate in milliseconds (ms)."
    },
    {
        "name": "coverage",
        "type": "FLOAT",
        "description": "Data completeness in terms of the number of interbeat intervals."
    },
    {
        "name": "hf",
        "type": "FLOAT",
        "description": "The power in interbeat interval fluctuations within the high frequency band (0.15 Hz - 0.4 Hz)."
    },
    {
        "name": "lf",
        "type": "FLOAT",
        "description": "The power in interbeat interval fluctuations within the low frequency band (0.04 Hz - 0.15 Hz)."
    },
]

SLEEP_STAGES_TABLE = "sleep_stages"
SLEEP_STAGES_SCHEMA = [
    {
        "name": "id",
        "type": "STRING",
        "description": "User id, Primary Key",
    },
    {
        "name": "time",
        "type": "TIMESTAMP",
        "description": "Timestamp of when the stage started."
    },
    {
        "name": "level",
        "type": "STRING",
        "description": "Name of the stage"
    },
    {
        "name": "seconds",
        "type": "INTEGER",
        "description": "Seconds spent in stage",
    },
    {
        "name": "log_id",
        "type": "INTEGER",
        "description": "Id of the record, foreign key"
    }
]

SLEEP_RECORDS_TABLE = "sleep"
SLEEP_RECORDS_SCHEMA = [
    {
        "name": "id",
        "type": "STRING",
        "description": "User id, Primary Key",
    },
    #{
    #    "name": "date_of_sleep",
    #    "type": "DATE",
    #    "description": "Date at which the sleep log ended."
    #},
    {
        "name": "duration",
        "type": "INTEGER",
        "description": "Duration of the sleep in ms."
    },
    {
        "name": "efficiency",
        "type": "INTEGER",
        "description": "Calculated sleep efficiency score. This is not the sleep score available in the "
                       "mobile application."
    },
    {
        "name": "end_time",
        "type": "TIMESTAMP",
        "description": "Time the sleep log ended"
    },
    {
        "name": "info_code",
        "type": "INTEGER",
        "description": ""
    },
    {
        "name": "is_main_sleep",
        "type": "BOOLEAN",
        "description": "Boolean value"
    },
    {
        "name": "log_id",
        "type": "INTEGER",
        "description": "Sleep log ID.",
    },
    {
        "name": "minutes_after_wakeup",
        "type": "INTEGER",
        "description": "The total number of minutes after the user woke up.",
    },
    {
        "name": "minutes_asleep",
        "type": "INTEGER",
        "description": "The total number of minutes the user was asleep.",
    },
    {
        "name": "minutes_awake",
        "type": "INTEGER",
        "description": "The total number of minutes the user was awake.",
    },
    {
        "name": "minutes_to_fall_asleep",
        "type": "INTEGER",
        "decription": "The total number of minutes before the user falls asleep. This value is generally 0 for "
                      "autosleep created sleep logs.",
    },
    {
        "name": "log_type",
        "type": "INTEGER",
        "decription": "The log creation method, auto_detected or manual",
    },
    {
        "name": "start_time",
        "type": "TIMESTAMP",
        "description": "Time the sleep log begins.",
    },
    {
        "name": "time_in_bed",
        "type": "INTEGER",
        "description": "Total number of minutes the user was in bed.",
    },
    {
        "name": "type",
        "type": "STRING",
        "description": "The type of sleep log, can be classic or stages"
    },
    {
        "name": "deep_count",
        "type": "INTEGER",
        "description": "Total number of times the user entered the deep sleep level.",
    },
    {
        "name": "deep_minutes",
        "type": "INTEGER",
        "description": "Total minutes the user appeared in the deep sleep level.",
    },
    {
        "name": "deep_thirty_day_avg_minutes",
        "type": "INTEGER",
        "description": "The average deep sleep stage time over the past 30 days. A sleep stage log is required to "
                       "generate this value. When a classic sleep log is recorded, this value will be missing.",
    },
    {
        "name": "light_count",
        "type": "INTEGER",
        "description": "Total number of times the user entered the light sleep level.",
    },
    {
        "name": "light_minutes",
        "type": "INTEGER",
        "description": "Total minutes the user appeared in the light sleep level.",
    },
    {
        "name": "light_thirty_day_avg_minutes",
        "type": "INTEGER",
        "description": "The average light sleep stage time over the past 30 days. A sleep stage log is required to "
                       "generate this value. When a classic sleep log is recorded, this value will be missing.",
    },
    {
        "name": "rem_count",
        "type": "INTEGER",
        "description": "Total number of times the user entered the REM sleep level.",
    },
    {
        "name": "rem_minutes",
        "type": "INTEGER",
        "description": "Total minutes the user appeared in the REM sleep level.",
    },
    {
        "name": "rem_thirty_day_avg_minutes",
        "type": "INTEGER",
        "description": "The average REM sleep stage time over the past 30 days. A sleep stage log is required to "
                       "generate this value. When a classic sleep log is recorded, this value will be missing.",
    },
    {
        "name": "wake_count",
        "type": "INTEGER",
        "description": "Total number of times the user entered the awake sleep level.",
    },
    {
        "name": "wake_minutes",
        "type": "INTEGER",
        "description": "Total minutes the user appeared in the awake sleep level.",
    },
    {
        "name": "wake_thirty_day_avg_minutes",
        "type": "INTEGER",
        "description": "The average awake sleep stage time over the past 30 days. A sleep stage log is required to "
                       "generate this value. When a classic sleep log is recorded, this value will be missing.",
    },
]

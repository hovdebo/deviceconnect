

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

INTRADAY_HRV_TABLE = "intraday_hrv"
INTRADAY_HRV_SCHEMA = [
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


INTRADAY_SPO2_TABLE = "intraday_spo2"
INTRADAY_SPO2_SCHEMA = [
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
        "name": "spo2",
        "type": "FLOAT",
        "description": "The Root Mean Square of Successive Differences (RMSSD) between heart beats. It measures "
                       "short-term variability in the user’s heart rate in milliseconds (ms)."
    },
]


INTRADAY_STEPS_TABLE = "intraday_steps"
INTRADAY_STEPS_SCHEMA = [
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
        "name": "steps",
        "type": "INTEGER",
        "description": "Number of steps in the interval"
    },
]

INTRADAY_FLOORS_TABLE = "intraday_floors"
INTRADAY_FLOORS_SCHEMA = [
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
        "name": "floors",
        "type": "INTEGER",
        "description": "Number of floors in the interval"
    },
]

INTRADAY_DISTANCE_TABLE = "intraday_distance"
INTRADAY_DISTANCE_SCHEMA = [
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
        "name": "distance",
        "type": "FLOAT",
        "description": "Number of distance in the interval"
    },
]

INTRADAY_ELEVATION_TABLE = "intraday_elevation"
INTRADAY_ELEVATION_SCHEMA = [
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
        "name": "elevation",
        "type": "FLOAT",
        "description": "Number of elevation in the interval"
    },
]

INTRADAY_CALORIES_TABLE = "intraday_calories"
INTRADAY_CALORIES_SCHEMA = [
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
        "name": "calories",
        "type": "FLOAT",
        "description": "Number of calories in the interval"
    },
    {
        "name": "level",
        "type": "INTEGER",
        "description": "Activity level in the interval"
    },
    {
        "name": "mets",
        "type": "INTEGER",
        "description": "METs value in the interval"
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
    {
        "name": "date_of_sleep",
        "type": "DATE",
        "description": "Date at which the sleep log ended."
    },
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
        "type": "STRING",
        "description": "The log creation method, auto_detected or manual",
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

BADGES_TABLE = "badges"
BADGES_SCHEMA = [
    {
        "name": "id",
        "type": "STRING",
        "mode": "REQUIRED",
        "description": "Primary Key",
    },
    {
        "name": "date",
        "type": "DATE",
        "mode": "REQUIRED",
        "description": "The date values were extracted",
    },
    {"name": "badge_gradient_end_color", "type": "STRING"},
    {"name": "badge_gradient_start_color", "type": "STRING"},
    {
        "name": "badge_type",
        "type": "STRING",
        "description": "Type of badge received.",
    },
    {"name": "category", "type": "STRING"},
    {
        "name": "date_time",
        "type": "STRING",
        "description": "Date the badge was achieved.",
    },
    {"name": "description", "type": "STRING"},
    {"name": "image_100px", "type": "STRING"},
    {"name": "image_125px", "type": "STRING"},
    {"name": "image_300px", "type": "STRING"},
    {"name": "image_50px", "type": "STRING"},
    {"name": "image_75px", "type": "STRING"},
    {"name": "name", "type": "STRING"},
    {"name": "share_image_640px", "type": "STRING"},
    {"name": "share_text", "type": "STRING"},
    {"name": "short_name", "type": "STRING"},
    {
        "name": "times_achieved",
        "type": "INTEGER",
        "description": "Number of times the user has achieved the badge.",
    },
    {
        "name": "value",
        "type": "INTEGER",
        "description": "Units of meaure based on localization settings.",
    },
    {
        "name": "unit",
        "type": "STRING",
        "description": "The badge goal in the unit measurement.",
    },
]

DEVICES_TABLE = "devices"
DEVICES_SCHEMA = [
    {
        "name": "id",
        "type": "STRING",
        "description": "Primary Key",
    },
    {
        "name": "date",
        "type": "DATE",
        "description": "The date values were extracted",
    },
    {
        "name": "battery",
        "type": "STRING",
        "description": "Returns the battery level of the device. Supported: High | Medium | Low | Empty",
    },
    {
        "name": "battery_level",
        "type": "INTEGER",
        "description": "Returns the battery level percentage of the device.",
    },
    {
        "name": "device_version",
        "type": "STRING",
        "description": "The product name of the device.",
    },
    {
        "name": "last_sync_time",
        "type": "TIMESTAMP",
        "description": "Timestamp representing the last time the device was sync'd with the Fitbit mobile application.",
    },
]

SOCIAL_TABLE = "social"
SOCIAL_SCHEMA = [
    {
        "name": "id",
        "type": "STRING",
        "description": "Primary Key",
    },
    {
        "name": "date",
        "type": "DATE",
        "description": "The date values were extracted",
    },
    {
        "name": "friend_id",
        "type": "STRING",
        "description": "Fitbit user id",
    },
    {
        "name": "type",
        "type": "STRING",
        "description": "Fitbit user id",
    },
    {
        "name": "attributes_name",
        "type": "STRING",
        "description": "Person's display name.",
    },
    {
        "name": "attributes_friend",
        "type": "BOOLEAN",
        "description": "The product name of the device.",
    },
    {
        "name": "attributes_avatar",
        "type": "STRING",
        "description": "Link to user's avatar picture.",
    },
    {
        "name": "attributes_child",
        "type": "BOOLEAN",
        "description": "Boolean value describing friend as a child account.",
    },
]

BODY_WEIGHT_TABLE = "body_weight"
BODY_WEIGHT_SCHEMA = [
    {
        "name": "id",
        "type": "STRING",
        "mode": "REQUIRED",
        "description": "Primary Key",
    },
    {
        "name": "date",
        "type": "DATE",
        "mode": "REQUIRED",
        "description": "The date values were extracted",
    },
    {
        "name": "bmi",
        "type": "FLOAT",
        "description": "Calculated BMI in the format X.XX",
    },
    {
        "name": "fat",
        "type": "FLOAT",
        "description": "The body fat percentage.",
    },
    {
        "name": "log_id",
        "type": "INTEGER",
        "description": "Weight Log IDs are unique to the user, but not globally unique.",
    },
    {
        "name": "source",
        "type": "STRING",
        "description": "The source of the weight log.",
    },
    {
        "name": "weight",
        "type": "FLOAT",
        "description": "Weight in the format X.XX,",
    },
]

NUTRITION_SUMMARY_TABLE = "nutrition_summary"
NUTRITION_SUMMARY_SCHEMA = [
    {
        "name": "id",
        "type": "STRING",
        "mode": "REQUIRED",
        "description": "Primary Key",
    },
    {
        "name": "date",
        "type": "DATE",
        "mode": "REQUIRED",
        "description": "The date values were extracted",
    },
    {
        "name": "calories",
        "type": "FLOAT",
        "description": "Total calories consumed.",
    },
    {
        "name": "carbs",
        "type": "FLOAT",
        "description": "Total carbs consumed.",
    },
    {
        "name": "fat",
        "type": "FLOAT",
        "description": "Total fats consumed.",
    },
    {
        "name": "fiber",
        "type": "FLOAT",
        "description": "Total fibers cosnsumed.",
    },
    {
        "name": "protein",
        "type": "FLOAT",
        "description": "Total proteins consumed.",
    },
    {
        "name": "sodium",
        "type": "FLOAT",
        "description": "Total sodium consumed.",
    },
    {
        "name": "water",
        "type": "FLOAT",
        "description": "Total water consumed",
    },
]

NUTRITION_LOGS_TABLE = "nutrition_logs"
NUTRITION_LOGS_SCHEMA = [
    {
        "name": "id",
        "type": "STRING",
        "mode": "REQUIRED",
        "description": "Primary Key",
    },
    {
        "name": "date",
        "type": "DATE",
        "mode": "REQUIRED",
        "description": "The date values were extracted",
    },
    {
        "name": "is_favorite",
        "type": "BOOLEAN",
        "mode": "NULLABLE",
        "description": "Total calories consumed.",
    },
    {
        "name": "log_date",
        "type": "DATE",
        "mode": "NULLABLE",
        "description": "Date of the food log.",
    },
    {
        "name": "log_id",
        "type": "INTEGER",
        "mode": "NULLABLE",
        "description": "Food log id.",
    },
    {
        "name": "logged_food_access_level",
        "type": "STRING",
        "mode": "NULLABLE",
    },
    {
        "name": "logged_food_amount",
        "type": "FLOAT",
        "mode": "NULLABLE",
    },
    {
        "name": "logged_food_brand",
        "type": "STRING",
        "mode": "NULLABLE",
    },
    {
        "name": "logged_food_calories",
        "type": "INTEGER",
        "mode": "NULLABLE",
    },
    {
        "name": "logged_food_food_id",
        "type": "INTEGER",
        "mode": "NULLABLE",
    },
    {
        "name": "logged_food_meal_type_id",
        "type": "INTEGER",
        "mode": "NULLABLE",
    },
    {
        "name": "logged_food_name",
        "type": "STRING",
        "mode": "NULLABLE",
    },
    {
        "name": "logged_food_unit_name",
        "type": "STRING",
        "mode": "NULLABLE",
    },
    {
        "name": "logged_food_unit_plural",
        "type": "STRING",
        "mode": "NULLABLE",
    },
    {
        "name": "nutritional_values_calories",
        "type": "FLOAT",
        "mode": "NULLABLE",
    },
    {
        "name": "nutritional_values_carbs",
        "type": "FLOAT",
        "mode": "NULLABLE",
    },
    {
        "name": "nutritional_values_fat",
        "type": "FLOAT",
        "mode": "NULLABLE",
    },
    {
        "name": "nutritional_values_fiber",
        "type": "FLOAT",
        "mode": "NULLABLE",
    },
    {
        "name": "nutritional_values_protein",
        "type": "FLOAT",
        "mode": "NULLABLE",
    },
    {
        "name": "nutritional_values_sodium",
        "type": "FLOAT",
        "mode": "NULLABLE",
    },
    {
        "name": "logged_food_locale",
        "type": "STRING",
        "mode": "NULLABLE",
    },
]

NUTRITION_GOALS_TABLE = "nutrition_goals"
NUTRITION_GOALS_SCHEMA = [
    {
        "name": "id",
        "type": "STRING",
        "mode": "REQUIRED",
        "description": "Primary Key",
    },
    {
        "name": "date",
        "type": "DATE",
        "mode": "REQUIRED",
        "description": "The date values were extracted",
    },
    {
        "name": "calories",
        "type": "INTEGER",
        "description": "The users set calorie goal",
    },
]

ACTIVITY_LOGS_TABLE = "activity_logs"
ACTIVITY_LOGS_SCHEMA = [
    {
        "name": "id",
        "type": "STRING",
        "description": "Primary Key",
    },
    {
        "name": "date",
        "type": "DATE",
        "description": "The date values were extracted",
    },
    {
        "name": "activity_id",
        "type": "INTEGER",
        "description": "The ID of the activity.",
    },
    {
        "name": "activity_parent_id",
        "type": "INTEGER",
        "description": 'The ID of the top level ("parent") activity.',
    },
    {
        "name": "activity_parent_name",
        "type": "STRING",
        "description": 'The name of the top level ("parent") activity.',
    },
    {
        "name": "calories",
        "type": "INTEGER",
        "description": "Number of calories burned during the exercise.",
    },
    {
        "name": "description",
        "type": "STRING",
        "description": "The description of the recorded exercise.",
    },
    {
        "name": "distance",
        "type": "FLOAT",
        "description": "The distance traveled during the recorded exercise.",
    },
    {
        "name": "duration",
        "type": "INTEGER",
        "description": "The activeDuration (milliseconds) + any pauses that occurred during the activity recording.",
    },
    {
        "name": "has_active_zone_minutes",
        "type": "BOOLEAN",
        "description": "True | False",
    },
    {
        "name": "has_start_time",
        "type": "BOOLEAN",
        "description": "True | False",
    },
    {
        "name": "is_favorite",
        "type": "BOOLEAN",
        "description": "True | False",
    },
    # {'name': 'last_modified', 'type': 'TIMESTAMP', 'description':'Timestamp the exercise was last modified.'},
    {
        "name": "log_id",
        "type": "INTEGER",
        "description": "The activity log identifier for the exercise.",
    },
    {
        "name": "name",
        "type": "STRING",
        "description": "Name of the recorded exercise.",
    },
    {
        "name": "start_datetime",
        "type": "TIMESTAMP",
        "description": "The start time of the recorded exercise.",
    },
    {
        "name": "steps",
        "type": "INTEGER",
        "description": "User defined goal for daily step count.",
    },
]

ACTIVITY_SUMMARY_TABLE = "activity_summary"
ACTIVITY_SUMMARY_SCHEMA = [
    {
        "name": "id",
        "type": "STRING",
        "mode": "REQUIRED",
        "description": "Primary Key",
    },
    {
        "name": "date",
        "type": "DATE",
        "mode": "REQUIRED",
        "description": "The date values were extracted",
    },
    {
        "name": "activity_score",
        "type": "INTEGER",
        "description": "No Description",
    },
    {
        "name": "activity_calories",
        "type": "INTEGER",
        "description": "The number of calories burned for the day during periods the user was active above sedentary level. This includes both activity burned calories and BMR.",
    },
    {
        "name": "calories_bmr",
        "type": "INTEGER",
        "description": "Total BMR calories burned for the day.",
    },
    {
        "name": "calories_out",
        "type": "INTEGER",
        "description": "Total calories burned for the day (daily timeseries total).",
    },
    {
        "name": "elevation",
        "type": "INTEGER",
        "description": "The elevation traveled for the day.",
    },
    {
        "name": "fairly_active_minutes",
        "type": "INTEGER",
        "description": "Total minutes the user was fairly/moderately active.",
    },
    {
        "name": "floors",
        "type": "INTEGER",
        "description": "The equivalent floors climbed for the day.",
    },
    {
        "name": "lightly_active_minutes",
        "type": "INTEGER",
        "description": "	Total minutes the user was lightly active.",
    },
    {
        "name": "marginal_calories",
        "type": "INTEGER",
        "description": "Total marginal estimated calories burned for the day.",
    },
    {
        "name": "resting_heart_rate",
        "type": "INTEGER",
        "description": "The resting heart rate for the day",
    },
    {
        "name": "sedentary_minutes",
        "type": "INTEGER",
        "description": "Total minutes the user was sedentary.",
    },
    {
        "name": "very_active_minutes",
        "type": "INTEGER",
        "description": "Total minutes the user was very active.",
    },
    {
        "name": "steps",
        "type": "INTEGER",
        "description": "Total steps taken for the day.",
    },
]

ACTIVITY_GOALS_TABLE = "activity_goals"
ACTIVITY_GOALS_SCHEMA = [
    {
        "name": "id",
        "type": "STRING",
        "mode": "REQUIRED",
        "description": "Primary Key",
    },
    {
        "name": "date",
        "type": "DATE",
        "mode": "REQUIRED",
        "description": "The date values were extracted",
    },
    {
        "name": "active_minutes",
        "type": "INTEGER",
        "description": "User defined goal for daily active minutes.",
    },
    {
        "name": "calories_out",
        "type": "INTEGER",
        "description": "User defined goal for daily calories burned.",
    },
    {
        "name": "distance",
        "type": "FLOAT",
        "description": "User defined goal for daily distance traveled.",
    },
    {
        "name": "floors",
        "type": "INTEGER",
        "description": "User defined goal for daily floor count.",
    },
    {
        "name": "steps",
        "type": "INTEGER",
        "description": "User defined goal for daily step count.",
    },
]

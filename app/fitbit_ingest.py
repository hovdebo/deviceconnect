# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""routes for fitbit data ingestion into bigquery

provides several routes used to query fitbit web apis
and process and ingest data into bigquery tables.  Typically
this would be provided only for administrative access or
run on a schedule.

Routes:

    /ingest: test route to test if the blueprint is correctly registered

    /update_tokens: will refresh all fitbit tokens to ensure they are valid
        when being used.


    /fitbit_heart_rate_scope: heart rate information
    /fitbit_sleep_scope:  sleep data
    /fitbit_intraday_scope: includes intraday hrv, steps, floors, distance, elevation, calories



    /fitbit_chunk_1: Badges, Social, Device information

    /fitbit_body_weight: body and weight data

    /fitbit_nutrition_scope: nutrition data







Dependencies:

    - fitbit application configuration is required to access the
        fitbit web apis.  see documentation on configuration

    - user refresh tokens are required to refresh the access token.
        this is stored in the backend firestore tables.  See
        documentation for details.

Configuration:

    * `GOOGLE_CLOUD_PROJECT`: gcp project where bigquery is available.
    * `GOOGLE_APPLICATION_CREDENTIALS`: points to a service account json.
    * `BIGQUERY_DATASET`: dataset to use to store user data.

Notes:

    all the data is ingested into BigQuery tables.

    there is currently no protection for these routes.

"""

import os
import timeit
from datetime import date, datetime, timedelta
import logging

import pandas as pd
import pandas_gbq
from flask import Blueprint, request
from flask_dance.contrib.fitbit import fitbit
from authlib.integrations.flask_client import OAuth
from skimpy import clean_columns

from .fitbit_auth import fitbit_bp

from . import schema
from . import fitbit_classes

log = logging.getLogger(__name__)


bp = Blueprint("fitbit_ingest_bp", __name__)

bigquery_datasetname = os.environ.get("BIGQUERY_DATASET")
if not bigquery_datasetname:
    bigquery_datasetname = "fitbit2"


def _tablename(table: str) -> str:
    return bigquery_datasetname + "." + table

def _normalize_response(df, column_list, email, date_pulled):
    for col in column_list:
        if col not in df.columns:
            df[col] = None
    df = df.reindex(columns=column_list)
    df.insert(0, "id", email)
    df.insert(1, "date", date_pulled)
    df = clean_columns(df)
    return df


def _date_pulled():
    """set the date pulled"""

    date_pulled = date.today() - timedelta(days=1)
    return date_pulled.strftime("%Y-%m-%d")


def _process_request(request):
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    # if caller provided date as query params, use that otherwise use yesterday
    date_pulled = request.args.get("date", _date_pulled())
    user_list = fitbit_bp.storage.all_users()
    if request.args.get("user") in user_list:
        user_list = [request.args.get("user")]

    return project_id, date_pulled, user_list


def _write_to_bq(df_list, table_name, project_id, table_schema):
    if len(df_list) > 0:
        try:
            bulk_df = pd.concat(df_list, axis=0)
            pandas_gbq.to_gbq(
                dataframe=bulk_df,
                destination_table=_tablename(table_name),
                project_id=project_id,
                if_exists="append",
                table_schema=table_schema
            )
        except Exception as e:
            log.error("exception occurred: %s", str(e))


@bp.route("/fitbit_heart_rate_scope")
def fitbit_heart_rate_scope():
    start = timeit.default_timer()
    project_id, date_pulled, user_list = _process_request(request)

    hr_zones_list = []
    hr_list = []
    for user in user_list:
        fitbit_bp.storage.user = user

        if fitbit_bp.session.token:
            del fitbit_bp.session.token

        try:
            resp = fitbit.get(
                "1.2/user/-/activities/heart/date/" + date_pulled + "/1d.json"
            )

            log.debug("%s: %d [%s]", resp.url, resp.status_code, resp.reason)

            intraday_hr = fitbit_classes.IntradayHeartRate(resp.json())

            intraday_hr.heart_rate_df.insert(0, "id", user)
            hr_list.append(intraday_hr.heart_rate_df)

            intraday_hr.zones_df.insert(0, "id", user)
            hr_zones_list.append(intraday_hr.zones_df)
        except Exception as e:
            log.error("exception occured: %s", str(e))

    load_stop = timeit.default_timer()
    time_to_load = load_stop - start
    print("Heart Rate Zones " + str(time_to_load))

    _write_to_bq(hr_zones_list, schema.ZONE_TABLE, project_id, schema.ZONE_SCHEMA)
    _write_to_bq(hr_list, schema.HEART_RATE_TABLE, project_id, schema.HEART_RATE_SCHEMA)

    stop = timeit.default_timer()
    execution_time = stop - start
    print("Heart Rate Scope Loaded " + str(execution_time))

    fitbit_bp.storage.user = None
    return "Heart Rate Scope Loaded"


@bp.route("/fitbit_sleep_scope")
def fitbit_sleep_scope():
    start = timeit.default_timer()
    project_id, date_pulled, user_list = _process_request(request)

    sleep_meta_list = []
    sleep_stage_list = []
    for user in user_list:

        log.debug("user: %s", user)

        fitbit_bp.storage.user = user

        if fitbit_bp.session.token:
            del fitbit_bp.session.token

        try:

            resp = fitbit.get("/1.2/user/-/sleep/date/" + date_pulled + ".json")

            log.debug("%s: %d [%s]", resp.url, resp.status_code, resp.reason)

            sleep = fitbit_classes.SleepLog(resp.json())

            sleep.stage_df.insert(0, "id", user)
            sleep_stage_list.append(sleep.stage_df)

            sleep.meta_df.insert(0, "id", user)
            sleep_meta_list.append(sleep.meta_df)

        except Exception as e:
            log.error("exception occured: %s", str(e))

    # end loop over users

    fitbit_stop = timeit.default_timer()
    fitbit_execution_time = fitbit_stop - start
    print("Sleep Scope: " + str(fitbit_execution_time))

    _write_to_bq(sleep_stage_list, schema.SLEEP_STAGES_TABLE, project_id, schema.SLEEP_STAGES_SCHEMA)
    _write_to_bq(sleep_meta_list, schema.SLEEP_RECORDS_TABLE, project_id, schema.SLEEP_RECORDS_SCHEMA)

    stop = timeit.default_timer()
    execution_time = stop - start
    print("Sleep Scope Loaded: " + str(execution_time))

    fitbit_bp.storage.user = None

    return "Sleep Scope Loaded"


@bp.route("/fitbit_intraday_scope")
def fitbit_intraday_scope():
    start = timeit.default_timer()
    project_id, date_pulled, user_list = _process_request(request)

    intraday_hrv_list = []
    intraday_spo2_list = []
    intraday_steps_list = []
    intraday_floors_list = []
    intraday_distance_list = []
    intraday_elevation_list = []
    intraday_calories_list = []

    activities = [
        [f"/1/user/-/hrv/date/{date_pulled}/all.json", fitbit_classes.IntradayHrv,
         intraday_hrv_list, schema.INTRADAY_HRV_TABLE, schema.INTRADAY_HRV_SCHEMA],
        [f"/1/user/-/spo2/date/{date_pulled}/all.json", fitbit_classes.IntradaySpo2,
         intraday_spo2_list, schema.INTRADAY_SPO2_TABLE, schema.INTRADAY_SPO2_TABLE],
        [f"/1/user/-/activities/steps/date/{date_pulled}/1d/1min.json", fitbit_classes.IntradaySteps,
         intraday_steps_list, schema.INTRADAY_STEPS_TABLE, schema.INTRADAY_STEPS_SCHEMA],
        [f"/1/user/-/activities/floors/date/{date_pulled}/1d/1min.json", fitbit_classes.IntradayFloors,
         intraday_floors_list, schema.INTRADAY_FLOORS_TABLE, schema.INTRADAY_FLOORS_SCHEMA],
        [f"/1/user/-/activities/distance/date/{date_pulled}/1d/1min.json", fitbit_classes.IntradayDistance,
         intraday_distance_list, schema.INTRADAY_DISTANCE_TABLE, schema.INTRADAY_DISTANCE_SCHEMA],
        [f"/1/user/-/activities/elevation/date/{date_pulled}/1d/1min.json", fitbit_classes.IntradayElevation,
         intraday_elevation_list, schema.INTRADAY_ELEVATION_TABLE, schema.INTRADAY_ELEVATION_SCHEMA],
        [f"/1/user/-/activities/calories/date/{date_pulled}/1d/1min.json", fitbit_classes.IntradayCalories,
         intraday_calories_list, schema.INTRADAY_CALORIES_TABLE, schema.INTRADAY_CALORIES_SCHEMA],
    ]

    for user in user_list:
        log.debug("user: %s", user)
        fitbit_bp.storage.user = user

        if fitbit_bp.session.token:
            del fitbit_bp.session.token

        for activity in activities:
            try:
                url = activity[0]
                class_type = activity[1]
                df_list = activity[2]
                
                resp = fitbit.get(url)
                log.debug("%s: %d [%s]", resp.url, resp.status_code, resp.reason)
                df = class_type(resp.json()).df
                df.insert(0, "id", user)
                df_list.append(df)
            except Exception as e:
                log.error(f"Exception occurred during processing of url '{url}': {e}")

    # end loop over users

    fitbit_stop = timeit.default_timer()
    fitbit_execution_time = fitbit_stop - start
    print("Intraday Scope: " + str(fitbit_execution_time))

    for activity in activities:
        df_list = activity[2]
        table_name = activity[3]
        table_schema = activity[4]
        _write_to_bq(df_list, table_name, project_id, table_schema)

    stop = timeit.default_timer()
    execution_time = stop - start
    print("Intraday Scope Loaded: " + str(execution_time))

    fitbit_bp.storage.user = None

    return "Intraday Scope Loaded"



# Not touched yet

@bp.route("/ingest")
def ingest():
    """test route to ensure that blueprint is loaded"""

    result = []
    allusers = fitbit_bp.storage.all_users()
    log.debug(allusers)

    for x in allusers:

        try:

            log.debug("user = " + x)

            fitbit_bp.storage.user = x
            if fitbit_bp.session.token:
                del fitbit_bp.session.token

            token = fitbit_bp.token

            log.debug("access token: " + token["access_token"])
            log.debug("refresh_token: " + token["refresh_token"])
            log.debug("expiration time " + str(token["expires_at"]))
            log.debug("             in " + str(token["expires_in"]))

            resp = fitbit.get("/1/user/-/profile.json")

            log.debug("%s: %d [%s]", resp.url, resp.status_code, resp.reason)

            j = resp.json()

            log.debug(f"retrieved profile: {resp.reason}")
            log.debug(
                f"{x}: {j['user']['fullName']} ({j['user']['gender']}/{j['user']['age']})"
            )
            result.append(
                f"{x}: {j['user']['fullName']} ({j['user']['gender']}/{j['user']['age']})"
            )

        except (Exception) as e:
            log.error("exception occured: %s", str(e))

    return str(result)


#
# Chunk 1: Badges, Social, Device
#
@bp.route("/fitbit_chunk_1")
def fitbit_chunk_1():
    start = timeit.default_timer()
    project_id, date_pulled, user_list = _process_request(request)

    badges_list = []
    device_list = []
    social_list = []

    for user in user_list:

        log.debug("user: %s", user)

        fitbit_bp.storage.user = user

        if fitbit_bp.session.token:
            del fitbit_bp.session.token

        try:

            ############## CONNECT TO BADGES ENDPOINT #################

            resp = fitbit.get("/1/user/-/badges.json")

            log.debug("%s: %d [%s]", resp.url, resp.status_code, resp.reason)

            badges = resp.json()["badges"]

            badges_df = pd.json_normalize(badges)
            badges_columns = [
                "badgeGradientEndColor",
                "badgeGradientStartColor",
                "badgeType",
                "category",
                "cheers",
                "dateTime",
                "description",
                "earnedMessage",
                "encodedId",
                "image100px",
                "image125px",
                "image300px",
                "image50px",
                "image75px",
                "marketingDescription",
                "mobileDescription",
                "name",
                "shareImage640px",
                "shareText",
                "shortDescription",
                "shortName",
                "timesAchieved",
                "value",
                "unit",
            ]
            badges_df = _normalize_response(
                badges_df, badges_columns, user, date_pulled
            )
            try:
                badges_df = badges_df.drop(["cheers"], axis=1)
            except:
                pass

            badges_list.append(badges_df)

        except (Exception) as e:
            log.error("exception occured: %s", str(e))

        try:
            ############## CONNECT TO DEVICE ENDPOINT #################
            resp = fitbit.get("1/user/-/devices.json")

            log.debug("%s: %d [%s]", resp.url, resp.status_code, resp.reason)

            device_df = pd.json_normalize(resp.json())
            try:
                device_df = device_df.drop(
                    ["features", "id", "mac", "type"], axis=1
                )
            except:
                pass

            device_columns = [
                "battery",
                "batteryLevel",
                "deviceVersion",
                "lastSyncTime",
            ]
            device_df = _normalize_response(
                device_df, device_columns, user, date_pulled
            )
            device_df["last_sync_time"] = device_df["last_sync_time"].apply(
                lambda x: datetime.strptime(x, "%Y-%m-%dT%H:%M:%S.%f")
            )
            device_list.append(device_df)

        except (Exception) as e:
            log.error("exception occured: %s", str(e))

        try:
            ############## CONNECT TO SOCIAL ENDPOINT #################
            resp = fitbit.get("1.1/user/-/friends.json")

            log.debug("%s: %d [%s]", resp.url, resp.status_code, resp.reason)

            social_df = pd.json_normalize(resp.json()["data"])
            social_df = social_df.rename(columns={"id": "friend_id"})
            social_columns = [
                "friend_id",
                "type",
                "attributes.name",
                "attributes.friend",
                "attributes.avatar",
                "attributes.child",
            ]
            social_df = _normalize_response(
                social_df, social_columns, user, date_pulled
            )
            social_list.append(social_df)

        except (Exception) as e:
            log.error("exception occured: %s", str(e))

    # end loop over users

    #### CONCAT DATAFRAMES INTO BULK DF ####

    load_stop = timeit.default_timer()
    time_to_load = load_stop - start
    print("Program Executed in " + str(time_to_load))

    # ######## LOAD DATA INTO BIGQUERY #########
    log.debug("push to BQ")
    _write_to_bq(badges_list, schema.BADGES_TABLE, project_id, schema.BADGES_SCHEMA)
    _write_to_bq(device_list, schema.DEVICES_TABLE, project_id, schema.DEVICES_SCHEMA)
    _write_to_bq(social_list, schema.SOCIAL_TABLE, project_id, schema.SOCIAL_SCHEMA)

    stop = timeit.default_timer()
    execution_time = stop - start
    print("Fitbit Chunk Loaded " + str(execution_time))

    fitbit_bp.storage.user = None

    return "Fitbit Chunk Loaded"


#
# Body and Weight
#
@bp.route("/fitbit_body_weight")
def fitbit_body_weight():
    start = timeit.default_timer()
    project_id, date_pulled, user_list = _process_request(request)

    body_weight_df_list = []

    for user in user_list:

        log.debug("user: %s", user)

        fitbit_bp.storage.user = user

        if fitbit_bp.session.token:
            del fitbit_bp.session.token

        try:

            resp = fitbit.get(
                "/1/user/-/body/log/weight/date/" + date_pulled + ".json"
            )

            log.debug("%s: %d [%s]", resp.url, resp.status_code, resp.reason)

            body_weight = resp.json()["weight"]
            assert body_weight, "weight returned no data"
            body_weight_df = pd.json_normalize(body_weight)
            try:
                body_weight_df = body_weight_df.drop(["date", "time"], axis=1)
            except:
                pass

            body_weight_columns = ["bmi", "fat", "logId", "source", "weight"]
            body_weight_df = _normalize_response(
                body_weight_df, body_weight_columns, user, date_pulled
            )
            body_weight_df_list.append(body_weight_df)

        except (Exception) as e:
            log.error("exception occured: %s", str(e))

    # end loop over users

    log.debug("push to BQ")
    _write_to_bq(body_weight_df_list, schema.BODY_WEIGHT_TABLE, project_id, schema.BODY_WEIGHT_SCHEMA)

    stop = timeit.default_timer()
    execution_time = stop - start
    print("Body & Weight Scope Loaded " + str(execution_time))

    fitbit_bp.storage.user = None

    return "Body & Weight Scope Loaded"


#
# Nutrition Data
#
@bp.route("/fitbit_nutrition_scope")
def fitbit_nutrition_scope():
    start = timeit.default_timer()
    project_id, date_pulled, user_list = _process_request(request)

    nutrition_summary_list = []
    nutrition_logs_list = []
    nutrition_goals_list = []

    for user in user_list:

        log.debug("user: %s", user)

        fitbit_bp.storage.user = user

        if fitbit_bp.session.token:
            del fitbit_bp.session.token

        try:

            resp = fitbit.get(
                "/1/user/-/foods/log/date/" + date_pulled + ".json"
            )

            log.debug("%s: %d [%s]", resp.url, resp.status_code, resp.reason)

            nutrition_summary = resp.json()["summary"]
            nutrition_logs = resp.json()["foods"]

            nutrition_summary_df = pd.json_normalize(nutrition_summary)
            nutrition_logs_df = pd.json_normalize(nutrition_logs)

            try:
                nutrition_logs_df = nutrition_logs_df.drop(
                    [
                        "loggedFood.creatorEncodedId",
                        "loggedFood.unit.id",
                        "loggedFood.units",
                    ],
                    axis=1,
                )
            except:
                pass

            nutrition_summary_columns = [
                "calories",
                "carbs",
                "fat",
                "fiber",
                "protein",
                "sodium",
                "water",
            ]
            nutrition_logs_columns = [
                "isFavorite",
                "logDate",
                "logId",
                "loggedFood.accessLevel",
                "loggedFood.amount",
                "loggedFood.brand",
                "loggedFood.calories",
                "loggedFood.foodId",
                "loggedFood.mealTypeId",
                "loggedFood.name",
                "loggedFood.unit.name",
                "loggedFood.unit.plural",
                "nutritionalValues.calories",
                "nutritionalValues.carbs",
                "nutritionalValues.fat",
                "nutritionalValues.fiber",
                "nutritionalValues.protein",
                "nutritionalValues.sodium",
                "loggedFood.locale",
            ]

            nutrition_summary_df = _normalize_response(
                nutrition_summary_df,
                nutrition_summary_columns,
                user,
                date_pulled,
            )
            nutrition_logs_df = _normalize_response(
                nutrition_logs_df, nutrition_logs_columns, user, date_pulled
            )

            nutrition_summary_list.append(nutrition_summary_df)
            nutrition_logs_list.append(nutrition_logs_df)

        except (Exception) as e:
            log.error("exception occured: %s", str(e))

        try:
            resp = fitbit.get("/1/user/-/foods/log/goal.json")

            log.debug("%s: %d [%s]", resp.url, resp.status_code, resp.reason)

            nutrition_goal = resp.json()["goals"]
            nutrition_goal_df = pd.json_normalize(nutrition_goal)
            nutrition_goal_columns = ["calories"]
            nutrition_goal_df = _normalize_response(
                nutrition_goal_df, nutrition_goal_columns, user, date_pulled
            )
            nutrition_goals_list.append(nutrition_goal_df)

        except (Exception) as e:
            log.error("exception occured: %s", str(e))

    # end of loop over users
    log.debug("push to BQ")

    _write_to_bq(nutrition_summary_list, schema.NUTRITION_SUMMARY_TABLE, project_id, schema.NUTRITION_SUMMARY_SCHEMA)
    _write_to_bq(nutrition_logs_list, schema.NUTRITION_LOGS_TABLE, project_id, schema.NUTRITION_LOGS_SCHEMA)
    _write_to_bq(nutrition_goals_list, schema.NUTRITION_GOALS_TABLE, project_id, schema.NUTRITION_GOALS_SCHEMA)

    stop = timeit.default_timer()
    execution_time = stop - start
    print("Nutrition Scope Loaded " + str(execution_time))

    fitbit_bp.storage.user = None

    return "Nutrition Scope Loaded"


#
# Activity Data
#
@bp.route("/fitbit_activity_scope")
def fitbit_activity_scope():
    start = timeit.default_timer()
    project_id, date_pulled, user_list = _process_request(request)

    activities_list = []
    activity_summary_list = []
    activity_distance_list = []
    activity_goals_list = []
    omh_activity_list = []

    for user in user_list:

        log.debug("user: %s", user)

        fitbit_bp.storage.user = user

        if fitbit_bp.session.token:
            del fitbit_bp.session.token

        try:

            resp = fitbit.get(
                "/1/user/-/activities/date/" + date_pulled + ".json"
            )

            log.debug("%s: %d [%s]", resp.url, resp.status_code, resp.reason)

            # subset response for activites, summary, and goals
            activity_goals = resp.json()["goals"]
            activities = resp.json()["activities"]
            activity_summary = resp.json()["summary"]

            activity_goals_df = pd.json_normalize(activity_goals)
            activity_goals_columns = [
                "activeMinutes",
                "caloriesOut",
                "distance",
                "floors",
                "steps",
            ]
            activity_goals_df = _normalize_response(
                activity_goals_df, activity_goals_columns, user, date_pulled
            )

            # activity_distances = resp.json()["summary"]["distances"]
            # activity_distances_df = pd.json_normalize(activity_distances)
            # activity_distances_columns = [
            #     "activity",
            #     "total_distance",
            #     "tracker_distance",
            #     "logged_activites_distance",
            #     "very_active_distance",
            #     "moderetly_active_distance",
            #     "lightly_active_distance",
            #     "sedentary_active_distance",
            # ]

            activities_df = pd.json_normalize(activities)
            # Define columns
            activites_columns = [
                "activityId",
                "activityParentId",
                "activityParentName",
                "calories",
                "description",
                "distance",
                "duration",
                "hasActiveZoneMinutes",
                "hasStartTime",
                "isFavorite",
                "lastModified",
                "logId",
                "name",
                "startDate",
                "startTime",
                "steps",
            ]
            activities_df = _normalize_response(
                activities_df, activites_columns, user, date_pulled
            )
            activities_df["start_datetime"] = pd.to_datetime(
                activities_df["start_date"] + " " + activities_df["start_time"]
            )
            activities_df = activities_df.drop(
                ["start_date", "start_time", "last_modified"], axis=1
            )

            activity_summary_df = pd.json_normalize(activity_summary)
            try:
                activity_summary_df = activity_summary_df.drop(
                    ["distances", "heartRateZones"], axis=1
                )
            except:
                pass

            activity_summary_columns = [
                "activeScore",
                "activityCalories",
                "caloriesBMR",
                "caloriesOut",
                "elevation",
                "fairlyActiveMinutes",
                "floors",
                "lightlyActiveMinutes",
                "marginalCalories",
                "restingHeartRate",
                "sedentaryMinutes",
                "steps",
                "veryActiveMinutes",
            ]

            activity_summary_df = _normalize_response(
                activity_summary_df, activity_summary_columns, user, date_pulled
            )

            # Append dfs to df list
            activities_list.append(activities_df)
            activity_summary_list.append(activity_summary_df)
            activity_goals_list.append(activity_goals_df)

        except (Exception) as e:
            log.error("exception occured: %s", str(e))

    fitbit_stop = timeit.default_timer()
    fitbit_execution_time = fitbit_stop - start
    print("Activity Scope: " + str(fitbit_execution_time))

    # bulk_omh_activity_df = pd.concat(omh_activity_list, axis=0)

    if len(activities_list) > 0:

        try:

            bulk_activities_df = pd.concat(activities_list, axis=0)

            pandas_gbq.to_gbq(
                dataframe=bulk_activities_df,
                destination_table=_tablename("activity_logs"),
                project_id=project_id,
                if_exists="append",
                table_schema=[
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
                ],
            )

        except (Exception) as e:
            log.error("exception occured: %s", str(e))

    if len(activity_summary_list) > 0:

        try:

            bulk_activity_summary_df = pd.concat(activity_summary_list, axis=0)

            pandas_gbq.to_gbq(
                dataframe=bulk_activity_summary_df,
                destination_table=_tablename("activity_summary"),
                project_id=project_id,
                if_exists="append",
                table_schema=[
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
                ],
            )

        except (Exception) as e:
            log.error("exception occured: %s", str(e))

    if len(activity_goals_list) > 0:

        try:

            bulk_activity_goals_df = pd.concat(activity_goals_list, axis=0)

            pandas_gbq.to_gbq(
                dataframe=bulk_activity_goals_df,
                destination_table=_tablename("activity_goals"),
                project_id=project_id,
                if_exists="append",
                table_schema=[
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
                ],
            )
        except (Exception) as e:
            log.error("exception occured: %s", str(e))

    stop = timeit.default_timer()
    execution_time = stop - start
    print("Activity Scope Loaded: " + str(execution_time))

    fitbit_bp.storage.user = None

    return "Activity Scope Loaded"



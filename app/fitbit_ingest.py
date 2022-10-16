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
and process and ingest data into bigquery tables.  Typically,
this would be provided only for administrative access or
run on a schedule.

Routes:

    /ingest: test route to test if the blueprint is correctly registered

    /download: download everything for the day to files

    /update_tokens: will refresh all fitbit tokens to ensure they are valid
        when being used.


    /fitbit_sleep_scope:  sleep data
    /fitbit_intraday_scope: includes intraday hrv, spo2, breathing_rate, steps, floors, distance,
                             elevation, calories, heart_rate



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
from datetime import date, timedelta
import logging
import pickle

import pandas_gbq
from flask import Blueprint, request
from flask_dance.contrib.fitbit import fitbit
from skimpy import clean_columns

from .fitbit_auth import fitbit_bp

from . import schema
from . import fitbit_classes

log = logging.getLogger(__name__)

bp = Blueprint("fitbit_ingest_bp", __name__)

bigquery_dataset_name = os.environ.get("BIGQUERY_DATASET")
if not bigquery_dataset_name:
    bigquery_dataset_name = "fitbit2"


def _table_name(table: str) -> str:
    return bigquery_dataset_name + "." + table


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


def _write_to_bq(bulk_df, table_name, project_id, table_schema):
    if bulk_df.shape[0] > 0:
        try:
            pandas_gbq.to_gbq(
                dataframe=bulk_df,
                destination_table=_table_name(table_name),
                project_id=project_id,
                if_exists="append",
                table_schema=table_schema
            )
        except Exception as e:
            log.error("exception occurred: %s", str(e))


@bp.route("/download")
def download():
    project_id, date_pulled, user_list = _process_request(request)
    for user in user_list:
        fitbit_bp.storage.user = user

        if fitbit_bp.session.token:
            del fitbit_bp.session.token

        classes = [
            [fitbit_classes.HeartRateIntraday, "HeartRateIntraday"],
            [fitbit_classes.CaloriesIntraday, "CaloriesIntraday"],
            [fitbit_classes.DistanceIntraday, "DistancesIntraday"],
            [fitbit_classes.ElevationIntraday, "ElevationIntraday"],
            [fitbit_classes.FloorsIntraday, "FloorsIntraday"],
            [fitbit_classes.HrvIntraday, "HrvIntraday"],
            [fitbit_classes.Spo2Intraday, "Spo2Intraday"],
            [fitbit_classes.StepsIntraday, "StepsIntraday"],
            [fitbit_classes.BreathingRateIntraday, "BreathingRateIntraday"],
            [fitbit_classes.SleepLog, "SleepLog"],
        ]

        for class_type, class_string in classes:
            try:
                resp = fitbit.get(
                    class_type.url("-", date_pulled)
                )

                log.debug("%s: %d [%s]", resp.url, resp.status_code, resp.reason)
                if resp.status_code == 200:
                    json_response = resp.json()
                    filename = f"{class_string}_{date_pulled}_{user}.pickle"
                    with open(filename, 'wb') as f:
                        pickle.dump(json_response, f)

            except Exception as e:
                log.error(f"exception occurred while loading '{class_string}': {e}")

        return "Downloaded"


@bp.route("/fitbit_sleep_scope")
def fitbit_sleep_scope():
    project_id, date_pulled, user_list = _process_request(request)
    for user in user_list:
        fitbit_bp.storage.user = user

        if fitbit_bp.session.token:
            del fitbit_bp.session.token

        try:
            resp = fitbit.get(fitbit_classes.SleepLog.url("-", date_pulled))
            log.debug("%s: %d [%s]", resp.url, resp.status_code, resp.reason)

            sleep = fitbit_classes.SleepLog(resp.json())

            df = sleep.dataframe
            df.insert(0, "id", user)

            meta_df = sleep.meta_dataframe
            meta_df.insert(0, "id", user)
        except Exception as e:
            log.error("exception occurred: %s", str(e))
            continue

        _write_to_bq(df, schema.SLEEP_STAGES_TABLE, project_id, schema.SLEEP_STAGES_SCHEMA)
        _write_to_bq(meta_df, schema.SLEEP_RECORDS_TABLE, project_id, schema.SLEEP_RECORDS_SCHEMA)

    fitbit_bp.storage.user = None

    return "Sleep Scope Loaded"


@bp.route("/fitbit_intraday_scope")
def fitbit_intraday_scope():
    project_id, date_pulled, user_list = _process_request(request)

    activities = [
        [fitbit_classes.HrvIntraday, schema.INTRADAY_HRV_TABLE, schema.INTRADAY_HRV_SCHEMA],
        [fitbit_classes.Spo2Intraday, schema.INTRADAY_SPO2_TABLE, schema.INTRADAY_SPO2_TABLE],
        [fitbit_classes.StepsIntraday, schema.INTRADAY_STEPS_TABLE, schema.INTRADAY_STEPS_SCHEMA],
        [fitbit_classes.FloorsIntraday, schema.INTRADAY_FLOORS_TABLE, schema.INTRADAY_FLOORS_SCHEMA],
        [fitbit_classes.DistanceIntraday, schema.INTRADAY_DISTANCE_TABLE, schema.INTRADAY_DISTANCE_SCHEMA],
        [fitbit_classes.ElevationIntraday, schema.INTRADAY_ELEVATION_TABLE, schema.INTRADAY_ELEVATION_SCHEMA],
        [fitbit_classes.CaloriesIntraday, schema.INTRADAY_CALORIES_TABLE, schema.INTRADAY_CALORIES_SCHEMA],
        [fitbit_classes.HeartRateIntraday,
         schema.INTRADAY_HEART_RATE_TABLE,
         schema.INTRADAY_HEART_RATE_SCHEMA],
        [fitbit_classes.BreathingRateIntraday,
         schema.INTRADAY_BREATHING_RATE_TABLE,
         schema.INTRADAY_BREATHING_RATE_SCHEMA],
    ]

    for user in user_list:
        log.debug("user: %s", user)
        fitbit_bp.storage.user = user

        if fitbit_bp.session.token:
            del fitbit_bp.session.token

        for activity in activities:
            class_type = activity[0]
            table_name = activity[1]
            table_schema = activity[2]

            url = class_type.url("-", date_pulled)

            try:
                resp = fitbit.get(url)
                log.debug("%s: %d [%s]", resp.url, resp.status_code, resp.reason)
                df = class_type(resp.json()).dataframe
                df.insert(0, "id", user)
            except Exception as e:
                log.error(f"Exception occurred during processing of url '{url}': {e}")
                continue

            _write_to_bq(df, table_name, project_id, table_schema)

    fitbit_bp.storage.user = None

    return "Intraday Scope Loaded"


# Not touched yet

@bp.route("/ingest")
def ingest():
    """test route to ensure that blueprint is loaded"""

    result = []
    all_users = fitbit_bp.storage.all_users()
    log.debug(all_users)

    for x in all_users:
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

        except Exception as e:
            log.error("exception occurred: %s", str(e))

    return str(result)

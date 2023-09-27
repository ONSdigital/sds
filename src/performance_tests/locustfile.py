import json
import os
from urllib.parse import urlencode

import google.oauth2.id_token
import requests
from locust import HttpUser, task
from logging_config import logging

logger = logging.getLogger(__name__)


def get_value_from_env(env_value, default_value="") -> str:
    """
    Method to determine if a desired enviroment variable has been set and return it.
    If an enviroment variable or default value are not set an expection is raised.

    Parameters:
        env_value: value to check environment for
        default_value: optional argument to allow defaulting of values

    Returns:
        str: the environment value corresponding to the input
    """
    value = os.environ.get(env_value)
    if value:
        return value
    elif default_value != "":
        return default_value
    else:
        raise Exception(
            f"The environment variable {env_value} must be set to proceed",
        )


class Config:
    BASE_URL = get_value_from_env("BASE_URL", "http://127.0.0.1:3000")
    FIRESTORE_EMULATOR_HOST = "0.0.0.0:8200"
    PROJECT_ID = get_value_from_env("PROJECT_ID", "ons-sds-sandbox-01")
    STORAGE_EMULATOR_HOST = "http://localhost:9023"
    TEST_SCHEMA_FILE = "schema.json"
    OAUTH_CLIENT_ID = get_value_from_env(
        "OAUTH_CLIENT_ID",
        "293516424663-6ebeaknvn4b3s6lplvo6v12trahghfsc.apps.googleusercontent.com",
    )


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "sandbox-key.json"

config = Config()
BASE_URL = config.BASE_URL
auth_req = google.auth.transport.requests.Request()
auth_token = google.oauth2.id_token.fetch_id_token(
    auth_req, audience=config.OAUTH_CLIENT_ID
)
logger.info("Authorization token.....")
logger.info(auth_token)
logger.info(config.OAUTH_CLIENT_ID)
HEADERS = {"Authorization": f"Bearer {auth_token}"}


def delete_docs(survey_id):
    """
    Deletes firestore documents
    Args:
        survey_id (str) endpoint to be added to DELETE_CI_PATH

    Returns:
        obj: response object
    """
    return requests.delete(
        f"{BASE_URL}/v1/dev/teardown/{survey_id}", headers=HEADERS, timeout=60
    )


def post_sds_v1(payload):
    """Creates schema for testing purposes

    Args:
        payload (json): json to be sent to API

    Returns:
        obj: response object
    """
    return requests.post(
        f"{BASE_URL}/v1/schema?survey_id=123",
        headers=HEADERS,
        json=payload,
        timeout=60,
    )


def load_json(filepath: str) -> dict:
    """
    Method to load json from a file.

    Parameters:
        filepath: string specifiing the location of the file to be loaded.

    Returns:
        dict: the json object from the specified file.
    """
    with open(filepath) as f:
        return json.load(f)


class PerformanceTests(HttpUser):
    host = config.BASE_URL

    def __init__(self, *args, **kwargs):
        """Override default init to save some additional class attributes"""
        super().__init__(*args, **kwargs)

        self.post_sds_schema_payload = load_json(config.TEST_SCHEMA_FILE)
        self.request_headers = HEADERS

    def on_start(self):
        """Create a ci to find"""
        super().on_start()
        post_sds_v1(self.post_sds_schema_payload)

    def on_stop(self):
        """Delete any cis we've created"""
        super().on_stop()
        # delete_docs(self.survey_id)

    @task
    def http_post_sds_v1(self):
        """Performance test task for the `http_post_sds_v1` function"""
        self.client.post(
            f"{BASE_URL}/v1/schema?survey_id=123",
            json=self.post_sds_schema_payload,
            headers=HEADERS,
        )

    @task
    def http_get_sds_schema_metadata_v1(self):
        """Performance test task for the `http_get_sds_schema_metadata_v1` function"""
        querystring_params = {
            "survey_id": "123",
        }
        self.client.get(
            f"{BASE_URL}/v1/schema_metadata?{urlencode(querystring_params)}",
            headers=HEADERS,
        )

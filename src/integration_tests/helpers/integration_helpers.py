import json
import os
import time

import google.oauth2.id_token
import requests
from config.config_factory import config
from google.cloud import storage
from oauthlib.oauth2 import MobileApplicationClient
from repositories.buckets.bucket_loader import bucket_loader
from repositories.firebase.firebase_loader import firebase_loader
from requests.adapters import HTTPAdapter
from requests_oauthlib import OAuth2Session
from urllib3 import Retry

from src.integration_tests.helpers.bucket_helpers import (
    delete_blobs,
    delete_local_bucket_data,
)
from src.integration_tests.helpers.firestore_helpers import (
    delete_local_firestore_data,
    perform_delete_transaction,
)

storage_client = storage.Client()


def setup_session() -> requests.Session:
    """
    Method to setup a http/s session to facilitate testing.

    Parameters:
        None

    Returns:
        Session: a http/s session.
    """
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    return session


def generate_headers() -> dict[str, str]:
    """
    Method to create headers for authentication if connecting to a remote version of the API.

    Parameters:
        None

    Returns:
        dict[str, str]: the headers required for remote authentication.
    """
    headers = {}
    auth_token = os.environ.get("ACCESS_TOKEN")
    if auth_token is None:
        auth_req = google.auth.transport.requests.Request()
        auth_token = google.oauth2.id_token.fetch_id_token(
            auth_req, audience=config.OAUTH_CLIENT_ID
        )

    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json",
    }

    return headers


def load_json(filepath: str) -> dict:
    """
    Method to load json from a file.

    Parameters:
        filepath: string specifiing the location of the file to be loaded.

    Returns:
        dict: the json object from the specifiede file.
    """
    with open(filepath) as f:
        return json.load(f)


def create_dataset(
    filename: str, dataset: dict, session: requests.Session, headers: dict[str, str]
) -> int | None:
    """
    Method to create a dataset using either the remote new dataset function or the local version.

    Parameters:
        filename: the filename to use for the dataset
        dataset: the dataset to be created
        session: a session instance for http/s connections
        headers: the relevant headers for authentication for http/s calls

    Returns:
        int | None: status code for local function and no return for remote.
    """
    if config.API_URL.__contains__("local"):
        return _create_local_dataset(session, dataset)
    else:
        _create_remote_dataset(session, filename, dataset, headers)


def _create_local_dataset(session: requests.Session, dataset: dict) -> int:
    """
    Method to create a local dataset.

    Parameters:
        dataset: the dataset to be created
        session: a session instance for http/s connections

    Returns:
        int: status code for local function.
    """
    simulate_post_dataset_request = session.post("http://localhost:3006", json=dataset)

    return simulate_post_dataset_request.status_code


def _create_remote_dataset(
    session: requests.Session, filename: str, dataset: dict, headers: dict[str, str]
) -> None:
    """
    Method to create a remote dataset.

    Parameters:
        filename: the filename to use for the dataset
        dataset: the dataset to be created
        session: a session instance for http/s connections
        headers: the relevant headers for authentication for http/s calls

    Returns:
        None
    """
    bucket = storage_client.bucket(config.DATASET_BUCKET_NAME)
    blob = bucket.blob(filename)
    blob.upload_from_string(
        json.dumps(dataset, indent=2), content_type="application/json"
    )
    wait_until_dataset_ready(
        dataset["survey_id"], dataset["period_id"], session, headers
    )


def wait_until_dataset_ready(
    survey_id: str,
    period_id: str,
    session: requests.Session,
    headers: dict[str, str],
    attempts: int = 5,
    backoff: int = 0.5,
) -> None:
    """
    Method to wait until the specified dataset has been created. Includes exponential back off with adjustable defaults.

    Parameters:
        survey_id: the survey id of the desired dataset metadata
        period_id: the period id of the desired dataset metadata
        session: a session instance for http/s connections
        headers: the relevant headers for authentication for http/s calls
        attempts: the number of polling attempts made, this value defaults to 3 attempts
        backoff: the value determining the exponential backoff, this defaults to 0.5.
                Please note increasing this value could drastically affect runtime.

    Returns:
        None
    """
    while attempts != 0:
        test_response = session.get(
            f"{config.API_URL}/v1/dataset_metadata?survey_id={survey_id}&period_id={period_id}",
            headers=headers,
        )

        if test_response.status_code == 200:
            return
        else:
            attempts -= 1
            time.sleep(backoff)
            backoff += backoff


def cleanup() -> None:
    """
    Method to cleanup all test data created depending on local or remote run.
    Should be ran before and after test to account for test failures.

    Parameters:
        None

    Returns:
        None
    """
    if config.API_URL.__contains__("local"):
        delete_local_firestore_data()

        delete_local_bucket_data("devtools/gcp-storage-emulator/data/schema_bucket/")
        delete_local_bucket_data("devtools/gcp-storage-emulator/data/dataset_bucket/")
    else:
        delete_blobs(bucket_loader.get_dataset_bucket())
        delete_blobs(bucket_loader.get_schema_bucket())

        client = firebase_loader.get_client()

        perform_delete_transaction(
            client.transaction(),
            firebase_loader.get_datasets_collection(),
        )
        perform_delete_transaction(
            client.transaction(),
            firebase_loader.get_schemas_collection(),
        )

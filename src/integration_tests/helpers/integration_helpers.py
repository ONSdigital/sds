import json
import time

import google.oauth2.id_token
import requests
from config.config_factory import config
from repositories.buckets.bucket_loader import bucket_loader
from repositories.firebase.firebase_loader import firebase_loader
from google.cloud import storage
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from src.integration_tests.helpers.bucket_helpers import (
    delete_blobs,
    delete_blobs_with_test_survey_id,
    delete_local_bucket_data,
)
from src.integration_tests.helpers.firestore_helpers import (
    delete_local_firestore_data,
    perform_delete_on_collection_with_test_survey_id,
)
from src.integration_tests.helpers.pubsub_helper import PubSubHelper
from src.test_data.dataset_test_data import test_survey_id

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
        dict: the json object from the specified file.
    """
    with open(filepath) as f:
        return json.load(f)


def cleanup() -> None:
    """
    Method to cleanup all test data created depending on local or remote run.
    Should be ran before and after test to account for test failures.

    Parameters:
        None

    Returns:
        None
    """
    if config.OAUTH_CLIENT_ID.__contains__("local"):
        delete_local_firestore_data()

        delete_local_bucket_data("devtools/gcp-storage-emulator/data/schema_bucket/")
        delete_local_bucket_data("devtools/gcp-storage-emulator/data/dataset_bucket/")
    else:
        delete_blobs_with_test_survey_id(bucket_loader.get_schema_bucket(), test_survey_id)

        client = firebase_loader.get_client()

        perform_delete_on_collection_with_test_survey_id(
            client,
            firebase_loader.get_datasets_collection(),
            test_survey_id
        )
        perform_delete_on_collection_with_test_survey_id(
            client,
            firebase_loader.get_schemas_collection(),
            test_survey_id
        )


def pubsub_setup(pubsub_helper: PubSubHelper, subscriber_id: str) -> None:
    """Creates any subscribers that may be used in tests"""
    pubsub_helper.try_create_subscriber(subscriber_id)


def pubsub_teardown(pubsub_helper: PubSubHelper, subscriber_id: str) -> None:
    """Deletes subscribers that may have been used in tests"""
    pubsub_helper.try_delete_subscriber(subscriber_id)


def pubsub_purge_messages(pubsub_helper: PubSubHelper, subscriber_id: str) -> None:
    """Purge any messages that may have been sent to a subscriber"""   
    pubsub_helper.purge_messages(subscriber_id)


def inject_wait_time(seconds: int) -> None:
    """
    Method to inject a wait time into the test to allow resources properly spin up and tear down.

    Parameters:
        seconds: the number of seconds to wait

    Returns:
        None
    """
    time.sleep(seconds)


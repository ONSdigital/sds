import json

from app.config import settings
from app.repositories.firebase.firebase_loader import firebase_loader
from google.cloud import storage

from tests.integration_tests.helpers.firestore_helpers import (
    delete_local_firestore_data,
    perform_delete_on_collection_with_test_survey_id,
)
from tests.test_data.dataset_test_data import test_survey_id

storage_client = storage.Client()


def load_json(filepath: str) -> dict:
    """
    Method to load json from a file.

    Parameters:
        filepath: string specifying the location of the file to be loaded.

    Returns:
        dict: the json object from the specified file.
    """
    with open(filepath) as f:
        return json.load(f)


def cleanup() -> None:
    """
    Method to clean up all test data created depending on local or remote run.
    Should be run before and after test to account for test failures.

    Returns:
        None
    """
    if settings.API_URL.__contains__("local"):
        delete_local_firestore_data()
    else:
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


def is_json_response(response):
    try:
        response.json()
        return True
    except Exception:
        return False
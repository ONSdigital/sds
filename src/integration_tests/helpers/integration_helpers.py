import json
import os
import shutil
import time
from pathlib import Path

import google.auth.transport.requests
import google.oauth2.id_token
import requests
from config.config_factory import ConfigFactory
from firebase_admin import firestore
from repositories.buckets.bucket_loader import BucketLoader
from repositories.firebase.firebase_loader import FirebaseLoader
from requests.adapters import HTTPAdapter
from urllib3 import Retry

config = ConfigFactory.get_config()
bucket_loader = BucketLoader()
firebase_loader = FirebaseLoader()


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
        auth_token = google.oauth2.id_token.fetch_id_token(auth_req, config.API_URL)

    headers = {"Authorization": f"Bearer {auth_token}"}

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
    bucket = bucket_loader.get_dataset_bucket()
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
        _delete_local_firestore_data()

        _delete_local_bucket_data("devtools/gcp-storage-emulator/data/schema_bucket/")

        _delete_local_bucket_data("devtools/gcp-storage-emulator/data/dataset_bucket/")
    else:
        _delete_blobs(bucket_loader.get_dataset_bucket())

        _delete_blobs(bucket_loader.get_schema_bucket())

        _delete_collection(firebase_loader.get_datasets_collection())

        _delete_collection(firebase_loader.get_schemas_collection())


def _delete_local_firestore_data():
    """
    Method to cleanup local test data in the emulated firestore instance.

    Parameters:
        None

    Returns:
        None
    """
    requests.delete(
        f"http://localhost:8080/emulator/v1/projects/{config.PROJECT_ID}/databases/(default)/documents"
    )


def _delete_local_bucket_data(filepath: str):
    """
    Method to cleanup local test data in the bucket instance.

    Parameters:
        filepath: the filepath for the bucket instance to be deleted

    Returns:
        None
    """
    path_instance = Path(filepath)
    if Path.is_dir(path_instance):
        shutil.rmtree(path_instance)


def _delete_blobs(bucket) -> None:
    """
    Method to delete all blobs in the specified bucket.

    Parameters:
        bucket: the bucket to clean

    Returns:
        None
    """
    blobs = bucket.list_blobs()

    for blob in blobs:
        blob.delete()


def _delete_collection(collection_ref: firestore.CollectionReference) -> None:
    """
    Recursively deletes the collection and its subcollections.
    Parameters:
    collection_ref (firestore.CollectionReference): the reference of the collection being deleted.
    """
    doc_collection = collection_ref.stream()

    for doc in doc_collection:
        _recursively_delete_document_and_sub_collections(doc.reference)


def _recursively_delete_document_and_sub_collections(
    doc_ref: firestore.DocumentReference,
) -> None:
    """
    Loops through each collection in a document and deletes the collection.
    Parameters:
    doc_ref (firestore.DocumentReference): the reference of the document being deleted.
    """
    for collection_ref in doc_ref.collections():
        _delete_collection(collection_ref)

    doc_ref.delete()


def get_dataset_bucket():
    return bucket_loader.get_dataset_bucket()

from fastapi import status

from tests.test_config.endpoints import ENDPOINTS, COLLECTION_END
from tests.test_config.endpoints_loader import EndpointsLoader
from tests.test_data import dataset_test_data, shared_test_data
from tests.unit_tests.helpers.firestore_helpers import setup_mock_data

endpoints_loader = EndpointsLoader(ENDPOINTS)

def test_post_collection_exercise_end_200_response(dataset_collection_mock, deletion_collection_mock, test_client):
    """
    When a valid collection exercise end message is posted with a dataset_guid,
    the endpoint must return 200 with an accepted message.
    """
    # Set up mock data to simulate existing 2 dataset metadata in the collection
    setup_mock_data(
        mock_collection=dataset_collection_mock,
        mock_data=dataset_test_data.test_dataset_metadata_1.__dict__,
        mock_guid=shared_test_data.test_guid,
    )

    setup_mock_data(
        mock_collection=dataset_collection_mock,
        mock_data=dataset_test_data.test_dataset_metadata_2.__dict__,
        mock_guid=shared_test_data.test_guid_2,
    )

    # Set up mock data to simulate existing dataset metadata for another survey in the collection
    setup_mock_data(
        mock_collection=dataset_collection_mock,
        mock_data=dataset_test_data.test_dataset_metadata_other.__dict__,
        mock_guid=shared_test_data.test_guid_3,
    )

    response = endpoints_loader.send_request(
        client=test_client,
        key=COLLECTION_END,
        body=dataset_test_data.test_data_raw_collection_end.__dict__,
    )

    assert response.status_code == status.HTTP_200_OK
    message = response.json()

    # Check that the message is accepted and the dataset_delete_guid_list contains the expected dataset GUIDs
    assert message["message"] == "accepted"
    assert len(message["dataset_delete_guid_list"]) == 2
    assert shared_test_data.test_guid in message["dataset_delete_guid_list"]
    assert shared_test_data.test_guid_2 in message["dataset_delete_guid_list"]


def test_post_collection_exercise_end_dataset_not_found(dataset_collection_mock, deletion_collection_mock, test_client):
    """
    When a valid collection exercise end message is posted with a dataset_guid but the dataset metadata is not found in the collection,
    the endpoint must return 200 with an accepted message (no deletion is triggered but the message is accepted).
    """
    # Set up mock data to simulate existing 2 dataset metadata in the collection
    setup_mock_data(
        mock_collection=dataset_collection_mock,
        mock_data=dataset_test_data.test_dataset_metadata_1.__dict__,
        mock_guid=shared_test_data.test_guid,
    )

    setup_mock_data(
        mock_collection=dataset_collection_mock,
        mock_data=dataset_test_data.test_dataset_metadata_2.__dict__,
        mock_guid=shared_test_data.test_guid_2,
    )

    response = endpoints_loader.send_request(
        client=test_client,
        key=COLLECTION_END,
        body=dataset_test_data.test_data_raw_collection_end_dataset_guid_not_found.__dict__,
    )

    assert response.status_code == status.HTTP_200_OK
    message = response.json()

    # Check that the message is accepted and the dataset_delete_guid_list contains the expected dataset GUIDs
    assert message["message"] == "accepted"
    assert message["dataset_delete_guid_list"] is None


def test_post_collection_exercise_end_missing_dataset_guid_200_response(test_client):
    """
    When a collection exercise end message is posted without a dataset_guid,
    the endpoint must still return 200 (no deletion is triggered but the message is accepted).
    """
    response = endpoints_loader.send_request(
        client=test_client,
        key=COLLECTION_END,
        body=dataset_test_data.test_data_raw_collection_end_missing_id.__dict__,
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "accepted", "dataset_delete_guid_list": None}


def test_post_collection_exercise_end_missing_data(test_client):
    """
    When a collection exercise end message is posted without any data,
    the endpoint must still return 400 with validation has failed error.
    """
    response = endpoints_loader.send_request(
        client=test_client,
        key=COLLECTION_END,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'message': 'Validation has failed', 'status': 'error'}


def test_global_error(firestore_mock, dataset_collection_mock, test_client_no_server_exception):
    """
    Checks that if app encounter a global exception error
    fastAPI will return a 500 exception with appropriate msg
    Func get_schema_metadata is patched and raised with exception
    Fixture client_no_server_exception is used to avoid exiting
    the test at exception so that the response can be validated
    """
    # Set up mock data to simulate existing 2 dataset metadata in the collection
    setup_mock_data(
        mock_collection=dataset_collection_mock,
        mock_data=dataset_test_data.test_dataset_metadata_1.__dict__,
        mock_guid=shared_test_data.test_guid,
    )

    setup_mock_data(
        mock_collection=dataset_collection_mock,
        mock_data=dataset_test_data.test_dataset_metadata_2.__dict__,
        mock_guid=shared_test_data.test_guid_2,
    )

    firestore_mock.get_deletion_collection = lambda: None

    response = endpoints_loader.send_request(
        client=test_client_no_server_exception,
        key=COLLECTION_END,
        body=dataset_test_data.test_data_raw_collection_end.__dict__,
    )

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json()["message"] == "Unable to process request"

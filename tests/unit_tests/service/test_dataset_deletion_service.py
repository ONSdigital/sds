from fastapi import status

from tests.test_config.endpoints import ENDPOINTS, COLLECTION_END
from tests.test_config.endpoints_loader import EndpointsLoader
from tests.test_data import dataset_test_data, shared_test_data
from tests.unit_tests.helpers.firestore_helpers import setup_mock_data

endpoints_loader = EndpointsLoader(ENDPOINTS)


def test_process_collection_exercise_end_message_through_endpoint(
        dataset_collection_mock,
        test_client
):
    """
    This test will always return a 200 response as there is currently no implementation of unhappy path
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
        body=dataset_test_data.test_data_collection_end.__dict__,
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "accepted"}

def test_check_if_collection_has_supplementary_data_return_true_when_dataset_id_present(dataset_delete_service_setup):
    """
    When the collection exercise end message contains dataset_guid, the check function should return true
    indicating that there is dataset to be deleted
    """

    result = dataset_delete_service_setup._check_if_collection_has_dataset_guid(
        dataset_test_data.test_data_collection_end
    )

    assert result

def test_check_if_collection_has_supplementary_data_return_false_when_dataset_id_not_present(dataset_delete_service_setup):
    """
    When the collection exercise end message does not contain dataset_guid, the check function should return false
    indicating that there is no dataset to be deleted
    """

    result = dataset_delete_service_setup._check_if_collection_has_dataset_guid(
        dataset_test_data.test_data_collection_end_missing_id
    )

    assert not result

def test_collect_metadata_for_period_and_survey_returns_list_metadata(dataset_collection_mock, dataset_delete_service_setup):
    """
    When dataset metadata collection is successfully retrieved for a survey and period there should be a list of dataset metadata returned
    matching the survey id and period id in the collection exercise end message
    and not containing dataset metadata for other surveys or periods
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

    result = dataset_delete_service_setup._collect_metadata_for_period_and_survey(
        dataset_test_data.test_data_collection_end
    )

    assert result == [dataset_metadata for dataset_metadata in dataset_test_data.test_dataset_metadata]

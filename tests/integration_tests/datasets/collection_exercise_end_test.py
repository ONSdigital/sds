from tests.integration_tests.helpers.firestore_helpers import query_collection_with_test_survey_id
from tests.integration_tests.helpers.utils import make_iap_request
from tests.test_config.endpoints import ENDPOINTS, COLLECTION_END
from tests.test_config.endpoints_loader import EndpointsLoader
from tests.test_data.dataset_test_data import collection_exercise_end_message, \
    collection_exercise_end_message_without_dataset_guid
from tests.test_data.shared_test_data import test_survey_id

endpoints_loader = EndpointsLoader(ENDPOINTS)


class TestCollectionExerciseEnd:
    """
    Integration tests for the Collection Exercise End Endpoints.
    """

    def test_collection_exercise_end_message(self, setup_dataset_for_collection_exercise_end):
        """
        Test the collection exercise end endpoint by sending a request with the collection exercise end message and checking the response.
        1. Send a request to the collection exercise end endpoint with the collection exercise end message
        2. Check the response status code and message
        3. Check the dataset_delete_guid_list in the response to ensure it contains the expected dataset IDs
        4. Check the deletion collection to ensure the datasets are marked for deletion
        """
        dataset_metadata_list = setup_dataset_for_collection_exercise_end[0]
        dataset_deletion_collection = setup_dataset_for_collection_exercise_end[1]

        url, method = endpoints_loader.formulate_url_and_method(
            key=COLLECTION_END,
        )

        response = make_iap_request(method, path=url, json=collection_exercise_end_message.__dict__)

        assert response.status_code == 204

        marked_deletion_list = query_collection_with_test_survey_id(dataset_deletion_collection, test_survey_id)
        assert len(marked_deletion_list) == 2
        for marked_deletion in marked_deletion_list:
            assert marked_deletion in [
            {
                "dataset_guid": dataset_metadata_list[1].dataset_id,
                "period_id": collection_exercise_end_message.period,
                "survey_id": collection_exercise_end_message.surveyRef,
                "end_date": collection_exercise_end_message.endDate,
                "sds_dataset_version": dataset_metadata_list[1].sds_dataset_version,
                "status": "pending",
                "mark_deleted_at": marked_deletion_list[0]["mark_deleted_at"],
                "deleted_at": "n/a",
            },
            {
                "dataset_guid": dataset_metadata_list[0].dataset_id,
                "period_id": collection_exercise_end_message.period,
                "survey_id": collection_exercise_end_message.surveyRef,
                "end_date": collection_exercise_end_message.endDate,
                "sds_dataset_version": dataset_metadata_list[0].sds_dataset_version,
                "status": "pending",
                "mark_deleted_at": marked_deletion_list[1]["mark_deleted_at"],
                "deleted_at": "n/a",
            }
        ]


    def test_collection_exercise_end_message_without_dataset_guid(self, setup_dataset_for_collection_exercise_end):
        """
        Test the collection exercise end endpoint by sending a request with the collection exercise end message and checking the response.
        1. Send a request to the collection exercise end endpoint with the collection exercise end message
        2. Check the response status code and message
        3. Check the dataset_delete_guid_list in the response to ensure it contains the expected dataset IDs
        """
        dataset_deletion_collection = setup_dataset_for_collection_exercise_end[1]

        url, method = endpoints_loader.formulate_url_and_method(
            key=COLLECTION_END,
        )

        response = make_iap_request(method, path=url, json=collection_exercise_end_message_without_dataset_guid.__dict__)

        assert response.status_code == 204

        marked_deletion_list = query_collection_with_test_survey_id(dataset_deletion_collection, test_survey_id)
        assert len(marked_deletion_list) == 0

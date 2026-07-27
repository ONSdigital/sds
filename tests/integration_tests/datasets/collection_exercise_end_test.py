from app.models.collection_exericise_end_data import CollectionExerciseEndResponse
from tests.integration_tests.helpers.utils import make_iap_request
from tests.test_config.endpoints import ENDPOINTS, COLLECTION_END
from tests.test_config.endpoints_loader import EndpointsLoader
from tests.test_data.dataset_test_data import collection_exercise_end_message, \
    collection_exercise_end_message_without_dataset_guid

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
        """
        url, method = endpoints_loader.formulate_url_and_method(
            key=COLLECTION_END,
        )

        response = make_iap_request(method, path=url, json=collection_exercise_end_message.__dict__)

        assert response.status_code == 200
        response_message =  response.json()

        assert response_message["message"] == "accepted"
        assert response_message["dataset_delete_guid_list"] == [
                setup_dataset_for_collection_exercise_end[1].dataset_id,
                setup_dataset_for_collection_exercise_end[0].dataset_id,
        ]

    def test_collection_exercise_end_message_without_dataset_guid(self, setup_dataset_for_collection_exercise_end):
        """
        Test the collection exercise end endpoint by sending a request with the collection exercise end message and checking the response.
        1. Send a request to the collection exercise end endpoint with the collection exercise end message
        2. Check the response status code and message
        3. Check the dataset_delete_guid_list in the response to ensure it contains the expected dataset IDs
        """
        url, method = endpoints_loader.formulate_url_and_method(
            key=COLLECTION_END,
        )

        response = make_iap_request(method, path=url, json=collection_exercise_end_message_without_dataset_guid.__dict__)

        assert response.status_code == 200
        response_message =  response.json()

        assert response_message["message"] == "accepted"
        assert response_message["dataset_delete_guid_list"] is None

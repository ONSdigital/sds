import os

import pytest

from app.config import settings

from tests.integration_tests.helpers.utils import make_iap_request
from tests.test_config.endpoints import ENDPOINTS, GET_DATASET_METADATA, GET_ALL_DATASET_METADATA, GET_UNIT_DATA
from tests.test_config.endpoints_loader import EndpointsLoader
from tests.test_data.dataset_test_data import (
    dataset_metadata_collection_for_endpoints_test, 
    dataset_unit_data_collection_for_endpoints_test,
    dataset_unit_data_id,
    dataset_404_test_data,
    random_string,
)

endpoints_loader = EndpointsLoader(ENDPOINTS)


class TestDatasetEndpoints:
    """
    Integration tests for the Dataset Endpoints.

    This test covers fetching metadata and unit data from firestore,
    and checking that dataset metadata and unit data is handled correctly.
    """

    def test_get_dataset_metadata_collection(self, setup_dataset):
        """
        Test the GET /v1/dataset_metadata endpoint by retrieving dataset metadata.

        - Sends a GET request to retrieve metadata for a dataset
        - Asserts the metadata retrieved matches the expected structure.
        """
        url, method = endpoints_loader.formulate_url_and_method(
            key=GET_DATASET_METADATA,
            params={
                "survey_id": dataset_metadata_collection_for_endpoints_test[0].survey_id,
                "period_id": dataset_metadata_collection_for_endpoints_test[0].period_id,
            }
        )

        response = make_iap_request(method, path=url)
        
        expected_data = [dataset_metadata_collection_for_endpoints_test[0].__dict__]

        assert response.status_code == 200
        assert response.json() == expected_data


    def test_get_all_dataset_metadata_collection(self, setup_dataset):
        """
        Test the GET /v1/dataset_metadata endpoint by retrieving all dataset metadata.

        - Sends a GET request to retrieve all metadata for a dataset
        - Asserts the metadata retrieved matches the expected structure.
        """

        url, method = endpoints_loader.formulate_url_and_method(
            key=GET_ALL_DATASET_METADATA,
        )

        response = make_iap_request(method, path=url)

        assert response.status_code == 200

        # Filter out the metadata that are not for one of the test survey_ids (existing Firestore data is unpredictable)
        test_survey_ids = [dataset_metadata.survey_id for dataset_metadata in dataset_metadata_collection_for_endpoints_test]
        filtered_response = [dataset_metadata for dataset_metadata in response.json() if dataset_metadata['survey_id'] in test_survey_ids]

        assert filtered_response == [dataset_metadata.__dict__ for dataset_metadata in dataset_metadata_collection_for_endpoints_test]


    def test_get_dataset_unit_supplementary_data(self, setup_dataset):
        """
        Test the /v1/unit_data endpoint by retrieving unit data for a dataset

        - Get request to retrieve unit data for a dataset
        - Asserts if unit data matches the expected structure
        """
        url, method = endpoints_loader.formulate_url_and_method(
            key=GET_UNIT_DATA,
            params={
                "dataset_id": dataset_unit_data_collection_for_endpoints_test[0].dataset_id,
                "identifier": dataset_unit_data_id[0],
            }
        )

        response = make_iap_request(method=method, path=url)

        assert response.status_code == 200
        assert response.json() == dataset_unit_data_collection_for_endpoints_test[0].__dict__


    def test_dataset_without_title(self, setup_dataset):
        """
        Test the /v1/dataset_metadata endpoint retrieving a dataset metadata without a title

        - Get request to retrieve a metadata missing a title
        - Assert status code is 200
        - Checks if the metadata matches the expected structure without a title
        """

        url, method = endpoints_loader.formulate_url_and_method(
            key=GET_DATASET_METADATA,
            params={
                "survey_id": dataset_metadata_collection_for_endpoints_test[1].survey_id,
                "period_id": dataset_metadata_collection_for_endpoints_test[1].period_id,
            }
        )

        response = make_iap_request(method, path=url)

        expected_data = [dataset_metadata_collection_for_endpoints_test[1].__dict__]

        assert response.status_code == 200
        assert response.json() == expected_data
    

    def test_dataset_metadata_without_survey_id(self):
        """
        Test for /v1/dataset_metadata endpoint without passing survey_id parameter
        
        - Get request to retrieve metadata without passing survey_id
        - Assert status code is 400
        - Checks the error message in the response
        """

        url, method = endpoints_loader.formulate_url_and_method(
            key=GET_DATASET_METADATA,
            params={
                "period_id": dataset_metadata_collection_for_endpoints_test[0].period_id,
            }
        )

        response = make_iap_request(method, path=url)


        assert response.status_code == 400
        assert response.json()["message"] == "Invalid search parameters provided"


    def test_dataset_metadata_without_period_id(self):
        """
        Test for /v1/dataset_metadata endpoint without passing period_id parameter
        
        - Get request to retrieve metadata without passing period_id
        - Assert status code is 400
        - Checks the error message in the response
        """

        url, method = endpoints_loader.formulate_url_and_method(
            key=GET_DATASET_METADATA,
            params={
                "survey_id": dataset_metadata_collection_for_endpoints_test[0].survey_id,
            }
        )

        response = make_iap_request(method, path=url)

        assert response.status_code == 400
        assert response.json()["message"] == "Invalid search parameters provided"


    def test_dataset_metadata_no_valid_query_params(self):
        """
        Test for /v1/dataset_metadata endpoint without passing valid query parameters
        
        - Get request to retrieve metadata without passing valid query parameters
        - Assert status code is 400
        - Checks the error message in the response
        """

        url, method = endpoints_loader.formulate_url_and_method(
            key=GET_DATASET_METADATA,
        )

        response = make_iap_request(method, path=url)

        assert response.status_code == 400
        assert response.json()["message"] == "Invalid search parameters provided"
    

    def test_dataset_metadata_garbage_query_params(self):
        """
        Test for /v1/dataset_metadata endpoint with garbage query parameters
        
        - Get request to retrieve metadata with garbage query parameters
        - Assert status code is 400
        - Checks the error message in the response
        """

        url, method = endpoints_loader.formulate_url_and_method(
            key=GET_DATASET_METADATA,
            params={
                "random_string": random_string,
            }
        )

        response = make_iap_request(method, path=url)

        assert response.status_code == 400
        assert response.json()["message"] == "Invalid search parameters provided"


    def test_dataset_metadata_404_response(self, setup_dataset):
        """
        Test for /v1/dataset_metadata endpoint when no dataset metadata is retrieved
        
        - Get request to retrieve metadata when no dataset is found
        - Assert status code is 404
        - Checks the error message in the response
        """

        url, method = endpoints_loader.formulate_url_and_method(
            key=GET_DATASET_METADATA,
            params={
                "survey_id": dataset_404_test_data['survey_id'],
                "period_id": dataset_404_test_data['period_id'],
            }
        )

        response = make_iap_request(method, path=url)

        assert response.status_code == 404
        assert response.json()["message"] == "No datasets found"


    def test_dataset_metadata_unauthorised(self):
        """
        Test the /v1/dataset_metadata endpoint with an unauthorized token
        
        - Get request to retrieve metadata with an unauthorized token
        - Assert status code is 401
        """
        if settings.CONF == "local-int-tests":
            pytest.skip("Skipping test_dataset_metadata_unauthorised on local environment")

        url, method = endpoints_loader.formulate_url_and_method(
            key=GET_DATASET_METADATA,
            params={
                "survey_id": dataset_metadata_collection_for_endpoints_test[0].survey_id,
                "period_id": dataset_metadata_collection_for_endpoints_test[0].period_id,
            }
        )

        response = make_iap_request(method, path=url, unauthenticated=True)

        assert response.status_code == 401


    def test_all_dataset_metadata_unauthorised(self):
        """
        Test the /v1/all_dataset_metadata endpoint with an unauthorized token

        - Get request to retrieve all metadata with an unauthorized token
        - Assert status code is 401
        """
        if settings.CONF == "local-int-tests":
            pytest.skip("Skipping test_all_dataset_metadata_unauthorised on local environment")

        url, method = endpoints_loader.formulate_url_and_method(
            key=GET_ALL_DATASET_METADATA,
        )

        response = make_iap_request(method, path=url, unauthenticated=True)

        assert response.status_code == 401


    def test_dataset_unit_data_without_dataset_id(self):
        """
        Test for /v1/unit_data endpoint without passing dataset_id parameter
        
        - Get request to retrieve unit data without passing dataset_id
        - Assert status code is 400
        - Checks the error message in the response
        """
        if not endpoints_loader.endpoints_deprecated:
            pytest.skip("Skipping test_dataset_unit_data_without_dataset_id on new endpoint")

        url, method = endpoints_loader.formulate_url_and_method(
            key=GET_UNIT_DATA,
            params={
                "identifier": dataset_unit_data_id[0],
            }
        )

        response = make_iap_request(method, path=url)

        assert response.status_code == 400
        assert response.json()["message"] == "Validation has failed"


    def test_dataset_unit_data_without_identifier(self):
        """
        Test for /v1/unit_data endpoint without passing identifier parameter
        
        - Get request to retrieve unit data without passing identifier
        - Assert status code is 400
        - Checks the error message in the response
        """
        if not endpoints_loader.endpoints_deprecated:
            pytest.skip("Skipping test_dataset_unit_data_without_identifier on new endpoint")

        url, method = endpoints_loader.formulate_url_and_method(
            key=GET_UNIT_DATA,
            params={
                "dataset_id": dataset_unit_data_collection_for_endpoints_test[0].dataset_id,
            }
        )

        response = make_iap_request(method, path=url)

        assert response.status_code == 400
        assert response.json()["message"] == "Validation has failed"
    

    def test_dataset_unit_data_404_response(self, setup_dataset):
        """
        Test for /v1/unit_data endpoint when no unit data is retrieved
        
        - Get request to retrieve unit data when no unit data is found
        - Assert status code is 404
        - Checks the error message in the response
        """

        url, method = endpoints_loader.formulate_url_and_method(
            key=GET_UNIT_DATA,
            params={
                "dataset_id": dataset_404_test_data['dataset_id'],
                "identifier": dataset_404_test_data['identifier'],
            }
        )

        response = make_iap_request(method, path=url)

        assert response.status_code == 404
        assert response.json()["message"] == "No unit data found"


    def test_dataset_unit_data_unauthorised(self):
        """
        Test the /v1/unit_data endpoint with an unauthorized token
        
        - Get request to retrieve unit data with an unauthorized token
        - Assert status code is 401
        """
        if settings.CONF == "local-int-tests":
            pytest.skip("Skipping test_dataset_unit_data_unauthorised on local environment")

        url, method = endpoints_loader.formulate_url_and_method(
            key=GET_UNIT_DATA,
            params={
                "dataset_id": dataset_unit_data_collection_for_endpoints_test[0].dataset_id,
                "identifier": dataset_unit_data_id[0],
            }
        )

        response = make_iap_request(method, path=url, unauthenticated=True)

        assert response.status_code == 401


    def test_dataset_unit_data_no_valid_query_params(self):
        """
        Test for /v1/unit_data endpoint without passing valid query parameters
        
        - Get request to retrieve unit data without passing valid query parameters
        - Assert status code is 400
        - Checks the error message in the response
        """
        if not endpoints_loader.endpoints_deprecated:
            pytest.skip("Skipping test_dataset_unit_data_no_valid_query_params on new endpoint")

        url, method = endpoints_loader.formulate_url_and_method(
            key=GET_UNIT_DATA,
        )

        response = make_iap_request(method, path=url)

        assert response.status_code == 400
        assert response.json()["message"] == "Validation has failed"


    def test_dataset_unit_data_garbage_query_params(self):
        """
        Test for /v1/unit_data endpoint with garbage query parameters
        
        - Get request to retrieve unit data with garbage query parameters
        - Assert status code is 400
        - Checks the error message in the response
        """
        if not endpoints_loader.endpoints_deprecated:
            pytest.skip("Skipping test_dataset_unit_data_garbage_query_params on new endpoint")

        url, method = endpoints_loader.formulate_url_and_method(
            key=GET_UNIT_DATA,
            params={
                "random_string": random_string,
            }
        )

        response = make_iap_request(method, path=url)

        assert response.status_code == 400
        assert response.json()["message"] == "Validation has failed"

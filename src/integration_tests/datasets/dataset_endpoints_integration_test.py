import pytest
from unittest import TestCase
from src.app.config.config_factory import config
from src.test_data.dataset_test_data import ( 
    dataset_metadata_collection_for_endpoints_test, 
    dataset_unit_data_collection_for_endpoints_test,
    dataset_unit_data_id
)
from repositories.firebase.firebase_loader import firebase_loader
from src.integration_tests.helpers.integration_helpers import (
    cleanup,
    generate_headers,
    setup_session,
    inject_wait_time,
)
from src.integration_tests.helpers.firestore_helpers import upload_dataset
from google.cloud import firestore


class DatasetEndpointsIntegrationTest(TestCase):
    """
    Integration tests for the Dataset Endpoints.

    This test covers fetching metadata and unit data from firestore,
    and checking that dataset metadata and unit data is handled correctly.
    """
    session = None
    headers = None
    firestore_client = None
    
    @classmethod
    def setup_class(self) -> None:
        cleanup()
        inject_wait_time(3) # Inject wait time to allow resources properly set up
        self.session = setup_session()
        self.headers = generate_headers()
        self.firestore_client = firestore.Client(project=config.PROJECT_ID, database=config.FIRESTORE_DB_NAME)
        self.dataset = upload_dataset(self.firestore_client, dataset_metadata_collection_for_endpoints_test, dataset_unit_data_collection_for_endpoints_test)
        

    @classmethod
    def teardown_class(self) -> None:
        cleanup()

    @pytest.mark.order(1)
    def test_get_dataset_metadata_collection(self):
        """
        Test the GET /v1/dataset_metadata endpoint by retrieving dataset metadata.

        - Sends a GET request to retrieve metadata for a dataset
        - Asserts the metadata retrieved matches the expected structure.
        """

        response = self.session.get(
            f"{config.API_URL}/v1/dataset_metadata?"
            f"survey_id={dataset_metadata_collection_for_endpoints_test[0]['survey_id']}&"
            f"period_id={dataset_metadata_collection_for_endpoints_test[0]['period_id']}",
            headers = self.headers
        )
        
        expected_data = [
            {
                **dataset_metadata_collection_for_endpoints_test[0],
            }
        ]

        assert response.status_code == 200
        assert response.json() == expected_data



    @pytest.mark.order(2)
    def test_get_dataset_unit_supplementary_data(self):
        """
        Test the /v1/unit_data endpoint by retrieving unit data for a dataset

        - Get request to retrieve unit data for a dataset
        - Asserts if unit data matches the expected structure
        """

        response = self.session.get(
            f"{config.API_URL}/v1/unit_data?"
            f"dataset_id={dataset_unit_data_collection_for_endpoints_test[0]['dataset_id']}&identifier={dataset_unit_data_id[0]}",
            headers = self.headers
        )

        assert response.status_code == 200
        assert response.json() == dataset_unit_data_collection_for_endpoints_test[0]


    @pytest.mark.order(3)
    def test_dataset_without_title(self):
        """
        Test the /v1/dataset_metadata endpoint retrieving a dataset metadata without a title

        - Get request to retrieve a metadata missing a title
        - Assert status code is 200
        - Checks if the metadata matches the expected structure without a title
        """

        response = self.session.get(
            f"{config.API_URL}/v1/dataset_metadata?"
            f"survey_id={dataset_metadata_collection_for_endpoints_test[1]['survey_id']}&"
            f"period_id={dataset_metadata_collection_for_endpoints_test[1]['period_id']}",
            headers = self.headers
        )

        expected_data = [
            {
                **dataset_metadata_collection_for_endpoints_test[1],
            }
        ]

        assert response.status_code == 200
        assert response.json() == expected_data
    

    @pytest.mark.order(4)
    def test_dataset_without_survey_id(self):
        """
        Test for /v1/dataset_metadata endpoint without passing survey_id parameter
        
        - Get request to retrieve metadata without passing survey_id
        - Assert status code is 400
        - Checks the error message in the response
        """
            
        response = self.session.get(
            f"{config.API_URL}/v1/dataset_metadata?"
            f"period_id={dataset_metadata_collection_for_endpoints_test[0]['period_id']}",
            headers = self.headers
        )

        assert response.status_code == 400
        assert response.json()["message"] == "Invalid search parameters provided"


    @pytest.mark.order(5)
    def test_dataset_without_period_id(self):
        """
        Test for /v1/dataset_metadata endpoint without passing period_id parameter
        
        - Get request to retrieve metadata without passing period_id
        - Assert status code is 400
        - Checks the error message in the response
        """
            
        response = self.session.get(
            f"{config.API_URL}/v1/dataset_metadata?"
            f"survey_id={dataset_metadata_collection_for_endpoints_test[0]['survey_id']}",
            headers = self.headers
        )

        assert response.status_code == 400
        assert response.json()["message"] == "Invalid search parameters provided"


    @pytest.mark.order(6)
    def test_dataset_metadata_404_response(self):
        """
        Test for /v1/dataset_metadata endpoint when no dataset metadata is retrieved
        
        - Get request to retrieve metadata when no dataset is found
        - Assert status code is 404
        - Checks the error message in the response
        """
            
        response = self.session.get(
            f"{config.API_URL}/v1/dataset_metadata?"
            f"survey_id=xyz&period_id=abc",
            headers = self.headers
        )

        assert response.status_code == 404
        assert response.json()["message"] == "No datasets found"


    @pytest.mark.order(7)
    def test_dataset_unit_data_without_dataset_id(self):
        """
        Test for /v1/unit_data endpoint without passing dataset_id parameter
        
        - Get request to retrieve unit data without passing dataset_id
        - Assert status code is 400
        - Checks the error message in the response
        """
            
        response = self.session.get(
            f"{config.API_URL}/v1/unit_data?"
            f"identifier={dataset_unit_data_id[0]}",
            headers = self.headers
        )

        assert response.status_code == 400
        assert response.json()["message"] == "Validation has failed"


    @pytest.mark.order(8)
    def test_dataset_unit_data_without_identifier(self):
        """
        Test for /v1/unit_data endpoint without passing identifier parameter
        
        - Get request to retrieve unit data without passing identifier
        - Assert status code is 400
        - Checks the error message in the response
        """
            
        response = self.session.get(
            f"{config.API_URL}/v1/unit_data?"
            f"dataset_id={dataset_unit_data_collection_for_endpoints_test[0]['dataset_id']}",
            headers = self.headers
        )

        assert response.status_code == 400
        assert response.json()["message"] == "Validation has failed"
    

    @pytest.mark.order(9)
    def test_dataset_unit_data_404_response(self):
        """
        Test for /v1/unit_data endpoint when no unit data is retrieved
        
        - Get request to retrieve unit data when no unit data is found
        - Assert status code is 404
        - Checks the error message in the response
        """
            
        response = self.session.get(
            f"{config.API_URL}/v1/unit_data?"
            f"dataset_id=xyz&identifier=abc",
            headers = self.headers
        )

        assert response.status_code == 404
        assert response.json()["message"] == "No unit data found"
        
import pytest
from unittest import TestCase
from src.app.config.config_factory import config
from src.test_data.dataset_test_data import ( 
    dataset_metadata_collection_for_endpoints_test, 
    dataset_unit_data_collection_for_endpoints_test 
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

    This test covers fetching metdata and unit data from firestore,
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
        self.firestore_client = firestore.Client(project=config.PROJECT_ID, database=f"{config.PROJECT_ID}-sds")
        self.dataset = upload_dataset(self.firestore_client, dataset_metadata_collection_for_endpoints_test, dataset_unit_data_collection_for_endpoints_test)
        

    @classmethod
    def teardown_class(self) -> None:
        cleanup()
        inject_wait_time(3) # Inject wait time to allow all message to be processed

    @pytest.mark.order(1)
    def test_get_dataset_metadata_collection(self):
        """
        Test retriving dataset metadata.

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
        Test retrieving unit data for a dataset

        - Get request to retrieve unit data for a dataset
        - Asserts if unit data matches the expected structure
        """

        response = self.session.get(
            f"{config.API_URL}/v1/unit_data?"
            f"dataset_id={dataset_unit_data_collection_for_endpoints_test[0]['dataset_id']}&identifier=43532",
            headers = self.headers
        )

        assert response.status_code == 200
        assert response.json() == dataset_unit_data_collection_for_endpoints_test[0]

    @pytest.mark.order(3)
    def test_dataset_without_title(self):
        """
        Test retrieving a dataset metadata without a title

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
        
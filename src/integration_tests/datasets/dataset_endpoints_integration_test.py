import pytest
from unittest import TestCase
from src.app.config.config_factory import config
from src.test_data.dataset_test_data import dataset_metadata_collection_endpoints
from src.test_data.dataset_test_data import dataset_unit_data_collection_endpoints
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
    session = None
    headers = None
    first_dataset = None
    second_dataset = None
    firestore_client = None
    dataset_without_title = None
    dataset_different_period_id = None
    # 3 datasets - 2 with same survey n period id. 1 with same survey id but different period id
    # each dataset more than 1 unit data (2)...
    #
    
    @classmethod
    def setup_class(self) -> None:
        cleanup()
        inject_wait_time(3) # Inject wait time to allow resources properly set up
        self.session = setup_session()
        self.headers = generate_headers()
        self.firestore_client = firestore.Client(project=config.PROJECT_ID, database=f"{config.PROJECT_ID}-sds")
        self.dataset = upload_dataset(self.firestore_client, dataset_metadata_collection_endpoints, dataset_unit_data_collection_endpoints)
        # self.second_dataset = upload_dataset(self.firestore_client, dataset_metadata_collection_endpoints[1], dataset_unit_data_collection_endpoints)
        # self.dataset_without_title = upload_dataset(self.firestore_client, [dataset_metadata_collection[2]], dataset_unit_data_collection)
        # self.dataset_different_period_id = upload_dataset(self.firestore_client, [dataset_metadata_collection[3]], dataset_unit_data_collection)
        

    @classmethod
    def teardown_class(self) -> None:
        # cleanup()
        inject_wait_time(3) # Inject wait time to allow all message to be processed
    

    # method for grabbing unit data, dataset metadata and uploading 3 but return 2 wth same survey id

    @pytest.mark.order(1)
    def test_dataset_upload_and_metadata(self):
        """
        """

        assert self.dataset is not None, "first dataset upload failed"

    @pytest.mark.order(2)
    def test_grabbing_unit_data(self):
        """
        """

        response = self.session.get(
            f"{config.API_URL}/v1/unit_data?dataset_id=0&identifier=43532",
            headers = self.headers
        )

        assert response.status_code == 200, "not found"

        unit_data = response.json()

        assert unit_data == {
        "dataset_id": "0",
        "survey_id": "test_survey_id",
        "period_id": "test_period_id",
        "schema_version": "v1.0.0",
        "form_types": ["jke", "als", "sma"],
        "data": "test",
    }

    # @pytest.mark.order()
    # def test_dataset_without_title(self):
    #     """
    #     """

    
    # @pytest.mark.order()
    # def test_dataset_with_different_period_id(self):
    #     """
    #     """


    # @pytest.mark.order()
    # def test_dataset_with_different_period_id(self):
    #     """
    #     """

    





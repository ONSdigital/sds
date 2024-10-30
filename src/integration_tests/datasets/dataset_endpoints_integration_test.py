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
import logging

class DatasetEndpointsIntegrationTest(TestCase):
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
        self.dataset = upload_dataset(self.firestore_client, dataset_metadata_collection_endpoints, dataset_unit_data_collection_endpoints)
        

    @classmethod
    def teardown_class(self) -> None:
        cleanup()
        inject_wait_time(3) # Inject wait time to allow all message to be processed

    @pytest.mark.order(1)
    def test_dataset_upload_and_metadata(self):
        """
        """

        response = self.session.get(
            f"{config.API_URL}/v1/dataset_metadata?survey_id=test_survey_id&period_id=test_period_id_2",
            headers = self.headers
        )

        assert self.dataset is not None, "Dataset upload failed"
        assert response.status_code == 200, "not found"

        metadata_data = response.json()

        assert metadata_data == [{
        "dataset_id": "3",
        "survey_id": "test_survey_id",
        "period_id": "test_period_id_2",
        "form_types": ["knj", "okn", "ojdw"],
        "title": "Which side was better?",
        "sds_published_at": "2023-04-20T12:00:00Z",
        "total_reporting_units": 2,
        "schema_version": "v1.0.0",
        "sds_dataset_version": 1,
        "filename": "test_filename.json",
        } ]

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

    @pytest.mark.order(3)
    def test_dataset_without_title(self):
        """
        """

        response = self.session.get(
            f"{config.API_URL}/v1/dataset_metadata?survey_id=test_survey_id&period_id=test_period_id",
            headers = self.headers
        )

        assert response.status_code == 200, "not found"

        metadata_without_title = response.json()

        assert metadata_without_title == [{
        "dataset_id": "1",
        "survey_id": "test_survey_id",
        "period_id": "test_period_id",
        "form_types": ["oas", "alm", "lma"],
        "sds_published_at": "2023-04-20T12:00:00Z",
        "total_reporting_units": 2,
        "schema_version": "v1.0.0",
        "sds_dataset_version": 1,
        "filename": "test_filename.json",
        }]



    





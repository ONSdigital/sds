from unittest import TestCase
from unittest.mock import MagicMock

import pytest
from models.schema_models import Schema, SchemaMetadata
from repositories.buckets.schema_bucket_repository import SchemaBucketRepository
from repositories.firebase.schema_firebase_repository import SchemaFirebaseRepository

from src.test_data import schema_test_data


class PostSchemaTest(TestCase):
    @pytest.fixture(autouse=True)
    def prepare_fixture(self, test_client):
        self.test_client = test_client

    def setUp(self):
        self.store_schema_json_stash = SchemaBucketRepository.store_schema_json
        self.get_latest_schema_with_survey_id_stash = (
            SchemaFirebaseRepository.get_latest_schema_with_survey_id
        )
        self.perform_new_schema_transaction_stash = (
            SchemaFirebaseRepository.perform_new_schema_transaction
        )

    def tearDown(self):
        SchemaBucketRepository.store_schema_json = self.store_schema_json_stash
        SchemaFirebaseRepository.get_latest_schema_with_survey_id = (
            self.get_latest_schema_with_survey_id_stash
        )
        SchemaFirebaseRepository.perform_new_schema_transaction = (
            self.perform_new_schema_transaction_stash
        )

    def test_200_response_updated_schema_version(self):
        """
        Tests when a schema is posted, a 200 response and the schema metadata will be received
        """
        SchemaBucketRepository.store_schema_json = MagicMock()
        SchemaBucketRepository.store_schema_json.return_value = None

        SchemaFirebaseRepository.get_latest_schema_with_survey_id = MagicMock()
        SchemaFirebaseRepository.get_latest_schema_with_survey_id.return_value = (
            schema_test_data.test_post_schema_metadata_first_version_response
        )

        SchemaFirebaseRepository.perform_new_schema_transaction = MagicMock()
        SchemaFirebaseRepository.perform_new_schema_transaction.return_value = (
            schema_test_data.test_post_schema_metadata_updated_version_response
        )

        response = self.test_client.post(
            "/v1/schema", json=schema_test_data.test_post_schema_metadata_body
        )

        assert response.status_code == 200
        assert (
            response.json()
            == schema_test_data.test_post_schema_metadata_updated_version_response
        )

        SchemaFirebaseRepository.perform_new_schema_transaction.assert_called_once_with(
            schema_test_data.test_guid,
            SchemaMetadata(
                **schema_test_data.test_post_schema_metadata_updated_version_response
            ),
            Schema(**schema_test_data.test_post_schema_metadata_body),
            schema_test_data.test_filename,
        )

    def test_200_response_first_schema_version(self):
        """
        Tests when there the first version of a schema is posted it should give it version 1 and return 200.
        """

        SchemaBucketRepository.store_schema_json = MagicMock()
        SchemaBucketRepository.store_schema_json.return_value = None

        SchemaFirebaseRepository.get_latest_schema_with_survey_id = MagicMock()
        SchemaFirebaseRepository.get_latest_schema_with_survey_id.return_value = []

        SchemaFirebaseRepository.perform_new_schema_transaction = MagicMock()
        SchemaFirebaseRepository.perform_new_schema_transaction.return_value = (
            schema_test_data.test_post_schema_metadata_updated_version_response
        )

        response = self.test_client.post(
            "/v1/schema", json=schema_test_data.test_post_schema_metadata_body
        )

        assert response.status_code == 200
        assert (
            response.json()
            == schema_test_data.test_post_schema_metadata_first_version_response
        )
        SchemaFirebaseRepository.perform_new_schema_transaction.assert_called_once()

    def test_post_bad_schema_400_response(self):
        """
        Checks that fastAPI returns a 400 error with appropriate
        message if the schema is badly formatted.
        """
        response = self.test_client.post(
            "/v1/schema", json={"schema": "is missing some fields"}
        )
        assert response.status_code == 400
        assert response.json()["message"] == "Validation has failed"

    def test_post_schema_transaction_exception_500_response(self):
        """
        Test the post schema transaction. A 500 response will be received
        with appropriate error message if an exception is found in new
        schema transaction
        """
        SchemaFirebaseRepository.get_latest_schema_with_survey_id = MagicMock()
        SchemaFirebaseRepository.get_latest_schema_with_survey_id.return_value = (
            schema_test_data.test_post_schema_metadata_first_version_response
        )

        SchemaFirebaseRepository.perform_new_schema_transaction = MagicMock()
        SchemaFirebaseRepository.perform_new_schema_transaction.side_effect = Exception

        response = self.test_client.post(
            "/v1/schema", json=schema_test_data.test_post_schema_metadata_body
        )

        assert response.status_code == 500
        assert response.json()["message"] == "Unable to process request"

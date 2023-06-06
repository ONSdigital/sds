import pytest
from unittest import TestCase
from unittest.mock import MagicMock

from repositories.buckets.schema_bucket_repository import SchemaBucketRepository
from repositories.firebase.schema_firebase_repository import SchemaFirebaseRepository
from repositories.firebase.firebase_transaction_handler import FirebaseTransactionHandler

from src.test_data import schema_test_data
from src.unit_tests.test_helper import TestHelper


class PostSchemaMetadataTest(TestCase):
    @pytest.fixture(autouse=True)
    def prepare_fixture(self, test_client):
        self.test_client = test_client

    def setUp(self):
        self.store_schema_json_stash = (
            SchemaBucketRepository.store_schema_json
        )
        self.get_latest_schema_with_survey_id_stash = (
            SchemaFirebaseRepository.get_latest_schema_with_survey_id
        )
        self.create_schema_in_transaction_stash = (
            SchemaFirebaseRepository.create_schema_in_transaction
        )
        self.transaction_rollback_stash = (
            FirebaseTransactionHandler.transaction_rollback
        )
        self.transaction_commit_stash = (
            FirebaseTransactionHandler.transaction_commit
        )
        self.transaction_begin_stash = (
            FirebaseTransactionHandler.transaction_begin
        
        )
        FirebaseTransactionHandler.transaction_commit = MagicMock()
        FirebaseTransactionHandler.transaction_rollback = MagicMock()
        FirebaseTransactionHandler.transaction_begin = MagicMock()


    def tearDown(self):
        SchemaBucketRepository.store_schema_json = (
            self.store_schema_json_stash
        )
        SchemaFirebaseRepository.get_latest_schema_with_survey_id = (
            self.get_latest_schema_with_survey_id_stash
        )
        SchemaFirebaseRepository.create_schema_in_transaction = (
            self.create_schema_in_transaction_stash
        )
        FirebaseTransactionHandler.transaction_rollback = (
            self.transaction_rollback_stash
        )
        FirebaseTransactionHandler.transaction_commit = (
            self.transaction_commit_stash
        )
        FirebaseTransactionHandler.transaction_begin = (
            self.transaction_begin_stash
        )

    def test_200_response_updated_schema_version(self):
        SchemaBucketRepository.store_schema_json = MagicMock()
        SchemaBucketRepository.store_schema_json.return_value = None

        SchemaFirebaseRepository.get_latest_schema_with_survey_id = MagicMock()
        SchemaFirebaseRepository.get_latest_schema_with_survey_id.return_value = (
            TestHelper.create_document_snapshot_generator_mock(
                [schema_test_data.test_post_schema_metadata_first_version_response]
            )
        )

        SchemaFirebaseRepository.create_schema_in_transaction = MagicMock()
        SchemaFirebaseRepository.create_schema_in_transaction.return_value = (
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


    def test_200_response_first_schema_version(self):
        """
        Tests when there the first version of a schema is posted it should give it version 1 and return 200.
        """

        SchemaBucketRepository.store_schema_json = MagicMock()
        SchemaBucketRepository.store_schema_json.return_value = None

        SchemaFirebaseRepository.get_latest_schema_with_survey_id = MagicMock()
        SchemaFirebaseRepository.get_latest_schema_with_survey_id.return_value = (
            TestHelper.create_document_snapshot_generator_mock([])
        )

        SchemaFirebaseRepository.create_schema_in_transaction = MagicMock()
        SchemaFirebaseRepository.create_schema_in_transaction.return_value = (
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


    def test_post_bad_schema_400_response(self):
        """
        Checks that fastAPI returns a 400 error with appropriate
        message if the schema is badly formatted.
        """
        response = self.test_client.post("/v1/schema", json={"schema": "is missing some fields"})
        assert response.status_code == 400
        assert response.json()["message"] == "Validation has failed"


    def test_data_integrity_when_store_schema_failed(self):
        """
        """
        SchemaBucketRepository.store_schema_json = MagicMock()
        SchemaBucketRepository.store_schema_json.side_effect = Exception

        SchemaFirebaseRepository.get_latest_schema_with_survey_id = MagicMock()
        SchemaFirebaseRepository.get_latest_schema_with_survey_id.return_value = (
            TestHelper.create_document_snapshot_generator_mock(
                [schema_test_data.test_post_schema_metadata_first_version_response]
            )
        )

        SchemaFirebaseRepository.create_schema_in_transaction = MagicMock()
        SchemaFirebaseRepository.create_schema_in_transaction.return_value = (
            schema_test_data.test_post_schema_metadata_updated_version_response
        )

        response = self.test_client.post(
            "/v1/schema", json=schema_test_data.test_post_schema_metadata_body
        )

        assert response.status_code == 500
        assert response.json()["message"] == "Unable to process request"

        FirebaseTransactionHandler.transaction_commit.assert_not_called()
        FirebaseTransactionHandler.transaction_rollback.assert_called_once()

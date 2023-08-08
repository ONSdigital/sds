from unittest import TestCase
from unittest.mock import MagicMock

import pytest
from config.config_factory import config
from repositories.buckets.schema_bucket_repository import SchemaBucketRepository
from repositories.firebase.schema_firebase_repository import SchemaFirebaseRepository
from services.shared.publisher_service import PublisherService

from src.test_data import schema_test_data


class PostSchemaTest(TestCase):
    @pytest.fixture(autouse=True)
    def prepare_fixture(self, test_client):
        self.test_client = test_client

    def setUp(self):
        self.store_schema_json_stash = SchemaBucketRepository.store_schema_json
        self.get_latest_schema_metadata_with_survey_id_stash = (
            SchemaFirebaseRepository.get_latest_schema_metadata_with_survey_id
        )
        self.perform_new_schema_transaction_stash = (
            SchemaFirebaseRepository.perform_new_schema_transaction
        )
        self.publish_data_to_topic_stash = PublisherService.publish_data_to_topic

    def tearDown(self):
        SchemaBucketRepository.store_schema_json = self.store_schema_json_stash
        SchemaFirebaseRepository.get_latest_schema_metadata_with_survey_id = (
            self.get_latest_schema_metadata_with_survey_id_stash
        )
        SchemaFirebaseRepository.perform_new_schema_transaction = (
            self.perform_new_schema_transaction_stash
        )
        PublisherService.publish_data_to_topic = self.publish_data_to_topic_stash

    def test_200_response_first_schema_version(self):
        """
        Tests when there the first version of a schema is posted it should give it version 1 and return 200.
        """
        SchemaBucketRepository.store_schema_json = MagicMock(return_value=None)

        SchemaFirebaseRepository.get_latest_schema_metadata_with_survey_id = MagicMock(
            return_value=None
        )
        SchemaFirebaseRepository.perform_new_schema_transaction = MagicMock(
            return_value=schema_test_data.test_post_schema_metadata_updated_version_response
        )

        PublisherService.publish_data_to_topic = MagicMock()

        response = self.test_client.post(
            f"/v1/schema?survey_id={schema_test_data.test_survey_id}",
            json=schema_test_data.test_post_schema_body,
        )

        assert response.status_code == 200
        assert (
            response.json()
            == schema_test_data.test_post_schema_metadata_first_version_response
        )
        SchemaFirebaseRepository.perform_new_schema_transaction.assert_called_once()

    def test_200_response_updated_schema_version(self):
        """
        Tests when a schema is posted, a 200 response and the schema metadata will be received
        and the appropriate message will be sent to publisher
        """
        SchemaBucketRepository.store_schema_json = MagicMock()
        SchemaBucketRepository.store_schema_json.return_value = None

        SchemaFirebaseRepository.get_latest_schema_metadata_with_survey_id = MagicMock()
        SchemaFirebaseRepository.get_latest_schema_metadata_with_survey_id.return_value = (
            schema_test_data.test_post_schema_metadata_first_version_response
        )

        SchemaFirebaseRepository.perform_new_schema_transaction = MagicMock()
        SchemaFirebaseRepository.perform_new_schema_transaction.return_value = (
            schema_test_data.test_post_schema_metadata_updated_version_response
        )

        PublisherService.publish_data_to_topic = MagicMock()

        response = self.test_client.post(
            f"/v1/schema?survey_id={schema_test_data.test_survey_id}",
            json=schema_test_data.test_post_schema_body,
        )

        assert response.status_code == 200
        assert (
            response.json()
            == schema_test_data.test_post_schema_metadata_updated_version_response
        )

        PublisherService.publish_data_to_topic.assert_called_once_with(
            schema_test_data.test_post_schema_metadata_updated_version_response,
            config.PUBLISH_SCHEMA_TOPIC_ID,
        )

        SchemaFirebaseRepository.perform_new_schema_transaction.assert_called_once_with(
            schema_test_data.test_guid,
            schema_test_data.test_post_schema_metadata_updated_version_response,
            schema_test_data.test_post_schema_body,
            schema_test_data.test_filename,
        )

    def test_post_schema_with_missing_survey_id_400_response(self):
        """
        Checks that fastAPI returns a 400 error with appropriate
        message if the schema is missing mandatory fields.
        """
        response = self.test_client.post(
            f"/v1/schema?survey_id=",
            json=schema_test_data.test_post_schema_body_missing_fields,
        )
        assert response.status_code == 400
        assert response.json()["message"] == "Validation has failed"

    def test_post_missing_fields_schema_400_response(self):
        """
        Checks that fastAPI returns a 400 error with appropriate
        message if the schema is missing mandatory fields.
        """
        response = self.test_client.post(
            f"/v1/schema?survey_id={schema_test_data.test_survey_id}",
            json=schema_test_data.test_post_schema_body_missing_fields,
        )
        assert response.status_code == 400
        assert response.json()["message"] == "Validation has failed"

    def test_post_empty_fields_schema_400_response(self):
        """
        Checks that fastAPI returns a 400 error with appropriate
        message if the schema mandatory fields have null value
        """
        response = self.test_client.post(
            f"/v1/schema?survey_id={schema_test_data.test_survey_id}",
            json=schema_test_data.test_post_schema_body_empty_properties,
        )
        assert response.status_code == 400
        assert response.json()["message"] == "Validation has failed"

    def test_post_invalid_type_fields_schema_400_response(self):
        """
        Checks that fastAPI returns a 400 error with appropriate
        message if the schema required fields are not an object
        """
        response = self.test_client.post(
            f"/v1/schema?survey_id={schema_test_data.test_survey_id}",
            json=schema_test_data.test_post_schema_body_invalid_properties_type,
        )
        assert response.status_code == 400
        assert response.json()["message"] == "Validation has failed"

    def test_post_missing_schema_version_400_response(self):
        """
        Checks that fastAPI returns a 400 error with appropriate
        message if schema version is missing
        """
        response = self.test_client.post(
            f"/v1/schema?survey_id={schema_test_data.test_survey_id}",
            json=schema_test_data.test_post_schema_body_missing_schema_version,
        )
        assert response.status_code == 400
        assert response.json()["message"] == "Validation has failed"

    def test_post_invalid_schema_version_400_response(self):
        """
        Checks that fastAPI returns a 400 error with appropriate
        message if schema version is not an object
        """
        response = self.test_client.post(
            f"/v1/schema?survey_id={schema_test_data.test_survey_id}",
            json=schema_test_data.test_post_schema_body_invalid_schema_version,
        )
        assert response.status_code == 400
        assert response.json()["message"] == "Validation has failed"

    def test_post_invalid_schema_version_const_400_response(self):
        """
        Checks that fastAPI returns a 400 error with appropriate
        message if schema version const is not a string
        """
        response = self.test_client.post(
            f"/v1/schema?survey_id={schema_test_data.test_survey_id}",
            json=schema_test_data.test_post_schema_body_invalid_schema_version_const,
        )
        assert response.status_code == 400
        assert response.json()["message"] == "Validation has failed"

    def test_post_empty_schema_version_const_400_response(self):
        """
        Checks that fastAPI returns a 400 error with appropriate
        message if schema version const is empty
        """
        response = self.test_client.post(
            f"/v1/schema?survey_id={schema_test_data.test_survey_id}",
            json=schema_test_data.test_post_schema_body_empty_schema_version_const,
        )
        assert response.status_code == 400
        assert response.json()["message"] == "Validation has failed"

    def test_post_schema_transaction_exception_500_response(self):
        """
        Test the post schema transaction. A 500 response will be received
        with appropriate error message if an exception is found in new
        schema transaction
        """
        SchemaFirebaseRepository.get_latest_schema_metadata_with_survey_id = MagicMock()
        SchemaFirebaseRepository.get_latest_schema_metadata_with_survey_id.return_value = (
            schema_test_data.test_post_schema_metadata_first_version_response
        )

        SchemaFirebaseRepository.perform_new_schema_transaction = MagicMock(
            side_effect=Exception
        )

        response = self.test_client.post(
            f"/v1/schema?survey_id={schema_test_data.test_survey_id}",
            json=schema_test_data.test_post_schema_body,
        )

        assert response.status_code == 500
        assert response.json()["message"] == "Unable to process request"

    def test_publish_schema_exception_500_response(self):
        """
        Tests when a schema is posted and the publisher raised an exception
        a 500 response will be receieved with appropriate error message and
        error log
        """
        SchemaBucketRepository.store_schema_json = MagicMock()
        SchemaBucketRepository.store_schema_json.return_value = None

        SchemaFirebaseRepository.get_latest_schema_metadata_with_survey_id = MagicMock()
        SchemaFirebaseRepository.get_latest_schema_metadata_with_survey_id.return_value = (
            schema_test_data.test_post_schema_metadata_first_version_response
        )

        SchemaFirebaseRepository.perform_new_schema_transaction = MagicMock()
        SchemaFirebaseRepository.perform_new_schema_transaction.return_value = (
            schema_test_data.test_post_schema_metadata_updated_version_response
        )

        PublisherService.publish_data_to_topic = MagicMock(side_effect=Exception)

        with self.assertLogs(level="ERROR") as lm:
            response = self.test_client.post(
                f"/v1/schema?survey_id={schema_test_data.test_survey_id}",
                json=schema_test_data.test_post_schema_body,
            )

        assert response.status_code == 500
        assert response.json()["message"] == "Unable to process request"
        self.assertEqual(
            lm.output,
            [
                "ERROR:services.schema.schema_processor_service:"
                "Error publishing schema metadata to topic."
            ],
        )

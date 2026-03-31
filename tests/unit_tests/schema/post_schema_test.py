from unittest.mock import MagicMock
import logging

from app.config import settings
from app.models.schema_models import SchemaMetadata
from app.repositories.buckets.schema_bucket_repository import SchemaBucketRepository
from app.repositories.firebase.schema_firebase_repository import SchemaFirebaseRepository
from app.services.shared.publisher_service import PublisherService

from tests.test_data import schema_test_data


class TestPostSchema:

    def test_200_response_first_schema_version(self, test_client):
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

        response = test_client.post(
            f"/v1/schema?survey_id={schema_test_data.test_survey_id}",
            json=schema_test_data.test_post_schema_body,
        )

        assert response.status_code == 200
        assert (
                response.json()
                == schema_test_data.test_post_schema_metadata_first_version_response.__dict__
        )
        SchemaFirebaseRepository.perform_new_schema_transaction.assert_called_once()

    def test_200_response_updated_schema_version(self, test_client, pubsub_mock):
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

        #PublisherService.publish_data_to_topic = MagicMock()

        response = test_client.post(
            f"/v1/schema?survey_id={schema_test_data.test_survey_id}",
            json=schema_test_data.test_post_schema_body,
        )

        assert response.status_code == 200
        assert (
                response.json()
                == schema_test_data.test_post_schema_metadata_updated_version_response
        )

        pubsub_mock.publish_data_to_topic.assert_called_once_with(
            SchemaMetadata(**schema_test_data.test_post_schema_metadata_updated_version_response),
            settings.PUBLISH_SCHEMA_TOPIC_ID,
        )

        SchemaFirebaseRepository.perform_new_schema_transaction.assert_called_once_with(
            schema_test_data.test_guid,
            SchemaMetadata(**schema_test_data.test_post_schema_metadata_updated_version_response),
            schema_test_data.test_post_schema_body,
            f"{schema_test_data.test_survey_id}/{schema_test_data.test_guid}.json",
        )

    def test_post_schema_with_invalid_dict(self, test_client):
        """
        Checks that fastAPI returns a 400 error with appropriate
        message if the schema is not a valid dictionary.
        """
        response = test_client.post(
            "/v1/schema?survey_id=",
            json="invalid_json",
        )
        assert response.status_code == 400
        assert response.json()["message"] == "Validation has failed"

    def test_post_schema_with_missing_survey_id_400_response(self, test_client):
        """
        Checks that fastAPI returns a 400 error with appropriate
        message if the schema is missing mandatory fields.
        """
        response = test_client.post(
            "/v1/schema?survey_id=",
            json=schema_test_data.test_post_schema_body_missing_fields,
        )
        assert response.status_code == 400
        assert response.json()["message"] == "Validation has failed"

    def test_post_missing_fields_schema_400_response(self, test_client):
        """
        Checks that fastAPI returns a 400 error with appropriate
        message if the schema is missing mandatory fields.
        """
        response = test_client.post(
            f"/v1/schema?survey_id={schema_test_data.test_survey_id}",
            json=schema_test_data.test_post_schema_body_missing_fields,
        )
        assert response.status_code == 400
        assert response.json()["message"] == "Validation has failed"

    def test_post_empty_fields_schema_400_response(self, test_client):
        """
        Checks that fastAPI returns a 400 error with appropriate
        message if the schema mandatory fields have null value
        """
        response = test_client.post(
            f"/v1/schema?survey_id={schema_test_data.test_survey_id}",
            json=schema_test_data.test_post_schema_body_empty_properties,
        )
        assert response.status_code == 400
        assert response.json()["message"] == "Validation has failed"

    def test_post_invalid_type_fields_schema_400_response(self, test_client):
        """
        Checks that fastAPI returns a 400 error with appropriate
        message if the schema required fields are not an object
        """
        response = test_client.post(
            f"/v1/schema?survey_id={schema_test_data.test_survey_id}",
            json=schema_test_data.test_post_schema_body_invalid_properties_type,
        )
        assert response.status_code == 400
        assert response.json()["message"] == "Validation has failed"

    def test_post_missing_schema_version_400_response(self, test_client):
        """
        Checks that fastAPI returns a 400 error with appropriate
        message if schema version is missing
        """
        response = test_client.post(
            f"/v1/schema?survey_id={schema_test_data.test_survey_id}",
            json=schema_test_data.test_post_schema_body_missing_schema_version,
        )
        assert response.status_code == 400
        assert response.json()["message"] == "Validation has failed"

    def test_post_invalid_schema_version_400_response(self, test_client):
        """
        Checks that fastAPI returns a 400 error with appropriate
        message if schema version is not an object
        """
        response = test_client.post(
            f"/v1/schema?survey_id={schema_test_data.test_survey_id}",
            json=schema_test_data.test_post_schema_body_invalid_schema_version,
        )
        assert response.status_code == 400
        assert response.json()["message"] == "Validation has failed"

    def test_post_invalid_schema_version_const_400_response(self, test_client):
        """
        Checks that fastAPI returns a 400 error with appropriate
        message if schema version const is not a string
        """
        response = test_client.post(
            f"/v1/schema?survey_id={schema_test_data.test_survey_id}",
            json=schema_test_data.test_post_schema_body_invalid_schema_version_const,
        )
        assert response.status_code == 400
        assert response.json()["message"] == "Validation has failed"

    def test_post_empty_schema_version_const_400_response(self, test_client):
        """
        Checks that fastAPI returns a 400 error with appropriate
        message if schema version const is empty
        """
        response = test_client.post(
            f"/v1/schema?survey_id={schema_test_data.test_survey_id}",
            json=schema_test_data.test_post_schema_body_empty_schema_version_const,
        )
        assert response.status_code == 400
        assert response.json()["message"] == "Validation has failed"

    def test_post_missing_title_400_response(self, test_client):
        """
        Checks that fastAPI returns a 400 error with appropriate
        message if title is missing
        """
        response = test_client.post(
            f"/v1/schema?survey_id={schema_test_data.test_survey_id}",
            json=schema_test_data.test_post_schema_body_missing_title,
        )
        assert response.status_code == 400
        assert response.json()["message"] == "Validation has failed"

    def test_post_empty_title_400_response(self, test_client):
        """
        Checks that fastAPI returns a 400 error with appropriate
        message if title is empty
        """
        response = test_client.post(
            f"/v1/schema?survey_id={schema_test_data.test_survey_id}",
            json=schema_test_data.test_post_schema_body_empty_title,
        )
        assert response.status_code == 400
        assert response.json()["message"] == "Validation has failed"

    def test_post_schema_transaction_exception_500_response(self, test_client):
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

        response = test_client.post(
            f"/v1/schema?survey_id={schema_test_data.test_survey_id}",
            json=schema_test_data.test_post_schema_body,
        )

        assert response.status_code == 500
        assert response.json()["message"] == "Unable to process request"

    def test_publish_schema_exception_500_response(self, caplog, test_client, pubsub_mock):
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

        pubsub_mock.publish_data_to_topic = MagicMock(side_effect=Exception)

        with caplog.at_level(logging.ERROR, logger="app.services.schema.schema_processor_service"):
            response = test_client.post(
                f"/v1/schema?survey_id={schema_test_data.test_survey_id}",
                json=schema_test_data.test_post_schema_body,
            )

        assert response.status_code == 500
        assert response.json()["message"] == "Unable to process request"
        assert any(
            "Error publishing schema metadata to topic." in message for message in caplog.text.splitlines()
        )

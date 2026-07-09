from unittest.mock import MagicMock
from fastapi import status
import logging

from app.config import settings
from tests.test_config.endpoints import ENDPOINTS, POST_SCHEMA
from tests.test_config.endpoints_loader import EndpointsLoader

from tests.test_data import schema_test_data
from tests.unit_tests.helpers.firestore_helpers import setup_mock_data

endpoints_loader = EndpointsLoader(ENDPOINTS)


def test_200_response_first_schema_version(test_client):
    """
    Tests when there the first version of a schema is posted it should give it version 1 and return 200.
    """
    response = endpoints_loader.send_request(
        client=test_client,
        key=POST_SCHEMA,
        params={"survey_id": schema_test_data.test_survey_id},
        body=schema_test_data.test_schema,
    )

    assert response.status_code == status.HTTP_200_OK
    assert (
            response.json()
            == schema_test_data.test_schema_metadata_1.__dict__
    )


def test_200_response_updated_schema_version(schema_collection_mock, pubsub_mock, test_client):
    """
    Tests when a schema is posted, a 200 response and the schema metadata will be received
    and the appropriate message will be sent to publisher
    """
    # Set up mock data to simulate existing schema metadata in the collection
    setup_mock_data(
        mock_collection=schema_collection_mock,
        mock_data=schema_test_data.test_schema_metadata_1.__dict__,
        mock_guid=schema_test_data.test_guid,
    )

    response = endpoints_loader.send_request(
        client=test_client,
        key=POST_SCHEMA,
        params={"survey_id": schema_test_data.test_survey_id},
        body=schema_test_data.test_schema,
    )

    assert response.status_code == status.HTTP_200_OK
    assert (
            response.json()
            == schema_test_data.test_schema_metadata_2.__dict__
    )

    pubsub_mock.publish_data_to_topic.assert_called_once_with(
        schema_test_data.test_schema_metadata_2,
        settings.PUBLISH_SCHEMA_TOPIC_ID,
    )


def test_post_schema_with_invalid_dict(test_client):
    """
    Checks that fastAPI returns a 400 error with appropriate
    message if the schema is not a valid dictionary.
    """
    response = endpoints_loader.send_request(
        client=test_client,
        key=POST_SCHEMA,
        params={"survey_id": schema_test_data.test_survey_id},
        body="invalid_json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["message"] == "Validation has failed"


def test_post_schema_with_missing_survey_id_400_response(test_client):
    """
    Checks that fastAPI returns a 400 error with appropriate
    message if the schema is missing mandatory fields.
    """
    response = endpoints_loader.send_request(
        client=test_client,
        key=POST_SCHEMA,
        params={"survey_id": ""},
        body=schema_test_data.test_schema,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["message"] == "Validation has failed"


def test_post_missing_fields_schema_400_response(test_client):
    """
    Checks that fastAPI returns a 400 error with appropriate
    message if the schema is missing mandatory fields.
    """
    response = endpoints_loader.send_request(
        client=test_client,
        key=POST_SCHEMA,
        params={"survey_id": schema_test_data.test_survey_id},
        body=schema_test_data.test_post_schema_body_missing_fields,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["message"] == "Validation has failed"


def test_post_empty_fields_schema_400_response(test_client):
    """
    Checks that fastAPI returns a 400 error with appropriate
    message if the schema mandatory fields have null value
    """
    response = endpoints_loader.send_request(
        client=test_client,
        key=POST_SCHEMA,
        params={"survey_id": schema_test_data.test_survey_id},
        body=schema_test_data.test_post_schema_body_empty_properties,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["message"] == "Validation has failed"


def test_post_invalid_type_fields_schema_400_response(test_client):
    """
    Checks that fastAPI returns a 400 error with appropriate
    message if the schema required fields are not an object
    """
    response = endpoints_loader.send_request(
        client=test_client,
        key=POST_SCHEMA,
        params={"survey_id": schema_test_data.test_survey_id},
        body=schema_test_data.test_post_schema_body_invalid_properties_type,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["message"] == "Validation has failed"


def test_post_missing_schema_version_400_response(test_client):
    """
    Checks that fastAPI returns a 400 error with appropriate
    message if schema version is missing
    """
    response = endpoints_loader.send_request(
        client=test_client,
        key=POST_SCHEMA,
        params={"survey_id": schema_test_data.test_survey_id},
        body=schema_test_data.test_post_schema_body_missing_schema_version,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["message"] == "Validation has failed"


def test_post_invalid_schema_version_400_response(test_client):
    """
    Checks that fastAPI returns a 400 error with appropriate
    message if schema version is not an object
    """
    response = endpoints_loader.send_request(
        client=test_client,
        key=POST_SCHEMA,
        params={"survey_id": schema_test_data.test_survey_id},
        body=schema_test_data.test_post_schema_body_invalid_schema_version,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["message"] == "Validation has failed"


def test_post_invalid_schema_version_const_400_response(test_client):
    """
    Checks that fastAPI returns a 400 error with appropriate
    message if schema version const is not a string
    """
    response = endpoints_loader.send_request(
        client=test_client,
        key=POST_SCHEMA,
        params={"survey_id": schema_test_data.test_survey_id},
        body=schema_test_data.test_post_schema_body_invalid_schema_version_const,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["message"] == "Validation has failed"


def test_post_empty_schema_version_const_400_response(test_client):
    """
    Checks that fastAPI returns a 400 error with appropriate
    message if schema version const is empty
    """
    response = endpoints_loader.send_request(
        client=test_client,
        key=POST_SCHEMA,
        params={"survey_id": schema_test_data.test_survey_id},
        body=schema_test_data.test_post_schema_body_empty_schema_version_const,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["message"] == "Validation has failed"


def test_post_missing_title_400_response(test_client):
    """
    Checks that fastAPI returns a 400 error with appropriate
    message if title is missing
    """
    response = endpoints_loader.send_request(
        client=test_client,
        key=POST_SCHEMA,
        params={"survey_id": schema_test_data.test_survey_id},
        body=schema_test_data.test_post_schema_body_missing_title,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["message"] == "Validation has failed"


def test_post_empty_title_400_response(test_client):
    """
    Checks that fastAPI returns a 400 error with appropriate
    message if title is empty
    """
    response = endpoints_loader.send_request(
        client=test_client,
        key=POST_SCHEMA,
        params={"survey_id": schema_test_data.test_survey_id},
        body=schema_test_data.test_post_schema_body_empty_title,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["message"] == "Validation has failed"


def test_post_schema_transaction_exception_500_response(firestore_mock, test_client):
    """
    Test the post schema transaction. A 500 response will be received
    with appropriate error message if an exception is found in new
    schema transaction
    """
    firestore_mock.set_transaction = MagicMock(side_effect=Exception)

    response = endpoints_loader.send_request(
        client=test_client,
        key=POST_SCHEMA,
        params={"survey_id": schema_test_data.test_survey_id},
        body=schema_test_data.test_schema,
    )

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json()["message"] == "Unable to process request"


def test_publish_schema_exception_500_response(
        caplog, pubsub_mock, test_client):
    """
    Tests when a schema is posted and the publisher raised an exception
    a 500 response will be received with appropriate error message and
    error log
    """
    pubsub_mock.publish_data_to_topic = MagicMock(side_effect=Exception)

    with caplog.at_level(logging.ERROR, logger="app.services.schema.schema_processor_service"):
        response = endpoints_loader.send_request(
            client=test_client,
            key=POST_SCHEMA,
            params={"survey_id": schema_test_data.test_survey_id},
            body=schema_test_data.test_schema,
        )

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json()["message"] == "Unable to process request"
    assert any(
        "Error publishing schema metadata to topic." in message for message in caplog.text.splitlines()
    )

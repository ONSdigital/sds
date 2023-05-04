from unittest.mock import MagicMock

from repositories.buckets.schema_bucket_repository import SchemaBucketRepository
from repositories.firebase.schema_firebase_repository import SchemaFirebaseRepository

from src.test_data import schema_test_data
from src.unit_tests.test_helper import TestHelper


def test_200_response_updated_schema_version(test_client, uuid_mock, datetime_mock):
    SchemaBucketRepository.store_schema_json = MagicMock()
    SchemaBucketRepository.store_schema_json.return_value = None

    SchemaFirebaseRepository.get_current_version_survey_schema = MagicMock()
    SchemaFirebaseRepository.get_current_version_survey_schema.return_value = (
        TestHelper.create_document_snapshot_generator_mock(
            [schema_test_data.test_schema_latest_version]
        )
    )

    SchemaFirebaseRepository.create_schema = MagicMock()
    SchemaFirebaseRepository.create_schema.return_value = (
        schema_test_data.test_post_schema_metadata_updated_version_response
    )

    response = test_client.post(
        "/v1/schema", json=schema_test_data.test_post_schema_metadata_body
    )

    assert response.status_code == 200
    assert (
        response.json()
        == schema_test_data.test_post_schema_metadata_updated_version_response
    )


def test_200_response_first_schema_version(test_client, uuid_mock, datetime_mock):
    SchemaBucketRepository.store_schema_json = MagicMock()
    SchemaBucketRepository.store_schema_json.return_value = None

    SchemaFirebaseRepository.get_current_version_survey_schema = MagicMock()
    SchemaFirebaseRepository.get_current_version_survey_schema.return_value = (
        TestHelper.create_document_snapshot_generator_mock([])
    )

    SchemaFirebaseRepository.create_schema = MagicMock()
    SchemaFirebaseRepository.create_schema.return_value = (
        schema_test_data.test_post_schema_metadata_updated_version_response
    )

    response = test_client.post(
        "/v1/schema", json=schema_test_data.test_post_schema_metadata_body
    )

    assert response.status_code == 200
    assert (
        response.json()
        == schema_test_data.test_post_schema_metadata_first_version_response
    )

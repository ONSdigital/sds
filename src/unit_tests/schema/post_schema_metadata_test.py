import logging
from unittest.mock import MagicMock, patch

from repositories.buckets.schema_bucket_repository import SchemaBucketRepository
from repositories.schema_repository import SchemaRepository

from src.test_data import schema_test_data
from src.unit_tests.test_helper import TestHelper


def test_post_schema_metadata_200_response(test_client, uuid_mock, datetime_mock):
    SchemaBucketRepository.store_schema_json = MagicMock()
    SchemaBucketRepository.store_schema_json.return_value = None

    SchemaRepository.get_current_version_survey_schema = MagicMock()
    SchemaRepository.get_current_version_survey_schema.return_value = (
        TestHelper.create_document_snapshot_generator_mock(
            [schema_test_data.test_schema_latest_version]
        )
    )

    SchemaRepository.create_schema = MagicMock()
    SchemaRepository.create_schema.return_value = (
        schema_test_data.test_post_schema_metadata_response
    )

    response = test_client.post(
        "/v1/schema", json=schema_test_data.test_post_schema_metadata_body
    )

    assert response.status_code == 200
    assert response.json() == schema_test_data.test_post_schema_metadata_response

import logging
from unittest.mock import MagicMock, patch

from repositories.buckets.schema_bucket_repository import SchemaBucketRepository
from repositories.schema_repository import SchemaRepository

from src.test_data import dataset_test_data
from src.unit_tests.test_helper import TestHelper

test_schema_latest_version = {
    "guid": dataset_test_data.test_dataset_id,
    "schema_location": "test_survey_id/test_dataset_id.json",
    "sds_published_at": "2023-04-20T12:00:00Z",
    "sds_schema_version": 1,
    "survey_id": "test_survey_id",
}

test_post_schema_body = {
    "guid": dataset_test_data.test_dataset_id,
    "schema_location": "test_survey_id/test_dataset_id.json",
    "sds_published_at": "2023-04-20T12:00:00Z",
    "sds_schema_version": 2,
    "survey_id": "test_survey_id",
}

test_schema_metadata_body = {
    "$schema": "test-schema",
    "$id": "test-id",
    "survey_id": "test_survey_id",
    "title": "test title",
    "description": "test description",
    "schema_version": "v1.0.0",
    "sample_unit_key_field": "test_ref",
    "properties": [],
    "examples": [],
}


def test_post_schema_metadata_200_response(test_client, uuid_mock, datetime_mock):
    SchemaBucketRepository.store_schema_json = MagicMock()
    SchemaBucketRepository.store_schema_json.return_value = None

    SchemaRepository.get_current_version_survey_schema = MagicMock()
    SchemaRepository.get_current_version_survey_schema.return_value = (
        TestHelper.create_document_snapshot_generator_mock([test_schema_latest_version])
    )

    SchemaRepository.create_schema = MagicMock()
    SchemaRepository.create_schema.return_value = test_post_schema_body

    response = test_client.post("/v1/schema", json=test_schema_metadata_body)

    assert response.status_code == 200
    assert response.json() == test_post_schema_body

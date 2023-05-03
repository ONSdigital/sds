from unittest.mock import MagicMock

from models.schema_models import SchemaMetadata, SchemaMetadataWithGuid
from repositories.firebase.schema_firebase_repository import SchemaFirebaseRepository

from src.unit_tests.test_helper import TestHelper

test_schema_metadata_collection_with_guid = [
    {
        "survey_id": "test_survey_id",
        "schema_location": "test_schema_location",
        "sds_schema_version": 1,
        "sds_published_at": "test_published_time",
        "guid": "id_0",
    },
    {
        "survey_id": "test_survey_id",
        "schema_location": "test_schema_location",
        "sds_schema_version": 2,
        "sds_published_at": "test_published_time",
        "guid": "id_1",
    },
]

test_schema_metadata_collection = [
    {
        "survey_id": "test_survey_id",
        "schema_location": "test_schema_location",
        "sds_schema_version": 1,
        "sds_published_at": "test_published_time",
    },
    {
        "survey_id": "test_survey_id",
        "schema_location": "test_schema_location",
        "sds_schema_version": 2,
        "sds_published_at": "test_published_time",
    },
]


def test_get_schema_metadata_collection_200_response(test_client):
    """
    When the schema is retrieved successfully from the bucket there should be a 200 status code and expected response.
    """
    SchemaFirebaseRepository.get_schema_metadata_collection = MagicMock()
    SchemaFirebaseRepository.get_schema_metadata_collection.return_value = (
        TestHelper.create_document_snapshot_generator_mock(
            test_schema_metadata_collection
        )
    )

    response = test_client.get("/v1/schema_metadata?survey_id=test_survey_id")

    assert response.status_code == 200
    assert response.json() == test_schema_metadata_collection_with_guid

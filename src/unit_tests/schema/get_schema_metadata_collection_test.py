from unittest.mock import MagicMock

from repositories.firebase.schema_firebase_repository import SchemaFirebaseRepository

from src.test_data import schema_test_data
from src.unit_tests.test_helper import TestHelper


def test_get_schema_metadata_collection_200_response(test_client):
    """
    When the schema is retrieved successfully from the bucket there should be a 200 status code and expected response.
    """
    SchemaFirebaseRepository.get_schema_metadata_collection = MagicMock()
    SchemaFirebaseRepository.get_schema_metadata_collection.return_value = (
        TestHelper.create_document_snapshot_generator_mock(
            schema_test_data.test_schema_metadata_collection_without_guid
        )
    )

    response = test_client.get("/v1/schema_metadata?survey_id=test_survey_id")

    assert response.status_code == 200
    assert response.json() == schema_test_data.test_schema_metadata_collection
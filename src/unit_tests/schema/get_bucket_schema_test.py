from unittest.mock import MagicMock

from repositories.buckets.schema_bucket_repository import SchemaBucketRepository
from repositories.firebase.schema_firebase_repository import SchemaFirebaseRepository

from src.test_data import schema_test_data


def test_get_bucket_schema_200_response(test_client):
    """
    When the schema is retrieved successfully from the bucket there should be a 200 status code and expected response.
    """
    SchemaFirebaseRepository.get_schema_metadata_bucket_location = MagicMock()
    SchemaFirebaseRepository.get_schema_metadata_bucket_location.return_value = (
        "test_location"
    )

    SchemaBucketRepository.get_bucket_file_as_json = MagicMock()
    SchemaBucketRepository.get_bucket_file_as_json.return_value = (
        schema_test_data.test_schema_bucket_metadata_response
    )

    response = test_client.get("/v1/schema?survey_id=test_survey_id&version=2")

    assert response.status_code == 200
    assert response.json() == schema_test_data.test_schema_bucket_metadata_response


def test_get_bucket_schema_404_response(test_client):
    """
    When the schema is unsuccessfully from the bucket there should be a 404 status code and expected response.
    """
    SchemaFirebaseRepository.get_schema_metadata_bucket_location = MagicMock()
    SchemaFirebaseRepository.get_schema_metadata_bucket_location.return_value = None

    SchemaBucketRepository.get_bucket_file_as_json = MagicMock()
    SchemaBucketRepository.get_bucket_file_as_json.return_value = (
        schema_test_data.test_schema_bucket_metadata_response
    )

    response = test_client.get("/v1/schema?survey_id=test_survey_id&version=2")

    assert response.status_code == 404

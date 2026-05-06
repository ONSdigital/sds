from unittest.mock import MagicMock

from app.repositories.firebase.schema_firebase_repository import SchemaFirebaseRepository

from tests.test_data import schema_test_data


def test_get_schema_metadata_collection_200_response(test_client):
    """
    When the schema is retrieved successfully from the bucket there should be a 200 status code and expected response.
    """
    SchemaFirebaseRepository.get_schema_metadata_collection = MagicMock()
    SchemaFirebaseRepository.get_schema_metadata_collection.return_value = (
        schema_test_data.test_schema_metadata_collection
    )

    response = test_client.get("/v1/schema_metadata?survey_id=test_survey_id")

    assert response.status_code == 200
    assert response.json() == [schema_metadata.__dict__ for schema_metadata in schema_test_data.test_schema_metadata_collection]


def test_get_schema_metadata_with_incorrect_key(test_client):
    """
    Checks that fastAPI return 400 error with appropriate msg
    when incorrect key is used to query schema metadata
    at get_schemas_metadata endpoint
    """
    response = test_client.get("/v1/schema_metadata?abc=123")

    assert response.status_code == 400
    assert response.json()["message"] == "Invalid search provided"


def test_get_schema_metadata_with_not_found_error(test_client):
    """
    Checks that fastAPI return 404 error with appropriate msg
    when schema metadata is not found at get_schemas_metadata
    endpoint
    """
    tmp_storage = SchemaFirebaseRepository.get_schema_metadata_collection
    SchemaFirebaseRepository.get_schema_metadata_collection = MagicMock()
    SchemaFirebaseRepository.get_schema_metadata_collection.return_value = {}

    response = test_client.get("/v1/schema_metadata?survey_id=123")

    assert response.status_code == 404
    assert response.json()["message"] == "No results found"

    SchemaFirebaseRepository.get_schema_metadata_collection = tmp_storage


def test_get_all_schema_metadata_collection_200_response(test_client):
    """
    When the schema is retrieved successfully from the bucket there should be a 200 status code and expected response.
    """
    SchemaFirebaseRepository.get_all_schema_metadata_collection = MagicMock()
    SchemaFirebaseRepository.get_all_schema_metadata_collection.return_value = (
        schema_test_data.test_schema_metadata_collection
    )

    response = test_client.get("/v1/all_schema_metadata?survey_id=test_survey_id")

    assert response.status_code == 200
    assert response.json() == [schema_metadata.__dict__ for schema_metadata in schema_test_data.test_schema_metadata_collection]


def test_get_all_schema_metadata_collection_404_response(test_client):
    """
    When the schema metadata collection is not found in firestore there should be a 404 status code and expected response.
    """
    SchemaFirebaseRepository.get_all_schema_metadata_collection = MagicMock()
    SchemaFirebaseRepository.get_all_schema_metadata_collection.return_value = []

    response = test_client.get("/v1/all_schema_metadata?survey_id=test_survey_id")

    assert response.status_code == 404
    assert response.json()["message"] == "No results found"

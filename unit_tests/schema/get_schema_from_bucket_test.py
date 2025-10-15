from unittest.mock import MagicMock

from app.repositories.buckets.schema_bucket_repository import SchemaBucketRepository
from app.repositories.firebase.schema_firebase_repository import SchemaFirebaseRepository
from app.services.schema.schema_processor_service import SchemaProcessorService

from test_data import schema_test_data


def test_get_schema_from_bucket_200_response(test_client):
    """
    When the schema is retrieved successfully from the bucket there should be a 200 status code and expected response.
    """
    tmp_storage_1 = SchemaFirebaseRepository.get_schema_bucket_filename
    SchemaFirebaseRepository.get_schema_bucket_filename = MagicMock()
    SchemaFirebaseRepository.get_schema_bucket_filename.return_value = "test_location"

    tmp_storage_2 = SchemaBucketRepository.get_schema_file_as_json
    SchemaBucketRepository.get_schema_file_as_json = MagicMock()
    SchemaBucketRepository.get_schema_file_as_json.return_value = (
        schema_test_data.test_schema_response
    )

    response = test_client.get("/v1/schema?survey_id=test_survey_id&version=2")

    assert response.status_code == 200
    assert response.json() == schema_test_data.test_schema_response

    SchemaFirebaseRepository.get_schema_bucket_filename = tmp_storage_1
    SchemaBucketRepository.get_schema_file_as_json = tmp_storage_2


def test_get_latest_schema_from_bucket_without_version(test_client):
    """
    When the schema is queried without version no, the schema of latest version
    should be returned with a 200 status code
    """
    tmp_storage_1 = SchemaFirebaseRepository.get_latest_schema_bucket_filename
    SchemaFirebaseRepository.get_latest_schema_bucket_filename = MagicMock()
    SchemaFirebaseRepository.get_latest_schema_bucket_filename.return_value = (
        "test_location"
    )

    tmp_storage_2 = SchemaBucketRepository.get_schema_file_as_json
    SchemaBucketRepository.get_schema_file_as_json = MagicMock()
    SchemaBucketRepository.get_schema_file_as_json.return_value = (
        schema_test_data.test_schema_response
    )

    response = test_client.get("/v1/schema?survey_id=test_survey_id")

    assert response.status_code == 200
    assert response.json() == schema_test_data.test_schema_response

    SchemaFirebaseRepository.get_latest_schema_bucket_filename = tmp_storage_1
    SchemaBucketRepository.get_schema_file_as_json = tmp_storage_2


def test_get_schema_from_bucket_with_guid(test_client):
    """
    When the schema is queried without version no, the schema of latest version
    should be returned with a 200 status code
    """
    tmp_storage_1 = SchemaFirebaseRepository.get_schema_bucket_filename_with_guid
    SchemaFirebaseRepository.get_schema_bucket_filename_with_guid = MagicMock()
    SchemaFirebaseRepository.get_schema_bucket_filename_with_guid.return_value = (
        "test_location"
    )

    tmp_storage_2 = SchemaBucketRepository.get_schema_file_as_json
    SchemaBucketRepository.get_schema_file_as_json = MagicMock()
    SchemaBucketRepository.get_schema_file_as_json.return_value = (
        schema_test_data.test_schema_response
    )

    response = test_client.get("/v2/schema?guid=test_guid")

    assert response.status_code == 200
    assert response.json() == schema_test_data.test_schema_response

    SchemaFirebaseRepository.get_schema_bucket_filename_with_guid = tmp_storage_1
    SchemaBucketRepository.get_schema_file_as_json = tmp_storage_2


def test_get_schema_from_bucket_404_response(test_client):
    """
    When the schema is unsuccessfully from the bucket there should be a 404 status code and expected response.
    """
    tmp_storage_1 = SchemaFirebaseRepository.get_schema_bucket_filename
    SchemaFirebaseRepository.get_schema_bucket_filename = MagicMock()
    SchemaFirebaseRepository.get_schema_bucket_filename.return_value = None

    tmp_storage_2 = SchemaBucketRepository.get_schema_file_as_json
    SchemaBucketRepository.get_schema_file_as_json = MagicMock()
    SchemaBucketRepository.get_schema_file_as_json.return_value = None

    response = test_client.get("/v1/schema?survey_id=test_survey_id&version=2")

    assert response.status_code == 404
    assert response.json()["message"] == "No schema found"

    SchemaFirebaseRepository.get_schema_bucket_filename = tmp_storage_1
    SchemaBucketRepository.get_schema_file_as_json = tmp_storage_2


def test_get_latest_schema_from_bucket_without_version_404_response(test_client):
    """
    When the schema is queried without version but no latest schema version is found,
    there should be a 404 status code and expected response
    """
    tmp_storage = SchemaFirebaseRepository.get_latest_schema_bucket_filename
    SchemaFirebaseRepository.get_latest_schema_bucket_filename = MagicMock()
    SchemaFirebaseRepository.get_latest_schema_bucket_filename.return_value = None

    response = test_client.get("/v1/schema?survey_id=abcdef")

    assert response.status_code == 404
    assert response.json()["message"] == "No schema found"

    SchemaFirebaseRepository.get_latest_schema_bucket_filename = tmp_storage


def test_get_schema_from_bucket_with_guid_404_response(test_client):
    """
    When the schema is unsuccessfully from the bucket there should be a 404 status code and expected response.
    """
    tmp_storage_1 = SchemaFirebaseRepository.get_schema_bucket_filename_with_guid
    SchemaFirebaseRepository.get_schema_bucket_filename_with_guid = MagicMock()
    SchemaFirebaseRepository.get_schema_bucket_filename_with_guid.return_value = None

    tmp_storage_2 = SchemaBucketRepository.get_schema_file_as_json
    SchemaBucketRepository.get_schema_file_as_json = MagicMock()
    SchemaBucketRepository.get_schema_file_as_json.return_value = None

    response = test_client.get("/v2/schema?guid=test_guid")

    assert response.status_code == 404
    assert response.json()["message"] == "No schema found"

    SchemaFirebaseRepository.get_schema_bucket_filename_with_guid = tmp_storage_1
    SchemaBucketRepository.get_schema_file_as_json = tmp_storage_2


def test_global_error(test_client_no_server_exception):
    """
    Checks that if app encounter a global exception error
    fastAPI will return a 500 exception with appropriate msg
    Func get_schema_metadata is patched and raised with exception
    Fixture client_no_server_exception is used to avoid exiting
    the test at exception so that the response can be validated
    """
    tmp_storage = SchemaFirebaseRepository.get_schema_bucket_filename
    SchemaFirebaseRepository.get_schema_bucket_filename = MagicMock(
        side_effect=Exception
    )

    response = test_client_no_server_exception.get(
        "/v1/schema?survey_id=076&version=123"
    )
    assert response.status_code == 500
    assert response.json()["message"] == "Unable to process request"

    SchemaFirebaseRepository.get_schema_bucket_filename = tmp_storage


def test_get_schema_with_invalid_version_error(test_client):
    """
    Checks that fastAPI does not accept non-numeric version
    and returns a 400 error with appropriate message at
    get_schema endpoint
    """
    response = test_client.get("/v1/schema?survey_id=076&version=xyz")

    assert response.status_code == 400
    assert response.json()["message"] == "Invalid search provided"


def test_get_schema_with_missing_survey_id_error(test_client):
    """
    Checks that fastAPI return 400 error with appropriate msg
    when survey id is missing when querying schema at get schema endpoint
    """
    response = test_client.get("/v1/schema")

    assert response.status_code == 400
    assert response.json()["message"] == "Invalid search provided"


def test_get_schema_with_missing_guid_error(test_client):
    """
    Checks that fastAPI return 400 error with appropriate msg
    when guid is missing when querying schema at get schema v2 endpoint
    """
    response = test_client.get("/v2/schema")

    assert response.status_code == 400
    assert response.json()["message"] == "Invalid parameter provided"


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
    Checks that fastAPI return 404 error with apppropriate msg
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


def test_get_survey_id_map_200_response(test_client):
    """
    When the list of Survey IDs is fetched successfully, the API must return the correct response with 200 status code
    """
    SchemaProcessorService.survey_id_map = MagicMock()
    SchemaProcessorService.get_survey_id_map.return_value = (
        schema_test_data.test_survey_id_map
    )
    response = test_client.get("/v1/survey_list")

    assert response.status_code == 200
    assert response.json() == schema_test_data.test_survey_id_map


def test_get_survey_id_map_404_response(test_client):
    """
    When the list of Survey IDs is empty, the API must return the error response with 404 status code
    """
    SchemaProcessorService.get_survey_id_map = MagicMock()
    SchemaProcessorService.get_survey_id_map.return_value = []
    response = test_client.get("/v1/survey_list")

    assert response.status_code == 404
    assert response.json()["message"] == "No Survey IDs found"


def test_get_survey_id_map_500_response(test_client_no_server_exception):
    """
    If the app encounters a global exception, the API must return the error response with 500 status code
    """
    SchemaProcessorService.get_survey_id_map = MagicMock(side_effect=Exception)

    response = test_client_no_server_exception.get("/v1/survey_list")

    assert response.status_code == 500
    assert response.json()["message"] == "Unable to process request"

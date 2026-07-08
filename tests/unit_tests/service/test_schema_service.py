from unittest.mock import MagicMock, Mock

import pytest
import requests
from fastapi import status

from app.config import settings
from app.exception import exceptions
from app.models.schema_models import SchemaMetadata
from app.services.schema_service import SchemaService
from tests.test_data import schema_test_data


def mock_response(status_code, json_data) -> MagicMock:
    response = Mock(spec=requests.Response)
    response.status_code = status_code
    response.json.return_value = json_data
    return response


def test_process_raw_schema_returns_first_version_metadata_and_stores_schema():
    """
    When a schema is processed for a survey with no previous versions,
    SchemaService must create version 1 metadata, store schema, and publish.
    """
    schema_repository = MagicMock()
    schema_repository.get_latest_schema_metadata.return_value = None
    publisher_service = MagicMock()

    service = SchemaService(
        schema_repository=schema_repository,
        publisher_service=publisher_service,
    )

    result = service.process_raw_schema(
        schema=schema_test_data.test_schema,
        survey_id=schema_test_data.test_survey_id,
    )

    expected = SchemaMetadata(
        guid=schema_test_data.test_guid,
        schema_location=f"{schema_test_data.test_survey_id}/{schema_test_data.test_guid}.json",
        sds_schema_version=1,
        survey_id=schema_test_data.test_survey_id,
        sds_published_at=schema_test_data.test_published_at,
        schema_version=schema_test_data.test_schema_version,
        title=schema_test_data.test_title,
    )

    assert result == expected
    schema_repository.store_schema.assert_called_once_with(
        schema_test_data.test_guid,
        expected,
        schema_test_data.test_schema_model,
    )
    publisher_service.publish_data_to_topic.assert_called_once_with(
        expected,
        settings.PUBLISH_SCHEMA_TOPIC_ID,
    )


def test_process_raw_schema_returns_incremented_schema_version():
    """
    When a schema already exists for a survey, SchemaService must assign
    the next SDS schema version.
    """
    schema_repository = MagicMock()
    schema_repository.get_latest_schema_metadata.return_value = schema_test_data.test_schema_metadata_1
    publisher_service = MagicMock()

    service = SchemaService(
        schema_repository=schema_repository,
        publisher_service=publisher_service,
    )

    result = service.process_raw_schema(
        schema=schema_test_data.test_schema,
        survey_id=schema_test_data.test_survey_id,
    )

    assert result.sds_schema_version == 2


def test_process_raw_schema_raises_global_exception_when_store_fails():
    """
    When schema storage fails, SchemaService must raise GlobalException and
    skip publishing.
    """
    schema_repository = MagicMock()
    schema_repository.get_latest_schema_metadata.return_value = None
    schema_repository.store_schema = MagicMock(side_effect=Exception)
    publisher_service = MagicMock()

    service = SchemaService(
        schema_repository=schema_repository,
        publisher_service=publisher_service,
    )

    with pytest.raises(exceptions.GlobalException):
        service.process_raw_schema(
            schema=schema_test_data.test_schema,
            survey_id=schema_test_data.test_survey_id,
        )

    publisher_service.publish_data_to_topic.assert_not_called()


def test_process_raw_schema_raises_global_exception_when_publish_fails():
    """
    When publishing schema metadata fails, SchemaService must raise
    GlobalException after schema storage succeeds.
    """
    schema_repository = MagicMock()
    schema_repository.get_latest_schema_metadata.return_value = None
    publisher_service = MagicMock()
    publisher_service.publish_data_to_topic = MagicMock(side_effect=Exception)

    service = SchemaService(
        schema_repository=schema_repository,
        publisher_service=publisher_service,
    )

    with pytest.raises(exceptions.GlobalException):
        service.process_raw_schema(
            schema=schema_test_data.test_schema,
            survey_id=schema_test_data.test_survey_id,
        )

    schema_repository.store_schema.assert_called_once()


def test_get_schema_metadata_collection_with_guid_calls_repository():
    """
    When metadata is requested for a survey, SchemaService must delegate to
    schema repository and return the repository result.
    """
    schema_repository = MagicMock()
    schema_repository.get_metadata.return_value = schema_test_data.test_schema_metadata
    publisher_service = MagicMock()

    service = SchemaService(
        schema_repository=schema_repository,
        publisher_service=publisher_service,
    )

    result = service.get_schema_metadata_collection_with_guid(schema_test_data.test_survey_id)

    assert result == schema_test_data.test_schema_metadata
    schema_repository.get_metadata.assert_called_once_with(schema_test_data.test_survey_id)


def test_get_all_schema_metadata_collection_calls_repository():
    """
    When all schema metadata is requested, SchemaService must delegate to
    schema repository and return the repository result.
    """
    schema_repository = MagicMock()
    schema_repository.get_all_metadata.return_value = schema_test_data.test_all_schema_metadata
    publisher_service = MagicMock()

    service = SchemaService(
        schema_repository=schema_repository,
        publisher_service=publisher_service,
    )

    result = service.get_all_schema_metadata_collection()

    assert result == schema_test_data.test_all_schema_metadata
    schema_repository.get_all_metadata.assert_called_once_with()


def test_get_guid_with_survey_id_and_version_without_version_calls_latest_guid():
    """
    When version is not provided, SchemaService must request latest guid.
    """
    schema_repository = MagicMock()
    schema_repository.get_latest_guid.return_value = schema_test_data.test_guid
    publisher_service = MagicMock()

    service = SchemaService(
        schema_repository=schema_repository,
        publisher_service=publisher_service,
    )

    result = service.get_guid_with_survey_id_and_version(schema_test_data.test_survey_id, None)

    assert result == schema_test_data.test_guid
    schema_repository.get_latest_guid.assert_called_once_with(schema_test_data.test_survey_id)
    schema_repository.get_guid.assert_not_called()


def test_get_guid_with_survey_id_and_version_with_version_calls_guid_lookup():
    """
    When version is provided, SchemaService must request guid for that version.
    """
    schema_repository = MagicMock()
    schema_repository.get_guid.return_value = schema_test_data.test_guid
    publisher_service = MagicMock()

    service = SchemaService(
        schema_repository=schema_repository,
        publisher_service=publisher_service,
    )

    result = service.get_guid_with_survey_id_and_version(schema_test_data.test_survey_id, 2)

    assert result == schema_test_data.test_guid
    schema_repository.get_guid.assert_called_once_with(schema_test_data.test_survey_id, 2)
    schema_repository.get_latest_guid.assert_not_called()


def test_get_schema_from_guid_calls_repository():
    """
    When schema content is requested by guid, SchemaService must delegate to
    schema repository and return the repository result.
    """
    schema_repository = MagicMock()
    schema_repository.get_schema_from_guid.return_value = schema_test_data.test_schema
    publisher_service = MagicMock()

    service = SchemaService(
        schema_repository=schema_repository,
        publisher_service=publisher_service,
    )

    result = service.get_schema_from_guid(schema_test_data.test_guid)

    assert result == schema_test_data.test_schema
    schema_repository.get_schema_from_guid.assert_called_once_with(schema_test_data.test_guid)


def test_get_survey_id_map_returns_mapping_when_response_is_200():
    """
    When survey map request succeeds, SchemaService must return the JSON payload.
    """
    schema_repository = MagicMock()
    publisher_service = MagicMock()

    service = SchemaService(
        schema_repository=schema_repository,
        publisher_service=publisher_service,
    )

    expected = schema_test_data.test_survey_id_map
    service_response = mock_response(status.HTTP_200_OK, expected)

    from app.services.shared.utility_functions import UtilityFunctions
    UtilityFunctions.request_survey_id_mapping = MagicMock(return_value=service_response)

    result = service.get_survey_id_map()

    assert result == expected


def test_get_survey_id_map_raises_no_survey_ids_exception_for_non_200_response():
    """
    When survey map request fails, SchemaService must raise ExceptionNoSurveyIDs.
    """
    schema_repository = MagicMock()
    publisher_service = MagicMock()

    service = SchemaService(
        schema_repository=schema_repository,
        publisher_service=publisher_service,
    )

    service_response = mock_response(status.HTTP_404_NOT_FOUND, None)

    from app.services.shared.utility_functions import UtilityFunctions
    UtilityFunctions.request_survey_id_mapping = MagicMock(return_value=service_response)

    with pytest.raises(exceptions.ExceptionNoSurveyIDs):
        service.get_survey_id_map()


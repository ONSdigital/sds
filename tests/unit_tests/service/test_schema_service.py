from unittest.mock import MagicMock

import pytest
from fastapi import status

from app.config import settings
from app.exception import exceptions
from app.models.schema_models import SchemaMetadata
from tests.test_data import schema_test_data


def test_process_raw_schema_returns_first_version_metadata_and_stores_schema(schema_service_with_dependencies):
    """
    When a schema is processed for a survey with no previous versions,
    SchemaService must create version 1 metadata, store schema, and publish.
    """
    service, schema_repository, publisher_service = schema_service_with_dependencies
    schema_repository.get_latest_schema_metadata.return_value = None

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


def test_process_raw_schema_returns_incremented_schema_version(schema_service_with_dependencies):
    """
    When a schema already exists for a survey, SchemaService must assign
    the next SDS schema version.
    """
    service, schema_repository, _ = schema_service_with_dependencies
    schema_repository.get_latest_schema_metadata.return_value = schema_test_data.test_schema_metadata_1

    result = service.process_raw_schema(
        schema=schema_test_data.test_schema,
        survey_id=schema_test_data.test_survey_id,
    )

    assert result.sds_schema_version == 2


def test_process_raw_schema_raises_global_exception_when_store_fails(schema_service_with_dependencies):
    """
    When schema storage fails, SchemaService must raise GlobalException and
    skip publishing.
    """
    service, schema_repository, publisher_service = schema_service_with_dependencies
    schema_repository.get_latest_schema_metadata.return_value = None
    schema_repository.store_schema = MagicMock(side_effect=Exception)

    with pytest.raises(exceptions.GlobalException):
        service.process_raw_schema(
            schema=schema_test_data.test_schema,
            survey_id=schema_test_data.test_survey_id,
        )

    publisher_service.publish_data_to_topic.assert_not_called()


def test_process_raw_schema_raises_global_exception_when_publish_fails(schema_service_with_dependencies):
    """
    When publishing schema metadata fails, SchemaService must raise
    GlobalException after schema storage succeeds.
    """
    service, schema_repository, publisher_service = schema_service_with_dependencies
    schema_repository.get_latest_schema_metadata.return_value = None
    publisher_service.publish_data_to_topic = MagicMock(side_effect=Exception)

    with pytest.raises(exceptions.GlobalException):
        service.process_raw_schema(
            schema=schema_test_data.test_schema,
            survey_id=schema_test_data.test_survey_id,
        )

    schema_repository.store_schema.assert_called_once()


def test_get_schema_metadata_collection_with_guid_calls_repository(schema_service_with_dependencies):
    """
    When metadata is requested for a survey, SchemaService must delegate to
    schema repository and return the repository result.
    """
    service, schema_repository, _ = schema_service_with_dependencies
    schema_repository.get_metadata.return_value = schema_test_data.test_schema_metadata

    result = service.get_schema_metadata_collection_with_guid(schema_test_data.test_survey_id)

    assert result == schema_test_data.test_schema_metadata
    schema_repository.get_metadata.assert_called_once_with(schema_test_data.test_survey_id)


def test_get_all_schema_metadata_collection_calls_repository(schema_service_with_dependencies):
    """
    When all schema metadata is requested, SchemaService must delegate to
    schema repository and return the repository result.
    """
    service, schema_repository, _ = schema_service_with_dependencies
    schema_repository.get_all_metadata.return_value = schema_test_data.test_all_schema_metadata

    result = service.get_all_schema_metadata_collection()

    assert result == schema_test_data.test_all_schema_metadata
    schema_repository.get_all_metadata.assert_called_once_with()


def test_get_guid_with_survey_id_and_version_without_version_calls_latest_guid(schema_service_with_dependencies):
    """
    When version is not provided, SchemaService must request latest guid.
    """
    service, schema_repository, _ = schema_service_with_dependencies
    schema_repository.get_latest_guid.return_value = schema_test_data.test_guid

    result = service.get_guid_with_survey_id_and_version(schema_test_data.test_survey_id, None)

    assert result == schema_test_data.test_guid
    schema_repository.get_latest_guid.assert_called_once_with(schema_test_data.test_survey_id)
    schema_repository.get_guid.assert_not_called()


def test_get_guid_with_survey_id_and_version_with_version_calls_guid_lookup(schema_service_with_dependencies):
    """
    When version is provided, SchemaService must request guid for that version.
    """
    service, schema_repository, _ = schema_service_with_dependencies
    schema_repository.get_guid.return_value = schema_test_data.test_guid

    result = service.get_guid_with_survey_id_and_version(schema_test_data.test_survey_id, 2)

    assert result == schema_test_data.test_guid
    schema_repository.get_guid.assert_called_once_with(schema_test_data.test_survey_id, 2)
    schema_repository.get_latest_guid.assert_not_called()


def test_get_schema_from_guid_calls_repository(schema_service_with_dependencies):
    """
    When schema content is requested by guid, SchemaService must delegate to
    schema repository and return the repository result.
    """
    service, schema_repository, _ = schema_service_with_dependencies
    schema_repository.get_schema_from_guid.return_value = schema_test_data.test_schema

    result = service.get_schema_from_guid(schema_test_data.test_guid)

    assert result == schema_test_data.test_schema
    schema_repository.get_schema_from_guid.assert_called_once_with(schema_test_data.test_guid)


def test_get_survey_id_map_returns_mapping_when_response_is_200(
    schema_service_with_dependencies,
    mock_http_response,
):
    """
    When survey map request succeeds, SchemaService must return the JSON payload.
    """
    service, _, _ = schema_service_with_dependencies

    expected = schema_test_data.test_survey_id_map
    service_response = mock_http_response(status.HTTP_200_OK, expected)

    from app.services.shared.utility_functions import UtilityFunctions
    UtilityFunctions.request_survey_id_mapping = MagicMock(return_value=service_response)

    result = service.get_survey_id_map()

    assert result == expected


def test_get_survey_id_map_raises_no_survey_ids_exception_for_non_200_response(
    schema_service_with_dependencies,
    mock_http_response,
):
    """
    When survey map request fails, SchemaService must raise ExceptionNoSurveyIDs.
    """
    service, _, _ = schema_service_with_dependencies

    service_response = mock_http_response(status.HTTP_404_NOT_FOUND, None)

    from app.services.shared.utility_functions import UtilityFunctions
    UtilityFunctions.request_survey_id_mapping = MagicMock(return_value=service_response)

    with pytest.raises(exceptions.ExceptionNoSurveyIDs):
        service.get_survey_id_map()


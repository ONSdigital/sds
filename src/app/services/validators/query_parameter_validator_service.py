import exception.exceptions as exceptions
from logging_config import logging

logger = logging.getLogger(__name__)


class QueryParameterValidatorService:
    @staticmethod
    def validate_survey_id_from_post_schema(survey_id: str) -> None:
        """
        Validates the present of survey id when posting schema

        Parameters:
        survey_id (str): survey id of the schema
        """
        if survey_id in (None, ""):
            logger.error("Survey ID not set when posting schema")
            raise exceptions.ValidationException

    @staticmethod
    def validate_schema_version_from_get_schema(version: str) -> None:
        """
        Validates the version from get schema v1 endpoint

        Parameters:
        version: version of the schema metadata
        """
        if version is not None:
            try:
                version = int(version)
            except ValueError:
                logger.error("Invalid version")
                raise exceptions.ExceptionIncorrectSchemaKey

    @staticmethod
    def validate_survey_id_from_get_schema(survey_id: str) -> None:
        """
        Validates the survey id from get schema v1 endpoint

        Parameters:
        survey_id: survey id of the schema
        """
        if survey_id is None:
            logger.error("Survey ID not set")
            raise exceptions.ExceptionIncorrectSchemaKey

    @staticmethod
    def validate_guid_from_get_schema(guid: str) -> None:
        """
        Validates the guid from get schema v2 endpoint

        Parameters:
        guid: guid of the schema
        """
        if guid is None:
            logger.error("GUID not set")
            raise exceptions.ExceptionIncorrectSchemaV2Key

    @staticmethod
    def validate_survey_id_from_schema_metadata(survey_id: str) -> None:
        """
        Validates the schema metadata survey id

        Parameters:
        survey_id: survey id of the schema metadata
        """
        if survey_id is None:
            logger.error("Survey ID not set")
            raise exceptions.ExceptionIncorrectSchemaKey

    @staticmethod
    def validate_survey_and_period_id_from_dataset_metadata(
        survey_id: str, period_id: str
    ) -> None:
        """
        Validates the dataset survey id and period id.

        Parameters:
        survey_id: survey id of the dataset metadata.
        period_id: period id of the dataset metadata.
        """

        if survey_id is None:
            logger.error("Survey ID not set")
            raise exceptions.ExceptionIncorrectDatasetKey

        if period_id is None:
            logger.error("Period ID not set")
            raise exceptions.ExceptionIncorrectDatasetKey

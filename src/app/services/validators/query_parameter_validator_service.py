import exception.exceptions as exceptions
from fastapi.exceptions import RequestValidationError
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
    def validate_schema_version_parses(version: str) -> None:
        """
        Validates the schema version parses to an integer

        Parameters:
        version: version of the schema metadata
        """
        if version is not None:
            try:
                version = int(version)
            except ValueError:
                logger.error("Invalid version")
                raise RequestValidationError(errors=ValueError)

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

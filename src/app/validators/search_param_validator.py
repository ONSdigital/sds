import exception.exceptions as exceptions
from fastapi.exceptions import RequestValidationError
from logging_config import logging

logger = logging.getLogger(__name__)


class SearchParamValidator:
    def validate_version_from_schema(version):
        try:
            version = int(version)
        except ValueError:
            logger.error("Invalid version")
            raise RequestValidationError(errors=ValueError)

    def validate_survey_id_from_schema_metadata(survey_id):
        if survey_id is None:
            logger.error("Survey ID not set")
            raise exceptions.ExceptionIncorrectSchemaKey

    def validate_survey_period_id_from_dataset_metadata(survey_id, period_id):
        if survey_id is None:
            logger.error("Survey ID not set")
            raise exceptions.ExceptionIncorrectDatasetKey

        if period_id is None:
            logger.error("Period ID not set")
            raise exceptions.ExceptionIncorrectDatasetKey

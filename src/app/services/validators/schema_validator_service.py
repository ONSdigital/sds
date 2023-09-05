from exception.exceptions import ValidationException
from logging_config import logging

logger = logging.getLogger(__name__)


class SchemaValidatorService:
    """
    Schema received contains optional unspecified fields at root level
    Pydantic model is not ideal to handle as optional fields are default
    with null value and fields unspecified in model are loss when read
    Therefore, Dict is used instead to allow flexibility in structure while
    this validator class ensures the integrity of the fields that have
    impact on SDS operation
    """

    @staticmethod
    def validate_schema(schema: dict) -> None:
        """
        Validate the schema

        Parameters:
        schema (dict): schema being validated
        """
        SchemaValidatorService._validate_schema_keys(schema)

        SchemaValidatorService._validate_schema_objects(schema)

        SchemaValidatorService._validate_schema_version_exists(schema)

    @staticmethod
    def _validate_schema_keys(schema: dict) -> None:
        # Temporary validation logic for card (SDSS-185)
        """
        Validate the existence of root level keys in a schema

        Parameters:
        schema (dict): schema to be validated
        """
        mandatory_keys = ["properties"]

        for mandatory_key in mandatory_keys:
            if mandatory_key not in schema:
                logger.error(f"Mandatory key {mandatory_key} is not found in schema")
                raise ValidationException

            if schema[mandatory_key] in (None, ""):
                logger.error(f"Mandatory key {mandatory_key} has no value in schema")
                raise ValidationException

    @staticmethod
    def _validate_schema_objects(schema: dict) -> None:
        """
        Validate the root level fields are in type object

        Parameters:
        schema (dict): schema to be validated
        """
        object_keys = ["properties"]

        for object_key in object_keys:
            if type(schema[object_key]) != dict:
                logger.error(f"Key {object_key} is not an object")
                raise ValidationException

    @staticmethod
    def _validate_schema_version_exists(schema: dict) -> None:
        """
        Validate schema version exists within properties

        Parameters:
        schema (dict): schema to be validated
        """
        level_keys = ["properties", "schema_version", "const"]
        field = schema

        for index, level_key in enumerate(level_keys):
            if level_key not in field:
                logger.error(f"Required key {level_key} has is not found in schema")
                raise ValidationException

            if index != len(level_keys) - 1:
                if type(field[level_key]) != dict:
                    logger.error(f"Key {level_key} is not an object")
                    raise ValidationException

                field = field[level_key]
            else:
                if type(field[level_key]) != str:
                    logger.error(f"Key {level_key} is not a string field")
                    raise ValidationException

                if field[level_key] in (None, ""):
                    logger.error(f"Key {level_key} has not value in schema")
                    raise ValidationException

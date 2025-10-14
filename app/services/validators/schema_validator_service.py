from app.exception.exceptions import ValidationException
from app.logging_config import logging

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
        # keys_definition_list is a list of keys definition (object) comprises the:
        # 1. key_hierarchy in list, which specify the hierarchy that leads to the key
        # 2. key_type, which specify the Python type of the key
        # Eg. "key_hierarchy": ["properties", "schema_version", "const"], "key_type": str
        # Means the field (properties > schema_version > const) must be a String
        # Finally, the field value will be validated that it is not a null value
        keys_definition_list = [
            {"key_hierarchy": ["title"], "key_type": str},
            {
                "key_hierarchy": ["properties", "schema_version", "const"],
                "key_type": str,
            },
        ]

        SchemaValidatorService._validate_keys(schema, keys_definition_list)

    @staticmethod
    def _validate_keys(schema: dict, keys_definition_list: list) -> None:
        """
        Validate schema matches the key definition

        Parameters:
        schema (dict): schema to be validated
        keys_definition_list (list): a list of keys definition to validate schema
        """
        for key_definition in keys_definition_list:
            rolling_field = schema
            key_hierarchy = key_definition["key_hierarchy"]
            key_type = key_definition["key_type"]

            for index, key in enumerate(key_hierarchy):
                # Check the key exists
                if key not in rolling_field:
                    logger.error(f"Required key '{key}' is not found in schema")
                    raise ValidationException

                # If not the last hierarchy, check the key is an object
                if index != len(key_hierarchy) - 1:
                    if type(rolling_field[key]) is not dict:
                        logger.error(f"Key '{key}' must be an object")
                        raise ValidationException

                    rolling_field = rolling_field[key]
                else:
                    # If at the last hierarchy, check the key type matches definition
                    if type(rolling_field[key]) is not key_type:
                        logger.error(
                            f"Key '{key}' must be in type {key_type}, but it is now {type(rolling_field[key])}"
                        )
                        raise ValidationException

                    # Check the key field is not null
                    if rolling_field[key] in (None, ""):
                        logger.error(f"Key '{key}' has no value in schema")
                        raise ValidationException

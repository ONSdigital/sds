from exception.exceptions import ValidationException


class SchemaValidatorService:
    @staticmethod
    def validate_schema(schema: dict) -> None:
        """
        Validate the schema

        Parameters:
        schema (dict): schema being validated
        """
        SchemaValidatorService._validate_schema_keys(schema)

        SchemaValidatorService._validate_schema_objects(schema)

    @staticmethod
    def _validate_schema_keys(schema: dict) -> None:
        # Temporary validation logic for card (SDSS-185)
        """
        Validate the existence of root level keys in a schema

        Parameters:
        schema (dict): schema to be validated
        """
        mandatory_keys = ["survey_id", "schema_version", "properties"]

        for mandatory_key in mandatory_keys:
            if mandatory_key not in schema:
                raise ValidationException

            if schema[mandatory_key] in (None, ""):
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
                raise ValidationException

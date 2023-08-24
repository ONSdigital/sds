from pydantic import BaseModel


class ExceptionResponseModel(BaseModel):
    status: str
    message: str


erm_500_global_exception = ExceptionResponseModel(
    status="error", message="Unable to process request"
)
erm_400_validation_exception = ExceptionResponseModel(
    status="error", message="Validation has failed"
)
erm_400_incorrect_schema_key_exception = ExceptionResponseModel(
    status="error", message="Invalid search provided"
)
erm_400_incorrect_schema_v2_key_exception = ExceptionResponseModel(
    status="error", message="Invalid parameter provided"
)
erm_404_no_schemas_metadata_exception = ExceptionResponseModel(
    status="error", message="No results found"
)
erm_404_no_schema_exception = ExceptionResponseModel(
    status="error", message="No schema found"
)
erm_400_incorrect_key_names_exception = ExceptionResponseModel(
    status="error", message="Invalid search parameters provided"
)
erm_404_no_result_exception = ExceptionResponseModel(
    status="error", message="No datasets found"
)
erm_404_unit_data_no_response_exception = ExceptionResponseModel(
    status="error", message="No unit data found"
)

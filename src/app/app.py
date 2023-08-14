import exception.exceptions as exceptions
from exception.exception_interceptor import ExceptionInterceptor
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from logging_config import logging
from routers import dataset_router, schema_router

logger = logging.getLogger(__name__)
app = FastAPI()

app.add_exception_handler(
    exceptions.ExceptionIncorrectSchemaKey,
    ExceptionInterceptor.throw_400_incorrect_schema_key_exception,
)
app.add_exception_handler(
    exceptions.ExceptionIncorrectSchemaV2Key,
    ExceptionInterceptor.throw_400_incorrect_schema_v2_key_exception,
)
app.add_exception_handler(
    exceptions.ExceptionNoSchemaMetadataCollection,
    ExceptionInterceptor.throw_404_no_schemas_metadata_exception,
)
app.add_exception_handler(
    exceptions.ExceptionNoSchemaFound,
    ExceptionInterceptor.throw_404_no_schema_exception,
)
app.add_exception_handler(
    exceptions.ExceptionIncorrectDatasetKey,
    ExceptionInterceptor.throw_400_incorrect_key_names_exception,
)
app.add_exception_handler(
    exceptions.ExceptionNoDatasetMetadata,
    ExceptionInterceptor.throw_404_no_result_exception,
)
app.add_exception_handler(
    exceptions.ExceptionNoUnitData,
    ExceptionInterceptor.throw_404_unit_data_no_response_exception,
)
app.add_exception_handler(
    exceptions.GlobalException,
    ExceptionInterceptor.throw_500_global_exception,
)
app.add_exception_handler(
    exceptions.ValidationException,
    ExceptionInterceptor.throw_400_validation_exception,
)


@app.exception_handler(500)
async def internal_exception_handler(request: Request, exc: Exception):
    """
    Override the global exception handler (500 internal server error) in
    FastAPI and throw error in JSON format
    """
    return ExceptionInterceptor.throw_500_global_exception(request, exc)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    When a request contains invalid data, FastAPI internally raises a
    RequestValidationError. This function override the default
    validation exception handler to return 400 instead of 422
    """
    return ExceptionInterceptor.throw_400_validation_exception(request, exc)


app.include_router(dataset_router.router)
app.include_router(schema_router.router)

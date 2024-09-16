import exception.exception_response_models as erm
from exception import exceptions
from exception.exception_response_models import ExceptionResponseModel
from fastapi import APIRouter, Body, Depends
from logging_config import logging
from models.schema_models import SchemaMetadata
from repositories.buckets.schema_bucket_repository import SchemaBucketRepository
from services.schema.schema_processor_service import SchemaProcessorService
from services.validators.query_parameter_validator_service import (
    QueryParameterValidatorService,
)
from services.validators.schema_validator_service import SchemaValidatorService

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post(
    "/v1/schema",
    response_model=SchemaMetadata,
    responses={
        400: {
            "model": ExceptionResponseModel,
            "content": {
                "application/json": {"example": erm.erm_400_validation_exception}
            },
        },
        500: {
            "model": ExceptionResponseModel,
            "content": {"application/json": {"example": erm.erm_500_global_exception}},
        },
    },
)
async def post_schema(
    survey_id: str,
    schema: dict = Body(...),
    schema_processor_service: SchemaProcessorService = Depends(),
) -> SchemaMetadata:
    """
    Posts the schema metadata to be processed.

    Parameters:
    survey_id (str): survey_id of the schema
    schema (dict): schema to be processed in JSON format.
    schema_processor_service (SchemaProcessorService): injected processor service for processing the schema.
    """
    logger.info("Posting schema metadata...")
    logger.debug(f"Input body: {{{schema}}}")

    QueryParameterValidatorService.validate_survey_id_from_post_schema(survey_id)
    SchemaValidatorService.validate_schema(schema)

    posted_schema_metadata = schema_processor_service.process_raw_schema(
        schema, survey_id
    )

    logger.info("Schema successfully posted.")
    logger.debug(f"Schema metadata: {posted_schema_metadata}")

    return posted_schema_metadata


@router.get(
    "/v1/schema",
    responses={
        400: {
            "model": ExceptionResponseModel,
            "content": {
                "application/json": {"example": erm.erm_400_invalid_search_exception}
            },
        },
        500: {
            "model": ExceptionResponseModel,
            "content": {"application/json": {"example": erm.erm_500_global_exception}},
        },
        404: {
            "model": ExceptionResponseModel,
            "content": {
                "application/json": {"example": erm.erm_404_no_schema_exception}
            },
        },
    },
)
async def get_schema_from_bucket(
    survey_id: str | None = None,
    version: str | None = None,
    schema_bucket_repository: SchemaBucketRepository = Depends(),
    schema_processor_service: SchemaProcessorService = Depends(),
) -> dict:
    """
    Gets the filename of the bucket schema metadata and uses that to retrieve the schema metadata
    with specific survey id and version from the bucket. Latest version schema will be retrieved
    if version is omitted

    Parameters:
    survey_id (str): survey id of the schema metadata.
    version (str) (optional): version of the survey.
    schema_firebase_repository (SchemaFirebaseRepository): injected dependency for
        interacting with the schema collection in firestore.
    schema_processor_service (SchemaProcessorService): injected dependency for
        interacting with the schema collection in firestore.
    """
    logger.info("Getting bucket schema metadata...")
    logger.debug(f"Input data: survey_id={survey_id}, version={version}")

    QueryParameterValidatorService.validate_survey_id_from_get_schema(survey_id)
    QueryParameterValidatorService.validate_schema_version_from_get_schema(version)

    bucket_schema_filename = schema_processor_service.get_schema_bucket_filename(
        survey_id, version
    )

    if not bucket_schema_filename:
        logger.error("Schema metadata not found")
        raise exceptions.ExceptionNoSchemaFound

    logger.debug(f"Bucket schema location: {bucket_schema_filename}")
    logger.info("Bucket schema location successfully retrieved. Getting schema...")

    schema = schema_bucket_repository.get_schema_file_as_json(bucket_schema_filename)

    logger.info("Schema successfully retrieved.")
    logger.debug(f"Schema: {schema}")

    return schema


@router.get(
    "/v2/schema",
    responses={
        400: {
            "model": ExceptionResponseModel,
            "content": {
                "application/json": {"example": erm.erm_400_invalid_parameter_exception}
            },
        },
        500: {
            "model": ExceptionResponseModel,
            "content": {"application/json": {"example": erm.erm_500_global_exception}},
        },
        404: {
            "model": ExceptionResponseModel,
            "content": {
                "application/json": {"example": erm.erm_404_no_schema_exception}
            },
        },
    },
)
async def get_schema_from_bucket_with_guid(
    guid: str | None = None,
    schema_bucket_repository: SchemaBucketRepository = Depends(),
    schema_processor_service: SchemaProcessorService = Depends(),
) -> dict:
    """
    Gets the filename of the bucket schema metadata and uses that to retrieve the schema metadata
    with specific guid from the bucket

    Parameters:
    guid (str): GUID of the schema.
    schema_firebase_repository (SchemaFirebaseRepository): injected dependency for
        interacting with the schema collection in firestore.
    schema_processor_service (SchemaProcessorService): injected dependency for
        interacting with the schema collection in firestore.
    """
    logger.info("Getting bucket schema metadata...")
    logger.debug(f"Input data: guid={guid}")

    QueryParameterValidatorService.validate_guid_from_get_schema(guid)

    bucket_schema_filename = (
        schema_processor_service.get_schema_bucket_filename_from_guid(guid)
    )

    if not bucket_schema_filename:
        logger.error("Schema metadata not found")
        raise exceptions.ExceptionNoSchemaFound

    logger.debug(f"Bucket schema location: {bucket_schema_filename}")
    logger.info("Bucket schema location successfully retrieved. Getting schema...")

    schema = schema_bucket_repository.get_schema_file_as_json(bucket_schema_filename)

    logger.info("Schema successfully retrieved.")
    logger.debug(f"Schema: {schema}")

    return schema


@router.get(
    "/v1/schema_metadata",
    response_model=list[SchemaMetadata],
    responses={
        400: {
            "model": ExceptionResponseModel,
            "content": {
                "application/json": {"example": erm.erm_400_invalid_search_exception}
            },
        },
        500: {
            "model": ExceptionResponseModel,
            "content": {"application/json": {"example": erm.erm_500_global_exception}},
        },
        404: {
            "model": ExceptionResponseModel,
            "content": {
                "application/json": {"example": erm.erm_404_no_results_exception}
            },
        },
    },
)
async def get_schema_metadata_collection(
    survey_id: str | None = None, schema_processor_service: SchemaProcessorService = Depends()
) -> list[SchemaMetadata]:
    """
    Get all schema metadata associated with a specific survey id.

    Parameters:
    survey_id (str): survey id of the collection
    schema_processor_service (SchemaProcessorService): injected dependency for processing the metadata collection.
    """
    QueryParameterValidatorService.validate_survey_id_from_schema_metadata(survey_id)

    logger.info("Getting schemas metadata...")
    logger.debug(f"Input data: survey_id={survey_id}")

    schema_metadata_collection = (
        schema_processor_service.get_schema_metadata_collection_with_guid(survey_id)
    )
    if not schema_metadata_collection:
        logger.error("Schemas metadata not found")
        raise exceptions.ExceptionNoSchemaMetadataCollection

    logger.info("Schemas metadata successfully retrieved.")
    logger.debug(f"Schemas metadata: {schema_metadata_collection}")

    return schema_metadata_collection


@router.get(
    "/v1/survey_list",
    response_model=list[dict],
    responses={
        500: {
            "model": ExceptionResponseModel,
            "content": {"application/json": {"example": erm.erm_500_global_exception}},
        },
        404: {
            "model": ExceptionResponseModel,
            "content": {
                "application/json": {"example": erm.erm_404_no_survey_id_exception}
            },
        },
    },
)
async def get_survey_id_map(
    schema_processor_service: SchemaProcessorService = Depends(),
) -> list[dict]:
    """
    Gets the Survey mapping data from the survey_map.json file in GitHub repository.
    Parameters:
    schema_processor_service (SchemaProcessorService): injected dependency for processing the survey_map.json file.
    """
    survey_id_map = schema_processor_service.get_survey_id_map()

    if not survey_id_map:
        logger.error("No Survey IDs found")
        raise exceptions.ExceptionNoSurveyIDs
    return survey_id_map

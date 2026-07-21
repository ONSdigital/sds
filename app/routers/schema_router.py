from fastapi import APIRouter, Body, Depends

import app.exception.exception_response_models as erm
from app.dependencies import get_schema_service
from app.exception import exceptions
from app.exception.exception_response_models import ExceptionResponseModel
from app.logging_config import logging
from app.models.schema_models import SchemaMetadata
from app.services.schema_service import SchemaService
from app.services.validators.query_parameter_validator_service import (
    QueryParameterValidatorService,
)
from app.services.validators.schema_validator_service import SchemaValidatorService

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post(
    "/v1/schema",
    name="Post Schema",
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
    deprecated=True,
)
async def post_schema(
    survey_id: str,
    schema: dict = Body(...),
    schema_service: SchemaService = Depends(get_schema_service),
) -> SchemaMetadata:
    """
    Posts the schema metadata to be processed.

    :param survey_id: survey id of the schema metadata.
    :param schema: schema to be processed.
    :param schema_service: injected dependency for processing the schema.

    """
    logger.info("Posting schema metadata...")
    logger.debug(f"Input body: {{{schema}}}")

    QueryParameterValidatorService.validate_survey_id_from_post_schema(survey_id)
    SchemaValidatorService.validate_schema(schema)

    posted_schema_metadata = schema_service.process_raw_schema(
        schema, survey_id
    )

    logger.info("Schema successfully posted.")
    logger.debug(f"Schema metadata: {posted_schema_metadata}")

    return posted_schema_metadata


@router.get(
    "/v1/schema",
    name="Get Schema",
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
    deprecated=True,
)
async def get_schema(
    survey_id: str | None = None,
    version: str | None = None,
    schema_service: SchemaService = Depends(get_schema_service),
) -> dict:
    """
    Gets the guid with specific survey id and version and uses that to retrieve a schema.
    Latest version schema will be retrieved if version is omitted

    Parameters:
    survey_id (str): survey id of the schema metadata.
    version (str) (optional): version of the survey.
    schema_processor_service (SchemaProcessorService): injected dependency for
        interacting with the schema collection in firestore.
    """
    logger.info("Getting schema from Survey ID and Version...")
    logger.debug(f"Input data: survey_id={survey_id}, version={version}")

    QueryParameterValidatorService.validate_survey_id_from_get_schema(survey_id)
    QueryParameterValidatorService.validate_schema_version_from_get_schema(version)

    # Attempt to get the GUID of the schema from the input parameters
    guid = schema_service.get_guid_with_survey_id_and_version(
        survey_id, int(version) if version is not None else None
    )

    # If the GUID is not found based on these parameters
    if not guid:
        logger.error("Schema metadata not found from survey id and version")
        raise exceptions.ExceptionNoSchemaFound

    logger.info("GUID successfully retrieved. Getting schema from GUID...")
    logger.debug(f"GUID of the schema to retrieve: {guid}")

    # Fetch the schema based on the found GUID
    schema = schema_service.get_schema_from_guid(guid)

    # If the schema cannot be found given the retrieved GUID
    if not schema:
        logger.error("Schema not found")
        raise exceptions.ExceptionNoSchemaFound

    logger.info("Schema successfully retrieved.")
    logger.debug(f"Schema: {schema}")

    return schema


@router.get(
    "/v2/schema",
    name="Get Schema with GUID",
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
    deprecated=True,
)
async def get_schema_with_guid(
    guid: str | None = None,
    schema_service: SchemaService = Depends(get_schema_service),
) -> dict:
    """
    Use the guid to retrieve a schema directly

    :param guid: guid of the schema to retrieve
    :param schema_service: injected dependency for fetching schema
    """
    logger.info("Getting schema from GUID...")
    logger.debug(f"Input data: guid={guid}")

    QueryParameterValidatorService.validate_guid_from_get_schema(guid)

    # Attempt to fetch the schema using the GUID
    schema = schema_service.get_schema_from_guid(guid)

    # If the schema is not found, raise an exception
    if not schema:
        logger.error("Schema not found")
        raise exceptions.ExceptionNoSchemaFound

    logger.info("Schema successfully retrieved.")
    logger.debug(f"Schema: {schema}")

    return schema


@router.get(
    "/v1/schema_metadata",
    name="Get Schema Metadata",
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
    deprecated=True,
)
async def get_schema_metadata_collection(
    survey_id: str | None = None,
    schema_service: SchemaService = Depends(get_schema_service),
) -> list[SchemaMetadata]:
    """
    Get all schema metadata associated with a specific survey id.

    Parameters:
    survey_id (str): survey id of the collection
    schema_service (SchemaService): injected dependency for processing the metadata collection.
    """
    QueryParameterValidatorService.validate_survey_id_from_schema_metadata(survey_id)

    logger.info("Getting schemas metadata...")
    logger.debug(f"Input data: survey_id={survey_id}")

    schema_metadata_collection = (
        schema_service.get_schema_metadata_collection_with_guid(survey_id)
    )
    if not schema_metadata_collection:
        logger.error("Schemas metadata not found")
        raise exceptions.ExceptionNoSchemaMetadataCollection

    logger.info("Schemas metadata successfully retrieved.")
    logger.debug(f"Schemas metadata: {schema_metadata_collection}")

    return schema_metadata_collection


@router.get(
    "/v1/survey_list",
    name="Get Survey Mapping",
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
    deprecated=True,
)
async def get_survey_id_map(
    schema_service: SchemaService = Depends(get_schema_service),
) -> list[str]:
    """
    Gets the Survey mapping data from the survey_map.json file in GitHub repository.
    Parameters:
    schema_service (SchemaService): injected dependency for processing the survey_map.json file.
    """
    survey_id_map = schema_service.get_survey_id_map()

    if not survey_id_map:
        logger.error("No Survey IDs found")
        raise exceptions.ExceptionNoSurveyIDs
    return survey_id_map


@router.get(
    "/v1/all_schema_metadata",
    name="Get All Schema Metadata",
    response_model=list[SchemaMetadata],
    responses={
        500: {
            "model": ExceptionResponseModel,
            "content": {"application/json": {"example": erm.erm_500_global_exception}},
        },
    },
)
async def get_all_schema_metadata_collection(
    schema_service: SchemaService = Depends(get_schema_service),
) -> list[SchemaMetadata]:
    """Retrieve all schema metadata from the schema collection.
    """
    logger.info("Getting all schema metadata collection...")

    schema_metadata_collection = schema_service.get_all_schema_metadata_collection()

    if not schema_metadata_collection:
        logger.error("Schema metadata collection not found.")
        raise exceptions.ExceptionNoSchemaMetadataCollection

    logger.info("Schema metadata collection successfully retrieved.")
    logger.debug(f"Schema metadata collection: {schema_metadata_collection}")

    return schema_metadata_collection

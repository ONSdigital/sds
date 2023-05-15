import exception.exceptions as exceptions
from fastapi import APIRouter, Body, Depends
from logging_config import logging
from models.schema_models import Schema, SchemaMetadata
from repositories.buckets.schema_bucket_repository import SchemaBucketRepository
from repositories.firebase.schema_firebase_repository import SchemaFirebaseRepository
from services.schema.schema_processor_service import SchemaProcessorService
from services.validators.query_parameter_validator_service import (
    QueryParameterValidatorService,
)

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/v1/schema", response_model=SchemaMetadata)
async def post_schema(
    schema: Schema = Body(...),
    schema_processor_service: SchemaProcessorService = Depends(),
) -> SchemaMetadata:
    """
    Posts the schema metadata to be processed.

    Parameters:
    schema (Schema): schema to be processed.
    schema_processor_service (SchemaProcessorService): injected processor service for processing the schema.
    """
    logger.info("Posting schema metadata...")
    logger.debug(f"Input body: {{{schema}}}")

    posted_schema_metadata = schema_processor_service.process_raw_schema(schema)

    logger.info("Schema successfully posted.")
    logger.debug(f"Schema metadata: {posted_schema_metadata}")

    return posted_schema_metadata


@router.get("/v1/schema")
async def get_schema_from_bucket(
    survey_id: str,
    version: str = None,
    schema_firebase_repository: SchemaFirebaseRepository = Depends(),
    schema_bucket_repository: SchemaBucketRepository = Depends(),
    schema_processor_service: SchemaProcessorService = Depends(),
) -> Schema:
    """
    Gets the filename of the bucket schema metadata and uses that to retrieve the schema metadata
    with specific survey id and version from the bucket.

    Parameters:
    survey_id (str): survey id of the schema metadata.
    version (str): version of the survey.
    schema_firebase_repository (SchemaFirebaseRepository): injected dependency for
        interacting with the schema collection in firestore.
    """
    logger.info("Getting bucket schema metadata...")
    logger.debug(f"Input data: survey_id={survey_id}, version={version}")

    QueryParameterValidatorService.validate_schema_version_parses(version)

    if version is None:
        latest_version = (
            schema_processor_service.get_latest_schema_version_with_survey_id(survey_id)
        )
        if latest_version is None:
            logger.error("Schema metadata not found")
            raise exceptions.ExceptionNoSchemaFound
        version = latest_version

    bucket_schema_filename = (
        schema_firebase_repository.get_schema_metadata_bucket_filename(
            survey_id, version
        )
    )

    if not bucket_schema_filename:
        logger.error("Schema metadata not found")
        raise exceptions.ExceptionNoSchemaFound

    logger.info("Bucket schema metadata location successfully retrieved.")
    logger.debug(f"Bucket schema metadata location: {bucket_schema_filename}")
    logger.info("Getting schema metadata...")

    schema = schema_bucket_repository.get_schema_file_as_json(bucket_schema_filename)

    logger.info("Schema successfully retrieved.")
    logger.debug(f"Schema: {schema}")

    return schema


@router.get("/v1/schema_metadata", response_model=list[SchemaMetadata])
async def get_schema_metadata_collection(
    survey_id: str = None, schema_processor_service: SchemaProcessorService = Depends()
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

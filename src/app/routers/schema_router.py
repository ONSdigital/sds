from fastapi import APIRouter, Body, Depends
from logging_config import logging
from models.schema_models import Schema, SchemaMetadata, SchemaMetadataWithGuid
from repositories.buckets.schema_bucket_repository import SchemaBucketRepository
from repositories.firebase.schema_firebase_repository import SchemaFirebaseRepository
from services.schema.schema_processor_service import SchemaProcessorService
from validators.search_param_validator import SearchParamValidator
import exception.exceptions as exceptions

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/v1/schema", response_model=SchemaMetadataWithGuid)
async def post_schema_metadata(
    schema_metadata: Schema = Body(...),
    schema_processor_service: SchemaProcessorService = Depends(),
) -> SchemaMetadataWithGuid:
    """
    Posts the schema metadata to be processed.

    Parameters:
    schema_metadata (Schema): schema metadata to be processed.
    schema_processor_service (SchemaProcessorService): injected processor service for processing the schema metadata.
    """
    logger.info("Posting schema metadata...")
    logger.debug(f"Input body: {{{schema_metadata}}}")

    posted_schema_metadata = schema_processor_service.process_schema_metadata(
        schema_metadata
    )

    logger.info("Schema metadata successfully posted.")
    logger.debug(f"Schema metadata: {posted_schema_metadata}")

    return posted_schema_metadata


@router.get("/v1/schema")
async def get_schema_metadata_from_bucket(
    survey_id: str,
    version: str,
    schema_firebase_repository: SchemaFirebaseRepository = Depends(),
    schema_bucket_repository: SchemaBucketRepository = Depends(),
) -> SchemaMetadata:
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

    SearchParamValidator.validate_version_from_schema(version)

    bucket_schema_metadata_filename = (
        schema_firebase_repository.get_schema_metadata_bucket_filename(
            survey_id, version
        )
    )

    if not bucket_schema_metadata_filename:
        logger.error("Schema metadata not found")
        raise exceptions.ExceptionNoSchemaMetadataFound

    logger.info("Bucket schema metadata location successfully retrieved.")
    logger.debug(f"Bucket schema metadata location: {bucket_schema_metadata_filename}")
    logger.info("Getting schema metadata...")

    schema_metadata = schema_bucket_repository.get_bucket_file_as_json(
        bucket_schema_metadata_filename
    )

    logger.info("Schema successfully retrieved.")
    logger.debug(f"Schema: {schema_metadata}")

    return schema_metadata


@router.get("/v1/schema_metadata", response_model=list[SchemaMetadataWithGuid])
async def get_schema_metadata_collection(
    survey_id: str, schema_processor_service: SchemaProcessorService = Depends()
) -> list[SchemaMetadataWithGuid]:
    """
    Get all schema metadata associated with a specific survey id.

    Parameters:
    survey_id (str): survey id of the collection
    schema_processor_service (SchemaProcessorService): injected dependency for processing the metadata collection.
    """
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

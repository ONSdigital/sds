from fastapi import APIRouter, Body, Depends, HTTPException
from logging_config import logging
from models.schema_models import Schema, SchemaMetadataWithGuid
from repositories.buckets.schema_bucket_repository import SchemaBucketRepository
from repositories.firebase.schema_firebase_repository import SchemaFirebaseRepository
from services.schema.schema_processor_service import SchemaProcessorService

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/v1/schema", response_model=SchemaMetadataWithGuid)
async def post_schema_metadata(
    schema: Schema = Body(...),
    schema_processor_service: SchemaProcessorService = Depends(),
):
    """
    Grab the survey_id from the schema file and call set_schema_metadata
    with the survey_id and schema_location and returned the generated
    schema metadata.
    """
    logger.info("Posting schema metadata...")
    logger.debug(f"Input body: {{{schema}}}")

    posted_schema_metadata = schema_processor_service.process_schema_metadata(schema)

    logger.info("Schema metadata successfully posted.")
    logger.debug(f"Schema metadata: {posted_schema_metadata}")

    return posted_schema_metadata


@router.get("/v1/schema")
async def get_file_from_bucket(
    survey_id: str,
    version: str,
    schema_firebase_repository: SchemaFirebaseRepository = Depends(),
    schema_bucket_repository: SchemaBucketRepository = Depends(),
) -> dict:
    """
    Lookup the schema metadata, given the survey_id and version. Then use
    that to look up the location of the schema file in the bucket and
    return that file.
    """
    logger.info("Getting bucket schema metadata...")
    logger.debug(f"Input data: survey_id={survey_id}, version={version}")

    bucket_schema_metadata_location = (
        schema_firebase_repository.get_schema_metadata_bucket_location(
            survey_id, version
        )
    )

    if not bucket_schema_metadata_location:
        logger.error("Schema metadata not found")
        raise HTTPException(status_code=404, detail="Schema metadata not found")

    logger.info("Bucket schema metadata location successfully retrieved.")
    logger.debug(f"Bucket schema metadata location: {bucket_schema_metadata_location}")
    logger.info("Getting schema metadata...")

    schema = schema_bucket_repository.get_bucket_file_as_json(
        bucket_schema_metadata_location
    )

    logger.info("Schema successfully retrieved.")
    logger.debug(f"Schema: {schema}")

    return schema

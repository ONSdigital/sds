from fastapi import APIRouter, Body, Depends
from logging_config import logging
from models.schema_models import Schema, SchemaMetadataWithGuid
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

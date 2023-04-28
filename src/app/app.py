import database
import storage
from fastapi import Body, Depends, FastAPI, HTTPException
from logging_config import logging
from models.dataset_models import DatasetMetadata
from models.schema_models import PostSchemaMetadata, ReturnedSchemaMetadata, Schema
from repositories.dataset_repository import DatasetRepository
from routers import dataset_router
from services.schema_metadata import schema_metadata_service

logger = logging.getLogger(__name__)
app = FastAPI()

app.include_router(dataset_router.router)


@app.post("/v1/schema", response_model=PostSchemaMetadata)
async def post_schema_metadata(schema: Schema = Body(...)):
    """
    Grab the survey_id from the schema file and call set_schema_metadata
    with the survey_id and schema_location and returned the generated
    schema metadata.
    """
    logger.info("Posting schema metadata...")
    logger.debug(f"Input body: {{{schema}}}")

    posted_schema_metadata = schema_metadata_service.process_schema_metadata(schema)

    logger.info("Schema metadata successfully posted.")
    logger.debug(f"Schema metadata: {posted_schema_metadata}")

    return posted_schema_metadata


@app.get("/v1/schema")
async def get_schema(survey_id: str, version: str) -> dict:
    """
    Lookup the schema metadata, given the survey_id and version. Then use
    that to look up the location of the schema file in the bucket and
    return that file.
    """
    logger.info("Getting schema metadata...")
    logger.debug(f"Input data: survey_id={survey_id}, version={version}")

    schema_metadata = database.get_schema_metadata(survey_id=survey_id, version=version)
    if not schema_metadata:
        logger.error("Schema metadata not found")
        raise HTTPException(status_code=404, detail="Schema metadata not found")

    logger.info("Schema metadata successfully retrieved.")
    logger.debug(f"Schema metadata: {schema_metadata}")

    logger.info("Getting schema...")

    schema = storage.get_schema(schema_metadata.schema_location)

    logger.info("Schema successfully retrieved.")
    logger.debug(f"Schema: {schema}")

    return schema


@app.get("/v1/schema_metadata", response_model=list[ReturnedSchemaMetadata])
async def get_schemas_metadata(survey_id: str) -> list[ReturnedSchemaMetadata]:
    """Retrieve the metadata for all the schemas that have a given survey_id."""
    logger.info("Getting schemas metadata...")
    logger.debug(f"Input data: survey_id={survey_id}")

    schemas_metadata = database.get_schemas_metadata(survey_id)

    logger.info("Schemas metadata successfully retrieved.")
    logger.debug(f"Schemas metadata: {schemas_metadata}")

    return schemas_metadata

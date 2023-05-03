import database
from fastapi import FastAPI
from logging_config import logging
from models.schema_models import SchemaMetadataWithGuid
from routers import dataset_router, schema_router

logger = logging.getLogger(__name__)
app = FastAPI()

app.include_router(dataset_router.router)
app.include_router(schema_router.router)


@app.get("/v1/schema_metadata", response_model=list[SchemaMetadataWithGuid])
async def get_schemas_metadata(survey_id: str) -> list[SchemaMetadataWithGuid]:
    """Retrieve the metadata for all the schemas that have a given survey_id."""
    logger.info("Getting schemas metadata...")
    logger.debug(f"Input data: survey_id={survey_id}")

    schemas_metadata = database.get_schemas_metadata(survey_id)

    logger.info("Schemas metadata successfully retrieved.")
    logger.debug(f"Schemas metadata: {schemas_metadata}")

    return schemas_metadata

import logging
import uuid

import database
import storage
from fastapi import Body, FastAPI, HTTPException
from models import Schema, SchemaMetadata, Schemas

logging.basicConfig(level=logging.INFO)


app = FastAPI()


@app.get("/v1/unit_data")
async def unit_data(dataset_id: str, unit_id: str):
    """Retrieve supplementary data for a particular unit given the unit id
    and the dataset id."""
    data = database.get_data(dataset_id=dataset_id, unit_id=unit_id)
    if not data:
        raise HTTPException(status_code=404, detail="Item not found")
    return data


@app.post("/v1/schema", response_model=SchemaMetadata)
async def publish_schema(schema: Schema = Body(...)):
    """
    Grab the survey_id from the schema file and call set_schema_metadata
    with the survey_id and schema_location and returned the generated
    schema metadata.
    """
    schema_id = str(uuid.uuid4())
    location = storage.store_schema(schema=schema, schema_id=schema_id)
    return database.set_schema_metadata(
        survey_id=schema.survey_id, schema_location=location, schema_id=schema_id
    )


@app.get("/v1/schema")
async def get_schema(survey_id: str, version: str) -> dict:
    """
    Lookup the schema metadata, given the survey_id and version. Then use
    that to lookup the location of the schema file in the bucket and
    return that file.
    """
    schema_metadata = database.get_schema(survey_id=survey_id, version=version)
    if not schema_metadata:
        raise HTTPException(status_code=404, detail="Item not found")
    return storage.get_schema(schema_metadata.schema_location)


@app.get("/v1/schema_metadata", response_model=Schemas)
async def query_schemas(survey_id: str) -> dict:
    """Retrieve the metadata for all the schemas that have a given survey_id."""
    data = database.get_schemas(survey_id)
    return data


@app.get("/datasets")
async def query_datasets(survey_id: str):
    """Retrieve the datasets, given the survey_id."""
    data = database.get_datasets(survey_id)
    return data

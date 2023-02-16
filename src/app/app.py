import logging
import uuid

import database
from fastapi import Body, FastAPI
from models import Schema, SchemaMetadata, Schemas

logging.basicConfig(level=logging.INFO)


app = FastAPI()


@app.post("/dataset")
async def dataset(payload: dict = Body(...)):
    """Put a dataset file into the database and return the dataset id."""
    dataset_id = str(uuid.uuid4())
    for sup_data in payload["data"]:
        database.set_data(dataset_id, sup_data)
    database.set_dataset(dataset_id, payload)
    return {"dataset_id": dataset_id}


@app.get("/unit_data")
async def unit_data(dataset_id: str, unit_id: str):
    """Retrieve supplementary data for a particular unit given the unit id
    and the dataset id."""
    data = database.get_data(dataset_id=dataset_id, unit_id=unit_id)
    return data


@app.post("/v1/schema", response_model=SchemaMetadata)
async def publish_schema(schema: Schema = Body(...)):
    """
    Grab the survey_id from the schema file and call set_schema_metadata
    with the survey_id and schema_location and returned the generated
    schema metadata.
    """
    return database.set_schema_metadata(survey_id=schema.survey_id, schema_location="/")


@app.get("/dataset_schema")
async def retrieve_schema(dataset_schema_id: str, version: int):
    """Retrieve the schema, given the schema_id."""
    data = database.get_schema(dataset_schema_id, version)
    return data


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

import logging
import uuid

import uvicorn
from fastapi import Body, FastAPI, Response

import database
from constants import (
    CONTENT_TYPE,
    DATASET_ID,
    DATASETS,
    OK,
    SCHEMA,
    SCHEMA_ID,
    SCHEMAS,
    SURVEY_ID,
    VERSION,
)
from content_types import TEXT_PLAIN_CONTENT_TYPE
from paths import (
    DATASET_PATH,
    DATASETS_PATH,
    HEALTHCHECK_PATH,
    SCHEMA_PATH,
    SCHEMAS_PATH,
)

level = logging.INFO

logging.basicConfig(level=level)


app = FastAPI()


@app.get(HEALTHCHECK_PATH)
async def get_healthcheck():
    """The healthcheck path."""
    content = OK

    headers = {CONTENT_TYPE: TEXT_PLAIN_CONTENT_TYPE}

    response = Response(content=content, headers=headers)

    return response


@app.get(SCHEMA_PATH)
async def get_schema(schema_id: str, version: str):
    """Get a schema given an identifier and version."""
    schema = database.get_schema(schema_id, version)

    json = {SCHEMA: schema, VERSION: version, SCHEMA_ID: schema_id}

    return json


@app.get(SCHEMAS_PATH)
async def get_schemas(survey_id: str):
    """Get all schemas for a given survey identifier."""
    schemas = database.get_schemas(survey_id)

    json = {SCHEMAS: schemas, SURVEY_ID: survey_id}

    return json


@app.get(DATASETS_PATH)
async def get_datasets(survey_id: str):
    """Get all datasets for a given survey identifier."""
    datasets = database.get_datasets(survey_id)

    json = {DATASETS: datasets, SURVEY_ID: survey_id}

    return json


@app.post(SCHEMA_PATH)
async def post_schema(schema_id: str, survey_id: str, payload: dict = Body(...)):
    """Post a schema given an identifier and survey identifier."""
    version = database.set_schema(schema_id, survey_id, payload)

    json = {VERSION: version, SCHEMA_ID: schema_id, SURVEY_ID: survey_id}

    return json


@app.post(DATASET_PATH)
async def post_dataset(payload: dict = Body(...)):
    """Post a dataset."""
    dataset_id = str(uuid.uuid4())

    database.set_dataset(dataset_id, payload)

    json = {DATASET_ID: dataset_id}

    return json


if __name__ == "__main__":
    uvicorn.run("app:app")

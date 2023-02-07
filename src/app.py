import logging
import uuid
import uvicorn

from fastapi import Body, FastAPI, Response


import database

from content_types import TEXT_PLAIN_CONTENT_TYPE
from constants import (
    OK,
    SCHEMA,
    SCHEMAS,
    VERSION,
    DATASETS,
    SCHEMA_ID,
    SURVEY_ID,
    CONTENT_TYPE
)
from paths import (
    HEALTHCHECK_PATH,
    SCHEMA_PATH,
    DATASET_PATH,
    SCHEMAS_PATH,
    DATASETS_PATH,
    UNIT_DATA_PATH
)


level = logging.INFO

logging.basicConfig(level=level)


app = FastAPI()


@app.get(HEALTHCHECK_PATH)
async def get_healthcheck():
    content = OK

    headers = {
        CONTENT_TYPE: TEXT_PLAIN_CONTENT_TYPE
    }

    response = Response(content=content, headers=headers)

    return response


@app.get(SCHEMA_PATH)
async def get_schema(schema_id: str, version: int):
    schema = database.get_schema(schema_id, version)

    json = {
        SCHEMA: schema,
        VERSION: version,
        SCHEMA_ID: schema_id
    }

    return json


@app.get(SCHEMAS_PATH)
async def get_schemas(survey_id: str):
    schemas = database.get_schemas(survey_id)

    json = {
        SCHEMAS: schemas,
        SURVEY_ID: survey_id
    }

    return json


@app.get(DATASETS_PATH)
async def get_datasets(survey_id: str):
    datasets = database.get_datasets(survey_id)

    json = {
        DATASETS: datasets,
        SURVEY_ID: survey_id
    }

    return json


@app.get(UNIT_DATA_PATH)
async def get_unit_data(dataset_id: str, unit_id: str):
    data = database.get_data(dataset_id=dataset_id, unit_id=unit_id)
    return data


@app.post(DATASET_PATH)
async def post_dataset(payload: dict = Body(...)):
    dataset_id = str(uuid.uuid4())
    for sup_data in payload["data"]:
        database.set_data(dataset_id, sup_data)
    database.set_dataset(dataset_id, payload)
    return {"dataset_id": dataset_id}


@app.post(SCHEMA_PATH)
async def post_dataset_schema(dataset_schema_id: str, survey_id: str, payload: dict = Body(...)):
    version = database.set_schema(dataset_schema_id, survey_id, payload)
    return {"dataset_schema_id": dataset_schema_id, "version": version}


if __name__ == "__main__":
    uvicorn.run("app:app")

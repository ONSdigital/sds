import logging
import uuid

from fastapi import Body, FastAPI, Response


import database

from constants import OK
from paths import (
    HEALTHCHECK_PATH,
    DATASET_PATH,
    DATASETS_PATH,
    UNIT_DATA_PATH,
    DATASET_SCHEMA_PATH,
    DATASET_SCHEMAS_PATH
)


level = logging.INFO

logging.basicConfig(level=level)


app = FastAPI()


@app.get(HEALTHCHECK_PATH)
async def get_healthcheck(response: Response):
    print("setting headers...")

    response.headers["content-type"] = "text/plain"

    return OK


@app.get(DATASETS_PATH)
async def get_datasets(survey_id: str):
    data = database.get_datasets(survey_id)
    return data


@app.get(UNIT_DATA_PATH)
async def get_unit_data(dataset_id: str, unit_id: str):
    data = database.get_data(dataset_id=dataset_id, unit_id=unit_id)
    return data


@app.get(DATASET_SCHEMA_PATH)
async def get_dataset_schema(dataset_schema_id: str, version: int):
    data = database.get_schema(dataset_schema_id, version)
    return data


@app.get(DATASET_SCHEMAS_PATH)
async def get_dataset_schemas(survey_id: str):
    data = database.get_schemas(survey_id)
    return data


@app.post(DATASET_PATH)
async def post_dataset(payload: dict = Body(...)):
    dataset_id = str(uuid.uuid4())
    for sup_data in payload["data"]:
        database.set_data(dataset_id, sup_data)
    database.set_dataset(dataset_id, payload)
    return {"dataset_id": dataset_id}


@app.post(DATASET_SCHEMA_PATH)
async def post_dataset_schema(dataset_schema_id: str, survey_id: str, payload: dict = Body(...)):
    version = database.set_schema(dataset_schema_id, survey_id, payload)
    return {"dataset_schema_id": dataset_schema_id, "version": version}



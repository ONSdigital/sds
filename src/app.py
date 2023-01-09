import logging
import uuid

import database

logging.basicConfig(level=logging.INFO)

from fastapi import Body, FastAPI

app = FastAPI()


@app.post("/dataset")
async def dataset(payload: dict = Body(...)):
    """Put a dataset file into the database and return the dataset id."""
    dataset_id = str(uuid.uuid4())
    for sup_data in payload["data"]:
        database.set_data(dataset_id, sup_data)
    return {"dataset_id": dataset_id}


@app.get("/unit_data")
async def unit_data(dataset_id: str, unit_id: str):
    """Retrieve supplementary data for a particular unit given the unit id
    and the dataset id."""
    data = database.get_data(dataset_id=dataset_id, unit_id=unit_id)
    return data


@app.post("/dataset_design")
async def publish_schema(dataset_design_id: str, payload: dict = Body(...)):
    """Put a schema into the database and return the schema_id."""
    version = database.set_schema(dataset_design_id, payload)
    return {"dataset_design_id": dataset_design_id, "version": version}


@app.get("/dataset_design")
async def retrieve_schema(dataset_design_id: str, version: int):
    """Retrieve the schema, given the schema_id."""
    data = database.get_schema(dataset_design_id, version)
    return data

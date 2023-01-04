import logging
import uuid

import database

logging.basicConfig(level=logging.INFO)

from fastapi import Body, FastAPI

app = FastAPI()


@app.post("/data_set")
async def data_set(payload: dict = Body(...)):
    """Put a dataset file into the database and return the data_set id."""
    data_set_id = str(uuid.uuid4())
    for sup_data in payload["data"]:
        database.set_data(data_set_id, sup_data)
    return {"data_set_id": data_set_id}


@app.get("/unit_data")
async def unit_data(data_set_id: str, unit_id: str):
    """Retrieve supplementary data for a particular unit given the unit id
    and the dataset id."""
    data = database.get_data(data_set_id=data_set_id, unit_id=unit_id)
    return data


@app.post("/schema")
async def publish_schema(payload: dict = Body(...)):
    """Put a schema into the database and return the schema_id."""
    schema_id = str(uuid.uuid4())
    database.set_schema(schema_id, payload)
    return {"schema_id": schema_id}


@app.get("/schema")
async def retrieve_schema(schema_id: str):
    """Retrieve the schema, given the schema_id."""
    data = database.get_schema(schema_id=schema_id)
    return data

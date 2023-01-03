import logging
import uuid

import database

logging.basicConfig(level=logging.INFO)

from fastapi import Body, FastAPI

app = FastAPI()


@app.post("/publish")
async def publish(payload: dict = Body(...)):
    """Put a dataset file into the database and return the data_set id."""
    print(payload)
    data_set_id = str(uuid.uuid4())
    for sup_data in payload["data"]:
        database.set_data(data_set_id, sup_data)
    return {"data_set_id": data_set_id}


@app.get("/unit_data")
async def retrieve(data_set_id: str, unit_id: str):
    """Retrieve supplementary data for a particular unit given the unit id
    and the dataset id."""
    data = database.get_data(data_set_id=data_set_id, unit_id=unit_id)
    return data

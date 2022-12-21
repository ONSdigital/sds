import logging

import database

logging.basicConfig(level=logging.INFO)

from fastapi import Body, FastAPI, Header

app = FastAPI(docs_url=None, redoc_url=None)


@app.put("/publish")
async def publish(payload: dict = Body(...)):
    print(payload)
    for sup_data in payload["data"]:
        database.set_data(payload["data_set_id"], sup_data)
    """Put a dataset file into the database."""


@app.get("/unit_data")
async def retrieve(data_set_id: str, unit_id: str):
    """Retrieve supplementary data for a particular unit given the unit id
    and the dataset id."""
    data = database.get_data(data_set_id=data_set_id, unit_id=unit_id)
    return data

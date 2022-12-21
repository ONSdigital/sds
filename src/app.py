import logging
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

logging.basicConfig(level=logging.INFO)

from fastapi import FastAPI, Request, Body

app = FastAPI(docs_url=None, redoc_url=None)

class Item(BaseModel):
    pass

@app.put("/publish")
async def publish(payload: dict = Body(...)):
    print(payload)
    """Put a dataset file into the database."""



@app.get("/retrieve")
async def retrieve():
    """Retrieve supplementary data for a particular unit given the unit id
    and the dataset id."""



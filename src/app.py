import logging
import uuid

from fastapi import Body, FastAPI
from pydantic import BaseModel

import database

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


@app.post("/dataset_schema")
async def publish_schema(
    dataset_schema_id: str, survey_id: str, payload: dict = Body(...)
):
    """Put a schema into the database and return the schema_id."""
    version = database.set_schema(dataset_schema_id, survey_id, payload)
    return {"dataset_schema_id": dataset_schema_id, "version": version}


@app.get("/dataset_schema")
async def retrieve_schema(dataset_schema_id: str, version: int):
    """Retrieve the schema, given the schema_id."""
    data = database.get_schema(dataset_schema_id, version)
    return data


class SchemaMetadata(BaseModel):
    survey_id: str
    schema_location: str
    sds_schema_version: int
    sds_published_at: str


class Schemas(BaseModel):
    supplementary_dataset_schema: dict[str, SchemaMetadata]


@app.get("/v1/schema_metadata")
async def query_schemas(survey_id: str) -> Schemas:
    """Retrieve the schemas, given the survey_id."""
    # data = database.get_schemas(survey_id)
    return Schemas(
        supplementary_dataset_schema={
            "x": SchemaMetadata(
                survey_id="x",
                schema_location="y",
                sds_schema_version=1,
                sds_published_at="x",
            )
        }
    )


@app.get("/datasets")
async def query_datasets(survey_id: str):
    """Retrieve the datasets, given the survey_id."""
    data = database.get_datasets(survey_id)
    return data

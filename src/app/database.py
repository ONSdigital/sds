from dataclasses import asdict
from datetime import datetime

import firebase_admin
from config.config_factory import ConfigFactory
from firebase_admin import firestore
from models.dataset_models import DatasetMetadata
from models.schema_models import (
    PostSchemaMetadata,
    ReturnedSchemaMetadata,
    SchemaMetadata,
)

firebase_admin.initialize_app()
db = firestore.client()
datasets_collection = db.collection("datasets")
schemas_collection = db.collection("schemas")
config = ConfigFactory.get_config()


def set_schema_metadata(survey_id, schema_location, schema_id) -> PostSchemaMetadata:
    """
    Takes the survey_id and schema_location (assumed to be in a bucket),
    and creates the metadata and stores it in Firebase. The latest version
    is acquired through querying the collection.
    This version is incremented and added to the meta-data.
    """
    schemas_result = (
        schemas_collection.where("survey_id", "==", survey_id)
        .order_by("sds_schema_version", direction=firestore.Query.DESCENDING)
        .limit(1)
        .stream()
    )

    try:
        latest_version = next(schemas_result).to_dict()["sds_schema_version"] + 1
    except StopIteration:
        latest_version = 1

    schema_metadata = PostSchemaMetadata(
        guid=schema_id,
        schema_location=schema_location,
        sds_schema_version=latest_version,
        survey_id=survey_id,
        sds_published_at=str(datetime.now().strftime(config.TIME_FORMAT)),
    )

    schemas_collection.document(schema_id).set(asdict(schema_metadata))
    return schema_metadata


def get_schemas_metadata(survey_id) -> list[ReturnedSchemaMetadata]:
    """
    Return all the schema meta-data that corresponds to a particular survey_id.

    Parameters:
        survey_id (str): the corresponding ID of the survey for the desired schema

    Returns:
        list[SchemaMetadata]: a list of all the metadata corresponding to the given ID
    """

    dataset_schemas = list()
    schemas_result = schemas_collection.where("survey_id", "==", survey_id).stream()

    for schema in schemas_result:
        return_schema = schema.to_dict()
        return_schema["guid"] = schema.id
        dataset_schemas.append(return_schema)

    return dataset_schemas


def get_datasets(survey_id):
    """
    Get a list of matching dataset meta-data, given the survey_id.
    """
    datasets = []
    datasets_result = datasets_collection.where("survey_id", "==", survey_id).stream()
    for dataset in datasets_result:
        return_dataset = dataset.to_dict()
        return_dataset.pop("survey_id")
        return_dataset["dataset_id"] = dataset.id
        datasets.append(return_dataset)
    return {"survey_id": survey_id, "datasets": datasets}


def get_schema_metadata(survey_id, version) -> SchemaMetadata:
    schemas_result = (
        schemas_collection.where("survey_id", "==", survey_id)
        .where("sds_schema_version", "==", int(version))
        .stream()
    )

    for schema in schemas_result:
        return_metadata = schema.to_dict()
        if "guid" in return_metadata:
            return_metadata.pop("guid")
        return SchemaMetadata(**return_metadata)

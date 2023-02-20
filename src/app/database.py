import os
from dataclasses import asdict
from datetime import datetime

import firebase_admin
from firebase_admin import firestore
from models import SchemaMetadata

if os.environ.get("KEYFILE_LOCATION"):
    cred_obj = firebase_admin.credentials.Certificate(
        os.environ.get("KEYFILE_LOCATION")
    )
    firebase_admin.initialize_app(cred_obj)
else:
    firebase_admin.initialize_app()
db = firestore.client()
datasets_collection = db.collection("datasets")
schemas_collection = db.collection("schemas")


def set_dataset(dataset_id, dataset):
    dataset.pop("data")
    datasets_collection.document(dataset_id).set(dataset)


def set_data(dataset_id, data):
    units_collection = datasets_collection.document(dataset_id).collection("units")
    units_collection.document(data["unit_id"]).set(data)


def get_data(dataset_id, unit_id):
    units_collection = datasets_collection.document(dataset_id).collection("units")
    return units_collection.document(unit_id).get().to_dict()


def set_schema_metadata(survey_id, schema_location, schema_id):
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
    schema_metadata = SchemaMetadata(
        schema_location=schema_location,
        sds_schema_version=latest_version,
        survey_id=survey_id,
        sds_published_at=str(datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")),
    )
    schemas_collection.document(schema_id).set(asdict(schema_metadata))
    return schema_metadata


def get_schemas(survey_id):
    dataset_schemas = {}
    schemas_result = schemas_collection.where("survey_id", "==", survey_id).stream()
    for schema in schemas_result:
        return_schema = schema.to_dict()
        dataset_schemas[schema.id] = return_schema
    return {"supplementary_dataset_schema": dataset_schemas}


def get_datasets(survey_id):
    datasets = []
    datasets_result = datasets_collection.where("survey_id", "==", survey_id).stream()
    for dataset in datasets_result:
        return_dataset = dataset.to_dict()
        return_dataset.pop("survey_id")
        return_dataset["dataset_id"] = dataset.id
        datasets.append(return_dataset)
    return {"survey_id": survey_id, "datasets": datasets}

import os
import uuid
from dataclasses import asdict
from datetime import datetime

import firebase_admin
from firebase_admin import firestore
from models import SchemaMetadata

cred_obj = firebase_admin.credentials.Certificate(
    os.environ.get("FIREBASE_KEYFILE_LOCATION")
)
default_app = firebase_admin.initialize_app(cred_obj)
db = firestore.client()
datasets_collection = db.collection("datasets")
schemas_collection = db.collection("schemas")
surveys_collection = db.collection("surveys")


def set_dataset(dataset_id, dataset):
    dataset.pop("data")
    datasets_collection.document(dataset_id).set(dataset)


def set_data(dataset_id, data):
    units_collection = datasets_collection.document(dataset_id).collection("units")
    units_collection.document(data["unit_id"]).set(data)


def get_data(dataset_id, unit_id):
    units_collection = datasets_collection.document(dataset_id).collection("units")
    return units_collection.document(unit_id).get().to_dict()


def set_schema_metadata(survey_id, schema_location):
    """
    Takes the survey_id and schema_location (assumed to be in a bucket),
    and creates the metadata and stores it in Firebase. The latest version
    is kept track of in a separate collection using the survey_id as the
    key. This version is incremented and added to the meta-data.
    """
    surveys = surveys_collection.document(survey_id)
    if not surveys.get().exists:
        surveys.set({"latest_schema_version": 1})
        latest_version = 1
    else:
        latest_version = surveys.get().to_dict()["latest_schema_version"]
        latest_version += 1
    surveys.update({"latest_schema_version": latest_version})
    guid = str(uuid.uuid4())
    schema_meta_data = SchemaMetadata(
        schema_location=schema_location,
        sds_schema_version=latest_version,
        survey_id=survey_id,
        sds_published_at=str(datetime.now()),
    )
    schemas_collection.document(guid).set(asdict(schema_meta_data))


def get_schema(dataset_schema_id, version):
    return (
        schemas_collection.document(dataset_schema_id)
        .collection("versions")
        .document(str(version))
        .get()
        .to_dict()
    )


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

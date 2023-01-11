import os

import firebase_admin
from firebase_admin import firestore

cred_obj = firebase_admin.credentials.Certificate(
    os.environ.get("FIREBASE_KEYFILE_LOCATION")
)
default_app = firebase_admin.initialize_app(cred_obj)
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


def set_schema(dataset_schema_id, survey_id, dataset_schema):
    dataset_schema_versions = schemas_collection.document(dataset_schema_id)
    if not dataset_schema_versions.get().exists:
        dataset_schema_versions.set({"latest": 1, "survey_id": survey_id})
        latest_version = 1
    else:
        latest_version = dataset_schema_versions.get().to_dict()["latest"]
        latest_version += 1
    dataset_schema_versions.collection("versions").document(str(latest_version)).set(
        dataset_schema
    )
    dataset_schema_versions.update({"latest": latest_version})
    return latest_version


def get_schema(dataset_schema_id, version):
    return (
        schemas_collection.document(dataset_schema_id)
        .collection("versions")
        .document(str(version))
        .get()
        .to_dict()
    )

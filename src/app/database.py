from dataclasses import asdict
from datetime import datetime

import firebase_admin
from firebase_admin import firestore
from models import (
    DatasetMetadata,
    PostSchemaMetadata,
    ReturnedSchemaMetadata,
    SchemaMetadata,
)

firebase_admin.initialize_app()
db = firestore.client()
datasets_collection = db.collection("datasets")
schemas_collection = db.collection("schemas")


def set_dataset(dataset_id, filename, dataset):
    """
    This method is invoked from the cloud function, it creates a dataset document in the firestore collection.
    * Added "sds_published_at" and "total_reporting_units" as new fields in the dataset dictionary.
    * Added "filename" as method argument passed from the cloud function which is the filename placed in the bucket.
    * Set the "filename" as a field in the dataset metadata document.
    """
    data = dataset.pop("data")
    dataset["filename"] = filename
    dataset["sds_published_at"] = str(datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"))
    dataset["total_reporting_units"] = len(data)

    datasets_result = (
        datasets_collection.where("survey_id", "==", dataset["survey_id"])
        .order_by("sds_dataset_version", direction=firestore.Query.DESCENDING)
        .limit(1)
        .stream()
    )
    try:
        latest_version = next(datasets_result).to_dict()["sds_dataset_version"] + 1
    except StopIteration:
        latest_version = 1

    dataset["sds_published_at"] = str(datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"))
    dataset["sds_dataset_version"] = latest_version
    dataset["total_reporting_units"] = len(data)
    datasets_collection.document(dataset_id).set(dataset)
    units_collection = datasets_collection.document(dataset_id).collection("units")
    for unit_data in data:
        units_collection.document(unit_data["ruref"]).set(unit_data)


def get_unit_supplementary_data(dataset_id, unit_id):
    """Get the unit data from dataset collection, that originally came from the dataset."""
    units_collection = datasets_collection.document(dataset_id).collection("units")
    return units_collection.document(unit_id).get().to_dict()


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
        sds_published_at=str(datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")),
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


def get_dataset_metadata_collection(
    survey_id: str, period_id: str
) -> list[DatasetMetadata]:
    """
    This method takes the survey_id and period_id as arguments, queries the firestore dataset document collection,
    and returns the matching datasets metadata which is a nested dictionary object with the dataset_id as the key.
    """
    datasets = []
    datasets_result = (
        datasets_collection.where("survey_id", "==", survey_id)
        .where("period_id", "==", period_id)
        .stream()
    )
    for dataset in datasets_result:
        return_dataset = dataset.to_dict()
        return_dataset["dataset_id"] = dataset.id
        datasets.append(return_dataset)

    return datasets


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

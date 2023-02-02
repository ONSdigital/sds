from client import client
from constants import (
    DATA,
    UNITS,
    UNIT_ID,
    SCHEMAS,
    DATASETS,
    VERSIONS,
    SURVEY_ID,
    DATASET_ID,
    DOUBLE_EQUALS,
    LATEST_VERSION,
    DATASET_SCHEMAS,
    DATASET_SCHEMA_ID
)


schemas_collection = client.collection(SCHEMAS)

datasets_collection = client.collection(DATASETS)


def set_dataset(dataset_id, dataset):
    dataset.pop(DATA)

    datasets_collection.document(dataset_id).set(dataset)


def set_data(dataset_id, data):
    units_collection = datasets_collection.document(dataset_id).collection(UNITS)

    units_collection.document(data[UNIT_ID]).set(data)


def get_data(dataset_id, unit_id):
    units_collection = datasets_collection.document(dataset_id).collection(UNITS)

    return units_collection.document(unit_id).get().to_dict()


def set_schema(dataset_schema_id, survey_id, dataset_schema):
    dataset_schema_versions = schemas_collection.document(dataset_schema_id)

    if not dataset_schema_versions.get().exists:
        dataset_schema_versions.set({LATEST_VERSION: 1, SURVEY_ID: survey_id})

        latest_version = 1

    else:
        latest_version = dataset_schema_versions.get().to_dict()[LATEST_VERSION]

        latest_version += 1

    dataset_schema_versions.collection(VERSIONS).document(str(latest_version)).set(
        dataset_schema
    )

    dataset_schema_versions.update({LATEST_VERSION: latest_version})

    return latest_version


def get_schema(dataset_schema_id, version):
    version_string = str(version)

    schema = schemas_collection.document(dataset_schema_id) \
        .collection(VERSIONS) \
        .document(version_string) \
        .get() \
        .to_dict()

    return schema


def get_schemas(survey_id):
    dataset_schemas = []

    schemas_result = schemas_collection.where(SURVEY_ID, DOUBLE_EQUALS, survey_id).stream()

    for schema in schemas_result:
        return_schema = schema.to_dict()

        return_schema.pop(SURVEY_ID)

        return_schema[DATASET_SCHEMA_ID] = schema.id

        dataset_schemas.append(return_schema)

    return {
        SURVEY_ID: survey_id,
        DATASET_SCHEMAS: dataset_schemas
    }


def get_datasets(survey_id):
    datasets = []

    datasets_result = datasets_collection.where(SURVEY_ID, DOUBLE_EQUALS, survey_id).stream()

    for dataset in datasets_result:
        return_dataset = dataset.to_dict()

        return_dataset.pop(SURVEY_ID)

        return_dataset[DATASET_ID] = dataset.id

        datasets.append(return_dataset)

    return {
        SURVEY_ID: survey_id,
        DATASETS: datasets
    }

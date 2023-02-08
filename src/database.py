from client import client
from constants import (
    DATA,
    UNITS,
    UNIT_ID,
    SCHEMAS,
    VERSION,
    DATASETS,
    VERSIONS,
    SCHEMA_ID,
    SURVEY_ID,
    DATASET_ID,
    DOUBLE_EQUALS,
    DATASET_SCHEMAS,
    DATASET_SCHEMA_ID
)


schemas_collection = client.collection(SCHEMAS)

datasets_collection = client.collection(DATASETS)


def set_data(dataset_id, data):
    units_collection = datasets_collection.document(dataset_id).collection(UNITS)

    units_collection.document(data[UNIT_ID]).set(data)


def get_data(dataset_id, unit_id):
    units_collection = datasets_collection.document(dataset_id).collection(UNITS)

    return units_collection.document(unit_id).get().to_dict()


def set_schema(schema_id, survey_id, payload):
    schemas_collection_document = schemas_collection.document(schema_id)

    schema_result = schemas_collection_document.get()

    if not schema_result.exists:
        version = 1

        schemas_collection_document.set({
            SURVEY_ID: survey_id
        })

    else:
        schema = schema_result.to_dict()

        version = schema[VERSION]

        version += 1

    schemas_collection_document.update({
        VERSION: version
    })

    version = str(version)

    return version


def set_dataset(dataset_id, dataset):
    dataset.pop(DATA)

    datasets_collection.document(dataset_id).set(dataset)


def get_schema(schema_id, version):
    schemas_collection_document = schemas_collection.document(schema_id)

    schema = schemas_collection_document \
        .collection(VERSIONS) \
        .document(version) \
        .get() \
        .to_dict()

    return schema


def get_schemas(survey_id):
    schemas = []

    schema_results = schemas_collection.where(SURVEY_ID, DOUBLE_EQUALS, survey_id).stream()

    for schema_result in schema_results:
        schema = schema_result.to_dict()

        schema.pop(SURVEY_ID)

        schemas.append(schema)

    return schemas


def get_datasets(survey_id):
    datasets = []

    dataset_results = datasets_collection.where(SURVEY_ID, DOUBLE_EQUALS, survey_id).stream()

    for dataset_result in dataset_results:
        dataset = dataset_result.to_dict()

        dataset.pop(SURVEY_ID)

        datasets.append(dataset)

    return datasets

from client import client
from constants import SCHEMAS, VERSION, DATASETS, SURVEY_ID


schemas_collection = client.collection(SCHEMAS)

datasets_collection = client.collection(DATASETS)


def set_schema(schema_id, survey_id, payload):
    schemas_collection_document = schemas_collection.document(schema_id)

    schema_result = schemas_collection_document.get()

    schema_result_exists = schema_result.exists

    if schema_result_exists:
        schema = schema_result.to_dict()

        version = schema[VERSION]

        version += 1

    else:
        schemas_collection_document.set({SURVEY_ID: survey_id})

        version = 1

    schemas_collection_document.update({VERSION: version})

    version = str(version)

    return version


def get_schema(schema_id, version):
    schemas_collection_document = schemas_collection.document(schema_id)

    schema_result = schemas_collection_document.get()

    schema = schema_result.to_dict()

    return schema


def get_schemas(survey_id):
    schemas = []

    schema_results = schemas_collection.where(SURVEY_ID, "==", survey_id).stream()

    for schema_result in schema_results:
        schema = schema_result.to_dict()

        schema.pop(SURVEY_ID)

        schemas.append(schema)

    return schemas


def delete_schema(schema_id):
    schemas_collection_document = schemas_collection.document(schema_id)

    schemas_collection_document.delete()


def set_dataset(dataset_id, payload):
    datasets_collection_document = datasets_collection.document(dataset_id)

    datasets_collection_document.set(payload)


def get_datasets(survey_id):
    datasets = []

    dataset_results = datasets_collection.where(
        SURVEY_ID, DOUBLE_EQUALS, survey_id
    ).stream()

    for dataset_result in dataset_results:
        dataset = dataset_result.to_dict()

        dataset.pop(SURVEY_ID)

        datasets.append(dataset)

    return datasets

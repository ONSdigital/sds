from json import load as json_load, loads as json_loads
from urllib import parse


from paths import (
    SCHEMA_PATH,
    DATASET_PATH,
    SCHEMAS_PATH,
    DATASETS_PATH
)
from constants import (
    SCHEMA,
    VERSION,
    SCHEMAS,
    DATASETS,
    SURVEY_ID,
    SCHEMA_ID,
    DATASET_ID
)
from database import schemas_collection


URL = u'{path}?{query_string}'


def test_get_schema(test_client):
    version = "1"
    schema_id = "0"

    parameters = {
        VERSION: version,
        SCHEMA_ID: schema_id
    }

    path = SCHEMA_PATH

    query_string = parse.urlencode(parameters)

    url = URL.format(path=path, query_string=query_string)

    response = test_client.get(url)

    status_code = response.status_code

    assert status_code == 200

    text = response.text

    json = json_loads(text)

    schema = json[SCHEMA]

    assert schema is not None


def _test_get_schemas(test_client):
    survey_id = "0"

    parameters = {
        SURVEY_ID: survey_id
    }

    path = SCHEMAS_PATH

    query_string = parse.urlencode(parameters)

    url = URL.format(path=path, query_string=query_string)

    response = test_client.get(url)

    status_code = response.status_code

    assert status_code == 200

    text = response.text

    json = json_loads(text)

    schemas = json[SCHEMAS]

    schemas_length = len(schemas)

    assert schemas_length == 0


def _test_get_datasets(test_client):
    survey_id = "0"

    parameters = {
        SURVEY_ID: survey_id
    }

    path = DATASETS_PATH

    query_string = parse.urlencode(parameters)

    url = URL.format(path=path, query_string=query_string)

    response = test_client.get(url)

    status_code = response.status_code

    assert status_code == 200

    text = response.text

    json = json_loads(text)

    datasets = json[DATASETS]

    datasets_length = len(datasets)

    assert datasets_length == 0


def _test_post_schema(test_client):
    schema_id = "1"

    survey_id = "1"

    schemas_collection_document = schemas_collection.document(schema_id)

    schemas_collection_document.delete()

    with open("test/integration/data/schema.json") as schema_json_file:
        schema_json = json_load(schema_json_file)

    parameters = {
        SURVEY_ID: survey_id,
        SCHEMA_ID: schema_id
    }

    json = schema_json

    path = SCHEMA_PATH

    query_string = parse.urlencode(parameters)

    url = URL.format(path=path, query_string=query_string)

    response = test_client.post(url, json=json)

    status_code = response.status_code

    assert status_code == 200

    text = response.text

    json = json_loads(text)

    version = json[VERSION]

    assert version == "2"


def _test_post_dataset(test_client):
    with open("test/integration/data/dataset.json") as dataset_json_file:
        dataset_json = json_load(dataset_json_file)

    parameters = {}

    json = dataset_json

    path = DATASET_PATH

    query_string = parse.urlencode(parameters)

    url = URL.format(path=path, query_string=query_string)

    response = test_client.post(url, json=json)

    status_code = response.status_code

    assert status_code == 200

    text = response.text

    json = json_loads(text)

    dataset_id = json[DATASET_ID]

    assert dataset_id is not None

import json

from urllib import parse


from paths import SCHEMAS_PATH
from constants import SURVEY_ID


URL = u'{path}?{query_string}'


def test_get_schemas(test_client):
    survey_id = 1

    parameters = {
        SURVEY_ID: survey_id
    }

    path = SCHEMAS_PATH

    query_string = parse.urlencode(parameters)

    url = URL.format(path=path, query_string=query_string)

    response = test_client.get(url)

    assert response.status_code == 200


def _test_dataset(test_client):
    with open("data/dataset.json") as f:
        dataset = json.load(f)
    response = test_client.post("/dataset", json=dataset)
    dataset_id = response.json()["dataset_id"]
    assert response.status_code == 200
    unit_id = "55e64129-6acd-438b-a23a-3cf9524ab912"
    response = test_client.get(f"/unit_data?dataset_id={dataset_id}&unit_id={unit_id}")
    assert response.status_code == 200
    assert response.json() == {
        "unit_id": "55e64129-6acd-438b-a23a-3cf9524ab912",
        "properties": {
            "sample_unit": {
                "units_of_sale": "MILES MAPPED",
                "currency_description": "SILVER COINS",
                "time_items": [
                    {"ref": "M1", "grade": "Chief mapper"},
                    {"ref": "M2", "grade": "Junior mapper"},
                    {"ref": "M3", "grade": "Bag carrier"},
                ],
            }
        },
    }


def _test_dataset_schema(test_client):
    with open("data/schema.json") as f:
        schema = json.load(f)
    dataset_schema_id = "sppi_dataset_schema"
    survey_id = "Survey 1"
    response = test_client.post(
        f"/dataset_schema?dataset_schema_id={dataset_schema_id}&survey_id={survey_id}",
        json=schema,
    )
    version = response.json()["version"]
    assert response.status_code == 200
    response = test_client.get(
        f"/dataset_schema?dataset_schema_id={dataset_schema_id}&version={version}"
    )
    assert response.status_code == 200
    assert response.json() == schema

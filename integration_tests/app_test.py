import json


def test_dataset(client):
    with open("data/dataset.json") as f:
        dataset = json.load(f)
    response = client.post("/dataset", json=dataset)
    dataset_id = response.json()["dataset_id"]
    assert response.status_code == 200
    unit_id = "55e64129-6acd-438b-a23a-3cf9524ab912"
    response = client.get(f"/unit_data?dataset_id={dataset_id}&unit_id={unit_id}")
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


def test_get_schema_metadata(client, database):
    survey_id = "xyz"
    schema_location = "/home_of_schema"
    database.set_schema_metadata(survey_id=survey_id, schema_location=schema_location)
    response = client.get(f"/v1/schema_metadata?survey_id={survey_id}")
    assert response.status_code == 200
    json_response = response.json()
    assert len(json_response["supplementary_dataset_schema"]) > 0
    for schema in json_response["supplementary_dataset_schema"].values():
        assert schema == {
            "survey_id": survey_id,
            "schema_location": schema_location,
            "sds_schema_version": schema["sds_schema_version"],
            "sds_published_at": schema["sds_published_at"],
        }

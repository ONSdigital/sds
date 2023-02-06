def _test_post_dataset(client):
    response = client.post("/dataset", json={"data": {}})
    dataset_id = response.json()["dataset_id"]
    assert response.status_code == 200
    unit_id = "55e64129-6acd-438b-a23a-3cf9524ab912"
    client.get(f"/unit_data?dataset_id={dataset_id}&unit_id={unit_id}")


def _test_get_unit_data(client):
    unit_id = "55e64129-6acd-438b-a23a-3cf9524ab912"
    dataset_id = "55e64129-6acd-438b-a23a-3cf9524ab912"
    client.get(f"/unit_data?dataset_id={dataset_id}&unit_id={unit_id}")


def _test_post_dataset_schema(client):
    dataset_schema_id = "sppi_dataset_schema"
    survey_id = "Survey 1"
    client.post(
        f"/dataset_schema?dataset_schema_id={dataset_schema_id}&survey_id={survey_id}",
        json={},
    )


def _test_get_dataset_schema(client):
    dataset_schema_id = "sppi_dataset_schema"
    version = "1"
    response = client.get(
        f"/dataset_schema?dataset_schema_id={dataset_schema_id}&version={version}"
    )
    assert response.status_code == 200


def _test_get_dataset_schemas(client):
    survey_id = "Survey 1"
    response = client.get(f"/dataset_schemas?&survey_id={survey_id}")
    assert response.status_code == 200


def _test_get_datasets(client):
    survey_id = "Survey 1"
    response = client.get(f"/datasets?&survey_id={survey_id}")
    assert response.status_code == 200

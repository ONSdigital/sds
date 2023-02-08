def test_post_dataset(client):
    response = client.post("/dataset", json={"data": {}})
    dataset_id = response.json()["dataset_id"]
    assert response.status_code == 200
    unit_id = "55e64129-6acd-438b-a23a-3cf9524ab912"
    client.get(f"/unit_data?dataset_id={dataset_id}&unit_id={unit_id}")


def test_get_unit_data(client):
    unit_id = "55e64129-6acd-438b-a23a-3cf9524ab912"
    dataset_id = "55e64129-6acd-438b-a23a-3cf9524ab912"
    client.get(f"/unit_data?dataset_id={dataset_id}&unit_id={unit_id}")


def test_post_dataset_schema(client):
    dataset_schema_id = "sppi_dataset_schema"
    survey_id = "Survey 1"
    client.post(
        f"/dataset_schema?dataset_schema_id={dataset_schema_id}&survey_id={survey_id}",
        json={},
    )


def test_get_dataset_schema(client):
    dataset_schema_id = "sppi_dataset_schema"
    version = "1"
    response = client.get(
        f"/dataset_schema?dataset_schema_id={dataset_schema_id}&version={version}"
    )
    assert response.status_code == 200


def test_query_schemas(client, database):
    schema_meta_data = {
        "supplementary_dataset_schema": {
            "111-222-xxx-fff": {
                "survey_id": "xxx",
                "schema_location": "GC-BUCKET:/schema/111-222-xxx-fff.json",
                "sds_schema_version": 1,
                "sds_published_at": "2023-02-06T13:33:44Z",
            }
        }
    }
    database.get_schemas = lambda _: schema_meta_data
    survey_id = "Survey 1"
    response = client.get(f"/v1/schema_metadata?survey_id={survey_id}")
    assert response.status_code == 200
    assert response.json() == schema_meta_data


def test_get_datasets(client):
    survey_id = "Survey 1"
    response = client.get(f"/datasets?&survey_id={survey_id}")
    assert response.status_code == 200

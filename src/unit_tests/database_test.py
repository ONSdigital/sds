from unittest.mock import MagicMock

import firebase_admin
import pytest
from firebase_admin import firestore


@pytest.fixture
def database(monkeypatch):
    monkeypatch.setattr(firebase_admin, "credentials", MagicMock())
    monkeypatch.setattr(firebase_admin, "initialize_app", MagicMock())
    monkeypatch.setattr(firestore, "client", MagicMock())
    import database

    yield database


def test_set_dataset(database):
    database.set_dataset(dataset_id="1", dataset={"data": {}})


def test_set_data(database):
    database.set_data(dataset_id="1", data={"unit_id": "fake_id"})


def test_get_data(database):
    database.get_data(dataset_id="1", unit_id="1")


def test_set_schema_metadata(database):
    database.set_schema_metadata(survey_id="1", schema_location="/")


def test_get_schema(database):
    database.get_schema(dataset_schema_id="1", version="1")


def test_get_schemas(database):
    """
    Mocks out the imports that talk to Firestore. This test will emulate that Firestore
    has returned a list of schemas and show that the get_schemas function has formulated
    them correctly into the expected structure.
    """
    expected_schema = {
        "survey_id": "xxx",
        "schema_location": "GC-BUCKET:/schema/111-222-xxx-fff.json",
        "sds_schema_version": 1,
        "sds_published_at": "2023-02-06T13:33:44Z",
    }
    schema_guid = "abc"
    mock_stream_obj = MagicMock()
    mock_stream_obj.to_dict.return_value = expected_schema
    mock_stream_obj.id = schema_guid
    database.schemas_collection.where().stream.return_value = [mock_stream_obj]
    schemas = database.get_schemas(survey_id="1")
    assert schemas["supplementary_dataset_schema"][schema_guid] == expected_schema


def test_get_datasets(database):
    database.get_datasets(survey_id="1")

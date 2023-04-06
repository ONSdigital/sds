import json
from unittest.mock import MagicMock


def test_set_dataset(database):
    # This test ensures that the 'set_dataset' database method is able to save the dataset metadata in the collection
    with open("../test_data/dataset.json") as f:
        dataset = json.load(f)
    database.set_dataset(dataset_id="1", filename="dataset.json", dataset=dataset)


def test_get_data(database):
    database.get_unit_supplementary_data(dataset_id="1", unit_id="1")


def test_set_schema_metadata(database):
    """
    Checks that set_schema_metadata accepts the survey_id and schema_location and stores them in
    a schema_meta_data object. Also checks that it generates a version number is which an increment
    of 1 over the highest version number of the schema with a matching survey_id.
    """
    database.schemas_collection.where().order_by().limit().stream().__next__().to_dict.return_value = {
        "sds_schema_version": 25
    }

    database.set_schema_metadata(survey_id="1", schema_location="/", schema_id="1")
    schema_meta_data = database.schemas_collection.document().set.call_args[0][0]

    assert schema_meta_data == {
        "guid": "1",
        "survey_id": "1",
        "schema_location": "/",
        "sds_schema_version": 26,
        "sds_published_at": schema_meta_data["sds_published_at"],
    }


def test_get_schemas(database):
    """
    Mocks out the imports that talk to Firestore. This test will emulate that Firestore
    has returned a list of schemas and show that the get_schemas function has formulated
    them correctly into the expected structure.
    """
    expected_schema = {
        "survey_id": "xyz",
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


def test_get_dataset_metadata(database):
    """
    Mocks the database collection document, invokes the get_dataset_metadata with the survey_id and period_id arguments,
    then checks that it returns the expected nested dictionary object which contains the dataset metadata.
    """
    expected_metadata = {
        "dataset_id": "abc-xyz",
        "survey_id": "xyz",
        "period_id": "abc",
        "title": "Which side was better?",
        "sds_schema_version": 4,
        "sds_published_at": "2023-03-13T14:34:57Z",
        "total_reporting_units": 2,
        "schema_version": "v1.0.0",
        "form_id": "yyy",
        "filename": "file1.json",
    }
    dataset_id = "abc-xyz"
    mock_stream_obj = MagicMock()
    mock_stream_obj.to_dict.return_value = expected_metadata
    mock_stream_obj.id = dataset_id
    database.schemas_collection.where().where().stream.return_value = [mock_stream_obj]
    dataset_metadata = database.get_dataset_metadata(survey_id="xyz", period_id="abc")
    assert dataset_metadata[0] == expected_metadata

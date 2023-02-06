def test_set_dataset(database):
    database.set_dataset(dataset_id="1", dataset={"data": {}})


def test_set_data(database):
    database.set_data(dataset_id="1", data={"unit_id": "fake_id"})


def test_get_data(database):
    database.get_data(dataset_id="1", unit_id="1")


def test_set_schema(database):
    database.set_schema(dataset_schema_id="1", survey_id="1", dataset_schema={})


def test_get_schema(database):
    database.get_schema(dataset_schema_id="1", version="1")


def test_get_schemas(database):
    database.get_schemas(survey_id="1")


def test_get_datasets(database):
    database.get_datasets(survey_id="1")

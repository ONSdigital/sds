def test_store_schema(storage):
    storage.store_schema({"survey_id": "abc"}, "1")


def test_get_schema(storage):
    storage.get_schema("/a_file.json")

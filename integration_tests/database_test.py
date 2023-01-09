import os

os.environ["FIREBASE_KEYFILE_LOCATION"] = "../firebase_key.json"

import database


def test_set_get_data():
    expected_data = {
        "unit_id": "2",
        "title": "Hello",
    }
    database.set_data(dataset_id="1", data=expected_data)
    actual_data = database.get_data(dataset_id="1", unit_id="2")
    assert actual_data == expected_data

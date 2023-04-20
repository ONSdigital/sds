import json
from unittest.mock import MagicMock, patch


def test_get_dataset_validate_keys(dataset_storage):
    with open("../test_data/dataset.json") as f:
        dataset = json.load(f)
    mandatory_keys = [
        "survey_id",
        "period_id",
        "sds_schema_version",
        "schema_version",
        "form_type",
        "data",
    ]
    missing_keys = []
    message = ""
    for key in mandatory_keys:
        dataset.pop(key)
        missing_keys.append(key)
        expected_message = ", ".join(missing_keys)

        isValid, message = dataset_storage.validate_keys(dataset)

        assert isValid == False
        assert message == expected_message

import json

from config.config_factory import ConfigFactory

config = ConfigFactory.get_config()


def test_get_dataset_invalid_json(dataset_storage):
    """
    This is to test the scenario when the file contains invalid JSON.
    The value in conftest.py has the survey_id without the quotes.
    """
    dataset = dataset_storage.get_dataset("dataset.json", "hello")
    assert not dataset


def test_get_dataset_validate_keys(dataset_storage):
    """
    This method checks if the 'validate_keys' method ensures that each mandatory key is present in the dataset JSON.
    """
    with open(config.TEST_DATASET_PATH) as f:
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

        assert [isValid, message] == [False, expected_message]

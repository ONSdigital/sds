import json
from unittest.mock import MagicMock, patch

def test_get_dataset_validate_keys(dataset_storage):
    mandatory_keys = ['survey_id', 'period_id', 'sds_schema_version', 'schema_version', 'form_type', 'data']
    for key in mandatory_keys:
        with open("../test_data/dataset.json") as f:
            dataset = json.load(f)          
        dataset.pop(key)
        isValid, message = dataset_storage.validate_keys(dataset)
        assert isValid == False
        assert message == key

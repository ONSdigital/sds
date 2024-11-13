from models.collection_exericise_end_data import CollectionExerciseEndData
from models.dataset_models import DatasetMetadata, DatasetMetadataWithoutId, UnitDataset

from src.test_data.shared_test_data import test_guid, test_survey_id, test_period_id

"""
Local variables:
"""
first_dataset_version = 1
updated_dataset_version = 2


"""
Test data:
"""



# unit test - dataset - test data
string_cat = "cat"
string_byte_size_cat = 5

# unit test - dataset - test data
empty_dict = {}
empty_dict_byte_size = 2

# unit tests - dataset - test data
identifier = "test_identifier"

# e2e dataset integration test - test data
int_identifier = "43532"

# unit tests - cloud new dataset - test data
dataset_unit_data_identifier: list[str] = ["43532", "65871"]

# integration test tests - dataset - test data
dataset_unit_data_id: list[str] = ["43532", "65871"]

# unit tests - service - test data
test_data_collection_end: CollectionExerciseEndData = CollectionExerciseEndData(
    **{
        "dataset_guid": test_guid,
        "survey_id": test_survey_id,
        "period_id": test_period_id,
    }
)

# unit tests - service - test data
test_data_collection_end_input: CollectionExerciseEndData = {
    "dataset_guid": test_guid,
    "survey_id": test_survey_id,
    "period_id": test_period_id,
}

# unit tests - service - test data
test_data_collection_end_missing_id: CollectionExerciseEndData = (
    CollectionExerciseEndData(
        **{
            "dataset_guid": "",
            "survey_id": test_survey_id,
            "period_id": test_period_id,
        }
    )
)

# unit tests - cloud new dataset - test data
dataset_metadata_first_version: DatasetMetadata = {
    "dataset_id": test_guid,
    "survey_id": test_survey_id,
    "period_id": test_period_id,
    "form_types": ["klk", "xyz", "tzr"],
    "title": "Which side was better?",
    "sds_published_at": "2023-04-20T12:00:00Z",
    "total_reporting_units": 2,
    "schema_version": "v1.0.0",
    "sds_dataset_version": first_dataset_version,
    "filename": "test_filename.json",
}

# unit tests - cloud new dataset - test data
dataset_metadata_updated_version: DatasetMetadata = {
    "dataset_id": test_guid,
    "survey_id": test_survey_id,
    "period_id": test_period_id,
    "form_types": ["klk", "xyz", "tzr"],
    "title": "Which side was better?",
    "sds_published_at": "2023-04-20T12:00:00Z",
    "total_reporting_units": 2,
    "schema_version": "v1.0.0",
    "sds_dataset_version": updated_dataset_version,
    "filename": "test_filename.json",
}

# integration test - dataset endpoints - test data
dataset_metadata_collection_for_endpoints_test: list[DatasetMetadata] = [
    {
        "dataset_id": "0",
        "survey_id": f"{test_survey_id}_1",
        "period_id": f"{test_period_id}_1",
        "form_types": ["sda", "ajk", "iwu"],
        "title": "Which side was better?",
        "sds_published_at": "2023-04-20T12:00:00Z",
        "total_reporting_units": 2,
        "schema_version": "v1.0.0",
        "sds_dataset_version": first_dataset_version,
        "filename": "test_filename.json",
    },
    {
        "dataset_id": "1",
        "survey_id": f"{test_survey_id}_2",
        "period_id": f"{test_period_id}_2",
        "form_types": ["390", "219", "12O"],
        "title": None,
        "sds_published_at": "2023-04-20T12:00:00Z",
        "total_reporting_units": 2,
        "schema_version": "v1.0.0",
        "sds_dataset_version": updated_dataset_version,
        "filename": "test_filename.json",
    },
]

# unit tests - dataset - test data
dataset_metadata_collection: list[DatasetMetadata] = [
    {
        "survey_id": f"{test_survey_id}_1",
        "period_id": test_period_id,
        "form_types": ["123", "456", "789"],
        "title": "Which side was better?",
        "sds_published_at": "2023-04-20T12:00:00Z",
        "total_reporting_units": 1,
        "schema_version": "v1.0.0",
        "sds_dataset_version": first_dataset_version,
        "filename": "test_filename.json",
        "dataset_id": "0",
    },
    {
        "survey_id": f"{test_survey_id}_2",
        "period_id": test_period_id,
        "form_types": ["abc", "def", "hij"],
        "title": "Which side was better 2?",
        "sds_published_at": "2023-04-20T12:00:00Z",
        "total_reporting_units": 1,
        "schema_version": "v1.0.0",
        "sds_dataset_version": updated_dataset_version,
        "filename": "test_filename.json",
        "dataset_id": "1",
    },
]

# unit tests - service - test data
dataset_metadata_collection_deletion: list[DatasetMetadata] = [
    {
        "survey_id": test_survey_id,
        "period_id": test_period_id,
        "form_types": ["123", "456", "789"],
        "title": "Which side was better?",
        "sds_published_at": "2023-04-20T12:00:00Z",
        "total_reporting_units": 1,
        "schema_version": "v1.0.0",
        "sds_dataset_version": first_dataset_version,
        "filename": "test_filename.json",
        "dataset_id": "0",
    },
    {
        "survey_id": test_survey_id,
        "period_id": test_period_id,
        "form_types": ["123", "456", "789"],
        "title": "Which side was better 2?",
        "sds_published_at": "2023-04-20T12:00:00Z",
        "total_reporting_units": 1,
        "schema_version": "v1.0.0",
        "sds_dataset_version": updated_dataset_version,
        "filename": "test_filename.json",
        "dataset_id": "1",
    },
]


# unit tests - cloud new dataset - test data
first_dataset_metadata_without_id: DatasetMetadataWithoutId = {
    "survey_id": test_survey_id,
    "period_id": test_period_id,
    "form_types": ["klk", "xyz", "tzr"],
    "title": "Which side was better?",
    "sds_published_at": "2023-04-20T12:00:00Z",
    "total_reporting_units": 2,
    "schema_version": "v1.0.0",
    "sds_dataset_version": first_dataset_version,
    "filename": "test_filename.json",
}

# unit tests - cloud new dataset - test data
updated_dataset_metadata_without_id: DatasetMetadataWithoutId = {
    "survey_id": test_survey_id,
    "period_id": test_period_id,
    "form_types": ["klk", "xyz", "tzr"],
    "title": "Which side was better?",
    "sds_published_at": "2023-04-20T12:00:00Z",
    "total_reporting_units": 2,
    "schema_version": "v1.0.0",
    "sds_dataset_version": updated_dataset_version,
    "filename": "test_filename.json",
}

# unit tests - cloud new dataset - test data
updated_dataset_metadata: DatasetMetadata = {
    **updated_dataset_metadata_without_id,
    "dataset_id": test_guid,
}

# integration test - dataset endpoints - test data
dataset_unit_data_collection_for_endpoints_test: list[UnitDataset] = [
    {
        "dataset_id": "",
        "survey_id": test_survey_id,
        "period_id": test_period_id,
        "schema_version": "v1.0.0",
        "form_types": ["jke", "als", "sma"],
        "data": "test",
    },
    {
        "dataset_id": "",
        "survey_id": test_survey_id,
        "period_id": test_period_id,
        "schema_version": "v1.0.0",
        "form_types": ["skn", "qwd", "qkw"],
        "data": "test"
    },
]

# unit tests - dataset - test data
unit_supplementary_data: UnitDataset = {
    "dataset_id": test_guid,
    "survey_id": test_survey_id,
    "period_id": test_period_id,
    "schema_version": "v1.0.0",
    "form_types": ["klk", "xyz", "tzr"],
    "data": {
        "identifier": identifier,
        "runame": "Pipes and Maps Ltd",
        "ruaddr1": "111 Under Hill",
        "ruaddr2": "Hobbitton",
        "ruaddr4": "The Shire",
        "rupostcode": "HO1 1AA",
        "payeref": "123AB456",
        "busdesc": "Provision of equipment for hobbit adventures",
        "local_unit": [
            {
                "identifier": "2012763A",
                "luname": "Maps Factory",
                "luaddr1": "1 Bag End",
                "luaddr2": "Underhill",
                "luaddr3": "Hobbiton",
                "lupostcode": "HO1 1AA",
                "tradstyle": "Also Does Adventures Ltd",
                "busdesc": "Creates old fashioned looking paper maps",
            },
            {
                "identifier": "20127364B",
                "luname": "Pipes R Us Subsidiary",
                "luaddr1": "12 The Farmstead",
                "luaddr2": "Maggotsville",
                "luaddr3": "Hobbiton",
                "lupostcode": "HO1 1AB",
                "busdesc": "Quality pipe manufacturer",
                "buslref": "pipe123",
            },
        ],
    },
}

# unit tests - cloud new dataset - test data
dataset_unit_data_collection: list[UnitDataset] = [
    {
        "dataset_id": test_guid,
        "survey_id": test_survey_id,
        "period_id": test_period_id,
        "schema_version": "v1.0.0",
        "form_types": ["klk", "xyz", "tzr"],
        "data": "<encrypted data>",
    },
    {
        "dataset_id": test_guid,
        "survey_id": test_survey_id,
        "period_id": test_period_id,
        "schema_version": "v1.0.0",
        "form_types": ["klk", "xyz", "tzr"],
        "data": {
            "identifier": "65871",
            "runame": "Boats and Floats Ltd",
            "ruaddr1": "111 Upper Hill",
            "ruaddr2": "Mordor",
            "rupostcode": "HO10 1AA",
            "payeref": "8888",
            "busdesc": "Provision of equipment for the bad guys.",
            "local_unit": [
                {
                    "identifier": "2012763A",
                    "luname": "Arms Factory",
                    "luaddr1": "1 Bag End",
                    "luaddr2": "Underhill",
                    "luaddr3": "Hobbiton",
                    "lupostcode": "HO1 1AA",
                    "tradstyle": "Also Does Adventures Ltd",
                    "busdesc": "Creates old fashioned looking paper maps",
                },
                {
                    "identifier": "20127364B",
                    "luname": "Swords Subsidiary",
                    "luaddr1": "12 The Farmstead",
                    "luaddr2": "Maggotsville",
                    "luaddr3": "Hobbiton",
                    "lupostcode": "HO1 1AB",
                    "busdesc": "Quality pipe manufacturer",
                    "buslref": "pipe123",
                },
                {
                    "identifier": "20127365C",
                    "luname": "Armor N Things",
                    "luaddr1": "5 Barrow Lane",
                    "luaddr2": "Striderton",
                    "luaddr3": "Bree",
                    "lupostcode": "BR1 1AC",
                    "busdesc": "Magic ring foundry",
                },
            ],
        },
    },
]

# unit tests - cloud new dataset - test data
missing_keys_dataset_metadata = {
    "period_id": test_period_id,
    "schema_version": 1,
    "form_types": [
        "abc",
        "def",
        "ghi",
    ],
    "data": [{"unit_data": "test_data", "identifier": "12345"}],
}

# e2e dataset integration test - test data
nonrandom_pubsub_first_dataset_metadata = {
    "survey_id": test_survey_id,
    "period_id": test_period_id,
    "form_types": ["klk", "xyz", "tzr"],
    "title": "Which side was better?",
    "total_reporting_units": 2,
    "schema_version": "v1.0.0",
    "sds_dataset_version": first_dataset_version,
}

# e2e dataset integration test - test data
nonrandom_pubsub_second_dataset_metadata = {
    "survey_id": test_survey_id,
    "period_id": test_period_id,
    "form_types": ["abc", "fgg", "ynm"],
    "title": "Which side was better? - Amended",
    "total_reporting_units": 3,
    "schema_version": "v2.0.0",
    "sds_dataset_version": updated_dataset_version,
}

# e2e dataset integration test - test data
unit_response = {
    "schema_version": "v1.0.0",
    "survey_id": test_survey_id,
    "period_id": test_period_id,
    "form_types": ["klk", "xyz", "tzr"],
    "data": "<encrypted data>",
}

# e2e dataset integration test - test data
unit_response_amended = {
    "schema_version": "v2.0.0",
    "survey_id": test_survey_id,
    "period_id": test_period_id,
    "form_types": ["abc", "fgg", "ynm"],
    "data": "<encrypted data>",
}

# e2e dataset integration test - test data for testing 404 response of dataset endpoints
dataset_metadata_404 = {
    "survey_id": "111",
    "period_id": "222",
    "dataset_id": "333",
    "identifier": "444",
}

# unused
incorrect_file_extension_message = {
    "error": "Filetype error",
    "message": "Invalid filetype received.",
}

# unused
invalid_json_message = {
    "error": "File content error",
    "message": "Invalid JSON content received.",
}

# unused
missing_keys_message = {
    "error": "Mandatory key(s) error",
    "message": "Mandatory key(s) missing from JSON.",
}

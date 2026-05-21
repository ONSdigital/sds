from app.models.collection_exericise_end_data import CollectionExerciseEndData
from app.models.dataset_models import DatasetMetadata, DatasetMetadataWithoutId, UnitDataset

from tests.test_data.shared_test_data import test_guid, test_survey_id, test_period_id, test_guid_2, test_guid_3

"""
Local variables:
"""
first_dataset_version = 1
updated_dataset_version = 2
test_published_at = "2023-04-20T12:00:00Z"

"""
Unit Test data:
"""
# unit test - dataset - test data
sub_collection_name = "units"

# unit test - dataset - test data
string_cat = "cat"
string_byte_size_cat = 5

# unit test - dataset - test data
empty_dict = {}
empty_dict_byte_size = 2

# unit tests - dataset - test data
identifier = "test_identifier"

# unit tests - dataset - test data
test_dataset_metadata_1 = DatasetMetadata(**{
        "survey_id": test_survey_id,
        "period_id": test_period_id,
        "form_types": ["123", "456", "789"],
        "title": "Which side was better?",
        "sds_published_at": test_published_at,
        "total_reporting_units": 1,
        "sds_dataset_version": 1,
        "filename": "test_filename_1.json",
        "dataset_id": test_guid,
    })

test_dataset_metadata_2 = DatasetMetadata(**{
        "survey_id": test_survey_id,
        "period_id": test_period_id,
        "form_types": ["123", "456", "789"],
        "title": "Which side was better?",
        "sds_published_at": test_published_at,
        "total_reporting_units": 1,
        "sds_dataset_version": 2,
        "filename": "test_filename_2.json",
        "dataset_id": test_guid_2,
    })

test_dataset_metadata_other = DatasetMetadata(**{
        "survey_id": "another_survey",
        "period_id": test_period_id,
        "form_types": ["123", "456", "789"],
        "title": "Which side was better?",
        "sds_published_at": test_published_at,
        "total_reporting_units": 1,
        "sds_dataset_version": 2,
        "filename": "test_filename_3.json",
        "dataset_id": test_guid_3,
    })

test_dataset_metadata: list[DatasetMetadata] = [
    test_dataset_metadata_2,
    test_dataset_metadata_1,
]

test_all_dataset_metadata: list[DatasetMetadata] = [
    test_dataset_metadata_other,
    test_dataset_metadata_2,
    test_dataset_metadata_1,
]


test_unit_data: UnitDataset = UnitDataset(**{
    "dataset_id": test_guid,
    "survey_id": test_survey_id,
    "period_id": test_period_id,
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
})

# For testing collection exercise end endpoint and dataset deletion service
test_data_collection_end: CollectionExerciseEndData = CollectionExerciseEndData(
    **{
        "dataset_guid": test_guid,
        "survey_id": test_survey_id,
        "period_id": test_period_id,
    }
)

# For testing collection exercise end endpoint and dataset deletion service
test_data_collection_end_missing_id: CollectionExerciseEndData = (
    CollectionExerciseEndData(
        **{
            "dataset_guid": "",
            "survey_id": test_survey_id,
            "period_id": test_period_id,
        }
    )
)


"""
Integration Test data:
"""

# e2e dataset integration test - test data
int_identifier = "43532"

# integration test tests - dataset - test data
dataset_unit_data_id: list[str] = ["43532", "65871"]

# integration test - dataset endpoints - test data
dataset_unit_data_collection_for_endpoints_test: list[UnitDataset] = [
    UnitDataset(**{
        "dataset_id": "",
        "survey_id": test_survey_id,
        "period_id": test_period_id,
        "form_types": ["jke", "als", "sma"],
        "data": "test",
    }),
    UnitDataset(**{
        "dataset_id": "",
        "survey_id": test_survey_id,
        "period_id": test_period_id,
        "form_types": ["skn", "qwd", "qkw"],
        "data": "test"
    }),
]

# integration test - dataset endpoints - test data
dataset_metadata_collection_for_endpoints_test: list[DatasetMetadata] = [
    DatasetMetadata(**{
        "dataset_id": "0",
        "survey_id": f"{test_survey_id}_1",
        "period_id": f"{test_period_id}_1",
        "form_types": ["sda", "ajk", "iwu"],
        "title": "Which side was better?",
        "sds_published_at": "2023-04-20T12:00:00Z",
        "total_reporting_units": 2,
        "sds_dataset_version": first_dataset_version,
        "filename": "test_filename.json",
    }),
    DatasetMetadata(**{
        "dataset_id": "1",
        "survey_id": f"{test_survey_id}_2",
        "period_id": f"{test_period_id}_2",
        "form_types": ["390", "219", "12O"],
        "title": None,
        "sds_published_at": "2023-04-20T12:00:00Z",
        "total_reporting_units": 2,
        "sds_dataset_version": updated_dataset_version,
        "filename": "test_filename.json",
    }),
]

# e2e dataset integration test - test data for testing 404 response of dataset endpoints
dataset_404_test_data = {
    "survey_id": "111",
    "period_id": "222",
    "dataset_id": "333",
    "identifier": "444",
}

# e2e dataset integration test - random string to test invalid query params
random_string = "random_string"

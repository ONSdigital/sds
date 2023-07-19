from models.dataset_models import DatasetMetadata, DatasetMetadataWithoutId, UnitDataset

from src.test_data import shared_test_data

cloud_event_data = {
    "id": "test_id",
    "type": "test_type",
    "bucket": "test_bucket",
    "metageneration": "1",
    "timeCreated": "test_time_created",
    "updated": "test_time_updated",
    "name": "test_filename.json",
}

cloud_event_invalid_filename_data = {
    "id": "test_id",
    "type": "test_type",
    "bucket": "test_bucket",
    "metageneration": "1",
    "timeCreated": "test_time_created",
    "updated": "test_time_updated",
    "name": "bad_filename.test",
}


unit_id = "test_unit_id"
survey_id = "test_survey_id"
period_id = "test_period_id"

first_dataset_version = 1
updated_dataset_version = 2


dataset_metadata_first_version: DatasetMetadata = {
    "dataset_id": shared_test_data.test_guid,
    "survey_id": survey_id,
    "period_id": period_id,
    "form_types": ["klk", "xyz", "tzr"],
    "title": "Which side was better?",
    "sds_published_at": "2023-04-20T12:00:00Z",
    "total_reporting_units": 1,
    "schema_version": "v1.0.0",
    "sds_dataset_version": first_dataset_version,
    "filename": "test_filename.json",
}

dataset_metadata_collection: list[DatasetMetadata] = [
    {
        "survey_id": f"{survey_id}_1",
        "period_id": period_id,
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
        "survey_id": f"{survey_id}_2",
        "period_id": period_id,
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

first_dataset_metadata_without_id: DatasetMetadataWithoutId = {
    "survey_id": survey_id,
    "period_id": period_id,
    "form_types": ["klk", "xyz", "tzr"],
    "title": "Which side was better?",
    "sds_published_at": "2023-04-20T12:00:00Z",
    "total_reporting_units": 2,
    "schema_version": "v1.0.0",
    "sds_dataset_version": first_dataset_version,
    "filename": "test_filename.json",
}

updated_dataset_metadata_without_id: DatasetMetadataWithoutId = {
    "survey_id": survey_id,
    "period_id": period_id,
    "form_types": ["klk", "xyz", "tzr"],
    "title": "Which side was better?",
    "sds_published_at": "2023-04-20T12:00:00Z",
    "total_reporting_units": 2,
    "schema_version": "v1.0.0",
    "sds_dataset_version": updated_dataset_version,
    "filename": "test_filename.json",
}

updated_dataset_metadata: DatasetMetadata = {
    **updated_dataset_metadata_without_id,
    "dataset_id": shared_test_data.test_guid,
}

unit_supplementary_data: UnitDataset = {
    "dataset_id": shared_test_data.test_guid,
    "survey_id": survey_id,
    "period_id": period_id,
    "schema_version": "v1.0.0",
    "form_types": ["klk", "xyz", "tzr"],
    "data": {
        "identifier": unit_id,
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

dataset_unit_data_collection: list[UnitDataset] = [
    {
        "dataset_id": shared_test_data.test_guid,
        "survey_id": survey_id,
        "period_id": period_id,
        "schema_version": "v1.0.0",
        "form_types": ["klk", "xyz", "tzr"],
        "data": "<encrypted data>",
    },
    {
        "dataset_id": shared_test_data.test_guid,
        "survey_id": survey_id,
        "period_id": period_id,
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

dataset_unit_data_identifier: list[str] = ["43532", "65871"]

missing_keys_dataset_metadata = {
    "period_id": period_id,
    "schema_version": 1,
    "form_types": [
        "abc",
        "def",
        "ghi",
    ],
    "data": [{"unit_data": "test_data", "identifier": "12345"}],
}

test_dataset_subscriber_id = "test_dataset_subscriber_id"
nonrandom_pubsub_dataset_metadata = {
    "survey_id": survey_id,
    "period_id": period_id,
    "form_types": ["klk", "xyz", "tzr"],
    "title": "Which side was better?",
    "total_reporting_units": 2,
    "schema_version": "v1.0.0",
    "sds_dataset_version": 1,
}

unit_response = {
    "schema_version": "v1.0.0",
    "survey_id": survey_id,
    "period_id": period_id,
    "form_types": ["klk", "xyz", "tzr"],
    "data": "<encrypted data>",
}

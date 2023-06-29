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
old_dataset_version = 1
new_dataset_version = 2


dataset_metadata: DatasetMetadata = {
    "dataset_id": shared_test_data.test_guid,
    "survey_id": survey_id,
    "period_id": "abc",
    "title": "Which side was better?",
    "sds_schema_version": 4,
    "sds_published_at": "2023-04-20T12:00:00Z",
    "total_reporting_units": 1,
    "schema_version": "v1.0.0",
    "sds_dataset_version": old_dataset_version,
    "filename": "test_filename.json",
}

dataset_metadata_collection: list[DatasetMetadata] = [
    {
        "survey_id": f"{survey_id}_1",
        "period_id": "abc",
        "title": "Which side was better?",
        "sds_schema_version": 4,
        "sds_published_at": "2023-04-20T12:00:00Z",
        "total_reporting_units": 1,
        "schema_version": "v1.0.0",
        "sds_dataset_version": old_dataset_version,
        "filename": "test_filename.json",
        "dataset_id": "0",
    },
    {
        "survey_id": f"{survey_id}_2",
        "period_id": "abc",
        "title": "Which side was better 2?",
        "sds_schema_version": 4,
        "sds_published_at": "2023-04-20T12:00:00Z",
        "total_reporting_units": 1,
        "schema_version": "v1.0.0",
        "sds_dataset_version": new_dataset_version,
        "filename": "test_filename.json",
        "dataset_id": "1",
    },
]

existing_dataset_unit_data_collection: list[UnitDataset] = [
    {
        "dataset_id": shared_test_data.test_guid,
        "survey_id": survey_id,
        "period_id": "abc",
        "sds_schema_version": 4,
        "schema_version": "v1.0.0",
        "data": {"test": "data", "ruref": "12345"},
    },
    {
        "dataset_id": shared_test_data.test_guid,
        "survey_id": survey_id,
        "period_id": "abc",
        "sds_schema_version": 4,
        "schema_version": "v1.0.0",
        "data": {"hello": "world", "ruref": "56789"},
    },
]


updated_dataset_metadata_without_id: DatasetMetadataWithoutId = {
    "survey_id": survey_id,
    "period_id": "abc",
    "title": "Which side was better?",
    "sds_schema_version": 4,
    "sds_published_at": "2023-04-20T12:00:00Z",
    "total_reporting_units": 2,
    "schema_version": "v1.0.0",
    "sds_dataset_version": new_dataset_version,
    "filename": "test_filename.json",
}

updated_dataset_metadata: DatasetMetadata = {
    **updated_dataset_metadata_without_id,
    "dataset_id": shared_test_data.test_guid,
}

unit_supplementary_data: UnitDataset = {
    "dataset_id": shared_test_data.test_guid,
    "survey_id": survey_id,
    "period_id": "abc",
    "sds_schema_version": 4,
    "schema_version": "v1.0.0",
    "data": {
        "ruref": unit_id,
        "runame": "Pipes and Maps Ltd",
        "ruaddr1": "111 Under Hill",
        "ruaddr2": "Hobbitton",
        "ruaddr4": "The Shire",
        "rupostcode": "HO1 1AA",
        "payeref": "123AB456",
        "busdesc": "Provision of equipment for hobbit adventures",
        "local_unit": [
            {
                "luref": "2012763A",
                "luname": "Maps Factory",
                "luaddr1": "1 Bag End",
                "luaddr2": "Underhill",
                "luaddr3": "Hobbiton",
                "lupostcode": "HO1 1AA",
                "tradstyle": "Also Does Adventures Ltd",
                "busdesc": "Creates old fashioned looking paper maps",
            },
            {
                "luref": "20127364B",
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
        "period_id": "abc",
        "sds_schema_version": 4,
        "schema_version": "v1.0.0",
        "data": "<encrypted data>",
    },
    {
        "dataset_id": shared_test_data.test_guid,
        "survey_id": survey_id,
        "period_id": "abc",
        "sds_schema_version": 4,
        "schema_version": "v1.0.0",
        "data": {
            "ruref": "65871",
            "runame": "Boats and Floats Ltd",
            "ruaddr1": "111 Upper Hill",
            "ruaddr2": "Mordor",
            "rupostcode": "HO10 1AA",
            "payeref": "8888",
            "busdesc": "Provision of equipment for the bad guys.",
            "local_unit": [
                {
                    "luref": "2012763A",
                    "luname": "Arms Factory",
                    "luaddr1": "1 Bag End",
                    "luaddr2": "Underhill",
                    "luaddr3": "Hobbiton",
                    "lupostcode": "HO1 1AA",
                    "tradstyle": "Also Does Adventures Ltd",
                    "busdesc": "Creates old fashioned looking paper maps",
                },
                {
                    "luref": "20127364B",
                    "luname": "Swords Subsidiary",
                    "luaddr1": "12 The Farmstead",
                    "luaddr2": "Maggotsville",
                    "luaddr3": "Hobbiton",
                    "lupostcode": "HO1 1AB",
                    "busdesc": "Quality pipe manufacturer",
                    "buslref": "pipe123",
                },
                {
                    "luref": "20127365C",
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

dataset_unit_data_ruref: list[str] = ["43532", "65871"]

missing_keys_dataset_metadata = {
    "period_id": "test_period_id",
    "sds_schema_version": "test_sds_schema_version",
    "schema_version": 1,
    "data": [{"unit_data": "test_data", "ruref": "12345"}],
}

test_dataset_subscriber_id = "test_dataset_subscriber_id"
nonrandom_pubsub_dataset_metadata = {
    "survey_id": "test_survey_id",
    "period_id": "abc",
    "title": "Which side was better?",
    "sds_schema_version": 4,
    "total_reporting_units": 2,
    "schema_version": "v1.0.0",
    "sds_dataset_version": 1,
}

cloud_event_test_data = {
    "id": "test_id",
    "type": "test_type",
    "bucket": "test_bucket",
    "metageneration": "1",
    "timeCreated": "test_time_created",
    "updated": "test_time_updated",
    "name": "test_filename.json",
}

test_dataset_id = "test_dataset_id"
test_survey_id = "xyz"


dataset_metadata = {
    "dataset_id": test_dataset_id,
    "survey_id": test_survey_id,
    "period_id": "abc",
    "title": "Which side was better?",
    "sds_schema_version": 4,
    "sds_published_at": "2023-04-20T12:00:00Z",
    "total_reporting_units": 1,
    "schema_version": "v1.0.0",
    "sds_dataset_version": 1,
    "filename": "test_filename.json",
}

existing_dataset_unit_data_collection = [
    {
        "dataset_id": test_dataset_id,
        "survey_id": test_survey_id,
        "period_id": "abc",
        "sds_schema_version": 4,
        "schema_version": "v1.0.0",
        "data": {"test": "data", "ruref": "12345"},
    },
    {
        "dataset_id": "test_dataset_id",
        "survey_id": "xyz",
        "period_id": "abc",
        "sds_schema_version": 4,
        "schema_version": "v1.0.0",
        "data": {"hello": "world", "ruref": "56789"},
    },
]

dataset_metadata_without_id = {
    "survey_id": "xyz",
    "period_id": "abc",
    "title": "Which side was better?",
    "sds_schema_version": 4,
    "sds_published_at": "2023-04-20T12:00:00Z",
    "total_reporting_units": 2,
    "schema_version": "v1.0.0",
    "sds_dataset_version": 2,
    "filename": "test_filename.json",
}

new_dataset_unit_data_collection = [
    {
        "dataset_id": "test_dataset_id",
        "survey_id": "xyz",
        "period_id": "abc",
        "sds_schema_version": 4,
        "schema_version": "v1.0.0",
        "data": {
            "ruref": "43532",
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
    },
    {
        "dataset_id": "test_dataset_id",
        "survey_id": "xyz",
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

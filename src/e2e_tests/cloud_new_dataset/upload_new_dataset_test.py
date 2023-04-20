import uuid
from datetime import datetime
from unittest.mock import MagicMock, call

from repositories.dataset_repository import DatasetRepository
from services.datetime_service import DatetimeService

cloud_event_test_data = {
    "id": "test_id",
    "type": "test_type",
    "bucket": "test_bucket",
    "metageneration": "1",
    "timeCreated": "test_time_created",
    "updated": "test_time_updated",
    "name": "test_filename.json",
}


def test_upload_new_dataset(new_dataset):
    """
    There should be a log for when the cloud function is triggered and when the
    new dataset is successfully uploaded.
    """
    cloud_event = MagicMock()
    cloud_event.data = cloud_event_test_data

    DatasetRepository.get_dataset_with_survey_id = MagicMock()
    DatasetRepository.get_dataset_with_survey_id.return_value = [
        {
            "dataset_id": "test_dataset_id",
            "survey_id": "xyz",
            "period_id": "abc",
            "title": "Which side was better?",
            "sds_schema_version": 4,
            "sds_published_at": "2023-04-20T12:00:00Z",
            "total_reporting_units": 1,
            "schema_version": "v1.0.0",
            "sds_dataset_version": 1,
            "filename": "test_filename.json",
            "form_type": "yyy",
        }
    ]

    DatasetRepository.create_new_dataset = MagicMock()
    DatasetRepository.create_new_dataset.return_value = None

    uuid.uuid4 = MagicMock()
    uuid.uuid4.return_value = "test_dataset_id"

    test_date = datetime(2023, 4, 20, 12, 0, 0)
    DatetimeService.get_current_date_and_time = MagicMock()
    DatetimeService.get_current_date_and_time.return_value = test_date

    DatasetRepository.get_dataset_unit_collection = MagicMock()
    DatasetRepository.get_dataset_unit_collection.return_value = [
        {
            "dataset_id": "test_dataset_id",
            "survey_id": "xyz",
            "period_id": "abc",
            "sds_schema_version": 4,
            "schema_version": "v1.0.0",
            "form_type": "yyy",
            "data": {"test": "data", "ruref": "12345"},
        },
        {
            "dataset_id": "test_dataset_id",
            "survey_id": "xyz",
            "period_id": "abc",
            "sds_schema_version": 4,
            "schema_version": "v1.0.0",
            "form_type": "yyy",
            "data": {"hello": "world", "ruref": "56789"},
        },
    ]

    DatasetRepository.append_unit_to_dataset_units_collection = MagicMock()
    DatasetRepository.append_unit_to_dataset_units_collection.return_value = None

    new_dataset(cloud_event=cloud_event)

    DatasetRepository.get_dataset_with_survey_id.assert_called_once_with("xyz")
    DatasetRepository.create_new_dataset.assert_called_once_with(
        "test_dataset_id",
        {
            "survey_id": "xyz",
            "period_id": "abc",
            "title": "Which side was better?",
            "sds_schema_version": 4,
            "sds_published_at": "2023-04-20T12:00:00Z",
            "total_reporting_units": 2,
            "schema_version": "v1.0.0",
            "sds_dataset_version": 2,
            "filename": "test_filename.json",
            "form_type": "yyy",
        },
    )

    DatasetRepository.get_dataset_unit_collection.assert_called_once_with(
        "test_dataset_id"
    )

    append_calls = [
        call(
            [
                {
                    "dataset_id": "test_dataset_id",
                    "survey_id": "xyz",
                    "period_id": "abc",
                    "sds_schema_version": 4,
                    "schema_version": "v1.0.0",
                    "form_type": "yyy",
                    "data": {"test": "data", "ruref": "12345"},
                },
                {
                    "dataset_id": "test_dataset_id",
                    "survey_id": "xyz",
                    "period_id": "abc",
                    "sds_schema_version": 4,
                    "schema_version": "v1.0.0",
                    "form_type": "yyy",
                    "data": {"hello": "world", "ruref": "56789"},
                },
            ],
            {
                "dataset_id": "test_dataset_id",
                "survey_id": "xyz",
                "period_id": "abc",
                "sds_schema_version": 4,
                "schema_version": "v1.0.0",
                "form_type": "yyy",
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
        ),
        call(
            [
                {
                    "dataset_id": "test_dataset_id",
                    "survey_id": "xyz",
                    "period_id": "abc",
                    "sds_schema_version": 4,
                    "schema_version": "v1.0.0",
                    "form_type": "yyy",
                    "data": {"test": "data", "ruref": "12345"},
                },
                {
                    "dataset_id": "test_dataset_id",
                    "survey_id": "xyz",
                    "period_id": "abc",
                    "sds_schema_version": 4,
                    "schema_version": "v1.0.0",
                    "form_type": "yyy",
                    "data": {"hello": "world", "ruref": "56789"},
                },
            ],
            {
                "dataset_id": "test_dataset_id",
                "survey_id": "xyz",
                "period_id": "abc",
                "sds_schema_version": 4,
                "schema_version": "v1.0.0",
                "form_type": "yyy",
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
        ),
    ]
    DatasetRepository.append_unit_to_dataset_units_collection.assert_has_calls(
        append_calls
    )

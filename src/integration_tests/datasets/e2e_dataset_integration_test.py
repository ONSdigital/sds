from unittest import TestCase

from config.config_factory import config
from google.cloud import storage

from src.integration_tests.helpers.integration_helpers import (
    cleanup,
    create_dataset,
    create_filepath,
    generate_headers,
    load_json,
    pubsub_setup,
    pubsub_teardown,
    setup_session,
)
from src.integration_tests.helpers.pubsub_helper import dataset_pubsub_helper
from src.test_data import dataset_test_data
from src.test_data.shared_test_data import test_dataset_subscriber_id, unit_id


class E2EDatasetIntegrationTest(TestCase):
    def setUp(self) -> None:
        cleanup()
        pubsub_setup(dataset_pubsub_helper, test_dataset_subscriber_id)

    def tearDown(self) -> None:
        cleanup()
        pubsub_teardown(dataset_pubsub_helper, test_dataset_subscriber_id)

    def test_dataset_e2e(self):
        """
        Test that we can upload a dataset and then retrieve the data. This checks the cloud function worked.

        * We load the sample dataset json file
        * Upload the dataset file to the dataset bucket with the dataset_id as the name
        * We then check the uploaded file has been deleted from the bucket
        * We then use the API to get some unit data back using the dataset_id and a known ru_ref
        * The dataset id an auto generated GUID
        """
        session = setup_session()
        headers = generate_headers()

        dataset = load_json(f"{config.TEST_DATASET_PATH}dataset.json")

        filename = create_filepath("integration-test")

        create_dataset_response = create_dataset(filename, dataset, session, headers)

        if create_dataset_response is not None and create_dataset_response != 200:
            assert False, "Unsuccessful request to create dataset"

        assert (
            not storage.Client()
            .bucket(config.DATASET_BUCKET_NAME)
            .blob(filename)
            .exists()
        )

        dataset_metadata_response = session.get(
            f"{config.API_URL}/v1/dataset_metadata?"
            f"survey_id={dataset['survey_id']}&period_id={dataset['period_id']}",
            headers=headers,
        )
        assert dataset_metadata_response.status_code == 200

        for dataset_metadata in dataset_metadata_response.json():
            if dataset_metadata["filename"] == filename:
                dataset_id = dataset_metadata["dataset_id"]
                response = session.get(
                    f"{config.API_URL}/v1/unit_data?dataset_id={dataset_id}&unit_id={unit_id}",
                    headers=headers,
                )

                assert response.status_code == 200

                json_response = response.json()
                assert json_response["dataset_id"] is not None

                json_response.pop("dataset_id")
                assert dataset_test_data.unit_response.items() == json_response.items()

                assert "sds_dataset_version" in dataset_metadata
                assert "filename" in dataset_metadata
                assert "form_types" in dataset_metadata

        received_messages = dataset_pubsub_helper.pull_and_acknowledge_messages(
            test_dataset_subscriber_id
        )

        for key, value in dataset_test_data.nonrandom_pubsub_dataset_metadata.items():
            assert received_messages[0][key] == value

    def test_different_period_and_survey_id(self):
        """
        Test that if we upload datasets that have the same survey_id or period_id but not both then distinct entries will
        be created in firestore.

        * We load the sample dataset json files, kicking off the dataset e2e upload to firestore
        * Use the API to get some metadata back using the survey and period ids
        * Check the datasets are distinct and no versions are incremented
        """
        session = setup_session()
        headers = generate_headers()

        dataset = load_json(f"{config.TEST_DATASET_PATH}dataset.json")
        dataset_different_survey_id = load_json(
            f"{config.TEST_DATASET_PATH}dataset_different_survey_id.json"
        )
        dataset_different_period_id = load_json(
            f"{config.TEST_DATASET_PATH}dataset_different_period_id.json"
        )

        filename = create_filepath("integration-test")
        filename_different_survey_id = create_filepath(
            "integration-test-different-survey-id"
        )
        filename_different_period_id = create_filepath(
            "integration-test-different-period-id"
        )

        create_dataset(filename, dataset, session, headers)
        create_dataset(
            filename_different_survey_id, dataset_different_survey_id, session, headers
        )
        create_dataset(
            filename_different_period_id, dataset_different_period_id, session, headers
        )

        get_dataset_metadata = lambda survey_id, period_id: (  # noqa: E731
            session.get(
                f"{config.API_URL}/v1/dataset_metadata?"
                f"survey_id={survey_id}&period_id={period_id}",
                headers=headers,
            )
        )

        dataset_metadata_response = get_dataset_metadata(
            dataset["survey_id"], dataset["period_id"]
        )
        dataset_metadata_different_survey_id_response = get_dataset_metadata(
            dataset_different_survey_id["survey_id"],
            dataset_different_survey_id["period_id"],
        )
        dataset_metadata_different_period_id_response = get_dataset_metadata(
            dataset_different_period_id["survey_id"],
            dataset_different_period_id["period_id"],
        )

        assert dataset_metadata_response.status_code == 200
        assert dataset_metadata_different_survey_id_response.status_code == 200
        assert dataset_metadata_different_period_id_response.status_code == 200

        assert len(dataset_metadata_response.json()) == 1
        assert len(dataset_metadata_different_survey_id_response.json()) == 1
        assert len(dataset_metadata_different_period_id_response.json()) == 1

        dataset_json = dataset_metadata_response.json()[0]
        dataset_different_survey_id_json = (
            dataset_metadata_different_survey_id_response.json()[0]
        )
        dataset_different_period_id_json = (
            dataset_metadata_different_period_id_response.json()[0]
        )

        assert dataset_json["sds_dataset_version"] == 1
        assert dataset_different_survey_id_json["sds_dataset_version"] == 1
        assert dataset_different_period_id_json["sds_dataset_version"] == 1

        assert dataset_json["survey_id"] == "test_survey_id"
        assert dataset_json["period_id"] == "test_period_id"

        assert (
            dataset_different_survey_id_json["survey_id"] == "test_different_survey_id"
        )
        assert dataset_different_survey_id_json["period_id"] == "test_period_id"

        assert dataset_different_period_id_json["survey_id"] == "test_survey_id"
        assert (
            dataset_different_period_id_json["period_id"] == "test_different_period_id"
        )

    def test_dataset_without_title(self):
        """
        Test that we can upload a dataset without a title and then retrieve the metadata with title = None.
        This checks the dataset metadata endpoint work even without title to handle the bug (Bug Card SDSS-179)

        * We load the dataset json file that is without title
        * Use the API to get the metadata back using the survey and period id
        * Check the process is successful and title = None
        * Use the API to get unit data and check the process is successful
        """
        session = setup_session()
        headers = generate_headers()

        dataset_without_title = load_json(f"{config.TEST_DATASET_PATH}dataset_without_title.json")

        dataset_without_title_filename = create_filepath("integration-test-file-without-title")

        create_dataset_response = create_dataset(
            dataset_without_title_filename, dataset_without_title, session, headers
        )
        
        # Check against dataset_metadata endpoint
        dataset_metadata_response = session.get(
            f"{config.API_URL}/v1/dataset_metadata?"
            f"survey_id={dataset_without_title['survey_id']}&period_id={dataset_without_title['period_id']}",
            headers=headers,
        )
        assert dataset_metadata_response.status_code == 200

        for dataset_metadata in dataset_metadata_response.json():
            assert dataset_metadata == {
                "dataset_id": dataset_metadata["dataset_id"],
                "filename": dataset_without_title_filename,
                "sds_dataset_version": 1,
                "schema_version": dataset_without_title["schema_version"],
                "total_reporting_units": len(dataset_without_title["data"]),
                "sds_published_at": dataset_metadata["sds_published_at"],
                "title": None,
                "form_types": dataset_without_title["form_types"],
                "period_id": dataset_without_title["period_id"],
                "survey_id": dataset_without_title["survey_id"],
            }

            # Check against unit_data endpoint
            dataset_id = dataset_metadata["dataset_id"]
            unit_data_response = session.get(
                f"{config.API_URL}/v1/unit_data?dataset_id={dataset_id}&unit_id={unit_id}",
                headers=headers,
            )
            assert unit_data_response.status_code == 200
            json_response = unit_data_response.json()
            assert json_response["dataset_id"] is not None

            json_response.pop("dataset_id")
            assert dataset_test_data.unit_response.items() == json_response.items()
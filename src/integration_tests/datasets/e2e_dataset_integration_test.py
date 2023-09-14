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
        Test that we can upload 2 datasets of same survey id and period and then retrieve the data.
        This checks the cloud function worked and the datasets are retained according to the retain flag.

        * We load the first sample dataset json file
        * Upload the dataset file to the dataset bucket with the dataset_id as the name
        * We then check the uploaded file has been deleted from the bucket
        * We repeat the steps for the second dataset
        * We check the count and respective dataset version using dataset_metadata endpoint
        * We check the dataset metadata accuracy
        * We then use the unit_data endpoint to get some unit data back using the dataset_id and a known unit identifier
        * We check the unit data response
        * We check the pubsub messages
        """
        session = setup_session()
        headers = generate_headers()

        # First dataset
        first_dataset = load_json(f"{config.TEST_DATASET_PATH}dataset.json")

        first_dataset_filename = create_filepath("integration-test-first-file")

        create_dataset_response_for_first_dataset = create_dataset(
            first_dataset_filename, first_dataset, session, headers
        )

        if (
            create_dataset_response_for_first_dataset is not None
            and create_dataset_response_for_first_dataset != 200
        ):
            assert False, "Unsuccessful request to create dataset"

        if config.AUTODELETE_DATASET_BUCKET_FILE is True:
            assert (
                not storage.Client()
                .bucket(config.DATASET_BUCKET_NAME)
                .blob(first_dataset_filename)
                .exists()
            )

        # Second dataset
        second_dataset = load_json(f"{config.TEST_DATASET_PATH}dataset_amended.json")

        second_dataset_filename = create_filepath("integration-test-second-file")

        create_dataset_response_for_second_dataset = create_dataset(
            second_dataset_filename, second_dataset, session, headers
        )

        if (
            create_dataset_response_for_second_dataset is not None
            and create_dataset_response_for_second_dataset != 200
        ):
            assert False, "Unsuccessful request to create dataset"

        # This config is within the integration test environment and has to match with
        # the actual running environment to pass the test
        if config.AUTODELETE_DATASET_BUCKET_FILE is True:
            assert (
                not storage.Client()
                .bucket(config.DATASET_BUCKET_NAME)
                .blob(second_dataset_filename)
                .exists()
            )

        # Check against dataset_metadata endpoint
        dataset_metadata_response = session.get(
            f"{config.API_URL}/v1/dataset_metadata?"
            f"survey_id={first_dataset['survey_id']}&period_id={first_dataset['period_id']}",
            headers=headers,
        )
        assert dataset_metadata_response.status_code == 200

        # This config is within the integration test environment and has to match with
        # the actual running environment to pass the test
        if config.RETAIN_DATASET_FIRESTORE is True:
            assert len(dataset_metadata_response.json()) == 2
        else:
            assert len(dataset_metadata_response.json()) == 1

        # Dataset metadata is in descending order of sds_dataset_version
        # 0 => second dataset
        # 1 => first dataset (if retain flag is on)
        for count, dataset_metadata in enumerate(dataset_metadata_response.json()):
            if count == 0:
                dataset_metadata_second_dataset = {
                    "dataset_id": dataset_metadata["dataset_id"],
                    "filename": second_dataset_filename,
                    "sds_dataset_version": 2,
                    "schema_version": second_dataset["schema_version"],
                    "total_reporting_units": len(second_dataset["data"]),
                    "sds_published_at": dataset_metadata["sds_published_at"],
                    "title": second_dataset["title"],
                    "form_types": second_dataset["form_types"],
                    "period_id": second_dataset["period_id"],
                    "survey_id": second_dataset["survey_id"],
                }
                assert dataset_metadata == dataset_metadata_second_dataset

                # Check against unit_data endpoint for second dataset
                dataset_id = dataset_metadata["dataset_id"]
                response = session.get(
                    f"{config.API_URL}/v1/unit_data?dataset_id={dataset_id}&unit_id={unit_id}",
                    headers=headers,
                )

                assert response.status_code == 200

                json_response = response.json()
                assert json_response["dataset_id"] is not None

                json_response.pop("dataset_id")
                assert (
                    dataset_test_data.unit_response_amended.items()
                    == json_response.items()
                )

            if count == 1:
                dataset_metadata_first_dataset = {
                    "dataset_id": dataset_metadata["dataset_id"],
                    "filename": first_dataset_filename,
                    "sds_dataset_version": 1,
                    "schema_version": first_dataset["schema_version"],
                    "total_reporting_units": len(first_dataset["data"]),
                    "sds_published_at": dataset_metadata["sds_published_at"],
                    "title": first_dataset["title"],
                    "form_types": first_dataset["form_types"],
                    "period_id": first_dataset["period_id"],
                    "survey_id": first_dataset["survey_id"],
                }
                assert dataset_metadata == dataset_metadata_first_dataset

                # Check against unit_data endpoint for first dataset
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

        # Check pubsub messages
        received_messages = dataset_pubsub_helper.pull_and_acknowledge_messages(
            test_dataset_subscriber_id
        )

        for (
            key,
            value,
        ) in dataset_test_data.nonrandom_pubsub_first_dataset_metadata.items():
            assert received_messages[0][key] == value

        for (
            key,
            value,
        ) in dataset_test_data.nonrandom_pubsub_second_dataset_metadata.items():
            assert received_messages[1][key] == value

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

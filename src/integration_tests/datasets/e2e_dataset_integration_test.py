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
    create_dataset_as_string,
    pubsub_purge_messages,
    inject_wait_time,
)
from src.integration_tests.helpers.pubsub_helper import (
    dataset_error_pubsub_helper,
    dataset_pubsub_helper,
)
from src.test_data import dataset_test_data
from src.test_data.shared_test_data import (
    test_dataset_error_subscriber_id,
    test_dataset_subscriber_id,
)


class E2EDatasetIntegrationTest(TestCase):
    @classmethod
    def setup_class(self) -> None:
        cleanup()
        pubsub_setup(dataset_pubsub_helper, test_dataset_subscriber_id)
        pubsub_setup(dataset_error_pubsub_helper, test_dataset_error_subscriber_id)
        inject_wait_time(3) # Inject wait time to allow resources properly set up

    @classmethod
    def teardown_class(self) -> None:
        cleanup()
        pubsub_teardown(dataset_pubsub_helper, test_dataset_subscriber_id)
        pubsub_teardown(dataset_error_pubsub_helper, test_dataset_error_subscriber_id)

    def tearDown(self) -> None:
        cleanup()
        inject_wait_time(3) # Inject wait time to allow all message to be processed
        pubsub_purge_messages(dataset_pubsub_helper, test_dataset_subscriber_id)
        pubsub_purge_messages(dataset_error_pubsub_helper, test_dataset_error_subscriber_id)

    def test_dataset_e2e(self):
        """
        Test that we can upload 2 datasets of same survey id and period and then retrieve the data.
        This checks the cloud function worked and the datasets are retained according to the retain flag.

        * We load the first sample dataset json file
        * Upload the dataset file to the dataset bucket with the dataset_id as the name
        * We then check the uploaded file has been deleted from the bucket
        * We check and ack the pubsub message for first dataset
        * We repeat the steps for the second dataset
        * We check the count and respective dataset version using dataset_metadata endpoint
        * We check the dataset metadata accuracy
        * We then use the unit_data endpoint to get some unit data back using the dataset_id and a known unit identifier
        * We check the unit data response
        """
        session = setup_session()
        headers = generate_headers()

        # Upload first dataset
        first_dataset = load_json(f"{config.TEST_DATASET_PATH}dataset.json")

        first_dataset_filename = create_filepath("integration-test-first-file")

        create_dataset(first_dataset_filename, first_dataset, session, headers)

        # Check file is removed from bucket
        # This config is within the integration test environment and has to match with
        # the actual running environment to pass the test
        if config.AUTODELETE_DATASET_BUCKET_FILE is True:
            assert (
                not storage.Client()
                .bucket(config.DATASET_BUCKET_NAME)
                .blob(first_dataset_filename)
                .exists()
            )

        # Check pubsub messages and ack
        received_messages = dataset_pubsub_helper.pull_and_acknowledge_messages(
            test_dataset_subscriber_id
        )

        for (
            key,
            value,
        ) in dataset_test_data.nonrandom_pubsub_first_dataset_metadata.items():
            assert received_messages[0][key] == value

        # Upload second dataset
        second_dataset = load_json(f"{config.TEST_DATASET_PATH}dataset_amended.json")

        second_dataset_filename = create_filepath("integration-test-second-file")

        create_dataset(second_dataset_filename, second_dataset, session, headers)

        # Check file is removed from bucket
        # This config is within the integration test environment and has to match with
        # the actual running environment to pass the test
        if config.AUTODELETE_DATASET_BUCKET_FILE is True:
            assert (
                not storage.Client()
                .bucket(config.DATASET_BUCKET_NAME)
                .blob(first_dataset_filename)
                .exists()
            )

        # Check pubsub messages and ack
        received_messages = dataset_pubsub_helper.pull_and_acknowledge_messages(
            test_dataset_subscriber_id
        )

        for (
            key,
            value,
        ) in dataset_test_data.nonrandom_pubsub_second_dataset_metadata.items():
            assert received_messages[0][key] == value

        # Check result from endpoints

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
                    f"{config.API_URL}/v1/unit_data?dataset_id={dataset_id}&identifier={dataset_test_data.int_identifier}",
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
                    f"{config.API_URL}/v1/unit_data?dataset_id={dataset_id}&identifier={dataset_test_data.int_identifier}",
                    headers=headers,
                )

                assert response.status_code == 200

                json_response = response.json()
                assert json_response["dataset_id"] is not None

                json_response.pop("dataset_id")
                assert dataset_test_data.unit_response.items() == json_response.items()

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

        # Define a function to get dataset metadata using survey and period IDs
        get_dataset_metadata = lambda survey_id, period_id: (  # noqa: E731
            session.get(
                f"{config.API_URL}/v1/dataset_metadata?"
                f"survey_id={survey_id}&period_id={period_id}",
                headers=headers,
            )
        )

        # Retrieve dataset metadata for different combinations of IDs
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

        # Verify that each response contains a single dataset entry
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

        # Verify that the dataset versions are not incremented
        assert dataset_json["sds_dataset_version"] == 1
        assert dataset_different_survey_id_json["sds_dataset_version"] == 1
        assert dataset_different_period_id_json["sds_dataset_version"] == 1

        assert dataset_json["survey_id"] == "test_survey_id"
        assert dataset_json["period_id"] == "test_period_id"

        assert (
            dataset_different_survey_id_json["survey_id"] == dataset_different_survey_id["survey_id"]
        )
        assert dataset_different_survey_id_json["period_id"] == dataset_different_survey_id["period_id"]

        assert dataset_different_period_id_json["survey_id"] == dataset_different_period_id["survey_id"]
        assert (
            dataset_different_period_id_json["period_id"] == dataset_different_period_id["period_id"]
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

        dataset_without_title = load_json(
            f"{config.TEST_DATASET_PATH}dataset_without_title.json"
        )

        dataset_without_title_filename = create_filepath(
            "integration-test-file-without-title"
        )

        create_dataset(
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
                f"{config.API_URL}/v1/unit_data?dataset_id={dataset_id}&identifier={dataset_test_data.int_identifier}",
                headers=headers,
            )
            assert unit_data_response.status_code == 200
            json_response = unit_data_response.json()
            assert json_response["dataset_id"] is not None

            json_response.pop("dataset_id")
            assert dataset_test_data.unit_response.items() == json_response.items()

    def test_dataset_error_invalid_extension(self):
        """
        Test that when we upload three datasets with errors, the correct error is published to the error topic.
        This checks the cloud function works when there are errors in the dataset.
        There are errors on 3 instances:
        - When the dataset file extension is not json
        - When the dataset file is not valid json
        - When the dataset file is missing required keys
        * We load the sample dataset json files with errors
        * Upload the dataset files to the dataset bucket
        * Check the files are not removed from the bucket
        * Check the error messages are published to the error topic
        """
        session = setup_session()
        headers = generate_headers()
        # Upload dataset with invalid filename
        dataset_incorrect_extension = load_json(
            f"{config.TEST_DATASET_PATH}dataset.json"
        )
        dataset_incorrect_extension_filename = create_filepath(
            "integration-test-incorrect-extension"
        ).replace(".json", ".txt")

        create_dataset_response = create_dataset(
            dataset_incorrect_extension_filename,
            dataset_incorrect_extension,
            session,
            headers,
            skip_wait=True,
        )
        if create_dataset_response is not None and create_dataset_response != 200:
            assert False, "Unsuccessful request to create dataset"
        # Check pubsub messages and ack
        received_messages = dataset_error_pubsub_helper.pull_and_acknowledge_messages(
            test_dataset_error_subscriber_id
        )
        for (
            key,
            value,
        ) in dataset_test_data.incorrect_file_extension_message.items():
            assert received_messages[0][key] == value

        # Upload dataset with invalid json
        with open(f"{config.TEST_DATASET_PATH}dataset_invalid_json.json", "r") as file:
            dataset_invalid_json = file.read()
            file.close()

        dataset_invalid_json_filename = create_filepath("integration-test-invalid-json")
        create_dataset_response = create_dataset_as_string(
            dataset_invalid_json_filename, dataset_invalid_json, session, headers
        )
        if create_dataset_response is not None and create_dataset_response != 200:
            assert False, "Unsuccessful request to create dataset"
        # Check pubsub messages and ack
        received_messages = dataset_error_pubsub_helper.pull_and_acknowledge_messages(
            test_dataset_error_subscriber_id
        )
        for (
            key,
            value,
        ) in dataset_test_data.invalid_json_message.items():
            assert received_messages[0][key] == value

        # Upload dataset with missing keys
        dataset_missing_keys = load_json(
            f"{config.TEST_DATASET_PATH}dataset_missing_keys.json"
        )
        dataset_missing_keys_filename = create_filepath("integration-test-missing-keys")
        create_dataset_response = create_dataset(
            dataset_missing_keys_filename,
            dataset_missing_keys,
            session,
            headers,
            skip_wait=True,
        )
        if create_dataset_response is not None and create_dataset_response != 200:
            assert False, "Unsuccessful request to create dataset"
        # Check pubsub messages and ack
        received_messages = dataset_error_pubsub_helper.pull_and_acknowledge_messages(
            test_dataset_error_subscriber_id
        )
        for (
            key,
            value,
        ) in dataset_test_data.missing_keys_message.items():
            assert received_messages[0][key] == value

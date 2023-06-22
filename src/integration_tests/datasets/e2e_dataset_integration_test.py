from datetime import datetime
from unittest import TestCase

from config.config_factory import config

from src.integration_tests.helpers.integration_helpers import (
    cleanup,
    create_dataset,
    generate_headers,
    get_bucket,
    load_json,
    setup_session,
)
from src.test_data.shared_test_data import unit_id, unit_response


class E2ESchemaIntegrationTest(TestCase):
    def setUp(self) -> None:
        cleanup()

    def tearDown(self) -> None:
        cleanup()

    def test_dataset_e2e(self):
        """
        Test that we can upload a dataset and then retrieve the data. This checks the cloud function worked.

        * We load the sample dataset json file
        * Upload the dataset file to the dataset bucket with the dataset_id as the name
        * We then check the uploaded file has been deleted from the bucket
        * We then use the API to get some unit data back using the dataset_id and a known ru_re
        * The dataset id an auto generated GUID
        """
        session = setup_session()
        headers = generate_headers()

        dataset = load_json(config.TEST_DATASET_PATH)

        filename = f"integration-test-{str(datetime.now()).replace(' ','-')}.json"

        create_dataset_response = create_dataset(filename, dataset, session, headers)

        if create_dataset_response is not None and create_dataset_response != 200:
            assert False, "Unsuccessful request to create dataset"

        assert not get_bucket(config.DATASET_BUCKET_NAME).blob(filename).exists()

        dataset_metadata_response = session.get(
            f"{config.API_URL}/v1/dataset_metadata?survey_id={dataset['survey_id']}&period_id={dataset['period_id']}",
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
                assert unit_response.items() == json_response.items()

                assert "sds_dataset_version" in dataset_metadata
                assert "filename" in dataset_metadata

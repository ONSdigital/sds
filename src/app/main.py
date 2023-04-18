import uuid

import database
import dataset_storage
import functions_framework
from logging_config import logging

logger = logging.getLogger(__name__)


@functions_framework.cloud_event
def new_dataset(cloud_event):
    """
    Triggered by uploading a new dataset file to the
    dataset storage bucket. See the 'Cloud Functions' section
    in the README.md file for details as to how this function
    is set up.
    * The dataset_id is an auto generated GUID and the filename is saved as a new field in the metadata.
    """
    logger.info("Uploading new dataset...")
    logger.debug(f"Cloud event data: {cloud_event.data}")

    bucket_name = cloud_event.data["bucket"]
    filename = cloud_event.data["name"]

    """
    Check if the filename ends with '.json'.
    Process the contents if it is a valid '.json' file or else log the error.
    """
    if filename[-5:].lower() == ".json":
        dataset = dataset_storage.get_dataset(
            filename=filename, bucket_name=bucket_name
        )

        if dataset is not None:
            isValid, missing_keys = validate_keys_dataset(dataset)
            if isValid is True:
                logger.info("Dataset obtained successfully.")
                logger.debug(f"Dataset: {dataset}")
                dataset_id = str(uuid.uuid4())
                database.set_dataset(
                    dataset_id=dataset_id, filename=filename, dataset=dataset
                )
                logger.info("Dataset uploaded successfully.")
            else:
                message = ""
                for key in missing_keys:
                    message = message + key + ", "
                logger.error(f"The keys {message} are missing in the JSON object")
        else:
            logger.error("Invalid JSON file contents")
    else:
        logger.error(f"Invalid filetype received - {filename}")


def validate_keys_dataset(dataset):
    isValid = True
    missing_keys = []
    if "survey_id" not in dataset:
        missing_keys.append("survey_id")
    if "period_id" not in dataset:
        missing_keys.append("period_id")
    if "sds_schema_ version" not in dataset:
        missing_keys.append("sds_schema_ version")
    if "schema_version" not in dataset:
        missing_keys.append("schema_version")
    if "form_type" not in dataset:
        missing_keys.append("schema_version")

    if len(missing_keys) > 0:
        isValid = False

    return isValid, missing_keys

import functions_framework
from logging_config import logging
from services.dataset.dataset_bucket_service import DatasetBucketService
from services.dataset.dataset_processor_service import DatasetProcessorService
from services.validators.dataset_validator_service import DatasetValidatorService

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

    filename = cloud_event.data["name"]

    DatasetValidatorService.validate_file_is_json(filename)

    raw_dataset = DatasetBucketService().get_and_validate_dataset(filename)

    logger.info("Dataset obtained from bucket successfully.")
    logger.debug(f"Dataset: {raw_dataset}")

    DatasetProcessorService().process_raw_dataset(filename, raw_dataset)

    logger.info("Dataset uploaded successfully.")

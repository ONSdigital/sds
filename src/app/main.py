import functions_framework
from config.config_factory import ConfigFactory
from logging_config import logging
from services.dataset.dataset_bucket_service import DatasetBucketService
from services.dataset.dataset_processor_service import DatasetProcessorService
from services.validators.dataset_validator_service import DatasetValidatorService

logger = logging.getLogger(__name__)

config = ConfigFactory.get_config()


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

    DatasetValidatorService.validate_file_is_json(filename)

    dataset_bucket_service = DatasetBucketService(bucket_name)

    raw_dataset_with_metadata = dataset_bucket_service.get_and_validate_dataset(
        filename
    )

    logger.info("Dataset obtained from bucket successfully.")
    logger.debug(f"Dataset: {raw_dataset_with_metadata}")

    DatasetProcessorService().process_raw_dataset(filename, raw_dataset_with_metadata)

    logger.info("Dataset uploaded successfully.")

    if config.AUTODELETE_DATASET_BUCKET_FILE is True:
        dataset_bucket_service.try_empty_bucket()

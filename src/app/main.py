import functions_framework
from logging_config import logging
from repositories.buckets.dataset_bucket_repository import DatasetBucketRepository
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

    bucket_name = cloud_event.data["bucket"]
    filename = cloud_event.data["name"]

    DatasetValidatorService.validate_file_is_json(filename)

    raw_dataset_with_metadata = DatasetBucketRepository(
        bucket_name
    ).get_bucket_file_as_json(filename=filename, bucket_name=bucket_name)

    DatasetValidatorService.validate_raw_dataset(raw_dataset_with_metadata)

    logger.info("Dataset obtained successfully.")
    logger.debug(f"Dataset: {raw_dataset_with_metadata}")

    DatasetProcessorService().process_new_dataset(filename, raw_dataset_with_metadata)

    logger.info("Dataset uploaded successfully.")

import functions_framework
from logging_config import logging
from repositories.buckets.dataset_bucket_repository import DatasetBucketRepository
from services.dataset.dataset_processor_service import DatasetProcessorService
from services.dataset.dataset_validator_service import DatasetValidatorService

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

    DatasetValidatorService().validate_filename(filename)

    dataset = DatasetBucketRepository().get_file_from_bucket(
        filename=filename, bucket_name=bucket_name
    )

    DatasetValidatorService().validate_dataset_exists_in_bucket(dataset)
    DatasetValidatorService().validate_dataset_keys(dataset)

    logger.info("Dataset obtained successfully.")
    logger.debug(f"Dataset: {dataset}")

    DatasetProcessorService().process_new_dataset(filename, dataset)

    logger.info("Dataset uploaded successfully.")

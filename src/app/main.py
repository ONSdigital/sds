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

    dataset = dataset_storage.get_dataset(filename=filename, bucket_name=bucket_name)

    logger.info("Dataset obtained successfully.")
    logger.debug(f"Dataset: {dataset}")

    dataset_id = str(uuid.uuid4())
    if dataset:
        database.set_dataset(dataset_id=dataset_id, filename=filename, dataset=dataset)
        logger.info("Dataset uploaded successfully.")
    else:
        logger.error("Invalid JSON file contents")       

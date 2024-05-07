from config.config_factory import config
from logging_config import logging
from models.dataset_models import (
    DatasetError,
    DatasetMetadata,
    DatasetMetadataWithoutId,
    DatasetPublishResponse,
    UnitDataset,
)
from repositories.firebase.dataset_firebase_repository import DatasetFirebaseRepository
from services.shared.publisher_service import publisher_service

logger = logging.getLogger(__name__)


class DatasetWriterService:
    def __init__(
        self,
        dataset_firebase_repository: DatasetFirebaseRepository,
    ):
        self.dataset_firebase_repository = dataset_firebase_repository

    def perform_dataset_transaction(
        self,
        dataset_id: str,
        dataset_metadata_without_id: DatasetMetadataWithoutId,
        unit_data_collection_with_metadata: list[UnitDataset],
        extracted_unit_data_identifiers: list[str],
    ) -> DatasetMetadata | DatasetPublishResponse:
        """
        Performs a transaction on dataset data, committing if dataset metadata and unit data operations are successful,
        rolling back otherwise, and returning a publish response.

        Parameters:
        dataset_id: the uniquely generated id of the dataset
        dataset_metadata_without_id: the metadata of the dataset without its id
        unit_data_collection_with_metadata: the collection of unit data associated with the new dataset
        extracted_unit_data_identifiers: list of identifiers ordered to match the identifier for each set of
            unit data in the collection.
        """
        logger.info("Beginning dataset transaction...")
        try:
            self.dataset_firebase_repository.perform_new_dataset_transaction(
                dataset_id,
                dataset_metadata_without_id,
                unit_data_collection_with_metadata,
                extracted_unit_data_identifiers,
            )
            logger.info(
                "Dataset transaction committed successfully. Publishing dataset metadata to topic..."
            )

            return {
                **dataset_metadata_without_id,
                "dataset_id": dataset_id,
            }
        except Exception as e:
            logger.error(f"Dataset transaction error, exception raised: {e}")
            logger.error("Rolling back dataset transaction.")

            logger.info("Publishing dataset error response to topic.")
            return {"status": "error", "message": "Publishing dataset has failed."}

    def try_publish_dataset_metadata_to_topic(
        self,
        dataset_publish_response: (
            DatasetMetadata | DatasetPublishResponse | DatasetError
        ),
    ) -> None:
        """
        Publishes dataset response to google pubsub topic, raising an exception if unsuccessful.

        Parameters:
        dataset_publish_response: dataset metadata or unhappy path response to be published.
        """
        # if the dataset publish response is an error, set topic_id to the error topic id
        topic_id = (
            config.PUBLISH_DATASET_ERROR_TOPIC_ID
            if isinstance(dataset_publish_response, DatasetError)
            else config.PUBLISH_DATASET_TOPIC_ID
        )

        try:
            publisher_service.publish_data_to_topic(
                dataset_publish_response,
                config.PUBLISH_DATASET_TOPIC_ID,
            )
            logger.debug(
                f"Dataset response {dataset_publish_response} published to topic {topic_id}"
            )
            logger.info("Dataset response published successfully.")
        except Exception as e:
            logger.debug(
                f"Dataset response {dataset_publish_response} failed to publish to topic {topic_id} "
                f"with error {e}"
            )
            raise RuntimeError("Error publishing dataset response to the topic.")

    def try_perform_delete_previous_version_dataset_transaction(
        self, survey_id: str, period_id: str, previous_version: int
    ) -> None:
        """
        Tries to delete the latest previous version of a dataset, if this fails an error is raised.

        Parameters:
        survey_id: survey id of the dataset.
        previous_version: latest previous version of the dataset.
        """
        logger.info(
            f"Deleting a previous version dataset. Version nnumber: {previous_version}..."
        )
        try:
            self.dataset_firebase_repository.perform_delete_previous_version_dataset_transaction(
                survey_id, period_id, previous_version
            )
            logger.info("Previous version of dataset deleted succesfully.")
        except Exception as e:
            logger.debug(
                f"Failed to delete previous version of dataset with survey id: {survey_id} \
                and version number: {previous_version}, message: {e}"
            )
            raise RuntimeError(
                "Failed to delete previous version of dataset from firestore. Rolling back..."
            )

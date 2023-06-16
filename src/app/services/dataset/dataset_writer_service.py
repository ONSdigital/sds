from config.config_factory import config
from logging_config import logging
from models.dataset_models import DatasetMetadata, DatasetMetadataWithoutId, UnitDataset
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
        extracted_unit_data_rurefs: list[str],
    ) -> None:
        """
        Performs a transaction on dataset data, committing if dataset metadata and unit data operations are successful,
        rolling back otherwise.

        Parameters:
        dataset_id: the uniquely generated id of the dataset
        dataset_metadata_without_id: the metadata of the dataset without its id
        unit_data_collection_with_metadata: the collection of unit data associated with the new dataset
        extracted_unit_data_rurefs: list of rurefs ordered to match the ruref for each set of unit data in the collection
        """
        logger.info("Beginning dataset transaction...")
        try:
            self.dataset_firebase_repository.perform_new_dataset_transaction(
                dataset_id,
                dataset_metadata_without_id,
                unit_data_collection_with_metadata,
                extracted_unit_data_rurefs,
            )
        except Exception as e:
            logger.error(f"Dataset transaction error, exception raised: {e}")
            logger.error("Rolling back dataset transaction")
            raise Exception("Error performing dataset transaction.")

        logger.info("Dataset transaction committed successfully.")

    def try_publish_dataset_metadata_to_topic(
        self,
        dataset_metadata: DatasetMetadata,
    ) -> None:
        try:
            logger.info("Publishing dataset metadata to topic...")
            publisher_service.publish_data_to_topic(
                dataset_metadata,
                config.DATASET_TOPIC_ID,
            )
            logger.debug(
                f"Dataset metadata {dataset_metadata} published to topic {config.DATASET_TOPIC_ID}"
            )
            logger.info("Dataset metadata published successfully.")
        except Exception as e:
            logger.debug(
                f"Dataset metadata {dataset_metadata} failed to publish to topic {config.DATASET_TOPIC_ID} with error {e}"
            )
            logger.error("Error publishing dataset metadata to topic.")

    def try_perform_delete_previous_versions_datasets_transaction(
        self, survey_id: str, latest_version: int
    ) -> None:
        """
        Tries to delete all versions of a dataset except the latest version, if this fails an error is raised.

        Parameters:
        survey_id: survey id of the dataset.
        latest_version: latest version of the dataset.
        """
        logger.info("Deleting previous dataset versions...")
        try:
            self.dataset_firebase_repository.perform_delete_previous_versions_datasets_transaction(
                survey_id, latest_version
            )
            logger.info("Previous versions deleted succesfully.")
        except Exception as e:
            logger.debug(
                f"Failed to delete previous versions of dataset with survey id {survey_id} \
                and latest version {latest_version}, message: {e}"
            )
            raise RuntimeError(
                "Failed to delete previous dataset versions from firestore. Rolling back..."
            )

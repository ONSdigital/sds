from logging_config import logging
from models.dataset_models import DatasetMetadataWithoutId, UnitDataset
from repositories.firebase.dataset_firebase_repository import DatasetFirebaseRepository

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

    def try_delete_previous_versions_datasets(
        self, survey_id: str, latest_version: int
    ) -> None:
        """
        Tries to delete all versions of a dataset except the latest version, if this fails an error is raised.

        Parameters:
        survey_id (str): survey id of the dataset.
        latest_version (int): latest version of the dataset.
        """

        logger.info("Deleting previous dataset versions...")
        try:
            self.dataset_firebase_repository.delete_previous_versions_datasets(
                survey_id, latest_version
            )
            logger.info("Previous versions deleted succesfully.")
        except Exception as e:
            logger.debug(
                f"Failed to delete previous versions of dataset with survey id {survey_id} \
                and latest version {latest_version}, message: {e}"
            )
            raise RuntimeError(
                "Failed to delete previous dataset versions from firestore."
            )

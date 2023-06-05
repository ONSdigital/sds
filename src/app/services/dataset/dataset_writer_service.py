from logging_config import logging
from models.dataset_models import DatasetMetadataWithoutId, UnitDataset
from repositories.firebase.dataset_firebase_repository import DatasetFirebaseRepository
from services.shared.firestore_transaction_service import firestore_transaction_service

logger = logging.getLogger(__name__)


class DatasetWriterService:
    def __init__(
        self,
        dataset_repository: DatasetFirebaseRepository,
    ):
        self.dataset_repository = dataset_repository

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
            self.dataset_repository.write_dataset_metadata_to_repository(
                dataset_id, dataset_metadata_without_id
            )
            self._write_unit_data_to_repository(
                dataset_id,
                unit_data_collection_with_metadata,
                extracted_unit_data_rurefs,
            )

            logger.info("Committing dataset transaction")
            firestore_transaction_service.commit_transaction()
            logger.info("Dataset transaction committed")
        except Exception as e:
            logger.error(f"Performing dataset transaction: exception raised: {e}")
            logger.error("Rolling back dataset transaction")
            firestore_transaction_service.rollback_transaction()
            logger.info("Dataset transaction rolled back")

    def _write_unit_data_to_repository(
        self,
        dataset_id: str,
        unit_data_collection_with_metadata: list[UnitDataset],
        rurefs: list[str],
    ) -> None:
        """
        Writes the new unit data to the database

        Parameters:
        dataset_id: the uniquely generated id of the dataset
        unit_data_collection_with_metadata: the collection of unit data associated with the new dataset
        extracted_unit_data_rurefs: list of rurefs ordered to match the ruref for each set of unit data in the collection
        """
        logger.info("Writing transformed unit data to repository...")
        database_unit_data_collection = (
            self.dataset_repository.get_dataset_unit_collection(dataset_id)
        )

        rurefs_iter = iter(rurefs)

        for unit_data in unit_data_collection_with_metadata:
            self.dataset_repository.append_unit_to_dataset_units_collection(
                database_unit_data_collection, unit_data, next(rurefs_iter)
            )

        logger.info("Transformed unit data written to repository successfully.")

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
            self.dataset_repository.delete_previous_versions_datasets(
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

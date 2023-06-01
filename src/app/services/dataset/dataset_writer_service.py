from logging_config import logging
from models.dataset_models import DatasetMetadata, DatasetMetadataWithoutId
from repositories.firebase.dataset_firebase_repository import DatasetFirebaseRepository

logger = logging.getLogger(__name__)


class DatasetWriterService:
    def __init__(
        self,
        dataset_repository: DatasetFirebaseRepository,
    ):
        self.dataset_repository = dataset_repository

    def write_dataset_metadata_to_repository(
        self,
        dataset_id: str,
        dataset_metadata_without_id: DatasetMetadataWithoutId,
    ) -> None:
        """
        Writes the dataset metadata data to the database

        Parameters:
        dataset_id: id of the dataset
        dataset_metadata_without_id: the dataset metadata being written
        """
        logger.info("Writing Dataset metadata to repository...")
        logger.debug(f"Writing dataset metadata with id {dataset_id}")

        self.dataset_repository.write_dataset_metadata_to_repository(
            dataset_id, dataset_metadata_without_id
        )

        logger.info("Dataset metadata written to repository successfully.")

    def write_unit_data_to_repository(
        self,
        dataset_id: str,
        new_dataset_unit_data_collection: list[object],
        rurefs: list,
    ) -> None:
        """
        Writes the new unit data to the database

        Parameters:
        dataset_id (str): the uniquely generated id of the dataset
        new_dataset_unit_data_collection (list[object]): the collection of unit data associated with the new dataset
        """
        logger.info("Writing transformed unit data to repository...")
        database_unit_data_collection = (
            self.dataset_repository.get_dataset_unit_collection(dataset_id)
        )

        rurefs_iter = iter(rurefs)

        for unit_data in new_dataset_unit_data_collection:
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

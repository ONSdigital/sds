from models.dataset_models import DatasetMetadata
from repositories.firebase.dataset_firebase_repository import DatasetFirebaseRepository


class DatasetWriterService:
    def __init__(
        self,
        dataset_repository: DatasetFirebaseRepository,
    ):
        self.dataset_repository = dataset_repository

    def write_transformed_dataset_to_repository(
        self,
        dataset_id,
        transformed_dataset: DatasetMetadata,
    ) -> None:
        """
        Writes the transformed data to the database

        Parameters:
        transformed_dataset (DatasetMetadata): the transformed dataset being written
        """
        self.dataset_repository.create_new_dataset(dataset_id, transformed_dataset)

    def write_transformed_unit_data_to_repository(
        self, dataset_id: str, new_dataset_unit_data_collection: list[object]
    ) -> None:
        """
        Writes the new unit data to the database

        Parameters:
        dataset_id (str): the uniquely generated id of the dataset
        new_dataset_unit_data_collection (list[object]): the collection of unit data associated with the new dataset
        """
        database_unit_data_collection = (
            self.dataset_repository.get_dataset_unit_collection(dataset_id)
        )

        for unit_data in new_dataset_unit_data_collection:
            self.dataset_repository.append_unit_to_dataset_units_collection(
                database_unit_data_collection, unit_data
            )

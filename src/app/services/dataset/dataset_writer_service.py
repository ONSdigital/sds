import uuid

from models import DatasetMetadataDto
from repositories.dataset_repository import DatasetRepository


class DatasetWriterService:
    def __init__(self, dataset_repository: DatasetRepository):
        self.dataset_repository = dataset_repository

    def write_transformed_dataset_to_database(
        self,
        transformed_dataset: DatasetMetadataDto,
        dataset_unit_data_collection: list[object],
    ) -> None:
        """
        Writes the transformed data to the database

        Parameters:
        transformed_dataset (DatasetMetadataDto): the transformed dataset being written
        dataset_unit_data_collection (list[object]): the collection of unit data associated with the dataset
        """
        dataset_id = str(uuid.uuid4())
        self.dataset_repository.create_new_dataset(dataset_id, transformed_dataset)
        self.write_new_unit_data_to_database(dataset_id, dataset_unit_data_collection)
        

    def write_new_unit_data_to_database(
        self, dataset_id: str, dataset_unit_data_collection: list[object]
    ) -> None:
        """
        Writes the new unit data to the database

        Parameters:
        dataset_id (str): the uniquely generated id of the dataset
        dataset_unit_data_collection (list[object]): the collection of unit data associated with the dataset
        """
        database_unit_data_collection = (
            self.dataset_repository.get_dataset_unit_collection(dataset_id)
        )
        for unit_data in dataset_unit_data_collection:
            self.dataset_repository.append_unit_to_dataset_units_collection(
                database_unit_data_collection, unit_data
            )

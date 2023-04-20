from models import DatasetMetadataDto
from repositories.dataset_repository import DatasetRepository
from services.dataset.dataset_reader_service import DatasetReaderService


class DatasetWriterService:
    def __init__(
        self,
        dataset_repository: DatasetRepository,
        dataset_reader_service: DatasetReaderService,
    ):
        self.dataset_repository = dataset_repository
        self.dataset_reader_service = dataset_reader_service

    def write_transformed_dataset_to_database(
        self,
        dataset_id,
        transformed_dataset: DatasetMetadataDto,
    ) -> None:
        """
        Writes the transformed data to the database

        Parameters:
        transformed_dataset (DatasetMetadataDto): the transformed dataset being written
        dataset_unit_data_collection (list[object]): the collection of unit data associated with the dataset
        """
        self.dataset_repository.create_new_dataset(dataset_id, transformed_dataset)

    def write_new_unit_data_to_database(
        self, dataset_id: str, new_dataset_unit_data_collection: list[object]
    ) -> None:
        """
        Writes the new unit data to the database

        Parameters:
        dataset_id (str): the uniquely generated id of the dataset
        dataset_unit_data_collection (list[object]): the collection of unit data associated with the dataset
        """
        database_unit_data_collection = (
            self.dataset_reader_service.get_dataset_unit_collection(dataset_id)
        )

        for unit_data in new_dataset_unit_data_collection:
            self.dataset_repository.append_unit_to_dataset_units_collection(
                database_unit_data_collection, unit_data
            )

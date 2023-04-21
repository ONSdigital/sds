import uuid

from models import (
    DatasetMetadataDto,
    DatasetMetadataWithoutIdDto,
    NewDatasetMetadata,
    NewDatasetWithMetadata,
    UnitDataset,
)
from repositories.dataset_repository import DatasetRepository
from services.dataset.dataset_reader_service import DatasetReaderService
from services.dataset.dataset_writer_service import DatasetWriterService
from services.datetime_service import DatetimeService


class DatasetProcessorService:
    def __init__(self) -> None:
        self.dataset_repository = DatasetRepository()

        self.dataset_reader_service = DatasetReaderService(self.dataset_repository)
        self.dataset_writer_service = DatasetWriterService(
            self.dataset_repository, self.dataset_reader_service
        )
        pass

    def process_new_dataset(
        self, filename: str, dataset: NewDatasetWithMetadata
    ) -> None:
        """
        Processes the incoming dataset.

        Parameters:
        filename (str): the filename of the json containing the dataset data
        dataset (NewDatasetWithMetadata): dataset to be processed
        """
        new_dataset_unit_data_collection = dataset.pop("data")

        transformed_dataset = self.transform_dataset_metadata(
            dataset, filename, new_dataset_unit_data_collection
        )

        dataset_id = str(uuid.uuid4())
        self.dataset_writer_service.write_transformed_dataset_to_database(
            dataset_id,
            transformed_dataset,
        )

        transformed_unit_data_collection = self.transform_dataset_unit_data_collection(
            dataset_id, transformed_dataset, new_dataset_unit_data_collection
        )
        self.dataset_writer_service.write_new_unit_data_to_database(
            dataset_id, transformed_unit_data_collection
        )

    def transform_dataset_metadata(
        self,
        dataset: NewDatasetMetadata,
        filename: str,
        dataset_unit_data_collection: list[object],
    ) -> DatasetMetadataWithoutIdDto:
        """
        Returns a copy of the dataset with added metadata.

        Parameters:
        dataset (NewDatasetMetadata): the original dataset.
        filename (str): the filename of the json containing the dataset data
        dataset_data (list[object]): unit
        """
        return {
            **dataset,
            "filename": filename,
            "sds_published_at": str(
                DatetimeService.get_current_date_and_time().strftime(
                    "%Y-%m-%dT%H:%M:%SZ"
                )
            ),
            "total_reporting_units": len(dataset_unit_data_collection),
            "sds_dataset_version": self.calculate_next_dataset_version(
                dataset["survey_id"]
            ),
        }

    def calculate_next_dataset_version(self, survey_id: str) -> int:
        """
        Calculates the next sds_dataset_version from a single dataset from firestore with a specific survey_id.

        Parameters:
        survey_id (str): survey_id of the specified dataset.
        """
        datasets_result = self.dataset_reader_service.get_dataset_with_survey_id(
            survey_id
        )

        try:
            latest_version = next(iter(datasets_result))["sds_dataset_version"] + 1
        except StopIteration:
            latest_version = 1

        return latest_version

    def transform_dataset_unit_data_collection(
        self,
        dataset_id: str,
        transformed_dataset: DatasetMetadataWithoutIdDto,
        new_dataset_unit_data_collection: list[object],
    ) -> list[UnitDataset]:
        return [
            self.transform_unit_data_item(dataset_id, transformed_dataset, item)
            for item in new_dataset_unit_data_collection
        ]

    def transform_unit_data_item(
        self,
        dataset_id: str,
        transformed_dataset: DatasetMetadataWithoutIdDto,
        unit_data_item: object,
    ):
        return {
            "dataset_id": dataset_id,
            "survey_id": transformed_dataset["survey_id"],
            "period_id": transformed_dataset["period_id"],
            "sds_schema_version": transformed_dataset["sds_schema_version"],
            "schema_version": transformed_dataset["schema_version"],
            "form_type": transformed_dataset["form_type"],
            "data": unit_data_item,
        }
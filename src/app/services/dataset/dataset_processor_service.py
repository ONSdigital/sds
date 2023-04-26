import uuid

from config.config_factory import ConfigFactory
from models.dataset_models import (
    DatasetMetadataWithoutId,
    NewDatasetMetadata,
    NewDatasetWithMetadata,
    UnitDataset,
)
from repositories.dataset_repository import DatasetRepository
from services.dataset.dataset_reader_service import DatasetReaderService
from services.dataset.dataset_writer_service import DatasetWriterService
from services.datetime_service import DatetimeService

config = ConfigFactory.get_config()

from logging_config import logging

logger = logging.getLogger(__name__)


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

        transformed_dataset = self._transform_dataset_metadata(
            dataset, filename, new_dataset_unit_data_collection
        )
        logger.debug(f"Transformed dataset: {transformed_dataset}")

        dataset_id = str(uuid.uuid4())
        self.dataset_writer_service.write_transformed_dataset_to_repository(
            dataset_id,
            transformed_dataset,
        )

        transformed_unit_data_collection = self._transform_dataset_unit_data_collection(
            dataset_id, transformed_dataset, new_dataset_unit_data_collection
        )
        logger.debug(
            f"Transformed unit data collection: {transformed_unit_data_collection}"
        )

        self.dataset_writer_service.write_new_unit_data_to_repository(
            dataset_id, transformed_unit_data_collection
        )

    def _transform_dataset_metadata(
        self,
        dataset: NewDatasetMetadata,
        filename: str,
        dataset_unit_data_collection: list[object],
    ) -> DatasetMetadataWithoutId:
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
                DatetimeService.get_current_date_and_time().strftime(config.TIME_FORMAT)
            ),
            "total_reporting_units": len(dataset_unit_data_collection),
            "sds_dataset_version": self.dataset_repository.get_latest_survey_version(
                dataset["survey_id"]
            ),
        }

    def _transform_dataset_unit_data_collection(
        self,
        dataset_id: str,
        transformed_dataset_metadata: DatasetMetadataWithoutId,
        new_dataset_unit_data_collection: list[object],
    ) -> list[UnitDataset]:
        """
        Transforms the new unit data to a new format for storing in firestore.

        Parameters:
        dataset_id (str): dataset_id for the new dataset.
        transformed_dataset_metadata (DatasetMetadataWithoutIdDto): the dataset metadata without id
        new_dataset_unit_data_collection (list[object]): list of unit data to be transformed
        """
        return [
            self._transform_unit_data_item(
                dataset_id, transformed_dataset_metadata, item
            )
            for item in new_dataset_unit_data_collection
        ]

    def _transform_unit_data_item(
        self,
        dataset_id: str,
        transformed_dataset_metadata: DatasetMetadataWithoutId,
        unit_data_item: object,
    ) -> UnitDataset:
        """
        Transforms a unit data item to a new format for storing in firestore.

        Parameters:
        dataset_id (str): dataset_id for the new dataset.
        transformed_dataset_metadata (DatasetMetadataWithoutIdDto): the dataset metadata without id
        unit_data_item (object): unit data item to be transformed
        """
        return {
            "dataset_id": dataset_id,
            "survey_id": transformed_dataset_metadata["survey_id"],
            "period_id": transformed_dataset_metadata["period_id"],
            "sds_schema_version": transformed_dataset_metadata["sds_schema_version"],
            "schema_version": transformed_dataset_metadata["schema_version"],
            "form_type": transformed_dataset_metadata["form_type"],
            "data": unit_data_item,
        }

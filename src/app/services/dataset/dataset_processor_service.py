import uuid

from config.config_factory import ConfigFactory
from logging_config import logging
from models.dataset_models import (
    DatasetMetadata,
    DatasetMetadataWithoutId,
    RawDatasetMetadata,
    RawDatasetWithMetadata,
    UnitDataset,
)
from repositories.firebase.dataset_firebase_repository import DatasetFirebaseRepository
from services.dataset.dataset_writer_service import DatasetWriterService
from services.shared.datetime_service import DatetimeService
from services.shared.document_version_service import DocumentVersionService

logger = logging.getLogger(__name__)


class DatasetProcessorService:
    def __init__(self) -> None:
        self.config = ConfigFactory.get_config()

        self.dataset_repository = DatasetFirebaseRepository()
        self.dataset_writer_service = DatasetWriterService(self.dataset_repository)

    def process_new_dataset(
        self, filename: str, new_dataset: RawDatasetWithMetadata
    ) -> None:
        """
        Processes the incoming dataset.

        Parameters:
        filename (str): the filename of the json containing the dataset data
        new_dataset (NewDatasetWithMetadata): new dataset to be processed
        """
        logger.info("Processing new dataset...")
        logger.debug(f"Dataset being processed: {new_dataset}")

        new_dataset_unit_data_collection = new_dataset.pop("data")
        dataset_id = str(uuid.uuid4())

        logger.info("Transforming new dataset metadata...")
        transformed_dataset = self._add_metadata_to_new_dataset(
            new_dataset, filename, new_dataset_unit_data_collection
        )
        logger.info("Dataset transformed successfully.")

        logger.info("Writing transformed dataset to repository...")
        logger.debug(f"Writing dataset with id {dataset_id}")
        self.dataset_writer_service.write_transformed_dataset_to_repository(
            dataset_id,
            transformed_dataset,
        )
        logger.info("Transformed dataset written to repository successfully.")

        logger.info("Transforming unit data collection...")
        transformed_unit_data_collection = self._add_metadata_to_unit_data_collection(
            dataset_id, transformed_dataset, new_dataset_unit_data_collection
        )
        logger.info("Unit data collection transformed successfully.")
        logger.debug(
            f"Transformed unit data collection for dataset with id: {dataset_id}"
        )

        logger.info("Writing transformed unit data to repository...")
        self.dataset_writer_service.write_transformed_unit_data_to_repository(
            dataset_id, transformed_unit_data_collection
        )
        logger.info("Transformed unit data written to repository successfully.")

    def _add_metadata_to_new_dataset(
        self,
        new_dataset_metadata: RawDatasetMetadata,
        filename: str,
        dataset_unit_data_collection: list[object],
    ) -> DatasetMetadataWithoutId:
        """
        Returns a copy of the dataset with added metadata.

        Parameters:
        new_dataset_metadata (NewDatasetMetadata): the original dataset.
        filename (str): the filename of the json containing the dataset data
        dataset_unit_data_collection (list[object]): collection of unit data in the new dataset
        """
        return {
            **new_dataset_metadata,
            "filename": filename,
            "sds_published_at": str(
                DatetimeService.get_current_date_and_time().strftime(
                    self.config.TIME_FORMAT
                )
            ),
            "total_reporting_units": len(dataset_unit_data_collection),
            "sds_dataset_version": self._calculate_next_dataset_version(
                new_dataset_metadata["survey_id"]
            ),
        }

    def _calculate_next_dataset_version(self, survey_id: str) -> int:
        """
        Calculates the next sds_dataset_version from a single dataset from firestore with a specific survey_id.

        Parameters:
        survey_id (str): survey_id of the specified dataset.
        """
        datasets_result = self.dataset_repository.get_dataset_with_survey_id(survey_id)

        return DocumentVersionService.calculate_survey_version(
            datasets_result, "sds_dataset_version"
        )

    def _add_metadata_to_unit_data_collection(
        self,
        dataset_id: str,
        transformed_dataset_metadata: DatasetMetadataWithoutId,
        new_dataset_unit_data_collection: list[object],
    ) -> list[UnitDataset]:
        """
        Transforms the new unit data to a new format for storing in firestore.

        Parameters:
        dataset_id (str): dataset_id for the new dataset.
        transformed_dataset_metadata (DatasetMetadataWithoutId): the dataset metadata without id
        new_dataset_unit_data_collection (list[object]): list of unit data to be transformed
        """
        return [
            self._add_metatadata_to_unit_data_item(
                dataset_id, transformed_dataset_metadata, item
            )
            for item in new_dataset_unit_data_collection
        ]

    def _add_metatadata_to_unit_data_item(
        self,
        dataset_id: str,
        transformed_dataset_metadata: DatasetMetadataWithoutId,
        unit_data_item: object,
    ) -> UnitDataset:
        """
        Transforms a unit data item to a new format for storing in firestore.

        Parameters:
        dataset_id (str): dataset_id for the new dataset.
        transformed_dataset_metadata (DatasetMetadataWithoutId): the dataset metadata without id
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

    def get_dataset_metadata_collection(
        self, survey_id, period_id
    ) -> list[DatasetMetadata]:
        dataset_metadata_collection_generator = (
            self.dataset_repository.get_dataset_metadata_collection(
                survey_id, period_id
            )
        )

        dataset_metadata_collection = []
        for dataset in dataset_metadata_collection_generator:
            metadata_collection_item = dataset.to_dict()
            metadata_collection_item["dataset_id"] = dataset.id
            dataset_metadata_collection.append(metadata_collection_item)

        return dataset_metadata_collection

import uuid

from config.config_factory import ConfigFactory
from google.cloud.firestore_v1.document import DocumentSnapshot
from logging_config import logging
from models.dataset_models import (
    DatasetMetadata,
    DatasetMetadataWithoutId,
    UnitDataset,
    UnitDatasetWithoutData,
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

    def process_raw_dataset(self, filename: str, raw_dataset: UnitDataset) -> None:
        """
        Processes the incoming dataset.

        Parameters:
        filename (str): the filename of the json containing the dataset data
        raw_dataset (RawDatasetWithMetadata): new dataset to be processed
        """
        logger.info("Processing new dataset...")
        logger.debug(f"Dataset being processed: {raw_dataset}")

        new_dataset_unit_data_collection = raw_dataset.pop("data")
        dataset_id = str(uuid.uuid4())

        dataset_metadata_without_id = self._add_metadata_to_new_dataset(
            raw_dataset, filename, new_dataset_unit_data_collection
        )

        self.dataset_writer_service.write_dataset_metadata_to_repository(
            dataset_id,
            dataset_metadata_without_id,
        )

        extracted_unit_data_rurefs = self._extract_rurefs_from_unit_data(
            new_dataset_unit_data_collection
        )

        unit_data_collection_with_metadata = self._add_metadata_to_unit_data_collection(
            dataset_id, dataset_metadata_without_id, new_dataset_unit_data_collection
        )

        self.dataset_writer_service.write_unit_data_to_repository(
            dataset_id, unit_data_collection_with_metadata, extracted_unit_data_rurefs
        )

        self.dataset_writer_service.try_delete_previous_versions_datasets(
            dataset_metadata_without_id["survey_id"],
            dataset_metadata_without_id["sds_dataset_version"],
        )

    def _add_metadata_to_new_dataset(
        self,
        raw_dataset_metadata: UnitDatasetWithoutData,
        filename: str,
        dataset_unit_data_collection: list[object],
    ) -> DatasetMetadataWithoutId:
        """
        Returns a copy of the dataset with added metadata.

        Parameters:
        raw_dataset_metadata (RawDatasetMetadata): the original dataset.
        filename (str): the filename of the json containing the dataset data
        dataset_unit_data_collection (list[object]): collection of unit data in the new dataset
        """
        logger.info("Adding metadata to new dataset...")

        dataset_metadata_without_id = {
            **raw_dataset_metadata,
            "filename": filename,
            "sds_published_at": str(
                DatetimeService.get_current_date_and_time().strftime(
                    self.config.TIME_FORMAT
                )
            ),
            "total_reporting_units": len(dataset_unit_data_collection),
            "sds_dataset_version": self._calculate_next_dataset_version(
                raw_dataset_metadata["survey_id"]
            ),
        }

        logger.info("Metadata added to new dataset successfully.")

        return dataset_metadata_without_id

    def _calculate_next_dataset_version(self, survey_id: str) -> int:
        """
        Calculates the next sds_dataset_version from a single dataset from firestore with a specific survey_id.

        Parameters:
        survey_id (str): survey_id of the specified dataset.
        """
        datasets_result = self.dataset_repository.get_latest_dataset_with_survey_id(
            survey_id
        )

        return DocumentVersionService.calculate_survey_version(
            datasets_result, "sds_dataset_version"
        )

    def _add_metadata_to_unit_data_collection(
        self,
        dataset_id: str,
        transformed_dataset_metadata: DatasetMetadataWithoutId,
        raw_dataset_unit_data_collection: list[object],
    ) -> list[UnitDataset]:
        """
        Transforms the new unit data to a new format for storing in firestore.

        Parameters:
        dataset_id (str): dataset_id for the new dataset.
        transformed_dataset_metadata (DatasetMetadataWithoutId): the dataset metadata without id
        raw_dataset_unit_data_collection (list[object]): list of unit data to be transformed
        """
        logger.info("Adding metadata to unit data collection...")

        unit_data_collection_with_metadata = [
            self._add_metatadata_to_unit_data_item(
                dataset_id, transformed_dataset_metadata, item
            )
            for item in raw_dataset_unit_data_collection
        ]

        logger.info("Metadata added to unit data collection transformed successfully.")
        logger.debug(
            f"Metadata added to unit data collection for dataset with id: {dataset_id}"
        )

        return unit_data_collection_with_metadata

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
            "data": unit_data_item["unit_data"],
        }

    def get_dataset_metadata_collection(
        self, survey_id: str, period_id: str
    ) -> list[DatasetMetadata]:
        """
        Gets the collection of dataset metadata associated with a specific survey and period id.

        Parameters:
        survey_id (str): survey id of the collection.
        period_id (str): period id of the collection.
        """

        dataset_metadata_collection_generator = (
            self.dataset_repository.get_dataset_metadata_collection(
                survey_id, period_id
            )
        )

        return [
            self._create_dataset_metadata_item_with_id(dataset_metadata_snapshot_item)
            for dataset_metadata_snapshot_item in dataset_metadata_collection_generator
        ]

    def _create_dataset_metadata_item_with_id(
        self, dataset_metadata_snapshot: DocumentSnapshot
    ):
        """
        Creates a dataset metadata dictionary item from a firestore document snapshot.

        Parameters:
        dataset_metadata_snapshot (DocumentSnapshot): firestore document snapshot of a dataset metadata item.
        """
        metadata_collection_item = dataset_metadata_snapshot.to_dict()
        metadata_collection_item["dataset_id"] = dataset_metadata_snapshot.id

        return metadata_collection_item

    def _extract_rurefs_from_unit_data(
        self, raw_dataset_unit_data_collection: list[object]
    ) -> list:
        """
        Extracts all rurefs from unit data to store in a separate list

        Parameters:
        raw_dataset_unit_data_collection (list[object]): list of unit data containing ruref
        """
        logger.info("Extracting rurefs from unit data...")

        extracted_unit_data_rurefs = [
            item["ruref"] for item in raw_dataset_unit_data_collection
        ]

        logger.info("Rurefs are extracted and stored successfully.")
        logger.debug(f"Extracted rurefs: {extracted_unit_data_rurefs}")

        return extracted_unit_data_rurefs

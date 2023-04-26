import firebase_admin
from firebase_admin import _apps, firestore
from google.cloud.firestore_v1.document import DocumentSnapshot
from logging_config import logging
from models.dataset_models import DatasetMetadataWithoutId, UnitDataset
from typing import Generator

logger = logging.getLogger(__name__)


class DatasetRepository:
    def __init__(self):
        if not _apps:
            firebase_admin.initialize_app()

        self.db = firestore.client()
        self.datasets_collection = self.db.collection("datasets")

    def get_dataset_with_survey_id(self, survey_id: str) -> Generator[DocumentSnapshot, None, None]:
        """
        Gets the survey id of a single dataset from firestore with a specific survey_id.

        Parameters:
        survey_id (str): survey_id of the specified dataset.
        """
        return (
            self.datasets_collection.where("survey_id", "==", survey_id)
            .order_by("sds_dataset_version", direction=firestore.Query.DESCENDING)
            .limit(1)
            .stream()
        )

    def create_new_dataset(
        self,
        dataset_id: str,
        dataset_metadata_without_id_dto: DatasetMetadataWithoutId,
    ) -> None:
        """
        Creates a new dataset in firestore with a specified ID and data.

        Parameters:
        dataset_id (str): uniquely generated GUID id of the dataset.
        dataset (UnitData): unit dataset being created in firestore.
        """
        self.datasets_collection.document(dataset_id).set(
            dataset_metadata_without_id_dto
        )

    def get_dataset_unit_collection(self, dataset_id: str) -> list[UnitDataset]:
        """
        Gets the collection of units associated with a particular dataset.

        Parameters:
        dataset_id (str): uniquely generated GUID id of the dataset.
        """
        return self.datasets_collection.document(dataset_id).collection("units")

    def append_unit_to_dataset_units_collection(
        self, units_collection: list[UnitDataset], unit_data: UnitDataset
    ) -> None:
        """
        Appends a new unit to the collection of units associated with a particular dataset.

        Parameters:
        units_collection (any): The collection of units that data is being appended to.
        unit_data (any): The unit being appended
        """
        logger.debug(f"Unit data being appended: {unit_data}")
        units_collection.document(unit_data["data"]["ruref"]).set(unit_data)

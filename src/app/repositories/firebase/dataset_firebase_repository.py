from typing import Generator

import firebase_admin
from firebase_admin import _apps, firestore
from google.cloud.firestore_v1.document import DocumentSnapshot
from logging_config import logging
from models.dataset_models import DatasetMetadataWithoutId, UnitDataset

logger = logging.getLogger(__name__)


class DatasetFirebaseRepository:
    def __init__(self):
        if not _apps:
            firebase_admin.initialize_app()

        self.db = firestore.client()
        self.datasets_collection = self.db.collection("datasets")

        self.document_units_key = "units"

    def get_latest_dataset_with_survey_id(
        self, survey_id: str
    ) -> Generator[DocumentSnapshot, None, None]:
        """
        Gets a DocumentSnapshot generator of the latest dataset from firestore with a specific survey_id.

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
        dataset_metadata_without_id: DatasetMetadataWithoutId,
    ) -> None:
        """
        Creates a new dataset in firestore with a specified ID and data.

        Parameters:
        dataset_id (str): uniquely generated GUID id of the dataset.
        dataset_metadata_without_id (DatasetMetadataWithoutId): metadata of the new dataset without id.
        """
        logger.debug(
            f"Setting dataset with id {dataset_id} and data {dataset_metadata_without_id}"
        )
        self.datasets_collection.document(dataset_id).set(dataset_metadata_without_id)

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

    def get_unit_supplementary_data(self, dataset_id: str, unit_id: str) -> UnitDataset:
        """
        Get the unit supplementary data of a specified unit from a dataset collection

        Parameters:
        dataset_id (str): The unique id of the dataset
        unit_id (str): The id of the unit on the dataset
        """
        return (
            self.datasets_collection.document(dataset_id)
            .collection(self.document_units_key)
            .document(unit_id)
            .get()
            .to_dict()
        )

    def get_dataset_metadata_collection(
        self, survey_id: str, period_id: str
    ) -> Generator[DocumentSnapshot, None, None]:
        """
        Get the collection of dataset metadata from firestore associated with a specific survey and period id.

        Parameters:
        survey_id (str): The survey id of the dataset.
        period_id (str): The period id of the unit on the dataset.
        """
        return (
            self.datasets_collection.where("survey_id", "==", survey_id)
            .where("period_id", "==", period_id)
            .stream()
        )

    def delete_previous_dataset_versions(
        self, survey_id: str, latest_version: int
    ) -> None:
        previous_dataset_versions = self.datasets_collection.where(
            "survey_id", "==", survey_id
        ).where("sds_dataset_version", "!=", latest_version)

        self._recursively_delete_collection(previous_dataset_versions)

    def _recursively_delete_collection(self, collection_ref):
        for doc_ref in collection_ref.stream():
            for subcollection_ref in doc_ref.stream():
                self._recursively_delete_collection(subcollection_ref)

        collection_ref.delete()

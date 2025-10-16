
from firebase_admin import firestore

from app.logging_config import logging
from app.models.dataset_models import DatasetMetadata, DatasetMetadataWithoutId, UnitDataset
from app.repositories.firebase.firebase_loader import firebase_loader

logger = logging.getLogger(__name__)


class DatasetFirebaseRepository:
    MAX_BATCH_SIZE_BYTES = 9 * 1024 * 1024

    def __init__(self):
        self.client = firebase_loader.get_client()
        self.datasets_collection = firebase_loader.get_datasets_collection()

    def get_latest_dataset_with_survey_id_and_period_id(
        self, survey_id: str, period_id: str
    ) -> DatasetMetadataWithoutId | None:
        """
        Gets the latest dataset metadata from firestore with a specific survey_id and period_id.

        Parameters:
        survey_id (str): survey_id of the specified dataset.
        period_id (str): period_id of the specified dataset.
        """
        latest_dataset = (
            self.datasets_collection.where("survey_id", "==", survey_id)
            .where("period_id", "==", period_id)
            .order_by("sds_dataset_version", direction=firestore.Query.DESCENDING)
            .limit(1)
            .stream()
        )

        dataset_metadata: DatasetMetadataWithoutId = None
        for dataset in latest_dataset:
            dataset_metadata: DatasetMetadataWithoutId = {**(dataset.to_dict())}

        return dataset_metadata


    def get_unit_supplementary_data(
        self, dataset_id: str, identifier: str
    ) -> UnitDataset:
        """
        Get the unit supplementary data of a specified unit from a dataset collection

        Parameters:
        dataset_id (str): The unique id of the dataset
        identifier (str): The id of the unit on the dataset
        """
        return (
            self.datasets_collection.document(dataset_id)
            .collection("units")
            .document(identifier)
            .get()
            .to_dict()
        )

    def get_number_of_unit_supplementary_data_with_dataset_id(
        self, dataset_id: str, cursor=None
    ) -> int:
        """
        Get the number of unit supplementary data associated with a dataset id.
        This function use a cursor to create a snapshot of unit data and aggregate
        the count. This is to prevent 530 query timed out error when the number of
        unit data is too large.

        Parameters:
        dataset_id (str): The unique id of the dataset

        Returns:
        int: The number of unit supplementary data associated with the dataset id
        """
        limit = 1000
        count = 0

        collection_ref = self.datasets_collection.document(dataset_id).collection(
            "units"
        )

        while True:
            # Frees memory incurred in the recursion algorithm
            docs = []

            if cursor:
                docs = list(collection_ref.limit(limit)
                    .order_by("__name__")
                    .start_after(cursor)
                    .stream())
            else:
                docs = list(collection_ref.limit(limit)
                    .order_by("__name__")
                    .stream())

            count = count + len(docs)

            if len(docs) == limit:
                cursor = docs[limit - 1]
                continue

            break

        return count

    def get_dataset_metadata_collection(
        self, survey_id: str, period_id: str
    ) -> list[DatasetMetadata]:
        """
        Get the collection of dataset metadata from firestore associated with a specific survey and period id.

        Parameters:
        survey_id (str): The survey id of the dataset.
        period_id (str): The period id of the unit on the dataset.
        """
        returned_dataset_metadata = (
            self.datasets_collection.where("survey_id", "==", survey_id)
            .where("period_id", "==", period_id)
            .order_by("sds_dataset_version", direction=firestore.Query.DESCENDING)
            .stream()
        )

        dataset_metadata_list: list[DatasetMetadata] = []
        for dataset_metadata in returned_dataset_metadata:
            metadata: DatasetMetadata = {**dataset_metadata.to_dict()}
            metadata["dataset_id"] = dataset_metadata.id
            dataset_metadata_list.append(metadata)

        return dataset_metadata_list

    def get_all_dataset_metadata_collection(self) -> list[DatasetMetadata]:
        """Get the collection of dataset metadata from firestore for all datasets.
        """
        returned_dataset_metadata = (
            self.datasets_collection
            .order_by("survey_id")
            .order_by("sds_dataset_version", direction=firestore.Query.DESCENDING)
            .stream()
        )
        dataset_metadata_list: list[DatasetMetadata] = []
        for dataset_metadata in returned_dataset_metadata:
            metadata_dict = dataset_metadata.to_dict()
            metadata_dict["dataset_id"] = dataset_metadata.id
            metadata = DatasetMetadata(**metadata_dict)
            dataset_metadata_list.append(metadata)

        return dataset_metadata_list

    def get_dataset_metadata_with_survey_id_period_id_and_version(
        self, survey_id: str, period_id: str, version: int
    ) -> DatasetMetadata | None:
        """
        Get the dataset metadata from firestore associated with a specific survey and period id and version.

        Parameters:
        survey_id (str): The survey id of the dataset.
        period_id (str): The period id of the unit on the dataset.
        version (int): The version of the dataset.

        Returns:
        DatasetMetadata | None: The dataset metadata associated with the survey id, period id and version.
        """
        retrieved_dataset = (
            self.datasets_collection.where("survey_id", "==", survey_id)
            .where("period_id", "==", period_id)
            .where("sds_dataset_version", "==", version)
            .stream()
        )

        dataset_metadata: DatasetMetadata = None
        for dataset in retrieved_dataset:
            dataset_metadata: DatasetMetadata = {**(dataset.to_dict())}
            dataset_metadata["dataset_id"] = dataset.id

        return dataset_metadata

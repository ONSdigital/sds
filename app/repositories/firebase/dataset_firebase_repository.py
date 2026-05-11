
from firebase_admin import firestore

from app.logging_config import logging
from app.models.dataset_models import DatasetMetadata, UnitDataset
from app.repositories.firebase.firebase_loader import FirebaseLoader

logger = logging.getLogger(__name__)


class DatasetFirebaseRepository:

    def __init__(self, firebase_loader: FirebaseLoader) -> None:
        self.client = firebase_loader.get_client()
        self.datasets_collection = firebase_loader.get_datasets_collection()


    def get_unit_supplementary_data(
        self, dataset_id: str, identifier: str
    ) -> UnitDataset:
        """
        Get the unit supplementary data of a specified unit from a dataset collection

        Parameters:
        dataset_id (str): The unique id of the dataset
        identifier (str): The id of the unit on the dataset
        """
        return UnitDataset(
            **self.datasets_collection.document(dataset_id)
            .collection("units")
            .document(identifier)
            .get()
            .to_dict()
        )


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
            metadata_dict = dataset_metadata.to_dict()
            metadata_dict["dataset_id"] = dataset_metadata.id
            metadata = DatasetMetadata(**metadata_dict)
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

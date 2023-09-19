from firebase_admin import firestore
from logging_config import logging
from models.dataset_models import DatasetMetadata, DatasetMetadataWithoutId, UnitDataset
from repositories.firebase.firebase_loader import firebase_loader

logger = logging.getLogger(__name__)


class DatasetFirebaseRepository:
    def __init__(self):
        self.client = firebase_loader.get_client()
        self.datasets_collection = firebase_loader.get_datasets_collection()

    def get_latest_dataset_with_survey_id_and_period_id(
        self, survey_id: str, period_id: str
    ) -> DatasetMetadataWithoutId | None:
        """
        Gets the latest dataset from firestore with a specific survey_id.

        Parameters:
        survey_id (str): survey_id of the specified dataset.
        """
        latest_dataset = (
            self.datasets_collection.where("survey_id", "==", survey_id)
            .where("period_id", "==", period_id)
            .order_by("sds_dataset_version", direction=firestore.Query.DESCENDING)
            .limit(1)
            .stream()
        )

        unit_dataset: DatasetMetadataWithoutId = None
        for dataset in latest_dataset:
            unit_dataset: DatasetMetadataWithoutId = {**(dataset.to_dict())}

        return unit_dataset

    def perform_new_dataset_transaction(
        self,
        dataset_id: str,
        dataset_metadata_without_id: DatasetMetadataWithoutId,
        unit_data_collection_with_metadata: list[UnitDataset],
        extracted_unit_data_identifiers: list[str],
    ):
        """
        Writes dataset metadata and unit data to firestore as a transaction, which is
        rolled back if any of the operations fail.

        Parameters:
        dataset_id: id of the dataset
        dataset_metadata_without_id: dataset metadata without a dataset id
        unit_data_collection_with_metadata: collection of unit data associated to a dataset
        extracted_unit_data_identifiers: identifiers associated with the unit data collection
        """

        # A stipulation of the @firestore.transactional decorator is the first parameter HAS
        # to be 'transaction', but since we're using classes the first parameter is always
        # 'self'. Encapsulating the transaction within this function circumvents the issue.
        @firestore.transactional
        def dataset_transaction(transaction: firestore.Transaction):
            new_dataset_document = self.datasets_collection.document(dataset_id)

            transaction.set(
                new_dataset_document, dataset_metadata_without_id, merge=True
            )
            unit_data_collection_snapshot = new_dataset_document.collection("units")

            for unit_data, identifier in zip(
                unit_data_collection_with_metadata,
                iter(extracted_unit_data_identifiers),
            ):
                new_unit = unit_data_collection_snapshot.document(identifier)
                transaction.set(new_unit, unit_data, merge=True)

        dataset_transaction(self.client.transaction())

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

    def perform_delete_previous_version_dataset_transaction(
        self, survey_id: str, period_id: str, previous_version: int
    ) -> None:
        """
        Queries firestore for a previous version of a dataset associated with a survey id
        and period id, iterates to delete it and their subcollections recursively. The
        recursion is needed because you cannot delete subcollections of a document in firestore
        just by deleting the document, it does not cascade.

        Parameters:
        survey_id: survey id of the dataset.
        period_id: period id of the dataset.
        previous_version: previous version of the dataset to delete.
        """

        # A stipulation of the @firestore.transactional decorator is the first parameter HAS
        # to be 'transaction', but since we're using classes the first parameter is always
        # 'self'. Encapsulating the transaction within this function circumvents the issue.
        @firestore.transactional
        def delete_collection_transaction(transaction: firestore.Transaction):
            previous_version_dataset = (
                self.datasets_collection.where("survey_id", "==", survey_id)
                .where("period_id", "==", period_id)
                .where("sds_dataset_version", "==", previous_version)
            )

            self._delete_collection(transaction, previous_version_dataset)

        delete_collection_transaction(self.client.transaction())

    def _delete_collection(
        self,
        transaction: firestore.Transaction,
        collection_ref: firestore.CollectionReference,
    ) -> None:
        """
        Recursively deletes the collection and its subcollections.

        Parameters:
        transaction: the firestore transaction performing the delete.
        collection_ref: the reference of the collection being deleted.
        """
        doc_collection = collection_ref.stream()

        for doc in doc_collection:
            self._recursively_delete_document_and_sub_collections(
                transaction, doc.reference
            )

    def _recursively_delete_document_and_sub_collections(
        self, transaction: firestore.Transaction, doc_ref: firestore.DocumentReference
    ) -> None:
        """
        Loops through each collection in a document and deletes the collection.

        Parameters:
        transaction: the firestore transaction performing the delete.
        doc_ref: the reference of the document being deleted.
        """
        for collection_ref in doc_ref.collections():
            self._delete_collection(transaction, collection_ref)

        transaction.delete(doc_ref)

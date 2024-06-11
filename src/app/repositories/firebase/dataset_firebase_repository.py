from firebase_admin import firestore
from logging_config import logging
from models.dataset_models import DatasetMetadata, DatasetMetadataWithoutId, UnitDataset
from repositories.firebase.firebase_loader import firebase_loader

logger = logging.getLogger(__name__)


class DatasetFirebaseRepository:
    BATCH_SIZE = 500

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

    def perform_batched_dataset_write(
        self,
        dataset_id: str,
        dataset_metadata_without_id: DatasetMetadataWithoutId,
        unit_data_collection_with_metadata: list[UnitDataset],
        extracted_unit_data_identifiers: list[str],
    ) -> bool:
        """
        Write dataset metadata and unit data to firestore in batches.
        Parameters:
        dataset_id (str): The unique id of the dataset
        dataset_metadata_without_id (DatasetMetadataWithoutId): The metadata of the dataset without its id
        unit_data_collection_with_metadata (list[UnitDataset]): The collection of unit data associated with the new dataset
        extracted_unit_data_identifiers (list[str]): List of identifiers ordered to match the identifier for each set of
        unit data in the collection.

        """

        logger.info("Performing batch writes")
        new_dataset_document = self.datasets_collection.document(dataset_id)
        unit_data_collection_snapshot = new_dataset_document.collection("units")

        try:
            batch = self.client.batch()
            batch.set(new_dataset_document, dataset_metadata_without_id, merge=True)
            batch.commit()

            batch_counter = 0
            batch = self.client.batch()

            for i in range(len(unit_data_collection_with_metadata)):
                if batch_counter > 0 and batch_counter % self.BATCH_SIZE == 0:
                    batch.commit()
                    batch = self.client.batch()

                new_unit = unit_data_collection_snapshot.document(
                    extracted_unit_data_identifiers[i]
                )
                batch.set(new_unit, unit_data_collection_with_metadata[i], merge=True)
                batch_counter += 1

            batch.commit()

            logger.info("Batch writes for dataset completed successfully.")

        except Exception as e:
            logger.error(f"Error performing batched dataset write: {e}")
            self.delete_collection_in_batches(self.datasets_collection, 100, dataset_id)
            logger.info("Dataset clean up is completed")

            raise RuntimeError("Error performing batched dataset write.")

    def delete_collection_in_batches(
        self,
        collection_ref: firestore.CollectionReference,
        batch_size: int,
        dataset_id: str | None = None,
    ):
        logger.info("Deleting data in batches")

        try:
            if dataset_id:
                doc = collection_ref.document(dataset_id).get()
                for subcollection in doc.reference.collections():
                    self.delete_collection_in_batches(subcollection, batch_size)
                doc.reference.delete()
            else:
                docs = collection_ref.limit(batch_size).get()
                doc_count = 0
                for doc in docs:
                    doc_count += 1
                    for subcollection in doc.reference.collections():
                        self.delete_collection_in_batches(subcollection, batch_size)
                    doc.reference.delete()
                if doc_count < batch_size:
                    return None

                return self.delete_collection_in_batches(
                    collection_ref, batch_size, dataset_id
                )
        except Exception as e:
            logger.error(f"Error deleting collection in batches: {e}")
            raise RuntimeError("Error deleting collection in batches.")

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
        self, dataset_id: str
    ) -> int:
        """
        Get the number of unit supplementary data associated with a dataset id.

        Parameters:
        dataset_id (str): The unique id of the dataset
        """

        returned_unit_data = (
            self.datasets_collection.document(dataset_id).collection("units").stream()
        )

        unit_data_count = 0
        for unit_data in returned_unit_data:
            unit_data_count += 1

        return unit_data_count

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

    def perform_delete_previous_version_dataset_batch(
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

        previous_version_dataset = (
            self.datasets_collection.where("survey_id", "==", survey_id)
            .where("period_id", "==", period_id)
            .where("sds_dataset_version", "==", previous_version)
            .stream()
        )

        for dataset in previous_version_dataset:
            dataset_id = dataset.id
            logger.info(f"dataset id {dataset_id}")

        self.delete_collection_in_batches(self.datasets_collection, 100, dataset_id)
        logger.info("Successfully deleted previous version dataset")

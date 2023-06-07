from models.dataset_models import DatasetMetadataWithoutId, UnitDataset
from repositories.firebase.dataset_firebase_repository import DatasetFirebaseRepository
from repositories.firebase.firebase_loader import firebase_loader
from google.cloud.firestore_v1.document import DocumentReference
from google.cloud.firestore_v1 import Transaction


class FirebaseTransactionService:
    def __init__(self) -> None:
        self.client = firebase_loader.get_client()

    def run_transaction(self, transaction_callback):
        self.client.transaction(transaction_callback)

    def dataset_transaction_callback(
        self, 
        transaction: Transaction, 
        dataset_id: str,
        dataset_metadata_without_id: DatasetMetadataWithoutId,
        unit_data_collection_with_metadata: list[UnitDataset],
        extracted_unit_data_rurefs: list[str],
    ):
        new_dataset_document = firebase_loader.datasets_collection().document(dataset_id)
        # datasets_collection.document(dataset_id).set(dataset_metadata_without_id)

        transaction.set(new_dataset_document, dataset_metadata_without_id, merge=True)


        # self.dataset_repository.write_dataset_metadata_to_repository(
        #         dataset_id, dataset_metadata_without_id
        #     )
        
        self._perform_unit_data_transaction(
            new_dataset_document,
            unit_data_collection_with_metadata,
            extracted_unit_data_rurefs,
        )
        
    def _perform_unit_data_transaction(
        self,
        transaction,
        new_dataset_document,
        unit_data_collection_with_metadata: list[UnitDataset],
        rurefs: list[str],
    ) -> None:
        unit_data_collection_snapshot = transaction.get(new_dataset_document.collection("units"))

        rurefs_iter = iter(rurefs)
        for unit_data in unit_data_collection_with_metadata:
            new_unit = unit_data_collection_snapshot(next(rurefs_iter))
            transaction.set(new_unit, unit_data, merge=True)
            # unit_data_collection_snapshot.document(next(rurefs_iter)).set(unit_data)




firebase_transaction_service = FirebaseTransactionService()

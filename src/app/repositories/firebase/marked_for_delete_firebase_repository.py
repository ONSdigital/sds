from firebase_admin import firestore
from google.cloud.firestore import Transaction
from models.collection_exericise_end_data import (
    CollectionExerciseEndData,
    DeleteMetadata,
)
from repositories.firebase.firebase_loader import firebase_loader


class DeletionMetadataFirebaseRepository:

    def __init__(self):
        self.client = firebase_loader.get_client()
        self.marked_for_deletion_collection = firebase_loader.deletion_collection()

    def create_delete_in_transaction(
        self,
        delete_metadata: DeleteMetadata,
    ) -> None:
        """
        Creates a new deletion entry in firestore.

        Parameters:
        delete_metadata (DeleteMetadata): The deletion metadata being added to firestore.
        """
        self.marked_for_deletion_collection.document().set(delete_metadata)

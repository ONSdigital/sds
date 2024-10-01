from models.deletion_models import DeleteMetadata
from repositories.firebase.firebase_loader import firebase_loader


class DeletionMetadataFirebaseRepository:

    def __init__(self):
        self.client = firebase_loader.get_client()
        self.deletion_collection = firebase_loader.get_deletion_collection()

    def mark_dataset_for_deletion(
        self,
        delete_metadata: DeleteMetadata,
    ) -> None:
        """
        Creates a new deletion entry in firestore.

        Parameters:
        delete_metadata (DeleteMetadata): The deletion metadata being added to firestore.
        """
        self.deletion_collection.document().set(delete_metadata)

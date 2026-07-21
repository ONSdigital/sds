from dataclasses import asdict

from app.interfaces.dataset_deletion_repository_interface import DatasetDeletionRepositoryInterface
from app.models.deletion_models import DeleteMetadata
from app.util.firebase_loader import FirebaseLoader


class FirestoreDatasetDeletionRepository(DatasetDeletionRepositoryInterface):
    def __init__(self, firebase_loader: FirebaseLoader):
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
        self.deletion_collection.document().set(asdict(delete_metadata))

from google.cloud import firestore

from app.config import settings


class FirebaseLoader:
    def __init__(self):
        self.client = self._connect_client()
        self.datasets_collection = self._set_collection("datasets")
        self.schemas_collection = self._set_collection("schemas")
        self.deletion_collection = self._set_collection("marked_for_deletion")

    def get_client(self) -> firestore.Client:
        """
        Get the firestore client
        """
        return self.client

    def get_datasets_collection(self) -> firestore.CollectionReference:
        """
        Get the datasets collection from firestore
        """
        return self.datasets_collection

    def get_schemas_collection(self) -> firestore.CollectionReference:
        """
        Get the schemas collection from firestore
        """
        return self.schemas_collection

    def get_deletion_collection(self) -> firestore.CollectionReference:
        """
        Get the marked_for_deletion collection from firestore
        """
        return self.deletion_collection

    def _connect_client(self) -> firestore.Client:
        """
        Connect to the firestore client using PROJECT_ID
        """
        if settings.CONF == "unit":
            return None
        return firestore.Client(
            project=settings.PROJECT_ID, database=settings.FIRESTORE_DB_NAME
        )

    def _set_collection(self, collection) -> firestore.CollectionReference:
        """
        Setup the collection reference for schemas and datasets
        """
        if settings.CONF == "unit":
            return None
        return self.client.collection(collection)


firebase_loader = FirebaseLoader()

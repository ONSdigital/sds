from config.config_factory import config
from google.cloud import firestore


class FirebaseLoader:
    def __init__(self):
        self.client = self._connect_client()
        self.datasets_collection = self._set_collection("datasets")
        self.schemas_collection = self._set_collection("schemas")

    def get_client(self) -> firestore.Client:
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

    def _connect_client(self) -> firestore.Client:
        """
        Connect to the firestore client using PROJECT_ID
        """
        if config.CONF == "unit":
            return None
        return firestore.Client(project=config.PROJECT_ID)

    def _set_collection(self, collection) -> firestore.CollectionReference:
        """
        Setup the collection reference for schemas and datasets
        """
        if config.CONF == "unit":
            return None
        return self.client.collection(collection)


firebase_loader = FirebaseLoader()

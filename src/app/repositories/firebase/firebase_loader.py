from config.config_factory import config
from google.cloud import firestore


class FirebaseLoader:
    def __init__(self):
        self.client = firestore.Client(project=config.PROJECT_ID)
        self.datasets_collection = self.client.collection("datasets")
        self.schemas_collection = self.client.collection("schemas")

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


firebase_loader = FirebaseLoader()

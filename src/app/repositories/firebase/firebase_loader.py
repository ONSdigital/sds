from config.config_factory import ConfigFactory
from google.cloud import firestore

config = ConfigFactory.get_config()


class FirebaseLoader:
    def __init__(self):
        self.database = None
        self.datasets_collection = None
        self.schemas_collection = None
        self._connect_db()
        self._set_collections()

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

    def _connect_db(self):
        """
        Connect to the firestore client using PROJECT_ID
        Bypassed in UnitTest environment
        """
        if config.CONF != "unit":
            self.database = firestore.Client(project=config.PROJECT_ID)

    def _set_collections(self):
        """
        Setup the collection reference for schemas and datasets
        Bypassed in UnitTest environment
        """
        if config.CONF != "unit":
            self.datasets_collection = self.database.collection("datasets")
            self.schemas_collection = self.database.collection("schemas")

from config.config_factory import ConfigFactory
from google.cloud import firestore

config = ConfigFactory.get_config()


class FirebaseLoader:
    def __init__(self):
        self.database = None
        self.datasets_collection = None
        self.schemas_collection = None

    def __get_db(self):
        if config.CONF != "unit":
            self.database = firestore.Client(project=config.PROJECT_ID)
        return self.database

    def get_datasets_collection(self):
        if config.CONF != "unit":
            self.datasets_collection = self.__get_db().collection("datasets")
        return self.datasets_collection

    def get_schemas_collection(self):
        if config.CONF != "unit":
            self.schemas_collection = self.__get_db().collection("schemas")
        return self.schemas_collection

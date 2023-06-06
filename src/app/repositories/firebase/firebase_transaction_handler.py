import exception.exceptions as exceptions
from config.config_factory import ConfigFactory
from google.cloud.firestore import Client, Transaction
from logging_config import logging

logger = logging.getLogger(__name__)
config = ConfigFactory.get_config()


class FirebaseTransactionHandler:
    def __init__(self, client: Client):
        self._client = client
        self._transaction = None

    def transaction_initiate(self) -> Transaction:
        self._transaction = self._client.transaction()
        return self._transaction

    def transaction_commit(self):
        self._transaction.commit()

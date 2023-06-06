import exception.exceptions as exceptions
from config.config_factory import ConfigFactory
from google.cloud.firestore import Client, Transaction
from logging_config import logging

logger = logging.getLogger(__name__)
config = ConfigFactory.get_config()


class FirebaseTransactionHandler:
    def __init__(self, client: Client):
        if config.CONF != "unit":
            self._transaction = client.transaction()
        else:
            self._transaction = None

    def transaction_begin(self) -> Transaction:
        if self._transaction.id is None:
            self._transaction._begin()
            return self._transaction
        else:
            logger.error(
                "Transaction is already active and re-initialising is not allowed before commit or rollback"
            )
            raise exceptions.GlobalException

    def transaction_commit(self):
        if self._transaction.id is None:
            logger.error("No active transaction to commit. Transaction ID is missing")
            raise exceptions.GlobalException
        else:
            self._transaction.commit()

    def transaction_rollback(self):
        if self._transaction.id is None:
            logger.error("No active transaction to rollback. Transaction ID is missing")
            raise exceptions.GlobalException
        else:
            self._transaction._rollback()

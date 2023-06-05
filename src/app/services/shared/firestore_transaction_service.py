from repositories.firebase.firebase_loader import firebase_loader


class FirestoreTransactionService:
    def __init__(self) -> None:
        self.transaction = firebase_loader.get_transaction()

    def commit_transaction(self) -> None:
        self.transaction.commit()

    def rollback_transaction(self) -> None:
        self.transaction._rollback()


firestore_transaction_service = FirestoreTransactionService()

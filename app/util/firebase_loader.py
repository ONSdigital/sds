from google.cloud import firestore


class FirebaseLoader:
    def __init__(self, client: firestore.Client) -> None:
        self.client = client
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

    def set_transaction(self):
        """
        Set the transaction for firestore client
        """
        return self.client.transaction()

    def _set_collection(self, collection) -> firestore.CollectionReference:
        """
        Set up the collection reference for schemas and datasets
        """
        return self.client.collection(collection)

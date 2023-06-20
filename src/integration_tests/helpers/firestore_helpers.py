import requests
from config.config_factory import config
from firebase_admin import firestore


@firestore.transactional
def perform_delete_transaction(
    transaction: firestore.Transaction, collection_ref: firestore.CollectionReference
):
    _delete_collection(transaction, collection_ref)


def _delete_collection(
    transaction: firestore.Transaction, collection_ref: firestore.CollectionReference
) -> None:
    """
    Recursively deletes the collection and its subcollections.
    Parameters:
    collection_ref (firestore.CollectionReference): the reference of the collection being deleted.
    """
    doc_collection = collection_ref.stream()

    for doc in doc_collection:
        _recursively_delete_document_and_sub_collections(transaction, doc.reference)


def _recursively_delete_document_and_sub_collections(
    transaction: firestore.Transaction,
    doc_ref: firestore.DocumentReference,
) -> None:
    """
    Loops through each collection in a document and deletes the collection.
    Parameters:
    doc_ref (firestore.DocumentReference): the reference of the document being deleted.
    """
    for collection_ref in doc_ref.collections():
        _delete_collection(transaction, collection_ref)

    transaction.delete(doc_ref)


def delete_local_firestore_data():
    """
    Method to cleanup local test data in the emulated firestore instance.

    Parameters:
        None

    Returns:
        None
    """
    requests.delete(
        f"http://localhost:8080/emulator/v1/projects/{config.PROJECT_ID}/databases/(default)/documents"
    )

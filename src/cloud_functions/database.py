import firebase_admin
from firebase_admin import firestore

firebase_admin.initialize_app()
db = firestore.client()
datasets_collection = db.collection("datasets")


def set_dataset(dataset_id, dataset):
    dataset.pop("data")
    datasets_collection.document(dataset_id).set(dataset)


def set_data(dataset_id, data):
    units_collection = datasets_collection.document(dataset_id).collection("units")
    units_collection.document(data["unit_id"]).set(data)

import firebase_admin
from firebase_admin import firestore

cred_obj = firebase_admin.credentials.Certificate("../firebase_key.json")
default_app = firebase_admin.initialize_app(cred_obj)
db = firestore.client()
data_sets_collection = db.collection("data_sets")


def set_data(data_set_id, data):
    units_collection = data_sets_collection.document(data_set_id).collection("units")
    units_collection.document(data["unit_id"]).set(data)


def get_data(data_set_id, unit_id):
    units_collection = data_sets_collection.document(data_set_id).collection("units")
    return units_collection.document(unit_id).get().to_dict()

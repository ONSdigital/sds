import os
import firebase_admin

from firebase_admin import firestore


FIRESTORE_PROJECT_ID = os.environ.get("FIRESTORE_PROJECT_ID")
FIREBASE_KEYFILE_LOCATION = os.environ.get("FIREBASE_KEYFILE_LOCATION")

credentials = firebase_admin.credentials.Certificate(FIREBASE_KEYFILE_LOCATION)

projectId = FIRESTORE_PROJECT_ID

options = {
    "projectId": projectId
}

firebase_admin.initialize_app(credentials, options)

client = firestore.client()


datasets_collection = client.collection("datasets")

schemas_collection = client.collection("schemas")


def set_data(dataset_id, data):
    units_collection = datasets_collection.document(dataset_id).collection("units")
    units_collection.document(data["unit_id"]).set(data)


def get_data(dataset_id, unit_id):
    units_collection = datasets_collection.document(dataset_id).collection("units")
    return units_collection.document(unit_id).get().to_dict()


dataset_id = "1"
unit_id = "2"
data = {
    "unit_id": unit_id
}

set_data(dataset_id, data)

data = get_data(dataset_id, unit_id)

print(data)

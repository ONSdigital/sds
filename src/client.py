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

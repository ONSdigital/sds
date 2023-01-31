import os
import firebase_admin

from firebase_admin import firestore


FIRESTORE_PROJECT_ID = os.environ.get("FIRESTORE_PROJECT_ID")


projectId = FIRESTORE_PROJECT_ID

credentials = firebase_admin.credentials.ApplicationDefault()

options = {
    'projectId': projectId
}

firebase_admin.initialize_app(credentials, options)

client = firestore.client()


print("ok!")

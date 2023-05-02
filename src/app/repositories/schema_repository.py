from dataclasses import asdict
from typing import Generator

import firebase_admin
from firebase_admin import _apps, firestore
from google.cloud.firestore_v1.document import DocumentSnapshot


class SchemaRepository:
    def __init__(self):
        if not _apps:
            firebase_admin.initialize_app()

        self.db = firestore.client()
        self.schemas_collection = self.db.collection("schemas")

    def get_current_version_survey_schema(
        self, survey_id: str
    ) -> Generator[DocumentSnapshot, None, None]:
        return (
            self.schemas_collection.where("survey_id", "==", survey_id)
            .order_by("sds_schema_version", direction=firestore.Query.DESCENDING)
            .limit(1)
            .stream()
        )

    def create_schema(self, schema_id: str, schema_metadata):
        self.schemas_collection.document(schema_id).set(asdict(schema_metadata))

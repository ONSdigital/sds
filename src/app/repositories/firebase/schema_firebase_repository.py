from dataclasses import asdict
from typing import Generator

import firebase_admin
from firebase_admin import _apps, firestore
from google.cloud.firestore_v1.document import DocumentSnapshot
from models.schema_models import SchemaMetadata, SchemaMetadataWithGuid


class SchemaFirebaseRepository:
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

    def create_schema(self, schema_id: str, schema_metadata) -> SchemaMetadataWithGuid:
        self.schemas_collection.document(schema_id).set(asdict(schema_metadata))

    def get_schema_metadata_bucket_location(self, survey_id, version) -> str:
        schemas_result = (
            self.schemas_collection.where("survey_id", "==", survey_id)
            .where("sds_schema_version", "==", int(version))
            .stream()
        )

        for schema in schemas_result:
            return SchemaMetadata(**schema.to_dict()).schema_location

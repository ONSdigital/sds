import uuid

from config.config_factory import ConfigFactory
from models.schema_models import SchemaMetadata, SchemaMetadataWithGuid
from repositories.buckets.schema_bucket_repository import SchemaBucketRepository
from repositories.firebase.schema_firebase_repository import SchemaFirebaseRepository
from services.shared.datetime_service import DatetimeService
from services.shared.document_version_service import DocumentVersionService


class SchemaProcessorService:
    def __init__(self) -> None:
        self.config = ConfigFactory.get_config()

        self.schema_firebase_repository = SchemaFirebaseRepository()
        self.schema_bucket_repository = SchemaBucketRepository()

    def process_schema_metadata(self, schema: SchemaMetadata):
        schema_id = str(uuid.uuid4())
        stored_schema_filename = f"{schema.survey_id}/{schema_id}.json"

        self.schema_bucket_repository.store_schema_json(stored_schema_filename, schema)

        next_version_schema_metadata = self.build_next_version_schema_metadata(
            schema_id, stored_schema_filename, schema
        )

        self.schema_firebase_repository.create_schema(
            schema_id, next_version_schema_metadata
        )

        return next_version_schema_metadata

    def build_next_version_schema_metadata(
        self, schema_id: str, stored_schema_filename: str, schema: SchemaMetadata
    ) -> SchemaMetadataWithGuid:
        return SchemaMetadataWithGuid(
            guid=schema_id,
            schema_location=stored_schema_filename,
            sds_schema_version=self.calculate_next_schema_version(schema),
            survey_id=schema.survey_id,
            sds_published_at=str(
                DatetimeService.get_current_date_and_time().strftime(
                    self.config.TIME_FORMAT
                )
            ),
        )

    def calculate_next_schema_version(self, schema):
        current_version_metadata = (
            self.schema_firebase_repository.get_current_version_survey_schema(
                schema.survey_id
            )
        )

        return DocumentVersionService.calculate_survey_version(
            current_version_metadata, "sds_schema_version"
        )

    def get_schema_metadata_collection_with_guid(
        self, survey_id: str
    ) -> list[SchemaMetadataWithGuid]:
        schema_metadata_collection = (
            self.schema_firebase_repository.get_schema_metadata_collection(survey_id)
        )

        schema_metadata_collection_with_guid = []
        for schema in schema_metadata_collection:
            return_schema = schema.to_dict()
            return_schema["guid"] = schema.id
            schema_metadata_collection_with_guid.append(return_schema)

        return schema_metadata_collection_with_guid

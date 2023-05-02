import uuid

import storage
from config.config_factory import ConfigFactory
from models.schema_models import SchemaMetadataWithGuid
from repositories.buckets.schema_bucket_repository import SchemaBucketRepository
from repositories.schema_repository import SchemaRepository
from services.datetime_service import DatetimeService
from services.document_version_service import DocumentVersionService

config = ConfigFactory.get_config()


class SchemaProcessorService:
    def __init__(self) -> None:
        self.schema_repository = SchemaRepository()
        self.schema_bucket_repository = SchemaBucketRepository()

    def process_schema_metadata(self, schema):
        schema_id = str(uuid.uuid4())
        stored_schema_filename = f"{schema.survey_id}/{schema_id}.json"
        self.schema_bucket_repository.store_schema_json(stored_schema_filename, schema)

        current_version_metadata = (
            self.schema_repository.get_current_version_survey_schema(schema.survey_id)
        )

        schema_metadata = SchemaMetadataWithGuid(
            guid=schema_id,
            schema_location=stored_schema_filename,
            sds_schema_version=DocumentVersionService.calculate_survey_version(
                current_version_metadata, "sds_schema_version"
            ),
            survey_id=schema.survey_id,
            sds_published_at=str(
                DatetimeService.get_current_date_and_time().strftime(config.TIME_FORMAT)
            ),
        )

        self.schema_repository.create_schema(schema_id, schema_metadata)

        return schema_metadata

import uuid

import exception.exceptions as exceptions
from config.config_factory import config
from logging_config import logging
from models.schema_models import Schema, SchemaMetadata
from repositories.buckets.schema_bucket_repository import SchemaBucketRepository
from repositories.firebase.schema_firebase_repository import SchemaFirebaseRepository
from services.shared.datetime_service import DatetimeService
from services.shared.document_version_service import DocumentVersionService
from services.shared.publisher_service import publisher_service

logger = logging.getLogger(__name__)


class SchemaProcessorService:
    def __init__(self) -> None:
        self.schema_firebase_repository = SchemaFirebaseRepository()
        self.schema_bucket_repository = SchemaBucketRepository()

    def process_raw_schema(self, schema: Schema) -> SchemaMetadata:
        """
        Processes incoming schema.

        Parameters:
        schema (Schema): incoming schema.
        """

        schema_id = str(uuid.uuid4())
        stored_schema_filename = f"{schema.survey_id}/{schema_id}.json"

        next_version_schema_metadata = self.build_next_version_schema_metadata(
            schema_id, stored_schema_filename, schema
        )

        self.process_raw_schema_in_transaction(
            schema_id, next_version_schema_metadata, schema, stored_schema_filename
        )

        self.try_publish_schema_metadata_to_topic(
            next_version_schema_metadata
        )

        return next_version_schema_metadata

    def process_raw_schema_in_transaction(
        self,
        schema_id: str,
        next_version_schema_metadata: SchemaMetadata,
        schema: Schema,
        stored_schema_filename: str,
    ):
        """
        Process the new schema by calling a transactional function that wrap the procedures
        Commit if the function is sucessful, rolling back otherwise.

        Parameters:
        schema_id (str): The unique id of the new schema.
        next_version_schema_metadata (SchemaMetadata): The schema metadata being added to firestore.
        schema (Schema): The schema being stored.
        stored_schema_filename (str): Filename of uploaded json schema.
        """
        try:
            logger.info("Beginning schema transaction...")
            self.schema_firebase_repository.perform_new_schema_transaction(
                schema_id, next_version_schema_metadata, schema, stored_schema_filename
            )

            logger.info("Schema transaction committed successfully.")
            return next_version_schema_metadata
        except Exception as e:
            logger.error(f"Performing schema transaction: exception raised: {e}")
            logger.error("Rolling back schema transaction")
            raise exceptions.GlobalException

    def build_next_version_schema_metadata(
        self,
        schema_id: str,
        stored_schema_filename: str,
        schema: Schema,
    ) -> SchemaMetadata:
        """
        Builds the next version of schema metadata being processed.

        Parameters:
        schema_id (str): the schema id of the metadata.
        stored_schema_filename (str): the filename of schema when it is stored.
        schema_metadata (SchemaMetadata): schema metadata being processed.
        """
        return SchemaMetadata(
            guid=schema_id,
            schema_location=stored_schema_filename,
            sds_schema_version=self.calculate_next_schema_version(schema),
            survey_id=schema.survey_id,
            sds_published_at=str(
                DatetimeService.get_current_date_and_time().strftime(config.TIME_FORMAT)
            ),
        )

    def calculate_next_schema_version(self, schema: Schema):
        """
        Calculates the next schema version for the metadata being built.

        Parameters:
        schema_metadata (SchemaMetadata): schema metadata being processed.
        """

        current_version_metadata = (
            self.schema_firebase_repository.get_latest_schema_with_survey_id(
                schema.survey_id
            )
        )

        return DocumentVersionService.calculate_survey_version(
            current_version_metadata, "sds_schema_version"
        )

    def get_schema_metadata_collection_with_guid(
        self, survey_id: str
    ) -> list[SchemaMetadata]:
        """
        Gets the collection of schema metadata associated with a specific survey id from firestore.

        Parameters:
        survey_id (str): the survey id of the schema metadata.
        """

        schema_metadata_collection = (
            self.schema_firebase_repository.get_schema_metadata_collection(survey_id)
        )

        schema_metadata_collection_with_guid = []
        for schema in schema_metadata_collection:
            return_schema = schema.to_dict()
            return_schema["guid"] = schema.id
            schema_metadata_collection_with_guid.append(return_schema)

        return schema_metadata_collection_with_guid

    def get_schema_bucket_filename(self, survey_id: str, version: str) -> str:
        """
        Gets the filename of the schema in bucket. If version is omitted,
        the latest schema filename is retrieved
        """
        if version is None:
            return self.schema_firebase_repository.get_latest_schema_bucket_filename(
                survey_id
            )
        else:
            return self.schema_firebase_repository.get_schema_bucket_filename(
                survey_id, version
            )

    def try_publish_schema_metadata_to_topic(self, next_version_schema_metadata: SchemaMetadata) -> None:
        try:
            logger.info("Publishing schema metadata to topic...")
            publisher_service.publish_schema_data_to_topic(
                next_version_schema_metadata,
                config.SCHEMA_TOPIC_ID,
            )
            logger.debug(
                f"Schema metadata {next_version_schema_metadata} published to topic {config.SCHEMA_TOPIC_ID}"
            )
            logger.info("Schema metadata published successfully.")
        except Exception as e:
            logger.debug(
                f"Schema metadata {next_version_schema_metadata} failed to publish to topic {config.SCHEMA_TOPIC_ID} with error {e}"
            )
            logger.error("Error publishing schema metadata to topic.")
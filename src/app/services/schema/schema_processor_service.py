import uuid

import exception.exceptions as exceptions
from config.config_factory import config
from logging_config import logging
from models.schema_models import SchemaMetadata
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

    def process_raw_schema(self, schema: dict, survey_id: str) -> SchemaMetadata:
        """
        Processes incoming schema.

        Parameters:
        schema (dict): incoming schema.
        """

        schema_id = str(uuid.uuid4())
        stored_schema_filename = f"{survey_id}/{schema_id}.json"

        next_version_schema_metadata = self.build_next_version_schema_metadata(
            schema_id, stored_schema_filename, schema, survey_id
        )

        self.process_raw_schema_in_transaction(
            schema_id, next_version_schema_metadata, schema, stored_schema_filename
        )

        self.try_publish_schema_metadata_to_topic(next_version_schema_metadata)

        return next_version_schema_metadata

    def process_raw_schema_in_transaction(
        self,
        schema_id: str,
        next_version_schema_metadata: SchemaMetadata,
        schema: dict,
        stored_schema_filename: str,
    ):
        """
        Process the new schema by calling a transactional function that wrap the procedures
        Commit if the function is sucessful, rolling back otherwise.

        Parameters:
        schema_id (str): The unique id of the new schema.
        next_version_schema_metadata (SchemaMetadata): The schema metadata being added to firestore.
        schema (dict): The schema being stored.
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
        schema: dict,
        survey_id: str,
    ) -> SchemaMetadata:
        """
        Builds the next version of schema metadata being processed.

        Parameters:
        schema_id (str): the guid of the metadata.
        stored_schema_filename (str): the filename of schema when it is stored.
        schema (dict): schema being processed.
        survey_id (str): the survey id of the schema.
        """
        next_version_schema_metadata = {
            "guid": schema_id,
            "schema_location": stored_schema_filename,
            "sds_schema_version": self.calculate_next_schema_version(survey_id),
            "survey_id": survey_id,
            "sds_published_at": str(
                DatetimeService.get_current_date_and_time().strftime(config.TIME_FORMAT)
            ),
            "schema_version": self.get_schema_version_from_properties(schema),
        }
        return next_version_schema_metadata

    def calculate_next_schema_version(self, survey_id: str) -> int:
        """
        Calculates the next schema version for the metadata being built.

        Parameters:
        survey_id (str): the survey id of the schema.
        """

        current_version_metadata = (
            self.schema_firebase_repository.get_latest_schema_metadata_with_survey_id(
                survey_id
            )
        )

        return DocumentVersionService.calculate_survey_version(
            current_version_metadata, "sds_schema_version"
        )

    def get_schema_version_from_properties(self, schema: dict) -> str:
        """
        Get schema version from the properties object of the schema.

        Parameters:
        schema (dict); schema being processed.
        """

        level_keys = ["properties", "schema_version", "const"]
        return self.get_child_property(schema, level_keys)

    def get_child_property(self, nested_dict: dict, keys: list) -> str:
        """
        Get a child property from a nested dictionary

        Paramenters:
        nested_dict (dict): A nested dictionary that is being fetched
        keys (list): A list of keys within the nested dictionary that lead to the child property
        """
        field = nested_dict

        for key in keys:
            field = field[key]
        else:
            result = field

        return result

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

        return schema_metadata_collection

    def get_schema_bucket_filename(self, survey_id: str, version: str) -> str:
        """
        Gets the filename of the schema in bucket. If version is omitted,
        the latest schema filename is retrieved

        Parameters:
        survey_id (str): the survey id of the schema
        version (str): the sds schema version of the schema
        """
        if version is None:
            return self.schema_firebase_repository.get_latest_schema_bucket_filename(
                survey_id
            )
        else:
            return self.schema_firebase_repository.get_schema_bucket_filename(
                survey_id, version
            )

    def get_schema_bucket_filename_from_guid(self, guid: str) -> str:
        """
        Gets the filename of the schema in bucket from guid

        Parameters:
        guid (str): the guid of the schema
        """
        return self.schema_firebase_repository.get_schema_bucket_filename_with_guid(
            guid
        )

    def try_publish_schema_metadata_to_topic(
        self, next_version_schema_metadata: SchemaMetadata
    ) -> None:
        """
        Publish schema metadata to pubsub topic

        Parameters:
        next_version_schema_metadata (SchemaMetadata): the schema metadata of the newly published schema
        """
        try:
            logger.info("Publishing schema metadata to topic...")
            publisher_service.publish_data_to_topic(
                next_version_schema_metadata,
                config.PUBLISH_SCHEMA_TOPIC_ID,
            )
            logger.debug(
                f"Schema metadata {next_version_schema_metadata} published to topic {config.PUBLISH_SCHEMA_TOPIC_ID}"
            )
            logger.info("Schema metadata published successfully.")
        except Exception as e:
            logger.debug(
                f"Schema metadata {next_version_schema_metadata} failed to publish to topic "
                f"{config.PUBLISH_SCHEMA_TOPIC_ID} with error {e}"
            )
            logger.error("Error publishing schema metadata to topic.")
            raise exceptions.GlobalException

    def get_list_survey_id(self) -> list[str]:
        """ """
        list_survey_id = self.schema_firebase_repository.get_list_survey_id()

        return list_survey_id

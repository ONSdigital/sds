from firebase_admin import firestore
from google.cloud.firestore import Transaction
from models.schema_models import SchemaMetadata
from repositories.buckets.schema_bucket_repository import SchemaBucketRepository
from repositories.firebase.firebase_loader import firebase_loader


class SchemaFirebaseRepository:
    def __init__(self):
        self.client = firebase_loader.get_client()
        self.schemas_collection = firebase_loader.get_schemas_collection()
        self.schema_bucket_repository = SchemaBucketRepository()

    def get_latest_schema_metadata_with_survey_id(
        self, survey_id: str
    ) -> SchemaMetadata | None:
        """
        Gets a stream of the most up to date schema metadata in firestore with a specific survey id.

        Parameters:
        survey_id (str): The survey id of the dataset.
        """
        latest_schema = (
            self.schemas_collection.where("survey_id", "==", survey_id)
            .order_by("sds_schema_version", direction=firestore.Query.DESCENDING)
            .limit(1)
            .stream()
        )

        schema_metadata: SchemaMetadata = None
        for returned_schema in latest_schema:
            schema_metadata: SchemaMetadata = {**returned_schema.to_dict()}

        return schema_metadata

    def perform_new_schema_transaction(
        self,
        schema_id: str,
        next_version_schema_metadata: SchemaMetadata,
        schema: dict,
        stored_schema_filename: str,
    ) -> None:
        """
        A transactional function that wrap schema creation and schema storage processes

        Parameters:
        schema_id (str): The unique id of the new schema.
        next_version_schema_metadata (SchemaMetadata): The schema metadata being added to firestore.
        schema (dict): The schema being stored.
        stored_schema_filename (str): Filename of uploaded json schema.
        """

        # A stipulation of the @firestore.transactional decorator is the first parameter HAS
        # to be 'transaction', but since we're using classes the first parameter is always
        # 'self'. Encapsulating the transaction within this function circumvents the issue.
        @firestore.transactional
        def post_schema_transaction_run(transaction: Transaction):
            self.create_schema_in_transaction(
                transaction, schema_id, next_version_schema_metadata
            )
            self.schema_bucket_repository.store_schema_json(
                stored_schema_filename, schema
            )

        post_schema_transaction_run(self.client.transaction())

    def create_schema_in_transaction(
        self,
        transaction: Transaction,
        schema_id: str,
        schema_metadata: SchemaMetadata,
    ) -> None:
        """
        Creates a new schema metadata entry in firestore.

        Parameters:
        schema_id (str): The unique id of the new schema.
        schema_metadata (SchemaMetadata): The schema metadata being added to firestore.
        """
        transaction.set(
            self.schemas_collection.document(schema_id),
            schema_metadata,
            merge=True,
        )

    def get_schema_bucket_filename(self, survey_id: str, version: str) -> str:
        """
        Gets the filename of schema with a specific survey id and version. Should only ever return one entry.

        Parameters:
        survey_id (str): The survey id of the survey being queried.
        version (str): The version of the survey being queried
        """
        schemas_result = (
            self.schemas_collection.where("survey_id", "==", survey_id)
            .where("sds_schema_version", "==", int(version))
            .stream()
        )

        for schema in schemas_result:
            return schema.to_dict()["schema_location"]

    def get_latest_schema_bucket_filename(self, survey_id: str) -> str:
        """
        Gets the filename of the latest version schema of a specific survey id. Should only ever return one entry.

        Parameters:
        survey_id (str): The survey id of the survey being queried.
        """
        schemas_result = (
            self.schemas_collection.where("survey_id", "==", survey_id)
            .order_by("sds_schema_version", direction=firestore.Query.DESCENDING)
            .limit(1)
            .stream()
        )

        for schema in schemas_result:
            return schema.to_dict()["schema_location"]

    def get_schema_bucket_filename_with_guid(self, guid: str) -> str:
        """
        Gets the filename of the schema of a specific guid. Should only ever return one entry.

        Parameters:
        guid (str): The guid of the survey being queried.
        """
        schemas_result = self.schemas_collection.where("guid", "==", guid).stream()

        for schema in schemas_result:
            return schema.to_dict()["schema_location"]

    def get_schema_metadata_collection(self, survey_id: str) -> list[SchemaMetadata]:
        """
        Gets the collection of schema metadata with a specific survey id.

        Parameters:
        survey_id (str): The survey id of the schema metadata being collected.
        """
        returned_schema_metadata = (
            self.schemas_collection.where("survey_id", "==", survey_id)
            .order_by("sds_schema_version", direction=firestore.Query.DESCENDING)
            .stream()
        )

        schema_metadata_list: list[SchemaMetadata] = []
        for schema_metadata in returned_schema_metadata:
            metadata: SchemaMetadata = {**(schema_metadata.to_dict())}
            schema_metadata_list.append(metadata)

        return schema_metadata_list

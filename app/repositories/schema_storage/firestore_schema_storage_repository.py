import json

from google.cloud import firestore
from google.cloud.firestore import Transaction

from app.interfaces.schema_storage_repository_interface import SchemaStorageRepositoryInterface
from app.models.schema_models import SchemaMetadata, SchemaModel
from app.util.firebase_loader import FirebaseLoader


class SchemaFirebaseRepository(SchemaStorageRepositoryInterface):

    def __init__(self, firebase_loader: FirebaseLoader) -> None:
        self.firestore = firebase_loader
        self.schemas_collection = firebase_loader.get_schemas_collection()

    def get_latest_schema_metadata(
        self, survey_id: str
    ) -> SchemaMetadata | None:
        """
        Gets a stream of the most up-to-date schema metadata in firestore with a specific survey id.

        Parameters:
        survey_id (str): The survey id of the dataset.
        """
        latest_schema = (
            self.schemas_collection.where("survey_id", "==", survey_id)
            .order_by("sds_schema_version", direction=firestore.Query.DESCENDING)
            .limit(1)
            .stream()
        )

        schema_metadata: SchemaMetadata

        schema_found = next(latest_schema, None)
        if schema_found is None:
            return None
        else:
            schema_metadata: SchemaMetadata = SchemaMetadata(**schema_found.to_dict())

            return schema_metadata

    def perform_new_schema_transaction(
        self,
        schema_id: str,
        next_version_schema_metadata: SchemaMetadata,
        schema_model: SchemaModel,
    ) -> None:
        """
        A transactional function that wrap schema creation and schema storage processes

        Parameters:
        schema_id (str): The unique id of the new schema.
        next_version_schema_metadata (SchemaMetadata): The schema metadata being added to firestore.
        schema (dict): The schema being stored.
        stored_schema_filename (str): Filename of uploaded json schema.
        """

        # TODO make this private and refactor external usages

        # A stipulation of the @firestore.transactional decorator is the first parameter HAS
        # to be 'transaction', but since we're using classes the first parameter is always
        # 'self'. Encapsulating the transaction within this function circumvents the issue.
        @firestore.transactional
        def post_schema_transaction_run(transaction: Transaction):
            self.create_schema_metadata_in_transaction(
                transaction, schema_id, next_version_schema_metadata
            )
            self.create_schema_in_transaction(
                transaction, schema_id, schema_model
            )

        post_schema_transaction_run(self.firestore.set_transaction())

    def create_schema_metadata_in_transaction(
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
            schema_metadata.__dict__,
            merge=True,
        )

    def create_schema_in_transaction(
        self,
        transaction: Transaction,
        schema_id: str,
        schema_model: SchemaModel,
    ) -> None:
        """
        Creates a new schema metadata entry in firestore.

        Parameters:
        schema_id (str): The unique id of the new schema.
        """
        transaction.set(
            self.schemas_collection.document(schema_id).collection("schema").document(schema_id),
            schema_model.__dict__,
            merge=True,
        )

    def get_metadata(self, survey_id: str) -> list[SchemaMetadata]:
        returned_schema_metadata = (
            self.schemas_collection.where("survey_id", "==", survey_id)
            .order_by("sds_schema_version", direction=firestore.Query.DESCENDING)
            .stream()
        )

        schema_metadata_list: list[SchemaMetadata] = []
        for schema_metadata in returned_schema_metadata:
            metadata = SchemaMetadata(**schema_metadata.to_dict())
            schema_metadata_list.append(metadata)

        return schema_metadata_list

    def get_all_metadata(self) -> list[SchemaMetadata]:
        returned_schema_metadata = (
            self.schemas_collection
            .order_by("survey_id")
            .order_by("sds_schema_version", direction=firestore.Query.DESCENDING)
            .stream()
        )

        schema_metadata_list: list[SchemaMetadata] = []
        for schema_metadata in returned_schema_metadata:
            metadata: SchemaMetadata = SchemaMetadata(**schema_metadata.to_dict())
            schema_metadata_list.append(metadata)

        return schema_metadata_list

    def get_schema_from_guid(self, guid: str) -> dict | None:
        returned_schema = self.schemas_collection.document(guid).collection("schema").document(guid).get()

        if not returned_schema.exists:
            return None

        return json.loads(returned_schema.to_dict()["schema"])

    def get_latest_guid(self, survey_id: str) -> str | None:
        schemas_result = (
            self.schemas_collection.where("survey_id", "==", survey_id)
            .order_by("sds_schema_version", direction=firestore.Query.DESCENDING)
            .limit(1)
            .stream()
        )

        schema_found = next(schemas_result, None)
        if schema_found is None:
            return None
        else:
            return schema_found.to_dict()["guid"]

    def get_guid(self, survey_id: str, version: str) -> str | None:
        schemas_result = (
            self.schemas_collection.where("survey_id", "==", survey_id)
            .where("sds_schema_version", "==", int(version))
            .stream()
        )

        schema_found = next(schemas_result, None)
        if schema_found is None:
            return None
        else:
            return schema_found.to_dict()["guid"]


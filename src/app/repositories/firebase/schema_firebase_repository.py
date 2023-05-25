from dataclasses import asdict
from typing import Generator

from firebase_admin import firestore
from google.cloud.firestore_v1.document import DocumentSnapshot
from models.schema_models import SchemaMetadata, SchemaMetadataWithoutGuid
from repositories.firebase.firebase_loader import FirebaseLoader


class SchemaFirebaseRepository:
    def __init__(self):
        firebase_loader = FirebaseLoader()
        self.schemas_collection = firebase_loader.get_schemas_collection()

    def get_latest_schema_with_survey_id(
        self, survey_id: str
    ) -> Generator[DocumentSnapshot, None, None]:
        """
        Gets a stream of the most up to date schema in firestore with a specific survey id.

        Parameters:
        survey_id (str): The survey id of the dataset.
        """

        return (
            self.schemas_collection.where("survey_id", "==", survey_id)
            .order_by("sds_schema_version", direction=firestore.Query.DESCENDING)
            .limit(1)
            .stream()
        )

    def create_schema(
        self, schema_id: str, schema_metadata: SchemaMetadataWithoutGuid
    ) -> SchemaMetadata:
        """
        Creates a new schema metadata entry in firestore.

        Parameters:
        schema_id (str): The unique id of the new schema.
        schema_metadata (SchemaMetadata): The schema metadata being added to firestore.
        """

        self.schemas_collection.document(schema_id).set(asdict(schema_metadata))

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

    def get_schema_metadata_collection(
        self, survey_id: str
    ) -> Generator[DocumentSnapshot, None, None]:
        """
        Gets the collection of schema metadata with a specific survey id.

        Parameters:
        survey_id (str): The survey id of the schema metadata being collected.
        """

        return self.schemas_collection.where("survey_id", "==", survey_id).stream()

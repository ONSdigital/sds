from abc import ABC, abstractmethod

from app.models.schema_models import SchemaMetadata, SchemaModel


class SchemaStorageRepositoryInterface(ABC):
    """
    This interface defines where schemas are
    stored
    """

    @abstractmethod
    def get_latest_schema_metadata(
            self,
            survey_id: str
    ) -> SchemaMetadata | None:
        """
        Get the latest schema metadata for a specific survey

        :param survey_id: The id of the dataset survey
        """
        raise NotImplementedError

    @abstractmethod
    def get_latest_guid(
            self,
            survey_id: str,
    ) -> str | None:
        """
        Get the guid of a schema with a specific survey and latest version

        :param survey_id: The survey id of the survey being queried.
        """
        raise NotImplementedError

    @abstractmethod
    def get_guid(
            self,
            survey_id: str,
            version: int
    ) -> str | None:
        """
        Get the guid of a schema with a specific survey id and version

        :param survey_id: The survey id of the survey being queried.
        :param version: The version of the survey being queried
        """
        raise NotImplementedError

    @abstractmethod
    def get_metadata(
            self,
            survey_id: str
    ) -> list[SchemaMetadata]:
        """
        Gets the collection of schema metadata with a specific survey id.

        :param survey_id: The survey id of the survey being queried.
        """
        raise NotImplementedError

    @abstractmethod
    def get_all_metadata(
            self,
    ) -> list[SchemaMetadata]:
        """
        Gets the collection of schema metadata for all surveys.
        """
        raise NotImplementedError

    @abstractmethod
    def get_schema_from_guid(
            self,
            guid: str
    ) -> dict | None:
        """
        Gets the schema of a specific guid from the sub-collection.
        Should only ever return one entry.

        :param guid: The guid of the schema being queried.
        """
        raise NotImplementedError

    @abstractmethod
    def store_schema(
            self,
            schema_id: str,
            schema_metadata: SchemaMetadata,
            schema_model: SchemaModel,
    ):
        """
        Store the schema in storage

        :param schema_id: The id of the schema to be stored
        :param schema_metadata: The metadata of the schema to be added
        :param schema_model: The schema being stored.
        """
        raise NotImplementedError

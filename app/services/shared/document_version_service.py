from typing import Literal

from app.models.dataset_models import DatasetMetadataWithoutId
from app.models.schema_models import SchemaMetadata


class DocumentVersionService:
    @staticmethod
    def calculate_survey_version(
        metadata: SchemaMetadata | DatasetMetadataWithoutId | None,
        version_key: Literal["sds_dataset_version", "sds_schema_version"],
    ) -> int:
        """
        Calculates the next version number of a document based on a version key, returning 1 by default if no document exists.

        Parameters:
        document_current_version: document that the version is being calculated from
        version_key: the key being accessed to find out the document version.
        """
        if metadata is None:
            return 1

        metadata_dict = metadata.__dict__

        if version_key not in metadata_dict:
            raise RuntimeError("Document must contain version key")

        return metadata_dict[version_key] + 1

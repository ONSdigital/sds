from typing import Literal

from models.dataset_models import UnitDataset
from models.schema_models import Schema


class DocumentVersionService:
    @staticmethod
    def calculate_survey_version(
        document_current_version: Schema | UnitDataset,
        version_key: Literal["sds_dataset_version", "sds_schema_version"],
    ) -> int:
        """
        Calculates the next version number of a document based on a version key, returning 1 by default if no document exists.

        Parameters:
        document_current_version: document that the version is being calculated form
        version_key: the key being accessed to find out the document version.
        """
        if document_current_version is None:
            return 1

        if version_key not in document_current_version:
            raise RuntimeError("Document must contain version key")

        return document_current_version[version_key] + 1

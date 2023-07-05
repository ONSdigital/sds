from models.dataset_models import UnitDataset
from models.schema_models import Schema


class DocumentVersionService:
    @staticmethod
    def calculate_survey_version(
        document_current_version: Schema | UnitDataset,
        version_key: str,
    ) -> int:
        """
        Calculates the next version number of a document based on a version key, returning 1 by default if no document exists.

        Parameters:
        version_key (str): the key being accessed to find out the document version.
        """
        if document_current_version is None:
            return 1

        return document_current_version[version_key] + 1

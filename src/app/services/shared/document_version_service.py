from typing import Generator

from google.cloud.firestore_v1.document import DocumentSnapshot


class DocumentVersionService:
    @staticmethod
    def calculate_survey_version(
        document_current_version: Generator[DocumentSnapshot, None, None],
        version_key: str,
    ) -> int:
        """
        Calculates the next version number of a document based on a version key, returning 1 by default if no document exists.

        Parameters:
        version_key (str): the key being accessed to find out the document version.
        """
        try:
            latest_version = next(document_current_version).to_dict()[version_key] + 1
        except StopIteration:
            latest_version = 1

        return latest_version

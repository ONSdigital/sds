from typing import Generator
from unittest.mock import MagicMock

from google.cloud.firestore_v1.document import DocumentSnapshot


class TestHelper:
    @staticmethod
    def create_document_snapshot_generator_mock(
        yield_data_collection,
    ) -> Generator[DocumentSnapshot, None, None]:
        """
        When firestore data is streamed via their SDK, it returns a generator of a DocumentSnapshot. This helper function
        simulates the functionality of the generator to be used in tests.
        """

        id_count = 0
        for data in yield_data_collection:
            generator_wrapper = MagicMock(spec=DocumentSnapshot)
            generator_wrapper.id = f"id_{id_count}"
            id_count += 1
            generator_wrapper.to_dict.return_value = data

            yield generator_wrapper

from typing import Any

def setup_mock_data(
        mock_collection: Any,
        mock_data: dict,
        mock_guid: str,
        sub_collection_name: str = None,
        sub_collection_data: dict = None,
        sub_collection_guid: str = None,
):
    """
    Sets up the mock collection to return the provided data when queried.
    If a sub_collection_name is provided, it will set up the mock collection to return a sub-collection with the provided data.
    """
    mock_collection.document(mock_guid).set(mock_data)

    if sub_collection_name:
        (mock_collection.document(mock_guid).collection(sub_collection_name).document(sub_collection_guid)
         .set(sub_collection_data))

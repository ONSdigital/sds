from mockfirestore import CollectionReference as MockCollectionReference

def setup_mock_data(
        mock_collection: MockCollectionReference,
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


def query_collection_with_test_survey_id(
        mock_collection: MockCollectionReference,
        test_survey_id: str
) -> list[dict] | None:
    """
    Queries the collection for documents of a test survey id

    Parameters:
    mock_collection (MockCollectionReference): the reference of the collection being queried.
    test_survey_id (str): the survey id to query for.

    Returns:
    list[dict]: a list of dictionary data that match the query.
    """

    # \uf8ff is a unicode character that is greater than any other character
    doc_collection = (
            mock_collection.where('survey_id', '==', test_survey_id)
                    .stream()
    )

    doc_dict: list[dict] = []
    for doc in doc_collection:
        doc_dict.append(doc.to_dict())

    return doc_dict

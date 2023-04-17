import database

from models import NewDatasetWithMetadata


def get_dataset_with_survey_id(survey_id: str) -> NewDatasetWithMetadata:
    """
    Returns a dataset associated with a specific survey id.

    Parameters:
    survey_id (str): survey_id used for query match
    """
    return database.get_dataset_with_survey_id(survey_id)

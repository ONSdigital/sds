from datetime import datetime

import database


def calculate_next_dataset_version(survey_id: str) -> int:
    """
    Calculates the latest sds_dataset_version from a single dataset from firestore with a specific survey_id.

    Parameters:
    survey_id (str): survey_id of the specified dataset.
    """
    datasets_result = database.get_dataset_with_survey_id(survey_id)
    try:
        latest_version = next(datasets_result).to_dict()["sds_dataset_version"] + 1
    except StopIteration:
        latest_version = 1

    return latest_version


def transform_dataset(dataset, filename, dataset_data):
    """
    Returns a copy of the dataset with added metadata.

    Parameters:
    dataset (str): the original dataset.
    filename (str): the filename of the json containing the dataset data
    dataset_data (str): unit
    """

    return {
        **dataset,
        "filename": filename,
        "sds_published_at": str(datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")),
        "total_reporting_units": len(dataset_data),
        "sds_dataset_version": calculate_next_dataset_version(dataset["survey_id"]),
    }


def process_new_dataset(dataset_id, filename, dataset):
    dataset_unit_data_collection = dataset.pop("data")

    transformed_dataset = transform_dataset(dataset, filename, dataset_unit_data_collection)

    database.create_new_dataset(dataset_id, transformed_dataset)

    database_unit_data_collection = database.get_dataset_unit_collection(dataset_id)

    for unit_data in dataset_unit_data_collection:
        database.append_unit_to_dataset_units_collection(database_unit_data_collection, unit_data)
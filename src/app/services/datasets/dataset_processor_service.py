import uuid
from datetime import datetime

from models import NewDatasetMetadata, NewDatasetWithMetadata
from services.datasets import dataset_reader_service, dataset_writer_service


def process_new_dataset(
    filename: str, dataset: NewDatasetWithMetadata
) -> None:
    """
    Processes the incoming dataset.

    Parameters:
    dataset_id (str): the original dataset.
    filename (str): the filename of the json containing the dataset data
    dataset (NewDatasetWithMetadata): dataset to be processed
    """

    dataset_unit_data_collection = dataset.pop("data")

    transformed_dataset = transform_dataset_metadata(
        dataset, filename, dataset_unit_data_collection
    )

    dataset_writer_service.write_transformed_dataset_to_database(
        str(uuid.uuid4()), transformed_dataset, dataset_unit_data_collection
    )


def transform_dataset_metadata(
    dataset: NewDatasetMetadata,
    filename: str,
    dataset_unit_data_collection: list[object],
):
    """
    Returns a copy of the dataset with added metadata.

    Parameters:
    dataset (NewDatasetMetadata): the original dataset.
    filename (str): the filename of the json containing the dataset data
    dataset_data (list[object]): unit
    """

    return {
        **dataset,
        "filename": filename,
        "sds_published_at": str(datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")),
        "total_reporting_units": len(dataset_unit_data_collection),
        "sds_dataset_version": calculate_next_dataset_version(dataset["survey_id"]),
    }


def calculate_next_dataset_version(survey_id: str) -> int:
    """
    Calculates the next sds_dataset_version from a single dataset from firestore with a specific survey_id.

    Parameters:
    survey_id (str): survey_id of the specified dataset.
    """
    datasets_result = dataset_reader_service.get_dataset_with_survey_id(survey_id)

    return (
        next(datasets_result).to_dict().get("sds_dataset_version", 0) + 1
        if datasets_result
        else 1
    )

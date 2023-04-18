import uuid

import database
from models import DatasetMetadataDto


def write_transformed_dataset_to_database(
    transformed_dataset: DatasetMetadataDto, dataset_unit_data_collection: list[object]
) -> None:
    """
    Writes the transformed data to the database

    Parameters:
    transformed_dataset (DatasetMetadataDto): the transformed dataset being written
    dataset_unit_data_collection (list[object]): the collection of unit data associated with the dataset
    """
    dataset_id = str(uuid.uuid4())
    database.create_new_dataset(dataset_id, transformed_dataset)
    write_new_unit_data_to_database(dataset_id, dataset_unit_data_collection)


def write_new_unit_data_to_database(
    dataset_id: str, dataset_unit_data_collection: list[object]
) -> None:
    """
    Writes the new unit data to the database

    Parameters:
    dataset_id (str): the uniquely generated id of the dataset
    dataset_unit_data_collection (list[object]): the collection of unit data associated with the dataset
    """
    database_unit_data_collection = database.get_dataset_unit_collection(dataset_id)
    for unit_data in dataset_unit_data_collection:
        database.append_unit_to_dataset_units_collection(
            database_unit_data_collection, unit_data
        )

import database


def write_transformed_dataset_to_database(
    dataset_id, transformed_dataset, dataset_unit_data_collection
):
    database.create_new_dataset(dataset_id, transformed_dataset)
    write_new_unit_data_to_database(dataset_id, dataset_unit_data_collection)


def write_new_unit_data_to_database(dataset_id, dataset_unit_data_collection):
    database_unit_data_collection = database.get_dataset_unit_collection(dataset_id)
    for unit_data in dataset_unit_data_collection:
        database.append_unit_to_dataset_units_collection(
            database_unit_data_collection, unit_data
        )

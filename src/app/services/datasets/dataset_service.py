from datetime import datetime

import database


def get_latest_version(survey_id):
    datasets_result = database.get_dataset_with_survey_id(survey_id)
    try:
        latest_version = next(datasets_result).to_dict()["sds_dataset_version"] + 1
    except StopIteration:
        latest_version = 1

    return latest_version


def process_new_dataset(dataset_id, filename, dataset):
    dataset_data = dataset.pop("data")

    dataset["filename"] = filename
    dataset["sds_published_at"] = str(datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"))
    dataset["total_reporting_units"] = len(dataset_data)
    dataset["sds_published_at"] = str(datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"))
    dataset["sds_dataset_version"] = get_latest_version(dataset["survey_id"])
    dataset["total_reporting_units"] = len(dataset_data)

    database.create_new_dataset(dataset_id, dataset)
    units_collection = database.get_dataset_unit_collection(dataset_id)

    for unit_data in dataset_data:
        database.append_unit_to_dataset_units_collection(units_collection, unit_data)

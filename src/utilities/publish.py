import uuid

from datetime import datetime


def get_dataset_id():
    dataset_id = str(uuid.uuid4())

    return dataset_id


def get_datetime_published():
    datetime_published = str(datetime.now())

    return datetime_published
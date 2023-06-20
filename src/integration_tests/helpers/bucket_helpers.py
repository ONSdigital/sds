import shutil
from pathlib import Path

from repositories.buckets.bucket_loader import bucket_loader


def delete_local_bucket_data(filepath: str):
    """
    Method to cleanup local test data in the bucket instance.

    Parameters:
        filepath: the filepath for the bucket instance to be deleted

    Returns:
        None
    """
    path_instance = Path(filepath)
    if Path.is_dir(path_instance):
        shutil.rmtree(path_instance)


def delete_blobs(bucket) -> None:
    """
    Method to delete all blobs in the specified bucket.

    Parameters:
        bucket: the bucket to clean

    Returns:
        None
    """
    blobs = bucket.list_blobs()

    for blob in blobs:
        blob.delete()


def get_dataset_bucket():
    return bucket_loader.get_dataset_bucket()
import database
import dataset_storage
import functions_framework


@functions_framework.cloud_event
def new_dataset(cloud_event):
    """
    Triggered by uploading a new dataset file to the
    dataset storage bucket. See the 'Cloud Functions' section
    in the README.md file for details as to how this function
    is set up.
    """
    data = cloud_event.data

    bucket_name = data["bucket"]
    filename = data["name"]

    dataset_id = filename.split(".json")[0]

    dataset = dataset_storage.get_dataset(filename=filename, bucket_name=bucket_name)
    database.set_dataset(dataset_id=dataset_id, dataset=dataset)

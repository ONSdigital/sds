import database
import dataset_storage
import functions_framework


# Triggered by a change in a storage bucket
@functions_framework.cloud_event
def new_dataset(cloud_event):
    data = cloud_event.data

    event_id = cloud_event["id"]
    event_type = cloud_event["type"]

    bucket_name = data["bucket"]
    filename = data["name"]
    metageneration = data["metageneration"]
    time_created = data["timeCreated"]
    updated = data["updated"]

    print(f"Event ID: {event_id}")
    print(f"Event type: {event_type}")
    print(f"Bucket: {bucket_name}")
    print(f"File: {filename}")
    print(f"Metageneration: {metageneration}")
    print(f"Created: {time_created}")
    print(f"Updated: {updated}")
    dataset_id = filename.split(".json")[0]
    print(f"dataset_id: {dataset_id}")

    dataset = dataset_storage.get_dataset(filename=filename, bucket_name=bucket_name)
    database.set_dataset(dataset_id=dataset_id, dataset=dataset)

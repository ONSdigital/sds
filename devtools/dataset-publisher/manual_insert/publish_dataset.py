import json
import os

from google.cloud import storage

storage_client = storage.Client()

if os.environ.get("DATASET_BUCKET_NAME"):
    bucket = storage_client.bucket(os.environ.get("DATASET_BUCKET_NAME"))
    if not bucket.exists():
        bucket = storage_client.create_bucket(os.environ.get("DATASET_BUCKET_NAME"))
elif os.environ.get("STORAGE_EMULATOR_HOST"):
    bucket = storage_client.create_bucket("dataset_bucket")
else:
    raise Exception("You need to set DATASET_BUCKET_NAME")


def store_schema(data):

    filename = f"{data['survey_id']}.json"

    blob = bucket.blob(filename)
    blob.upload_from_string(
        json.dumps(data, indent=2),
        content_type="application/json",
    )
    return filename

def load_json_file(filename):
    f = open(filename)  
    data = json.load(f)
    f.close()
    return data


data = load_json_file('test_dataset.json')
filename = store_schema(data)
print(filename)



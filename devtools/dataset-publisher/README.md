# Dataset-Publisher

This folder is a supporting tool for developers. Its purpose is to emulate the SDX process where a dataset is written to a bucket and a trigger would then call the new_dataset cloud function.

1. The `app.py` and `Dockerfile` are used to create a easy to use HTTP endpoint where a dataset can be published to with the dockerized version. It will post the dataset, write it to the bucket and then "simulate" the trigger by called a dockerized version of the cloud function that process datasets. The end result can be viewed within the firestore emulator or use the metadata or retrieve unit data endpoint.

2. Curl the endpoint directory as follows:

```
curl -X POST localhost:3006 \
-H "Content-Type: application/cloudevents+json" \
-d '{ "survey_id": "NRX",
  "period_id": "ttt",
  "form_id": "yyy",
  "title": "Which side was better?",
  "sds_schema_version": 4,
  "schema_version": "v1.0.0",
  "data": [
    {
      "ruref": "43532",
      "runame": "Pipes and Maps Ltd",
      "local_unit": [
        {
          "luref": "2012763A",
          "luname": "Maps Factory"
        },
        {
          "luref": "20127364B",
          "luname": "Pipes R Us Subsidiary"
        }
      ]
    }
 ]
}'
```


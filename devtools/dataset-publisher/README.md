# Dataset-Publisher

This folder is used for supporting tools for developers. 

### Simulate SDX publish process
Its purpose is to emulate the SDX process where a dataset is written to a bucket and a trigger then calls the new_dataset cloud function.
Curl the endpoint as follows:

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


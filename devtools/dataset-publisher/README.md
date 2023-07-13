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
  "title": "Which side was better?",
  "schema_version": "v1.0.0",
  "form_types": [
    "klk",
    "xyz",
    "tzr"
  ],
  "data": [
    {
      "identifier": "43532",
      "runame": "Pipes and Maps Ltd",
      "local_unit": [
        {
          "identifier": "2012763A",
          "luname": "Maps Factory"
        },
        {
          "identifier": "20127364B",
          "luname": "Pipes R Us Subsidiary"
        }
      ]
    }
 ]
}'
```

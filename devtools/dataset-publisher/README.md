# Dataset-Publisher

This folder is a supporting tool for developers to emulate part of the SDX process where they would write a file to the SDS bucket and an event is fired to process the newly added file. There are three parts to this tool.

1. The `main.py` and `Dockerfile` are used to create a cloud function within a docker container to simulate a publish endpoint to POST a dataset to the dataset bucket. 
2. The `manual_insert` folder has a python script and dummy JSON file, where a developer may want to create data locally and then read that file to submit to the dataset bucket. This is run via the following command within the folder `python3 publish_dataset.py` ensure that the filename in the folder matches what is within the scipt.
3. Within the `thunder-collection_Local Development - SDS-v1.json` file there is an example of a cloud event HTTP POST request that will simulate the EventArc trigger used within the project. This is useful for debugging.


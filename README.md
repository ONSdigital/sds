# Supplementary Data Service (sds)

More information on this service can be found on Confluence:

* https://confluence.ons.gov.uk/display/SDC/SDS

## Running and developing locally

To run this service locally, you will need the following:

* Python 3.11
* VirtualEnv
* Docker

### Creating, activating and deactivating a Python virtual environment

Check that you have the correct version of Python installed and then run the following commands:

```
virtualenv venv
source venv/bin/activate
```

This will create and activate the virtual environment. To deactivate the environment, run the following command:

```
deactivate
```

You can use another name for the virtual environment's directory if you wish but please add it to the `.gitignore` file.

### Installing the dependencies

Assuming that the virtual environment is activated, run the following command:

```
pip install -r requirement.txt
```

### Storing environment variables

Git is configured to ignore the `local.env` file. If you want to use another file to store environment variables 
then please add it to the `.gitignore` file. 

At the very least you need to include the following:

```
export FIRESTORE_PROJECT_ID=localhost
export FIRESTORE_EMULATOR_HOST=localhost:8200
export GOOGLE_APPLICATION_CREDENTIALS=integration_tests/google_application_credentials.json
export FIREBASE_KEYFILE_LOCATION=firebase_key.json
```

Note that the `FIRESTORE_PROJECT_ID` and `FIRESTORE_EMULATOR_HOST` environment variables match the settings in
the `docker-compose.yml` file. The other two are covered in a later subsection.

### Installing and running Firestore with Docker

In order to install the Firestore emulator, and assuming that you have Docker installed, run the following command:

```
docker-compose up -d firestore
```

And to check that the container is running:

```
docker ps
```

To subsequently stop and start the container, run the following commands respectively:

```
docker stop firestore
docker start firestore
```

To delete the container once and for all, whether currently running or not, run the following command:

```
docker-compose down
```

The `docker` commands can be run anywhere. The `docker-compose` commands should be run from the repository root so that
the `docker-compose.yml` file can be found, unless you want to explicitly specify its path.

### Connecting to the Firestore instance

The Firebase emulator instance running inside Docker needs to be configured with default application credentials. These
are found in the `google_application_credentials.json` file in the `integration_tests` directory and the instance is
made aware of them by way on the `GOOGLE_APPLICATION_CREDENTIALS` environment variable. The credentials are not meant to be secure,
see the following discussion: 

* https://groups.google.com/g/firebase-talk/c/IKo6PsXMqlQ

The credentials can be found here:

* https://github.com/firebase/firebase-admin-python/blob/master/tests/data/service_account.json

There is a `scratch.py` file that can be run to check the connection to Firestore instance. Before running the file,
copy the default application credentials to a new file...

```
cp google_application_credentials.json firebase_key.json 
```
...and make sure the `FIREBASE_KEYFILE_LOCATION` environment variable is set to point to that file.

### Running the application

Assuming the above steps have been completed, the server can be run with the following command:

```
uvicorn src.app:app --reload
```

Try the healthcheck path first:

* http://localhost/healthcheck

If running Uvicorn directly means that your debugger will not work, you can run it programmatically with the following command.

```
python src/app.py PYTHONPATH=src
```

### Linting, etc

With the virtual environment activated, run the following commands:

```
black .
isort . --profile black
flake8 src test --max-line-length=127
```

### Integration tests

Assuming that the virtual environment is activated and the Firestore emulator is running in Docker, run the following command:

```
pytest test/integration
coverage report --fail-under=90
```

## API documentation

This is auto-generated from the Python code and can be viewed when the application is running at the following URL:

* http://localhost:8000/docs

# Contact

* mike.tidman@ons.gov.uk
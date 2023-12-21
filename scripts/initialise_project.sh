#!/bin/bash

# Unset all relevant envars
echo "Unsetting all relevant env variables..."
unset API_URL
unset BUILD_ID
unset DATASET_BUCKET_NAME
unset FIRESTORE_DB_NAME
unset LOG_LEVEL
unset OAUTH_CLIENT_ID
unset OAUTH_CLIENT_NAME
unset PROJECT_ID
unset PUBLISH_DATASET_TOPIC_ID
unset PUBLISH_SCHEMA_TOPIC_ID
unset REGION
unset RETAIN_DATASET_FIRESTORE
unset SCHEMA_BUCKET_NAME

# Prompt the user for their GCP project ID and store it in a variable
echo -n "Enter your GCP project ID: "
read PROJECT_ID

echo "Setting project to ${PROJECT_ID}..."
gcloud config set project $PROJECT_ID

SSL_CERT_NAME="${PROJECT_ID}-sds-ssl-cert"

CI_STORAGE_BUCKET_NAME=$PROJECT_ID
DATASET_BUCKET_NAME=${PROJECT_ID}-sds-europe-west2-dataset
DEFAULT_HOSTNAME=$(gcloud compute ssl-certificates describe $SSL_CERT_NAME \
    --format='value(subjectAlternativeNames)')
FIRESTORE_DB_NAME=${PROJECT_ID}-sds
SCHEMA_BUCKET_NAME=${PROJECT_ID}-sds-europe-west2-schema
URL_SCHEME="https"

API_URL="${URL_SCHEME}://${DEFAULT_HOSTNAME}"

# Get the credentials file and save locally as <PROJECT_ID>-cloudbuild-sa-key.json
# Exports CLOUDBUILD_SA and GOOGLE_APPLICATION_CREDENTIALS env vars
source ./scripts/generate_key.sh

echo "Fetching oauth brand and client names..."
# Get the oauth client name (required along with key to create access tokens)
OAUTH_BRAND_NAME=$(gcloud iap oauth-brands list --format='value(name)' --limit=1 \
    --project=${PROJECT_ID})
OAUTH_CLIENT_NAME=$(gcloud iap oauth-clients list ${OAUTH_BRAND_NAME} --format='value(name)' \
    --limit=1 --project=${PROJECT_ID})

echo "Setting env variables for $PROJECT_ID project..."
export API_URL=${API_URL}
echo "API_URL=${API_URL}"
echo "GOOGLE_APPLICATION_CREDENTIALS: ${GOOGLE_APPLICATION_CREDENTIALS}"
export DATASET_BUCKET_NAME=${DATASET_BUCKET_NAME}
echo "DATASET_BUCKET_NAME=${DATASET_BUCKET_NAME}"
export FIRESTORE_DB_NAME=${FIRESTORE_DB_NAME}
echo "FIRESTORE_DB_NAME=${FIRESTORE_DB_NAME}"
# gcloud returns client name as '$OAUTH_BRAND_NAME/identityAwareProxy/OAUTH_CLIENT_ID' so we have to
# split by / and use the last part of the string here to get client id
export OAUTH_CLIENT_ID=${${OAUTH_CLIENT_NAME}##*/}
echo "OAUTH_CLIENT_ID=${OAUTH_CLIENT_ID}"
export OAUTH_CLIENT_NAME=${OAUTH_CLIENT_NAME}
echo "OAUTH_CLIENT_NAME=${OAUTH_CLIENT_NAME}"
export PROJECT_ID=${PROJECT_ID}
echo "PROJECT_ID=${PROJECT_ID}"
export SCHEMA_BUCKET_NAME=${SCHEMA_BUCKET_NAME}
echo "SCHEMA_BUCKET_NAME=${SCHEMA_BUCKET_NAME}"

echo "Project with id '${PROJECT_ID}' initialised."

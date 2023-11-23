#!/bin/bash

# Unset all relevant envars
echo "Unsetting all relevant env variables..."
unset BUILD_ID
unset CI_STORAGE_BUCKET_NAME
unset DEFAULT_HOSTNAME
unset GOOGLE_APPLICATION_CREDENTIALS
unset OAUTH_CLIENT_ID
unset PROJECT_ID

# Prompt the user for their GCP project ID and store it in a variable
read PROJECT_ID"?Enter your GCP project ID: "

SSL_CERT_NAME="${PROJECT_ID}-sds-ssl-cert"

AUTODELETE_DATASET_BUCKET_FILE="True"
CI_STORAGE_BUCKET_NAME=$PROJECT_ID
DATASET_BUCKET_NAME=ons-sds-preprod-sds-europe-west2-dataset
DEFAULT_HOSTNAME=$(gcloud compute ssl-certificates describe $SSL_CERT_NAME \
    --format='value(subjectAlternativeNames)')
FIRESTORE_DB_NAME=${PROJECT_ID}-sds
LOG_LEVEL="INFO"
PUBLISH_DATASET_TOPIC_ID="ons-sds-publish-dataset"
PUBLISH_SCHEMA_TOPIC_ID="ons-sds-publish-schema"
REGION="europe-west2"
RETAIN_DATASET_FIRESTORE="True"
SCHEMA_BUCKET_NAME=ons-sds-preprod-sds-europe-west2-schema
SURVEY_MAP_URL=https://raw.githubusercontent.com/ONSdigital/sds-schema-definitions/main/mapping/survey_map.json
URL_SCHEME="https"

echo "Setting project to $PROJECT_ID..."
gcloud config set project $PROJECT_ID

# Get the credentials file and save locally as <PROJECT_ID>-cloudbuild-sa-key.json
# Exports CLOUDBUILD_SA and GOOGLE_APPLICATION_CREDENTIALS env vars
source ./scripts/generate_key.sh

echo "Activating $CLOUDBUILD_SA service account and authenticating with docker..."
gcloud auth activate-service-account $CLOUDBUILD_SA --key-file=$GOOGLE_APPLICATION_CREDENTIALS
gcloud auth print-access-token | docker login -u oauth2accesstoken --password-stdin https://${REGION}-docker.pkg.dev

echo "Building and pushing the docker container(s)..."
# Generate a build id including a random hash to uniquely identify this build
BUILD_ID="dev-$(openssl rand -hex 4)"
docker build -t "${REGION}-docker.pkg.dev/${PROJECT_ID}/sds/sds:$BUILD_ID" -t "${REGION}-docker.pkg.dev/${PROJECT_ID}/sds/sds:latest" .
docker push "${REGION}-docker.pkg.dev/${PROJECT_ID}/sds/sds:$BUILD_ID"
docker push "${REGION}-docker.pkg.dev/${PROJECT_ID}/sds/sds:latest"

echo "Deploying the docker container(s)..."
gcloud run deploy sds --image="${REGION}-docker.pkg.dev/${PROJECT_ID}/sds/sds:${BUILD_ID}" \
    --region=$REGION --allow-unauthenticated --ingress=internal-and-cloud-load-balancing

gcloud functions deploy new-dataset-function --allow-unauthenticated --gen2 --ingress-settings=internal-and-gclb \
    --runtime=python311 --region=europe-west2 --source=./src/app/ --entry-point=new_dataset \
    --trigger-event-filters="type=google.cloud.storage.object.v1.finalized" \
    --trigger-event-filters="bucket=${DATASET_BUCKET_NAME}" \
    --set-env-vars="DATASET_BUCKET_NAME=${DATASET_BUCKET_NAME},SCHEMA_BUCKET_NAME=${SCHEMA_BUCKET_NAME},CONF=cloud-build,AUTODELETE_DATASET_BUCKET_FILE=${AUTODELETE_DATASET_BUCKET_FILE},RETAIN_DATASET_FIRESTORE=${RETAIN_DATASET_FIRESTORE},LOG_LEVEL=${LOG_LEVEL},PROJECT_ID=${PROJECT_ID},PUBLISH_SCHEMA_TOPIC_ID=${PUBLISH_SCHEMA_TOPIC_ID},PUBLISH_DATASET_TOPIC_ID=${PUBLISH_DATASET_TOPIC_ID},FIRESTORE_DB_NAME=${FIRESTORE_DB_NAME},SURVEY_MAP_URL=${SURVEY_MAP_URL}"

echo "Fetching oauth brand and client names..."
# Get the oauth client name (required along with key to create access tokens)
OAUTH_BRAND_NAME=$(gcloud iap oauth-brands list --format='value(name)' --limit=1 \
    --project=${PROJECT_ID})
OAUTH_CLIENT_NAME=$(gcloud iap oauth-clients list ${OAUTH_BRAND_NAME} --format='value(name)' \
    --limit=1)

echo "Setting env variables for $PROJECT_ID project..."
export API_URL=
export BUILD_ID=$BUILD_ID
echo "BUILD_ID: ${BUILD_ID}"
export CI_STORAGE_BUCKET_NAME=$CI_STORAGE_BUCKET_NAME
echo "CI_STORAGE_BUCKET_NAME: ${CI_STORAGE_BUCKET_NAME}"
export DEFAULT_HOSTNAME=$(gcloud compute ssl-certificates describe $SSL_CERT_NAME \
    --format='value(subjectAlternativeNames)')
echo "DEFAULT_HOSTNAME: ${DEFAULT_HOSTNAME}"
echo "GOOGLE_APPLICATION_CREDENTIALS: ${GOOGLE_APPLICATION_CREDENTIALS}"
# gcloud returns client name as '$OAUTH_BRAND_NAME/identityAwareProxy/OAUTH_CLIENT_ID' so we have to
# split by / and use the last part of the string here to get client id
export OAUTH_CLIENT_ID=${${OAUTH_CLIENT_NAME}##*/}
echo "OAUTH_CLIENT_ID: ${OAUTH_CLIENT_ID}"
export PROJECT_ID=$PROJECT_ID
echo "PROJECT_ID: ${PROJECT_ID}"
export URL_SCHEME="https"
echo "URL_SCHEME: ${URL_SCHEME}"

echo "Done!"

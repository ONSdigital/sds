#!/bin/bash

# Requests project id from user and sets up env vars and auth token
source ./scripts/initialise_project.sh

echo "Activating $CLOUDBUILD_SA service account and authenticating with docker..."
gcloud auth activate-service-account $CLOUDBUILD_SA --key-file=$GOOGLE_APPLICATION_CREDENTIALS
gcloud auth print-access-token | docker login -u oauth2accesstoken --password-stdin https://${REGION}-docker.pkg.dev

# echo "Building and pushing the docker container(s)..."
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

echo "App and cloud function deployed to ${PROJECT_ID} with build id ${BUILD_ID}."

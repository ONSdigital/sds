# Install jq for JSON parsing
apt-get -y update && apt-get install -y jq

# Get _IAC_BRANCH from argument, if empty string, set to 'main'
_IAC_BRANCH=${1:-main}

# Get SDS branch from argument
_SDS_BRANCH=${2}

echo "IaC branch: ${_IAC_BRANCH}"

# Trigger the build and store the response - dump the stdout to /dev/null to avoid cluttering the logs with the JSON response
echo "Triggering build on IaC branch: ${_IAC_BRANCH}..."
gcloud builds triggers run update-new-dataset-cloud-function --region=europe-west2 --branch=sdss-712-http-trigger-implementation --substitutions=_SDS_BRANCH=$_SDS_BRANCH --format=json | tee trigger_response.json >/dev/null

# Extract the build ID from the trigger response
_BUILD_ID=$(cat trigger_response.json | jq -r '.metadata.build.id')

# remove the trigger response file
rm trigger_response.json

echo "Triggered build with ID: ${_BUILD_ID}"

# Poll the build status every 15 seconds until it is no longer in progress to prevent the script from exiting before the build is complete
while true; do
    gcloud builds describe $_BUILD_ID --format=json --region=europe-west2 | tee build_status.json > /dev/null
    _BUILD_STATUS=$(cat build_status.json | jq -r '.status')
    # remove the build status file
    rm build_status.json
    echo "Current build status: ${_BUILD_STATUS}"
    if [[ "${_BUILD_STATUS}" == "SUCCESS" ]]; then
        echo "Build succeeded."
        break
    elif [[ "${_BUILD_STATUS}" == "FAILURE" || "${_BUILD_STATUS}" == "CANCELLED" ]]; then
        echo "Build failed or was cancelled."
        exit 1
    else
        echo "Build is still in progress..."
        sleep 15
    fi
done
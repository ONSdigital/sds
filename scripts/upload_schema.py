import json

from src.app.config.config_factory import config
from src.integration_tests.helpers.integration_helpers import (
    setup_session,
    generate_headers,
)

FILENAME = "bres_and_brs.json"
SURVEY_IDS = ["221", "241"]

session = setup_session()
headers = generate_headers()

# Get the json data
get_response = session.get(
    f"https://raw.githubusercontent.com/ONSdigital/sds-schema-definitions/main/schemas/{FILENAME}"
)

if get_response.status_code == 200:
    upload_schema = json.loads(get_response.content)
else:
    raise Exception(
        f"Request to get '{FILENAME}' data returned '{get_response.status_code}'."
    )

# Loop through survey ids and post the upload schema for each one
for survey_id in SURVEY_IDS:
    # Post the schema and check the response
    post_response = session.post(
        f"{config.API_URL}/v1/schema?survey_id={survey_id}",
        json=upload_schema,
        headers=headers,
    )

    if post_response.status_code == 200:
        print(
            f"Request to post '{FILENAME}' data with survey_id of {survey_id} successful."
        )
    else:
        raise Exception(
            f"Request to post '{FILENAME}' data with survey_id of '{survey_id}' returned '{post_response.status_code}'."
        )

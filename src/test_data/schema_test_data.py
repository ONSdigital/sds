test_guid = "test_guid"
test_survey_id = "test_survey_id"
test_published_at = "2023-04-20T12:00:00Z"

test_schema_latest_version = {
    "guid": test_guid,
    "schema_location": f"{test_survey_id}/{test_guid}.json",
    "sds_published_at": test_published_at,
    "sds_schema_version": 1,
    "survey_id": test_survey_id,
}

test_post_schema_metadata_updated_version_response = {
    "guid": test_guid,
    "schema_location": f"{test_survey_id}/{test_guid}.json",
    "sds_published_at": test_published_at,
    "sds_schema_version": 2,
    "survey_id": test_survey_id,
}

test_post_schema_metadata_first_version_response = {
    "guid": test_guid,
    "schema_location": f"{test_survey_id}/{test_guid}.json",
    "sds_published_at": test_published_at,
    "sds_schema_version": 1,
    "survey_id": test_survey_id,
}


test_post_schema_metadata_body = {
    "$schema": "test-schema",
    "$id": "test-id",
    "survey_id": test_survey_id,
    "title": "test title",
    "description": "test description",
    "schema_version": "v1.0.0",
    "sample_unit_key_field": "test_ref",
    "properties": [],
    "examples": [],
}

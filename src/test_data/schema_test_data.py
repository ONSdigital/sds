from models.schema_models import SchemaMetadata, SchemaMetadataWithoutGuid

test_guid = "test_guid"
test_survey_id = "test_survey_id"
test_published_at = "2023-04-20T12:00:00Z"
test_filename = f"{test_survey_id}/{test_guid}.json"
test_schema_version = "v1"
test_title = "test_title"

test_post_schema_metadata_first_version_response: SchemaMetadata = {
    "guid": test_guid,
    "schema_location": f"{test_survey_id}/{test_guid}.json",
    "sds_published_at": test_published_at,
    "sds_schema_version": 1,
    "survey_id": test_survey_id,
    "schema_version": test_schema_version,
    "title": test_title,
}

test_post_schema_metadata_updated_version_response: SchemaMetadata = {
    "guid": test_guid,
    "schema_location": test_filename,
    "sds_published_at": test_published_at,
    "sds_schema_version": 2,
    "survey_id": test_survey_id,
    "schema_version": test_schema_version,
    "title": test_title,
}

test_post_schema_body = {
    "$schema": "test-schema",
    "$id": "test-id",
    "title": test_title,
    "properties": {
        "schema_version": {
            "const": test_schema_version,
            "description": "Version of the schema spec",
        }
    },
}

test_post_schema_body_missing_fields = {
    "$schema": "test-schema",
    "$id": "test-id",
    "title": test_title,
}

test_post_schema_body_empty_properties = {
    "$schema": "test-schema",
    "$id": "test-id",
    "title": test_title,
    "properties": "",
}

test_post_schema_body_invalid_properties_type = {
    "$schema": "test-schema",
    "$id": "test-id",
    "title": test_title,
    "properties": [],
}

test_post_schema_body_missing_schema_version = {
    "$schema": "test-schema",
    "$id": "test-id",
    "title": test_title,
    "properties": {
        "schema_version": {},
    },
}

test_post_schema_body_invalid_schema_version = {
    "$schema": "test-schema",
    "$id": "test-id",
    "title": test_title,
    "properties": {
        "schema_version": [],
    },
}

test_post_schema_body_invalid_schema_version_const = {
    "$schema": "test-schema",
    "$id": "test-id",
    "title": test_title,
    "properties": {
        "schema_version": {
            "const": {},
        },
    },
}

test_post_schema_body_empty_schema_version_const = {
    "$schema": "test-schema",
    "$id": "test-id",
    "title": test_title,
    "properties": {
        "schema_version": {
            "const": "",
        },
    },
}

test_post_schema_body_missing_title = {
    "$schema": "test-schema",
    "$id": "test-id",
    "properties": {
        "schema_version": {
            "const": test_schema_version,
            "description": "Version of the schema spec",
        }
    },
}

test_post_schema_body_empty_title = {
    "$schema": "test-schema",
    "$id": "test-id",
    "title": "",
    "properties": {
        "schema_version": {
            "const": test_schema_version,
            "description": "Version of the schema spec",
        }
    },
}

test_schema_bucket_metadata_response: SchemaMetadataWithoutGuid = {
    "survey_id": test_survey_id,
    "schema_location": "test_location_2",
    "sds_schema_version": 2,
    "sds_published_at": "test_published_at_2",
    "title": test_title,
}

test_schema_response = {
    "title": test_title,
    "properties": {
        "schema_version": {
            "const": test_schema_version,
            "description": "Version of the schema spec",
        }
    },
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "roofing_tiles_and_slate.json",
}

test_schema_metadata_collection: list[SchemaMetadata] = [
    {
        "survey_id": "test_survey_id",
        "schema_location": "test_schema_location",
        "sds_schema_version": 1,
        "sds_published_at": "test_published_time",
        "schema_version": "v1",
        "guid": "id_0",
        "title": test_title,
    },
    {
        "survey_id": "test_survey_id",
        "schema_location": "test_schema_location",
        "sds_schema_version": 2,
        "sds_published_at": "test_published_time",
        "schema_version": "v1",
        "guid": "id_1",
        "title": test_title,
    },
]

test_list_survey_id = ["test-survey-id-1", "test-survey-id-2"]

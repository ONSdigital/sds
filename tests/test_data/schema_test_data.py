from app.models.schema_models import SchemaMetadata
from tests.test_data.shared_test_data import test_survey_id, test_guid

"""
Local variables:
"""
test_published_at = "2023-04-20T12:00:00Z"
test_schema_version = "v1"
test_title = "test_title"


"""
Test data:
"""
# unit tests - schema - test data
test_post_schema_metadata_first_version_response: SchemaMetadata = {
    "guid": test_guid,
    "schema_location": f"{test_survey_id}/{test_guid}.json",
    "sds_published_at": test_published_at,
    "sds_schema_version": 1,
    "survey_id": test_survey_id,
    "schema_version": test_schema_version,
    "title": test_title,
}

# unit tests - schema - test data
test_post_schema_metadata_updated_version_response: SchemaMetadata = {
    "guid": test_guid,
    "schema_location": f"{test_survey_id}/{test_guid}.json",
    "sds_published_at": test_published_at,
    "sds_schema_version": 2,
    "survey_id": test_survey_id,
    "schema_version": test_schema_version,
    "title": test_title,
}

# unit tests - schema - test data
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

# unit tests - schema - test data
test_post_schema_body_missing_fields = {
    "$schema": "test-schema",
    "$id": "test-id",
    "title": test_title,
}

# unit tests - schema - test data
test_post_schema_body_empty_properties = {
    "$schema": "test-schema",
    "$id": "test-id",
    "title": test_title,
    "properties": "",
}

# unit tests - schema - test data
test_post_schema_body_invalid_properties_type = {
    "$schema": "test-schema",
    "$id": "test-id",
    "title": test_title,
    "properties": [],
}

# unit tests - schema - test data
test_post_schema_body_missing_schema_version = {
    "$schema": "test-schema",
    "$id": "test-id",
    "title": test_title,
    "properties": {
        "schema_version": {},
    },
}

# unit tests - schema - test data
test_post_schema_body_invalid_schema_version = {
    "$schema": "test-schema",
    "$id": "test-id",
    "title": test_title,
    "properties": {
        "schema_version": [],
    },
}

# unit tests - schema - test data
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

# unit tests - schema - test data
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

# unit tests - schema - test data
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

# unit tests - schema - test data
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

# unit tests - schema - test data
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

# unit tests - schema - test data
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

# e2e schema integration test - test data
# unit tests - schema - test data
test_survey_id_map = [
    {"survey_id": "014", "survey_name": "Prodcom"},
    {"survey_id": "132", "survey_name": "PPI"},
    {"survey_id": "061", "survey_name": "SPPI"},
    {"survey_id": "133", "survey_name": "EPI"},
    {"survey_id": "156", "survey_name": "IPI"},
    {"survey_id": "141", "survey_name": "ASHE"},
    {"survey_id": "221", "survey_name": "BRES"},
    {"survey_id": "241", "survey_name": "BRS"},
    {"survey_id": "068", "survey_name": "Roofing Tiles"},
    {"survey_id": "071", "survey_name": "Slate"},
    {"survey_id": "066", "survey_name": "Sand & Gravel (Land Won)"},
    {"survey_id": "076", "survey_name": "Sand & Gravel (Marine Dredged)"},
]

# schema_test_data.py
invalid_survey_id = "nonexistent_survey"
invalid_data = {"invalid": "data"}
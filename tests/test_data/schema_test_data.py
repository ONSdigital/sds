import json

from app.models.schema_models import SchemaMetadata, SchemaModel
from tests.test_data.shared_test_data import test_survey_id, test_guid, test_guid_2, test_guid_3

"""
Local variables:
"""
test_published_at = "2023-04-20T12:00:00Z"
test_schema_version = "v1"
test_title = "test_title"
sub_collection_name = "schema"

"""
Unit Test data:
"""
# unit tests - schema - test data
test_schema_metadata_1 = SchemaMetadata(**{
    "guid": test_guid,
    "schema_location": f"{test_survey_id}/{test_guid}.json",
    "sds_published_at": test_published_at,
    "sds_schema_version": 1,
    "survey_id": test_survey_id,
    "schema_version": test_schema_version,
    "title": test_title,
})

test_schema_metadata_2 = SchemaMetadata(**{
    "guid": test_guid,
    "schema_location": f"{test_survey_id}/{test_guid}.json",
    "sds_published_at": test_published_at,
    "sds_schema_version": 2,
    "survey_id": test_survey_id,
    "schema_version": test_schema_version,
    "title": test_title,
})

test_schema_metadata_other = SchemaMetadata(**{
    "guid": test_guid,
    "schema_location": f"another_survey/{test_guid}.json",
    "sds_published_at": test_published_at,
    "sds_schema_version": 2,
    "survey_id": "another_survey",
    "schema_version": test_schema_version,
    "title": test_title,
})

test_schema_metadata: list[SchemaMetadata] = [
    test_schema_metadata_2,
    test_schema_metadata_1,
]

test_all_schema_metadata: list[SchemaMetadata] = [
    test_schema_metadata_other,
    test_schema_metadata_2,
    test_schema_metadata_1,
]

test_schema = {
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

test_schema_model = SchemaModel(**{
    "schema": json.dumps(test_schema)
})

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
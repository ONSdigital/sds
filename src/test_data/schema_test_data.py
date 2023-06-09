from models.schema_models import Schema, SchemaMetadata, SchemaMetadataWithoutGuid

test_guid = "test_guid"
test_survey_id = "test_survey_id"
test_published_at = "2023-04-20T12:00:00Z"
test_filename = f"{test_survey_id}/{test_guid}.json"

test_post_schema_metadata_first_version_response: SchemaMetadata = {
    "guid": test_guid,
    "schema_location": f"{test_survey_id}/{test_guid}.json",
    "sds_published_at": test_published_at,
    "sds_schema_version": 1,
    "survey_id": test_survey_id,
}

test_post_schema_metadata_updated_version_response: SchemaMetadata = {
    "guid": test_guid,
    "schema_location": test_filename,
    "sds_published_at": test_published_at,
    "sds_schema_version": 2,
    "survey_id": test_survey_id,
}


test_post_schema_metadata_body: Schema = {
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

test_schema_bucket_metadata_response: SchemaMetadataWithoutGuid = {
    "survey_id": test_survey_id,
    "schema_location": "test_location_2",
    "sds_schema_version": 2,
    "sds_published_at": "test_published_at_2",
}

test_schema_response: Schema = {
    "survey_id": test_survey_id,
    "title": "Roofing Tiles",
    "description": "Roofing Tiles",
    "schema_version": "v2.1.0",
    "sample_unit_key_field": "ruref",
    "properties": [],
    "examples": [],
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://ons.gov.uk/roofing_tiles_schema_for_data.schema.json",
}

test_schema_metadata_collection: list[SchemaMetadata] = [
    {
        "survey_id": "test_survey_id",
        "schema_location": "test_schema_location",
        "sds_schema_version": 1,
        "sds_published_at": "test_published_time",
        "guid": "id_0",
    },
    {
        "survey_id": "test_survey_id",
        "schema_location": "test_schema_location",
        "sds_schema_version": 2,
        "sds_published_at": "test_published_time",
        "guid": "id_1",
    },
]

test_schema_metadata_collection_without_guid: list[SchemaMetadataWithoutGuid] = [
    {
        "survey_id": "test_survey_id",
        "schema_location": "test_schema_location",
        "sds_schema_version": 1,
        "sds_published_at": "test_published_time",
    },
    {
        "survey_id": "test_survey_id",
        "schema_location": "test_schema_location",
        "sds_schema_version": 2,
        "sds_published_at": "test_published_time",
    },
]

test_latest_schema_without_guid: list[SchemaMetadataWithoutGuid] = [
    {
        "survey_id": "test_survey_id",
        "schema_location": "test_schema_location",
        "sds_schema_version": 2,
        "sds_published_at": "test_published_time",
    },
]

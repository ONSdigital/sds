from models import Schema


def test_store_schema(storage):
    storage.store_schema(
        Schema(
            **{
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "$id": "https://ons.gov.uk/bres_schema_for_data.schema.json",
                "survey_id": "abc",
                "title": "BRES Schema for BRES data",
                "description": "BRES data validation for use with SDS",
                "schema_version": "v1.0.0",
                "sample_unit_key_field": "ruref",
                "properties": [],
                "examples": [],
            }
        ),
        "1",
    )


def test_get_schema(storage):
    storage.get_schema("/a_file.json")

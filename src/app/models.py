from dataclasses import dataclass


@dataclass
class SchemaMetadata:
    survey_id: str
    schema_location: str
    sds_schema_version: int
    sds_published_at: str


@dataclass
class Schemas:
    supplementary_dataset_schema: dict[str, SchemaMetadata]

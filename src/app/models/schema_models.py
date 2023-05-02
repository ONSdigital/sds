from dataclasses import dataclass

from pydantic import BaseModel, Field


@dataclass
class SchemaMetadata:
    survey_id: str
    schema_location: str
    sds_schema_version: int
    sds_published_at: str


@dataclass
class SchemaMetadataWithGuid(SchemaMetadata):
    guid: str


class Schema(BaseModel):
    survey_id: str
    title: str
    description: str
    schema_version: str
    sample_unit_key_field: str
    properties: list
    examples: list
    d_schema: str = Field(alias="$schema")
    d_id: str = Field(alias="$id")

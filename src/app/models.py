from dataclasses import dataclass

from pydantic import BaseModel, Field


@dataclass
class SchemaMetadata:
    survey_id: str
    schema_location: str
    sds_schema_version: int
    sds_published_at: str


@dataclass
class Schemas:
    supplementary_dataset_schema: dict[str, SchemaMetadata]


class Schema(BaseModel):
    survey_id: str
    title: str
    description: str
    schemaVersion: str
    schemaVersionDate: str
    properties: dict
    examples: list
    d_schema: str = Field(alias="$schema")
    d_id: str = Field(alias="$id")

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
    schema_version: str
    sample_unit_key_field: str
    properties: list
    examples: list
    d_schema: str = Field(alias="$schema")
    d_id: str = Field(alias="$id")


@dataclass
class DatasetMetadata:
    dataset_id: str
    survey_id: str
    period_id: str
    title: str
    sds_schema_version: int
    sds_published_at: str
    total_reporting_units: int
    schema_version: str
    sds_dataset_version: int
    filename: str


@dataclass
class Datasets:
    supplementary_dataset: dict[str, DatasetMetadata]

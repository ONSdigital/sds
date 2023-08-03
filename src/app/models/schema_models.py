from dataclasses import dataclass
from typing import Optional

from pydantic import BaseModel, Field


@dataclass
class SchemaMetadataWithoutGuid:
    survey_id: str
    schema_location: str
    sds_schema_version: int
    sds_published_at: str


@dataclass
class SchemaMetadata(SchemaMetadataWithoutGuid):
    guid: str

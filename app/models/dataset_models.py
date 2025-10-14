from dataclasses import dataclass
from typing import Optional


@dataclass
class DatasetMetadataWithoutId:
    survey_id: str
    period_id: str
    form_types: list[str]
    sds_published_at: str
    total_reporting_units: int
    sds_dataset_version: int
    filename: str
    title: str | None


@dataclass
class DatasetMetadata:
    dataset_id: str
    survey_id: str
    period_id: str
    form_types: list[str]
    sds_published_at: str
    total_reporting_units: int
    sds_dataset_version: int
    filename: str
    title: Optional[str] = None


@dataclass
class UnitDataset:
    dataset_id: str
    survey_id: str
    period_id: str
    form_types: list[str]
    data: object


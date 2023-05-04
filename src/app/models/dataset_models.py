from dataclasses import dataclass


@dataclass
class DatasetMetadataWithoutId:
    survey_id: str
    period_id: str
    title: str
    sds_schema_version: int
    sds_published_at: str
    total_reporting_units: int
    schema_version: str
    sds_dataset_version: int
    filename: str
    form_type: str


@dataclass
class DatasetMetadata(DatasetMetadataWithoutId):
    dataset_id: str


@dataclass
class RawDatasetMetadata:
    dataset_id: str
    survey_id: str
    period_id: str
    title: str
    sds_schema_version: str
    schema_version: str
    form_type: str


@dataclass
class RawDatasetWithMetadata(RawDatasetMetadata):
    data: list[object]


@dataclass
class UnitDataset:
    dataset_id: str
    survey_id: str
    period_id: str
    sds_schema_version: int
    schema_version: str
    form_type: str
    data: object

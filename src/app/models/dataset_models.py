from dataclasses import dataclass


@dataclass
class DatasetMetadataWithoutId:
    survey_id: str
    period_id: str
    form_types: list[str]
    title: str
    sds_published_at: str
    total_reporting_units: int
    schema_version: str
    sds_dataset_version: int
    filename: str


@dataclass
class DatasetMetadata(DatasetMetadataWithoutId):
    dataset_id: str


@dataclass
class UnitDatasetWithoutData:
    dataset_id: str
    survey_id: str
    period_id: str
    form_types: list[str]
    title: str
    schema_version: str


@dataclass
class UnitDataset:
    dataset_id: str
    survey_id: str
    period_id: str
    schema_version: str
    form_types: list[str]
    data: object


@dataclass
class DatasetPublishResponse:
    status: str
    message: str

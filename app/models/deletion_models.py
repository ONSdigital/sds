from dataclasses import dataclass


@dataclass
class DeleteMetadata:
    dataset_guid: str
    period_id: str
    survey_id: str
    sds_dataset_version: str
    status: str
    mark_deleted_at: str
    deleted_at: str

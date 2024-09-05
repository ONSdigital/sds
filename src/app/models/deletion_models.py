from dataclasses import dataclass


@dataclass
class DeleteMetadata:
    dataset_guid: str
    status: str
    mark_deleted_at: str
    deleted_at: str

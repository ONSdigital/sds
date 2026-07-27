from dataclasses import dataclass


@dataclass
class CollectionExerciseEndData:
    survey_id: str
    period_id: str
    dataset_guid: str | None = None

@dataclass
class CollectionExerciseEndResponse:
    message: str
    dataset_delete_guid_list: list[str] | None = None

from dataclasses import dataclass


@dataclass
class CollectionExerciseEndData:
    survey_id: str
    period_id: str
    dataset_guid: str | None = None

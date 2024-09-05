from dataclasses import dataclass


@dataclass
class CollectionExerciseEndData:
    dataset_guid: str
    survey_id: str
    period: str

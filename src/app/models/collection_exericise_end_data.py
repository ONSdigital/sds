from dataclasses import dataclass
from typing import Optional


@dataclass
class CollectionExerciseEndData:
    survey_id: str
    period: str
    dataset_guid: Optional[str] = ""

from dataclasses import dataclass


@dataclass
class CollectionExerciseEndDataRaw:
    surveyRef: str
    period: str
    endDate: str
    SupplementaryDatasetId: str | None = None

@dataclass
class CollectionExerciseEndData:
    survey_id: str
    period_id: str
    end_date: str
    dataset_guid: str | None = None

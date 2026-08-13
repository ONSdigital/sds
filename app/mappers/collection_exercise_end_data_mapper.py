from app.models.collection_exericise_end_data import CollectionExerciseEndData, CollectionExerciseEndDataRaw


class CollectionExerciseEndDataMapper:
    @staticmethod
    def map(raw_data: CollectionExerciseEndDataRaw) -> CollectionExerciseEndData:
        return CollectionExerciseEndData(
            survey_id=raw_data.surveyRef,
            period_id=raw_data.period,
            end_date=raw_data.endDate,
            dataset_guid=raw_data.SupplementaryDatasetId,
        )

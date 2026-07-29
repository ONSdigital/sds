from app.mappers.collection_exercise_end_data_mapper import CollectionExerciseEndDataMapper
from app.models.collection_exericise_end_data import CollectionExerciseEndDataRaw, CollectionExerciseEndData


def test_collection_exercise_end_data_mapper():
    """
    Test the CollectionExerciseEndDataMapper class.
    """
    mapper = CollectionExerciseEndDataMapper()

    raw_data = CollectionExerciseEndDataRaw(
        surveyRef="test_survey",
        period="test_period",
        endDate="test_end_date",
        SupplementaryDatasetId="test_dataset_guid"
    )

    expected_output = CollectionExerciseEndData(
        survey_id="test_survey",
        period_id="test_period",
        end_date="test_end_date",
        dataset_guid="test_dataset_guid"
    )

    result = mapper.map(raw_data)

    assert result == expected_output
    assert isinstance(result, CollectionExerciseEndData)

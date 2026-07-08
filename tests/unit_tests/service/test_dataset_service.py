from unittest.mock import MagicMock, call

from app.models.collection_exericise_end_data import CollectionExerciseEndData
from app.models.deletion_models import DeleteMetadata
from app.services.dataset_service import DatasetService
from tests.test_data import dataset_test_data


def test_get_dataset_metadata_collection_calls_storage_repository():
    """
    When dataset metadata for a survey/period is requested, DatasetService must
    delegate to dataset storage repository and return the repository result.
    """
    dataset_storage_repository = MagicMock()
    dataset_deletion_repository = MagicMock()
    dataset_storage_repository.get_metadata.return_value = dataset_test_data.test_dataset_metadata

    service = DatasetService(
        dataset_deletion_repository=dataset_deletion_repository,
        dataset_storage_repository=dataset_storage_repository,
    )

    result = service.get_dataset_metadata_collection(
        survey_id=dataset_test_data.test_survey_id,
        period_id=dataset_test_data.test_period_id,
    )

    assert result == dataset_test_data.test_dataset_metadata
    dataset_storage_repository.get_metadata.assert_called_once_with(
        dataset_test_data.test_survey_id,
        dataset_test_data.test_period_id,
    )


def test_get_all_dataset_metadata_collection_calls_storage_repository():
    """
    When all dataset metadata is requested, DatasetService must delegate to
    dataset storage repository and return the repository result.
    """
    dataset_storage_repository = MagicMock()
    dataset_deletion_repository = MagicMock()
    dataset_storage_repository.get_all_metadata.return_value = dataset_test_data.test_all_dataset_metadata

    service = DatasetService(
        dataset_deletion_repository=dataset_deletion_repository,
        dataset_storage_repository=dataset_storage_repository,
    )

    result = service.get_all_dataset_metadata_collection()

    assert result == dataset_test_data.test_all_dataset_metadata
    dataset_storage_repository.get_all_metadata.assert_called_once_with()


def test_get_unit_supplementary_data_calls_storage_repository():
    """
    When unit supplementary data is requested, DatasetService must delegate to
    dataset storage repository and return the repository result.
    """
    dataset_storage_repository = MagicMock()
    dataset_deletion_repository = MagicMock()
    dataset_storage_repository.get_unit_supplementary_data.return_value = dataset_test_data.test_unit_data

    service = DatasetService(
        dataset_deletion_repository=dataset_deletion_repository,
        dataset_storage_repository=dataset_storage_repository,
    )

    result = service.get_unit_supplementary_data(
        dataset_id=dataset_test_data.test_guid,
        identifier=dataset_test_data.identifier,
    )

    assert result == dataset_test_data.test_unit_data
    dataset_storage_repository.get_unit_supplementary_data.assert_called_once_with(
        dataset_test_data.test_guid,
        dataset_test_data.identifier,
    )


def test_get_unit_supplementary_data_returns_none_when_not_found():
    """
    When unit supplementary data does not exist for the requested identifier,
    DatasetService must return None.
    """
    dataset_storage_repository = MagicMock()
    dataset_deletion_repository = MagicMock()
    dataset_storage_repository.get_unit_supplementary_data.return_value = None

    service = DatasetService(
        dataset_deletion_repository=dataset_deletion_repository,
        dataset_storage_repository=dataset_storage_repository,
    )

    result = service.get_unit_supplementary_data(
        dataset_id=dataset_test_data.test_guid,
        identifier=dataset_test_data.identifier,
    )

    assert result is None
    dataset_storage_repository.get_unit_supplementary_data.assert_called_once_with(
        dataset_test_data.test_guid,
        dataset_test_data.identifier,
    )


def test_end_collection_exercise_marks_all_matching_datasets_for_deletion():
    """
    When a collection exercise end event includes dataset_guid, DatasetService
    must retrieve metadata for the survey/period and mark each dataset version
    for deletion.
    """
    dataset_storage_repository = MagicMock()
    dataset_deletion_repository = MagicMock()
    dataset_storage_repository.get_metadata.return_value = dataset_test_data.test_dataset_metadata

    service = DatasetService(
        dataset_deletion_repository=dataset_deletion_repository,
        dataset_storage_repository=dataset_storage_repository,
    )

    service.end_collection_exercise(dataset_test_data.test_data_collection_end)

    dataset_storage_repository.get_metadata.assert_called_once_with(
        dataset_test_data.test_survey_id,
        dataset_test_data.test_period_id,
    )

    expected_mark_for_deletion = [
        DeleteMetadata(
            dataset_guid=dataset_test_data.test_dataset_metadata_2.dataset_id,
            period_id=dataset_test_data.test_period_id,
            survey_id=dataset_test_data.test_survey_id,
            sds_dataset_version=dataset_test_data.test_dataset_metadata_2.sds_dataset_version,
            status="Pending",
            mark_deleted_at="2023-04-20T12:00:00Z",
            deleted_at="n/a",
        ),
        DeleteMetadata(
            dataset_guid=dataset_test_data.test_dataset_metadata_1.dataset_id,
            period_id=dataset_test_data.test_period_id,
            survey_id=dataset_test_data.test_survey_id,
            sds_dataset_version=dataset_test_data.test_dataset_metadata_1.sds_dataset_version,
            status="Pending",
            mark_deleted_at="2023-04-20T12:00:00Z",
            deleted_at="n/a",
        ),
    ]

    dataset_deletion_repository.mark_dataset_for_deletion.assert_has_calls(
        [call(delete_metadata) for delete_metadata in expected_mark_for_deletion]
    )
    assert dataset_deletion_repository.mark_dataset_for_deletion.call_count == 2


def test_end_collection_exercise_with_missing_dataset_guid_does_not_mark_for_deletion():
    """
    When a collection exercise end event does not include dataset_guid,
    DatasetService must not mark any dataset for deletion.
    """
    dataset_storage_repository = MagicMock()
    dataset_deletion_repository = MagicMock()

    service = DatasetService(
        dataset_deletion_repository=dataset_deletion_repository,
        dataset_storage_repository=dataset_storage_repository,
    )

    service.end_collection_exercise(dataset_test_data.test_data_collection_end_missing_id)

    dataset_storage_repository.get_metadata.assert_not_called()
    dataset_deletion_repository.mark_dataset_for_deletion.assert_not_called()


def test_end_collection_exercise_with_none_dataset_guid_does_not_mark_for_deletion():
    """
    When a collection exercise end event includes dataset_guid=None,
    DatasetService must not mark any dataset for deletion.
    """
    dataset_storage_repository = MagicMock()
    dataset_deletion_repository = MagicMock()

    service = DatasetService(
        dataset_deletion_repository=dataset_deletion_repository,
        dataset_storage_repository=dataset_storage_repository,
    )

    collection_exercise_end_data = CollectionExerciseEndData(
        survey_id=dataset_test_data.test_survey_id,
        period_id=dataset_test_data.test_period_id,
        dataset_guid=None,
    )

    service.end_collection_exercise(collection_exercise_end_data)

    dataset_storage_repository.get_metadata.assert_not_called()
    dataset_deletion_repository.mark_dataset_for_deletion.assert_not_called()


def test_end_collection_exercise_with_no_matching_metadata_marks_nothing_for_deletion():
    """
    When collection exercise end event includes dataset_guid but no dataset
    metadata exists for the survey/period, DatasetService must not mark
    anything for deletion.
    """
    dataset_storage_repository = MagicMock()
    dataset_deletion_repository = MagicMock()
    dataset_storage_repository.get_metadata.return_value = []

    service = DatasetService(
        dataset_deletion_repository=dataset_deletion_repository,
        dataset_storage_repository=dataset_storage_repository,
    )

    service.end_collection_exercise(dataset_test_data.test_data_collection_end)

    dataset_storage_repository.get_metadata.assert_called_once_with(
        dataset_test_data.test_survey_id,
        dataset_test_data.test_period_id,
    )
    dataset_deletion_repository.mark_dataset_for_deletion.assert_not_called()

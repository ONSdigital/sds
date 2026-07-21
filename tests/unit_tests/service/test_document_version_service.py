import pytest

from app.models.schema_models import SchemaMetadata
from app.models.dataset_models import DatasetMetadataWithoutId
from app.services.shared.document_version_service import DocumentVersionService
from tests.test_data import schema_test_data


def test_calculate_survey_version_returns_1_when_no_existing_metadata():
    """
    When no existing metadata is provided, the next version must be 1.
    """
    result = DocumentVersionService.calculate_survey_version(None, "sds_schema_version")

    assert result == 1


def test_calculate_survey_version_increments_schema_version():
    """
    When existing schema metadata is provided, the next version must be current + 1.
    """
    result = DocumentVersionService.calculate_survey_version(
        schema_test_data.test_schema_metadata_1, "sds_schema_version"
    )

    assert result == schema_test_data.test_schema_metadata_1.sds_schema_version + 1


def test_calculate_survey_version_raises_runtime_error_when_version_key_missing():
    """
    When the metadata does not contain the specified version key, a RuntimeError must be raised.
    """
    metadata_without_key = SchemaMetadata(
        guid="test",
        schema_location="test",
        sds_published_at="2023-04-20T12:00:00Z",
        sds_schema_version=1,
        survey_id="test",
        schema_version="v1",
        title="test",
    )

    with pytest.raises(RuntimeError, match="Document must contain version key"):
        DocumentVersionService.calculate_survey_version(metadata_without_key, "sds_dataset_version")


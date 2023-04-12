import logging
from unittest.mock import MagicMock


def test_get_unit_supplementary_data_logs_message_on_start(caplog, client):
    """
    A message should be logged when the get_unit_supplementary_data endpoint is hit
    """
    caplog.set_level(logging.INFO)

    unit_id = "test-unit-id"
    dataset_id = "test-dataset-id"
    client.get(f"/v1/unit_data?dataset_id={dataset_id}&unit_id={unit_id}")

    assert len(caplog.records) == 2
    assert caplog.records[0].message == "Getting unit supplementary data..."


def test_get_unit_supplementary_data_200_is_logged(caplog, client, database):
    """
    When the unit supplementary data is retrieved successfully a success message is logged.
    """
    caplog.set_level(logging.INFO)

    mock_database_get_unit_supplementary_data = MagicMock()
    mock_database_get_unit_supplementary_data.return_value = {"success": True}
    database.get_unit_supplementary_data = mock_database_get_unit_supplementary_data

    unit_id = "55e64129-6acd-438b-a23a-3cf9524ab912"
    dataset_id = "55e64129-6acd-438b-a23a-3cf9524ab912"
    response = client.get(f"/v1/unit_data?dataset_id={dataset_id}&unit_id={unit_id}")

    assert response.status_code == 200
    assert len(caplog.records) == 2
    assert caplog.records[1].message == "Unit supplementary data successfully outputted"


def test_get_unit_supplementary_data_404_error_is_logged(caplog, client, database):
    """
    When the unit supplementary data is retrieved successfully a success message is logged.
    """
    caplog.set_level(logging.ERROR)

    mock_database_get_unit_supplementary_data = MagicMock()
    mock_database_get_unit_supplementary_data.return_value = None
    database.get_unit_supplementary_data = mock_database_get_unit_supplementary_data

    unit_id = "test-unit-id"
    dataset_id = "test-dataset-id"
    response = client.get(f"/v1/unit_data?dataset_id={dataset_id}&unit_id={unit_id}")

    assert response.status_code == 404
    assert len(caplog.records) == 1
    assert caplog.records[0].message == "Item not found"

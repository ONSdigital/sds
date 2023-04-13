import logging
from unittest.mock import MagicMock

test_dataset_id = "test_dataset_id"
test_unit_id = "test_unit_id"

def test_get_unit_supplementary_data_200_is_logged(caplog, client, database):
    """
    There should be a log at the start of the function and another when the unit supplementary data is retrieved
    successfully.
    """
    caplog.set_level(logging.INFO)

    mock_database_get_unit_supplementary_data = MagicMock()
    mock_database_get_unit_supplementary_data.return_value = {"success": True}
    database.get_unit_supplementary_data = mock_database_get_unit_supplementary_data

    response = client.get(f"/v1/unit_data?dataset_id={test_dataset_id}&unit_id={test_unit_id}")

    assert response.status_code == 200
    assert len(caplog.records) == 2
    assert caplog.records[0].message == "Getting unit supplementary data..."
    assert caplog.records[1].message == "Unit supplementary data successfully outputted"


def test_get_unit_supplementary_data_input_data_debug_logged(caplog, client, database):
    """
    There should be a debug log containing the input data.
    """
    caplog.set_level(logging.DEBUG)

    mock_database_get_unit_supplementary_data = MagicMock()
    mock_database_get_unit_supplementary_data.return_value = {"test": 'data'}
    database.get_unit_supplementary_data = mock_database_get_unit_supplementary_data

    client.get(f"/v1/unit_data?dataset_id={test_dataset_id}&unit_id={test_unit_id}")

    assert (
        caplog.records[2].message
        == "Input data: dataset_id=test_dataset_id, unit_id=test_unit_id"
    )
    assert (
            caplog.records[4].message
            == "Unit supplementary data: {'test': 'data'}"
    )


def test_get_unit_supplementary_data_404_error_is_logged(caplog, client, database):
    """
    When there is a 404 the error is logged.
    """
    caplog.set_level(logging.ERROR)

    mock_database_get_unit_supplementary_data = MagicMock()
    mock_database_get_unit_supplementary_data.return_value = None
    database.get_unit_supplementary_data = mock_database_get_unit_supplementary_data

    response = client.get(f"/v1/unit_data?dataset_id={test_dataset_id}&unit_id={test_unit_id}")

    assert response.status_code == 404
    assert len(caplog.records) == 1
    assert caplog.records[0].message == "Item not found"

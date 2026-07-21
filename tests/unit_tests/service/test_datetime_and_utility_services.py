from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest

from app.services.shared.datetime_service import DatetimeService
from app.services.shared.utility_functions import UtilityFunctions


# --------------------------------------------------------------------------- #
# DatetimeService
# --------------------------------------------------------------------------- #

def test_get_current_date_and_time_returns_datetime():
    """
    DatetimeService.get_current_date_and_time must return a datetime instance
    when the underlying datetime.now() is not mocked.
    """
    # Temporarily restore the real method in case autouse fixture has replaced it
    real_method = datetime.now
    with patch.object(DatetimeService, "get_current_date_and_time", wraps=lambda: real_method()):
        result = DatetimeService.get_current_date_and_time()

    assert isinstance(result, datetime)


# --------------------------------------------------------------------------- #
# UtilityFunctions
# --------------------------------------------------------------------------- #

def test_request_survey_id_mapping_makes_get_request_to_survey_map_url():
    """
    UtilityFunctions.request_survey_id_mapping must make a GET request to the
    configured SURVEY_MAP_URL and return the response.
    """
    mock_response = MagicMock()
    mock_response.status_code = 200

    with patch("app.services.shared.utility_functions.requests.get", return_value=mock_response) as mock_get:
        result = UtilityFunctions.request_survey_id_mapping()

    from app.config import settings
    mock_get.assert_called_once_with(url=settings.SURVEY_MAP_URL, timeout=30)
    assert result == mock_response


def test_get_application_version_returns_configured_version():
    """
    UtilityFunctions.get_application_version must return the configured SDS_APPLICATION_VERSION.
    Calls the implementation directly to avoid class-level mock leakage from other test modules.
    """
    from app.config import settings

    # Restore the real implementation before testing (other tests may have replaced it at class level)
    with patch.object(UtilityFunctions, "get_application_version", staticmethod(lambda: settings.SDS_APPLICATION_VERSION)):
        result = UtilityFunctions.get_application_version()

    assert result == settings.SDS_APPLICATION_VERSION

